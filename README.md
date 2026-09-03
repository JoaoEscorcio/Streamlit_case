# Miami Real Estate Market Dashboard

Interactive dashboard built with Streamlit and FastAPI, consuming real
estate data from Miami to deliver visual analyses and insights on property
prices, locations, structural quality, and external factors like noise and
distance to amenities.

## Stack

- [Streamlit](https://streamlit.io/) — interactive web interface
- [FastAPI](https://fastapi.tiangolo.com/) — backend API
- [Supabase](https://supabase.com/) — PostgreSQL database and auth
- [Plotly](https://plotly.com/python/) — visualizations
- [Pydeck](https://deckgl.readthedocs.io/en/latest/) — interactive geographic maps

## Features

**Interactive Map** — geographic visualization of filtered properties, scatterplot colored by structure quality, hexbin map showing property density by region.

**Price Analysis** — KPIs (average, median, min, max), price histogram and boxplot, area vs. price scatterplot, geographic clustering by price range.

**Impact of Distances** — KPIs comparing prices by proximity to ocean, highways, and airport noise; bar charts, boxplots, and distance vs. price scatterplots.

**Sales Time Analysis** — monthly evolution of sales prices, comparative KPIs with monthly variation, 3-month moving average trend.

**Filters** — price range, area and age ranges, structure quality, distance to ocean/highway/airport noise.

## Project structure

```
.
├── api/                    # FastAPI - data endpoints
│   └── main.py
├── frontend/                # Streamlit app
│   ├── app.py
│   └── pages/
│       ├── aba1_map.py
│       ├── aba2_price.py
│       ├── aba3_distance.py
│       └── aba4_temporal.py
├── poetry.lock
├── pyproject.toml
```

## Requirements

- Python 3.10+
- A [Supabase](https://supabase.com/) project

## Running locally

```bash
git clone https://github.com/JoaoEscorcio/Streamlit_case.git
cd Streamlit_case

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

poetry install
```

Create a `.env` file:

```env
SUPABASE_URL=https://<your-project>.supabase.co
SUPABASE_KEY=<your-api-key>
```

Run the API:

```bash
cd api
uvicorn main:app --reload --port 8000
```

Run the frontend (separate terminal):

```bash
cd frontend
streamlit run app.py
```

## Deployment

- **Render.com** for the FastAPI backend
- **Streamlit Community Cloud** for the frontend

## Possible next steps

- User authentication
- Report export
- Price prediction (ML)

## Author

João Escórcio — AI & Data Engineer
[LinkedIn](https://www.linkedin.com/in/joaovictorescorcio) · [Medium](https://medium.com/@jv.escorcio)
