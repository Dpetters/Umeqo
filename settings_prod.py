import socket
import os

# Compress static content?
COMPRESS = True

# Students need an invite code to register
INVITE_ONLY = False

# Base page is the landing page
USE_LANDING_PAGE = True

# Can students register?
REGISTRATION_OPEN = True

BACKUP_DIR = "/var/www/umeqo_backups/"

ROOT = os.path.dirname(os.path.realpath(__file__))

def is_prod():
    return ['66.228.51.22'] == socket.gethostbyname_ex(socket.gethostname())[2]

# 1 - Prod, 2 - Staging, 3 - Dev/Local
if is_prod():
    UMEQO_RECRUITER_ID = 4
    WELCOME_EVENT_ID = 1
    SITE_ID = 1
    DB_PASSWORD = "Bl4ckVelv3t"
    DEBUG = False
else:
    UMEQO_RECRUITER_ID = 3
    WELCOME_EVENT_ID = 6
    SITE_ID = 2
    DB_PASSWORD = "Perf3ctP0ur"
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ("Umeqo Team", "contact@umeqo.com"),
)
MANAGERS = ADMINS

STATIC_ROOT = "/var/www/static/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'umeqo_main',                   # Or path to database file if using sqlite3.
        'USER': 'root',                         # Not used with sqlite3.
        'PASSWORD': DB_PASSWORD,                # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
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
            'handlers': ['sentry', 'file_handler'],
            'level': 'WARNING',
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}