"""
Django settings for sismoTT project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#from django.core.urlresolvers import reverse_lazy
#LOGIN_URL=reverse_lazy('login')
#LOGIN_REDIRECT_URL=reverse_lazy('login')
#LOGOUT_URL=reverse_lazy('logout')

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@431ww-9)7y8ymwx3&7!$=om851t17qm+6gqerznrp9inmb43m'

# SECURITY WARNING: don't run with debug turned on in production!

#DEBUG = True
DEBUG = False

#ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inicio',
    'WSsismoTT'
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'sismoTT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI_APPLICATION = 'sismoTT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
    # 'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'sismodb',
        # 'USER':'root',
        #'PASSWORD':'yourpassword',
        # 'HOST':'localhost'
    #}
#}
DATABASES = {
     'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME':'sismodb',
        'USER':'postgres',
        'PASSWORD':'diana369',
        'HOST':'localhost'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),"static_in_env","static_root")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_in_pro","our_static"),
    #'/var/www/static/',
]
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(os.path.dirname(BASE_DIR),"static_in_env","media_root")

LOGIN_REDIRECT_URL='/home'
LOGIN_URL='/login'

ALLOWED_HOSTS = ['*']

import dj_database_url

DATABASES=['default']=dj_database_url.config()

SECURE_PROXY_SSL_HEADER={'HTTP_X_FORWARDED_PROTO','https'}

try:
  from local_settings import *
except Exception as e:
  pass


