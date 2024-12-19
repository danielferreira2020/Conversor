import pandas as pd

file_path = 'Z:/Planilhas/Folha.csv'
output_excel = 'Z:/Planilhas/Folha_analitica_estruturada.xlsx'

# Função para leitura de CSV sem um padrão claro de colunas
def read_dynamic_csv(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Dividindo as linhas usando uma vírgula como delimitador (ou outro delimitador)
                row = line.strip().split(',')
                data.append(row)
    except UnicodeDecodeError:
        # Tentando outra codificação se UTF-8 falhar
        with open(file_path, 'r', encoding='latin1') as f:
            for line in f:
                row = line.strip().split(',')
                data.append(row)
    
    # Transformar os dados em um DataFrame do pandas, lidando com diferentes tamanhos de linha
    df = pd.DataFrame(data)
    
    # Remover linhas vazias ou quase vazias
    df.replace('', None, inplace=True)
    df.dropna(how='all', inplace=True)
    
    return df

# Ler o CSV e estruturar os dados
df = read_dynamic_csv(file_path)

# Exibir algumas linhas do DataFrame para ver a estrutura que obtivemos
print(df.head())

# Salvar os dados estruturados em um arquivo Excel
df.to_excel(output_excel, index=False, sheet_name='Folha_analitica')

print(f"Dados extraídos e salvos no arquivo {output_excel}")