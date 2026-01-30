import streamlit as st
import yt_dlp
import os
import re

st.set_page_config(page_title="Rádio Hub - Local Pro", page_icon="📻")

def limpar(texto):
    return re.sub(r'[\\/*?:"<>|]', "", texto)

st.title("📻 Rádio Hub - Download Direto")
st.markdown("Esta versão baixa o arquivo direto para a pasta do seu computador.")

# Criar pasta 'downloads' se não existir
if not os.path.exists("musicas_radio"):
    os.makedirs("musicas_radio")

links_input = st.text_area("Cole os links (um por linha):", height=150)

if st.button("🚀 Baixar Tudo Agora"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    for idx, link in enumerate(links):
        with st.status(f"Processando link {idx+1}...", expanded=True) as status:
            try:
                # Configuração "Tanque de Guerra" do yt-dlp
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': 'musicas_radio/%(uploader)s - %(title)s.%(ext)s',
                    'quiet': False,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    nome_arquivo = f"{info.get('uploader')} - {info.get('title')}.mp3"
                    st.success(f"Baixado: {nome_arquivo}")
                
            except Exception as e:
                st.error(f"Erro no link {link}: Verifique se o FFmpeg está instalado.")
    
    st.balloons()
    st.info(f"📂 Verifique a pasta 'musicas_radio' no seu computador!")
