#AUTOR: DANIEL FERREIRA SOARES DA SILVA#
import psycopg2

try:
    # Conectar ao banco de dados
    conn = psycopg2.connect(
        dbname="faturamento_convenios",
        user="daniel.soares",
        password="daniel.RC",
        host="localhost",
        port="3080"
    )

    # Criar um cursor
    cur = conn.cursor()

    # Chamar o procedimento armazenado
    proc_name = "stages_rc_card.carga_faturamento_2024"
    cur.callproc(proc_name)
    
    # Obter e processar resultados, se necessário
    result = cur.fetchall()
    print(result)

    # Confirmar as alterações
    conn.commit()

except Exception as e:
    print(f"Erro: {e}")
    if conn:
        conn.rollback()

finally:
    # Fechar cursor e conexão
    if cur:
        cur.close()
    if conn:
        conn.close()
