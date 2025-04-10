import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_temporal(get_data):
    st.header("📅 Análise Temporal de Vendas")

    # Corrigido: Endpoint correto
    stats = get_data("houses/sales-time")

    if stats:
        df = pd.DataFrame(stats)

        # Ordenar e garantir integridade
        df = df.sort_values("month")
        df["average_price"] = df["average_price"].astype(float)

        # KPIs
        st.subheader("📊 Indicadores de Vendas Temporais")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Médio Atual", f"${df['average_price'].iloc[-1]:,.2f}")
        col2.metric("Preço Médio Anterior", f"${df['average_price'].iloc[-2]:,.2f}")
        var_percent = ((df['average_price'].iloc[-1] - df['average_price'].iloc[-2]) / df['average_price'].iloc[-2]) * 100
        col3.metric("Variação Mensal", f"{var_percent:.2f}%")

        # Melhor e pior mês
        best_month = df.loc[df['average_price'].idxmax()]
        worst_month = df.loc[df['average_price'].idxmin()]

        st.markdown("### 🏆 Mês com Maior Preço")
        st.write(f"**Mês {int(best_month['month'])}** — ${best_month['average_price']:,.2f}")

        st.markdown("### 📉 Mês com Menor Preço")
        st.write(f"**Mês {int(worst_month['month'])}** — ${worst_month['average_price']:,.2f}")

        # 📈 Gráfico de Evolução Mensal
        st.subheader("📈 Evolução dos Preços ao Longo do Tempo")
        fig = px.line(
            df, x="month", y="average_price",
            title="Variação Mensal dos Preços",
            labels={"month": "Mês", "average_price": "Preço Médio ($)"},
            template="plotly_white"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)

        # 📊 Gráfico da Média Móvel
        st.subheader("📊 Média Móvel dos Preços (3 Meses)")
        df["media_movel"] = df["average_price"].rolling(window=3).mean()
        fig_ma = go.Figure()
        fig_ma.add_trace(go.Scatter(x=df["month"], y=df["average_price"], mode="lines+markers", name="Preço Médio"))
        fig_ma.add_trace(go.Scatter(x=df["month"], y=df["media_movel"], mode="lines", name="Média Móvel (3 meses)", line=dict(dash="dash")))
        fig_ma.update_layout(
            title="Média Móvel de 3 Meses dos Preços",
            xaxis_title="Mês",
            yaxis_title="Preço ($)",
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_ma, use_container_width=True)

    else:
        st.warning("Dados temporais não encontrados.")
