import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

st.set_page_config(page_title="Gerador de Posts - Muro", layout="centered")

st.title("📸 Gerador de Frases no Muro")
st.write("Suba a foto do muro, digite sua mensagem em português ou espanhol!")

# Função inteligente que busca a fonte Arial no Mac ou no Servidor Linux do GitHub
@st.cache_data
def carregar_fonte_sistema(font_size):
    # Lista de caminhos comuns para fontes com suporte a acentos
    caminhos_fontes = [
        "/Library/Fonts/Arial.ttf",              # Caminho no seu Mac
        "/System/Library/Fonts/Supplemental/Arial.ttf", # Caminho alternativo no Mac
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", # Caminho no Linux (GitHub)
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" # Alternativa Linux
    ]
    
    for caminho in caminhos_fontes:
        if os.path.exists(caminho):
            return ImageFont.truetype(caminho, font_size)
            
    # Se rodar em algum ambiente sem essas fontes, usa a padrão redimensionada
    return ImageFont.load_default(size=font_size)

uploaded_image = st.file_uploader("1. Suba a imagem de fundo", type=["jpg", "jpeg", "png"])
text_input = st.text_input("2. Digite a mensagem para o muro (Máx. 100 caracteres):", max_chars=100)

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    W, H = image.size

    st.subheader("Visualização")

    if text_input:
        img_edit = image.copy()
        draw = ImageDraw.Draw(img_edit)

        font_size = int(W * 0.045)
        font = carregar_fonte_sistema(font_size)

        lines = textwrap.wrap(text_input, width=18)

        muro_width = int(W * 0.48)
        margem_esquerda = int(W * 0.05)
        
        linha_altura = font_size + int(font_size * 0.4)
        total_text_height = len(lines) * linha_altura
        
        # Mantém o texto bem posicionado no meio/baixo do muro
        muro_center_y = int(H * 0.60)
        current_y = muro_center_y - (total_text_height // 2)

        for line in lines:
            left, top, right, bottom = font.getbbox(line)
            text_w = right - left

            text_x = margem_esquerda + ((muro_width - text_w) // 2)

            draw.text((text_x, current_y), line, fill="black", font=font)
            current_y += linha_altura

        st.image(img_edit, caption="Seu post está pronto!", use_column_width=True)

        import io
        img_byte_arr = io.BytesIO()
        img_edit.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        st.download_button(
            label="📥 Baixar Imagem para Rede Social",
            data=img_byte_arr,
            file_name="post_muro.jpg",
            mime="image/jpeg"
        )
    else:
        st.image(image, caption="Aguardando texto...", use_column_width=True)
