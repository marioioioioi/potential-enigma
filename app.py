import streamlit as st
import yt_dlp
import re

st.set_page_config(page_title="Rádio Hub - Bypass", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

st.title("📻 Rádio Hub - Sistema Anti-Bloqueio")
st.markdown("Como o YouTube bloqueou o servidor, os links abaixo abrirão o áudio direto no seu navegador.")

links_input = st.text_area("Cole os links (um por linha):", height=150, placeholder="https://youtube.com/...")

if st.button("🚀 Gerar Links de Áudio"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    if not links:
        st.warning("Cole os links primeiro!")
    else:
        for idx, link in enumerate(links):
            try:
                # O servidor apenas lê o título e o link direto (sem baixar os bytes)
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                    audio_url = info['url']
                    artista = limpar_nome(info.get('uploader', 'Artista')).replace(' - Topic', '')
                    titulo = limpar_nome(info.get('title', 'Musica'))
                    nome_f = f"{artista} - {titulo}.mp3"
                    
                    with st.container():
                        st.write(f"🎵 **{nome_f}**")
                        # Botão HTML que manda o link direto para o seu IP pessoal baixar
                        st.markdown(f'''
                            <a href="{audio_url}" target="_blank" style="text-decoration:none;">
                                <button style="width:100%; background-color:#28a745; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold;">
                                    📥 Abrir Áudio / Baixar
                                </button>
                            </a>
                        ''', unsafe_allow_html=True)
                        st.caption("Dica: Se abrir uma tela preta tocando a música, clique nos 3 pontinhos e escolha 'Fazer download'.")
                        st.divider()
            except Exception as e:
                st.error(f"Erro no link {idx+1}: Link inválido ou restrito.")

st.info("💡 Se baixar como 'videoplayback', basta renomear o arquivo no seu computador para o nome da música.")
