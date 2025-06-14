import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_temporal(get_data):
    st.header("📅 Sales Time Analysis")

    stats = get_data("houses/sales-time")

    if stats:
        df = pd.DataFrame(stats)
        df = df.sort_values("month")
        df["average_price"] = df["average_price"].astype(float)

        # Month number to name (English)
        month_map = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }
        df["Month"] = df["month"].map(month_map)

        # ----------- KPIs ----------
        st.subheader("📊 Price Variation Indicators")
        col1, col2, col3 = st.columns(3)
        current = df["average_price"].iloc[-1]
        previous = df["average_price"].iloc[-2]
        variation = ((current - previous) / previous) * 100

        col1.metric("Current Avg. Price", f"${current:,.2f}")
        col2.metric("Previous Avg. Price", f"${previous:,.2f}")
        col3.metric("Monthly Variation", f"{variation:.2f}%", delta_color="inverse" if variation < 0 else "normal")

        # ----------- Highlights ----------
        best = df.loc[df["average_price"].idxmax()]
        worst = df.loc[df["average_price"].idxmin()]
        st.markdown("### 🏆 Best Month")
        st.write(f"**{month_map[int(best['month'])]}** — ${best['average_price']:,.2f}")

        st.markdown("### 📉 Worst Month")
        st.write(f"**{month_map[int(worst['month'])]}** — ${worst['average_price']:,.2f}")

        # ----------- Moving Average Chart ----------
        st.subheader("📈 Price Evolution with Moving Average")

        df["3-Month Moving Avg."] = df["average_price"].rolling(window=3).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Month"], y=df["average_price"],
            mode="lines+markers", name="Average Price",
            line=dict(color="#4C8BF5", width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df["Month"], y=df["3-Month Moving Avg."],
            mode="lines", name="3-Month Moving Avg.",
            line=dict(color="#FF9900", dash="dash", width=2)
        ))
        fig.update_layout(
            title="Monthly Average Price (with Moving Average)",
            xaxis_title="Month",
            yaxis_title="Price ($)",
            font=dict(color="#31333F"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Temporal data not found.")
