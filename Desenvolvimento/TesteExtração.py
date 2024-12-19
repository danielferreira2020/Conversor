import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
import os

# Função para criar o PDF
def criar_pdf(nome_arquivo):
    url = 'https://pt.wikipedia.org/wiki/P%C3%A1gina_principal'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        headers = soup.find_all(['h1', 'h2', 'h3'])
        for header in headers:
            pdf.multi_cell(0, 10, header.get_text())
            pdf.ln()

        pdf.output(nome_arquivo)
        print("PDF gerado com sucesso!")
    else:
        print(f'Falha ao acessar a página. Status code: {response.status_code}')

# Função para enviar e-mail
def enviar_email(nome_arquivo, destinatario_email, remetente_email, remetente_senha):
    # Configurações do e-mail
    smtp_server = 'smtp.example.com'  # Substitua pelo servidor SMTP do seu provedor de e-mail
    smtp_port = 587  # Porta para SMTP com TLS

    # Criar o e-mail
    msg = MIMEMultipart()
    msg['From'] = formataddr(('Seu Nome', remetente_email))
    msg['To'] = destinatario_email
    msg['Subject'] = 'Aqui está o PDF solicitado'

    # Adicionar o corpo do e-mail
    corpo = MIMEText('Olá,\n\nEm anexo está o arquivo PDF solicitado.\n\nAtenciosamente,\nSeu Nome', 'plain')
    msg.attach(corpo)

    # Adicionar o anexo
    with open(nome_arquivo, 'rb') as arquivo_pdf:
        anexo = MIMEApplication(arquivo_pdf.read(), _subtype='pdf')
        anexo.add_header('Content-Disposition', 'attachment', filename=nome_arquivo)
        msg.attach(anexo)

    # Enviar o e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as servidor:
        servidor.starttls()
        servidor.login(remetente_email, remetente_senha)
        servidor.send_message(msg)

    print("E-mail enviado com sucesso!")

# Defina os parâmetros
nome_arquivo = 'titulos_wikipedia.pdf'
remetente_email = 'seuemail@example.com'
# Use uma variável de ambiente para a senha, se possível
remetente_senha = os.getenv('EMAIL_PASSWORD', 'suasenha')  # Substitua 'suasenha' com uma senha segura
destinatario_email = 'destinatario@example.com'

# Criar o PDF
criar_pdf(nome_arquivo)

# Enviar o e-mail
enviar_email(nome_arquivo, destinatario_email, remetente_email, remetente_senha)
