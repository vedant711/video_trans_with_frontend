"""
Django settings for translation_tool project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# import rest_framework

import mimetypes
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/html", ".html", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import logging
# from . import settings

# class IPAddressFilter(logging.Filter):

#     def filter(self, record):
#         if hasattr(record, 'request'):
#             x_forwarded_for = record.request.META.get('HTTP_X_FORWARDED_FOR')
#             if x_forwarded_for:
#                 record.ip = x_forwarded_for.split(',')[0]
#             else:
#                 record.ip = record.request.META.get('REMOTE_ADDR')
#         return True

# print(ip)
# LOGGING = {
#     "version": 1,
#     "formatters": {
#         "request_formatter": {
#             "format": "%(asctime)s  - %(name)s - %(ip)s - %(levelname)s -  %(message)s",
#             "datefmt": "%Y-%m-%d %H:%M:%S"
#         },
#     },
#     "handlers": {
#         "request": {
#             "level": "INFO",
#             "class": "logging.FileHandler",
#             "formatter": "request_formatter",
#             "filename": "debug.log",
#             # "maxBytes": 1024000,
#             # "backupCount": 3
#         }
#     },
#     'filters': {
#         'add_ip_address': {
#             '()': 'trans.ip_catcher.IPAddressFilter' # You can move IPAddressFilter class from settings.py to another location (e.g., apps.other.filters.IPAddressFilter)
#         }
#     },
#     "loggers": {
#         'django.request': {
#             "level": "INFO",
#             'filters': ['add_ip_address'],
#              "handlers": ["request"]
#         },
#     },
#     "disable_existing_loggers": False
# }

# LOGGING = {
#     'version': 1,
#     # 'disable_existing_loggers': False,
#     "formatters": {
#         "request_formatter": {
#             "format": "%(asctime)s - %(message)s",
#             "datefmt": "%Y-%m-%d %H:%M:%S"
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'formatter':'request_formatter',
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#         'trans.views': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#         # 'apps': {
#         #     'handlers': ['file'],
#         #     'level': 'WARNING',
#         #     'propagate': True,
#         # },
#     },
# }

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+9h9ez7irsc+8d6cbxy%%9)&-2a*_e3x4rl0d!iaw6!tr@wpk_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trans',
    "rest_framework",
    "rest_framework_api_key",
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',
]

ROOT_URLCONF = 'translation_tool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'trans/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'translation_tool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
        'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'translator1',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST':'localhost',
        'PORT':'3306',
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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'trans/static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTO_LOGOUT = {'IDLE_TIME': 600}