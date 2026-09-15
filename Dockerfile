FROM python:3.13-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Ставим Poetry официальным способом
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Копируем файлы зависимостей и устанавливаем их (включая dev)
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install

# Копируем весь проект
COPY . .

# По умолчанию запускаем Django, но в docker-compose переопределим для worker/beat
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
