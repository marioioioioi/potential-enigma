import streamlit as st
import yt_dlp
import os
import subprocess
import re

st.set_page_config(page_title="Rádio Hub Multitask", page_icon="📻", layout="wide")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

aba1, aba2 = st.tabs(["📥 Download de Links", "🔄 Conversor em Lote"])

# --- ABA 1: MÚLTIPLOS LINKS ---
with aba1:
    st.header("Extração de Links")
    links_input = st.text_area("Cole os links do YouTube (um por linha):", height=150)
    
    if st.button("Analisar Links"):
        links = [l.strip() for l in links_input.split('\n') if l.strip()]
        for idx, link in enumerate(links):
            try:
                with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'quiet': True}) as ydl:
                    info = ydl.extract_info(link, download=False)
                    url = info['url']
                    nome = limpar_nome(f"{info.get('uploader', 'Art')} - {info.get('title', 'Musica')}")
                    
                    col1, col2 = st.columns([3, 1])
                    col1.write(f"🎵 **{nome}**")
                    col2.markdown(f'<a href="{url}" target="_blank"><button style="width:100%; cursor:pointer;">📥 Baixar</button></a>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro no link {idx+1}: {e}")

# --- ABA 2: MÚLTIPLOS ARQUIVOS (CONVERSOR) ---
with aba2:
    st.header("Conversor em Massa")
    st.write("Arraste todos os arquivos .weba/.webm de uma vez só.")
    
    arquivos = st.file_uploader("Upload de arquivos", type=["weba", "webm", "m4a", "opus"], accept_multiple_files=True)
    
    if arquivos and st.button("Converter Todos para MP3"):
        for arq in arquivos:
            nome_base = limpar_nome(os.path.splitext(arq.name)[0])
            temp_in = f"in_{nome_base}"
            temp_out = f"{nome_base}.mp3"
            
            with st.status(f"Convertendo {nome_base}...", expanded=False):
                with open(temp_in, "wb") as f:
                    f.write(arq.getbuffer())
                
                try:
                    subprocess.run(['ffmpeg', '-i', temp_in, '-ab', '320k', '-y', temp_out], check=True)
                    with open(temp_out, "rb") as f:
                        st.download_button(label=f"💾 Salvar {nome_base}.mp3", data=f, file_name=f"{nome_base}.mp3", mime="audio/mpeg")
                    
                    if os.path.exists(temp_in): os.remove(temp_in)
                    if os.path.exists(temp_out): os.remove(temp_out)
                except Exception as e:
                    st.error(f"Erro em {nome_base}: {e}")
