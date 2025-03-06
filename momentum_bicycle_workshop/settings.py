import os
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()  # Load environment variables from .env

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "default-insecure-key")

DEBUG = False

ALLOWED_HOSTS = [
    "momentum-bicycle-workshop-22fb69372d3e.herokuapp.com",
    "localhost",
    "127.0.0.1",
    "raypt808-momentumbicycl-oy02jiub9mw.ws-eu117.gitpod.io",
    "8000-raypt808-momentumbicycl-oy02jiub9mw.ws-eu117.gitpod.io",
    "8000-raypt808-momentumbicycl-txfjkc4i0ss.ws-eu117.gitpod.io",
    "8000-raypt808-momentumbicycl-7y8dk9my9ip.ws-eu117.gitpod.io",
    "8000-raypt808-momentumbicycl-7y8dk9my9ip.ws-eu118.gitpod.io",
    "8000-raypt808-momentumbicycl-plilexjoq34.ws-eu118.gitpod.io",
    "8080-raypt808-momentumbicycl-plilexjoq34.ws-eu118.gitpod.io",
    "8000-raypt808-momentumbicycl-9m2enmotpf7.ws-eu118.gitpod.io",
    "8000-raypt808-momentumbicycl-ziz20zznbiv.ws-eu118.gitpod.io",
]


CSRF_TRUSTED_ORIGINS = [
    "https://momentum-bicycle-workshop-22fb69372d3e.herokuapp.com",
    "https://momentumbicycl-8ufp2aa6k6a.ws-eu117.gitpod.io",
    "https://8000-raypt808-momentumbicycl-oy02jiub9mw.ws-eu117.gitpod.io",
    "https://8000-raypt808-momentumbicycl-txfjkc4i0ss.ws-eu117.gitpod.io",
    "https://8000-raypt808-momentumbicycl-7y8dk9my9ip.ws-eu117.gitpod.io",
    "https://8000-raypt808-momentumbicycl-7y8dk9my9ip.ws-eu118.gitpod.io",
    "https://8000-raypt808-momentumbicycl-plilexjoq34.ws-eu118.gitpod.io",
    "https://8000-raypt808-momentumbicycl-9m2enmotpf7.ws-eu118.gitpod.io",
    "https://8000-raypt808-momentumbicycl-ziz20zznbiv.ws-eu118.gitpod.io",
]


LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "myapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "momentum_bicycle_workshop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "momentum_bicycle_workshop.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Media settings
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",  
}

X_FRAME_OPTIONS = "ALLOWALL"
