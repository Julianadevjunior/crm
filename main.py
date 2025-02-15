import streamlit as st
import defs
from datetime import datetime
import pandas as pd

if 'novo' not in st.session_state:
    st.session_state['novo'] = []

if 'container' not in st.session_state:
    st.session_state['container'] = []

dados = pd.read_excel("dados.xlsx")


def comparacao(quarto, bairro):
    dados_site = pd.read_excel("bd_imoveis.xlsx")
    oferta = False
    imovel = ""
    for linha in range(0, len(dados_site)):
        bairro_site = str(dados_site.iloc[linha, 2])
        quarto_site = str(dados_site.iloc[linha, 5])[0]

        if str(quarto) == quarto_site and bairro_site == str(bairro):
            oferta = True
            imovel = dados_site.iloc[linha, 0]

    if oferta == True:
        return imovel
    else:
        return f"Sem compatibilidade, procurar imóvel com {quartos} quartos no bairro {bairro}."


if st.button('Novo➕'):
    st.session_state['novo'].append(1)

if len(st.session_state['novo']) > 0:
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 4, 1])

        with col1:
            data_atual = datetime.today().now().strftime("%d/%m/%Y")
            st.markdown(f'{data_atual}', unsafe_allow_html=True)

        with col3:
            if st.button('✖ Fechar'):
                st.session_state['novo'] = []
                st.rerun()

        col4, col5, col6 = st.columns([10, 1, 10])

        with col4:
            nome = st.text_input(label='Nome')

        with col6:
            telefone = st.text_input(label='Telefone')

        col7, col8, col9 = st.columns([10, 1, 10])

        with col7:
            bairro = st.selectbox(label='Bairro', options=['Canto do Forte', 'Boqueirão'])

        with col9:
            quartos = st.radio(label='Quartos', options=[1, 2, 3, 4, 5], horizontal=True)

        descricao = st.text_area(label='Descrição')
        bd = pd.read_excel('dados.xlsx')
        cod = 0
        while True:
            if cod not in bd['cod']:
                break
            else:
                cod += 1
        bd.loc[len(bd)] = [cod, f'{data_atual}', f'{nome}', f'{telefone}', f'{bairro}', f'{quartos}', f'{descricao}']
        if st.button('Confirmar ➡'):
            bd.to_excel('dados.xlsx', index=False)
            st.session_state['novo'] = []
            st.rerun()

for idx, linha in enumerate(dados.values):
    cod = dados.iloc[idx, 0]
    entrada = dados.iloc[idx, 1]
    nome = dados.iloc[idx, 2]
    telefone = dados.iloc[idx, 3]
    bairro = dados.iloc[idx, 4]
    quartos = dados.iloc[idx, 5]
    descricao = dados.iloc[idx, 6]

    with st.container(border=True, key=f"box_{idx}"):
        col9, col10, col11 = st.columns([4, 1.5, 1.2])
        with col10:
            with st.container(border=True, key=f"container_data_{idx}", height=47):
                st.markdown(f"<p>{entrada}</p>", unsafe_allow_html=True)
        with col11:
            with st.expander(label="Opções"):
                if st.button(label="fechar", key=f"fechar_{idx}"):
                    dados = dados.drop(idx)
                    dados.to_excel("dados.xlsx", index=False)
                    st.rerun()
        col12, col13, col14 = st.columns([1, 2, 2])
        with col12:
            st.markdown(f"<p>Código: {cod}</p>", unsafe_allow_html=True)
        with col13:
            st.markdown(f"<p>Nome: {nome}</p>", unsafe_allow_html=True)
        with col14:
            st.markdown(f"<p>Telefone: {telefone}</p>", unsafe_allow_html=True)

        col15, col16, col17 = st.columns([2, 2, 6])
        with col15:
            st.markdown(f"<p>Quartos: {quartos}</p>", unsafe_allow_html=True)
        with col16:
            st.markdown(f"<p>Bairro: {bairro}</p>", unsafe_allow_html=True)

        with st.container(border=True, key=f"descricao_{idx}"):
            st.markdown(f"<p>Descrição:</p>", unsafe_allow_html=True)
            st.markdown(f"<p>{descricao}</p>", unsafe_allow_html=True)

        compatibilidade = comparacao(quartos, bairro)
        print(compatibilidade)
        if "Sem compatibilidade" in str(compatibilidade):
            st.error(f"{compatibilidade}")
        else:
            st.info(f"https://sitefelipe.streamlit.app/pagina_{compatibilidade}")

teste = pd.read_excel('venv/dados.xlsx')
st.write(teste)