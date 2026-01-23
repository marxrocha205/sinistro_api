FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# deps do sistema (mysql + build)
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libmariadb-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# deps python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copia projeto
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
