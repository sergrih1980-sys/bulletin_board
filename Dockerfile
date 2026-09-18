FROM python:3.13-slim

# 1. Создаём группу и пользователя (пока ещё от root)
RUN groupadd -g 1000 appgroup
RUN useradd -m -u 1000 -g appgroup appuser

WORKDIR /app

# 2. Назначаем права на папку (пока ещё от root)
RUN chown -R appuser:appgroup /app

# 3. Ставим системные зависимости (ОБЯЗАТЕЛЬНО от root!)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Переключаемся на обычного пользователя (только теперь!)
USER appuser

# Дальше идут команды Poetry, копирование файлов и т.д.
COPY --chown=appuser:appgroup pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY --chown=appuser:appgroup . .

EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
