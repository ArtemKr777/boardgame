"""
Django settings for blog project.
Optimized for Hugging Face Spaces deployment.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env (если есть)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# БЕЗОПАСНОСТЬ И НАСТРОЙКИ ХОСТИНГА
# =====================================================

# Секретный ключ (лучше хранить в переменных окружения на Hugging Face)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-key-for-hf-spaces-demo')

# Для демо-режима на HF Spaces включаем DEBUG
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Разрешаем все хосты для HF Spaces
ALLOWED_HOSTS = ['*', '.hf.space', 'localhost', '127.0.0.1']

# Доверенные источники для CSRF (обязательно для Hugging Face)
CSRF_TRUSTED_ORIGINS = [
    'https://*.hf.space',
    'http://*.hf.space',
]

# =====================================================
# ПРИЛОЖЕНИЯ (INSTALLED APPS)
# =====================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Для allauth

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Ваши приложения
    'entries.apps.EntriesConfig',
    'games',
    'users',
    'recommendations',
]

# =====================================================
# МИДЛВАРЫ (MIDDLEWARE)
# =====================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

# =====================================================
# ШАБЛОНЫ (TEMPLATES)
# =====================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'

# =====================================================
# БАЗА ДАННЫХ (SQLite — для простоты)
# =====================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =====================================================
# ВАЛИДАЦИЯ ПАРОЛЕЙ
# =====================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =====================================================
# ИНТЕРНАЦИОНАЛИЗАЦИЯ
# =====================================================

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# =====================================================
# СТАТИЧЕСКИЕ ФАЙЛЫ (STATIC FILES)
# =====================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# =====================================================
# АУТЕНТИФИКАЦИЯ И ПЕРЕНАПРАВЛЕНИЯ
# =====================================================

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'games'
LOGOUT_REDIRECT_URL = 'account_login'

# =====================================================
# DJANGO-ALLAUTH НАСТРОЙКИ (упрощены для HF)
# =====================================================

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# Для демо-режима — подтверждение почты можно отключить
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # или 'none'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_PRESERVE_USERNAME_CASING = False

# =====================================================
# НАСТРОЙКИ EMAIL (опционально — если понадобится)
# =====================================================

# Если не нужны письма — оставьте консольный бэкенд
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER