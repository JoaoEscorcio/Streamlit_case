# Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import plotly.express as px

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

# Barra lateral - Filtros Comuns
st.sidebar.header("🔍 Filtros Comuns")
min_price, max_price = st.sidebar.slider("Faixa de Preço ($)", 50000, 3000000, (100000, 800000))
max_age = st.sidebar.slider("Idade máxima das casas", 0, 100, 30)
min_area = st.sidebar.slider("Área Mínima (sq ft)", 500, 5000, 1000)
quality_options = ["Qualquer"] + [str(i) for i in range(1, 10)]
structure_quality = st.sidebar.selectbox("Qualidade da Estrutura", quality_options)

# Filtros Adicionais
st.sidebar.header("🌊 Distância e Ruído")
max_ocean_dist = st.sidebar.slider("Distância Máxima ao Oceano (m)", 0, 30000, 15000)
max_hwy_dist = st.sidebar.slider("Distância Máxima à Rodovia (m)", 0, 10000, 5000)
airport_noise = st.sidebar.selectbox("Ruído Aéreo", ["Qualquer", "Sim", "Não"])

# Prepara os parâmetros para a requisição
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

# 🗺️ Aba 1 - Mapa Interativo
if selected_tab == "Mapa Interativo":
    st.header("📍 Mapa Interativo com Filtros Avançados")
    houses = get_data("houses", params)
    if houses:
        df = pd.DataFrame(houses)
        # Verifica se as colunas corretas estão presentes
        if not all(col in df.columns for col in ["latitude", "longitude", "sale_prc", "tot_lvg_area", "structure_quality"]):
            st.error("Dados insuficientes para gerar o mapa.")
        else:
            # Renderizando o mapa com Pydeck
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=df["latitude"].mean(),
                    longitude=df["longitude"].mean(),
                    zoom=10,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=df,
                        get_position='[longitude, latitude]',
                        get_color='[200, 30, 0, 160]',
                        get_radius=100,
                        pickable=True,
                        auto_highlight=True,
                    )
                ],
                tooltip={"text": "Preço: ${sale_prc}\nÁrea: {tot_lvg_area} sq ft\nQualidade: {structure_quality}"}
            ))
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

