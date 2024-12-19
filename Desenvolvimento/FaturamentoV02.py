import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus

# Função para criar uma tabela única no PostgreSQL
def create_single_table(schema, table_name, engine):
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS "{schema}"."{table_name}" (
        id SERIAL PRIMARY KEY,
        sheet_name VARCHAR,
        data JSONB
    );
    """
    with engine.connect() as connection:
        try:
            connection.execute(text(create_table_sql))
            print(f"Tabela '{schema}.{table_name}' criada com sucesso.")
        except SQLAlchemyError as e:
            print(f"Erro ao criar a tabela '{schema}.{table_name}': {e}")

# Função para obter os nomes das colunas da tabela existente
def get_existing_columns(schema, table_name, engine):
    query = f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = '{schema}' AND table_name = '{table_name}';
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(text(query))
            return {row['column_name'] for row in result}
        except SQLAlchemyError as e:
            print(f"Erro ao obter colunas existentes da tabela '{schema}.{table_name}': {e}")
            return set()

# Função para adicionar colunas à tabela existente
def add_columns_to_table(schema, table_name, new_columns, engine):
    with engine.connect() as connection:
        for column in new_columns:
            try:
                add_column_sql = f"""
                ALTER TABLE "{schema}"."{table_name}"
                ADD COLUMN IF NOT EXISTS "{column}" TEXT;
                """
                connection.execute(text(add_column_sql))
                print(f"Coluna '{column}' adicionada à tabela '{schema}.{table_name}'.")
            except SQLAlchemyError as e:
                print(f"Erro ao adicionar a coluna '{column}' à tabela '{schema}.{table_name}': {e}")

# Função para limpar nomes de colunas (remover espaços e caracteres especiais)
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('-', '_').str.replace('/', '_')
    return df

# Função para importar dados para a tabela única
def import_data_to_single_table(df, schema, table_name, engine, sheet_name):
    try:
        df['sheet_name'] = sheet_name
        df = clean_column_names(df)  # Limpar nomes das colunas antes de importar
        
        # Obter colunas existentes
        existing_columns = get_existing_columns(schema, table_name, engine)
        
        # Adicionar novas colunas se necessário
        new_columns = set(df.columns) - existing_columns
        if new_columns:
            add_columns_to_table(schema, table_name, new_columns, engine)
        
        # Inserir dados
        df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False, method='multi')
        print(f"Dados importados para a tabela '{schema}.{table_name}' com sucesso.")
    except Exception as e:
        print(f"Erro ao importar dados para a tabela '{schema}.{table_name}': {e}")

# Configurações de conexão com o banco de dados
db_user = 'daniel.soares'
db_password = 'daniel.rc'  # Senha em texto claro; considere usar variáveis de ambiente
db_host = 'localhost'
db_port = '3080'  # Porta personalizada; ajuste se necessário
db_name = 'rc_card'
db_schema = 'stages_rc_card'
table_name = 'consolidated_data'

# Codifica a senha para a string de conexão
db_password_encoded = quote_plus(db_password)

# Criação da string de conexão
connection_string = f'postgresql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}'
print(f'String de conexão: {connection_string}')

# Criação do engine
engine = create_engine(connection_string)

# Criação da tabela única
create_single_table(db_schema, table_name, engine)

# Caminho para o arquivo Excel
excel_file_path = '//srv/ie/IE_Faturamento/FATURAMENTO DE CONVÊNIOS.xlsx'

# Ler todas as abas em um dicionário de DataFrames
dfs = pd.read_excel(excel_file_path, sheet_name=None)

# Função para codificar strings (aplicada a cada coluna de strings)
def encode_strings(x):
    if isinstance(x, str):
        return x.encode('utf-8').decode('utf-8')
    return x

# Iterar sobre cada aba e importar dados para a tabela única
for sheet_name, df in dfs.items():
    print(f"Tipo de df: {type(df)}")  # Verifique se é um DataFrame
    if isinstance(df, pd.DataFrame):
        # Aplicar transformação de codificação a cada coluna de strings
        for col in df.select_dtypes(include=[object]).columns:
            df[col] = df[col].map(encode_strings)
        
        # Importar os dados para a tabela única
        import_data_to_single_table(df, db_schema, table_name, engine, sheet_name)
    else:
        print(f"Erro: Esperado um DataFrame, mas obtido {type(df)}")
