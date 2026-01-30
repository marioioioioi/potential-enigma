import streamlit as st
import yt_dlp
import requests
import re

st.set_page_config(page_title="Rádio Hub Pro", page_icon="📻")

def limpar(texto):
    return re.sub(r'[\\/*?:"<>|]', "", texto)

st.title("📻 Rádio Hub - Nome Automático")

links_input = st.text_area("Cole os links (um por linha):")

if st.button("🚀 Gerar Downloads"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    for idx, link in enumerate(links):
        try:
            with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'quiet': True}) as ydl:
                info = ydl.extract_info(link, download=False)
                audio_url = info['url']
                
                # Pegando Artista e Título para o nome automático
                nome_musica = limpar(info.get('title', 'Musica'))
                nome_artista = limpar(info.get('uploader', 'Artista')).replace(' - Topic', '')
                nome_final = f"{nome_artista} - {nome_musica}.mp3"
                
                # O servidor tenta buscar os dados para renomear
                res = requests.get(audio_url, timeout=60)
                
                if res.status_code == 200:
                    st.write("✅ " + nome_final)
                    st.download_button(
                        label="📥 Baixar MP3",
                        data=res.content,
                        file_name=nome_final,
                        mime="audio/mpeg",
                        key=f"dl_{idx}"
                    )
                else:
                    st.error("YouTube negou o acesso (403).")
        except:
            st.error("Erro ao processar este link.")
