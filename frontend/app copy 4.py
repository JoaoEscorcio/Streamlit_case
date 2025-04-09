import streamlit as st
import pandas as pd
import plotly.express as px

def render_temporal(get_data):
    st.header("📅 Análise Temporal de Vendas")

    stats = get_data("houses/temporal-analysis")

    if stats:
        st.subheader("📊 Indicadores de Vendas Temporais")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Médio Atual", f"${stats['avg_price']:,.2f}")
        col2.metric("Preço Médio Anterior", f"${stats['prev_avg_price']:,.2f}")
        col3.metric("Variação Anual", f"{stats['annual_variation']:.2f}%")

        col4, col5 = st.columns(2)
        col4.metric("📈 Mês com Maior Preço", f"Mês {stats['month_max']}", delta=f"${stats['max_price']:,.2f}")
        col5.metric("📉 Mês com Menor Preço", f"Mês {stats['month_min']}", delta=f"${stats['min_price']:,.2f}")

        # Gráfico de Linha - Variação dos Preços ao Longo do Tempo
        st.subheader("📉 Evolução dos Preços ao Longo do Tempo")
        df_monthly = pd.DataFrame({
            "Mês": stats["months"],
            "Preço Médio": stats["monthly_prices"]
        })

        fig_line = px.line(df_monthly, x="Mês", y="Preço Médio",
                           title="Variação Mensal dos Preços",
                           labels={"Mês": "Mês", "Preço Médio": "Preço ($)"},
                           template=None)

        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#1E1E2F"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.07)")
        )

        st.plotly_chart(fig_line, use_container_width=True)

        # Média móvel de 3 meses
        st.subheader("📊 Média Móvel dos Preços (3 Meses)")
        df_monthly["Média Móvel"] = df_monthly["Preço Médio"].rolling(window=3).mean()

        fig_avg = px.line(df_monthly, x="Mês", y="Média Móvel",
                          title="Média Móvel de 3 Meses dos Preços",
                          labels={"Mês": "Mês", "Média Móvel": "Preço ($)"},
                          template=None)

        fig_avg.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#1E1E2F"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.07)")
        )

        st.plotly_chart(fig_avg, use_container_width=True)
    else:
        st.warning("Dados temporais não encontrados.")
