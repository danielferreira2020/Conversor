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
    
    # Verificar as colunas existentes no banco de dados
    inspector = inspect(engine)
    columns_in_db = []
    if inspector.has_table(table_name, schema=schema):
        columns_in_db = [col['name'] for col in inspector.get_columns(table_name, schema=schema)]

    with engine.connect() as connection:
        # Verificar cada coluna do DataFrame
        for column, dtype in df.dtypes.items():
            column_type = dtype_mapping.get(str(dtype), 'VARCHAR')
            
            # Se a coluna não existir no banco, será adicionada
            if column not in columns_in_db:
                alter_table_sql = f'ALTER TABLE "{schema}"."{table_name}" ADD COLUMN "{column}" {column_type};'
                try:
                    connection.execute(text(alter_table_sql))
                    print(f"Coluna '{column}' adicionada na tabela '{schema}.{table_name}'.")
                except SQLAlchemyError as e:
                    print(f"Erro ao adicionar a coluna '{column}' na tabela '{schema}.{table_name}': {e}")

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

# Função para importar dados para a tabela
def import_data_to_table(df, schema, table_name, engine):
    try:
        df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)
        print(f"Dados importados para a tabela '{schema}.{table_name}' com sucesso.")
    except Exception as e:
        print(f"Erro ao importar dados para a tabela '{schema}.{table_name}': {e}")

# Função para filtrar linhas onde colunas com 'cliente' no nome não são nulas
def filter_non_null_data_columns(df):
    # Identificar colunas cujo nome contém a palavra 'cliente'
    data_columns = [col for col in df.columns if 'cliente' in col.lower()]
    
    if data_columns:
        # Filtrar linhas onde pelo menos uma coluna 'cliente' não é nula
        df = df.dropna(subset=data_columns, how='all')  # Remove linhas onde todas as colunas 'cliente' são nulas
    
    return df

# Configurações de conexão com o banco de dados
db_user = 'daniel.soares'
db_password = 'daniel.rc'  # Senha em texto claro
db_host = '192.168.10.6'
db_port = '5432'  # Porta personalizada; ajuste se necessário
db_name = 'rc_card'
db_schema = 'stages_rc_card'

# Codifica a senha para a string de conexão
db_password_encoded = quote_plus(db_password)

# Criação da string de conexão
connection_string = f'postgresql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}'
print(f'String de conexão: {connection_string}')

# Criação do engine
engine = create_engine(connection_string)

# Caminho para a pasta com arquivos Excel
folder_path = '//srv/ie/Planilhas/ComprasClientes/CopiaGeral'

# Nome da planilha que você quer selecionar
selected_sheet_name = 'Sheet1'

# Nome da tabela no banco de dados
table_name = 'compras_clientes'

# Lista para armazenar os dataframes de todas as planilhas
planilhas = []

# Listar todos os arquivos .xls na pasta "2023-24"
files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Iterar sobre cada arquivo .xls e combiná-los em um dataframe
for file in files:
    file_path = os.path.join(folder_path, file)
    print(f"Lendo o arquivo: {file_path}")
    
    try:
        # Ler a planilha especificada
        df = pd.read_excel(file_path, sheet_name=selected_sheet_name)
        
        # Verificar e ajustar os dados, se necessário
        df = df.applymap(lambda x: x.encode('utf-8').decode('utf-8') if isinstance(x, str) else x)
        
        # Filtrar linhas onde colunas com 'cliente' no nome não são nulas
        df = filter_non_null_data_columns(df)
        
        # Adiciona o dataframe à lista de planilhas
        planilhas.append(df)
    
    except Exception as e:
        print(f"Erro ao processar a planilha '{selected_sheet_name}' no arquivo '{file_path}': {e}")

# Combinar todas as planilhas em um único dataframe
df_combinado = pd.concat(planilhas, ignore_index=True)

# Criar a tabela no banco de dados (caso não exista)
create_table_from_df(df_combinado, db_schema, table_name, engine)

# Verificar e adicionar colunas que não existem no banco de dados
create_or_alter_table(df_combinado, db_schema, table_name, engine)

# Importar os dados combinados para a tabela
import_data_to_table(df_combinado, db_schema, table_name, engine)

print(f'Todas as planilhas foram combinadas e importadas para a tabela "{db_schema}.{table_name}".')