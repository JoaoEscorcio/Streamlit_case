import streamlit as st
import pandas as pd
import requests
from aba1_mapa import render_mapa
from aba2_preco import render_preco
from aba3_distancias import render_distancias
from aba4_temporal import render_temporal

# ------------------- CONFIG -------------------
st.set_page_config(page_title="Dashboard do Mercado Imobiliário em Miami", layout="wide")

# ------------------- ESTILO EMBUTIDO -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root {
    --primary-color: #2E3A59;
    --secondary-color: #5A5A5A;
    --accent-color: #4C8BF5;
    --background-color: #F4F6FA;
    --card-color: #F4F6FA;
    --border-radius: 12px;
    --shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* Reset */
html, body, .stApp {
    background-color: var(--background-color) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--secondary-color) !important;
}

/* Remover fundo branco da barra de topo do Streamlit */
header[data-testid="stHeader"] {
    background-color: var(--light-bg) !important;
    box-shadow: none !important;
}


/* Cabeçalhos */
h1, h2, h3, h4, h5, h6 {
    color: var(--primary-color) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
}

/* Sidebar e elementos */
[data-testid="stSidebar"] > div {
    background-color: var(--background-color) !important;
    padding: 1rem;
}

/* Componentes interativos (sliders, selects, etc) */
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stNumberInput,
[data-testid="stSidebar"] .stCheckbox,
[data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] .stExpander {
    background-color: var(--card-color) !important;
    padding: 12px;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    border: none !important;
    margin-bottom: 18px;
}

/* Selectbox dropdown */
.stSelectbox label,
.stRadio label,
.stCheckbox label {
    font-weight: 600 !important;
    color: var(--primary-color) !important;
}

/* Botões */
.stButton > button {
    background-color: var(--accent-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: var(--border-radius);
    font-weight: 600;
    box-shadow: var(--shadow);
}

/* Caixas centrais do conteúdo */
.stSelectbox, .stSlider, .stNumberInput, .stTextInput, .stTextArea {
    background-color: var(--card-color) !important;
    border-radius: var(--border-radius);
    border: none !important;
    padding: 10px !important;
}

/* Container principal */
.block-container {
    padding: 2rem 3rem;
}

/* Rodapé */
footer {
    color: #999;
    text-align: center;
    font-size: 0.8rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ------------------- API -------------------
API_URL = "http://localhost:8000/api"

def get_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao obter dados: {e}")
        return {}

# ------------------- TOPO -------------------
st.markdown("<h1>Dashboard do Mercado Imobiliário em Miami</h1>", unsafe_allow_html=True)
st.markdown("<h2>Navegação entre Análises</h2>", unsafe_allow_html=True)

abas = ["Mapa Interativo", "Análise de Preço", "Impacto das Distâncias", "Análise Temporal de Vendas"]
aberta = st.selectbox("", options=abas)

# ------------------- FILTROS -------------------
st.sidebar.markdown("## Filtros Comuns")
quality_options = ["Qualquer"] + [str(i) for i in range(1, 10)]

min_price, max_price = st.sidebar.slider("Faixa de Preço ($)", 50000, 3000000, (100000, 800000))
max_age = st.sidebar.slider("Idade máxima das casas", 0, 100, 30)
min_area = st.sidebar.slider("Área Mínima (sq ft)", 500, 5000, 1000)
structure_quality = st.sidebar.selectbox("Qualidade da Estrutura", quality_options)

with st.sidebar.expander(" Distância e Ruído", expanded=False):
    max_ocean_dist = st.slider("Distância ao Oceano (m)", 0, 30000, 15000)
    max_hwy_dist = st.slider("Distância à Rodovia (m)", 0, 10000, 5000)
    airport_noise = st.selectbox("Ruído Aéreo", ["Qualquer", "Sim", "Não"])

params = {
    "min_price": min_price,
    "max_price": max_price,
    "max_age": max_age,
    "min_area": min_area,
    "max_ocean_dist": max_ocean_dist,
    "max_hwy_dist": max_hwy_dist,
}

if structure_quality != "Qualquer":
    params["structure_quality"] = int(structure_quality)

if airport_noise == "Sim":
    params["avno60plus"] = 1
elif airport_noise == "Não":
    params["avno60plus"] = 0

# ------------------- ABAS -------------------
if aberta == "Mapa Interativo":
    render_mapa(get_data, params)
elif aberta == "Análise de Preço":
    render_preco(get_data)
elif aberta == "Impacto das Distâncias":
    render_distancias(get_data)
elif aberta == "Análise Temporal de Vendas":
    render_temporal(get_data)

# ------------------- FOOTER -------------------
st.markdown("""
    <footer>Desenvolvido por João Victor Escorcio • <a href='mailto:jv.escorcio@gmail.com'>Contato</a></footer>
""", unsafe_allow_html=True)
