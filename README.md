# bewise-part-2

Вторая часть тестового задания от компании Bewise

Проект реализован на Django и REST Framework

В нём реализовано три эндпоинта
- Создание пользователя
- Отправка файла с форматом .wav
- Возможность скачать файл .mp3, сконвертированный из файла .wav

Создание пользователя происходит через URL [127.0.0.1:8000/api/create-user/](http://127.0.0.1:8000/api/create-user/), отправляется json c данными

    {
      "username": string
    }

Возвращется ответ в виде

    {
        "id": 1,
        "username": "user",
        "access_token": "c44c3e2e-d248-4a11-aed2-ebc5e904ab03"
    }

Отправка файла с форматом .wav происходит через URL [127.0.0.1:8000/api/add-audio/](http://127.0.0.1:8000/api/add-audio/), отправляется multipart form data

![image](https://github.com/abushka/bewise-part-2/assets/65396568/8467ee8c-5b5d-4d1a-ac06-420d65e8a5ad)

Возвращается ответ в виде

    {
        "id": 1,
        "uuid": "46d17a12-6a39-495f-97ca-93b3dc550d25",
        "file": "/websdr_recording_2021-09-07T11_51_05Z_973.5kHz.mp3",
        "url": "http://127.0.0.1:8000/record?id=1&user=1"
    }

Скачать файл можно по полученным данным из прошлого запроса, а именно из полученного нами url [http://127.0.0.1:8000/record?id=1&user=1](http://127.0.0.1:8000/record?id=1&user=1)


# Dockerfile
Dockerfile в данном репозитории определяет контейнер для запуска веб-сервиса. Он устанавливает необходимые зависимости, копирует приложение внутрь контейнера и указывает команду для его запуска.

Определение базового образа

`FROM python:3.9-slim`

Устанавливаем переменную среды PYTHONUNBUFFERED в значение 1

`ENV PYTHONUNBUFFERED=1`

Создание рабочей директории /app

`WORKDIR /app`

Копирование файла requirements.txt  и .env

`COPY requirements.txt .env ./`

Установка зависимостей, указанных в файле requirements.txt

`RUN pip install --no-cache-dir -r requirements.txt`

Устанавливаем ffmpeg и PostgreSQL-клиент

`RUN apt-get update \
    && apt-get install -y ffmpeg \
    && apt-get install -y postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*`

Копирование приложения

`COPY . .`


# docker-compose.yml
docker-compose.yml в данном репозитории определяет сервисы web и db. Он указывает на сборку и настройку контейнера для веб-сервиса web, использование образа PostgreSQL для сервиса db, а также настройки портов и переменных окружения для каждого сервиса

Определение версии compose-файла: version: "3"

Определение сервисов:

`web:`
`db:`

Сборка контейнера для сервиса web из текущего каталога (где находится docker-compose.yml) с использованием Dockerfile.

`build:
      context: .
      dockerfile: Dockerfile`

Команда для запуска проекта

`command: python manage.py runserver 0.0.0.0:8000`

Пробрасывание порта 8080 на локальной машине на порт 8080 внутри контейнера. Это позволяет обращаться к веб-сервису через порт 8080 на хосте.

`ports: - 8080:8080`

Указание, что сервис web зависит от сервиса db и должен быть запущен после него.

`depends_on: - db`

Использование образа postgres для сервиса db. Это означает, что будет развернут контейнер с PostgreSQL.

`image: postgres`

Загрузка переменных окружения из файла .env.db.

`env_file: - ./.env.db`

Монтирование тома postgres_data для сохранения данных PostgreSQL. Данные будут храниться в каталоге /var/lib/postgresql/data внутри контейнера.

`volumes: - postgres_data:/var/lib/postgresql/data`

Пробрасывание порта 5432 на локальной машине на порт 5432 внутри контейнера. Это позволяет подключаться к базе данных PostgreSQL через порт 5432 на хосте.

`ports: - 5432:5432`

Создание именованного тома postgres_data, который будет использоваться для хранения данных PostgreSQL.

`volumes: postgres_data:`


# Запуск проекта
Для запуска проекта нужно переименовать `.env_example` и `.env.db_example`, в `.env` и `.env.db`, заполнив значения переменных, в .env.db указывается пользователь базы данных, пароль пользователя базы данных и имя базы данных, в .env заполняется полный путь к к базе данных

Запустить можно командой `docker compose up -d --build`
