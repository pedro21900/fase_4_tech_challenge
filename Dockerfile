FROM python:3.12-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libopenblas-dev \
    liblapack-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar todos os arquivos para o diretório de trabalho
COPY . /app

# Instalar as dependências do Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Definir o entrypoint do contêiner
ENTRYPOINT ["python3", "-m", "uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]