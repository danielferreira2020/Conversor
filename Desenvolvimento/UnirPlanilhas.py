import pandas as pd
import os

# Diretório onde as planilhas Excel estão localizadas
caminho_diretorio = 'C:\\Users\\DAniel\\Downloads\\RELACAO-DE-AGOSTO.xlsx'

# Nome do arquivo final
arquivo_saida = '08-2024.xlsx'

# Lista para armazenar os dataframes de cada planilha
planilhas = []

# Loop para ler cada arquivo Excel no diretório
for arquivo in os.listdir(caminho_diretorio):
    if arquivo.endswith('.xlsx'):  # Filtra apenas arquivos com extensão .xls
        caminho_arquivo = os.path.join(caminho_diretorio, arquivo)
        
        # Lê a planilha ignorando a primeira linha (header=0)
        df = pd.read_excel(caminho_arquivo, engine='xlrd', header=0)
        
        # Remove o cabeçalho (primeira linha)
        df = df.iloc[1:]
        
        # Ignora as duas primeiras colunas
        df = df.iloc[:, 2:]
        
        # Adiciona o dataframe à lista
        planilhas.append(df)

# Concatena todas as planilhas ignorando os cabeçalhos duplicados
planilha_combinada = pd.concat(planilhas, ignore_index=True)

# Salva o dataframe combinado em um novo arquivo Excel
planilha_combinada.to_excel(arquivo_saida, index=False)

print(f'Planilhas combinadas com sucesso em {arquivo_saida}')