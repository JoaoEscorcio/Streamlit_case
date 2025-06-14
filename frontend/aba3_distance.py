import streamlit as st
import pandas as pd
import plotly.express as px

def render_distancias(get_data):
    st.header("🚗 Impact of Distance on Price")

    distance_stats = get_data("houses/distance-impact")
    if distance_stats:
        # ---------------- KPIs ----------------
        st.subheader("📊 Price Indicators by Distance")
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg. Price Near Ocean", f"${distance_stats['avg_price_near_ocean']:,.2f}")
        col2.metric("Avg. Price Far from Ocean", f"${distance_stats['avg_price_far_from_ocean']:,.2f}")
        col3.metric("Properties Near Ocean", f"{distance_stats['count_near_ocean']}")

        col4, col5, col6 = st.columns(3)
        col4.metric("Avg. Price Near Highway", f"${distance_stats['avg_price_near_highway']:,.2f}")
        col5.metric("Avg. Price Far from Highway", f"${distance_stats['avg_price_far_from_highway']:,.2f}")
        col6.metric("Properties Near Highway", f"{distance_stats['count_near_highway']}")

        col7, col8, col9 = st.columns(3)
        col7.metric("Price with Airport Noise", f"${distance_stats['avg_price_airport_noise']:,.2f}" if distance_stats['avg_price_airport_noise'] else "N/A")
        col8.metric("Price without Airport Noise", f"${distance_stats['avg_price_no_airport_noise']:,.2f}" if distance_stats['avg_price_no_airport_noise'] else "N/A")
        col9.metric("Properties with Noise", f"{distance_stats['count_airport_noise']}" if distance_stats['count_airport_noise'] else "N/A")

        # ---------------- Bar Chart ----------------
        st.subheader("📊 Average Price by Distance Category")
        df_dist = pd.DataFrame({
            "Category": ["Near Ocean", "Far from Ocean", "Near Highway", "Far from Highway", "With Noise", "Without Noise"],
            "Average Price": [
                distance_stats.get('avg_price_near_ocean', 0),
                distance_stats.get('avg_price_far_from_ocean', 0),
                distance_stats.get('avg_price_near_highway', 0),
                distance_stats.get('avg_price_far_from_highway', 0),
                distance_stats.get('avg_price_airport_noise', 0),
                distance_stats.get('avg_price_no_airport_noise', 0)
            ]
        })
        fig_bar = px.bar(df_dist, x="Category", y="Average Price", title="Average Price by Distance Category")
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#31333F"), title_font=dict(size=18, color="#31333F"),
            hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # ---------------- Boxplot ----------------
        st.subheader("📦 Price Distribution by Category")
        df_boxplot = pd.DataFrame({
            "Category": (
                ["Near Ocean"] * len(distance_stats['prices_near_ocean']) +
                ["Far from Ocean"] * len(distance_stats['prices_far_ocean']) +
                ["Near Highway"] * len(distance_stats['prices_near_highway']) +
                ["Far from Highway"] * len(distance_stats['prices_far_highway']) +
                ["With Noise"] * len(distance_stats['prices_airport_noise']) +
                ["Without Noise"] * len(distance_stats['prices_no_airport_noise'])
            ),
            "Price": (
                distance_stats['prices_near_ocean'] + distance_stats['prices_far_ocean'] +
                distance_stats['prices_near_highway'] + distance_stats['prices_far_highway'] +
                distance_stats['prices_airport_noise'] + distance_stats['prices_no_airport_noise']
            )
        })
        fig_box = px.box(df_boxplot, x="Category", y="Price", title="Price Boxplot by Category")
        fig_box.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#31333F"), title_font=dict(size=18, color="#31333F"),
            hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
        )
        st.plotly_chart(fig_box, use_container_width=True)

        # ---------------- Scatter: Ocean Distance ----------------
        st.subheader("🌊 Scatter: Distance to Ocean vs Price")
        if distance_stats.get("dist_ocean") and distance_stats.get("dist_ocean_price"):
            df_scatter_ocean = pd.DataFrame({
                "Distance to Ocean (m)": distance_stats["dist_ocean"],
                "Price ($)": distance_stats["dist_ocean_price"]
            })
            fig_ocean = px.scatter(
                df_scatter_ocean, x="Distance to Ocean (m)", y="Price ($)",
                title="Distance to Ocean vs Price"
            )
            fig_ocean.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#31333F"), title_font=dict(size=18, color="#31333F"),
                hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
            )
            st.plotly_chart(fig_ocean, use_container_width=True)

        # ---------------- Scatter: Highway Distance ----------------
        st.subheader("🛣️ Scatter: Distance to Highway vs Price")
        if distance_stats.get("dist_hwy") and distance_stats.get("dist_hwy_price"):
            df_scatter_hwy = pd.DataFrame({
                "Distance to Highway (m)": distance_stats["dist_hwy"],
                "Price ($)": distance_stats["dist_hwy_price"]
            })
            fig_hwy = px.scatter(
                df_scatter_hwy, x="Distance to Highway (m)", y="Price ($)",
                title="Distance to Highway vs Price"
            )
            fig_hwy.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#31333F"), title_font=dict(size=18, color="#31333F"),
                hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
            )
            st.plotly_chart(fig_hwy, use_container_width=True)
    else:
        st.warning("Distance impact data not found.")
