import requests
import pandas as pd

# Token de autenticação
token = 'c612a092017fc39036d10905bf6ce586'

# Cabeçalho de autenticação
headers = {"Authorization": f"Bearer {token}"}

# URLs da API
url_category = "https://xfinanceapp.com/api/1.1/obj/category/"
url_recipient = "https://xfinanceapp.com/api/1.1/obj/recipient/"


# Fazendo a solicitação para a primeira URL
def chamar_api_myfinance(url):
    response = requests.get(url, headers=headers)
    return response

# guardar o response de cada chamada da api em uma variavel
response_category = chamar_api_myfinance(url_category)
response_recipient = chamar_api_myfinance(url_recipient)

# navegar no json até onde estão dos dados necessários
category_ajustado_json = response_category.json()['response']['results']
recipient_ajustado_json = response_recipient.json()['response']['results']

#transformar o json ajustado em dataframe com o pandas
df_category = pd.DataFrame(category_ajustado_json,columns=['title', '_id'])
df_recipient = pd.DataFrame(recipient_ajustado_json,columns=['title', '_id','category_ref'])

#salvar o dataframe em .xlxs e .parquet
df_category.to_excel('Category.xlsx', index=False)
df_category.to_parquet('Category.parquet', index=False)

df_recipient.to_excel('Recipient.xlsx', index=False)
df_recipient.to_parquet('Recipient.parquet', index=False)