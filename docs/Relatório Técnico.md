# RELATÓRIO TÉCNICO DE ARQUITETURA E ENGENHARIA DE DADOS

**Projeto:** LogiTech Analytics  
**Domínio:** Logística e Controle de Qualidade  
**Stack:** PostgreSQL 15 (Docker), Python 3.10+, Pandas, SQLAlchemy  

---

## 1. RESUMO EXECUTIVO

Este documento apresenta a especificação técnica da infraestrutura de dados desenvolvida para o projeto **LogiTech Analytics**. A solução abrange desde o isolamento da camada de banco de dados via Docker até o orquestrador de ETL em Python para processamento de arquivos transacionais e disponibilização de inteligência analítica em SQL.

---

## 2. ARQUITETURA DE INFRAESTRUTURA (DOCKER)

A camada de persistência utiliza uma imagem otimizada do **PostgreSQL 15 (Alpine Linux)** para garantir baixo consumo de recursos e alta portabilidade.

### Especificação da Containerização (`docker-compose.yml`)
* **Serviço:** `postgres_db`
* **Nome do Container:** `logitech_postgres`
* **Porta Exposta:** `5432:5432`
* **Volume Persistente:** `pgdata -> /var/lib/postgresql/data` (Garante a permanência dos dados mesmo após a remoção ou reinicialização dos containers).
* **Credenciais e Banco:** `logitech_analytics` (User: `data_analyst`).

---

## 3. MODELAGEM DE DADOS E SCHEMAS (DDL)

A modelagem relacional segue a terceira forma normal (3FN) para garantir a integridade dos dados operacionais e minimizar redundâncias.

### DDL das Tabelas (`sql/schema.sql`)
* **`clientes`**: Contém `cliente_id` (PK), `nome`, `cidade`, `estado`.
* **`transportadoras`**: Contém `transportadora_id` (PK), `nome_transportadora`, `sla_dias`.
* **`pedidos`**: Contém `pedido_id` (PK), `cliente_id` (FK), `transportadora_id` (FK), `data_pedido`, `data_envio`, `data_entrega_prometida`, `data_entrega_real`, `status_pedido`, `valor_frete` (DECIMAL), `valor_pedido` (DECIMAL).
* **`controle_qualidade`**: Contém `inspecao_id` (PK), `pedido_id` (FK UNIQUE), `motivo_devolucao`, `custo_prejuizo` (DECIMAL).

---

## 4. PIPELINE DE EXTRAÇÃO, TRANSFORMAÇÃO E CARGA (ETL)

O pipeline em Python (`scripts/ingest.py`) adota uma abordagem resiliente e estruturada em 3 etapas:

1. **Extract**: Leitura dinâmica da planilha `data/dados_logisticos.xlsx` contendo as abas do sistema de origem.
2. **Transform**:
   * Conversão coercitiva dos atributos temporais para `DATETIME`.
   * Garantia de precisão numérica nos campos financeiros (`FLOAT`/`DECIMAL`).
3. **Load**: Carga via `SQLAlchemy` respeitando a árvore de dependências das Chaves Estrangeiras (`FKs`):
   * `clientes` e `transportadoras` $\rightarrow$ `pedidos` $\rightarrow$ `controle_qualidade`.

---

## 5. CONSULTAS E MÉTRICAS ANALÍTICAS (`sql/queries.sql`)

A camada analítica responde a 4 questões centrais do negócio:

1. **Gargalo de Transportadoras**: Identificação da taxa percentual de descumprimento de SLA por parceiro.
2. **Impacto por UF**: Soma monetária dos pedidos com status *Atrasado* ou *Devolvido* por estado.
3. **Custos da Não-Qualidade**: Agrupamento do prejuízo financeiro acumulado por motivo de devolução.
4. **Análise de Tendência**: Uso de **Window Function** (`AVG(...) OVER (PARTITION BY ... ORDER BY ...)`) para calcular a média móvel do tempo real de entrega por cliente.