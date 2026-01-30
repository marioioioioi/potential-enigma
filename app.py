import streamlit as st
import yt_dlp
import os
import subprocess
import re

st.set_page_config(page_title="Rádio Hub - MP3 Pro", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

aba1, aba2 = st.tabs(["📥 1. Pegar Link (YouTube)", "🔄 2. Converter e Renomear"])

# --- ABA 1: APENAS PARA PEGAR O LINK DIRETO ---
with aba1:
    st.header("Passo 1: Baixar o áudio bruto")
    link_yt = st.text_input("Cole o link do YouTube aqui:")
    if link_yt:
        with st.spinner("Gerando link de download..."):
            try:
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link_yt, download=False)
                    st.success(f"Vídeo encontrado: {info['title']}")
                    st.markdown(f'''
                        <a href="{info['url']}" target="_blank">
                            <button style="background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:5px; cursor:pointer; font-weight:bold;">
                                📥 BAIXAR ARQUIVO BRUTO (.weba)
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                    st.info("Após baixar o arquivo 'videoplayback', vá para a aba 'Converter e Renomear'.")
            except Exception as e:
                st.error("Erro ao acessar o YouTube. Tente outro link.")

# --- ABA 2: CONVERSOR QUE RENOMEIA SOZINHO ---
with aba2:
    st.header("Passo 2: Transformar em MP3 com Nome")
    st.write("Suba o arquivo 'videoplayback' e cole o link novamente para eu saber o nome da música.")
    
    link_para_nome = st.text_input("Cole o link do vídeo novamente (para eu renomear):", key="nome_link")
    arquivo_bruto = st.file_uploader("Suba o arquivo .weba aqui", type=["weba", "webm", "m4a"])

    if arquivo_bruto and link_para_nome:
        if st.button("🚀 CONVERTER E RENOMEAR AGORA"):
            with st.spinner("Processando..."):
                try:
                    # 1. Busca o nome real da música
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        info = ydl.extract_info(link_para_nome, download=False)
                        artista = info.get('uploader', 'Artista').replace(' - Topic', '')
                        titulo = info.get('
