import pandas as pd

caminho_arquivo = '//srv/ie/Planilhas/ComprasClientes.xls'

df = pd.read_excel(caminho_arquivo,  sheet_name=0)

df = df.rename(columns={
    'Data': 'DATA',
    'Cliente': 'CLIENTE',
    'Número do Cartão': 'NUMERO_CARTAO',
    'Valor Compra': 'VALOR_COMPRA',
    'Loja': 'REDE',
    'Unnamed: 9': 'LOJA',
    'Unnamed: 11 ': 'CPF'
})
print(df)