# frontend/pages/aba1_mapa.py

import streamlit as st
import pandas as pd
import pydeck as pdk

def render_mapa(get_data, params):
    st.header("📍 Mapa Interativo com Filtros Avançados")
    houses = get_data("houses", params)
    
    if houses:
        df = pd.DataFrame(houses)
        # Verifica se as colunas corretas estão presentes
        required_cols = ["latitude", "longitude", "sale_prc", "tot_lvg_area", "structure_quality"]
        if not all(col in df.columns for col in required_cols):
            st.error("Dados insuficientes para gerar o mapa.")
        else:
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
                        'ScatterplotLayer',
                        data=df,
                        get_position='[longitude, latitude]',
                        get_color='[200, 30, 0, 160]',
                        get_radius=100,
                        pickable=True,
                        auto_highlight=True,
                    )
                ],
                tooltip={"text": "Preço: ${sale_prc}\nÁrea: {tot_lvg_area} sq ft\nQualidade: {structure_quality}"}
            ))
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
