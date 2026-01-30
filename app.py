import streamlit as st
import yt_dlp
import requests
import io
import re

st.set_page_config(page_title="Rádio Hub v2026", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

st.title("📻 Rádio Hub - Multi-Download")
st.markdown("### Cole os links abaixo (um por linha)")

# Área para colar vários links
links_input = st.text_area("Links do YouTube:", height=150, placeholder="https://www.youtube.com/watch?v=...")

if st.button("🚀 Processar e Gerar Downloads"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    if not links:
        st.warning("Por favor, cole pelo menos um link.")
    else:
        for idx, link in enumerate(links):
            with st.container():
                with st.spinner(f"Extraindo: {link}"):
                    try:
                        # Configuração para pegar o link de áudio
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'quiet': True,
                            'no_warnings': True,
                        }
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=False)
                            audio_url = info['url']
                            
                            # Organiza o nome do arquivo
                            artista = limpar_nome(info.get('uploader', 'Artista')).replace(' - Topic', '')
                            titulo = limpar_nome(info.get('title', 'Musica'))
                            nome_arquivo = f"{artista} - {titulo}.mp3"
                            
                            # O servidor "puxa" o áudio para evitar o erro 403 de acesso negado
                            response = requests.get(audio_url, timeout=30)
                            
                            if response.status_code == 200:
                                col1, col2 = st.columns([3, 1])
                                col1.write(f"✅ **{nome_arquivo}**")
                                
                                # Botão de download corrigido e fechado corretamente
                                col2.download_button(
                                    label="📥 Baixar",
                                    data=response.content,
                                    file_name=nome_arquivo,
                                    mime="audio/mpeg",
                                    key=f"btn_{idx}"
                                )
                            else
