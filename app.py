import streamlit as st
import yt_dlp
import requests
import re
import os

st.set_page_config(page_title="Rádio Hub Premium", page_icon="🎵")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("Acesso Rádio")
    senha = st.text_input("Senha da rádio:", type="password")
    if st.button("Entrar"):
        if senha == "difusora": # Mude sua senha aqui
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

st.title("🎵 Rádio Hub - Multi Download & Capa")

links_input = st.text_area("Cole os links (YouTube ou Spotify) - Um por linha:", height=150)

if st.button("🚀 Processar tudo para a Rádio"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    if not links:
        st.warning("Adicione pelo menos um link!")
    else:
        for link in links:
            with st.status(f"Processando: {link}...", expanded=True) as status:
                try:
                    # Configuração para buscar áudio + metadados (capa e nomes)
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'writethumbnail': True,
                        'quiet': True,
                        'noplaylist': False
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(link, download=False)
                        
                        # Se for playlist, processa cada música
                        entries = info.get('entries', [info])
                        
                        for entry in entries:
                            artista = entry.get('artist') or entry.get('uploader') or "Artista"
                            titulo = entry.get('title') or "Musica"
                            nome_f = limpar_nome(f"{artista} - {titulo}.mp3")
                            capa = entry.get('thumbnail')

                            if capa:
                                st.image(capa, width=150)
                            
                            st.write(f"✅ **{nome_f}** pronta!")
                            
                            # Botão de download direto do servidor do YT para o PC
                            st.download_button(
                                label=f"Baixar: {nome_f[:40]}...",
                                data=requests.get(entry['url']).content,
                                file_name=nome_f,
                                mime="audio/mpeg",
                                key=entry['id']
                            )
                    status.update(label="Concluído!", state="complete")
                except Exception as e:
                    st.error(f"Erro no link {link}: {e}")

st.divider()
st.caption("Dica: Se o nome vier como 'Uploader', é porque o YouTube não forneceu o metadado de Artista oficial.")
