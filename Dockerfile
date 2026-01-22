FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libmariadb-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# deps python
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# copia código
COPY . .

# cria pasta uploads
RUN mkdir -p app/uploads/sinistros

EXPOSE 8000

CMD gunicorn sinistro_dash.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 120
