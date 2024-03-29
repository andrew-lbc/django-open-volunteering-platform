"""
Django settings for sandbox project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from ovp import get_core_apps

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#o2l1rv2g5$w7655n10fm68c8-+2lfd#h99nsmp(n5hro35cya'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [".localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
] + get_core_apps()

AUTH_USER_MODEL='users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'ovp.apps.channels.middlewares.channel.ChannelRecognizerMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'ovp.apps.channels.middlewares.channel.ChannelProcessorMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# Rest framework

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'PAGINATE_BY_PARAM': 'page_size',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'django.contrib.auth.backends.ModelBackend',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    )
}

# Email

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/email-messages'

EMAIL_HOST=os.environ.get('EMAIL_HOST', None)
EMAIL_PORT=os.environ.get('EMAIL_PORT', 465)
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD', None)
DEFAULT_FROM_EMAIL="{} <{}>".format(os.environ.get('EMAIL_FROM_NAME', 'default'), EMAIL_HOST_USER)

SSL=os.environ.get('EMAIL_USE_SSL', False)
if SSL:
  EMAIL_USE_SSL=True

# Haystack

HAYSTACK_CONNECTIONS={
'default': {
  'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
  'PATH': os.path.join('/tmp', 'whoosh_index'),
  },
}
HAYSTACK_SIGNAL_PROCESSOR='ovp.apps.search.signals.TiedModelRealtimeSignalProcessor'

# System checks

SILENCED_SYSTEM_CHECKS = ["auth.E003", "auth.W004"]

# Authentication backends

AUTHENTICATION_BACKENDS = [
    "ovp.apps.users.auth.oauth2.backends.facebook.FacebookOAuth2",
    "ovp.apps.users.auth.oauth2.backends.google.GoogleOAuth2",
    "rest_framework_social_oauth2.backends.DjangoOAuth2",
    "ovp.apps.users.auth.backends.ChannelBasedAuthentication"
]
