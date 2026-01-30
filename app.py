import streamlit as st
import yt_dlp
import os
import re
import shutil

st.set_page_config(page_title="Rádio Hub 2026", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("📻 Acesso Rádio")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if senha == "radio123":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

st.title("📻 Rádio Hub - Sistema Anti-Bloqueio")

link = st.text_input("Cole o link do YouTube:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Gerar MP3 de 320kbps"):
    if link:
        # Limpar pasta de downloads antigos para não dar erro de permissão
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
        os.makedirs("downloads")

        with st.spinner("Burlando bloqueios e processando áudio..."):
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': 'downloads/%(uploader)s - %(title)s.%(ext)s',
                    'quiet': False,
                    'no_warnings': False,
                    'nocheckcertificate': True,
                    'rm_cachedir': True, # Limpa o cache para evitar o erro 403
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # O segredo: o yt-dlp vai detectar o Node.js do packages.txt automaticamente
                    info = ydl.extract_info(link, download=True)
                    # Resolve o nome do arquivo final
                    file_path = ydl.prepare_filename(info)
                    base, ext = os.path.splitext(file_path)
                    mp3_path = base + ".mp3"
                    
                    if os.path.exists(mp3_path):
                        with open(mp3_path, "rb") as f:
                            st.success(f"✅ Sucesso: {os.path.basename(mp3_path)}")
                            st.download_button(
                                label="📥 BAIXAR AGORA (320kbps)",
                                data=f,
                                file_name=os.path.basename(mp3_path),
                                mime="audio/mpeg"
                            )
                    else:
                        st.error("Ocorreu um erro na conversão para MP3.")

            except Exception as e:
                st.error(f"Erro Crítico: {e}")
                st.info("Dica: Tente atualizar o link ou verifique se o vídeo não tem restrição de idade.")
