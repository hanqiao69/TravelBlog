"""
Django settings for brandplug project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*fq&5g)av00h@vra***0xgzdn3$#^b9=i-60k-*^1ch0#=x7f$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = ('templates', 'accounts/templates')
ALLOWED_HOSTS = []
SITE_ID = 1

# Application definition
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "django.contrib.auth.context_processors.auth",
    "allauth.socialaccount.context_processors.socialaccount",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.sites',
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.instagram',
)
ROOT_URLCONF = 'brandplug.urls'
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
SOCIALACCOUNT_PROVIDERS = {
    'instagram': {'SCOPE': ['basic']}
}

WSGI_APPLICATION = 'brandplug.wsgi.application'
LOGIN_REDIRECT_URL = "/"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
# comment
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False
ADAPTER = 'accounts.adapter.CorporateAdapter'
ACCOUNT_ADAPTER = 'accounts.adapter.CorporateAdapter'
AUTH_USER_MODEL = 'accounts.CustomUser'
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
ACCOUNT_SIGNUP_FORM_CLASS = 'accounts.forms.SignupForm'
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_EMAIL_REQUIRED = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

from os import path

PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/'
import django
django.setup()

from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()
admin.site.register(User)
