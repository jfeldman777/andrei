import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from dotenv import load_dotenv

load_dotenv()
# ...

SECURE_PROXY_SSL_HEADER = None

# ...
IS_HEROKU = False
IS_HEROKU = os.getenv("IS_HEROKU")

if IS_HEROKU:
    try:
        import django_heroku
    except:
        pass




SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = ["andrei2.herokuapp.com", "andrei.herokuapp.com",
                 "pmlogicx.pro",
"pmlogix-7aab066f32c1.herokuapp.com",
"pmlogix-2023.herokuapp.com",
                 "127.0.0.1", "testserver", "localhost"]
#
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'locahost'  # SMTP server address
# EMAIL_PORT = 1025  # SMTP server port (usually 25 or 587)
# EMAIL_HOST_USER = 'your_email@example.com'  # SMTP server username
# EMAIL_HOST_PASSWORD = ''  # SMTP server password
# EMAIL_USE_TLS = False  # Use TLS encryption (optional)
# DEFAULT_FROM_EMAIL = 'your_email@example.com'  # Default sender email address

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jacob",
    "members",
    "bootstrap4",
    "jacob.templatetags",
    "crispy_forms",
    "crispy_bootstrap4",
    'import_export',
]
from .middleware import AllowFrameMiddleware

IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'delete'
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'delete'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "andrei2.middleware.AllowFrameMiddleware",
    # ...
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"
#
# CRISPY_TEMPLATE_PACK = 'uni_form'
ROOT_URLCONF = "andrei2.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates",
                 "templates/4",
                "templates/1"
                 ],
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

WSGI_APPLICATION = "andrei2.wsgi.application"

#
#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": BASE_DIR / "db.sqlite3",
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}


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

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


if IS_HEROKU:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = "ru"  #'en-us'
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]


import gettext

language_code = "ru"
gettext.bindtextdomain("django", "locale")
gettext.textdomain("django")


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if IS_HEROKU:
    try:
        import dj_database_url
        db_from_env = dj_database_url.config(conn_max_age=600)  #, ssl_require=True)
        DATABASES['default'].update(db_from_env)
    except:
        pass