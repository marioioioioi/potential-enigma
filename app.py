import streamlit as st
import yt_dlp
import requests
import re
import os

st.set_page_config(page_title="Rádio Hub Local", page_icon="📻")

def limpar(texto):
    return re.sub(r'[\\/*?:"<>|]', "", texto)

st.title("📻 Rádio Hub - Versão Local (Sem Bloqueio)")
st.markdown("Esta versão usa sua internet, então o YouTube não bloqueia o nome automático.")

links_input = st.text_area("Cole os links (um por linha):", height=150)

if st.button("🚀 Baixar e Renomear"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    for idx, link in enumerate(links):
        try:
            with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'quiet': True}) as ydl:
                info = ydl.extract_info(link, download=False)
                audio_url = info['url']
                nome_f = limpar(f"{info.get('uploader', 'Art')} - {info.get('title', 'Musica')}.mp3")
                
                with st.spinner(f"Processando: {nome_f}"):
                    res = requests.get(audio_url, timeout=60)
                    if res.status_code == 200:
                        st.write(f"✅ {nome_f}")
                        st.download_button(
                            label=f"Salvar MP3",
                            data=res.content,
                            file_name=nome_f,
                            mime="audio/mpeg",
                            key=f"pc_{idx}"
                        )
                    else:
                        st.error("Erro ao puxar áudio.")
        except Exception as e:
            st.error(f"Erro no link: {link}")
