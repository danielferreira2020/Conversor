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

# Função para importar dados para a tabela
def import_data_to_table(df, schema, table_name, engine):
    try:
        df.to_sql(table_name, engine, schema=schema, if_exists='replace', index=False)
        print(f"Dados importados para a tabela '{schema}.{table_name}' com sucesso.")
    except Exception as e:
        print(f"Erro ao importar dados para a tabela '{schema}.{table_name}': {e}")

# Configurações de conexão com o banco de dados
db_user = 'daniel.soares'
db_password = 'daniel.rc'  # Senha em texto claro
db_host = 'srv'
db_port = '5432'
db_name = 'rc_card'
db_schema = 'stages_rc_card'

# Codifica a senha para a string de conexão
db_password_encoded = quote_plus(db_password)

# Criação da string de conexão
connection_string = f'postgresql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}'
print(f'String de conexão: {connection_string}')

# Criação do engine
engine = create_engine(connection_string)

# Caminho para o arquivo XLS
xls_file_path = "C:/Users/DAniel/Documents/TESTE.xlsx"

# Nome da planilha a ser lida
sheet_name = 'PENSIONISTAS'  # Defina o nome da planilha

# Tentar ler a planilha específica do arquivo Excel com pandas
try:
    df = pd.read_excel(xls_file_path, sheet_name=sheet_name, header=None)  # Carregar a planilha pelo nome
    print("Dados lidos com sucesso da planilha específica.")
except Exception as e:
    print(f"Erro ao ler a planilha '{sheet_name}': {e}")

# Verificar o número de colunas no DataFrame
num_columns = df.shape[1]
print(f"Número de colunas detectado: {num_columns}")

# Nomes das colunas conforme o número de colunas detectado
column_names = [f'coluna{i+1}' for i in range(num_columns)]  # Substitua conforme necessário

# Aplicar os nomes de colunas ao DataFrame
df.columns = column_names

# Remover colunas completamente nulas
df = df.dropna(axis=1, how='all')

# Verificar o número de colunas restantes
remaining_columns = df.shape[1]
print(f"Número de colunas restantes após remover nulas: {remaining_columns}")

# Nome da tabela
table_name = 'teste06'  # Defina o nome da tabela conforme necessário

# Criar a tabela no banco de dados
create_table_from_df(df, db_schema, table_name, engine)

# Importar os dados para a tabela criada
import_data_to_table(df, db_schema, table_name, engine)
