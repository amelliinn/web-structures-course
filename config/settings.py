from pathlib import Path
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Если ключа нет в .env, возьмем запасной (но лучше, чтобы был)
SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
# os.getenv возвращает строку. Нам нужно превратить строку 'True' в булево True.
DEBUG = os.getenv('DEBUG') == 'True'

# Разрешенные хосты. В продакшене здесь будет имя сайта.
# Звездочка * разрешает всем (пока оставим так для простоты)
# Читаем из .env и преобразуем в список
ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', '').split(',') if host.strip()]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Наше приложение:
    'gallery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise для статики
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'  # Изменил на русский (было en-us)
TIME_ZONE = 'Europe/Moscow'  # Изменил на московское время (было UTC)
USE_I18N = True
USE_TZ = True


# ================== НАСТРОЙКИ СТАТИКИ И МЕДИА ==================

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# URL, по которому браузер ищет статику
STATIC_URL = 'static/'

# Папки, где мы (разработчики) храним статику
STATICFILES_DIRS = [
    BASE_DIR / 'gallery' / 'static',
]

# Папка, куда collectstatic соберет ВСЕ файлы для сервера
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Включаем сжатие и кэширование статики для WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA FILES (пользовательские загрузки)
# Базовый URL для доступа к медиафайлам через браузер
MEDIA_URL = '/media/'

# Абсолютный путь к папке на сервере, где будут храниться медиафайлы
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'