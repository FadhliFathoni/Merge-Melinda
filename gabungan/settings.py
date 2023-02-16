
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=fa3d@ps()hbfy1+9^f^o7=aq3o!&*p&--)x1#@ze0y1ri7@$k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'corsheaders',

    'Account',
    'API.Poin',
    'API.Mesin',
    'API.Minyak',
    'API.Produk',
    'API.Transaction',
    'API.ManagementUser',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://melinda-rosy.vercel.app',
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    'http://localhost:3000',
    'https://melinda-rosy.vercel.app'
]


ROOT_URLCONF = 'gabungan.urls'

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

WSGI_APPLICATION = 'gabungan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# MongoDb
DATABASES = {
    # 'default': {
    #     'ENGINE': 'djongo',
    #     'CLIENT': {
    #         'name': 'melinda',
    #         'host': 'mongodb://127.0.0.1:27017/melinda'
    #     }
    # }
    'default': {
        'ENGINE': 'djongo',
        'CLIENT': {
            'name': 'melinda',
            'host': 'mongodb://cobadulu:cobadulu@%2Fhome%2Ffourtour%2Fmongodb-0.sock/melinda?authSource=admin'
        }
    }
    # 'default': {
    #     'ENGINE': 'djongo',
    #     'NAME': 'melinda',
    #     'HOST': 'mongodb+srv://dazveloper:d4z-m0n9O4tL@cluster0.c76glns.mongodb.net/melinda?retryWrites=true&w=majority',
    #     'ENFORCE_SCHEMA': False
    # }
}

# SQL Lite
# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'melinda',
#         'HOST': 'mongodb+srv://dazveloper:d4z-m0n9O4tL@cluster0.c76glns.mongodb.net/melinda?retryWrites=true&w=majority',
#         'ENFORCE_SCHEMA': False
#     }
# }

# SQL Lite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'Account.User'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = "/home/Fadhli/Merge-Melinda/static"
# or, eg,
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
