"""
Django settings for safm_project project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Added
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'django_rest_passwordreset',
    'corsheaders',
    'django_extensions',
    'safm_api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

MIDDLEWARE = [
    # Added
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'safm.urls'

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

WSGI_APPLICATION = 'safm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = os.environ.get('MEDIA_URL', 'media/')
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)


# Default directory

DEFAULT_PROFILE_PICTURE = 'default/pictures/pp.png'


# Password reset

DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 2  # in hours
CLIENT_APP_URL = os.environ.get('CLIENT_APP_URL', 'localhost:3000')


# file upload limit settings in bytes :- (1<<20) is 1mb

WEBSERVER_FILE_UPLOAD_LIMIT = 50 * (1 << 20)

MAX_FILE_UPLOAD_SIZE = 10 * (1 << 20)
_max_file_size = os.environ.get('MAX_FILE_SIZE')
if _max_file_size:
    # always less than webserver's limit so an error
    # can be displayed through application server
    MAX_FILE_UPLOAD_SIZE = min(
        WEBSERVER_FILE_UPLOAD_LIMIT - (5 * (1 << 20)),
        int(_max_file_size)
    )


# audio file duration limit settings in seconds
MAX_AUDIO_DURATION = float(os.environ.get('MAX_AUDIO_DURATION', '30'))
