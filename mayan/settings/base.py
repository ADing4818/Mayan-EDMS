"""
Django settings for mayan10 project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from __future__ import unicode_literals

import os
import sys

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.literals import BOOTSTRAP_SETTING_LIST
from mayan.apps.smart_settings.utils import (
    get_environment_setting, get_environment_variables, read_configuration_file
)

from .literals import (
    CONFIGURATION_FILENAME, CONFIGURATION_LAST_GOOD_FILENAME,
    DEFAULT_SECRET_KEY, SECRET_KEY_FILENAME, SYSTEM_DIR
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

MEDIA_ROOT = get_environment_setting(
    name='MEDIA_ROOT', fallback_default=os.path.join(BASE_DIR, 'media')
)

# SECURITY WARNING: keep the secret key used in production secret!
environment_secret_key = os.environ.get('MAYAN_SECRET_KEY')
if environment_secret_key:
    SECRET_KEY = environment_secret_key
else:
    try:
        with open(os.path.join(MEDIA_ROOT, SYSTEM_DIR, SECRET_KEY_FILENAME)) as file_object:
            SECRET_KEY = file_object.read().strip()
    except IOError:
        SECRET_KEY = DEFAULT_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_environment_setting(name='DEBUG')

ALLOWED_HOSTS = get_environment_setting(name='ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = (
    # Placed at the top so it can override any template
    'mayan.apps.appearance',
    # Django
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    # Allow using WhiteNoise in development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # 3rd party
    'actstream',
    'colorful',
    'corsheaders',
    'django_celery_beat',
    'formtools',
    'mathfilters',
    'mptt',
    'pure_pagination',
    'rest_framework',
    'rest_framework.authtoken',
    'solo',
    'stronghold',
    'widget_tweaks',
    # Base apps
    'mayan.apps.acls',
    'mayan.apps.authentication',
    'mayan.apps.autoadmin',
    'mayan.apps.common',
    'mayan.apps.converter',
    'mayan.apps.dashboards',
    'mayan.apps.dependencies',
    'mayan.apps.django_gpg',
    'mayan.apps.dynamic_search',
    'mayan.apps.events',
    'mayan.apps.file_caching',
    'mayan.apps.lock_manager',
    'mayan.apps.mimetype',
    'mayan.apps.navigation',
    'mayan.apps.permissions',
    'mayan.apps.platform',
    'mayan.apps.rest_api',
    'mayan.apps.smart_settings',
    'mayan.apps.task_manager',
    'mayan.apps.user_management',
    # Project apps
    'mayan.apps.motd',
    # Document apps
    'mayan.apps.cabinets',
    'mayan.apps.checkouts',
    'mayan.apps.document_comments',
    'mayan.apps.document_indexing',
    'mayan.apps.document_parsing',
    'mayan.apps.document_signatures',
    'mayan.apps.document_states',
    'mayan.apps.documents',
    'mayan.apps.file_metadata',
    'mayan.apps.linking',
    'mayan.apps.mailer',
    'mayan.apps.mayan_statistics',
    'mayan.apps.metadata',
    'mayan.apps.mirroring',
    'mayan.apps.ocr',
    'mayan.apps.sources',
    'mayan.apps.storage',
    'mayan.apps.tags',
    'mayan.apps.web_links',
    # Placed after rest_api to allow template overriding
    'drf_yasg',
)

MIDDLEWARE = (
    'mayan.apps.common.middleware.error_logging.ErrorLoggingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'mayan.apps.common.middleware.timezone.TimezoneMiddleware',
    'stronghold.middleware.LoginRequiredMiddleware',
    'mayan.apps.common.middleware.ajax_redirect.AjaxRedirect',
)

ROOT_URLCONF = 'mayan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ]
        },
    },
]

WSGI_APPLICATION = 'mayan.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# ------------ Custom settings section ----------

LANGUAGES = (
    ('ar', _('Arabic')),
    ('bg', _('Bulgarian')),
    ('bs', _('Bosnian')),
    ('cs', _('Czech')),
    ('da', _('Danish')),
    ('de', _('German')),
    ('el', _('Greek')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fa', _('Persian')),
    ('fr', _('French')),
    ('hu', _('Hungarian')),
    ('id', _('Indonesian')),
    ('it', _('Italian')),
    ('lv', _('Latvian')),
    ('nl', _('Dutch')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('pt-br', _('Portuguese (Brazil)')),
    ('ro', _('Romanian')),
    ('ru', _('Russian')),
    ('sl', _('Slovenian')),
    ('tr', _('Turkish')),
    ('vi', _('Vietnamese')),
    ('zh', _('Chinese')),
)

SITE_ID = 1

STATIC_ROOT = os.environ.get(
    'MAYAN_STATIC_ROOT', os.path.join(MEDIA_ROOT, 'static')
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEST_RUNNER = 'mayan.apps.common.tests.runner.MayanTestRunner'

# --------- Django -------------------

LOGIN_URL = get_environment_setting(name='LOGIN_URL')
LOGIN_REDIRECT_URL = get_environment_setting(name='LOGIN_REDIRECT_URL')
LOGOUT_REDIRECT_URL = get_environment_setting(name='LOGOUT_REDIRECT_URL')
INTERNAL_IPS = get_environment_setting(name='INTERNAL_IPS')

# ---------- Django REST framework -----------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# --------- Pagination --------

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 5,
    'MARGIN_PAGES_DISPLAYED': 2,
}

# ----------- Celery ----------

CELERY_BROKER_URL = get_environment_setting(name='CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = get_environment_setting(name='CELERY_RESULT_BACKEND')
CELERY_TASK_ALWAYS_EAGER = get_environment_setting(
    name='CELERY_TASK_ALWAYS_EAGER'
)

CELERY_ACCEPT_CONTENT = ('json',)
CELERY_BEAT_SCHEDULE = {}
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ENABLE_UTC = True
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_CREATE_MISSING_QUEUES = False
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_QUEUES = []
CELERY_TASK_ROUTES = {}
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# ------------ CORS ------------

CORS_ORIGIN_ALLOW_ALL = True

# ------ Timezone --------

TIMEZONE_COOKIE_NAME = 'django_timezone'
TIMEZONE_SESSION_KEY = 'django_timezone'

# ----- Stronghold -------

STRONGHOLD_PUBLIC_URLS = (r'^/docs/.+$',)

# ----- Swagger --------

SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'rest_api.schemas.openapi_info',
    'DEFAULT_MODEL_DEPTH': 1,
    'DOC_EXPANSION': 'None',
}

# ----- AJAX REDIRECT -----

AJAX_REDIRECT_CODE = 278

# ----- Database -----
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MEDIA_ROOT, 'db.sqlite3'),
    }
}

BASE_INSTALLED_APPS = INSTALLED_APPS
COMMON_EXTRA_APPS = ()
COMMON_DISABLED_APPS = ()

CONFIGURATION_FILEPATH = get_environment_setting(
    name='CONFIGURATION_FILEPATH', fallback_default=os.path.join(
        MEDIA_ROOT, CONFIGURATION_FILENAME
    )
)

CONFIGURATION_LAST_GOOD_FILEPATH = get_environment_setting(
    name='CONFIGURATION_LAST_GOOD_FILEPATH', fallback_default=os.path.join(
        MEDIA_ROOT, CONFIGURATION_LAST_GOOD_FILENAME
    )
)

if 'revertsettings' not in sys.argv:
    configuration_result = read_configuration_file(CONFIGURATION_FILEPATH)
    environment_result = get_environment_variables()

    for setting in BOOTSTRAP_SETTING_LIST:
        if setting['name'] in configuration_result:
            globals().update({setting['name']: configuration_result[setting['name']]})
        elif setting['name'] in environment_result:
            globals().update({setting['name']: environment_result[setting['name']]})


for app in INSTALLED_APPS:
    if 'mayan.apps.{}'.format(app) in BASE_INSTALLED_APPS:
        raise ImproperlyConfigured(
            'Update the app references in the file config.yml as detailed '
            'in https://docs.mayan-edms.com/releases/3.2.html#backward-incompatible-changes'
        )


for APP in (COMMON_EXTRA_APPS or ()):
    INSTALLED_APPS = INSTALLED_APPS + (APP,)


INSTALLED_APPS = [
    APP for APP in INSTALLED_APPS if APP not in (COMMON_DISABLED_APPS or ())
]
