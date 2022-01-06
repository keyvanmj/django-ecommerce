import os
from os.path import dirname
from pathlib import Path
import django.core.mail.backends.filebased
from django.utils.translation import ugettext_lazy as _
import warnings





# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = os.path.join(BASE_DIR, 'static_content')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%d6&mubdg##mr3u6!2aor+=9qcsg$g3iapr%8#b0q=^4zgj@#&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    # my apps
    'accounts',
    'ecommerce',
    'ecommerce_category',
    'site_settings',
    'ecommerce_cart',
    'ecommerce_comment',
    'ecommerce_filter',
    'tag',
    'user_ip',
    'django_render_partial',
    'crispy_forms',
    'bootstrap4',
    'ecommerce_profile.apps.EcommerceProfileConfig',
    'sorl.thumbnail',
    'captcha',
    'ecommerce_favourite',
    'ecommerce_stats',
    'ecommerce_search',
    'ecommerce_manager',
]
SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_ip.middleware.SaveIPAddressMiddleware',
    'ecommerce_profile.middleware.ActiveUserMiddleware',
]

SESSION_COOKIE_NAME = 'cart_id'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 60*60*24*7*2
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_SECURE = False

ROOT_URLCONF = 'Django_ECommerce.urls'

PRODUCT_PER_ROW = 4

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(CONTENT_DIR), 'templates'
        ]
        ,
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Number of seconds of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 300

# Number of seconds that we will keep track of inactive user for before
# their last seen is removed from cache

USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7




WSGI_APPLICATION = 'Django_ECommerce.wsgi.application'
if __name__ == '__main__':
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(CONTENT_DIR, 'tmp/emails')
EMAIL_HOST_USER = 'Email'
DEFAULT_FROM_EMAIL = 'Email'
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_PASSWORD = '********'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, 'db.sqlite3')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
ENABLE_USER_ACTIVATION = True
DISABLE_USERNAME = False
LOGIN_VIA_EMAIL = True
LOGIN_VIA_EMAIL_OR_USERNAME = True
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'accounts:log_in'
USE_REMEMBER_ME = True

RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = True
ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE = True
SIGN_UP_FIELDS = ['username', 'email']
if DISABLE_USERNAME:
    SIGN_UP_FIELDS = ['email']

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(CONTENT_DIR, 'assets'),
]
STATIC_ROOT = os.path.join(CONTENT_DIR, 'static_root')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(CONTENT_DIR, 'media_root')
LOCALE_PATHS = [
    os.path.join(CONTENT_DIR, 'locale')
]
CRISPY_TEMPLATE_PACKS = 'bootstrap3'

SITE_NAME = 'E-Commerce'
META_KEYWORDS = 'transport,digital,accessories,courses'
META_DESCRIPTION = 'E-Commerce is a online shop of everything you want it'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


RECAPTCHA_PUBLIC_KEY = '6LeEd9gbAAAAABVTByznMwtac_57RI8AGSUFy_3G'
RECAPTCHA_PRIVATE_KEY = '6LeEd9gbAAAAAHWn8ExBlkCXhpLO3Zcucv1BiD8j'
