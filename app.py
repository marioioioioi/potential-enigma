import streamlit as st
import yt_dlp
import requests
import re

st.set_page_config(page_title="Rádio Hub v2026", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    senha = st.text_input("Senha da Rádio:", type="password")
    if st.button("Entrar"):
        if senha == "radio123":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

st.title("📻 Rádio Hub - Final Edition")

link = st.text_input("Cole o link do YouTube:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Extrair Áudio Original"):
    if link:
        with st.spinner("Localizando áudio e formatando nome..."):
            try:
                # 1. Extrair o link direto e o título usando yt-dlp
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'nocheckcertificate': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                    audio_url = info['url']
                    artista = info.get('uploader', 'Artista').replace(' - Topic', '')
                    titulo = info.get('title', 'Musica')
                    nome_final = limpar_nome(f"{artista} - {titulo}.mp3")

                # 2. Capturar os bytes do áudio pelo servidor (Proxy)
                # Fazemos o streaming do conteúdo para não estourar a RAM
                response = requests.get(audio_url, stream=True)
                
                if response.status_code == 200:
                    st.success(f"✅ Pronto para baixar: {nome_final}")
                    
                    # O download_button força o navegador a salvar com o nome e extensão que definimos
                    st.download_button(
                        label="📥 BAIXAR MP3 AGORA",
                        data=response.content, # Aqui os bytes entram no botão
                        file_name=nome_final,
                        mime="audio/mpeg"
                    )
                else:
                    st.error("O YouTube recusou a conexão (Erro 403).")

            except Exception as e:
                if "403" in str(e):
                    st.error("Bloqueio de IP detectado pelo YouTube.")
                    st.info("Dica: Tente novamente em 1 minuto ou use um link de outro vídeo.")
                else:
                    st.error(f"Erro: {e}")

st.divider()
st.caption("Nota: Se o download vier vazio, o YouTube bloqueou o IP do servidor definitivamente.")
