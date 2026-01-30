import streamlit as st
import yt_dlp
import requests
import re
import os

# Configuração da página
st.set_page_config(page_title="Rádio Hub v15.0", page_icon="📻", layout="wide")

def limpar_nome(nome):
    """Remove caracteres proibidos no Windows para evitar erro ao salvar"""
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# --- LOGIN SIMPLES ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("📻 Acesso ao Sistema de Rádio")
    senha = st.text_input("Senha da Rádio:", type="password")
    if st.button("Entrar"):
        if senha == "radio123": # Pode mudar a senha aqui
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# --- INTERFACE ---
st.title("📻 Rádio Hub - Download YouTube 320kbps")
st.info("Cole links de vídeos individuais ou playlists abaixo.")

links_input = st.text_area("Links (um por linha):", height=150, placeholder="https://www.youtube.com/watch?v=...")

if st.button("🚀 Iniciar Processamento"):
    links = [l.strip() for l in links_input.split('\n') if l.strip()]
    
    if not links:
        st.warning("Nenhum link detectado.")
    else:
        for link in links:
            with st.status(f"Analisando: {link}", expanded=True) as status:
                try:
                    # Configurações otimizadas para evitar erro de JS e DRM
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'quiet': True,
                        'noplaylist': False,
                        'extract_flat': False,
                        'nocheckcertificate': True,
                        'ignoreerrors': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(link, download=False)
                        
                        # Se for playlist, pega as entradas, se não, coloca o vídeo numa lista
                        entries = info_dict.get('entries', [info_dict])
                        
                        for entry in entries:
                            if not entry: continue
                            
                            # Identificação do nome: Artista - Título
                            # O 'uploader' costuma ser o nome do canal/artista no YT
                            artista = entry.get('artist') or entry.get('uploader', 'Desconhecido')
                            artista = artista.replace(' - Topic', '') # Limpa o sufixo de canais oficiais
                            titulo = entry.get('title', 'Musica')
                            
                            nome_f = limpar_nome(f"{artista} - {titulo}.mp3")
                            
                            st.write(f"✅ Preparado: **{nome_f}**")
                            
                            # Botão de download: o Streamlit puxa o arquivo do servidor do YT
                            # e entrega direto para o navegador do PC da rádio.
                            st.download_button(
                                label=f"Download MP3",
                                data=requests.get(entry['url']).content,
                                file_name=nome_f,
                                mime="audio/mpeg",
                                key=f"{entry['id']}_{os.urandom(4).hex()}" # Chave única para evitar conflito
                            )
                    status.update(label="Concluído!", state="complete")
                    
                except Exception as e:
                    st.error(f"Erro no link {link}: {e}")

st.divider()
st.caption("v15.0 - Engine Local com suporte a JavaScript Runtime (QuickJS)")
