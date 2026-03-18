from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = 'django-insecure-=ao*nt*44o*l&ht+1za8iux$$*^y9as@5cz-x%8m8+(7^@+ydo'

def _env_bool(name, default):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}

_server_root = Path("/var/www/uninest")
_is_server = _server_root.exists()

DEBUG = _env_bool("DJANGO_DEBUG", not _is_server)

ALLOWED_HOSTS = ['18.171.169.58', 'uninest.website', 'www.uninest.website', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = [
    'http://18.171.169.58',
    'http://uninest.website',
    'http://www.uninest.website',
]

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get(
    'STATIC_ROOT',
    '/var/www/uninest/static' if _is_server else str(BASE_DIR / 'staticfiles'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get(
    'MEDIA_ROOT',
    '/var/www/uninest/media' if _is_server else str(BASE_DIR / 'media'),
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "properties",
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

ROOT_URLCONF = 'uninest.urls'

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

WSGI_APPLICATION = 'uninest.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'properties.User'
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = "/"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
