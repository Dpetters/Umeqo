import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

USE_LANDING_PAGE = True

# The primary key of the site model.
# 2 is dev, 1 is prod
SITE_ID = 1

ROOT = os.path.dirname(os.path.realpath("__file__"))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

LOCAL_SETTINGS_APPS = ('employer',
                       'student',
                       'events',
                       'registration',
                       'user',
                       )

ADMINS = (
    ("Dmitrij", "Dpetters91@gmail.com"),
    ("Zach", "zdearing@gmail.com"),
    ("Josh", "me@joshma.com")
    # Customer Support People
    # Customer Support Email Account
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'umeqo_main',                         # Or path to database file if using sqlite3.
        'USER': 'root',                         # Not used with sqlite3.
        'PASSWORD': 'Jamb4Juic3',                     # Not used with sqlite3.
        'HOST': '',                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                         # Set to empty string for default. Not used with sqlite3.
    }
}
