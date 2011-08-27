import os
ROOT = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

# By default, a session expires when the browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# The minimum password length that we allow
PASSWORD_MIN_LENGTH = 5
# How long do we allow dialogs to load for before showing "this is taking longer
# than usual..." message (in milliseconds)
LOAD_WAIT_TIME = 8000
# Students need an invite code to register
INVITE_ONLY = True
# Base page is the landing page
USE_LANDING_PAGE = True
# Can students register?
REGISTRATION_OPEN = True
# One-day activation window
ACCOUNT_ACTIVATION_DAYS = 1

# Max numbers of choices for each field on the student profile
SP_MAX_LANGUAGES = 12;
SP_MAX_CAMPUS_INVOLVEMENT = 12;
SP_MAX_INDUSTRIES_OF_INTEREST = 12;
SP_MAX_PREVIOUS_EMPLOYERS = 12;
SP_MAX_COUNTRIES_OF_CITIZENSHIP = 3;

# Max number of industries any one employer can claim to be in.
EP_MAX_INDUSTRIES = 5;

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

PROD_DATA_MODELS = {
    'campus_org': ['campusorg'],
    'employer':['employer'],
    'registration': ['interestedperson'],
    'core':['campusorgtype', 'location', 'topic', \
            'question', 'schoolyear', 'graduationyear', \
            'language', 'course','employmenttype', \
            'industry', 'eventtype'],
    'sites':['site']
}
LOCAL_DATA_MODELS = {
    'auth': ['user'],
    'student': ['student', 'studentpreferences', 'studentstatistics', 'studentinvite'],
    'registration':['userattributes', \
                    'sessionkey', 'registrationprofile'],
    'employer':['employerstatistics', 'recruiter', \
                'resumebook', 'studentfilteringparameters', \
                'employerstudentcomment', 'recruiterpreferences', \
                'recruiterstatistics'],
    'events':['event', 'rsvp', 'invitee', 'attendee']
}

PROD_PASSWORD = 'H3rcul3s'
STAGING_PASSWORD = 'Jamb4Juic3'

#Akismet Settings
AKISMET_API_KEY = "40daad1e6eb7"

#reCaptcha Settings
RECAPTCHA_PUBLIC_KEY = "6LeAXMcSAAAAAERV28inaaefrIPR29sUDUazGXxM"
RECAPTCHA_PRIVATE_KEY = "6LeAXMcSAAAAAFKWwcMK94XjO5Wvusu5FOQaYsS-"

# URL to redirect the user to if they try to 
# access a page and aren't logged in
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

# Emails sent to users will be coming from this email address
DEFAULT_FROM_EMAIL = 'no-reply@umeqo.com'

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

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [      'Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline',
            ],
            [      'HorizontalRule',
              '-', 'BulletedList', 'NumberedList',
            ]
        ],
        'width': 586,
        'resize_maxWidth' : 586,
        'resize_minWidth' : 586,
        'resize_minHeight' : 300,
        'height': 210,
        'skin':'kama',
        'toolbarCanCollapse': False,
    },
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ROOT + '/media/'

CKEDITOR_UPLOAD_PATH = "%sckeditor" % MEDIA_ROOT

LOCAL_FIXTURES_ROOT = ROOT + "/local_data/fixtures/"

LOCAL_MEDIA_ROOT = ROOT + "/local_data/media/"

PROD_MEDIA_ROOT = ROOT + "/prod_data/media/"

CKEDITOR_PATH = "ckeditor/"

# a list of folders inside of which of django looks for static files
STATICFILES_DIRS = (
    ROOT + '/static',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
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
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'notification.context_processors.notification',
    'core.context_processors.next',
    'core.context_processors.get_current_path',
    'core.context_processors.registration',
    'core.context_processors.load_wait_time'
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
    'messages': 'messages.migrations',
}

CKEDITOR_MEDIA_PREFIX = "/static/lib/ckeditor/"

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'core',
    'events',
    'student',
    'employer',
    'haystack',
    'messages',
    'countries',
    'notification',
    'registration',
    'south',
    'debug_toolbar',
    'compressor',
    'campus_org',
    'ckeditor'
)

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
        'file_handler': {
                'level':'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': ROOT + '/logs/umeqo.log',
                'maxBytes': 1024*1024*10,
                'backupCount': 5,
                'formatter':'standard',
        },
        'console':{
            'level':'ERROR',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': { # Stop SQL debug from logging to main logger
            'handlers': ['file_handler'],
            'level': 'DEBUG',
        },
        'django.request': { # Stop SQL debug from logging to main logger
            'handlers': ['file_handler'],
            'level': 'DEBUG',
            'propagate':True
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

#only allow toolbar from localhost
INTERNAL_IPS = ('127.0.0.1',)

NOTIFICATION_QUEUE_ALL = True

try:
    from settings_local import *
except ImportError:
    from settings_prod import *
