import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ("Umeqo Team", "contact@umeqo.com"),
)
MANAGERS = ADMINS

# Compress static content?
COMPRESS = True

STRIPE_PUBLISHABLE = # find live publishable key in stripe account settings and fill in
STRIPE_SECRET = # find live secret key in stripe account settings and fill in

# Students need an invite code to register
INVITE_ONLY = False

# Base page is the landing page
USE_LANDING_PAGE = True

# Can students register?
REGISTRATION_OPEN = True

BACKUP_DIR = "/var/www/umeqo_backups/"

ROOT = os.path.dirname(os.path.realpath(__file__))

SITE_ID = # fill out
SITE_NAMES = {1:"Prod", 2:"Staging", 3:"Local", 4:"Demo"}
SITE_NAME = SITE_NAMES[SITE_ID]

# prod - http://127.0.0.1:8983/solr
# staging - http://127.0.0.1:8983/solr
# demo - http://127.0.0.1:8984/solr
HAYSTACK_SOLR_URL = # fill out

# prod - 4
# staging - 3
# demo - 3 
# TODO: change this to UMEQO_RECRUITER_USER_ID
UMEQO_RECRUITER_ID = # fill out

# prod - 1 
# staging - 6
# demo - 6
WELCOME_EVENT_ID = # fill out

# prod - Bl4ckVelv3t
# staging - Perf3ctP0ur
# demo - Perf3ctP0ur
DB_PASSWORD = # fill out

# prod - /var/www/static/
# staging - /var/www/static/
# demo - /var/www/demo_static/
STATIC_ROOT = # fill out

STATICFILES_DIRS = (
    ROOT + "/static/",
)

# prod - /prod/
# staging - /static/
# demo - /demo_static/
STATIC_URL = # fill out

COUNTRIES_FLAG_PATH = STATIC_URL + 'images/flags/%s.png'

CKEDITOR_MEDIA_PREFIX = STATIC_URL + "lib/ckeditor/"

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

# name
# prod - umeqo_main
# staging - umeqo_main
# demo - umeqo_demo_main
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': # fill out,                   # Or path to database file if using sqlite3.
        'USER': 'root', # Not used with sqlite3.
        'PASSWORD': DB_PASSWORD, # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'file_handler': {
            'level':'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ROOT + '/logs/umeqo.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter':'standard',
        },
        'mail_admins': {
            'level': 'WARNING',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html':True
        },
        'sentry': {
            'level': 'DEBUG',
            'class': 'sentry.client.handlers.SentryHandler',
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'django.request': { # Stop SQL debug from logging to main logger
            'handlers': ['sentry', 'file_handler'],
            'level': 'WARNING',
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'code': {
            'level':'DEBUG',
            'handlers': ['file_handler'],
        }
    }
}
