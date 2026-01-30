import streamlit as st
import yt_dlp
import requests
import re

st.set_page_config(page_title="Rádio Hub Multi", page_icon="📻")

def limpar_nome(nome):
    # Remove caracteres que o Windows não aceita em nomes de arquivos
    return re.sub(r'[\\/*?:"<>|]', "", nome)

st.title("📻 Rádio Hub - Multi-Download")
st.markdown("### Cole seus links do YouTube (um por linha)")

# Área de texto para os links
links_input = st.text_area("Links:", height=150, placeholder="https://www.youtube.com/watch?v=...")

if st.button("🚀 Processar Lista"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    if not links:
        st.warning("Por favor, cole pelo menos um link.")
    else:
        for idx, link in enumerate(links):
            with st.container():
                try:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(link, download=False)
                        audio_url = info['url']
                        
                        # Formata o nome do artista e música
                        artista = limpar_nome(info.get('uploader', 'Artista')).replace(' - Topic', '')
                        titulo = limpar_nome(info.get('title', 'Musica'))
                        nome_arquivo = f"{artista} - {titulo}.mp3"
                        
                        # O servidor faz o download para evitar o erro 403 no seu PC
                        response = requests.get(audio_url, timeout=60)
                        
                        if response.status_code == 200:
                            col1, col2 = st.columns([3, 1])
                            col1.write(f"🎵 **{nome_arquivo}**")
                            
                            # Botão de download com ID único (key) para não dar erro
                            col2.download_button(
                                label="📥 Baixar",
                                data=response.content,
                                file_name=nome_arquivo,
                                mime="audio/mpeg",
                                key=f"btn_{idx}_{hash(link)}"
                            )
                        else:
                            st.error(f"Erro 403 no link: {link}")
                            
                except Exception as e:
                    st.error(f"Não foi possível carregar o link {idx+1}")

st.divider()
st.caption("Dica: Se a lista for muito grande, o site pode demorar a responder. Tente grupos de 5 em 5.")
