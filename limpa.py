import streamlit as st
from rembg import remove
from PIL import Image
import io

# Configuração da página do Streamlit
st.set_page_config(page_title="Removedor de Fundo", layout="centered")

st.title("✂️ Removedor de Fundo de Imagens")
st.write("Suba uma imagem para remover o fundo automaticamente, sem complicação.")

# Componente para o cliente subir a imagem
uploaded_file = st.file_uploader("Escolha uma imagem (PNG, JPG, JPEG)...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Abre a imagem enviada pelo usuário
    input_image = Image.open(uploaded_file)
    
    # Cria duas colunas para mostrar o "Antes e Depois"
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Imagem Original")
        st.image(input_image, use_container_width=True)
        
    with col2:
        st.subheader("Resultado")
        # Mostra uma mensagem de carregamento enquanto a mágica acontece
        with st.spinner("Removendo o fundo..."):
            # Remove o fundo usando a biblioteca rembg
            output_image = remove(input_image)
            st.image(output_image, use_container_width=True)
            
    # Prepara a imagem resultante para o botão de download (converte para bytes)
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Botão para o cliente baixar a imagem sem fundo
    st.download_button(
        label="📥 Baixar imagem sem fundo",
        data=img_byte_arr,
        file_name="imagem_sem_fundo.png",
        mime="image/png"
    )
