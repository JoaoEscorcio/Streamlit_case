# aba4_temporal.py

import streamlit as st
import pandas as pd
import plotly.express as px
#from app_utils import get_data  # Supondo que sua função get_data esteja em um módulo utilitário

def render_temporal(get_data):
    st.header("📅 Análise Temporal de Vendas")

    sales_time = get_data("houses/sales-time")
    if sales_time:
        df_sales = pd.DataFrame(sales_time)

        df_sales['month'] = pd.to_numeric(df_sales['month'], errors='coerce')
        df_sales['average_price'] = pd.to_numeric(df_sales['average_price'], errors='coerce')

        # 📊 KPIs
        st.subheader("📊 Indicadores de Vendas Temporais")
        col1, col2, col3 = st.columns(3)
        current_year_avg = df_sales['average_price'].mean()
        prev_year_avg = current_year_avg * 0.95
        col1.metric("Preço Médio Atual", f"${current_year_avg:,.2f}")
        col2.metric("Preço Médio Anterior", f"${prev_year_avg:,.2f}")
        col3.metric("Variação Anual", f"{((current_year_avg - prev_year_avg) / prev_year_avg) * 100:,.2f}%")

        max_month = df_sales.loc[df_sales['average_price'].idxmax()]
        min_month = df_sales.loc[df_sales['average_price'].idxmin()]
        col4, col5 = st.columns(2)
        col4.metric("📈 Mês com Maior Preço", f"Mês {int(max_month['month'])}", f"${max_month['average_price']:,.2f}")
        col5.metric("📉 Mês com Menor Preço", f"Mês {int(min_month['month'])}", f"${min_month['average_price']:,.2f}")

        # 📈 Evolução de preços
        st.subheader("📈 Evolução dos Preços ao Longo do Tempo")
        fig_line = px.line(df_sales, x="month", y="average_price", 
                           title="Variação Mensal dos Preços",
                           labels={"month": "Mês", "average_price": "Preço Médio ($)"},
                           template="plotly_white")
        st.plotly_chart(fig_line, use_container_width=True)

        # Média móvel
        st.subheader("📊 Média Móvel dos Preços (3 Meses)")
        df_sales['rolling_avg'] = df_sales['average_price'].rolling(window=3).mean()
        fig_rolling = px.line(df_sales, x="month", y="rolling_avg",
                              title="Média Móvel de 3 Meses dos Preços",
                              labels={"month": "Mês", "rolling_avg": "Preço Médio ($)"},
                              template="plotly_white")
        st.plotly_chart(fig_rolling, use_container_width=True)

        # Volume de vendas
        st.subheader("📊 Volume de Vendas por Mês")
        fig_bar = px.bar(df_sales, x="month", y="total_sales",
                         title="Número de Vendas por Mês",
                         labels={"month": "Mês", "total_sales": "Número de Vendas"},
                         template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)

        # Boxplot
        st.subheader("📦 Variação Mensal dos Preços")
        fig_box = px.box(df_sales, x="month", y="average_price",
                         title="Distribuição dos Preços por Mês",
                         labels={"month": "Mês", "average_price": "Preço Médio ($)"},
                         template="plotly_white")
        st.plotly_chart(fig_box, use_container_width=True)

        # Dispersão
        st.subheader("📍 Correlação Mês vs Preço")
        fig_scatter = px.scatter(df_sales, x="month", y="average_price", 
                                 title="Correlação entre Mês e Preço",
                                 labels={"month": "Mês", "average_price": "Preço Médio ($)"},
                                 template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Dados temporais não encontrados.")
