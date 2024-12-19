import pandas as pd

# Carregar o arquivo CSV da folha de pagamento
csv_file = 'C:/Users/DAniel/Documents/Planilhas/Folha analitica(4).csv'
df = pd.read_csv(csv_file)

# Exibir as primeiras linhas para entender a estrutura
print(df.head())

# Separar os dados conforme necessário
# Exemplo 1: Separar por Departamento
df_departamentos = df.groupby('Departamento')

# Exemplo 2: Separar por Categoria de Pagamento
df_categoria_pagamento = df.groupby('Categoria_Pagamento')

# Criar um arquivo Excel com múltiplas abas para cada separação
excel_file = 'folha_pagamento_analisada.xlsx'
with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
    for departamento, data in df_departamentos:
        data.to_excel(writer, sheet_name=f'Departamento_{departamento}', index=False)
    for categoria, data in df_categoria_pagamento:
        data.to_excel(writer, sheet_name=f'Categoria_{categoria}', index=False)

print(f"Análise da folha de pagamento salva em {excel_file}")