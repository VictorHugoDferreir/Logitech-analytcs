import os
import pandas as pd
from sqlalchemy import create_engine, text

# Configuração de Conexão com o PostgreSQL no Docker
DB_URL = "postgresql+psycopg2://data_analyst:analyst_password123@localhost:5432/logitech_analytics"
engine = create_engine(DB_URL)

def check_db_connection():
    """Verifica se o container PostgreSQL está ativo e acessível."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1;"))
            print(" Conexão com o PostgreSQL (Docker) estabelecida com sucesso!")
    except Exception as e:
        print(f"X Erro ao conectar ao banco de dados: {e}X")
        print("Certifique-se de que o container Docker está rodando ('docker-compose up -d').")
        exit(1)

def extract_data(file_path):
    """Extrai os dados do arquivo."""
    print(f"\n[1/3] Extraindo dados da fonte: {file_path}")
    
    dataframes = {}
    
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        xls = pd.ExcelFile(file_path)
        for sheet_name in ['clientes', 'transportadoras', 'pedidos', 'controle_qualidade']: #Procura as abas obrigatórias
            if sheet_name in xls.sheet_names:
                dataframes[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
                print(f"---> Aba '{sheet_name}' carregada ({len(dataframes[sheet_name])} linhas)")
            else:
                raise ValueError(f"Aba obrigatória '{sheet_name}' não encontrada na planilha!")
                
    elif os.path.isdir(file_path):
        for table_name in ['clientes', 'transportadoras', 'pedidos', 'controle_qualidade']:
            csv_file = os.path.join(file_path, f"{table_name}.csv")
            if os.path.exists(csv_file):
                dataframes[table_name] = pd.read_csv(csv_file)
                print(f"---> Arquivo '{table_name}.csv' carregado ({len(dataframes[table_name])} linhas)")
            else:
                raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_file}")
    else:
        raise FileNotFoundError(f"Caminho inválido ou formato não suportado: {file_path}")

    return dataframes

def transform_data(dfs):
    """Realiza a limpeza, tratamento de tipos de dados e coerção cronológica."""
    print("\n[2/3] Transformando e validando tipos de dados...")

    # Tratamento da Tabela Pedidos
    df_pedidos = dfs['pedidos'].copy()
    colunas_datas = ['data_pedido', 'data_envio', 'data_entrega_prometida', 'data_entrega_real']
    
    for col in colunas_datas:
        if col in df_pedidos.columns:
            df_pedidos[col] = pd.to_datetime(df_pedidos[col], errors='coerce')

    # Garantir que valores numéricos/monetários sejam decimal
    df_pedidos['valor_frete'] = pd.to_numeric(df_pedidos['valor_frete'], errors='coerce')
    df_pedidos['valor_pedido'] = pd.to_numeric(df_pedidos['valor_pedido'], errors='coerce')
    dfs['pedidos'] = df_pedidos

    # Tratamento da Tabela Controle de Qualidade
    df_qualidade = dfs['controle_qualidade'].copy()
    if 'custo_prejuizo' in df_qualidade.columns:
        df_qualidade['custo_prejuizo'] = pd.to_numeric(df_qualidade['custo_prejuizo'], errors='coerce')
    dfs['controle_qualidade'] = df_qualidade

    print("✓ Transformações de tipo concluídas com sucesso.")
    return dfs

def load_data(dfs):
    """Carrega os DataFrames no PostgreSQL respeitando a ordem de integridade referencial."""
    print("\n[3/3] Carregando dados no PostgreSQL...")

    # A ordem importa para não violar as chaves estrangeiras (FKs)
    ordem_carga = ['clientes', 'transportadoras', 'pedidos', 'controle_qualidade']

    for tabela in ordem_carga:
        df = dfs[tabela]
        try:
            # append insere as linhas sem recriar/destruir a DDL da tabela
            df.to_sql(tabela, engine, if_exists='append', index=False)
            print(f"  ✓ Tabela '{tabela}' populada ({len(df)} registros inseridos)")
        except Exception as e:
            print(f"X Erro ao carregar dados na tabela '{tabela}': {e} X")
            raise e

def run_etl_pipeline(source_path):
    """Função orquestradora do pipeline."""
    print("="*60)
    print(" INICIANDO PIPELINE DE ETL - LOGITECH ANALYTICS")
    print("="*60)
    
    check_db_connection()
    
    try:
        raw_dfs = extract_data(source_path)
        transformed_dfs = transform_data(raw_dfs)
        load_data(transformed_dfs)
        
        print("\n" + "="*60)
        print("PIPELINE EXECUTADO COM SUCESSO! DADOS PRONTOS NO BANCO.")
        print("="*60)
    except Exception as e:
        print(f"\nX Falha na execução do pipeline: {e} X")

if __name__ == "__main__":
    
    SOURCE = "data/dados_logisticos.xlsx" 
    
    run_etl_pipeline(SOURCE)