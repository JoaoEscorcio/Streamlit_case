import streamlit as st
import pandas as pd
import plotly.express as px

def render_distancias(get_data):
    st.header("🚗 Impacto da Distância no Preço")

    distance_stats = get_data("houses/distance-impact")
    if distance_stats:
        # KPIs 1
        st.subheader("📊 Indicadores de Preço por Distância")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Médio Próximo ao Oceano", f"${distance_stats['avg_price_near_ocean']:,.2f}")
        col2.metric("Preço Médio Longe do Oceano", f"${distance_stats['avg_price_far_from_ocean']:,.2f}")
        col3.metric("Nº Imóveis Próximos ao Oceano", f"{distance_stats['count_near_ocean']}")

        col4, col5, col6 = st.columns(3)
        col4.metric("Preço Médio Próximo à Rodovia", f"${distance_stats['avg_price_near_highway']:,.2f}")
        col5.metric("Preço Médio Longe da Rodovia", f"${distance_stats['avg_price_far_from_highway']:,.2f}")
        col6.metric("Nº Imóveis Próximos à Rodovia", f"{distance_stats['count_near_highway']}")

        col7, col8, col9 = st.columns(3)
        col7.metric("Preço com Ruído Aéreo", 
                   f"${distance_stats['avg_price_airport_noise']:,.2f}" if distance_stats['avg_price_airport_noise'] else "N/A")
        col8.metric("Preço sem Ruído Aéreo", 
                   f"${distance_stats['avg_price_no_airport_noise']:,.2f}" if distance_stats['avg_price_no_airport_noise'] else "N/A")
        col9.metric("Nº Imóveis com Ruído", 
                   f"{distance_stats['count_airport_noise']}" if distance_stats['count_airport_noise'] else "N/A")

        # Gráfico de Barras
        st.subheader("📊 Preço Médio por Categoria de Distância")
        df_dist = pd.DataFrame({
            "Categoria": ["Perto Oceano", "Longe Oceano", "Perto Rodovia", "Longe Rodovia", "Com Ruído", "Sem Ruído"],
            "Preço Médio": [
                distance_stats.get('avg_price_near_ocean', 0),
                distance_stats.get('avg_price_far_from_ocean', 0),
                distance_stats.get('avg_price_near_highway', 0),
                distance_stats.get('avg_price_far_from_highway', 0),
                distance_stats.get('avg_price_airport_noise', 0),
                distance_stats.get('avg_price_no_airport_noise', 0)
            ]
        })
        fig_bar = px.bar(
            df_dist, x="Categoria", y="Preço Médio", 
            title="Preço Médio por Categoria de Distância",
            labels={"Categoria": "Categoria", "Preço Médio": "Preço ($)"}
        )
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#31333F"),
            title_font=dict(size=18, color="#31333F"),
            hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Boxplot de Preços
        st.subheader("📦 Distribuição de Preços por Categoria")
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
        fig_box = px.box(
            df_boxplot, x="Categoria", y="Preço",
            title="Boxplot de Preços por Categoria",
            labels={"Categoria": "Categoria", "Preço": "Preço ($)"}
        )
        fig_box.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#31333F"),
            title_font=dict(size=18, color="#31333F"),
            hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
        )
        st.plotly_chart(fig_box, use_container_width=True)

        # Gráfico de Dispersão
        st.subheader("📍 Correlação entre Distância e Preço")
        ocean_dist = distance_stats['prices_near_ocean'] + distance_stats['prices_far_ocean']
        hwy_dist = distance_stats['prices_near_highway'] + distance_stats['prices_far_highway']
        prices = ocean_dist + hwy_dist

        min_len = min(len(ocean_dist), len(hwy_dist), len(prices))
        if min_len > 0:
            df_scatter = pd.DataFrame({
                "Distância ao Oceano (m)": ocean_dist[:min_len],
                "Distância à Rodovia (m)": hwy_dist[:min_len],
                "Preço": prices[:min_len]
            })
            fig_scatter = px.scatter(
                df_scatter, x="Distância ao Oceano (m)", y="Preço",
                title="Distância ao Oceano vs Preço",
                labels={"Distância ao Oceano (m)": "Distância ao Oceano (m)", "Preço": "Preço ($)"}
            )
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#31333F"),
                title_font=dict(size=18, color="#31333F"),
                hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("Dados insuficientes para o gráfico de dispersão.")
    else:
        st.warning("Dados de impacto de distância não encontrados.")
