import streamlit as st
import yt_dlp
import os
import subprocess
import re
import requests

st.set_page_config(page_title="Rádio Hub - Renomeador", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

aba1, aba2 = st.tabs(["📥 Download Direto", "🔄 Conversor Manual"])

# --- ABA 1: DOWNLOAD COM NOME FORÇADO ---
with aba1:
    st.header("Download com Nome Automático")
    link = st.text_input("Link do YouTube:")
    
    if st.button("Gerar Arquivo Renomeado"):
        with st.spinner("Extraindo áudio..."):
            try:
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                    audio_url = info['url']
                    # Monta o nome: Artista - Título
                    artista = info.get('uploader', 'Artista').replace(' - Topic', '')
                    titulo = info.get('title', 'Musica')
                    nome_final = limpar_nome(f"{artista} - {titulo}.mp3")
                    
                    # O SEGREDO: Em vez de link HTML, usamos o download_button do Streamlit
                    # com o conteúdo vindo via requests. Isso força o nome!
                    conteudo_audio = requests.get(audio_url).content
                    
                    st.success(f"✅ Arquivo preparado: {nome_final}")
                    st.download_button(
                        label="📥 BAIXAR MP3 AGORA",
                        data=conteudo_audio,
                        file_name=nome_final,
                        mime="audio/mpeg"
                    )
            except Exception as e:
                st.error(f"Erro: {e}")
                st.info("Se der erro 403, o YouTube bloqueou este download direto.")

# --- ABA 2: CONVERSOR (SE O ACIMA FALHAR) ---
with aba2:
    st.header("Conversor de Emergência")
    st.write("Se o de cima der erro 403, baixe o 'videoplayback' e jogue aqui.")
    
    # Campo para o usuário digitar o nome que ele quer, caso queira mudar
    novo_nome = st.text_input("Nome que você deseja no arquivo (opcional):")
    arquivo_subido = st.file_uploader("Suba o arquivo 'videoplayback' aqui", type=["weba", "webm", "m4a"])
    
    if arquivo_subido and st.button("Converter e Renomear"):
        with st.spinner("Processando..."):
            # Define o nome: ou o que o user digitou, ou o nome original do arquivo
            nome_save = novo_nome if novo_nome else os.path.splitext(arquivo_subido.name)[0]
            nome_save = limpar_nome(nome_save)
            
            t_in, t_out = "temp_in", f"{nome_save}.mp3"
            with open(t_in, "wb") as f:
                f.write(arquivo_subido.getbuffer())
            
            try:
                subprocess.run(['ffmpeg', '-i', t_in, '-ab', '320k', '-y', t_out], check=True)
                with open(t_out, "rb") as f:
                    st.download_button(label="📥 SALVAR MP3 RENOMEADO", data=f, file_name=f"{nome_save}.mp3", mime="audio/mpeg")
                os.remove(t_in)
                os.remove(t_out)
            except Exception as e:
                st.error(f"Erro: {e}")
