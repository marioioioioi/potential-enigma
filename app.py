import streamlit as st
import os
import subprocess
import re

st.set_page_config(page_title="Conversor Rádio Pro", page_icon="🔄")

def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "", nome)

st.title("🔄 Conversor WebA para MP3 (Rádio)")
st.info("Se o YouTube baixou um arquivo .weba estranho, jogue ele aqui para transformar em MP3 de 320kbps.")

# Upload do arquivo que veio do YouTube
arquivo_subido = st.file_uploader("Arraste o arquivo .weba ou .webm aqui", type=["weba", "webm", "m4a"])

if arquivo_subido is not None:
    nome_original = arquivo_subido.name
    nome_limpo = limpar_nome(nome_original.replace(".weba", "").replace(".webm", ""))
    
    st.write(f"📁 Arquivo detectado: {nome_original}")
    
    if st.button("Transformar em MP3"):
        with st.spinner("Convertendo... aguarde."):
            # Salva o arquivo temporariamente no servidor
            temp_input = "input_audio"
            temp_output = f"{nome_limpo}.mp3"
            
            with open(temp_input, "wb") as f:
                f.write(arquivo_subido.getbuffer())
            
            try:
                # Usa o FFmpeg do servidor para converter de verdade
                # -vn: sem vídeo | -ab: bitrate de 320k | -y: sobrescrever se existir
                subprocess.run([
                    'ffmpeg', '-i', temp_input, 
                    '-vn', '-ar', '44100', 
                    '-ac', '2', '-b:a', '320k', 
                    temp_output, '-y'
                ], check=True)

                with open(temp_output, "rb") as f:
                    st.success("✅ Conversão concluída com sucesso!")
                    st.download_button(
                        label="📥 BAIXAR MP3 FINAL",
                        data=f,
                        file_name=f"{nome_limpo}.mp3",
                        mime="audio/mpeg"
                    )
                
                # Limpa a sujeira
                os.remove(temp_input)
                os.remove(temp_output)
                
            except Exception as e:
                st.error(f"Erro na conversão: {e}")
                st.info("Certifique-se de que o 'ffmpeg' está no seu packages.txt")

st.divider()
st.caption("Dica: Use aquele código anterior que gerava o link direto, baixe o arquivo e use este aqui para finalizar.")
