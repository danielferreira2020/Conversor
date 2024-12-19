import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Parâmetros de conexão
db_user = 'daniel.soares'
db_password = 'daniel.rc'  # Senha em texto claro
db_host = 'srv'
db_port = '5432'
db_name = 'rc_card'
db_schema = 'stages_rc_card'

# Conexão com o banco de dados
try:
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    print("Conexão com o banco de dados estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar com o banco de dados: {e}")

# Consultas SQL para cada tabela
queries = {
    'PENSIONISTAS': """
        WITH PENSIONISTAS AS (
            SELECT 
                coluna1 as nome, 
                coluna2 as cpf, 
                coluna3 as valor_liquido,  
                coluna6 as email,
                REGEXP_REPLACE(coluna5, '[^0-9]', '', 'g') AS NUMERO
            FROM 
                stages_rc_card.pensionistas
            WHERE 
                coluna5 IS NOT NULL
        )
        SELECT * FROM PENSIONISTAS
        WHERE LENGTH(NUMERO) = 11
        AND NUMERO LIKE ('2%')
    """,
    'CIVIL': """
        WITH CIVIL AS (
            SELECT 
                coluna1 as nome, 
                coluna2 as cpf, 
                coluna3 as valor_liquido,  
                coluna5 as email,
                REGEXP_REPLACE(coluna4, '[^0-9]', '', 'g') AS NUMERO
            FROM 
                stages_rc_card.civil
            WHERE 
                coluna4 IS NOT NULL
        )
        SELECT * FROM CIVIL
        WHERE LENGTH(NUMERO) = 11
        AND NUMERO LIKE ('2%')
    """,
    'CIVIL_INATIVO': """
        WITH CIVIL_INATIVO AS (
            SELECT 
                coluna2 as nome, 
                coluna1 as cpf, 
                coluna3 as valor_liquido,  
                coluna4 as email,
                REGEXP_REPLACE(coluna5, '[^0-9]', '', 'g') AS NUMERO
            FROM 
                stages_rc_card.civil_inativo
            WHERE 
                coluna5 IS NOT NULL
        )
        SELECT * FROM CIVIL_INATIVO
        WHERE LENGTH(NUMERO) = 11
        AND NUMERO LIKE ('2%')
    """,
    'MILITAR': """
        WITH MILITAR AS (
            SELECT 
                coluna2 as nome, 
                coluna1 as cpf, 
                coluna3 as valor_liquido,  
                coluna4 como email,
                REGEXP_REPLACE(coluna5, '[^0-9]', '', 'g') AS NUMERO
            FROM 
                stages_rc_card.militar
            WHERE 
                coluna5 IS NOT NULL
        )
        SELECT * FROM MILITAR
        WHERE LENGTH(NUMERO) = 11
        AND NUMERO LIKE ('2%')
    """,
    'MILITAR_INATIVO': """
        WITH MILITAR_INATIVO AS (
            SELECT 
                coluna2 as nome, 
                coluna1 as cpf, 
                coluna3 as valor_liquido,  
                coluna4 as email,
                REGEXP_REPLACE(coluna5, '[^0-9]', '', 'g') AS NUMERO
            FROM 
                stages_rc_card.militar_inativo
            WHERE 
                coluna5 IS NOT NULL
        )
        SELECT * FROM MILITAR_INATIVO
        WHERE LENGTH(NUMERO) = 11
        AND NUMERO LIKE ('2%')
    """,
    'PENCAO_ESPECIAL': """
        WITH PENCAO_ESPECIAL AS (
            SELECT 
                coluna1 as nome, 
                coluna2 as cpf, 
                coluna3 as valor_liquido,  
                coluna5 as email,
                REGEXP_REPLACE(coluna4, '[^0-9]', '', 'g') AS NUMERO
            FROM 
                stages_rc_card.pensao_especial
            WHERE 
                coluna4 IS NOT NULL
        )
        SELECT * FROM PENCAO_ESPECIAL
        WHERE LENGTH(NUMERO) = 11
        AND NUMERO LIKE ('2%')
    """
}

# Nome do arquivo Excel
nome_arquivo = 'servidores_rio_de_janeiro.xlsx'

# Exportação para Excel
with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
    for sheet_name, query in queries.items():
        try:
            # Carregar o resultado da consulta para um DataFrame usando a 'engine' diretamente
            df = pd.read_sql(query, engine)
            if not df.empty:
                # Salvar o DataFrame em uma aba do Excel com o nome da consulta
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Tabela '{sheet_name}' exportada com sucesso.")
            else:
                print(f"A consulta para '{sheet_name}' retornou um DataFrame vazio. Nenhum dado exportado.")
        except Exception as e:
            print(f"Erro ao executar a consulta para '{sheet_name}': {e}")

print("Processo de exportação concluído.")

# Fechar a conexão com o banco de dados
engine.dispose()