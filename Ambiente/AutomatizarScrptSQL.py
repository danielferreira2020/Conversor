import psycopg2
import os

def execute_sql_script():
    try:
        # Verificar se o arquivo SQL existe
        sql_file_path = r'C:\caminho\para\seu\arquivo.sql'
        if not os.path.isfile(sql_file_path):
            raise FileNotFoundError(f"O arquivo {sql_file_path} não foi encontrado.")
        
        # Conectar ao banco de dados PostgreSQL usando context manager
        with psycopg2.connect(
            dbname="nome_banco",
            user="usuario",
            password="senha",
            host="localhost",  # ou o endereço do servidor PostgreSQL
            port="5432"        # substitua pela porta que seu banco usa, se for diferente
        ) as conn:
            with conn.cursor() as cursor:
                # Ler o arquivo SQL
                with open(sql_file_path, 'r') as file:
                    sql_script = file.read()

                # Executar o script SQL
                cursor.execute(sql_script)

                # Commit automático ao sair do bloco 'with'
                print("Script SQL executado com sucesso!")

    except psycopg2.OperationalError as op_err:
        print(f"Erro de conexão: {op_err}")
    except psycopg2.DatabaseError as db_err:
        print(f"Erro ao executar o SQL: {db_err}")
    except FileNotFoundError as fnf_err:
        print(fnf_err)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Executar o script SQL quando o script é chamado
if __name__ == "__main__":
    execute_sql_script()
