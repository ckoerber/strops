"""
Django settings for strops project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/

This file has been adjusted to espressodb settings.
"""
import os


from espressodb.management.utilities.files import get_project_settings
from espressodb.management.utilities.files import get_db_config
from espressodb.management.utilities.files import ESPRESSO_DB_ROOT

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
CONFIG_DIR = os.path.join(ROOT_DIR, "app")

_SETTINGS = get_project_settings(CONFIG_DIR)
SECRET_KEY = _SETTINGS.get("SECRET_KEY")
PROJECT_APPS = _SETTINGS.get("PROJECT_APPS", [])
ALLOWED_HOSTS = _SETTINGS.get("ALLOWED_HOSTS", [])
DEBUG = _SETTINGS.get("DEBUG", False)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = (
    PROJECT_APPS
    + [
        "espressodb.base",
        "espressodb.documentation",
        "espressodb.management",
        "espressodb.notifications",
    ]
    + ["bootstrap4", "widget_tweaks", "rest_framework",]
    + [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "strops.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(ESPRESSO_DB_ROOT, "espressodb", "base", "templates"),
            os.path.join(ESPRESSO_DB_ROOT, "espressodb", "documentation", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

for app in PROJECT_APPS[::-1]:
    _template_dir = os.path.join(ROOT_DIR, app.replace(".", os.sep), "templates")
    if os.path.exists(_template_dir):
        TEMPLATES[0]["DIRS"].insert(0, _template_dir)

WSGI_APPLICATION = "strops.config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DB_CONFIG = get_db_config(CONFIG_DIR)
DATABASES = {"default": DB_CONFIG}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, "strops", "static"),
    os.path.join(ESPRESSO_DB_ROOT, "espressodb", "base", "static"),
]
for app in PROJECT_APPS[::-1]:
    _static_dir = os.path.join(ROOT_DIR, app.replace(".", os.sep), "static")
    if os.path.exists(_static_dir):
        STATICFILES_DIRS.insert(0, _static_dir)


STATIC_ROOT = os.path.join(CONFIG_DIR, "static")
MEDIA_ROOT = os.path.join(CONFIG_DIR, "media")

LOGIN_REDIRECT_URL = "base:index"
LOGOUT_REDIRECT_URL = "base:index"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "%(asctime)s %(name)-8s %(levelname)-8s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "espressodb": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
        "strops": {"handlers": ["console"], "level": "INFO", "propagate": True},
    },
}


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}

PROJECT_NAME = "strops"

MIGRATION_MODULES = {"notifications": "strops.config.migrations.notifications"}

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
