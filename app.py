import streamlit as st
import yt_dlp
import os
import subprocess
import re

st.set_page_config(page_title="Rádio Hub - MP3 Pro", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# Inicializa o nome na memória do navegador para não perder entre abas
if 'nome_detectado' not in st.session_state:
    st.session_state.nome_detectado = "musica_radio"

aba1, aba2 = st.tabs(["📥 1. Pegar Link", "🔄 2. Converter e Renomear"])

# --- ABA 1: PEGAR O LINK E O NOME ---
with aba1:
    st.header("Passo 1: Baixar o áudio bruto")
    link_yt = st.text_input("Cole o link do YouTube aqui:")
    
    if link_yt:
        with st.spinner("Buscando informações..."):
            try:
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link_yt, download=False)
                    artista = info.get('uploader', 'Artista').replace(' - Topic', '')
                    titulo = info.get('title', 'Musica')
                    
                    # Salva o nome para usar na outra aba
                    st.session_state.nome_detectado = limpar_nome(f"{artista} - {titulo}")
                    
                    st.success(f"🎵 Pronto: {st.session_state.nome_detectado}")
                    
                    st.markdown(f'''
                        <a href="{info['url']}" target="_blank">
                            <button style="background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:5px; cursor:pointer; font-weight:bold; width:100%;">
                                📥 BAIXAR ARQUIVO "VIDEOPLAYBACK"
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                    st.info("Após o download terminar, clique na aba '2. Converter e Renomear'.")
            except Exception as e:
                st.error("Erro ao acessar o YouTube. Tente outro link.")

# --- ABA 2: CONVERSOR (MP3 320kbps) ---
with aba2:
    st.header("Passo 2: Gerar MP3 Final")
    st.write(f"Arquivo será renomeado como: **{st.session_state.nome_detectado}.mp3**")
    
    arquivo_bruto = st.file_uploader("Suba o arquivo 'videoplayback' aqui", type=["weba", "webm", "m4a"])

    if arquivo_bruto:
        if st.button("🚀 CONVERTER AG
