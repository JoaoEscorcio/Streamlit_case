# Usando uma imagem base leve com Python
FROM python:3.11-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Instalando o Poetry globalmente
RUN pip install poetry

# Copiando os arquivos do projeto
COPY pyproject.toml poetry.lock* /app/
COPY api /app/api
COPY frontend /app/frontend
COPY .env /app/

# Instalando as dependências do projeto
RUN poetry install --no-root

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Comando para rodar Uvicorn e Streamlit juntos
CMD poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000 & poetry run streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0

