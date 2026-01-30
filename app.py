import streamlit as st
import requests
import re

st.set_page_config(page_title="Rádio Hub - Emergência", page_icon="📻")

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    senha = st.text_input("Senha da Rádio:", type="password")
    if senha == "radio123":
        st.session_state.autenticado = True
        st.rerun()
    st.stop()

st.title("📻 Rádio Hub (Rota Alternativa)")
st.warning("O YouTube bloqueou o servidor principal. Usando rota de emergência via instâncias Invidious.")

link_yt = st.text_input("Cole o link do YouTube:")

if st.button("Obter Áudio"):
    if "v=" in link_yt:
        video_id = link_yt.split("v=")[1].split("&")[0]
    elif "be/" in link_yt:
        video_id = link_yt.split("be/")[1].split("?")[0]
    else:
        st.error("Link inválido!")
        st.stop()

    with st.spinner("Buscando servidor disponível..."):
        try:
            # Lista de instâncias públicas do Invidious (se uma falhar, tentamos outra)
            instancias = [
                "https://invidious.snopyta.org",
                "https://yewtu.be",
                "https://invidious.kavin.rocks",
                "https://inv.riverside.rocks"
            ]
            
            sucesso = False
            for instancia in instancias:
                api_url = f"{instancia}/api/v1/videos/{video_id}"
                res = requests.get(api_url, timeout=10)
                
                if res.status_code == 200:
                    data = res.json()
                    # Filtra apenas formatos de áudio
                    audio_streams = [f for f in data['adaptiveFormats'] if 'audio' in f['type']]
                    if audio_streams:
                        # Pega o áudio de melhor qualidade
                        audio_url = audio_streams[0]['url']
                        titulo = data['title']
                        
                        st.success(f"✅ Encontrado: {titulo}")
                        
                        # Botão de download fazendo o túnel do áudio
                        audio_bytes = requests.get(audio_url).content
                        st.download_button(
                            label="📥 BAIXAR MP3",
                            data=audio_bytes,
                            file_name=f"{titulo}.mp3",
                            mime="audio/mpeg"
                        )
                        sucesso = True
                        break
            
            if not sucesso:
                st.error("Nenhum servidor alternativo respondeu. O YouTube está apertando o cerco hoje.")
                
        except Exception as e:
            st.error(f"Erro na rota alternativa: {e}")

st.divider()
st.caption("Nota: Esta rota pode ser mais lenta que o normal.")
