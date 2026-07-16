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

# Função melhorada para carregar fonte com suporte a acentos
def carregar_fonte_correta(font_size):
    # PRIORIDADE 1: Fontes do sistema que SABEMOS que funcionam com acentos
    fontes_sistema = [
        # Linux (Streamlit Cloud usa Ubuntu)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        
        # Mac
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        
        # Windows
        "C:\\Windows\\Fonts\\Arial.ttf",
        "C:\\Windows\\Fonts\\Arialbd.ttf",
        "C:\\Windows\\Fonts\\SegoeUI.ttf"
    ]
    
    for caminho in fontes_sistema:
        if os.path.exists(caminho):
            try:
                font = ImageFont.truetype(caminho, font_size)
                # Testa se a fonte suporta acentos
                test_chars = "áéíóúãõç"
                try:
                    font.getbbox(test_chars)
                    return font
                except:
                    pass
            except Exception:
                pass

    # PRIORIDADE 2: Tentar a Roboto se existir (mas agora com verificação)
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminhos_roboto = [
        os.path.join(diretorio_atual, "Roboto-Bold.ttf"),
        os.path.join(diretorio_atual, "fonts", "Roboto-Bold.ttf"),
        "/mount/src/my_git/Roboto-Bold.ttf",
        "Roboto-Bold.ttf"
    ]
    
    for caminho in caminhos_roboto:
        if os.path.exists(caminho):
            try:
                font = ImageFont.truetype(caminho, font_size)
                # Testa acentos
                test_chars = "áéíóúãõç"
                try:
                    font.getbbox(test_chars)
                    return font
                except:
                    pass
            except Exception as e:
                # Ignora o erro e continua
                pass

    # PRIORIDADE 3: Fallback - DejaVu Sans (quase sempre funciona)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        return font
    except:
        # Último recurso
        return ImageFont.load_default()

# Inputs do Usuário
uploaded_image = st.file_uploader("Suba a imagem de fundo", type=["jpg", "jpeg", "png"])
text_input = st.text_input("Digite a mensagem para o muro (Máx. 100 caracteres):", max_chars=100)

# Opção para ajustar o tamanho da fonte
st.subheader("⚙️ Ajustes")
tamanho_fonte = st.slider(
    "Tamanho da fonte (%)", 
    min_value=5, 
    max_value=15, 
    value=8,  # Aumentei mais ainda
    help="Aumente ou diminua o tamanho da fonte na imagem"
)

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    W, H = image.size

    st.subheader("Visualização")

    if text_input:
        img_edit = image.copy()
        draw = ImageDraw.Draw(img_edit)

        # Tamanho da fonte ajustável
        font_size = int(W * (tamanho_fonte / 100))
        
        # Mostra informações de debug
        st.caption(f"📐 Tamanho da fonte: {font_size}px | Largura da imagem: {W}px")
        
        # Carrega a fonte
        font = carregar_fonte_correta(font_size)
        
        # Testa se a fonte suporta acentos
        try:
            test_text = "áéíóúãõç"
            font.getbbox(test_text)
            st.success("✅ Fonte com suporte a acentos carregada!")
        except:
            st.warning("⚠️ Fonte básica carregada (pode não mostrar acentos corretamente)")

        # Calcula quantos caracteres cabem por linha
        try:
            # Usa um caractere médio para calcular
            sample_text = "A"
            bbox = font.getbbox(sample_text)
            char_width = bbox[2] - bbox[0]
        except:
            char_width = font_size * 0.6
        
        # Largura disponível para texto (50% da imagem para mais espaço)
        espaco_disponivel = int(W * 0.45)
        char_limit = max(8, int(espaco_disponivel / char_width))
        
        # Quebra o texto em linhas
        lines = textwrap.wrap(text_input, width=char_limit)

        # Define a área útil do muro
        muro_width = int(W * 0.45)
        margem_esquerda = int(W * 0.05)
        
        # Espaçamento vertical
        linha_altura = int(font_size * 1.6)  # Mais espaçamento
        total_text_height = len(lines) * linha_altura
        
        # Centralização vertical (55% da altura)
        muro_center_y = int(H * 0.55)
        current_y = muro_center_y - (total_text_height // 2)

        # Desenha cada linha
        for line in lines:
            # Mede a largura exata da linha
            try:
                bbox = font.getbbox(line)
                text_w = bbox[2] - bbox[0]
            except AttributeError:
                text_w = draw.textlength(line, font=font)
            except:
                text_w = len(line) * char_width

            # Centraliza horizontalmente dentro da área do muro
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

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Baixar Imagem",
                data=img_byte_arr,
                file_name="post_muro.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
        with col2:
            # Mostra informações do texto
            st.caption(f"📝 Texto: {text_input}")
            st.caption(f"📏 Linhas: {len(lines)}")
            st.caption(f"🔤 Caracteres por linha: ~{char_limit}")
    else:
        st.image(image, caption="Aguardando texto...", use_container_width=True)
else:
    st.info("👆 Faça upload de uma imagem para começar!")

# Rodapé
st.markdown("---")
st.caption("Feito com ❤️ para a Betty - Com acentos e fonte ajustável!")
