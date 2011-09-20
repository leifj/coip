# Django settings for coip project.

import coip.site_logging

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

BASE_DIR = "."
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%s/db/sqlite.db' % BASE_DIR,                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'us-en'

SITE_ID = 1

PREFIX_URL = 'http://localhost:8000'
NOREPLY = 'noreply@localhost'
METADATA = 'http://md.swamid.se/md/swamid-1.0.xml'

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

MEDIA_ROOT = "%s/site-media" % BASE_DIR
ADMIN_MEDIA_ROOT = "%s/admin-media" % BASE_DIR 
MEDIA_URL = '/site-media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!=ren*@$dklhfm$3#$h=a2g4r3)ra#+al)9kwi4&rpylr$3xnf'
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',         
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'coip.middleware.UserMappingMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware'
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'coip.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/templates" % BASE_DIR
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django_extensions',
    'tagging',
    'djcelery',
    'ghettoq',
    'djkombu',
    'tastypie',
    'oauth_provider',
    'coip.extensions',
    'coip.apps.name',
    'coip.apps.membership',
    'coip.apps.invitation',
    'coip.apps.userprofile',
    'coip.apps.link',
)

CARROT_BACKEND = "django"

import djcelery
djcelery.setup_loader()