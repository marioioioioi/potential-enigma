import streamlit as st
import yt_dlp
import os
import subprocess
import re
import time

st.set_page_config(page_title="Rádio Hub - Multi", page_icon="📻", layout="wide")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

aba1, aba2 = st.tabs(["📥 Links (Download Direto)", "🔄 Conversor (Renomear e MP3)"])

# --- ABA 1: MULTI LINKS ---
with aba1:
    st.header("Extração de Links do YouTube")
    links_input = st.text_area("Cole os links (um por linha):", height=100)
    
    if st.button("Analisar todos os links"):
        links = [l.strip() for l in links_input.split('\n') if l.strip()]
        for idx, link in enumerate(links):
            try:
                with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'quiet': True}) as ydl:
                    info = ydl.extract_info(link, download=False)
                    url = info['url']
                    nome_f = limpar_nome(f"{info.get('uploader', 'Art')} - {info.get('title', 'Musica')}")
                    
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        col1.write(f"🎵 {nome_f}")
                        # Adicionamos o atributo 'download' no HTML para tentar forçar o nome no PC
                        col2.markdown(f'''
                            <a href="{url}" download="{nome_f}.mp3" target="_blank">
                                <button style="width:100%; cursor:pointer; background-color:#ff4b4b; color:white; border:none; border-radius:5px; padding:5px;">
                                    📥 Baixar
                                </button>
                            </a>
                        ''', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro no link {idx+1}")

# --- ABA 2: CONVERSOR MULTI (COM CHAVE ÚNICA) ---
with aba2:
    st.header("Conversor e Renomeador em Lote")
    st.write("Jogue os arquivos .weba aqui para virarem MP3 com nome certo.")
    
    arquivos = st.file_uploader("Upload de arquivos", type=["weba", "webm", "m4a"], accept_multiple_files=True)
    
    if arquivos:
        st.divider()
        if st.button("🚀 Converter tudo agora"):
            for arq in arquivos:
                # Pegamos o nome do arquivo que você subiu
                nome_base = limpar_nome(os.path.splitext(arq.name)[0])
                t_in = f"temp_in_{int(time.time())}_{nome_base}" # Nome temporário único
                t_out = f"{nome_base}.mp3"
                
                with st.status(f"Processando: {nome_base}", expanded=False):
                    try:
                        with open(t_in, "wb") as f:
                            f.write(arq.getbuffer())
                        
                        # Conversão via FFmpeg
                        subprocess.run(['ffmpeg', '-i', t_in, '-ab', '320k', '-y', t_out], check=True)
                        
                        with open(t_out, "rb") as f:
                            st.download_button(
                                label=f"💾 Baixar {nome_base}.mp3", 
                                data=f, 
                                file_name=f"{nome_base}.mp3", 
                                mime="audio/mpeg",
                                key=f"btn_{nome_base}_{time.time()}" # CHAVE ÚNICA PARA NÃO DAR ERRO
                            )
                        
                        if os.path.exists(t_in): os.remove(t_in)
                        # Não removemos o t_out imediatamente para o download_button não bugar
                    except Exception as e:
                        st.error(f"Erro: {e}")

st.divider()
st.caption("Dica: Se o botão de baixar sumir, clique em converter novamente.")
