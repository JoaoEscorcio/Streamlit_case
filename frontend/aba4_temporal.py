import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_temporal(get_data):
    st.header("📅 Análise Temporal de Vendas")

    stats = get_data("houses/sales-time")

    if stats:
        df = pd.DataFrame(stats)
        df = df.sort_values("month")
        df["average_price"] = df["average_price"].astype(float)

        # Transformar número do mês para nome
        month_map = {
            1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
            7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
        }
        df["Mês"] = df["month"].map(month_map)

        # ----------- KPIs ----------
        st.subheader("📊 Indicadores de Variação de Preço")
        col1, col2, col3 = st.columns(3)
        atual = df["average_price"].iloc[-1]
        anterior = df["average_price"].iloc[-2]
        variacao = ((atual - anterior) / anterior) * 100

        col1.metric("Preço Médio Atual", f"${atual:,.2f}")
        col2.metric("Preço Médio Anterior", f"${anterior:,.2f}")
        col3.metric("Variação Mensal", f"{variacao:.2f}%", delta_color="inverse" if variacao < 0 else "normal")

        # ----------- Destaques ----------
        best = df.loc[df["average_price"].idxmax()]
        worst = df.loc[df["average_price"].idxmin()]
        st.markdown("### 🏆 Melhor Mês")
        st.write(f"**{month_map[int(best['month'])]}** — ${best['average_price']:,.2f}")

        st.markdown("### 📉 Pior Mês")
        st.write(f"**{month_map[int(worst['month'])]}** — ${worst['average_price']:,.2f}")

        # ----------- Gráfico com Média Móvel ----------
        st.subheader("📈 Evolução dos Preços com Média Móvel")

        df["Média Móvel (3M)"] = df["average_price"].rolling(window=3).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Mês"], y=df["average_price"],
            mode="lines+markers", name="Preço Médio",
            line=dict(color="#4C8BF5", width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df["Mês"], y=df["Média Móvel (3M)"],
            mode="lines", name="Média Móvel (3M)",
            line=dict(color="#FF9900", dash="dash", width=2)
        ))
        fig.update_layout(
            title="Preço Médio por Mês (com Média Móvel)",
            xaxis_title="Mês",
            yaxis_title="Preço ($)",
            font=dict(color="#31333F"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Dados temporais não encontrados.")
