# Указываем базовый образ
FROM python:3.9-slim

# Устанавливаем переменную среды PYTHONUNBUFFERED в значение 1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы requirements.txt и .env в контейнер
COPY requirements.txt .env ./

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем ffmpeg и PostgreSQL-клиент
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && apt-get install -y postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем все файлы проекта в контейнер
COPY . .