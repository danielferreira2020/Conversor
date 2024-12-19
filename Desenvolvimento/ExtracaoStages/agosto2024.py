#AUTOR: DANIEL FERREIRA SOARES DA SILVA#
import pandas as pd
from sqlalchemy import create_engine

# Caminho para o arquivo Excel
excel_file_path = '//srv/ie/IE_Faturamento/FATURAMENTO DE CONVÊNIOS.xlsx'

# Ler todas as abas em um dicionário de DataFrames
dfs = pd.read_excel(excel_file_path, sheet_name=None)

# Concatenar todos os DataFrames em um único DataFrame
df_consolidado = pd.concat(dfs.values(), ignore_index=True)

# Verificar as primeiras linhas do DataFrame consolidado
print(df_consolidado.head())

# Informações de conexão com o banco de dados
db_user = 'daniel.soares'
db_password = 'daniel.rc'
db_host = 'localhost'
db_port = '3080'
db_name = 'stage_rc_card'

# Criação da string de conexão
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Importar dados para a tabela 'pagamentos'
df_consolidado.to_sql('pagamentos', engine, if_exists='replace', index=False)

print("Dados importados com sucesso!")
