# Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

# Configurações gerais do dashboard
st.set_page_config(page_title="Dashboard do Mercado Imobiliário em Miami", layout="wide")

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

# Cabeçalho do dashboard
st.title("🏡 Dashboard do Mercado Imobiliário em Miami")

# Definindo as abas do dashboard
tabs = ["Mapa Interativo", "Análise de Preço", "Impacto das Distâncias", "Análise Temporal de Vendas"]
selected_tab = st.sidebar.radio("Navegação", tabs)

# Barra lateral - Filtros
st.sidebar.header("🔍 Filtros")
min_price, max_price = st.sidebar.slider("Faixa de Preço ($)", 50000, 3000000, (100000, 800000))
max_age = st.sidebar.slider("Idade máxima das casas", 0, 100, 30)
min_area = st.sidebar.slider("Área Mínima (sq ft)", 500, 5000, 1000)
quality_options = ["Qualquer"] + [str(i) for i in range(1, 10)]
structure_quality = st.sidebar.selectbox("Qualidade da Estrutura", quality_options)

# Prepara os parâmetros para a requisição
params = {
    "min_price": min_price,
    "max_price": max_price,
    "max_age": max_age,
    "min_area": min_area
}

if structure_quality != "Qualquer":
    params["structure_quality"] = int(structure_quality)

# Aba 1 - Mapa Interativo
if selected_tab == "Mapa Interativo":
    st.header("📍 Mapa Interativo com Filtros")
    houses = get_data("houses", params)
    if houses:
        df = pd.DataFrame(houses)
        st.map(df)
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

# Aba 2 - Análise de Preço
elif selected_tab == "Análise de Preço":
    st.header("💰 Análise de Preço por Área")
    price_stats = get_data("houses/price-stats")
    if price_stats:
        df_price = pd.DataFrame([price_stats])
        st.table(df_price)
    else:
        st.warning("Dados de preço não encontrados.")

# Aba 3 - Impacto das Distâncias
elif selected_tab == "Impacto das Distâncias":
    st.header("🚗 Impacto da Distância no Preço")
    distance_stats = get_data("houses/distance-impact")
    if distance_stats:
        st.json(distance_stats)
    else:
        st.warning("Dados de impacto de distância não encontrados.")

# Aba 4 - Análise Temporal de Vendas
elif selected_tab == "Análise Temporal de Vendas":
    st.header("📅 Análise Temporal de Vendas")
    sales_time = get_data("houses/sales-time")
    if sales_time:
        df_sales = pd.DataFrame(sales_time)
        st.line_chart(df_sales, x="month", y="average_price")
    else:
        st.warning("Dados temporais não encontrados.")

st.markdown("---")
st.caption("Dashboard desenvolvido por João Victor Escorcio")
