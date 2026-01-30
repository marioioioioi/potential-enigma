import streamlit as st
import yt_dlp
import os
import subprocess
import re

st.set_page_config(page_title="Rádio Hub v2026", page_icon="📻")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

# Mantém o nome da música guardado entre as abas
if 'nome_radio' not in st.session_state:
    st.session_state.nome_radio = "musica_radio"

st.title("📻 Rádio Hub - Sistema de Conversão")

aba1, aba2 = st.tabs(["📥 1. Pegar Link", "🔄 2. Converter e Renomear"])

# --- ABA 1: EXTRAIR LINK ---
with aba1:
    st.header("Passo 1: Baixar o áudio bruto")
    url_yt = st.text_input("Cole o link do YouTube aqui:")
    
    if url_yt:
        with st.spinner("Buscando informações da música..."):
            try:
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_yt, download=False)
                    artista = info.get('uploader', 'Artista').replace(' - Topic', '')
                    titulo = info.get('title', 'Musica')
                    
                    # Guarda o nome para a próxima aba
                    st.session_state.nome_radio = limpar_nome(f"{artista} - {titulo}")
                    
                    st.success(f"🎵 Música identificada: {st.session_state.nome_radio}")
                    
                    # Botão para baixar o arquivo bruto (o que vem com nome videoplayback)
                    st.markdown(f'''
                        <a href="{info['url']}" target="_blank" style="text-decoration:none;">
                            <button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:15px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:16px;">
                                📥 BAIXAR ARQUIVO BRUTO (.weba)
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                    st.info("Após baixar o arquivo no botão vermelho, mude para a aba ao lado.")
            except Exception as e:
                st.error("Erro ao acessar o YouTube. Tente outro link ou verifique se o vídeo não é privado.")

# --- ABA 2: CONVERSOR MP3 ---
with aba2:
    st.header("Passo 2: Transformar em MP3")
    st.write(f"O arquivo será salvo como: **{st.session_state.nome_radio}.mp3**")
    
    arquivo_up = st.file_uploader("Suba o arquivo 'videoplayback' aqui", type=["weba", "webm", "m4a", "opus"])

    if arquivo_up:
        if st.button("🚀 CONVERTER PARA MP3 AGORA"):
            with st.spinner("Convertendo... isso pode levar alguns segundos."):
                try:
                    nome_final = f"{st.session_state.nome_radio}.mp3"
                    t_in = "arquivo_entrada"
                    t_out = "arquivo_saida.mp3"
                    
                    # Salva o arquivo enviado pelo usuário no servidor
                    with open(t_in, "wb") as f:
                        f.write(arquivo_up.getbuffer())

                    # Comando FFmpeg para converter em 320kbps reais
                    subprocess.run([
                        'ffmpeg', '-i', t_in, 
                        '-vn', '-ab', '320k', '-ar', '44100', '-y', t_out
                    ], check=True)

                    # Disponibiliza o download com o nome correto
                    with open(t_out, "rb") as f:
                        st.success("✅ Conversão concluída!")
                        st.download_button(
                            label=f"💾 SALVAR {nome_final}",
                            data=f,
                            file_name=nome_final,
                            mime="audio/mpeg"
                        )
                    
                    # Limpa os arquivos temporários do servidor
                    if os.path.exists(t_in): os.remove(t_in)
                    if os.path.exists(t_out): os.remove(t_out)
                    
                except Exception as e:
                    st.error(f"Erro no FFmpeg: {e}")
                    st.warning("Verifique se o arquivo 'packages.txt' no seu GitHub contém apenas a palavra 'ffmpeg'.")
