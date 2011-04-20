"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

import os
#import inspect
#ROOT = inspect.currentframe().f_code.co_filename

ROOT = os.path.dirname(os.path.realpath(__file__))#.replace('\\','/')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ("Dmitrij", "dpetters@mit.edu"),
    # Customer Support People
    # Customer Support Email Account
)
MANAGERS = ADMINS

# By default, a session expires when the browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ACCOUNT_ACTIVATION_DAYS = 1 # One-day activation window;

# Haystack Settings
HAYSTACK_INCLUDE_SPELLING = True
HAYSTACK_DEFAULT_OPERATOR = 'OR'
HAYSTACK_SITECONF = 'urls'
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_XAPIAN_PATH = ROOT + '/xapian_index'

# Email Settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sbconnect.mit@gmail.com'
EMAIL_HOST_PASSWORD = 'californiapizzakitchen'
EMAIL_PORT = 587

#Akismet Settings
AKISMET_API_KEY = "39ec1788fc8e"

# URL to redirect the user to if they try to 
# access a page and aren't logged in
LOGIN_URL = '/'

# Emails sent to users will be coming from this email address
DEFAULT_FROM_EMAIL = 'sbconnect.mit@gmail.com'

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

# The primary key of the site model.
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ROOT + '/media/'

# a list of folders inside of which of django looks for static files
STATICFILES_DIRS = (
    ROOT + '/static',
)
    
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

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
    #'core.middleware.UserTypeMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTH_PROFILE_MODULE = "student.Student"

AUTHENTICATION_BACKENDS = (
    "core.backends.CustomModelBackend",
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    ROOT + "/templates/"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'core',
    'registration',
    'student',
    'employer',
    'events',
    'contact_form',
    'notification',
    'messages',
    'help',
    'haystack',
    'digg_paginator'
)

try:
    from local_settings import * #@UnusedWildImport
except ImportError:
    
    CACHE_BACKEND = 'memcached://unix:' + ROOT + 'memcached.sock'
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.',    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '',                         # Or path to database file if using sqlite3.
            'USER': '',                         # Not used with sqlite3.
            'PASSWORD': '',                     # Not used with sqlite3.
            'HOST': '',                         # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                         # Set to empty string for default. Not used with sqlite3.
        }
    }
    
    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
    MEDIA_URL = ''
    
    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"
    STATIC_ROOT = ''
    
    # URL prefix for admin static files -- CSS, JavaScript and images.
    # Make sure to use a trailing slash.
    # Examples: "http://foo.com/static/admin/", "/static/admin/".
    ADMIN_MEDIA_PREFIX = ''