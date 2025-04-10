# 🌍 Dashboard do Mercado Imobiliário em Miami

Este projeto é um **dashboard interativo** desenvolvido com **Streamlit** e **FastAPI**, que consome dados imobiliários da cidade de Miami para fornecer **análises visuais e insights estratégicos** sobre preços de venda, localização, estrutura dos imóveis e influências externas como ruído e distâncias.

---

## 🚀 Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/) - Interface web interativa
- [FastAPI](https://fastapi.tiangolo.com/) - Backend para serviços de API
- [Supabase](https://supabase.com/) - Banco de dados e autenticação (PostgreSQL)
- [Plotly](https://plotly.com/python/) - Visualizações dinâmicas e profissionais
- [Pydeck](https://deckgl.readthedocs.io/en/latest/) - Visualização geográfica (mapas interativos)

---

## 🔍 Funcionalidades

### 📊 Aba 1: **Mapa Interativo**
- Visualização geográfica dos imóveis filtrados
- Scatterplot colorido por qualidade de estrutura
- Hexbin map mostrando densidade de imóveis por região

### 💰 Aba 2: **Análise de Preço**
- KPIs: preço médio, mediano, máximo e mínimo
- Histograma e boxplot dos preços
- Gráfico de dispersão entre área e preço
- Clusterização geográfica por faixa de preço (baixo, médio, alto)

### 🚗 Aba 3: **Impacto das Distâncias**
- KPIs comparando preços por proximidade ao oceano, rodovia e ruído aéreo
- Gráficos de barra e boxplot categorizando os efeitos
- Gráficos de dispersão entre distância e preço

### 🌐 Aba 4: **Análise Temporal**
- Evolução mensal dos preços de venda
- KPIs comparativos com variação percentual
- Média móvel de 3 meses para análise de tendência

### ⚙️ Filtros
- Faixa de preço
- Faixa de área e idade
- Qualidade da estrutura
- Distância ao oceano, rodovia e ruído

---

## 🚧 Estrutura do Projeto
```
.
├── api/                    # FastAPI - Endpoints de dados
│   ├── main.py             # Arquivo principal da API
├── frontend/               # Aplicativo Streamlit
│   ├── app.py              # Entrada principal da interface
│   ├── pages/
│   │   ├── aba1_mapa.py
│   │   ├── aba2_preco.py
│   │   ├── aba3_distancias.py
│   │   └── aba4_temporal.py
├── requirements.txt        # Dependências Python
├── README.md
```

---

## 🚫 Requisitos
- Python 3.10+
- Conta gratuita no [Supabase](https://supabase.com/)

---

## 📚 Como Rodar o Projeto Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/JoaoEscorcio/Streamlit_case.git
cd Streamlit_case
```

### 2. Crie um ambiente virtual e ative
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Crie o arquivo `.env`
```env
SUPABASE_URL=https://<seu-projeto>.supabase.co
SUPABASE_KEY=eyJhbGciOi...   # Chave da API
```

### 5. Rode a API (FastAPI)
```bash
cd api
uvicorn main:app --reload --port 8000
```

### 6. Rode o Frontend (Streamlit)
Abra outro terminal:
```bash
cd frontend
streamlit run app.py
```

---

## 🏙️ Deployment

### ✨ Opções sugeridas:
- **Render.com**: Ideal para rodar FastAPI (backend)
- **Streamlit Community Cloud**: Hospedagem gratuita do frontend

---

## 💼 Autor

**João Victor Escorcio**  
Data Analyst | Python | Streamlit | BI | Dados Imobiliários  
[LinkedIn](https://www.linkedin.com/in/joaoescorcio/) • [Medium](https://medium.com/@jv.escorcio) • jv.escorcio@gmail.com

---

## ✨ To-Do Futuro
- Autenticação de usuários
- Exportação de relatórios
- Previsão de preços com Machine Learning

---

Feito com ❤️ por um apaixonado por dados!

