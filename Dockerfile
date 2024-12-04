# Usar uma imagem base oficial do Amazon Linux 2023
FROM public.ecr.aws/amazonlinux/amazonlinux:2023.6.20241121.0

# Atualizar o sistema e instalar dependências do sistema
RUN yum update -y && \
    yum install -y \
    python3 \
    python3-pip \
    gcc \
    gcc-c++ \
    make \
    openblas-devel \
    lapack-devel \
    yum-utils && \
    yum clean all

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos da API para o container
COPY . /app

# Instalar as dependências da API a partir do requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Expor a porta 80
EXPOSE 80

# Definir o entrypoint do contêiner
ENTRYPOINT ["python3", "-m", "uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "debug"]