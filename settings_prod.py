import socket

DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS = False

def is_prod():
    return ['66.228.51.22'] == socket.gethostbyname_ex(socket.gethostname())[2]

# 1 - Prod, 2 - Staging, 3 - Dev/Local
if is_prod():
    SITE_ID = 1
    DB_PASSWORD = "H3rcul3s"
else:
    SITE_ID = 2
    DB_PASSWORD = "Jamb4Juic3"

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
        'PASSWORD': DB_PASSWORD,                # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
}