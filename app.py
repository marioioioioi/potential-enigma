import streamlit as st
import yt_dlp
import os
import subprocess
import re
import requests

st.set_page_config(page_title="Rádio Hub - Nome Automático", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

aba1, aba2 = st.tabs(["📥 Download Direto", "🔄 Conversor Inteligente"])

# --- ABA 1: TENTATIVA DIRETA ---
with aba1:
    st.header("1. Link do YouTube")
    link_direto = st.text_input("Cole o link aqui:", key="link_aba1")
    if st.button("Preparar Download"):
        with st.spinner("Buscando..."):
            try:
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link_direto, download=False)
                    audio_url = info['url']
                    nome_f = limpar_nome(f"{info.get('uploader', 'Art')} - {info.get('title', 'Musica')}.mp3")
                    
                    # Tenta baixar direto pelo servidor para forçar o nome
                    conteudo = requests.get(audio_url).content
                    st.download_button(label=f"📥 Baixar: {nome_f}", data=conteudo, file_name=nome_f, mime="audio/mpeg")
            except:
                st.error("Erro 403: Use a Aba 2 abaixo.")

# --- ABA 2: CONVERSOR COM RENOMEAÇÃO AUTOMÁTICA ---
with aba2:
    st.header("2. Conversor e Renomeador")
    st.write("Se o arquivo baixou como 'videoplayback', resolva aqui:")
    
    # Campo para colar o link e descobrir o nome
    link_para_nome = st.text_input("Cole o link do YouTube para pegar o nome real:", placeholder="https://youtube.com/...")
    
    arquivo_subido = st.file_uploader("Suba o arquivo 'videoplayback' aqui", type=["weba", "webm", "m4a"])
    
    if arquivo_subido and st.button("Converter com Nome Real"):
        with st.spinner("Identificando música e convertendo..."):
            nome_final = "musica_convertida.mp3" # Nome padrão de segurança
            
            # Tenta buscar o nome real pelo link fornecido
            if link_para_nome:
                try:
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        info = ydl.extract_info(link_para_nome, download=False)
                        artista = info.get('uploader', 'Artista').replace(' - Topic', '')
                        titulo = info.get('title', 'Musica')
                        nome_final = limpar_nome(f"{artista} - {titulo}.mp3")
                except:
                    st.warning("Não consegui pegar o nome pelo link, usando nome original.")
                    nome_final = limpar_nome(arquivo_subido.name.split('.')[0]) + ".mp3"
            
            t_in, t_out = "temp_in", "temp_out.mp3"
            with open(t_in, "wb") as f:
                f.write(arquivo_subido.getbuffer())
            
            try:
                # Conversão pesada para 320kbps
                subprocess.run(['ffmpeg', '-i', t_in, '-ab', '320k', '-ar', '44100', '-y', t_out], check=True)
                
                with open(t_out, "rb") as f:
                    st.success(f"✅ Convertido como: {nome_final}")
                    st.download_button(
                        label="📥 SALVAR MP3 RENOMEADO",
                        data=f,
                        file_name=nome_final, # AQUI ESTÁ A MÁGICA DO NOME
                        mime="audio/mpeg"
                    )
                os.remove(t_in)
                os.remove(t_out)
            except Exception as e:
                st.error(f"Erro no processo: {e}")
