import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Configuração da página do Streamlit
st.set_page_config(page_title="Gerador de Frases da Betty", layout="centered")

# Título principal do aplicativo
st.title("📸 Gerador de Frases no Muro")
st.write("Suba a foto do muro, digite sua mensagem em português ou espanhol!")

# Função para carregar a fonte Roboto com suporte a acentos
def carregar_fonte_correta(font_size):
    # Encontra a pasta atual do script e tenta montar caminhos absolutos
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Lista de tentativas para carregar a Roboto-Bold que você enviou
    caminhos_roboto = [
        os.path.join(diretorio_atual, "Roboto-Bold.ttf"),
        "/mount/src/my_git/Roboto-Bold.ttf", # Caminho padrão do Streamlit Cloud
        "Roboto-Bold.ttf"
    ]
    
    for caminho in caminhos_roboto:
        if os.path.exists(caminho):
            try:
                return ImageFont.truetype(caminho, font_size)
            except Exception:
                pass

    # Se a Roboto falhar por algum motivo, tenta usar fontes do Linux que suportam acentos
    fontes_sistema_com_acentos = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    
    for caminho in fontes_sistema_com_acentos:
        if os.path.exists(caminho):
            try:
                return ImageFont.truetype(caminho, font_size)
            except Exception:
                pass
                
    # Fallback final se tudo der errado (fonte padrão sem acentos)
    return ImageFont.load_default()

# Inputs do Usuário
uploaded_image = st.file_uploader("Suba a imagem de fundo", type=["jpg", "jpeg", "png"])
text_input = st.text_input("Digite a mensagem para o muro (Máx. 100 caracteres):", max_chars=100)

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    W, H = image.size

    st.subheader("Visualização")

    if text_input:
        img_edit = image.copy()
        draw = ImageDraw.Draw(img_edit)

        # Proporção da fonte (~4.5% da largura da imagem)
        font_size = int(W * 0.045)
        font = carregar_fonte_correta(font_size)

        # Quebra o texto em linhas curtas para caber no muro
        lines = textwrap.wrap(text_input, width=18)

        # Define a área útil do muro
        muro_width = int(W * 0.48)
        margem_esquerda = int(W * 0.05)
        
        # Espaçamento vertical
        linha_altura = font_size + int(font_size * 0.4)
        total_text_height = len(lines) * linha_altura
        
        # Centralização vertical no muro
        muro_center_y = int(H * 0.60)
        current_y = muro_center_y - (total_text_height // 2)

        for line in lines:
            # Mede as dimensões da linha de texto de forma segura
            try:
                left, top, right, bottom = font.getbbox(line)
                text_w = right - left
            except Exception:
                text_w = draw.textlength(line, font=font)

            # Centraliza horizontalmente
            text_x = margem_esquerda + ((muro_width - text_w) // 2)

            # Desenha o texto em preto
            draw.text((text_x, current_y), line, fill="black", font=font)
            current_y += linha_altura

        # Exibe o resultado final na tela
        st.image(img_edit, caption="Seu post está pronto!", use_container_width=True)

        # Prepara a imagem para download
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
        st.image(image, caption="Aguardando texto...", use_container_width=True)
