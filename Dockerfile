FROM python:3.13-slim
WORKDIR /app

# 1. Сначала создаём пользователя (до установки любых пакетов!)
RUN useradd -m -u 1000 -g 1000 appuser

# 2. Переключаемся на него
USER appuser

# 3. Ставим системные зависимости (нужны для сборки некоторых Python-пакетов)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Ставим Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/home/appuser/.local/bin:$PATH"

# 5. Копируем файлы зависимостей и ставим пакеты (теперь всё ставится от appuser)
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# 6. Копируем весь код проекта
COPY . .
