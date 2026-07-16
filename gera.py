import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import io

# Configuração da página do Streamlit
st.set_page_config(page_title="Gerador de Frases da Betty", layout="centered")

# Título principal do aplicativo
st.title("📸 Gerador de Frases no Muro")
st.write("Suba a foto do muro, digite sua mensagem em português ou espanhol!")

# Função para carregar a fonte Roboto com suporte a acentos
def carregar_fonte_correta(font_size):
    # Encontra a pasta atual do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Lista de tentativas para carregar a Roboto-Bold
    caminhos_roboto = [
        os.path.join(diretorio_atual, "Roboto-Bold.ttf"),
        os.path.join(diretorio_atual, "fonts", "Roboto-Bold.ttf"),
        "/mount/src/my_git/Roboto-Bold.ttf",
        "/mount/src/my_git/fonts/Roboto-Bold.ttf",
        "Roboto-Bold.ttf",
        "fonts/Roboto-Bold.ttf"
    ]
    
    for caminho in caminhos_roboto:
        if os.path.exists(caminho):
            try:
                return ImageFont.truetype(caminho, font_size)
            except Exception:
                pass

    # Se a Roboto falhar, tenta fontes do sistema
    fontes_sistema = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
        "/System/Library/Fonts/Helvetica.ttc",  # Mac
        "C:\\Windows\\Fonts\\Arial.ttf",        # Windows
        "C:\\Windows\\Fonts\\Arialbd.ttf"       # Windows Bold
    ]
    
    for caminho in fontes_sistema:
        if os.path.exists(caminho):
            try:
                return ImageFont.truetype(caminho, font_size)
            except Exception:
                pass
                
    # Fallback final
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except:
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
        # Ajusta a largura das linhas baseado no tamanho da imagem
        char_limit = max(12, int(W * 0.48 / (font_size * 0.6)))
        lines = textwrap.wrap(text_input, width=char_limit)

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
            # Mede as dimensões da linha de texto
            try:
                bbox = font.getbbox(line)
                text_w = bbox[2] - bbox[0]
            except AttributeError:
                # Fallback para versões mais antigas do Pillow
                text_w = draw.textlength(line, font=font)
            except:
                # Fallback genérico
                text_w = len(line) * font_size * 0.6

            # Centraliza horizontalmente
            text_x = margem_esquerda + ((muro_width - text_w) // 2)

            # Desenha o texto em preto
            draw.text((text_x, current_y), line, fill="black", font=font)
            current_y += linha_altura

        # Exibe o resultado final na tela
        st.image(img_edit, caption="Seu post está pronto!", use_container_width=True)

        # Prepara a imagem para download
        img_byte_arr = io.BytesIO()
        img_edit.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr = img_byte_arr.getvalue()

        st.download_button(
            label="📥 Baixar Imagem para Rede Social",
            data=img_byte_arr,
            file_name="post_muro.jpg",
            mime="image/jpeg"
        )
    else:
        st.image(image, caption="Aguardando texto...", use_container_width=True)
else:
    st.info("👆 Faça upload de uma imagem para começar!")

# Rodapé
st.markdown("---")
st.caption("App da Betty")
