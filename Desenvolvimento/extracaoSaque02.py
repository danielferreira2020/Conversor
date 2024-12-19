import os
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus

# Função para verificar e adicionar colunas que não existem
def create_or_alter_table(df, schema, table_name, engine):
    dtype_mapping = {
        'object': 'VARCHAR',
        'int64': 'INTEGER',
        'float64': 'NUMERIC',
        'datetime64[ns]': 'TIMESTAMP',
        'bool': 'BOOLEAN',
        'string': 'VARCHAR'
    }
    
    inspector = inspect(engine)
    columns_in_db = []
    if inspector.has_table(table_name, schema=schema):
        columns_in_db = [col['name'] for col in inspector.get_columns(table_name, schema=schema)]

    with engine.connect() as connection:
        for column, dtype in df.dtypes.items():
            column_type = dtype_mapping.get(str(dtype), 'VARCHAR')
            if column not in columns_in_db:
                alter_table_sql = f'ALTER TABLE "{schema}"."{table_name}" ADD COLUMN "{column}" {column_type};'
                try:
                    connection.execute(text(alter_table_sql))
                    print(f"Coluna '{column}' adicionada na tabela '{schema}.{table_name}'.")
                except SQLAlchemyError as e:
                    print(f"Erro ao adicionar a coluna '{column}' na tabela '{schema}.{table_name}': {e}")

# Função para truncar a tabela
def truncate_table(schema, table_name, engine):
    truncate_sql = f'TRUNCATE TABLE "{schema}"."{table_name}";'
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

# Função para filtrar linhas onde colunas com 'cliente' no nome não são nulas
def filter_non_null_data_columns(df):
    data_columns = [col for col in df.columns if 'cliente' in col.lower()]
    if data_columns:
        df = df.dropna(subset=data_columns, how='all')
    return df

# Configurações de conexão com o banco de dados
db_user = 'daniel.soares'
db_password = 'daniel.rc'
db_host = '192.168.10.6'
db_port = '5432'
db_name = 'rc_card'
db_schema = 'saque'

db_password_encoded = quote_plus(db_password)
connection_string = f'postgresql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}'
print(f'String de conexão: {connection_string}')

engine = create_engine(connection_string)

# Caminho para a pasta com arquivos Excel
folder_path = '//srv/ie/Saque/Vendas Saque/2023/'

# Nome da planilha que você quer selecionar
selected_sheet_name = 'Base_Saque'

# Listar todos os arquivos .xls na pasta
files = [f for f in os.listdir(folder_path) if f.endswith('.xls')]

if files:
    first_file_path = os.path.join(folder_path, files[0])
    
    try:
        df = pd.read_excel(first_file_path, sheet_name=selected_sheet_name)
        df = df.applymap(lambda x: x.encode('utf-8').decode('utf-8') if isinstance(x, str) else x)
        df = filter_non_null_data_columns(df)
        
        # Verificar se a tabela existe antes de truncar
        inspector = inspect(engine)
        if inspector.has_table(selected_sheet_name, schema=db_schema):
            # Truncar a tabela antes de criar ou alterar a estrutura
            truncate_table(db_schema, selected_sheet_name, engine)
            
            # Criar ou alterar a tabela
            create_or_alter_table(df, db_schema, selected_sheet_name, engine)
        else:
            print(f"A tabela '{db_schema}.{selected_sheet_name}' não existe. Não é possível truncar.")
    
    except Exception as e:
        print(f"Erro ao processar a planilha '{selected_sheet_name}' no arquivo '{first_file_path}': {e}")
else:
    print("Nenhum arquivo encontrado na pasta selecionada.")

# Iterar sobre cada arquivo .xls e inserir os dados
for file in files:
    file_path = os.path.join(folder_path, file)
    print(f"Lendo o arquivo: {file_path}")
    
    try:
        df = pd.read_excel(file_path, sheet_name=selected_sheet_name)
        df = df.applymap(lambda x: x.encode('utf-8').decode('utf-8') if isinstance(x, str) else x)
        df = filter_non_null_data_columns(df)
        
        # Verificar e adicionar colunas que não existem
        create_or_alter_table(df, db_schema, selected_sheet_name, engine)
        
        # Importar os dados para a tabela (sem truncar novamente)
        import_data_to_table(df, db_schema, selected_sheet_name, engine)
    
    except Exception as e:
        print(f"Erro ao processar a planilha '{selected_sheet_name}' no arquivo '{file_path}': {e}")
