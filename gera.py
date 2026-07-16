import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Configuração da página do Streamlit (Título da aba do navegador)
st.set_page_config(page_title="Gerador de Frases da Betty", layout="centered")

# Título principal do aplicativo (H1)
st.title("📸 Gerador de Frases da Betty")
st.write("Suba a foto do muro, digite sua mensagem em português ou espanhol!")

# Função inteligente que monta o caminho correto para a fonte no servidor do Streamlit
def carregar_fonte_sistema(font_size):
    # Encontra a pasta onde o gera.py está rodando no servidor
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    fonte_local = os.path.join(diretorio_atual, "Roboto-Bold.ttf")
    
    if os.path.exists(fonte_local):
        return ImageFont.truetype(fonte_local, font_size)
        
    # Lista de caminhos comuns para fontes caso a fonte local não seja encontrada
    caminhos_fontes = [
        "/Library/Fonts/Arial.ttf",              # Mac
        "/System/Library/Fonts/Supplemental/Arial.ttf", # Mac Alternativo
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", # Linux (GitHub/Streamlit)
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" # Linux Alternativo
    ]
    
    for caminho in caminhos_fontes:
        if os.path.exists(caminho):
            return ImageFont.truetype(caminho, font_size)
            
    # Se tudo falhar, usa a padrão
    return ImageFont.load_default(size=font_size)

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

        # Proporção ideal da fonte (~4.5% da largura da imagem)
        font_size = int(W * 0.045)
        font = carregar_fonte_sistema(font_size)

        # Quebra o texto em linhas curtas para caber no muro de forma elegante
        lines = textwrap.wrap(text_input, width=18)

        # Define a área útil do muro (até 48% da largura total)
        muro_width = int(W * 0.48)
        margem_esquerda = int(W * 0.05)
        
        # Espaçamento vertical entre as linhas
        linha_altura = font_size + int(font_size * 0.4)
        total_text_height = len(lines) * linha_altura
        
        # Mantém o texto bem posicionado no meio/baixo do muro
        muro_center_y = int(H * 0.60)
        current_y = muro_center_y - (total_text_height // 2)

        for line in lines:
            left, top, right, bottom = font.getbbox(line)
            text_w = right - left

            # Centraliza a linha horizontalmente na área útil do muro
            text_x = margem_esquerda + ((muro_width - text_w) // 2)

            # Desenha o texto
            draw.text((text_x, current_y), line, fill="black", font=font)
            current_y += linha_altura

        # Exibe o resultado final com o texto aplicado
        st.image(img_edit, caption="Seu post está pronto!", use_column_width=True)

        # Prepara a imagem para o botão de download
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
