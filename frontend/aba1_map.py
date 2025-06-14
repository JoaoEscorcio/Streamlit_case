# frontend/pages/aba1_map.py

import streamlit as st
import pandas as pd
import pydeck as pdk

def render_mapa(get_data, params):
    st.header("📍 Interactive Map with Advanced Filters")

    houses = get_data("houses", params)

    if not houses:
        st.warning("No data found for the selected filters.")
        return

    df = pd.DataFrame(houses)
    required_cols = ["latitude", "longitude", "sale_prc", "tot_lvg_area", "structure_quality"]
    if not all(col in df.columns for col in required_cols):
        st.error("Insufficient data to generate the map.")
        return

    # ------- Map 1: Scatterplot by Structure Quality --------
    st.subheader("🔴 Property Distribution by Structure Quality")

    df["color"] = df["structure_quality"].apply(lambda q: [255, int(255 - q * 28), 0, 160])  # orange/red gradient

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
                "ScatterplotLayer",
                data=df,
                get_position="[longitude, latitude]",
                get_color="color",
                get_radius=100,
                pickable=True,
                auto_highlight=True,
            )
        ],
        tooltip={
            "text": "🏡 Price: ${sale_prc}\n📐 Area: {tot_lvg_area} sq ft\n🏗️ Quality: {structure_quality}"
        }
    ))

    # ------- Map 2: Hexbin of Property Density --------
    st.subheader("🟣 Property Density by Region (Hexagons)")

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
                "HexagonLayer",
                data=df,
                get_position='[longitude, latitude]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            )
        ],
        tooltip={"text": "📍 Total properties in area: {elevationValue}"}
    ))
