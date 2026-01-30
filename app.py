import streamlit as st
import yt_dlp
import re

st.set_page_config(page_title="Rádio Hub - Bypass", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

st.title("📻 Rádio Hub - Solução de Bloqueio")
st.markdown("O YouTube bloqueou o servidor. Use os botões abaixo para baixar via seu navegador:")

links_input = st.text_area("Cole os links (um por linha):", height=150)

if st.button("🚀 Gerar Links de Download"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    if not links:
        st.warning("Cole os links primeiro.")
    else:
        for idx, link in enumerate(links):
            try:
                # Usamos apenas o metadado (isso o YouTube ainda deixa o servidor ver)
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                    audio_url = info['url']
                    artista = limpar_nome(info.get('uploader', 'Artista')).replace(' - Topic', '')
                    titulo = limpar_nome(info.get('title', 'Musica'))
                    nome_f = f"{artista} - {titulo}.mp3"
                    
                    st.write(f"🎵 **{nome_f}**")
                    
                    # Criamos um botão HTML que tenta forçar o download pelo seu IP
                    # O atributo 'download' tenta renomear o arquivo
                    st.markdown(f'''
                        <a href="{audio_url}" download="{nome_f}" target="_blank" style="text-decoration:none;">
                            <button style="background-color:#00c853; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer; font-weight:bold; width:100%;">
                                📥 Baixar pelo Navegador
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                    st.caption("Se abrir o player, clique nos 3 pontinhos e 'Fazer download'.")
                    st.divider()
                    
            except Exception as e:
                st.error(f"Não foi possível processar o vídeo {idx+1}.
