# Fast Queue 🚀

**Fast Queue** é uma plataforma de alta performance desenvolvida para streamers que desejam monetizar a interação com seu público através de filas de espera pagas via Pix. O sistema garante integridade financeira, baixa latência e atualizações em tempo real.

## 🏗️ Arquitetura do Sistema

O projeto segue o padrão de **Microsserviços** e **Arquitetura Baseada em Eventos (EDA)**, utilizando o padrão **CQRS** para separar as operações de escrita (Postgres) das operações de leitura e busca (Elasticsearch).

### Componentes Principais:
1.  **Queue Service (Python/FastAPI):** Core do sistema. Gerencia criação de filas, lógica de entrada e regras de negócio.
2.  **Payment Service (Python/FastAPI):** Integração com AbacatePay (Pix). Gerencia transações e processa reembolsos.
3.  **Search Service (Python/FastAPI):** Engine de busca ultra-rápida que consome dados pré-processados.
4.  **Frontend (Vue 3 + Pinia):** Interface reativa com sincronização em tempo real via Firebase/Firestore.

---

## 🛠️ Stack Tecnológica

-   **Backend:** Python 3.12, FastAPI, SQLAlchemy (Async), Pydantic v2.
-   **Frontend:** Vue 3, Vite, Tailwind CSS v4, Pinia.
-   **Bancos de Dados:** 
    -   **PostgreSQL:** Persistência ACID (Verdade absoluta).
    -   **Redis:** Cache, Locks Atômicos e Rate Limiting.
    -   **Cloud Firestore:** Projeção de dados em tempo real para o cliente.
-   **Engenharia de Dados:**
    -   **Apache Kafka:** Mensageria assíncrona entre serviços.
    -   **Debezium:** Change Data Capture (CDC) para sincronização automática entre Postgres e Search Engine.
    -   **Elasticsearch:** Busca Full-text e Fuzzy search.
-   **Infraestrutura:** Docker, Nginx (Gateway Local), Google Cloud Run (Serverless), Cloud SQL, Firebase Hosting.

---

## 🛰️ Pipeline de Dados (O Pulo do Gato)

Para garantir que a busca nunca fique desatualizada sem onerar a API principal, implementamos um pipeline de CDC:
1.  A API grava no **PostgreSQL**.
2.  O **Debezium** monitora o log binário do banco.
3.  As alterações são publicadas no **Kafka**.
4.  Um **Search Worker** consome o Kafka e popula o **Elasticsearch**.
5.  O resultado é uma busca instantânea com tolerância a erros de digitação.

---

## 🚀 Como Executar (Ambiente Local)

### Pré-requisitos:
- Docker e Docker Compose.
- Node.js e Python 3.12 instalados.
- Firebase CLI instalado.

### 1. Iniciar Infraestrutura e Emuladores:
```bash
# Na raiz, inicia Postgres, Kafka, ES e Redis
docker-compose up -d

# Inicia o Firebase Emulator Suite
firebase emulators:start
```

### 2. Preparar Bancos de Dados:
```bash
# Criar tabelas no Queue Service
docker exec -it queue-service python src/create_tables.py

# Criar tabelas no Payment Service
docker exec -it payment-service python src/create_tables.py

# Ativar o conector do Debezium
./scripts/setup-debezium-local.sh
```

---

## 🛡️ Qualidade e Testes

O sistema conta com uma suite de testes automatizados usando **Pytest** com **Mocks** de infraestrutura (Kafka/Firestore) e banco em memória (**SQLite**).

```bash
# Executar testes do Queue Service
cd services/queue-service
export ENV=testing
python3 -m pytest -v
```

---

## 🌐 Deploy (Produção)

O deploy é automatizado via script shell e utiliza o ecossistema **GCP**:
-   **Microsserviços:** Google Cloud Run.
-   **Banco de Dados:** Cloud SQL.
-   **Ponto de Entrada Único:** Firebase Hosting com Rewrites (Gateway).
-   **Domínio:** `fastq.site` com SSL gerenciado.

---

## 🔐 Variáveis de Ambiente (.env)

O sistema exige as seguintes chaves em cada serviço:
- `DATABASE_URL`: Conexão com Postgres.
- `KAFKA_SERVER`: Endereço do broker.
- `REDIS_URL`: Endereço do cache.
- `FIREBASE_ADMIN_SDK_PATH`: Caminho do JSON de Service Account.
- `ALLOWED_ORIGINS`: Lista de domínios permitidos pelo CORS.

---
**Desenvolvido como projeto de Arquitetura de Software Sênior por Marcos E. da Silva.**