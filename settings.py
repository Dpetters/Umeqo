"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

import os
ROOT = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

# By default, a session expires when the browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ACCOUNT_ACTIVATION_DAYS = 1 # One-day activation window;

# Haystack Settings
HAYSTACK_INCLUDE_SPELLING = True
HAYSTACK_DEFAULT_OPERATOR = 'AND'
HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'

# Email Settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@umeqo.com'
EMAIL_HOST_PASSWORD = 'californiapizzakitchen'
EMAIL_PORT = 587

#Akismet Settings
AKISMET_API_KEY = "39ec1788fc8e"

# URL to redirect the user to if they try to 
# access a page and aren't logged in
LOGIN_URL = '/'

# Emails sent to users will be coming from this email address
DEFAULT_FROM_EMAIL = 'umeqo@mit.edu'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ROOT + '/media/'

RESUME_BOOK_ROOT  = MEDIA_ROOT + "resume_books/"

SUBMITTED_RESUME_ROOT = MEDIA_ROOT + "submitted_resumes/"

# a list of folders inside of which of django looks for static files
STATICFILES_DIRS = (
    ROOT + '/static',
)

MAX_DIALOG_IMAGE_WIDTH = 200
MAX_DIALOG_IMAGE_HEIGHT = 140
    
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

COUNTRIES_FLAG_PATH = STATIC_URL + 'images/flags/%s.png'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=myl84m2+qr&d1&w^$(!ks0=6$6zlj4o438$c$_snv_45bpwow'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'notification.context_processors.notification'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'core.middleware.SetRemoteAddrMiddleware',
    'core.middleware.LogMiddleware'
)

AUTH_PROFILE_MODULE = "student.Student"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    ROOT + "/templates/"
)

SOUTH_MIGRATION_MODULES = {
    'messages': 'Umeqo.messages.migrations',
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'core',
    'employer',
    'events',
    'haystack',
    'messages',
    'countries',
    'notification',
    'registration',
    'south',
    'student',
    'debug_toolbar'
)


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

#only allow toolbar from localhost
#INTERNAL_IPS = ('127.0.0.1',)

try:
    from settings_local import *
except ImportError:
    from settings_prod import *

#this is used for absolute URLs, specifically FB API urls
DOMAIN = 'umeqo.com'
