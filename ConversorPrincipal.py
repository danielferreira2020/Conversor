import streamlit as st
import pandas as pd
import io
import datetime


# Classe base com métodos comuns
class ClasseBase:
    def __init__(self):
        pass

    def exibir_mensagem_erro(self, mensagem):
        st.error(f"Erro: {mensagem}")


# Classe 1: Conversão baseada na primeira lógica
class Classe1(ClasseBase):
    def formatar_linha(self, linha):
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

    def processar_arquivo(self, conteudo):
        linhas = conteudo.split('\n')
        linhas_formatadas = [self.formatar_linha(linha) for linha in linhas if linha.strip()]
        return '\n'.join(linhas_formatadas)


# Classe 2: Conversão baseada na segunda lógica
class Classe2(ClasseBase):
    def formatar_valor_parcela(self, valor):
        valor = valor.replace(",", ".")
        if valor.isdigit():
            valor = str(int(valor) / 100)
        try:
            valor = float(valor)
            valor = f"{valor:.2f}"
        except ValueError:
            valor = "0.00"
        return valor

    def gerar_arquivo_txt(self, dados):
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


# Classe 3: Converter arquivo para arquivo TXT
class Classe3:
    def formatar_linha(self, linha):
        """
        Formata uma linha com base no layout especificado.
        """
        partes = [parte.strip() for parte in linha.split(';')]

        if len(partes) < 6:
            print(f"Linha ignorada (menos de 6 campos): {linha}")
            return None

        try:
            # Matricula (Campo 1): Alinhar à direita com zeros à esquerda
            matricula = partes[0].zfill(15)

            # CPF (Campo 3): Apenas números, alinhar à direita com zeros
            cpf = ''.join(filter(str.isdigit, partes[2])).zfill(11)

            # Valor a ser descontado (Campo 5): Converter para float e formatar com vírgula
            valor = f"{float(partes[4]):,.2f}".replace('.', ',')

            # Ano e mês da folha (Campo 6): Apenas números, formato AAAAMM
            ano_mes = ''.join(filter(str.isdigit, partes[5]))

            # Nome do cliente (Campo 8): Apenas o nome completo
            nome_cliente = partes[7]

            # Monta a linha formatada
            linha_formatada = (
                f"{matricula};"  # Campo 1
                f",;"  # Campo 2 delimitador
                f"{cpf};"  # Campo 3
                f",;"  # Campo 4 delimitador
                f"{valor};"  # Campo 5
                f",;"  # Campo 6 delimitador
                f"LIFCC;"  # Campo 7 constante
                f",;"  # Campo 8 delimitador
                f"{ano_mes};"  # Campo 9
                f",;"  # Campo 10 delimitador
                f"{nome_cliente};"  # Campo 11
                f",;"  # Campo 12 delimitador
            )

            return linha_formatada

        except ValueError as e:
            print(f"Erro ao processar linha: {linha}\n{e}")
            return None

    def processar_arquivo(self, conteudo):
        """
        Processa um arquivo inteiro, formatando cada linha.
        """
        linhas = conteudo.split('\n')
        linhas_formatadas = [self.formatar_linha(linha) for linha in linhas if linha.strip()]
        return '\n'.join(filter(None, linhas_formatadas))

