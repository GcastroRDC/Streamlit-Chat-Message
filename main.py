import streamlit as st
from unidecode import unidecode
import pickle
import time
from pathlib import Path

PASTA_MENSAGENS = Path(__file__).parent / 'mensagens'
PASTA_MENSAGENS.mkdir(exist_ok=True)

PASTA_USUARIOS = Path(__file__).parent / 'usuarios'
PASTA_USUARIOS.mkdir(exist_ok=True)


def le_mensagens_armazenadas(usuario,conversando_com):

    nome_arquivo = nome_arquivo_armazenado(usuario,conversando_com)

    if (PASTA_MENSAGENS / nome_arquivo).exists():

        with open(PASTA_MENSAGENS / nome_arquivo, 'rb') as f:

            return pickle.load(f)
        
    else:

        return []

        
def armazena_mensagens(usuario,conversando_com,mensagens):

    nome_arquivo = nome_arquivo_armazenado(usuario,conversando_com)

    with open(PASTA_MENSAGENS / nome_arquivo,'wb') as f:
        pickle.dump(mensagens,f)


def nome_arquivo_armazenado(usuario,conversando_com):

    nome_arquivo = [usuario,conversando_com]
    nome_arquivo.sort()
    nome_arquivo = [u.replace(' ','_') for u in nome_arquivo]
    nome_arquivo = [unidecode(u) for u in nome_arquivo]

    return '&'.join(nome_arquivo).lower()

def salvar_novo_usuario(nome, senha):

    nome_arquivo = unidecode(nome.replace(' ','_').lower())

    if (PASTA_USUARIOS / nome_arquivo).exists():

        return False
    
    with open(PASTA_USUARIOS / nome_arquivo,'wb') as f:

        pickle.dump({'nome_usuario':nome,'senha':senha},f)

        return True

def validacao_senha(nome,senha):

    nome_arquivo = unidecode(nome.replace(' ','-').lower())

    if not (PASTA_USUARIOS / nome_arquivo).exists():

        return False
    
    else:

        with open(PASTA_USUARIOS / nome_arquivo,'rb') as f:

            arquivo_dados = pickle.load(f)

        return arquivo_dados['senha'] == senha
         
def mudar_pagina(nome_pagina):

    st.session_state['pagina_atual'] = nome_pagina

def cadastrar_usuario(nome,senha):

    if salvar_novo_usuario(nome,senha):

        st.success('Usuário cadastrado com sucesso')
        time.sleep(2)
        st.session_state['usuario_logado' ] = nome.upper()
        mudar_pagina('chat')
        st.rerun()

    else:

        st.error('Error ao cadastrar usuário')

def inicializacao():

    if not 'pagina_atual' in st.session_state:
        mudar_pagina('login')
    if not 'usuario_logado' in st.session_state:
        st.session_state['usuario_logado' ] = ''

def pagina_login():

    st.header('Bem-vindo ao Streamlit Messeger',divider=True)
    tab1,tab2 = st.tabs(['Entrar','Cadastrar'])

    with tab1.form(key='login'):

        nome = st.text_input('Digite o nome do seu usuário')
        senha = st.text_input('Digite sua senha')
        if st.form_submit_button('Entrar'):

            login_usuario(nome,senha)

    with tab2.form(key='cadastrar'):

        nome = st.text_input('Cadastre um novo nome de usuário')
        senha = st.text_input('Cadastre uma nova senha')

        if st.form_submit_button('Cadastrar'):

            cadastrar_usuario(nome,senha)

def login_usuario(nome,senha):
    if validacao_senha(nome,senha):

        st.success('Login realizado com sucesso')
        time.sleep(2)
        st.session_state['usuario_logado' ] = nome.upper()
        mudar_pagina('chat')
        st.rerun()
    
    else:

        st.error('Erro ao logar')
def pagina_chat():

    st.title("💬 Streamlit Chat Message ")
    st.divider()

    usuario_logado = st.session_state['usuario_logado' ] 
    conversando_com = 'RODRIGO'

    mensagens = le_mensagens_armazenadas(usuario_logado,conversando_com)

    for mensagem in mensagens:

        nome_usuario = mensagem['nome_usuario'] if mensagem['nome_usuario'] != usuario_logado else 'user'
        avatar = None if mensagem['nome_usuario'] == usuario_logado else '🤖'
        chat = st.chat_message(nome_usuario, avatar = avatar)
        chat.markdown(mensagem['conteudo'])
    
    nova_mensagem = st.chat_input('Digite uma mensagem')
    if nova_mensagem:
        nova_dict_mensagem = {'nome_usuario':usuario_logado,
                         'conteudo':nova_mensagem}
        
        chat = st.chat_message('user')
        chat.markdown(nova_dict_mensagem['conteudo'])
        mensagens.append(nova_dict_mensagem)
        armazena_mensagens(usuario_logado,conversando_com,mensagens)

def main():

    if not 'pagina_atual' in st.session_state:

        mudar_pagina('login')

    if st.session_state['pagina_atual'] == 'login':

        pagina_login()

    if st.session_state['pagina_atual'] == 'chat':

        pagina_chat()
    

if __name__ == '__main__':
    main()
