import streamlit as st
import yt_dlp
import os
import subprocess
import re
import time

st.set_page_config(page_title="Rádio Hub Multi-Download", page_icon="📻", layout="wide")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# Inicializa um dicionário para guardar os nomes de vários links
if 'biblioteca_nomes' not in st.session_state:
    st.session_state.biblioteca_nomes = {}

st.title("📻 Rádio Hub - Processamento em Lote")

aba1, aba2 = st.tabs(["📥 1. Links em Massa", "🔄 2. Converter Tudo"])

# --- ABA 1: MÚLTIPLOS LINKS ---
with aba1:
    st.header("Passo 1: Cole seus links")
    texto_links = st.text_area("Cole os links do YouTube (um por linha):", height=150)
    
    if st.button("Analisar todos os links"):
        links = [l.strip() for l in texto_links.split('\n') if l.strip()]
        if not links:
            st.warning("Cole pelo menos um link.")
        else:
            for idx, link in enumerate(links):
                try:
                    with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'quiet': True}) as ydl:
                        info = ydl.extract_info(link, download=False)
                        nome_limpo = limpar_nome(f"{info.get('uploader', 'Art')} - {info.get('title', 'Musica')}")
                        
                        # Guarda na memória para a aba 2
                        st.session_state.biblioteca_nomes[link] = nome_limpo
                        
                        col1, col2 = st.columns([3, 1])
                        col1.write(f"🎵 {nome_limpo}")
                        col2.markdown(f'''
                            <a href="{info['url']}" target="_blank">
                                <button style="width:100%; cursor:pointer; background-color:#ff4b4b; color:white; border:none; border-radius:5px;">
                                    Baixar Bruto
                                </button>
                            </a>
                        ''', unsafe_allow_html=True)
                except:
                    st.error(f"Erro no link: {link}")
            st.success("✅ Links processados! Baixe os arquivos e vá para a próxima aba.")

# --- ABA 2: CONVERSOR MÚLTIPLO ---
with aba2:
    st.header("Passo 2: Converter e Renomear vários")
    st.write("Arraste todos os arquivos 'videoplayback' que você baixou.")
    
    arquivos_up = st.file_uploader("Upload de arquivos", type=["weba", "webm", "m4a"], accept_multiple_files=True)

    if arquivos_up:
        if st.button("🚀 CONVERTER TUDO PARA MP3"):
            for arq in arquivos_up:
                # Tenta achar o nome original se ele estiver na biblioteca, senão usa o nome do arquivo
                # Para arquivos 'videoplayback', o ideal é converter um por um ou renomear manualmente
                nome_base = limpar_nome(os.path.splitext(arq.name)[0])
                
                # Se for o padrão 'videoplayback', tentamos dar um ID único
                if "videoplayback" in nome_base.lower():
                    nome_base = f"Musica_{int(time.time())}_{arq.size}"

                t_in = f"in_{nome_base}"
                t_out = f"out_{nome_base}.mp3"
                
                with st.status(f"Convertendo: {arq.name}...", expanded=False):
                    try:
                        with open(t_in, "wb") as f:
                            f.write(arq.getbuffer())

                        subprocess.run([
                            'ffmpeg', '-i', t_in, 
                            '-vn', '-ab', '320k', '-ar', '44100', '-y', t_out
                        ], check=True)

                        with open(t_out, "rb") as f:
                            st.download_button(
                                label=f"💾 Baixar MP3: {nome_base}",
                                data=f,
                                file_name=f"{nome_base}.mp3",
                                mime="audio/mpeg",
                                key=f"btn_{nome_base}_{time.time()}"
                            )
                        
                        if os.path.exists(t_in): os.remove(t_in)
                        if os.path.exists(t_out): os.remove(t_out)
                    except Exception as e:
                        st.error(f"Erro em {arq.name}: {e}")
