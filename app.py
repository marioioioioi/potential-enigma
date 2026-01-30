import streamlit as st
import yt_dlp
import os
import subprocess
import re
import requests

st.set_page_config(page_title="Rádio Hub Premium", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# --- SISTEMA DE ABAS ---
aba1, aba2 = st.tabs(["📥 Download Direto", "🔄 Conversor de Arquivo"])

# --- ABA 1: DOWNLOAD DO YOUTUBE ---
with aba1:
    st.header("Baixar do YouTube")
    link = st.text_input("Cole o link aqui:", key="yt_link")
    
    if st.button("Tentar Extração"):
        with st.spinner("Buscando link de áudio..."):
            try:
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                    audio_url = info['url']
                    nome_sugerido = limpar_nome(f"{info.get('uploader', 'Artista')} - {info.get('title', 'Musica')}")
                    
                    st.success("Link encontrado!")
                    st.markdown(f"**Nome sugerido:** `{nome_sugerido}.mp3`")
                    st.write("Se o arquivo baixar como `.weba`, use a aba ao lado para converter.")
                    
                    # Link direto para o navegador baixar (foge do erro 403 do servidor)
                    st.markdown(f'<a href="{audio_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#ff4b4b; color:white; border:none; padding:10px 20px; border_radius:5px; cursor:pointer;">📥 Baixar Arquivo Original</button></a>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro no YouTube: {e}")

# --- ABA 2: CONVERSOR (O PULO DO GATO) ---
with aba2:
    st.header("Conversor para MP3 (320kbps)")
    st.write("O arquivo veio em `.weba` ou sem nome? Jogue ele aqui.")
    
    arquivo_subido = st.file_uploader("Arraste o arquivo aqui", type=["weba", "webm", "m4a"], key="uploader")
    
    if arquivo_subido:
        nome_base = limpar_nome(arquivo_subido.name.rsplit('.', 1)[0])
        
        if st.button("Converter Agora"):
            with st.spinner("Transformando em MP3 Real..."):
                temp_in = "entrada_audio"
                temp_out = f"{nome_base}.mp3"
                
                with open(temp_in, "wb") as f:
                    f.write(arquivo_subido.getbuffer())
                
                try:
                    # Comando FFmpeg para converter em 320kbps
                    subprocess.run([
                        'ffmpeg', '-i', temp_in, 
                        '-vn', '-ab', '320k', '-ar', '44100', '-y', temp_out
                    ], check=True)
                    
                    with open(temp_out, "rb") as f:
                        st.success("✅ Conversão concluída!")
                        st.download_button(
                            label="📥 BAIXAR MP3 FINAL",
                            data=f,
                            file_name=f"{nome_base}.mp3",
                            mime="audio/mpeg"
                        )
                    os.remove(temp_in)
                    os.remove(temp_output)
                except Exception as e:
                    st.error(f"Erro no FFmpeg: {e}. Verifique se o packages.txt tem 'ffmpeg'.")
