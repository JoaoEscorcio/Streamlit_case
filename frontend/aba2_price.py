import streamlit as st
import pandas as pd
import plotly.express as px

def render_preco(get_data):
    st.header("💰 Price Analysis by Area")

    price_stats = get_data("houses/price-stats")
    if price_stats:
        # ---------------- KPIs ----------------
        st.subheader("📊 Price Indicators")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average Price", f"${price_stats['price_avg']:,.2f}")
        col2.metric("Median Price", f"${price_stats['price_median']:,.2f}")
        col3.metric("Minimum Price", f"${price_stats['price_min']:,.2f}")
        col4.metric("Maximum Price", f"${price_stats['price_max']:,.2f}")

        # ---------------- Histogram ----------------
        st.subheader("📈 Price Distribution")
        prices = price_stats.get("price_distribution", [])
        if prices:
            df_prices = pd.DataFrame(prices, columns=["Price"])
            fig_hist = px.histogram(df_prices, x="Price", nbins=30,
                                    title="Price Distribution",
                                    labels={'Price': 'Price ($)', 'y': 'Count'})
            fig_hist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#31333F"),
                title_font=dict(size=18, color="#31333F"),
                hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
            )
            st.plotly_chart(fig_hist, use_container_width=True)

            # ---------------- Boxplot ----------------
            st.subheader("📦 Price Boxplot")
            fig_box = px.box(df_prices, y="Price", title="Price Boxplot",
                             labels={'Price': 'Price ($)'})
            fig_box.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#31333F"),
                title_font=dict(size=18, color="#31333F"),
                hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
            )
            st.plotly_chart(fig_box, use_container_width=True)

        # ---------------- Bar by Quality ----------------
        st.subheader("🏠 Average Price by Structure Quality")
        quality_price_avg = price_stats.get("quality_price_avg", {})
        if quality_price_avg:
            df_quality = pd.DataFrame(list(quality_price_avg.items()), columns=["Quality", "Average Price"])
            fig_bar = px.bar(df_quality, x="Quality", y="Average Price",
                             title="Average Price by Structure Quality",
                             labels={"Quality": "Structure Quality", "Average Price": "Price ($)"})
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#31333F"),
                title_font=dict(size=18, color="#31333F"),
                hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # ---------------- Area vs Price Scatter ----------------
        st.subheader("📐 Area vs. Price Relationship")
        living_area = price_stats.get("living_area_distribution", [])
        if prices and living_area and len(prices) == len(living_area):
            df_area_price = pd.DataFrame({
                "Living Area (sq ft)": living_area,
                "Price ($)": prices
            })
            fig_scatter = px.scatter(df_area_price, x="Living Area (sq ft)", y="Price ($)",
                                     title="Correlation Between Area and Price",
                                     labels={"Living Area (sq ft)": "Living Area (sq ft)", "Price ($)": "Price ($)"})
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#31333F"),
                title_font=dict(size=18, color="#31333F"),
                hoverlabel=dict(bgcolor="#F0F2F6", font_size=12)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        # ---------------- Price Cluster by Location ----------------
        st.subheader("📍 Price Range Clustering by Location")

        price_cluster = price_stats.get("price_cluster", [])
        if price_cluster:
            df_cluster = pd.DataFrame(price_cluster)

            color_map = {
                "Baixo": "#3B82F6",   # Low (blue)
                "Médio": "#F59E0B",   # Medium (orange)
                "Alto": "#EF4444"     # High (red)
            }

            fig_cluster = px.scatter_mapbox(
                df_cluster,
                lat="latitude",
                lon="longitude",
                color="Faixa de Preço",
                color_discrete_map=color_map,
                zoom=9,
                height=550,
                mapbox_style="carto-positron",
                hover_data={"sale_prc": True, "latitude": False, "longitude": False}
            )

            fig_cluster.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#31333F")
            )

            st.plotly_chart(fig_cluster, use_container_width=True)
        else:
            st.warning("Clustering data not available.")
    else:
        st.warning("Price data not found.")
