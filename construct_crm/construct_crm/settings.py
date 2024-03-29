import json
import os
from pathlib import Path
from dotenv import load_dotenv

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = Path(__file__).resolve().parent.parent.parent
CONF_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(os.path.abspath(CONF_DIR / 'config' / '.env'))

try:
    with open(os.path.join(CONF_DIR, 'config', 'secret.json')) as handle:
        SECRETS = json.load(handle)
except IOError:  # потеря связи
    SECRETS = {
        'secret_key': 'a'
    }

PATH_LOG = Path(str(SECRETS['PATH_LOG']))

SECRET_KEY = SECRETS.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'crm',
    'drf_yasg',
    'rest_framework_api_key',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'construct_crm.urls'

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

WSGI_APPLICATION = 'construct_crm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': CONF_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'HOST': os.getenv('DB_HOST'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'PORT': os.getenv('DB_PORT'),
        'default-character-set': 'utf8',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = 'F:/Education/University/GitHub/Construct/construct/media/'
MEDIA_ROOT = os.path.join(MEDIA_DIR, 'construct', 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN_REDIRECT_URL = reverse_lazy('dashboard:home')
# LOGOUT_REDIRECT_URL = reverse_lazy('dashboard:home')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 1,
        }
    },
]

EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = SECRETS.get('user_host')
EMAIL_HOST_PASSWORD = SECRETS.get('user_host_password')
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
RECIPIENTS_EMAIL = SECRETS.get('recipients_email', [])
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# HasAPIKey CUSTOM HEADER
API_KEY_CUSTOM_HEADER = "HTTP_X_AUTHORIZATION"
