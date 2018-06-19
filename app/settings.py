import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'selectsomesecretkey'

DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'widget_tweaks',
    'huey.contrib.djhuey',
    'djangoformsetjs',

    'app',
    'accounts',
    'buildings',
    'place',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
VALIDATOR = 'django.contrib.auth.password_validation.{0}'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': VALIDATOR.format('UserAttributeSimilarityValidator'),
    },
    {
        'NAME': VALIDATOR.format('MinimumLengthValidator'),
    },
    {
        'NAME': VALIDATOR.format('CommonPasswordValidator'),
    },
    {
        'NAME': VALIDATOR.format('NumericPasswordValidator'),
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'auth_login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_URL = 'user_logout'
LOGOUT_REDIRECT_URL = 'home'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'level-and-date': {
            'format':
            '%(levelname)s\t%(asctime)s\t%(funcName)s\t%(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'level-and-date',
        },
    },
    'loggers': {
        'huey': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

EMAIL_SUBJECT = 'Copropiedad Integral - {0}'
BASE_URL = 'https://copropiedadintegral.com'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Local settings
settings_file = __import__('app.local_settings').local_settings
for setting_value in dir(settings_file):
    locals()[setting_value] = getattr(settings_file, setting_value)
