# Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import plotly.express as px

# Configurações gerais do dashboard
st.set_page_config(page_title="Dashboard do Mercado Imobiliário em Miami", layout="wide")

# Toggle de modo escuro ou claro
modo_escuro = st.sidebar.toggle("🌙 Modo Escuro", value=False)

# Atualiza classe do body com atributo `data-theme`
if modo_escuro:
    st.markdown('<body data-theme="dark">', unsafe_allow_html=True)
else:
    st.markdown('<body data-theme="light">', unsafe_allow_html=True)

# Importando os módulos das abas
from aba1_mapa import render_mapa
from aba2_preco import render_preco
from aba3_distancias import render_distancias
from aba4_temporal import render_temporal



# Carregando o CSS customizado
with open("frontend/style_moderno.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Definindo a URL da API
API_URL = "http://localhost:8000/api"

# Função para obter dados da API
def get_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao obter dados: {e}")
        return {}

# Início do container principal (estilizado via CSS)
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Título do dashboard
st.markdown("<h1>Dashboard do Mercado Imobiliário em Miami</h1>", unsafe_allow_html=True)

# Seletor de abas no topo
st.markdown("<h2>Navegação entre Análises</h2>", unsafe_allow_html=True)
tabs = ["Mapa Interativo", "Análise de Preço", "Impacto das Distâncias", "Análise Temporal de Vendas"]
selected_tab = st.selectbox(label="", options=tabs)

# Filtros da Sidebar
quality_options = ["Qualquer"] + [str(i) for i in range(1, 10)]

with st.sidebar.expander("🎛️ Filtros Comuns", expanded=True):
    min_price, max_price = st.slider("Faixa de Preço ($)", 50000, 3000000, (100000, 800000))
    max_age = st.slider("Idade máxima das casas", 0, 100, 30)
    min_area = st.slider("Área Mínima (sq ft)", 500, 5000, 1000)
    structure_quality = st.selectbox("Qualidade da Estrutura", quality_options)

with st.sidebar.expander("🌊 Distância e Ruído", expanded=False):
    max_ocean_dist = st.slider("Distância Máxima ao Oceano (m)", 0, 30000, 15000)
    max_hwy_dist = st.slider("Distância Máxima à Rodovia (m)", 0, 10000, 5000)
    airport_noise = st.selectbox("Ruído Aéreo", ["Qualquer", "Sim", "Não"])

# Parâmetros dos filtros
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

# Renderização das abas
if selected_tab == "Mapa Interativo":
    render_mapa(get_data, params)

elif selected_tab == "Análise de Preço":
    render_preco(get_data)

elif selected_tab == "Impacto das Distâncias":
    render_distancias(get_data)

elif selected_tab == "Análise Temporal de Vendas":
    render_temporal(get_data)

# Rodapé e fechamento do container

st.markdown("""
<div style="text-align:center; margin-top: 3rem; font-size: 0.9rem; color: #999;">
    Desenvolvido por João Victor Escorcio • <a href='mailto:jv.escorcio@gmail.com'>Contato</a>
</div>
""", unsafe_allow_html=True)

