import streamlit as st
import yt_dlp
import requests
import re

st.set_page_config(page_title="Rádio Hub - Final Boss", page_icon="📻")

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    senha = st.text_input("Senha:", type="password")
    if senha == "radio123":
        st.session_state.autenticado = True
        st.rerun()
    st.stop()

st.title("📻 Rádio Hub - Rota de Extração Direta")

link = st.text_input("Link do YouTube:")

if st.button("Tentar Extração"):
    if link:
        with st.spinner("Buscando rota de áudio disponível..."):
            try:
                # O segredo: Usar o yt-dlp apenas para extrair o LINK de stream
                # sem tentar baixar o arquivo no servidor do Streamlit
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    # Forçamos o yt-dlp a usar um "User Agent" de navegador real
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                    audio_url = info['url']
                    titulo = info.get('title', 'musica_radio')
                    
                    st.success(f"✅ Link de áudio localizado!")
                    
                    # Em vez de baixar no servidor, damos o link direto pro navegador do seu amigo baixar
                    # Isso pula o bloqueio de IP do Streamlit!
                    st.markdown(f"""
                        <a href="{audio_url}" download="{titulo}.mp3" style="
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: #ff4b4b;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                            font-weight: bold;
                        ">📥 CLIQUE AQUI PARA SALVAR NO PC</a>
                    """, unsafe_allow_html=True)
                    
                    st.info("Nota: Se o link abrir o áudio no navegador, clique com o botão direito e 'Salvar como'.")

            except Exception as e:
                st.error(f"Erro ao tentar extrair: {e}")
                st.info("O YouTube bloqueou este servidor. A última opção é rodar o script no seu PC pessoal.")
