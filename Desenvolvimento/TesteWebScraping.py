import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

# URL do site que queremos raspar
url = 'https://pt.wikipedia.org/wiki/P%C3%A1gina_principal'

# Enviar uma solicitação para a página
response = requests.get(url)

# Verificar se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Criar um objeto BeautifulSoup para analisar o conteúdo HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Criar um objeto FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Encontrar todos os títulos na página (exemplo com <h1>, <h2>, <h3>, etc.)
    headers = soup.find_all(['h1', 'h2', 'h3'])

    for header in headers:
        # Adicionar cada título ao PDF
        pdf.multi_cell(0, 10, header.get_text())
        pdf.ln()  # Adicionar uma nova linha

    # Salvar o PDF em um arquivo
    pdf.output("titulos_wikipedia.pdf")

    print("PDF gerado com sucesso!")

else:
    print(f'Falha ao acessar a página. Status code: {response.status_code}')
