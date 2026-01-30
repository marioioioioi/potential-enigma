import streamlit as st
import yt_dlp
import os
import re
import shutil

st.set_page_config(page_title="Rádio Hub v2026", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# --- SISTEMA DE SENHA ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 Acesso Rádio")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if senha == "radio123":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

st.title("📻 Rádio Hub - Sistema Anti-Bloqueio")

# Verifica se o arquivo de cookies está presente
if os.path.exists("cookies.txt"):
    st.success("✅ Cookies carregados! O YouTube não vai bloquear.")
else:
    st.warning("⚠️ cookies.txt não encontrado. O erro 403 pode ocorrer.")

link = st.text_input("Cole o link do YouTube:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Gerar MP3 de 320kbps"):
    if link:
        # Limpeza de segurança
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
        os.makedirs("downloads")

        with st.spinner("Autenticando e extraindo áudio..."):
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': 'downloads/%(uploader)s - %(title)s.%(ext)s',
                    'quiet': False,
                    'nocheckcertificate': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    # Resolve o caminho do arquivo final pós-conversão
                    temp_path = ydl.prepare_filename(info)
                    mp3_path = os.path.splitext(temp_path)[0] + ".mp3"
                    
                    if os.path.exists(mp3_path):
                        with open(mp3_path, "rb") as f:
                            nome_final = os.path.basename(mp3_path)
                            st.success(f"🎵 {nome_final} pronta!")
                            st.download_button(
                                label="📥 SALVAR NO PC DA RÁDIO",
                                data=f,
                                file_name=nome_final,
                                mime="audio/mpeg"
                            )
                    else:
                        st.error("Erro ao converter para MP3.")

            except Exception as e:
                st.error(f"Erro Crítico: {e}")
