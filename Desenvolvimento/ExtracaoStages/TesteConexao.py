#AUTOR: DANIEL FERREIRA SOARES DA SILVA#
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import psycopg2
import os

dbname = os.getenv('DB_NAME', 'default_dbname')
user = os.getenv('DB_USER', 'default_user')
password = os.getenv('DB_PASSWORD', 'default_password')
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '3080')

with psycopg2.connect(
    dbname=dbname,
    user="daniel.soares",
    password="daniel.rc",
    host="localhost",
    port="3080"
) as conn:
    # Teste de conexão
        print("Conexão bem-sucedida!")
