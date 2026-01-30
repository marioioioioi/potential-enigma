import streamlit as st
import yt_dlp
import os
import re

st.set_page_config(page_title="Rádio Hub v16.0", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("📻 Acesso Rádio")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if senha == "difusora":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

st.title("📻 Rádio Hub - Download Real")

link = st.text_input("Cole o link do YouTube:")

if st.button("Preparar Download"):
    if link:
        with st.spinner("Baixando e convertendo... Isso pode levar alguns segundos."):
            try:
                # Pasta temporária para o download
                if not os.path.exists("downloads"):
                    os.makedirs("downloads")

                # Configuração para download REAL no servidor
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': 'downloads/%(uploader)s - %(title)s.%(ext)s',
                    'quiet': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    # O yt-dlp nos dá o caminho exato do arquivo gerado
                    caminho_arquivo = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
                    
                    if os.path.exists(caminho_arquivo):
                        with open(caminho_arquivo, "rb") as f:
                            bytes_musica = f.read()
                            nome_exibicao = os.path.basename(caminho_arquivo)
                            
                            st.success(f"✅ Pronto: {nome_exibicao}")
                            st.download_button(
                                label="📥 SALVAR MP3 NO COMPUTADOR",
                                data=bytes_musica,
                                file_name=nome_exibicao,
                                mime="audio/mpeg"
                            )
                        # Limpa o arquivo do servidor para não encher o disco
                        os.remove(caminho_arquivo)
                    else:
                        st.error("Erro: Arquivo não foi gerado corretamente.")

            except Exception as e:
                st.error(f"Erro no processamento: {e}")
