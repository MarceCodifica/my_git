import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import io
import subprocess
import sys

# Configuração da página do Streamlit
st.set_page_config(page_title="Gerador de Frases da Betty", layout="centered")

# Título principal
st.title("📸 Gerador de Frases no Muro")
st.write("Suba a foto do muro, digite sua mensagem em português ou espanhol!")

# FUNÇÃO PARA INSTALAR FONTE NO STREAMLIT CLOUD
def instalar_fonte_noto():
    """Instala a fonte Noto Sans que suporta todos os acentos"""
    try:
        # Tenta instalar a fonte Noto Sans (funciona no Streamlit Cloud)
        subprocess.run(['apt-get', 'update'], check=False, capture_output=True)
        subprocess.run(['apt-get', 'install', '-y', 'fonts-noto'], check=False, capture_output=True)
        return True
    except:
        return False

# Tenta instalar a fonte Noto
if not os.path.exists("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"):
    with st.spinner("Instalando fontes com suporte a acentos..."):
        instalar_fonte_noto()

# FUNÇÃO MELHORADA PARA CARREGAR FONTE
def carregar_fonte_melhor(font_size):
    """
    Carrega uma fonte que SABEMOS que funciona com acentos
    Prioriza Noto Sans e DejaVu Sans
    """
    
    # Lista de fontes que funcionam com acentos (prioridade)
    fontes_confiaveis = [
        # Noto Sans (melhor para acentos)
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf",
        
        # DejaVu Sans (muito bom também)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        
        # Liberation Sans
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        
        # Ubuntu
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
    ]
    
    # Verifica cada fonte
    for caminho in fontes_confiaveis:
        if os.path.exists(caminho):
            try:
                # Tenta carregar a fonte
                font = ImageFont.truetype(caminho, font_size)
                
                # TESTA se a fonte realmente suporta acentos
                try:
                    test_text = "áéíóúãõç"
                    bbox = font.getbbox(test_text)
                    # Se chegou aqui, a fonte funciona!
                    return font
                except:
                    # Não suporta acentos, tenta a próxima
                    continue
                    
            except Exception:
                continue
    
    # Se nenhuma fonte com acentos foi encontrada, tenta o fallback
    try:
        # Último recurso: tenta qualquer fonte do sistema
        font = ImageFont.load_default()
        return font
    except:
        return ImageFont.load_default()

# Inputs do Usuário
uploaded_image = st.file_uploader("Suba a imagem de fundo", type=["jpg", "jpeg", "png"])
text_input = st.text_input("Digite a mensagem para o muro (Máx. 100 caracteres):", max_chars=100)

# Ajustes
st.subheader("⚙️ Ajustes")
col1, col2 = st.columns(2)
with col1:
    tamanho_fonte = st.slider(
        "Tamanho da fonte (%)", 
        min_value=5, 
        max_value=20, 
        value=30,  # Valor padrão maior
        help="Aumente ou diminua o tamanho da fonte"
    )
with col2:
    cor_texto = st.color_picker("Cor do texto", "#000000")

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    W, H = image.size

    st.subheader("Visualização")

    if text_input:
        img_edit = image.copy()
        draw = ImageDraw.Draw(img_edit)

        # Tamanho da fonte
        font_size = int(W * (tamanho_fonte / 100))
        
        # Carrega a fonte (agora com teste de acentos)
        font = carregar_fonte_melhor(font_size)
        
        # MOSTRA INFORMAÇÕES DA FONTE
        st.info(f"📐 Fonte: {font_size}px | Imagem: {W}x{H}")
        
        # Testa se a fonte suporta acentos
        try:
            test = "áéíóú"
            font.getbbox(test)
            st.success("✅ Fonte com suporte a acentos")
        except:
            st.error("❌ Fonte SEM suporte a acentos!")            
            st.warning("⚠️ Os acentos podem não aparecer corretamente")

        # Divide o texto em linhas
        # Calcula o tamanho de cada caractere
        try:
            sample = "A"
            bbox = font.getbbox(sample)
            char_width = bbox[2] - bbox[0]
        except:
            char_width = font_size * 0.6
        
        # Largura disponível (45% da imagem)
        largura_disponivel = int(W * 0.45)
        caracteres_por_linha = max(8, int(largura_disponivel / char_width))
        
        # Quebra o texto
        lines = textwrap.wrap(text_input, width=caracteres_por_linha)

        # Posicionamento
        muro_width = int(W * 0.45)
        margem_esquerda = int(W * 0.05)
        
        # Espaçamento entre linhas
        linha_altura = int(font_size * 1.8)  # Mais espaçamento
        total_text_height = len(lines) * linha_altura
        
        # Centraliza verticalmente
        muro_center_y = int(H * 0.50)
        current_y = muro_center_y - (total_text_height // 2)

        # Converte cor para tupla RGB
        cor_rgb = tuple(int(cor_texto[i:i+2], 16) for i in (1, 3, 5))

        # Desenha cada linha
        for line in lines:
            # Mede a largura da linha
            try:
                bbox = font.getbbox(line)
                text_w = bbox[2] - bbox[0]
            except:
                text_w = len(line) * char_width

            # Centraliza
            text_x = margem_esquerda + ((muro_width - text_w) // 2)

            # Desenha o texto
            draw.text((text_x, current_y), line, fill=cor_rgb, font=font)
            current_y += linha_altura

        # Exibe o resultado
        st.image(img_edit, caption="Resultado final", use_container_width=True)

        # Botão de download
        img_byte_arr = io.BytesIO()
        img_edit.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr = img_byte_arr.getvalue()

        st.download_button(
            label="📥 Baixar Imagem",
            data=img_byte_arr,
            file_name="post_muro.jpg",
            mime="image/jpeg",
            use_container_width=True
        )
        
        # Mostra o texto processado
        with st.expander("📝 Detalhes do texto"):
            st.write(f"**Texto original:** {text_input}")
            st.write(f"**Linhas:** {len(lines)}")
            for i, line in enumerate(lines, 1):
                st.write(f"Linha {i}: '{line}'")
                
    else:
        st.image(image, caption="Aguardando texto...", use_container_width=True)
else:
    st.info("👆 Faça upload de uma imagem para começar!")

# Rodapé
st.markdown("---")
st.caption("App da Betty!")
