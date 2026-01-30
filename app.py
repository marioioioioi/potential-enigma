import streamlit as st
import yt_dlp
import os
import re
import shutil

st.set_page_config(page_title="Rádio Hub v2026 - Versão Premium", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("📻 Sistema de Rádio")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if senha == "radio123":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

st.title("📻 Download Sem Bloqueio (Modo Cookies)")

# Verifica se o arquivo de cookies existe
if not os.path.exists("cookies.txt"):
    st.error("⚠️ Arquivo 'cookies.txt' não encontrado no servidor! O erro 403 pode voltar.")
else:
    st.success("✅ Sistema de Cookies ativo. Bloqueio 403 contornado.")

link = st.text_input("Cole o link do YouTube:")

if st.button("Gerar MP3"):
    if link:
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
        os.makedirs("downloads")

        with st.spinner("Baixando áudio oficial..."):
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None, # AQUI ESTÁ A MÁGICA
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': 'downloads/%(uploader)s - %(title)s.%(ext)s',
                    'nocheckcertificate': True,
                    'rm_cachedir': True,
                    'quiet': False
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    file_path = ydl.prepare_filename(info)
                    mp3_path = os.path.splitext(file_path)[0] + ".mp3"
                    
                    if os.path.exists(mp3_path):
                        with open(mp3_path, "rb") as f:
                            st.download_button(
                                label="📥 SALVAR MP3 (320kbps)",
                                data=f,
                                file_name=os.path.basename(mp3_path),
                                mime="audio/mpeg"
                            )
                    else:
                        st.error("Erro na conversão.")
            except Exception as e:
                st.error(f"Erro: {e}")
