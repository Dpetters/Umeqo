import os, socket

DEBUG = False
TEMPLATE_DEBUG = DEBUG

def is_prod():
    return "66.228.51.22" == socket.gethostbyname_ex(socket.gethostname())[2]

USE_LANDING_PAGE = is_prod()

# The primary key of the site model.
# 2 is dev, 1 is prod
SITE_ID = 1

ROOT = os.path.dirname(os.path.realpath("__file__"))

ADMINS = (
    ("Dmitrij", "Dpetters91@gmail.com"),
    ("Zach", "zdearing@gmail.com"),
    ("Josh", "me@joshma.com")
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': ['standard']
        }
    },
    'loggers': {
        'django.request': { # Stop SQL debug from logging to main logger
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}