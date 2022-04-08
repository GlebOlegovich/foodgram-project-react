import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

WHICH_DB_FOR_DEBUG = 'sqlite3'
# WHICH_DB_FOR_DEBUG = 'postgresql'


if DEBUG:
    env_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'infra'), '.env')
    load_dotenv(env_path)
    DB_HOST = 'localhost'
else:
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST", default="localhost")


SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    'https://*', 'https://*localhost', 'https://*.127.0.0.1',
    'http://*', 'http://*localhost', 'http://*.127.0.0.1',
    'http://*gudleifr.ru', 'http://51.250.79.6',
]

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    '127.0.0.1:8000',
    'localhost:8000'
]

# if DEBUG:
STATIC_URL = '/static_backend/'
# else:
#     STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-backend')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media_backend/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media-backend')
# MEDIAILES_DIRS = [os.path.join(BASE_DIR, 'media')]

POSTGRESQL_DB = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME", default="default"),
        "USER": os.getenv("POSTGRES_USER", default="default"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="default"),
        "HOST": DB_HOST,
        "PORT": os.getenv("DB_PORT", default="default")
    }
}

if DEBUG:
    if WHICH_DB_FOR_DEBUG == 'sqlite3':
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        }
    elif WHICH_DB_FOR_DEBUG == 'postgresql':
        DATABASES = POSTGRESQL_DB
else:
    DATABASES = POSTGRESQL_DB

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'djoser',
    'debug_toolbar',

    'users',
    'recipes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            }
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Это по дефолту вроде бы итак стоит
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

DJOSER = {
    # 'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    # 'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    # 'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'LOGIN_FIELD': 'email',
    'SEND_ACTIVATION_EMAIL': False,
    # 'SERIALIZERS': {
    #      'user_create': 'users.serializers.UserRegistrationSerializer'
    # }
}

GLOBAL_SETTINGS = {
    "OUR_EMAIL": "from@example.com",
    "ROLE": (
        # то как в БД / То, как видят при выборе
        # ("moderator", "Модератор"),
        ("user", "Юзер"),
        ("admin", "Админ"),
    ),
    "admin": "admin",
    # "moderator": "moderator",
    "user": "user",
}
