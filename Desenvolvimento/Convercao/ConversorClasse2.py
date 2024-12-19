import streamlit as st
import pandas as pd
import io  # Biblioteca para manipular arquivos em memória
import datetime

# Função para formatar o valor da parcela
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

# Função para gerar o arquivo TXT no formato final (agora usa StringIO)
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

# Obter mês e ano atual
mes_ano_atual = datetime.datetime.now().strftime("%m%Y")

# Interface do Streamlit para entrada de dados
st.title('📝 Gerador de Arquivo TXT - Layout Personalizado')

# Criar uma lista de registros
if 'dados' not in st.session_state:
    st.session_state['dados'] = []

# Formulário para adicionar os campos
with st.form("formulario"):
    matricula = st.text_input('Matrícula (máx. 10 dígitos)', value='542')
    cpf = st.text_input('CPF', value='00123456789')
    nome = st.text_input('Nome do Servidor', value='LILIAN CRISTIANE DO AMARAL')
    codigo_desconto = st.text_input('Código de Desconto', value='1234')
    valor_parcela = st.text_input('Valor da Parcela', value='12000')
    prazo_total = st.text_input('Prazo Total', value='999')
    competencia = st.text_input('Competência (MMAAAA)', value=mes_ano_atual)
    codigo_operacao = st.selectbox('Código de Operação', ['I', 'A', 'E'])

    submit_button = st.form_submit_button('Adicionar Registro')

    if submit_button:
        st.session_state['dados'].append({
            'matricula': matricula,
            'cpf': cpf,
            'nome': nome,
            'codigo_estabelecimento': '001',
            'orgao': '001',
            'codigo_desconto': codigo_desconto,
            'valor_parcela': formatar_valor_parcela(valor_parcela),
            'prazo_total': prazo_total,
            'competencia': competencia,
            'codigo_operacao': codigo_operacao
        })
        st.success('✅ Registro adicionado com sucesso!')

# Exibir a tabela de registros adicionados
if len(st.session_state['dados']) > 0:
    df = pd.DataFrame(st.session_state['dados'])
    st.write('📋 **Registros Adicionados:**')
    st.dataframe(df)

    # **Selecionar registro para editar ou excluir**
    opcoes = [f"Registro {i+1} - {row['nome']}" for i, row in df.iterrows()]
    registro_selecionado = st.selectbox('Selecione um registro para editar ou excluir', options=opcoes)

    # Identificar o índice do registro selecionado
    indice_selecionado = opcoes.index(registro_selecionado)

    # **Botão para excluir o registro**
    if st.button('❌ Excluir Registro'):
        st.session_state['dados'].pop(indice_selecionado)
        st.success('✅ Registro excluído com sucesso!')
        st.experimental_rerun()

    # **Botão para editar o registro**
    if st.button('✏️ Editar Registro'):
        registro = st.session_state['dados'][indice_selecionado]

        # Formulário para edição do registro
        with st.form("formulario_edicao"):
            matricula_edit = st.text_input('Matrícula', value=registro['matricula'])
            cpf_edit = st.text_input('CPF', value=registro['cpf'])
            nome_edit = st.text_input('Nome do Servidor', value=registro['nome'])
            codigo_desconto_edit = st.text_input('Código de Desconto', value=registro['codigo_desconto'])
            valor_parcela_edit = st.text_input('Valor da Parcela', value=registro['valor_parcela'])
            prazo_total_edit = st.text_input('Prazo Total', value=registro['prazo_total'])
            competencia_edit = st.text_input('Competência (MMAAAA)', value=registro['competencia'])
            codigo_operacao_edit = st.selectbox('Código de Operação', ['I', 'A', 'E'], index=['I', 'A', 'E'].index(registro['codigo_operacao']))

            salvar_edicao = st.form_submit_button('Salvar Edição')

            if salvar_edicao:
                st.session_state['dados'][indice_selecionado] = {
                    'matricula': matricula_edit,
                    'cpf': cpf_edit,
                    'nome': nome_edit,
                    'codigo_estabelecimento': '001',
                    'orgao': '001',
                    'codigo_desconto': codigo_desconto_edit,
                    'valor_parcela': formatar_valor_parcela(valor_parcela_edit),
                    'prazo_total': prazo_total_edit,
                    'competencia': competencia_edit,
                    'codigo_operacao': codigo_operacao_edit
                }
                st.success('✅ Registro editado com sucesso!')
                st.experimental_rerun()

    # Gerar o conteúdo do arquivo TXT (em memória)
    arquivo_txt = gerar_arquivo_txt(df)
    
    # Botão de download para baixar o arquivo TXT
    st.download_button(
        label='📥 Baixar Arquivo TXT',
        data=arquivo_txt,
        file_name='Arqui_confor_Layout.txt',
        mime='text/plain'
    )