import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-yh$rs9nxa+*7_c2$=(y#u-t5oc^@8)oc2te-mzxda^@sp2s0%0',
)
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    'ik-backend-780b39b1dc1f.herokuapp.com',
    'issyk-kul.vercel.app',
    'isykkol.kg',
    'localhost',
    '127.0.0.1',
]

extra_hosts = os.environ.get('ALLOWED_HOSTS', '')
if extra_hosts:
    ALLOWED_HOSTS.extend([host.strip() for host in extra_hosts.split(',') if host.strip()])

CSRF_TRUSTED_ORIGINS = [
    'https://ik-backend-780b39b1dc1f.herokuapp.com',
    'https://issyk-kul.vercel.app',
    'http://isykkol.kg',
    'https://www.isykkol.kg'
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://issyk-kul.vercel.app',
    'http://isykkol.kg',
    'https://www.isykkol.kg'
]

extra_cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if extra_cors_origins:
    CORS_ALLOWED_ORIGINS.extend(
        [origin.strip() for origin in extra_cors_origins.split(',') if origin.strip()]
    )

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'ckeditor',
    'news',
    'sights',
    'departments',
    'media',
]

BUCKETEER_AWS_ACCESS_KEY_ID = os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID')
BUCKETEER_AWS_SECRET_ACCESS_KEY = os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY')
BUCKETEER_AWS_REGION = os.environ.get('BUCKETEER_AWS_REGION')
BUCKETEER_BUCKET_NAME = os.environ.get('BUCKETEER_BUCKET_NAME')

USE_S3_MEDIA = all([
    BUCKETEER_AWS_ACCESS_KEY_ID,
    BUCKETEER_AWS_SECRET_ACCESS_KEY,
    BUCKETEER_AWS_REGION,
    BUCKETEER_BUCKET_NAME,
])

if USE_S3_MEDIA:
    INSTALLED_APPS.append('storages')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
elif DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    raise ImproperlyConfigured('DATABASE_URL is required when DEBUG=False')

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if USE_S3_MEDIA:
    AWS_ACCESS_KEY_ID = BUCKETEER_AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = BUCKETEER_AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = BUCKETEER_BUCKET_NAME
    AWS_S3_REGION_NAME = BUCKETEER_AWS_REGION
    # Bucketeer/S3 buckets often run with ACLs disabled (Object Ownership enforced).
    # Keep ACL unset and expose files via bucket policy instead.
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    AWS_LOCATION = 'public'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = (
        f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/'
        f'{AWS_LOCATION}/'
    )
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'mediafiles'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'backend.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
}
