import xml.etree.ElementTree as ET
import pandas as pd
import re
import chardet

# Função para corrigir o formato SGML para XML
def fix_sgml_format(sgml_content):
    # Corrigir tags de fechamento não fechadas
    sgml_content = re.sub(r'<([A-Z]+)(?![^>]*>)', r'</\1>', sgml_content)
    # Corrigir tags mal fechadas e adicionar declaração XML
    sgml_content = re.sub(r'(<[A-Z]+>)(?![^<]*>)', r'\1</\1>', sgml_content)
    sgml_content = re.sub(r'<(/?[A-Z]+)>(?![^<]*<)', r'<\1>', sgml_content)  # Corrige tags abertas/fechadas
    sgml_content = sgml_content.replace('<OFX>', '<?xml version="1.0" encoding="US-ASCII"?><OFX>')
    
    # Adicionar checagem de caracteres inválidos
    sgml_content = re.sub(r'[^\x00-\x7F]+', '', sgml_content)  # Remove caracteres não-ASCII

    return sgml_content

# Função para ler o arquivo OFX e extrair transações
def parse_ofx(file_path):
    try:
        # Detectar a codificação do arquivo
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'

        # Ler o arquivo SGML com a codificação detectada
        with open(file_path, 'r', encoding=encoding) as file:
            sgml_content = file.read()

        # Corrigir o formato SGML para XML
        xml_content = fix_sgml_format(sgml_content)

        # Verificar o conteúdo XML corrigido
        with open('debug_output.xml', 'w', encoding='utf-8') as debug_file:
            debug_file.write(xml_content)

        # Analisar o conteúdo XML corrigido
        root = ET.fromstring(xml_content)

    except ET.ParseError as e:
        print(f"Erro ao analisar o arquivo XML: {e}")
        return []
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
        return []
    except Exception as e:
        print(f"Erro inesperado ao abrir o arquivo OFX: {e}")
        return []

    transactions = []

    # Navegar pela estrutura XML
    for stmt_trn in root.findall(".//STMTTRN"):
        date = stmt_trn.find("DTPOSTED").text if stmt_trn.find("DTPOSTED") is not None else ""
        amount = stmt_trn.find("TRNAMT").text if stmt_trn.find("TRNAMT") is not None else ""
        name = stmt_trn.find("PAYEEID").text if stmt_trn.find("PAYEEID") is not None else ""  # Alterado de NAME para PAYEEID
        memo = stmt_trn.find("MEMO").text if stmt_trn.find("MEMO") is not None else ""

        # Substituir vírgulas por pontos no valor monetário
        amount = amount.replace(',', '.') if amount else ""
        
        transactions.append({
            "Date": date,
            "Amount": amount,
            "Name": name,
            "Memo": memo
        })

    return transactions

# Função para salvar as transações em uma planilha Excel
def save_to_excel(transactions, output_file):
    try:
        df = pd.DataFrame(transactions)
        df.to_excel(output_file, index=False)
        print(f"Dados exportados para {output_file}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo Excel: {e}")

# Caminho para o arquivo OFX e o arquivo de saída Excel
ofx_file_path = "C:/Users/DAniel/Documents/extrato0.ofx"
excel_file_path = "C:/Users/DAniel/Documents/arquivoOFX.xlsx"

# Processar o arquivo OFX e salvar os dados em Excel
transactions = parse_ofx(ofx_file_path)
if transactions:
    save_to_excel(transactions, excel_file_path)
