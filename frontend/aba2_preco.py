# aba2_preco.py

import streamlit as st
import pandas as pd
import plotly.express as px
#from app_utils import get_data  # Ou o caminho do seu get_data se estiver separado

def render_preco(get_data):
    st.header("💰 Análise de Preço por Área")

    price_stats = get_data("houses/price-stats")
    if price_stats:
        # KPIs
        st.subheader("📊 Indicadores de Preço")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Preço Médio", f"${price_stats['price_avg']:,.2f}")
        col2.metric("Preço Mediano", f"${price_stats['price_median']:,.2f}")
        col3.metric("Preço Mínimo", f"${price_stats['price_min']:,.2f}")
        col4.metric("Preço Máximo", f"${price_stats['price_max']:,.2f}")

        # Histograma de Preços
        st.subheader("📈 Distribuição de Preços")
        prices = price_stats.get("price_distribution", [])
        if prices:
            df_prices = pd.DataFrame(prices, columns=["Preço"])
            fig_hist = px.histogram(df_prices, x="Preço", nbins=30,
                                    title="Distribuição dos Preços",
                                    labels={'Preço': 'Preço ($)', 'y': 'Contagem'},
                                    template="plotly_white")
            st.plotly_chart(fig_hist, use_container_width=True)

            # Boxplot
            st.subheader("📦 Boxplot de Preços")
            fig_box = px.box(df_prices, y="Preço", title="Boxplot dos Preços",
                             labels={'Preço': 'Preço ($)'},
                             template="plotly_white")
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.warning("Nenhuma distribuição de preço disponível.")

        # Barras - Preço Médio por Qualidade
        st.subheader("🏠 Preço Médio por Qualidade da Estrutura")
        quality_price_avg = price_stats.get("quality_price_avg", {})
        if quality_price_avg:
            df_quality = pd.DataFrame(list(quality_price_avg.items()), columns=["Qualidade", "Preço Médio"])
            fig_bar = px.bar(df_quality, x="Qualidade", y="Preço Médio",
                             title="Preço Médio por Qualidade da Estrutura",
                             labels={"Qualidade": "Qualidade da Estrutura", "Preço Médio": "Preço ($)"},
                             template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Dados de preço médio por qualidade não encontrados.")

        # Dispersão - Área vs Preço
        st.subheader("📐 Relação entre Área e Preço")
        living_area = price_stats.get("living_area_distribution", [])
        if prices and living_area and len(prices) == len(living_area):
            df_area_price = pd.DataFrame({
                "Área (sq ft)": living_area,
                "Preço ($)": prices
            })
            fig_scatter = px.scatter(df_area_price, x="Área (sq ft)", y="Preço ($)",
                                     title="Correlação entre Área e Preço",
                                     labels={"Área (sq ft)": "Área (sq ft)", "Preço ($)": "Preço ($)"},
                                     template="plotly_white")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("Dados de área e preço não encontrados ou incompatíveis.")
    else:
        st.warning("Dados de preço não encontrados.")
