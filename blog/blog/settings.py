"""
Django settings for blog project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url  # pip install dj-database-url

# Загружаем переменные из .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# БЕЗОПАСНОСТЬ (SECURITY)
# =====================================================

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-0*8(j=de31!m!(#vpz+b3o*hkw&6guer^ilc2*2e4))4_bgg&w')

# ВАЖНО: Для продакшена на Render
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '.onrender.com',  # разрешает любые поддомены render.com
    'localhost',
    '127.0.0.1',
    'kravart10.pythonanywhere.com',  # старый хостинг, если нужно
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://kravart10.pythonanywhere.com',
]

# Настройки безопасности для HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
    'django.contrib.sites',

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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ДЛЯ СТАТИКИ НА RENDER
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
# БАЗА ДАННЫХ (DATABASE) — ДЛЯ RENDER
# =====================================================

# Используем DATABASE_URL от Render или SQLite локально
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =====================================================
# АУТЕНТИФИКАЦИЯ И ПЕРЕНАПРАВЛЕНИЯ
# =====================================================

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'games'
LOGOUT_REDIRECT_URL = 'account_login'

# =====================================================
# DJANGO-ALLAUTH НАСТРОЙКИ
# =====================================================

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# =====================================================
# НАСТРОЙКИ EMAIL (GMAIL SMTP)
# =====================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'boardguru10@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Если вы отключили подтверждение почты на PythonAnywhere, здесь можно оставить 'optional'
# ACCOUNT_EMAIL_VERIFICATION = 'optional'