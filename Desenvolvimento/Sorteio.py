import pandas as pd
import random
import pywhatkit as kit
import time

# Função para carregar os dados da planilha
def carregar_dados(caminho_planilha):
    try:
        df = pd.read_excel(caminho_planilha)  # Leia a planilha
        return df
    except Exception as e:
        print(f"Erro ao carregar a planilha: {e}")
        return None

# Função para formatar os números de telefone
def formatar_telefone(telefones):
    telefones_formatados = []
    for telefone in telefones:
        telefone_str = str(telefone).strip()  # Garantir que é uma string
        if not telefone_str.startswith('+'):
            telefone_str = '+' + telefone_str  # Adicionar o "+" se faltar
        telefones_formatados.append(telefone_str)
    return telefones_formatados

# Função para realizar o sorteio e enviar mensagens
def sortear_e_enviar(planilha):
    try:
        # Carregar os dados
        dados = carregar_dados(planilha)
        if dados is None:
            return
        
        nomes = dados['Nome'].tolist()
        telefones = dados['Telefone'].tolist()

        # Formatando os números de telefone
        telefones = formatar_telefone(telefones)

        # Verificar se os números e nomes têm o mesmo tamanho
        if len(nomes) != len(telefones):
            print("A quantidade de nomes e telefones deve ser igual!")
            return

        # Sortear um nome para cada telefone
        for telefone in telefones:
            nome_sorteado = random.choice(nomes)
            mensagem = f"Olá! Você recebeu o nome sorteado: {nome_sorteado}"
            
            # Enviar mensagem pelo WhatsApp
            print(f"Enviando mensagem para {telefone}: {mensagem}")
            kit.sendwhatmsg_instantly(telefone, mensagem)
            
            
            nomes.remove(nome_sorteado)  # Remover o nome já sorteado
            time.sleep(5)  # Intervalo entre as mensagens

        print("Mensagens enviadas com sucesso!")
    except Exception as e:
        print(f"Erro durante o sorteio ou envio: {e}")

# Caminho para a planilha
caminho = 'C:/Users/DAniel/Documents/sorteio.xlsx'

# Executar a função
sortear_e_enviar(caminho)

