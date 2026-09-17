import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-key-change-me')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'ads',

    'rest_framework',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'drf_spectacular',
    'django_filters',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ===== DATABASE (Postgres) =====
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "bulletin_board"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
    #}
#}


# ===== AUTH =====
AUTH_USER_MODEL = 'users.User'

# ===== CORS =====
CORS_ALLOW_ALL_ORIGINS = True

# ===== DRF =====
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 4,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

# ===== JWT =====
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=int(os.environ.get('SIMPLE_JWT_ACCESS_TOKEN_LIFETIME_HOURS', 1))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'SIGNING_KEY': os.environ.get('SIMPLE_JWT_SIGNING_KEY', 'dev-secret-key'),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Bulletin Board API',
    'DESCRIPTION': 'API для сайта объявлений',
    'VERSION': '1.0.0',
}

# ===== Email (для восстановления пароля) =====
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Для прод: SMTP настройки через .env
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@bulletin.local')

REST_AUTH = {
    'TOKEN_MODEL': None,
}

# ===== URL =====
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ===== i18n =====
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===== Celery =====

CELERY_BROKER_URL = f'redis://{os.environ.get("REDIS_HOST", "localhost")}:6379/0'
CELERY_RESULT_BACKEND = f'redis://{os.environ.get("REDIS_HOST", "localhost")}:6379/0'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

PASSWORD_RESET_CONFIRM_URL = "password-reset-confirm/{uid}/{token}"
PASSWORD_RESET_URL = "reset-password/{uid}/{token}"


# Медиа-файлы (аватарки, изображения объявлений)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Статика (если ещё не настроена)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")