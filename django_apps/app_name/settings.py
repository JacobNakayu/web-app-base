import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'vite_build'),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Application definition for migrations
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Steesh Apps
    "users.apps.UsersConfig",
    "owners.apps.OwnersConfig",
    "main.apps.MainConfig",
]

# Frameworks for processing requests as they go to and from the Views
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

WSGI_APPLICATION = "steesh.wsgi.application"

ROOT_URLCONF = "steesh.urls"

# Defines how to find, load, process, and use templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["/web-app-base"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Denver"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Variables that MUST be defined are intentionally left out of this file
#
try:
    from .local_settings import *  # noqa: F401, F403
except ModuleNotFoundError:
    raise ModuleNotFoundError("You need to create a local settings file!!!")

