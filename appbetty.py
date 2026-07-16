import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.set_page_config(
    page_title="Fazedor de Frases da Betty",
    layout="wide"
)

st.title("🐶 Fazedor de Frases da Betty")

st.write("Faça upload da imagem e escreva uma frase.")

uploaded = st.file_uploader(
    "Escolha a imagem",
    type=["jpg", "jpeg", "png"]
)

if uploaded:

    imagem = Image.open(uploaded).convert("RGB")

    st.image(imagem, use_container_width=True)

    texto = st.text_area(
        "Digite sua frase (máximo 150 caracteres)",
        max_chars=150,
        height=120
    )

    col1, col2 = st.columns(2)

    with col1:

        tamanho = st.slider(
            "Tamanho da fonte",
            20,
            120,
            48
        )

        cor = st.color_picker(
            "Cor da fonte",
            "#FFFFFF"
        )

    with col2:

        pos_x = st.slider(
            "Mover para direita",
            0,
            imagem.width,
            70
        )

        pos_y = st.slider(
            "Mover para baixo",
            0,
            imagem.height,
            180
        )

    if st.button("Gerar imagem"):

        img = imagem.copy()

        draw = ImageDraw.Draw(img)

        fonte = None

        caminhos = [
            "DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]

        for caminho in caminhos:
            if os.path.exists(caminho):
                fonte = ImageFont.truetype(caminho, tamanho)
                break

        if fonte is None:
            fonte = ImageFont.load_default()

        draw.text(
            (pos_x, pos_y),
            texto,
            font=fonte,
            fill=cor,
            stroke_width=3,
            stroke_fill="black"
        )

        st.image(img, caption="Resultado", use_container_width=True)

        buffer = io.BytesIO()

        img.save(buffer, format="PNG")

        st.download_button(
            "📥 Baixar imagem",
            data=buffer.getvalue(),
            file_name="betty_frase.png",
            mime="image/png"
        )
