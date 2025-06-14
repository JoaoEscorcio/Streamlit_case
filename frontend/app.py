import streamlit as st
import pandas as pd
import requests
from aba1_map import render_mapa
from aba2_price import render_preco
from aba3_distance import render_distancias
from aba4_temporal import render_temporal

# ------------------- INITIAL PAGE SETUP -------------------
st.set_page_config(page_title="Miami Real Estate Dashboard", layout="wide")

# ------------------- CUSTOM EMBEDDED CSS -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root {
    --primary-color: #2E3A59;
    --secondary-color: #5A5A5A;
    --accent-color: #4C8BF5;
    --background-color: #F4F6FA;
    --card-color: #F4F6FA;
    --border-radius: 12px;
    --shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

html, body, .stApp {
    background-color: var(--background-color) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--secondary-color) !important;
}

header[data-testid="stHeader"] {
    background-color: var(--light-bg) !important;
    box-shadow: none !important;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--primary-color) !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] > div {
    background-color: var(--background-color) !important;
    padding: 1rem;
}

[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stNumberInput,
[data-testid="stSidebar"] .stCheckbox,
[data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] .stExpander {
    background-color: var(--card-color) !important;
    padding: 12px;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    border: none !important;
    margin-bottom: 18px;
}

.stSelectbox label,
.stRadio label,
.stCheckbox label {
    font-weight: 600 !important;
    color: var(--primary-color) !important;
}

.stButton > button {
    background-color: var(--accent-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: var(--border-radius);
    font-weight: 600;
    box-shadow: var(--shadow);
}

.stSelectbox, .stSlider, .stNumberInput, .stTextInput, .stTextArea {
    background-color: var(--card-color) !important;
    border-radius: var(--border-radius);
    border: none !important;
    padding: 10px !important;
}

.block-container {
    padding: 2rem 3rem;
}

footer {
    color: #999;
    text-align: center;
    font-size: 0.8rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ------------------- FUNCTION TO FETCH DATA VIA API -------------------
API_URL = "http://localhost:8000/api"

def get_data(endpoint, params=None):
    """
    Generic function to make backend API calls.
    """
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return {}

# ------------------- DASHBOARD HEADER -------------------
st.markdown("<h1>Miami Real Estate Market Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h2>Navigate between analyses</h2>", unsafe_allow_html=True)

# Navigation tabs
tabs = [
    "Interactive Map",
    "Price Analysis",
    "Impact of Distances",
    "Sales Time Analysis"
]
selected_tab = st.selectbox("", options=tabs)

# ------------------- DYNAMIC FILTERS FROM API -------------------
filters_range = get_data("houses/filters-range")

# Default values in case API fails
price_min = filters_range.get("price_min", 0)
price_max = filters_range.get("price_max", 3000000)
age_min = filters_range.get("age_min", 0)
age_max = filters_range.get("age_max", 100)
area_min = filters_range.get("area_min", 0)
area_max = filters_range.get("area_max", 10000)
qualities = filters_range.get("qualities", list(range(1, 10)))

# ------------------- SIDEBAR: INTERACTIVE FILTERS -------------------
st.sidebar.markdown("## Common Filters")

# Structure quality options
quality_options = ["Any"] + [str(q) for q in qualities]

# Price range slider
min_price, max_price = st.sidebar.slider("Price Range ($)", price_min, price_max, (price_min, price_max))

# Age slider
max_age = st.sidebar.slider("Maximum House Age", age_min, age_max, age_max)

# Area slider
min_area, max_area = st.sidebar.slider("Area Range (sq ft)", area_min, area_max, (area_min, area_max))

# Structure quality selectbox
structure_quality = st.sidebar.selectbox("Structure Quality", quality_options)

# Additional filters
with st.sidebar.expander("🌊 Distance and Noise", expanded=False):
    max_ocean_dist = st.slider("Distance to Ocean (m)", 0, 30000, 30000)
    max_hwy_dist = st.slider("Distance to Highway (m)", 0, 10000, 10000)
    airport_noise = st.selectbox("Airport Noise", ["Any", "Yes", "No"])

# ------------------- PARAMETER DICTIONARY -------------------
params = {
    "min_price": min_price,
    "max_price": max_price,
    "max_age": max_age,
    "min_area": min_area,
    "max_area": max_area,
    "max_ocean_dist": max_ocean_dist,
    "max_hwy_dist": max_hwy_dist,
}

# Optional filters
if structure_quality != "Any":
    params["structure_quality"] = int(structure_quality)
if airport_noise == "Yes":
    params["avno60plus"] = 1
elif airport_noise == "No":
    params["avno60plus"] = 0

# ------------------- TAB LOGIC -------------------
if selected_tab == "Interactive Map":
    render_mapa(get_data, params)
elif selected_tab == "Price Analysis":
    render_preco(get_data)
elif selected_tab == "Impact of Distances":
    render_distancias(get_data)
elif selected_tab == "Sales Time Analysis":
    render_temporal(get_data)

# ------------------- FOOTER -------------------
st.markdown("""
    <footer>Developed by João Victor Escorcio • <a href='mailto:jv.escorcio@gmail.com'>Contact</a></footer>
""", unsafe_allow_html=True)
