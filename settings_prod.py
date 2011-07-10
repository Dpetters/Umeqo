import socket

DEBUG = False
TEMPLATE_DEBUG = DEBUG

def is_prod():
    return ['66.228.51.22'] == socket.gethostbyname_ex(socket.gethostname())[2]

STATIC_ROOT = "/var/www/static/"

USE_LANDING_PAGE = is_prod()

# 1 - Prod, 2 - Staging, 3 - Dev/Local
if is_prod():
    SITE_ID = 1
else:
    SITE_ID = 2

ADMINS = (
    ("Dmitrij", "Dpetters91@gmail.com"),
    ("Zach", "zdearing@gmail.com"),
    ("Josh", "me@joshma.com"),
)
MANAGERS = ADMINS

STATIC_ROOT = "/var/www/static/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'umeqo_main',                   # Or path to database file if using sqlite3.
        'USER': 'root',                         # Not used with sqlite3.
        'PASSWORD': 'H3rcul3s',               # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
}