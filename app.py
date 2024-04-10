import streamlit as st
import sqlite3

# Função para conectar ao banco de dados SQLite
def conectar_banco_dados():
    return sqlite3.connect('ordens.db')

# Função para listar todas as ordens presentes no banco de dados
def listar_ordens():
    conn = conectar_banco_dados()
    c = conn.cursor()
    c.execute("SELECT * FROM ordens")
    ordens = c.fetchall()
    conn.close()
    return ordens

# Função para pesquisar as ordens no banco de dados com base nos critérios fornecidos
def pesquisar_ordens(local_instalacao, ano, den_origem):
    conn = conectar_banco_dados()
    c = conn.cursor()
    query = "SELECT * FROM ordens WHERE 1=1"
    params = []
    if local_instalacao:
        query += " AND local_instalacao LIKE ?"
        params.append(f"%{local_instalacao}%")
    if ano:
        query += " AND ano LIKE ?"
        params.append(f"%{ano}%")
    if den_origem:
        query += " AND den_origem = ?"  # Modificado para uma correspondência exata em vez de pesquisa com LIKE
        params.append(den_origem)  # Não precisa de '%'
    c.execute(query, params)
    ordens = c.fetchall()
    conn.close()
    return ordens

# Função para adicionar uma nova ordem ao banco de dados
def adicionar_ordem(numero_pasta, pagina, local_instalacao, ano, den_origem):
    conn = conectar_banco_dados()
    c = conn.cursor()
    c.execute("INSERT INTO ordens (numero_pasta, pagina, local_instalacao, ano, den_origem) VALUES (?, ?, ?, ?, ?)",
              (numero_pasta, pagina, local_instalacao, ano, den_origem))
    conn.commit()
    conn.close()

# Função para obter todas as denominações de origem únicas do banco de dados
def obter_denominacoes_origem():
    conn = conectar_banco_dados()
    c = conn.cursor()
    c.execute("SELECT DISTINCT den_origem FROM ordens")
    denominacoes = [row[0] for row in c.fetchall()]
    conn.close()
    return denominacoes

# Configurar o título do aplicativo
st.title('G.S Localizador')

# Adicionar controles de entrada para inserir os dados da ordem
st.sidebar.header('Inserir Nova Ordem')
nova_pasta = st.sidebar.text_input('Número da Pasta')
nova_pagina = st.sidebar.number_input('Página', min_value=1, max_value=100, step=1)
local_instalacao = st.sidebar.text_input('Local de Instalação')
ano = st.sidebar.text_input('Ano')
den_origem = st.sidebar.selectbox('Denominação de Origem', obter_denominacoes_origem())

# Adicionar os novos dados da ordem ao banco de dados quando o botão for clicado
if st.sidebar.button('Adicionar Ordem'):
    adicionar_ordem(nova_pasta, nova_pagina, local_instalacao, ano, den_origem)
    st.sidebar.success('Ordem adicionada com sucesso!')

# Adicionar controles de entrada para pesquisa de ordens
pesquisar_local_instalacao = st.text_input('Pesquisar por Local de Instalação')
pesquisar_ano = st.text_input('Pesquisar por Ano')
pesquisar_den_origem = st.selectbox('Pesquisar por Denominação de Origem', [''] + obter_denominacoes_origem())

# Botão para acionar a pesquisa
if st.button('Buscar'):
    # Verificar se os campos de pesquisa estão vazios
    if not (pesquisar_local_instalacao or pesquisar_ano or pesquisar_den_origem):
        st.warning('Por favor, preencha pelo menos um campo de pesquisa.')
    else:
        # Pesquisar as ordens no banco de dados
        ordens_filtradas = pesquisar_ordens(pesquisar_local_instalacao, pesquisar_ano, pesquisar_den_origem)

        # Exibir as ordens filtradas se a pesquisa for realizada
        if ordens_filtradas:
            st.success('Ordens encontradas:')
            for ordem in ordens_filtradas:
                st.success(f"A ordem cujo o local de instalação é  {ordem[3]}, e sua  Denominação de Origem é : {ordem[5]}, está na  pasta: {ordem[1]}, na página: {ordem[2]}")
        else:
            st.error('Nenhuma ordem encontrada com os critérios de pesquisa fornecidos.')
