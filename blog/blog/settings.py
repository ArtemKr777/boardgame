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
<<<<<<< HEAD

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-0*8(j=de31!m!(#vpz+b3o*hkw&6guer^ilc2*2e4))4_bgg&w')
=======
>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7

# ВАЖНО: Для продакшена на Render
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

<<<<<<< HEAD
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

=======
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'kravart10.pythonanywhere.com',
    '127.0.0.1',
    'localhost',
]

>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7
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
<<<<<<< HEAD
    'django.contrib.sites',

    # allauth
=======
    'django.contrib.sites',  # Обязательно для allauth

    # allauth приложения
>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7
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
<<<<<<< HEAD
=======
    'users.middleware.SessionTrackingMiddleware',   # ← добавить эту строку
>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7
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
<<<<<<< HEAD
# БАЗА ДАННЫХ (DATABASE) — ДЛЯ RENDER
# =====================================================

# Используем DATABASE_URL от Render или SQLite локально
=======
# БАЗА ДАННЫХ (DATABASE)
# =====================================================

>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7
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
<<<<<<< HEAD
TIME_ZONE = 'Europe/Moscow'
=======

TIME_ZONE = 'Europe/Moscow'

>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7
USE_I18N = True
USE_TZ = True

# =====================================================
# СТАТИЧЕСКИЕ ФАЙЛЫ (STATIC FILES)
# =====================================================

STATIC_URL = '/static/'
<<<<<<< HEAD
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
=======
STATIC_ROOT = BASE_DIR / 'static'
>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7

# =====================================================
# АУТЕНТИФИКАЦИЯ И ПЕРЕНАПРАВЛЕНИЯ
# =====================================================

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'games'
<<<<<<< HEAD
LOGOUT_REDIRECT_URL = 'account_login'

# =====================================================
# DJANGO-ALLAUTH НАСТРОЙКИ
=======

# =====================================================
# НАСТРОЙКИ DJANGO-ALLAUTH
>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7
# =====================================================

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

<<<<<<< HEAD
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
=======
# Настройки входа и регистрации
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# Остальные настройки allauth
ACCOUNT_EMAIL_VERIFICATION = 'none'
>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
<<<<<<< HEAD
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# =====================================================
# НАСТРОЙКИ EMAIL (GMAIL SMTP)
=======
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# =====================================================
# НАСТРОЙКИ EMAIL (ПОЧТОВЫЙ СЕРВЕР PYTHONANYWHERE)
>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7
# =====================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.pythonanywhere.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
<<<<<<< HEAD
EMAIL_HOST_USER = 'boardguru10@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Если вы отключили подтверждение почты на PythonAnywhere, здесь можно оставить 'optional'
# ACCOUNT_EMAIL_VERIFICATION = 'optional'
=======
EMAIL_HOST_USER = 'KravArt10'  # ваш логин PythonAnywhere (KravArt10)
EMAIL_HOST_PASSWORD = 'bac10_01cab'  # пароль от PythonAnywhere
DEFAULT_FROM_EMAIL = 'KravArt10@pythonanywhere.com'

# =====================================================
# НАСТРОЙКИ БЕЗОПАСНОСТИ ДЛЯ PYTHONANYWHERE
# =====================================================

# Доверенные источники для CSRF (обязательно для HTTPS)
CSRF_TRUSTED_ORIGINS = [
    'https://kravart10.pythonanywhere.com',
    'http://kravart10.pythonanywhere.com',
]

# Настройки безопасности сессий и cookies
SESSION_COOKIE_SECURE = True      # Передавать cookies только по HTTPS
SESSION_COOKIE_HTTPONLY = True    # Защита от XSS
CSRF_COOKIE_SECURE = True         # CSRF токен только по HTTPS

# Настройка для работы за reverse-proxy (PythonAnywhere)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
>>>>>>> a1302b56bc1b4105deee8218cca67364ae1cd3f7
