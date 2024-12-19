import pandas as pd
import os

def txt_to_excel(directory_path, excel_file_path):
    # Lista para armazenar as linhas de dados processadas
    all_data = []
    
    # Definir o cabeçalho
    header = ["Títulos dos Cargos Comissionados", "Código", "Nível de Vencimento", "Quantitativo", "Ocupados", "Vagos"]

    # Iterar sobre todos os arquivos no diretório
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):  # Verifica se é um arquivo TXT
            txt_file_path = os.path.join(directory_path, filename)
            print(f"Lendo o arquivo: {txt_file_path}")

            # Tentar abrir o arquivo com a codificação 'ISO-8859-1'
            try:
                with open(txt_file_path, 'r', encoding='ISO-8859-1') as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                print(f"Erro ao ler o arquivo {txt_file_path} com a codificação ISO-8859-1")
                continue  # Pula para o próximo arquivo
            
            # Processar as linhas de dados
            for line in lines:
                line = line.strip()
                if line and not line.startswith('ADMINISTRAÇÃO DIRETA') and not line.startswith('ACESF') and not line.startswith('A.M.S.') and not line.startswith('CAAPSML') and not line.startswith('IDEL') and not line.startswith('IPPUL') and not line.startswith('FEL'):
                    # Usar tabulação como separador de colunas
                    columns = line.split('\t')
                    if len(columns) == 6:  # Verifica se a linha tem todas as colunas
                        all_data.append(columns)

    # Criar o DataFrame com os dados
    df = pd.DataFrame(all_data, columns=header)
    
    # Salvar o DataFrame como arquivo Excel
    df.to_excel(excel_file_path, index=False)
    
    print(f"Arquivo Excel salvo em: {excel_file_path}")

# Exemplo de uso
directory_path = 'Z:/Planilhas/Quantitativo/'  # Caminho do diretório que contém os arquivos TXT
excel_file_path = 'Folha_analitica_GO_202408.xlsx'  # Caminho de destino para o Excel

txt_to_excel(directory_path, excel_file_path)
