# Bulletin Board API

Доска объявлений с REST API на Django REST Framework. Проект включает авторизацию через JWT, CRUD для объявлений, фильтрацию, поиск и автоматическую документацию (Swagger).

## Стек технологий

- **Python 3.12+**
- **Django 5.0+**
- **Django REST Framework**
- **Simple JWT** (авторизация)
- **Django Filters** (фильтрация запросов)
- **DRF Spectacular** (автоматическая документация Swagger)
- **Poetry** (управление зависимостями и виртуальными окружениями)
- **SQLite** (база данных для разработки)

## Требования

- Python 3.12 или 3.13
- Poetry (`pip install poetry` или официальный установщик)
- Pillow (для работы с изображениями)

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <url-репозитория>
cd bulletin_board