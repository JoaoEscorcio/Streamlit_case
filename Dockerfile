# Usando uma imagem base leve com Python
FROM python:3.9-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Instalando o Poetry globalmente
RUN pip install poetry

# Copiando o arquivo de dependências do Poetry para dentro do container
COPY pyproject.toml poetry.lock* /app/

# Instalando as dependências do projeto
RUN poetry install --no-root

# Copiando o código fonte para dentro do container
COPY . /app

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Comando para rodar o script dentro do container
CMD ["poetry", "run", "python", "script.py"]
