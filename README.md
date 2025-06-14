# 🌍 Miami Real Estate Market Dashboard

This project is an **interactive dashboard** built with **Streamlit** and **FastAPI**, consuming real estate data from Miami to deliver **visual analyses and strategic insights** on property prices, locations, structural quality, and external influences like noise and distances.

---

## 🚀 Technologies Used

- [Streamlit](https://streamlit.io/) – Interactive web interface
- [FastAPI](https://fastapi.tiangolo.com/) – Backend API services
- [Supabase](https://supabase.com/) – Cloud-based database and authentication (PostgreSQL)
- [Plotly](https://plotly.com/python/) – Dynamic and professional visualizations
- [Pydeck](https://deckgl.readthedocs.io/en/latest/) – Geographic visualizations (interactive maps)

---

## 🔍 Features

### 📊 Tab 1: **Interactive Map**

- Geographic visualization of filtered properties
- Scatterplot colored by structure quality
- Hexbin map showing property density by region

### 💰 Tab 2: **Price Analysis**

- KPIs: average, median, minimum, and maximum prices
- Price histogram and boxplot
- Scatterplot of area vs. price
- Geographic clustering by price range (low, medium, high)

### 🚗 Tab 3: **Impact of Distances**

- KPIs comparing prices by proximity to ocean, highways, and airport noise
- Bar charts and boxplots categorizing these effects
- Scatterplots of distances vs. price

### 🌐 Tab 4: **Sales Time Analysis**

- Monthly evolution of sales prices
- Comparative KPIs with monthly variation percentage
- 3-month moving average trend analysis

### ⚙️ Filters

- Price range
- Area and age ranges
- Structure quality
- Distance to ocean, highway, and airport noise

---

## 🚧 Project Structure

```
.
├── api/                    # FastAPI - Data endpoints
│   ├── main.py             # Main API file
├── frontend/               # Streamlit app
│   ├── app.py              # Main entry point
│   ├── pages/
│   │   ├── aba1_map.py
│   │   ├── aba2_price.py
│   │   ├── aba3_distance.py
│   │   └── aba4_temporal.py
├── poetry.lock             # Dependencies lock file
├── pyproject.toml          # Project metadata and dependencies
├── README.md
```

---

## 🚫 Requirements

- Python 3.10+
- Free account on [Supabase](https://supabase.com/)

---

## 📚 How to Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/JoaoEscorcio/Streamlit_case.git
cd Streamlit_case
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies with Poetry

```bash
poetry install
```

### 4. Create the `.env` file

```env
SUPABASE_URL=https://<your-project>.supabase.co
SUPABASE_KEY=eyJhbGciOi...   # Your API Key
```

### 5. Run the API (FastAPI)

```bash
cd api
uvicorn main:app --reload --port 8000
```

### 6. Run the Frontend (Streamlit)

Open another terminal:

```bash
cd frontend
streamlit run app.py
```

---

## 🏙️ Deployment

### ✨ Suggested Platforms:

- **Render.com**: Ideal for running FastAPI (backend)
- **Streamlit Community Cloud**: Free frontend hosting

---

## 💼 Author

**João Victor Escorcio**\
Data Analyst | Python | Streamlit | BI | Real Estate Data\
[LinkedIn](https://www.linkedin.com/in/joaoescorcio/) • [Medium](https://medium.com/@jv.escorcio) • [jv.escorcio@gmail.com](mailto\:jv.escorcio@gmail.com)

---

## ✨ Future To-Do

- User authentication
- Report export functionality
- Price prediction using Machine Learning

---

Made with ❤️ by a data enthusiast!

