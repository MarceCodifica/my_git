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
    # Encontra a pasta atual do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # PRIORIDADE: Tentar carregar a Roboto-Bold que você enviou
    caminhos_roboto = [
        os.path.join(diretorio_atual, "Roboto-Bold.ttf"),
        os.path.join(diretorio_atual, "fonts", "Roboto-Bold.ttf"),
        os.path.join(diretorio_atual, "Roboto-Regular.ttf"),
        os.path.join(diretorio_atual, "fonts", "Roboto-Regular.ttf"),
        "/mount/src/my_git/Roboto-Bold.ttf",
        "/mount/src/my_git/fonts/Roboto-Bold.ttf",
        "Roboto-Bold.ttf",
        "fonts/Roboto-Bold.ttf"
    ]
    
    for caminho in caminhos_roboto:
        if os.path.exists(caminho):
            try:
                return ImageFont.truetype(caminho, font_size)
            except Exception as e:
                st.warning(f"Erro ao carregar {caminho}: {e}")
                pass

    # SEGUNDA OPÇÃO: Fontes do sistema com suporte a acentos
    fontes_sistema = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",  # Mac - suporte a acentos
        "/System/Library/Fonts/Helvetica.ttc",  # Mac
        "C:\\Windows\\Fonts\\Arial.ttf",  # Windows
        "C:\\Windows\\Fonts\\Arialbd.ttf",  # Windows Bold
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"  # Linux - ótimo para acentos
    ]
    
    for caminho in fontes_sistema:
        if os.path.exists(caminho):
            try:
                return ImageFont.truetype(caminho, font_size)
            except Exception:
                pass
                
    # Fallback final - tenta qualquer fonte disponível
    try:
        # Tenta DejaVu Sans que é muito bom com acentos
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except:
        # Último recurso - fonte padrão (pode não ter acentos)
        return ImageFont.load_default()

# Inputs do Usuário
uploaded_image = st.file_uploader("Suba a imagem de fundo", type=["jpg", "jpeg", "png"])
text_input = st.text_input("Digite a mensagem para o muro (Máx. 100 caracteres):", max_chars=100)

# Opção para ajustar o tamanho da fonte
st.subheader("⚙️ Ajustes")
tamanho_fonte = st.slider(
    "Tamanho da fonte (%)", 
    min_value=3, 
    max_value=10, 
    value=7,  # Aumentei o valor padrão de 4.5 para 7
    help="Aumente ou diminua o tamanho da fonte na imagem"
)

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    W, H = image.size

    st.subheader("Visualização")

    if text_input:
        img_edit = image.copy()
        draw = ImageDraw.Draw(img_edit)

        # Tamanho da fonte agora é ajustável (padrão 7% da largura)
        font_size = int(W * (tamanho_fonte / 100))
        
        # Mostra informações de debug
        st.caption(f"Tamanho da fonte: {font_size}px | Largura da imagem: {W}px")
        
        # Carrega a fonte
        font = carregar_fonte_correta(font_size)
        
        # Verifica se a fonte suporta acentos (apenas para debug)
        try:
            test_char = "áéíóúãõç"
            font.getbbox(test_char)
            st.success("✅ Fonte com suporte a acentos carregada!")
        except:
            st.warning("⚠️ A fonte carregada pode não suportar acentos corretamente")

        # Quebra o texto em linhas - ajuste dinâmico
        # Calcula quantos caracteres cabem em cada linha
        try:
            # Testa com um caractere médio
            char_width = font.getbbox("A")[2] - font.getbbox("A")[0]
        except:
            char_width = font_size * 0.6
        
        # Largura disponível para texto (45% da imagem)
        espaco_disponivel = int(W * 0.45)
        char_limit = max(8, int(espaco_disponivel / char_width))
        
        # Quebra o texto
        lines = textwrap.wrap(text_input, width=char_limit)
        
        # Se o texto não quebrou em múltiplas linhas, força uma quebra mais curta
        if len(lines) == 1 and len(text_input) > char_limit:
            lines = textwrap.wrap(text_input, width=char_limit - 3)

        # Define a área útil do muro
        muro_width = int(W * 0.45)
        margem_esquerda = int(W * 0.05)
        
        # Espaçamento vertical
        linha_altura = int(font_size * 1.5)  # Aumentei o espaçamento
        total_text_height = len(lines) * linha_altura
        
        # Centralização vertical no muro (60% da altura)
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
            # Mostra o texto que foi escrito
            st.caption(f"📝 Texto: {text_input}")
            st.caption(f"📏 Linhas: {len(lines)}")
    else:
        st.image(image, caption="Aguardando texto...", use_container_width=True)
else:
    st.info("👆 Faça upload de uma imagem para começar!")

# Rodapé
st.markdown("---")
st.caption("App da Betty")
