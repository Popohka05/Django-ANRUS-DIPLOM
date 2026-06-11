import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in {'1', 'true', 'yes', 'on'}


def env_list(name, default):
    value = os.environ.get(name)
    if not value:
        return default
    return [item.strip() for item in value.split(',') if item.strip()]


SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-for-educational-project-only')
DEBUG = env_bool('DEBUG', default=not env_bool('AMVERA', default=False))
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', ['127.0.0.1', 'localhost', '.amvera.io'])
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS', ['https://*.amvera.io'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vocabulary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'english_vocab_trainer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'english_vocab_trainer.wsgi.application'

database_url = os.environ.get('DATABASE_URL')
if database_url:
    DATABASES = {
        'default': dj_database_url.config(default=database_url, conn_max_age=600),
    }
else:
    data_dir = Path(os.environ.get('DATA_DIR', '/data' if env_bool('AMVERA', default=False) else BASE_DIR))
    data_dir.mkdir(parents=True, exist_ok=True)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': data_dir / 'db.sqlite3',
        },
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    STORAGES['staticfiles'] = {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    }
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE', default=True)
    SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE', default=True)
