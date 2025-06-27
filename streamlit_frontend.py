import streamlit as st
from PIL import Image
import base64
import requests

# Configuração da página
st.set_page_config(
    page_title="Art Value Predictor",
    page_icon="🎨",
    layout="centered"
)

# Função para carregar imagens em base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# CSS personalizado
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        display: flex;
        align-items: center;
        min-height: 100vh;
    }}
    .block-container {{
        background-color: white !important;
        border-radius: 15px !important;
        padding: 2.5rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
        max-width: 900px !important;
        margin: auto !important;
        width: 90% !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Aplica o fundo artístico
set_background('images/background.jpg')

# Conteúdo do aplicativo
st.title("🎨 Art Value Predictor")
st.markdown("""
    **Estimate the market value of works of art.**
    
    Upload an image to get an estimate!
""")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    # Área de upload
    uploaded_file = st.file_uploader(
        "Upload artwork image.",
        type=["jpg", "jpeg", "png"],
        help="Formatos suportados: JPG, JPEG, PNG"
    )

    # Logo centralizado abaixo do uploader
    st.markdown(
        f'<div style="text-align: center; margin: 1.5rem 0;">'
        f'<img src="data:image/png;base64,{get_base64("images/logo.jpg")}" width="240">'
        f'</div>',
        unsafe_allow_html=True
    )

    # Exibe a imagem carregada
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Artwork loaded", use_container_width=True)

with col2:
    # Seção de dimensões (atualmente comentada)
    st.subheader("    Evaluate the work:")
    # width_cm = st.number_input(
    #     "Largura (cm)",
    #     min_value=1,
    #     max_value=1000,
    #     value=50,
    #     step=1
    # )
    # height_cm = st.number_input(
    #     "Altura (cm)",
    #     min_value=1,
    #     max_value=1000,
    #     value=60,
    #     step=1
    # )
    # width_in = width_cm * 0.393701  # Conversão para inches
    # height_in = height_cm * 0.393701

    # Botão para estimar
    if st.button("Estimate Value", use_container_width=True):
        if uploaded_file is not None:
            try:
                # Chamada para a API
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(
                    "https://the-value-of-art-790412683890.europe-west1.run.app/predict",
                    files=files
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Estimated value: **${result['predicted_price']:,.2f}**")
                else:
                    st.error(f"API error: {response.status_code}. Tente novamente.")
            except Exception as e:
                st.error(f"Failed to connect to API: {str(e)}")
        else:
            st.warning("Please, load an image first.")

# Rodapé
st.markdown("---")
st.markdown(
    '<div style="font-size: 0.8rem; color: #666; text-align: center; margin-top: 1rem;">'
    'The Value of Art - Le Wagon Demo Day Batch #1887'
    '</div>',
    unsafe_allow_html=True
)
