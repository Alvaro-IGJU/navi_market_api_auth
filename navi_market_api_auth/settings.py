
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dv(0abc3z@l=85tp8*6xmyofjqs00zp(j1os6ede(258z=m^gd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['18.184.173.4', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'users',
    'corsheaders',
    'companies',
    'events',
    'interactions',
    'gamification',
    'campaigns',
    'django_extensions',

]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # El token de acceso dura 7 días
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # El token de actualización dura 30 días
    'ROTATE_REFRESH_TOKENS': True,  # No se genera un nuevo refresh token al usarse
    'BLACKLIST_AFTER_ROTATION': True,  # Los refresh tokens usados se pueden invalidar
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ), 
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


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

CORS_ALLOWED_ORIGINS = [
    'http://navi-market-demo.s3-website.eu-central-1.amazonaws.com',
    'http://localhost:3000',
]

CORS_ALLOW_METHODS = [
	"GET",
	"POST",
	"PUT", 
	"DELETE",
	"OPTIONS",
]

CORS_ALLOW_HEADERS = [
	"Authorization",
	"Content-Type",
]

CORS_ALLOW_CREDENTIALS = True

DATA_UPLOAD_MAX_MEMORY_SIZE= 104857600
FILE_UPLOAD_MAX_MEMORY_SIZE= 104857600

ROOT_URLCONF = 'navi_market_api_auth.urls'

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

WSGI_APPLICATION = 'navi_market_api_auth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'navimarketdb',
        'USER': 'admin',
        'PASSWORD': 'pruebanavimarket',
        'HOST': 'navimarketdb.c1aqeyy8gohs.eu-central-1.rds.amazonaws.com',  # O la IP del servidor de la base de datos
        'PORT': '3306',
    }
}



AUTHENTICATION_BACKENDS = [
    'users.authentication.EmailOrUsernameModelBackend',  # Backend personalizado
    'django.contrib.auth.backends.ModelBackend',  # Backend por defecto
]

# Looking to send emails in production? Check out our Email API/SMTP product!
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.navi-market.com'  # Servidor saliente (SMTP)
EMAIL_PORT = 465  # Puerto para SMTP
EMAIL_USE_SSL = True  # Utilizar conexión SSL (no es TLS en este caso)
EMAIL_HOST_USER = 'no-reply@navi-market.com'  # Tu cuenta de correo
EMAIL_HOST_PASSWORD = 'F2cInI1LPUhc'  # Contraseña de tu cuenta
DEFAULT_FROM_EMAIL = 'Navi Market <navimarket.dev@navi-market.com>'  # Email "De"

AUTH_USER_MODEL = 'users.User'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

import os

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OPENAI_API_KEY = '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'