# Aba 2 - Análise de Preço
if selected_tab == "Análise de Preço":
    st.header("💰 Análise de Preço por Área")

    price_stats = get_data("houses/price-stats")
    if price_stats:
        # Indicadores Principais (KPIs)
        st.subheader("📊 Indicadores de Preço")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Preço Médio", f"${price_stats['price_avg']:,.2f}")
        col2.metric("Preço Mediano", f"${price_stats['price_median']:,.2f}")
        col3.metric("Preço Mínimo", f"${price_stats['price_min']:,.2f}")
        col4.metric("Preço Máximo", f"${price_stats['price_max']:,.2f}")

        # Distribuição de Preços
        st.subheader("📈 Distribuição de Preços")
        prices = price_stats.get("price_distribution", [])
        if prices:
            df_prices = pd.DataFrame(prices, columns=["Preço"])
            fig_hist = px.histogram(df_prices, x="Preço", nbins=30, title="Distribuição dos Preços",
                                    labels={'Preço': 'Preço ($)', 'y': 'Contagem'},
                                    template="plotly_white")
            st.plotly_chart(fig_hist, use_container_width=True)

            # Gráfico Boxplot de Preço
            st.subheader("📦 Boxplot de Preços")
            fig_box = px.box(df_prices, y="Preço", title="Boxplot dos Preços",
                             labels={'y': 'Preço ($)'},
                             template="plotly_white")
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.warning("Nenhuma distribuição de preço disponível.")

        # Preço Médio por Qualidade da Estrutura
        st.subheader("🏠 Preço Médio por Qualidade da Estrutura")
        quality_price_avg = price_stats.get("quality_price_avg", {})
        if quality_price_avg:
            df_quality = pd.DataFrame(list(quality_price_avg.items()), columns=["Qualidade", "Preço Médio"])
            fig_bar = px.bar(df_quality, x="Qualidade", y="Preço Médio", title="Preço Médio por Qualidade da Estrutura",
                             labels={"Qualidade": "Qualidade da Estrutura", "Preço Médio": "Preço ($)"},
                             template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Dados de preço médio por qualidade não encontrados.")

        # Correlação entre Área e Preço
        st.subheader("📐 Relação entre Área e Preço")
        df_area_price = pd.DataFrame({
            "Área (sq ft)": [d for d in price_stats.get("living_area_distribution", [])],
            "Preço ($)": [d for d in price_stats.get("price_distribution", [])]
        })
        if not df_area_price.empty:
            fig_scatter = px.scatter(df_area_price, x="Área (sq ft)", y="Preço ($)", 
                                     title="Correlação entre Área e Preço",
                                     labels={"Área (sq ft)": "Área (sq ft)", "Preço ($)": "Preço ($)"},
                                     template="plotly_white")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("Dados de área e preço não encontrados.")
    else:
        st.warning("Dados de preço não encontrados.")


# 🛣️ Aba 3 - Impacto das Distâncias
elif selected_tab == "Impacto das Distâncias":
    st.header("🚗 Impacto da Distância no Preço")

    distance_stats = get_data("houses/distance-impact")
    if distance_stats:
        # 📊 Indicadores de Preço por Distância
        st.subheader("📊 Indicadores de Preço por Distância")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Médio Próximo ao Oceano", f"${distance_stats['avg_price_near_ocean']:,.2f}")
        col2.metric("Preço Médio Longe do Oceano", f"${distance_stats['avg_price_far_from_ocean']:,.2f}")
        col3.metric("Número de Imóveis Próximos ao Oceano", f"{distance_stats['count_near_ocean']}")

        col4, col5, col6 = st.columns(3)
        col4.metric("Preço Médio Próximo à Rodovia", f"${distance_stats['avg_price_near_highway']:,.2f}")
        col5.metric("Preço Médio Longe da Rodovia", f"${distance_stats['avg_price_far_from_highway']:,.2f}")
        col6.metric("Número de Imóveis Próximos à Rodovia", f"{distance_stats['count_near_highway']}")

        col7, col8, col9 = st.columns(3)
        col7.metric("Preço Médio com Ruído Aéreo", 
                   f"${distance_stats['avg_price_airport_noise']:,.2f}" if distance_stats['avg_price_airport_noise'] is not None else "N/A")
        col8.metric("Preço Médio sem Ruído Aéreo", 
                   f"${distance_stats['avg_price_no_airport_noise']:,.2f}" if distance_stats['avg_price_no_airport_noise'] is not None else "N/A")
        col9.metric("Número de Imóveis com Ruído Aéreo", 
                   f"{distance_stats['count_airport_noise']}" if distance_stats['count_airport_noise'] is not None else "N/A")

        # 🗺️ Gráfico de Barras - Preço Médio por Distância
        st.subheader("📊 Preço Médio por Distância")
        df_dist = pd.DataFrame({
            "Categoria": ["Perto Oceano", "Longe Oceano", "Perto Rodovia", "Longe Rodovia", "Com Ruído", "Sem Ruído"],
            "Preço Médio": [
                distance_stats.get('avg_price_near_ocean', 0), distance_stats.get('avg_price_far_from_ocean', 0),
                distance_stats.get('avg_price_near_highway', 0), distance_stats.get('avg_price_far_from_highway', 0),
                distance_stats.get('avg_price_airport_noise', 0), distance_stats.get('avg_price_no_airport_noise', 0)
            ]
        })
        fig_bar = px.bar(df_dist, x="Categoria", y="Preço Médio", title="Preço Médio por Categoria de Distância",
                         labels={"Categoria": "Categoria", "Preço Médio": "Preço ($)"},
                         template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)

        # 📦 Boxplot - Distribuição de Preços por Distância
        st.subheader("📦 Distribuição de Preços por Distância")
        df_boxplot = pd.DataFrame({
            "Categoria": (
                ["Perto Oceano"] * len(distance_stats['prices_near_ocean']) +
                ["Longe Oceano"] * len(distance_stats['prices_far_ocean']) +
                ["Perto Rodovia"] * len(distance_stats['prices_near_highway']) +
                ["Longe Rodovia"] * len(distance_stats['prices_far_highway']) +
                ["Com Ruído"] * len(distance_stats['prices_airport_noise']) +
                ["Sem Ruído"] * len(distance_stats['prices_no_airport_noise'])
            ),
            "Preço": (
                distance_stats['prices_near_ocean'] + distance_stats['prices_far_ocean'] +
                distance_stats['prices_near_highway'] + distance_stats['prices_far_highway'] +
                distance_stats['prices_airport_noise'] + distance_stats['prices_no_airport_noise']
            )
        })
        fig_box = px.box(df_boxplot, x="Categoria", y="Preço", title="Distribuição de Preços por Categoria",
                         labels={"Categoria": "Categoria", "Preço": "Preço ($)"},
                         template="plotly_white")
        st.plotly_chart(fig_box, use_container_width=True)

        # 📍 Gráfico de Dispersão - Distância vs Preço
        st.subheader("📍 Distância vs Preço")

        # Garantir consistência no tamanho das listas
        ocean_dist = distance_stats['prices_near_ocean'] + distance_stats['prices_far_ocean']
        hwy_dist = distance_stats['prices_near_highway'] + distance_stats['prices_far_highway']
        prices = distance_stats['prices_near_ocean'] + distance_stats['prices_far_ocean'] + \
                 distance_stats['prices_near_highway'] + distance_stats['prices_far_highway']

        min_length = min(len(ocean_dist), len(hwy_dist), len(prices))
        ocean_dist = ocean_dist[:min_length]
        hwy_dist = hwy_dist[:min_length]
        prices = prices[:min_length]

        df_scatter = pd.DataFrame({
            "Distância ao Oceano (m)": ocean_dist,
            "Distância à Rodovia (m)": hwy_dist,
            "Preço": prices
        })
        fig_scatter = px.scatter(df_scatter, x="Distância ao Oceano (m)", y="Preço", 
                                 title="Distância ao Oceano vs Preço",
                                 labels={"Distância ao Oceano (m)": "Distância ao Oceano (m)", "Preço": "Preço ($)"},
                                 template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)

    else:
        st.warning("Dados de impacto de distância não encontrados.")


# 🗓️ Aba 4 - Análise Temporal de Vendas
elif selected_tab == "Análise Temporal de Vendas":
    st.header("📅 Análise Temporal de Vendas")

    sales_time = get_data("houses/sales-time")
    if sales_time:
        # Convertendo os dados para DataFrame
        df_sales = pd.DataFrame(sales_time)

        # Garantindo que o tipo da coluna mês seja numérico
        df_sales['month'] = pd.to_numeric(df_sales['month'], errors='coerce')
        df_sales['average_price'] = pd.to_numeric(df_sales['average_price'], errors='coerce')

        # 📊 Indicadores Principais
        st.subheader("📊 Indicadores de Vendas Temporais")
        col1, col2, col3 = st.columns(3)
        current_year_avg = df_sales['average_price'].mean()
        prev_year_avg = current_year_avg * 0.95  # Estimando 5% de aumento para simulação
        col1.metric("Preço Médio Atual", f"${current_year_avg:,.2f}")
        col2.metric("Preço Médio Anterior", f"${prev_year_avg:,.2f}")
        col3.metric("Variação Anual", f"{((current_year_avg - prev_year_avg) / prev_year_avg) * 100:,.2f}%")

        # Mês com Maior e Menor Preço Médio
        max_month = df_sales.loc[df_sales['average_price'].idxmax()]
        min_month = df_sales.loc[df_sales['average_price'].idxmin()]
        col4, col5 = st.columns(2)
        col4.metric("📈 Mês com Maior Preço", f"Mês {int(max_month['month'])}", f"${max_month['average_price']:,.2f}")
        col5.metric("📉 Mês com Menor Preço", f"Mês {int(min_month['month'])}", f"${min_month['average_price']:,.2f}")

        # 📈 Gráfico de Linha - Evolução dos Preços
        st.subheader("📈 Evolução dos Preços ao Longo do Tempo")
        fig_line = px.line(df_sales, x="month", y="average_price", 
                           title="Variação Mensal dos Preços",
                           labels={"month": "Mês", "average_price": "Preço Médio ($)"},
                           template="plotly_white")
        st.plotly_chart(fig_line, use_container_width=True)

        # 📈 Gráfico de Linha com Média Móvel (3 Meses)
        st.subheader("📊 Média Móvel dos Preços (3 Meses)")
        df_sales['rolling_avg'] = df_sales['average_price'].rolling(window=3).mean()
        fig_rolling = px.line(df_sales, x="month", y="rolling_avg",
                              title="Média Móvel de 3 Meses dos Preços",
                              labels={"month": "Mês", "rolling_avg": "Preço Médio ($)"},
                              template="plotly_white")
        st.plotly_chart(fig_rolling, use_container_width=True)

        # 📊 Gráfico de Barras - Volume de Vendas por Mês
        st.subheader("📊 Volume de Vendas por Mês")
        fig_bar = px.bar(df_sales, x="month", y="total_sales",
                         title="Número de Vendas por Mês",
                         labels={"month": "Mês", "total_sales": "Número de Vendas"},
                         template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)

        # 📦 Gráfico Boxplot - Variação Mensal dos Preços
        st.subheader("📦 Variação Mensal dos Preços")
        fig_box = px.box(df_sales, x="month", y="average_price",
                         title="Distribuição dos Preços por Mês",
                         labels={"month": "Mês", "average_price": "Preço Médio ($)"},
                         template="plotly_white")
        st.plotly_chart(fig_box, use_container_width=True)

        # 📍 Gráfico de Dispersão - Mês vs Preço
        st.subheader("📍 Correlação Mês vs Preço")
        fig_scatter = px.scatter(df_sales, x="month", y="average_price", 
                                 title="Correlação entre Mês e Preço",
                                 labels={"month": "Mês", "average_price": "Preço Médio ($)"},
                                 template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)

    else:
        st.warning("Dados temporais não encontrados.")


st.markdown("---")
st.caption("Dashboard desenvolvido por João Victor Escorcio")
