FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

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

<<<<<<< HEAD
CMD gunicorn sinistro_dash.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 120
=======
CMD alembic upgrade head  && uvicorn app.main:app --host 0.0.0.0 --port 8000
>>>>>>> 2b504402ba5465de0f88fce4f690411b46447329
