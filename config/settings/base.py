"""
Django settings for project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import environ

env = environ.Env()

_ = lambda s: s  # noqa

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Application definition
INSTALLED_APPS = [
    "admin_tools",
    "admin_tools.theming",
    "admin_tools.menu",
    "admin_tools.dashboard",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "ckeditor",
    "ckeditor_uploader",
    "mptt",
    "rest_framework",
    "cities_light",
    "apps.generic",
    "apps.users",
    "apps.memberships",
    "apps.geo",
    "apps.management",
    "apps.storage",
    "apps.mail",
    "apps.logs",
    "apps.selects",
    "apps.groups",
    "apps.clubs",
    "apps.events",
    "apps.chat",
    "apps.comments",
    "apps.media",
    "apps.notifications",
    "apps.posts",
    "apps.shops",
    "apps.news",
    "apps.games",
    "apps.mobile",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.users.middleware.ActiveUserMiddleware",
    "apps.logs.middleware.LogExceptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        # 'APP_DIRS': True,
        "OPTIONS": {
            "loaders": [
                "admin_tools.template_loaders.Loader",
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},  # noqa
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},  # noqa
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},  # noqa
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},  # noqa
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "ru"
LANGUAGES = (("ru", _("Russian")), ("en", _("English")))

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/server_static/"
STATIC_ROOT = os.path.join(BASE_DIR, "server_static")

MEDIA_URL = env.str("MEDIA_URL", default="/server_media/")
MEDIA_ROOT = os.path.join(BASE_DIR, "server_media")

DEFAULT_FILE_STORAGE = "apps.storage.storage.FileSystemStorage"

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o755

AUTH_USER_MODEL = "users.User"

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_BACKEND_RESULTS = env.str("CELERY_BACKEND_RESULTS")


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "basic": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
        ],
    }
}

ADMIN_TOOLS_MENU = "config.menu.CustomMenu"
ADMIN_TOOLS_INDEX_DASHBOARD = "config.dashboard.CustomIndexDashboard"
ADMIN_TOOLS_APP_INDEX_DASHBOARD = "config.dashboard.CustomAppIndexDashboard"


# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",  # noqa
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "PAGE_SIZE": 30,
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

EMAIL_BACKEND = "apps.mail.backends.SendgridDatabaseBackend"
DEFAULT_FROM_EMAIL = "team@vteme.life"
SENDGRID_API_KEY = env("SENDGRID_API_KEY", default=None)

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "vteme"}}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "database": {"level": "ERROR", "class": "apps.logs.log.DataBaseHandler"},
    },
    "loggers": {"django": {"handlers": ["console", "database"], "level": env.str("DJANGO_LOG_LEVEL")}},
}

# Number of seconds of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 300

# Number of seconds that we will keep track of inactive users for before
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7


SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", default=True)
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

CITIES_LIGHT_TRANSLATION_LANGUAGES = ["ru", "en"]
CITIES_LIGHT_INCLUDE_COUNTRIES = None
CITIES_LIGHT_INCLUDE_CITY_TYPES = [
    "PPL",
    "PPLA",
    "PPLA2",
    "PPLA3",
    "PPLA4",
    "PPLC",
    "PPLF",
    "PPLG",
    "PPLL",
    "PPLR",
    "PPLS",
    "STLMT",
]
