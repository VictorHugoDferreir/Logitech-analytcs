# 🚚 LogiTech Analytics — Pipeline de Ingestão e Análise Operacional

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15--alpine-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)
![ETL](https://img.shields.io/badge/Pipeline-ETL-green)

Projeto end-to-end de Engenharia e Análise de Dados voltado ao domínio de Logística e Controle de Qualidade (**LogiTech**). O projeto simula a ingestão de dados operacionais a partir de planilhas Excel locais, carga estruturada em banco relacional PostgreSQL via Docker e geração de insights estratégicos via consultas SQL analíticas.

---

## 📐 Arquitetura da Solução

```text
[ Planilha Excel / CSVs ]
  │  (data/dados_logisticos.xlsx)
  ▼
[ Pipeline ETL em Python ] 
  │  (scripts/ingest.py — Pandas & SQLAlchemy)
  ▼
[ PostgreSQL 15 em Docker ] 
  │  (Porta 5432 / Volume pgdata)
  ▼
[ Consultas SQL Analíticas ] 
     (sql/queries.sql — SLA, Qualidade e Window Functions)
```

---

## 🗄️ Modelo de Dados Relacional (ERD)

O banco de dados relacional `logitech_analytics` é composto por 4 tabelas conectadas por chaves primárias e estrangeiras:

1. **`clientes`**: Informações cadastrais e localização (UF/Cidade).
2. **`transportadoras`**: Parceiros logísticos e prazos contratados de SLA.
3. **`pedidos`**: Registro transacional de envios, datas de entrega, status e valores monetários.
4. **`controle_qualidade`**: Registro de inspeção, motivos de devolução e prejuízos calculados.

---

## 📁 Estrutura de Pastas do Projeto

```text
logitech-analytics/
├── data/
│   └── dados_logisticos.xlsx   # Planilha-fonte com dados sintéticos (20 linhas/aba)
├── sql/
│   ├── schema.sql              # Script DDL de criação e destruição das tabelas
│   └── queries.sql             # Consultas analíticas e respostas de negócio
├── scripts/
│   └── ingest.py               # Pipeline de ETL em Python
├── docs/
│   └── relatorio_tecnico.md    # Especificações técnicas e arquitetura do projeto
├── docker-compose.yml          # Configuração do container PostgreSQL
├── requirements.txt            # Dependências Python do projeto
└── README.md                   # Documentação principal
```

---

## 🚀 Como Executar o Projeto Passo a Passo

### 1. Pré-requisitos
* **Docker Desktop** instalado e em execução na máquina.
* **Python 3.10+** e `pip` instalados.
* Terminal de comando (PowerShell, Bash ou CMD).

### 2. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/logitech-analytics.git
cd logitech-analytics
```

### 3. Instalar as Dependências do Python
```powershell
pip install -r requirements.txt
```

### 4. Subir o Banco de Dados PostgreSQL no Docker
Inicie o container do PostgreSQL em segundo plano:
```powershell
docker-compose up -d
```
*Para verificar se o container subiu corretamente:*
```powershell
docker ps
```

### 5. Executar o Script DDL (Criar a Estrutura do Banco)
No terminal PowerShell do Windows, execute:
```powershell
Get-Content sql/schema.sql | docker exec -i logitech_postgres psql -U data_analyst -d logitech_analytics
```
*(No Git Bash / Linux: `docker exec -i logitech_postgres psql -U data_analyst -d logitech_analytics < sql/schema.sql`)*

### 6. Executar o Pipeline de Ingestão ETL (Python)
Rode o script responsável por ler a planilha em `data/dados_logisticos.xlsx` e carregar o banco de dados:
```powershell
python scripts/ingest.py
```

### 7. Executar as Consultas Analíticas (SQL)
Para visualizar as respostas das perguntas de negócio e métricas operacionais diretamente no terminal:
```powershell
Get-Content sql/queries.sql | docker exec -i logitech_postgres psql -U data_analyst -d logitech_analytics
```

---

## 📊 Principais Insights Extraídos

1. **Cumprimento de SLA por Transportadora**: Mapeamento de percentual de atrasos por parceiro logístico para suporte em renegociações contratuais.
2. **Análise de Prejuízos de Qualidade**: Identificação dos principais motivos de devolução (ex: produto danificado vs item trocado) e o impacto financeiro direto.
3. **Média Móvel de Entregas (Window Function)**: Avaliação cronológica do histórico de prazo real de entrega acumulado por cliente.