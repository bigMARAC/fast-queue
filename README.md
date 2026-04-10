# Fast Queue 🚀

O **Fast Queue** é uma plataforma de alta performance desenvolvida para streamers que desejam monetizar a interação com seu público através de filas de espera pagas para jogar em conjunto.

## 📌 Visão Geral do Projeto

Este sistema foi projetado para suportar alta carga (picos de tráfego durante lives) com consistência de dados rigorosa e atualizações em tempo real.

---

## 1. Requisitos do Sistema

### Funcionais (RF)
- **RF01 (Gestão de Fila):** Streamers podem criar, configurar valores de entrada e fechar filas.
- **RF02 (Visualização):** Viewers podem visualizar a fila atual e sua posição em tempo real.
- **RF03 (Pagamento):** Integração com gateways de pagamento para entrada na fila.
- **RF04 (Ações do Streamer):** O streamer pode "chamar" o próximo viewer ou "recusar" um participante.
- **RF05 (Estorno):** Reembolso automático caso o streamer recuse a entrada ou a fila seja cancelada.
- **RF06 (Busca):** Busca global de streamers com filas ativas.

### Não Funcionais (RNF)
- **RNF01 (Disponibilidade):** Alta disponibilidade (99.9%) garantida por arquitetura em microsserviços.
- **RNF02 (Latência):** Atualizações de status da fila em < 200ms via Firebase Realtime/Firestore.
- **RNF03 (Escalabilidade):** Suporte a picos de 5.000+ RPS (Requests Per Second) usando Load Balancers e Cache.
- **RNF04 (Integridade):** Garantia de transações ACID para fluxos financeiros.
- **RNF05 (Auditabilidade):** Logs distribuídos e rastreamento de transações de ponta a ponta.

---

## 2. Estimativas de Carga (Back-of-the-envelope)

- **DAU (Usuários Ativos Diários):** ~100.000 usuários.
- **Carga Média:** 12 RPS.
- **Carga de Pico:** 2.000 a 5.000 RPS (Início de lives ou raids).
- **Armazenamento:** Estimativa de 75GB/ano para logs e transações financeiras.
- **Cache:** Necessidade de cache de alta performance (Redis) para controle de concorrência em tempo real.

---

## 3. Entidades Principais (Modelo de Domínio)

- **User (Streamer/Viewer):** Dados cadastrais, saldo e credenciais (Firebase Auth).
- **Queue (Fila):** Configurações, valor de entrada, status (Aberta/Fechada) e dono (Streamer).
- **QueueEntry (Ticket):** Registro de entrada de um viewer, posição na fila e status (Pendente, Aguardando, Chamado, Recusado).
- **Transaction:** Registro financeiro de débitos, créditos e reembolsos vinculados ao Gateway.

---

## 4. Stack Tecnológica e Arquitetura de Dados

A arquitetura utiliza o padrão de **Microsserviços** rodando em **GCP (Google Cloud Platform)**:

- **Linguagem:** Python (FastAPI/Flask)
- **Banco de Dados Relacional (Escrita/ACID):** Cloud SQL (PostgreSQL).
- **Banco de Dados NoSQL (Real-time):** Firestore (para sincronização instantânea com o frontend).
- **Cache e Locks:** Cloud Memorystore (Redis).
- **Busca Avançada:** Elasticsearch (alimentado via Debezium/Kafka através de CDC - Change Data Capture).
- **Mensageria e Eventos:** Apache Kafka (para comunicação assíncrona entre serviços e processos de reembolso).
- **Infraestrutura:** Google Kubernetes Engine (GKE), Load Balancer e Cloud Logging.

---

## 5. Design de API (Principais Endpoints)

### Queue Management Service
- `POST /v1/queues` - Criação de fila.
- `PATCH /v1/queues/{id}` - Alterar status da fila.
- `GET /v1/queues/{id}/next` - Chamar próximo participante.
- `POST /v1/queues/{id}/reject/{viewer_id}` - Recusar participante (dispara evento de estorno).

### Player Experience Service
- `GET /v1/search/streamers` - Busca full-text de filas/streamers ativos (Elasticsearch).
- `GET /v1/queues/{id}` - Consultar detalhes da fila.
- `POST /v1/queues/{id}/join` - Manifestar interesse de entrada e gerar Checkout.

### Payment Service
- `POST /v1/payments/webhook` - Callback do gateway de pagamento.
- `GET /v1/payments/status/{tx_id}` - Verificar status de uma transação.

---

## 🚀 Como Executar (Em breve)
*Documentação em desenvolvimento...*

---
**Desenvolvido por Marcos E. da Silva**
