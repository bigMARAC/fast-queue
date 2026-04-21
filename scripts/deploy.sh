#!/bin/bash

if [ -f .env ]; then
    export $(echo $(cat .env | sed 's/#.*//' | xargs) | envsubst)
else
    echo "❌ Arquivo .env não encontrado!"
    exit 1
fi

REPO_URL="$REGION-docker.pkg.dev/$PROJECT_ID/fast-queue"
FULL_DB_URL="postgresql+asyncpg://$DB_USER:$DB_PASS@$IP_DB:5432/$DB_NAME"

echo "🚀 Iniciando Deploy do Ecossistema Fast Queue..."

gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet

# --- QUEUE SERVICE ---
echo "📦 Construindo Queue Service..."
docker build -t "$REPO_URL/queue-service:v1" -f services/queue-service/Dockerfile .
docker push "$REPO_URL/queue-service:v1"
gcloud run deploy queue-service \
  --image "$REPO_URL/queue-service:v1" \
  --region "$REGION" \
  --vpc-connector "$VPC_CONNECTOR" \
  --vpc-egress private-ranges-only \
  --set-env-vars "DATABASE_URL=$FULL_DB_URL,REDIS_URL=redis://$IP_VM_INFRA:6379,KAFKA_SERVER=$IP_VM_INFRA:9092,ALLOWED_ORIGINS=$ALLOWED_ORIGINS,PAYMENT_SERVICE_URL=$PAYMENT_SERVICE_URL,FIREBASE_ADMIN_SDK_PATH=/app/firebase.json,ENV=production" \
  --allow-unauthenticated --quiet

# --- PAYMENT SERVICE ---
echo "📦 Construindo Payment Service..."
docker build -t "$REPO_URL/payment-service:v1" -f services/payment-service/Dockerfile .
docker push "$REPO_URL/payment-service:v1"
gcloud run deploy payment-service \
  --image "$REPO_URL/payment-service:v1" \
  --region "$REGION" \
  --vpc-connector "$VPC_CONNECTOR" \
  --vpc-egress private-ranges-only \
  --set-env-vars "DATABASE_URL=$FULL_DB_URL,KAFKA_SERVER=$IP_VM_INFRA:9092,ALLOWED_ORIGINS=$ALLOWED_ORIGINS,ENV=production" \
  --allow-unauthenticated --quiet

# --- SEARCH SERVICE ---
echo "📦 Construindo Search Service..."
docker build -t "$REPO_URL/search-service:v1" -f services/search-service/Dockerfile .
docker push "$REPO_URL/search-service:v1"
gcloud run deploy search-service \
  --image "$REPO_URL/search-service:v1" \
  --region "$REGION" \
  --vpc-connector "$VPC_CONNECTOR" \
  --vpc-egress private-ranges-only \
  --set-env-vars "ELASTICSEARCH_URL=http://$IP_VM_INFRA:9200,KAFKA_SERVER=$IP_VM_INFRA:9092,ALLOWED_ORIGINS=$ALLOWED_ORIGINS,ENV=production" \
  --allow-unauthenticated --quiet

echo "✅ DEPLOY FINALIZADO COM SUCESSO!"