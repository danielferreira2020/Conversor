import pandas as pd
from sqlalchemy import create_engine

# Parâmetros de conexão com o banco de dados de origem (onde será executada a consulta SQL)
db_user_src = 'daniel.soares'
db_password_src = 'daniel.rc'
db_host_src = 'srv'
db_port_src = '5432'
db_name_src = 'rc_card'

# Consulta SQL para extrair os dados
sql_query = '''
with f_operacao as (
SELECT "Data" as data,
"Cliente" as cliente,
"Número do Cartão" as numero_cartao,
"Valor Compra":: numeric (22,2) as valor_compra,
"Juros Compra":: numeric (22,2) as juros_compra,
"Entrada"::int as entrada,
"Valor Parcela":: int as quantidade_parcela,
"Rede":: numeric (22,2) as valor_parcela,
"Loja" as rede,
"Unnamed: 9" as convenio,
replace(replace("Unnamed: 11", '.', ''), '-', ''):: char(11) as cpf 
FROM stages_rc_card.compras_clientes 
where "Unnamed: 9" like ('%Saque%') 
and "Unnamed: 9" not in ('Saque Banco 24 Horas (G) (R)')), liberacao as (
SELECT "NOME", replace(replace("CPF", '.', ''), '-', '') as cpf, "LOJA", "EFETIVO OU COMISSIONADO", "VALOR DEPÓSITO", "VALOR DISPONIBILIZADO", "VALOR A RECEBER", "JUROS TOTAL", "TAXA DE JUROS", "QNTD DE PARCELAS", "VALOR DE PARCELAS", "DATA FECHAMENTO", "DADOS BANCÁRIO", "VALOR QUITADO", "VENDEDOR", "SISTEMA", "OBSERVAÇÃO", "COMPROVANTE DE TRANSFERÊNCIA", "Unnamed: 20"
	FROM stages_rc_card.liberacao_saque07
)
select *,
(valor_compra - juros_compra) as valor_principal,
to_char(data, 'mm'):: integer as mes_liberacao,
to_char(data, 'yyyy'):: integer as ano_liberacao,
(juros_compra/quantidade_parcela):: numeric(22,2) as juros_mes,
((valor_parcela)-(juros_compra/quantidade_parcela)):: numeric(22,2) as amortizacao_mes
from f_operacao

'''

# Criando a engine para o banco de origem
engine_src = create_engine(f'postgresql+psycopg2://{db_user_src}:{db_password_src}@{db_host_src}:{db_port_src}/{db_name_src}')

# Etapa de Extração (Extract) - executando a consulta SQL e trazendo os dados como DataFrame
df = pd.read_sql(sql_query, engine_src)

# Exibindo as primeiras linhas para verificar os dados extraídos
print(df.head())

# Etapa de Transformação (Transform)
# Convertendo colunas para tipos apropriados, caso ainda não estejam corretos
df['valor_compra'] = pd.to_numeric(df['valor_compra'], errors='coerce').round(2)
df['juros_compra'] = pd.to_numeric(df['juros_compra'], errors='coerce').round(2)
df['valor_parcela'] = pd.to_numeric(df['valor_parcela'], errors='coerce').round(2)

# Etapa de Carga (Load)
# Parâmetros de conexão com o banco de dados de destino (onde os dados serão carregados)
db_user_dest = 'daniel.soares'
db_password_dest = 'daniel.rc'
db_host_dest = 'srv'
db_port_dest = '5432'
db_name_dest = 'rc_card'

# Criando a engine para o banco de destino
engine_dest = create_engine(f'postgresql+psycopg2://{db_user_dest}:{db_password_dest}@{db_host_dest}:{db_port_dest}/{db_name_dest}')

# Carregando os dados transformados na tabela do banco de destino
df.to_sql('stages_rc_card.operacoes', engine_dest, if_exists='replace', index=False)

print("ETL concluído com sucesso!")