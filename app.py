import streamlit as st
import yt_dlp
import requests
import re

st.set_page_config(page_title="Rádio Hub - Auto Rename", page_icon="📻")

def limpar_nome(nome):
    # Remove caracteres que o Windows proíbe em nomes de arquivos
    return re.sub(r'[\\/*?:"<>|]', "", nome)

st.title("📻 Rádio Hub - Download Automático")
st.markdown("Os arquivos serão baixados já com o nome correto do YouTube.")

links_input = st.text_area("Cole os links (um por linha):", height=150)

if st.button("🚀 Gerar Downloads com Nome Real"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    if not links:
        st.warning("Cole os links primeiro!")
    else:
        for idx, link in enumerate(links):
            with st.container():
                try:
                    # 1. Extrair metadados e link direto
                    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(link, download=False)
                        audio_url = info['url']
                        
                        # Captura Artista e Título
                        artista = info.get('uploader', 'Artista').replace(' - Topic', '')
                        titulo = info.get('title', 'Musica')
                        nome_final = limpar_nome(f"{artista} - {titulo}.mp3")
                        
                    with st.spinner(f"Preparando: {nome_final}"):
                        # 2. O Servidor baixa o conteúdo para a memória
                        # Usamos um User-Agent para tentar enganar o bloqueio 403
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                        response = requests.get(audio_url, headers=headers, timeout=60)
                        
                        if response.status_code == 200:
                            st.write(f"✅ **{nome_final}**")
                            # 3. O download_button FORÇA o nome do arquivo no seu PC
                            st.download_button(
                                label=f"📥 Baixar MP3",
                                data=response.content,
                                file_name=nome_final,
                                mime="audio/mpeg",
                                key=f"dl_{idx}"
                            )
                        else:
                            st.error(f"Erro
