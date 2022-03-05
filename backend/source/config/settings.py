import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DEBUG = True
env_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'infra'), '.env')
load_dotenv(env_path)
DEBUG = os.getenv("DEBUG", default="True")

# if DEBUG:
#     env_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'infra'), '.env')
#     load_dotenv(env_path)
# else:
#     load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    'rest_framework.authtoken',
    'djoser',
    'api',
    'authentication',
    'users',
    'recipes'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.postgresql"),
            "NAME": os.getenv("DB_NAME", default="default"),
            "USER": os.getenv("POSTGRES_USER", default="default"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="default"),
            "HOST": os.getenv("DB_HOST", default="default"),
            "PORT": os.getenv("DB_PORT", default="default")
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 1
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

DJOSER = {
    # 'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    # 'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    # 'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'LOGIN_FIELD': 'email',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
         'user_create': 'users.serializers.UserRegistrationSerializer'
    }
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
