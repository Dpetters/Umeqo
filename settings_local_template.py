import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Compress static content?
COMPRESS = False

# Students need an invite code to register
INVITE_ONLY = False

WELCOME_EVENT_ID = 6
UMEQO_RECRUITER_ID = 3

BACKUP_DIR = "backup"

# Base page is the landing page
USE_LANDING_PAGE = True

# Can students register?
REGISTRATION_OPEN = True

ROOT = os.path.dirname(os.path.realpath("__file__"))

# 1 - Prod, 2 - Staging, 3 - Dev/Local
SITE_ID = 3

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': ROOT + '/database.db', # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
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
            'maxBytes': 1024*1024*10,
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
            'handlers': ['file_handler'],
            'level': 'WARNING',
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}