import streamlit as st
import yt_dlp
import requests
import io
import re

st.set_page_config(page_title="Rádio Hub v2026", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

st.title("📻 Rádio Hub - Multi-Download")
st.markdown("### Cole os links abaixo para baixar em MP3 (sem erro 403)")

# Área para colar vários links
links_input = st.text_area("Um link por linha:", height=150, placeholder="https://www.youtube.com/watch?v=...")

if st.button("🚀 Processar Links"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    if not links:
        st.warning("Por favor, cole pelo menos um link.")
    else:
        for link in links:
            with st.container():
                with st.spinner(f"Extraindo: {link}"):
                    try:
                        # Configuração para pegar o melhor áudio sem baixar o vídeo
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'quiet': True,
                            'no_warnings': True,
                        }
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=False)
                            audio_url = info['url']
                            titulo = limpar_nome(info.get('title', 'Audio_Radio'))
                            artista = limpar_nome(info.get('uploader', 'Artista'))
                            nome_arquivo = f"{artista} - {titulo}.mp3"
                            
                            # Fazemos o download dos dados para a memória do servidor
                            # Isso evita o erro 403 no seu navegador
                            response = requests.get(audio_url, timeout=30)
                            
                            if response.status_code == 200:
                                audio_bytes = io.BytesIO(response.content)
                                
                                col1, col2 = st.columns([3, 1])
                                col1.write(f"✅ **{nome_arquivo}**")
                                col2.download_button(
                                    label="📥 Baixar MP3",
                                    data=audio_bytes,
                                    file_name=nome_arquivo,
                                    mime="audio/mpeg",
                                    key
