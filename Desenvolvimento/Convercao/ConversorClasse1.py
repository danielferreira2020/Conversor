import streamlit as st
import pandas as pd
import io  # Biblioteca para manipular arquivos em memória
import datetime
import re

# Classe 1: Conversão baseada na primeira lógica
class ConversorClasse1:
    @staticmethod
    def formatar_linha(linha):
        partes = [parte.strip() for parte in linha.split(';')]
        partes[0] = partes[0].lstrip('0')  # Remove zeros à esquerda do primeiro campo
        partes[1] = partes[1][:11]         # Mantém apenas os 11 primeiros dígitos do segundo campo
        partes[2] = partes[1][11:]         # Captura os 3 dígitos seguintes e coloca no terceiro campo
        partes[3] = partes[3]              # Mantém o quarto campo sem alteração
        partes[4] = str(float(partes[4]) / 100).replace('.', ',')  # Converte o valor e formata para padrão brasileiro
        return ';'.join(partes)

    @staticmethod
    def processar_arquivo(conteudo):
        linhas = conteudo.split('\n')
        linhas_formatadas = [ConversorClasse1.formatar_linha(linha) for linha in linhas if linha.strip()]
        return '\n'.join(linhas_formatadas)

# Classe 2: Conversão baseada na segunda lógica
class ConversorClasse2:
    @staticmethod
    def formatar_valor_parcela(valor):
        valor = valor.replace(",", ".")
        if valor.isdigit():
            valor = str(int(valor) / 100)
        try:
            valor = float(valor)
            valor = f"{valor:.2f}"
        except ValueError:
            valor = "0.00"
        return valor

    @staticmethod
    def gerar_arquivo_txt(dados):
        output = io.StringIO()
        for index, row in dados.iterrows():
            linha = (
                f"{row['matricula'].zfill(10)}"
                f"{row['cpf'].zfill(11)}"
                f"{row['nome'].upper():<50}"
                f"{row['codigo_estabelecimento']:>3}"
                f"{row['orgao']:>3}"
                f"{row['codigo_desconto']:<4}"
                f"{str(row['valor_parcela']).zfill(10)}"
                f"{str(row['prazo_total']).zfill(3)}"
                f"{row['competencia']}"
                f"{row['codigo_operacao']}"
            )
            output.write(linha + '\n')
        return output.getvalue()

# Interface do Streamlit
st.title('📝 Conversor de Arquivos TXT')

# Opção para selecionar a classe de conversão
classe_selecionada = st.radio("Escolha o método de conversão:", ('Classe 1', 'Classe 2'))

if classe_selecionada == 'Classe 1':
    st.subheader('🔄 Conversão pela Classe 1')
    
    # Upload do arquivo TXT
    arquivo_txt = st.file_uploader("Selecione o arquivo .txt para conversão", type=['txt'])
    
    if arquivo_txt is not None:
        conteudo = arquivo_txt.getvalue().decode('utf-8')
        st.text_area("Conteúdo do arquivo de entrada", conteudo, height=200)
        
        if st.button("Converter Arquivo", key="btn_converter_classe1"):
            try:
                conteudo_convertido = ConversorClasse1.processar_arquivo(conteudo)
                st.text_area("Conteúdo do arquivo convertido", conteudo_convertido, height=200)
                
                # Botão para download do arquivo convertido
                st.download_button(
                    label="📥 Baixar Arquivo Convertido", 
                    data=conteudo_convertido, 
                    file_name="arquivo_convertido_classe1.txt", 
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Erro ao converter o arquivo: {e}")

elif classe_selecionada == 'Classe 2':
    st.subheader('🆕 Conversão pela Classe 2')
    
    # Formulário para entrada de dados
    matricula = st.text_input("Matrícula", max_chars=10)
    cpf = st.text_input("CPF", max_chars=11)
    nome = st.text_input("Nome", max_chars=50)
    codigo_estabelecimento = st.text_input("Código do Estabelecimento", max_chars=3)
    orgao = st.text_input("Órgão", max_chars=3)
    codigo_desconto = st.text_input("Código de Desconto", max_chars=4)
    valor_parcela = st.text_input("Valor da Parcela", max_chars=10)
    prazo_total = st.text_input("Prazo Total", max_chars=3)
    competencia = st.text_input("Competência", max_chars=6)
    codigo_operacao = st.text_input("Código de Operação", max_chars=10)
    
    if st.button("Gerar Arquivo", key="btn_gerar_classe2"):
        try:
            dados = pd.DataFrame([{
                'matricula': matricula,
                'cpf': cpf,
                'nome': nome,
                'codigo_estabelecimento': codigo_estabelecimento,
                'orgao': orgao,
                'codigo_desconto': codigo_desconto,
                'valor_parcela': ConversorClasse2.formatar_valor_parcela(valor_parcela),
                'prazo_total': prazo_total,
                'competencia': competencia,
                'codigo_operacao': codigo_operacao
            }])
            conteudo_arquivo = ConversorClasse2.gerar_arquivo_txt(dados)
            st.text_area("Conteúdo do arquivo gerado", conteudo_arquivo, height=200)
            
            # Botão para download do arquivo gerado
            st.download_button(
                label="📥 Baixar Arquivo Gerado", 
                data=conteudo_arquivo, 
                file_name="arquivo_gerado_classe2.txt", 
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Erro ao gerar o arquivo: {e}")
