import os

# Função para formatar cada linha do arquivo de entrada
def formatar_linha(linha):
    # Remove espaços em excesso antes e depois do ponto e vírgula
    partes = [parte.strip() for parte in linha.split(';')]

    # Verifica se a linha tem pelo menos 5 campos
    if len(partes) < 4:
        print(f"Linha ignorada (menos de 4 campos): {linha}")
        return None  # Retorna None para linhas mal formatadas ou com menos de 4 campos
    
    # Campo 1 (sem alterações, removendo espaços)
    campo1 = partes[0].strip()
    
    # Campo 2 (primeiros 11 dígitos)
    campo2 = partes[1][:11] 
    
    # Campo 3 (próximos 3 dígitos após os 11 primeiros)
    campo3 = partes[1][12:15]
    
    # Campo 4 (sem alterações)
    campo4 = partes[2].strip()
    
    try:
        # Converte o valor para float, arredonda para 2 casas decimais, e depois converte para string com a vírgula
        valor = f"{round(float(partes[3]), 2):.2f}".replace('.', ',')       
    except ValueError:
        print(f"Valor inválido no campo 4 (não numérico): {partes[3]}")
        return None  # Caso o valor no campo 4 não seja numérico, retorna None
    
    # Junta os campos novamente com o separador ';' e retorna
    return f"{campo1};{campo2};{campo3};{campo4};{valor}"

# Função para processar o arquivo de entrada e gerar a saída
def processar_arquivo(entrada, saida):
    with open(entrada, 'r', encoding='utf-8') as arquivo_entrada:
        linhas = arquivo_entrada.readlines()
    
    # Filtra as linhas vazias ou mal formatadas (None)
    linhas_formatadas = [formatar_linha(linha) for linha in linhas if linha.strip()]
    
    # Filtra valores None, que são linhas mal formatadas ou com erro de conversão
    linhas_formatadas = [linha for linha in linhas_formatadas if linha is not None]
    
    # Verifica se há linhas formatadas para escrever
    if linhas_formatadas:
        with open(saida, 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write('\n'.join(linhas_formatadas))
        print(f"Arquivo de saída gerado com {len(linhas_formatadas)} linhas.")
    else:
        print("Nenhuma linha válida foi processada.")

# Caminhos dos arquivos de entrada e saída
arquivo_entrada = 'C:/Users/DAniel/Documents/Projetos/Conversão/C0445_MIPIBU_Rem000012_Data20241213.txt'  # Substitua pelo caminho do seu arquivo de entrada
arquivo_saida = 'C:/Users/DAniel/Documents/Projetos/Conversão/saida.txt'  # Substitua pelo caminho do arquivo de saída desejado

# Verifica se o arquivo de entrada existe
if not os.path.exists(arquivo_entrada):
    print(f"Erro: O arquivo {arquivo_entrada} não foi encontrado.")
else:
    # Executa o processamento do arquivo
    processar_arquivo(arquivo_entrada, arquivo_saida)
