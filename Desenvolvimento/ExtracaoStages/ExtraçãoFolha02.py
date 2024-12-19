import pandas as pd

# Cole aqui o caminho exato do arquivo, obtido com "Copiar como caminho"
file_path = 'Z:/Planilhas/Folha_analitica(4).csv'
output_excel = 'Z:/Planilhas/Folha_analitica_estruturada.xlsx'

# Carregar o CSV, ignorando linhas mal formatadas com o parâmetro correto
df = pd.read_csv(file_path, on_bad_lines='skip', delimiter=',', encoding='utf-8', engine='python')

# Substituir valores NaN por strings vazias para não afetar a estrutura da planilha
df.fillna('', inplace=True)

# Criar um arquivo Excel e salvar o dataframe
df.to_excel(output_excel, index=False, sheet_name='Dados Estruturados')

print(f"Dados extraídos e salvos no arquivo {output_excel}")