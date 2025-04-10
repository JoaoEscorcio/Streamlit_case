# frontend/pages/aba1_mapa.py

import streamlit as st
import pandas as pd
import pydeck as pdk

def render_mapa(get_data, params):
    st.header("📍 Mapa Interativo com Filtros Avançados")

    houses = get_data("houses", params)

    if not houses:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    df = pd.DataFrame(houses)
    required_cols = ["latitude", "longitude", "sale_prc", "tot_lvg_area", "structure_quality"]
    if not all(col in df.columns for col in required_cols):
        st.error("Dados insuficientes para gerar o mapa.")
        return

    # ------- Mapa 1: Scatterplot por estrutura --------
    st.subheader("🔴 Distribuição dos Imóveis por Qualidade da Estrutura")

    df["color"] = df["structure_quality"].apply(lambda q: [255, int(255 - q * 28), 0, 160])  # degrade laranja/vermelho

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
            "text": "🏡 Preço: ${sale_prc}\n📐 Área: {tot_lvg_area} sq ft\n🏗️ Qualidade: {structure_quality}"
        }
    ))

    # ------- Mapa 2: Hexbin de densidade de imóveis -------
    st.subheader("🟣 Densidade de Imóveis por Região (Hexágonos)")

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
        tooltip={"text": "📍 Total de imóveis na área: {elevationValue}"}
    ))
