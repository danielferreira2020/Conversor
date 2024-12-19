import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus

# Função para criar a tabela no PostgreSQL
def create_table_from_df(df, schema, table_name, engine):
    dtype_mapping = {
        'object': 'VARCHAR',
        'int64': 'INTEGER',
        'float64': 'NUMERIC',
        'datetime64[ns]': 'TIMESTAMP',
        'bool': 'BOOLEAN',
        'string': 'VARCHAR'
    }
    
    columns_with_types = []
    for column, dtype in df.dtypes.items():
        column_type = dtype_mapping.get(str(dtype), 'VARCHAR')
        if column_type == 'NUMERIC':
            columns_with_types.append(f'"{column}" NUMERIC')
        else:
            columns_with_types.append(f'"{column}" {column_type}')
    
    columns_with_types_str = ", ".join(columns_with_types)
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS "{schema}"."{table_name}" (
        id SERIAL PRIMARY KEY,
        {columns_with_types_str}
    );
    """
    
    with engine.connect() as connection:
        try:
            connection.execute(text(create_table_sql))
            print(f"Tabela '{schema}.{table_name}' criada com sucesso.")
        except SQLAlchemyError as e:
            print(f"Erro ao criar a tabela '{schema}.{table_name}': {e}")

# Função para truncar a tabela antes de importar novos dados
def truncate_table(schema, table_name, engine):
    truncate_sql = f'TRUNCATE TABLE "{schema}"."{table_name}" RESTART IDENTITY CASCADE;'
    with engine.connect() as connection:
        try:
            connection.execute(text(truncate_sql))
            print(f"Tabela '{schema}.{table_name}' truncada com sucesso.")
        except SQLAlchemyError as e:
            print(f"Erro ao truncar a tabela '{schema}.{table_name}': {e}")

# Função para importar dados para a tabela
def import_data_to_table(df, schema, table_name, engine):
    try:
        df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)
        print(f"Dados importados para a tabela '{schema}.{table_name}' com sucesso.")
    except Exception as e:
        print(f"Erro ao importar dados para a tabela '{schema}.{table_name}': {e}")

# Configurações de conexão com o banco de dados
db_user = 'daniel.soares'
db_password = 'daniel.rc'  # Senha em texto claro
db_host = 'srv'
db_port = '5432'  # Porta personalizada; ajuste se necessário
db_name = 'rc_card'
db_schema = 'financeiro'

# Codifica a senha para a string de conexão
db_password_encoded = quote_plus(db_password)

# Criação da string de conexão
connection_string = f'postgresql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}'
print(f'String de conexão: {connection_string}')

# Criação do engine
engine = create_engine(connection_string)

# Caminho para o arquivo XLS
xls_file_path = "//srv/ie/Planilhas/Financeiro/DespesasBases.xlsx"
xls_file_path1 = "//srv/ie/Planilhas/Financeiro/visao_contas_a_pagar.xls"

# Tentar ler as duas planilhas Excel
try:
    df_area = pd.read_excel(xls_file_path, sheet_name='Area', header=0)  # Planilha 'Area'
    df_grupo_contabil = pd.read_excel(xls_file_path, sheet_name='Grupo_Contabil', header=0)  # Planilha 'Grupo Contábil'
    df_visao_contas_a_pagar = pd.read_excel(xls_file_path1, sheet_name='Visão Contas a Pagar', header=0)  # Planilha 'Visao Contas a Pagar'
    print("Dados lidos com sucesso das planilhas Excel.")
except Exception as e:
    print(f"Erro ao ler as planilhas Excel: {e}")

# Remover colunas completamente nulas nas três planilhas
df_area = df_area.dropna(axis=1, how='all')
df_grupo_contabil = df_grupo_contabil.dropna(axis=1, how='all')
df_visao_contas_a_pagar = df_visao_contas_a_pagar.dropna(axis=1, how='all')

# Nome das tabelas a serem criadas
table_name_area = 'setores'
table_name_grupo_contabil = 'grupos_contabeis'
table_name_visao_contas_a_pagar = 'contas_pagar'

# Criar e truncar a tabela para a planilha 'Area'
create_table_from_df(df_area, db_schema, table_name_area, engine)
truncate_table(db_schema, table_name_area, engine)

# Criar e truncar a tabela para a planilha 'Grupo_Contabil'
create_table_from_df(df_grupo_contabil, db_schema, table_name_grupo_contabil, engine)
truncate_table(db_schema, table_name_grupo_contabil, engine)

# Criar e truncar a tabela para a planilha 'visao_contas_a_pagar'
create_table_from_df(df_visao_contas_a_pagar, db_schema, table_name_visao_contas_a_pagar, engine)
truncate_table(db_schema, table_name_visao_contas_a_pagar, engine)

# Importar os dados para as respectivas tabelas
import_data_to_table(df_area, db_schema, table_name_area, engine)
import_data_to_table(df_grupo_contabil, db_schema, table_name_grupo_contabil, engine)
import_data_to_table(df_visao_contas_a_pagar, db_schema, table_name_visao_contas_a_pagar, engine)