# Classe Principal que gerencia as interações
class ClassePrincipal:
    def __init__(self):
        self.opcoes_classes = {
            'ConsigSimples': Classe1(),
            'eConsig': Classe2(),
            'SafeConsig': Classe3()
        }
    def executar(self):
        st.title('📝 Conversor de Arquivos de Lote')

        # Adiciona a seleção da classe na barra lateral
        classe_selecionada = st.sidebar.radio("Escolha o método de conversão:", list(self.opcoes_classes.keys()))
        
        # Exibe o conteúdo correspondente à classe selecionada
        if classe_selecionada == 'ConsigSimples':
            self.interface_classe1()
        elif classe_selecionada == 'eConsig':
            self.interface_classe2()
        elif classe_selecionada == 'SafeConsig':
            self.interface_classe3()

    def interface_classe1(self):
        conversor = self.opcoes_classes['ConsigSimples']
        st.subheader('🔄 Conversão Para ConsigSimples')
        arquivo_txt = st.file_uploader("Selecione o arquivo .txt para conversão", type=['txt'])

        if arquivo_txt is not None:
            conteudo = arquivo_txt.getvalue().decode('utf-8')
            st.text_area("Conteúdo do arquivo de entrada", conteudo, height=200)

            if st.button("Converter Arquivo", key="btn_converter_classe1"):
                try:
                    conteudo_convertido = conversor.processar_arquivo(conteudo)
                    st.text_area("Conteúdo do arquivo convertido", conteudo_convertido, height=200)
                    st.download_button("📥 Baixar Arquivo Convertido", conteudo_convertido, "arquivo_convertido_classe1.txt", "text/plain")
                except Exception as e:
                    conversor.exibir_mensagem_erro(e)

    def interface_classe2(self):
        conversor = self.opcoes_classes['eConsig']
        st.subheader('🆕 Conversão Para eConsig')

        mes_ano_atual = datetime.datetime.now().strftime("%m%Y")

        # Criar uma lista de registros
        if 'dados' not in st.session_state:
            st.session_state['dados'] = []

        # Formulário para adicionar os campos
        with st.form("formulario"):
            matricula = st.text_input('Matrícula (máx. 10 dígitos)', value='542')
            cpf = st.text_input('CPF', value='00123456789')
            nome = st.text_input('Nome do Servidor', value='Vinicius Ferinha')
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
                    'valor_parcela': conversor.formatar_valor_parcela(valor_parcela),
                    'prazo_total': prazo_total,
                    'competencia': competencia,
                    'codigo_operacao': codigo_operacao
                })
                st.success('✅ Registro adicionado com sucesso!')
                st.session_state['matricula'] = ''
                st.session_state['cpf'] = ''
                st.session_state['nome'] = ''     


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

            # **Botões de excluir, editar e limpar lado a lado**
            col1, col2, col3 = st.columns(3)  # Cria três colunas para os botões ficarem lado a lado

            with col1:
                # **Botão para excluir o registro**
                if st.button('❌ Excluir Registro'):
                    st.session_state['dados'].pop(indice_selecionado)
                    st.success('✅ Registro excluído com sucesso!')
                    st.rerun()  # Atualiza a interface após a exclusão

            with col2:
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
                        codigo_operacao_edit = st.selectbox(
                            'Código de Operação', 
                            ['I', 'A', 'E'], 
                            index=['I', 'A', 'E'].index(registro['codigo_operacao'])
                        )

                        salvar_edicao = st.form_submit_button('Salvar Edição')

                        if salvar_edicao:
                            st.session_state['dados'][indice_selecionado] = {
                                'matricula': matricula_edit,
                                'cpf': cpf_edit,
                                'nome': nome_edit,
                                'codigo_estabelecimento': '001',
                                'orgao': '001',
                                'codigo_desconto': codigo_desconto_edit,
                                'valor_parcela': conversor.formatar_valor_parcela(valor_parcela_edit),
                                'prazo_total': prazo_total_edit,
                                'competencia': competencia_edit,
                                'codigo_operacao': codigo_operacao_edit
                            }
                            st.success('✅ Registro editado com sucesso!')
                            st.rerun()  # Atualiza a interface após a edição

            with col3:
                # **Botão para limpar todos os registros**
                if st.button('🧹 Limpar Registros'):
                    st.session_state['dados'] = []
                    st.success('✅ Todos os registros foram limpos com sucesso!')
                    st.rerun()  # Atualiza a interface após a limpeza
            
            # Gerar o conteúdo do arquivo TXT (em memória)
            arquivo_txt = conversor.gerar_arquivo_txt(pd.DataFrame(st.session_state['dados']))

            # Botão de download para baixar o arquivo TXT
            st.download_button(
                label='📥 Baixar Arquivo TXT',
                data=arquivo_txt,
                file_name='Arqui_confor_Layout.txt',
                mime='text/plain'
            )


    def interface_classe3(self):
        conversor = self
        st.subheader('📄 Conversão Para SafeConsig')
        arquivo_excel = st.file_uploader("Selecione o arquivo .xlsx para conversão", type=['xlsx'])

        if arquivo_excel is not None:
            conteudo_excel = pd.read_excel(arquivo_excel)
            conteudo_txt = ''

            for _, row in conteudo_excel.iterrows():
                linha = ';'.join(map(str, row.values))
                linha_formatada = conversor.formatar_linha(linha)
                if linha_formatada:
                    conteudo_txt += linha_formatada + '\n'

            if conteudo_txt:
                st.text_area("Conteúdo do arquivo convertido", conteudo_txt, height=200)
                st.download_button("📥 Baixar Arquivo Convertido", conteudo_txt, "arquivo_convertido_classe3.txt", "text/plain")



# Execução da classe principal
if __name__ == "__main__":
    app = ClassePrincipal()
    app.executar()
    