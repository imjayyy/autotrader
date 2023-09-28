from pathlib import Path
import os
import sys
import dotenv
from celery.schedules import crontab

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../")
)
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "../autotrader_scraper/autotrader_scraper/",
    )
)
BASE_DIR = Path(__file__).resolve().parent.parent
# DEBUG = not bool(os.environ.get("PRODUCTION_SERVER", 0))
# if DEBUG:
#     dotenv.load_dotenv(os.path.join(BASE_DIR, "..", "app.default.env"))
# else:
#     dotenv.load_dotenv(os.path.join(BASE_DIR, "..", ".env.production"))

dotenv.load_dotenv(os.path.join(BASE_DIR, "..", "app.default.env"))


sys.path.append(os.path.join(BASE_DIR, "..", "autotrader_scraper"))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
os.environ[
    "ONLY_IMPORT_TASKS_FROM_CELERY"
] = "YES"  # this is to stop celery worker on setting up django (since we only need the worker file to import the tasks and not run the worker)

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", ["127.0.0.1"])
ALLOWED_HOSTS = ALLOWED_HOSTS.split(" ") if isinstance(ALLOWED_HOSTS, str) else ALLOWED_HOSTS

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    "car_details.apps.CarDetailsConfig",
    "search.apps.SearchConfig",
    "auction.apps.AuctionConfig",
    "myroot.apps.MyrootConfig",
    "rest_framework",
    "django_celery_beat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middlewares.language_middleware.language_middleware",
    "middlewares.admin_index_middleware.admin_index_middleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",

]

ROOT_URLCONF = "autotrader.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates/"],
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
WSGI_APPLICATION = "autotrader.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "mssql",
#         "NAME": os.getenv("DATABASE_NAME"),
#         "USER": os.getenv("DATABASE_USER"),
#         "PASSWORD": os.getenv("SA_PASSWORD"),
#         "HOST": os.getenv("DATABASE_HOST"),
#         "PORT": os.getenv("DATABASE_PORT"),
#         "OPTIONS": {"driver": "ODBC Driver 18 for SQL Server"},
#     },
# }


DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME":  "AutoTrader_Db",
        "USER": "SA",
        "PASSWORD":'Pakistan1',
        # 'HOST': '127.0.0.1',
        'HOST': 'localhost',
        "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 18 for SQL Server",
                    # "TrustServerCertificate":"yes"
                    'extra_params': "Encrypt=no"
                    },
    },
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

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

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "production-static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), os.path.join(BASE_DIR, "media")]

# LOGGING
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'gunicorn': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/log/django_errors.log',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['gunicorn'],
            'propagate': True,
        },
    }
}
"""
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

""" Celery Settings Start """

RABBITS_MQ_HOST = os.getenv('RABBITS_MQ_HOST', 'localhost')
RABBITS_MQ_PORT = os.getenv('RABBITS_MQ_PORT', '5672')

CELERY_BROKER_URL = f"amqp://guest:guest@{RABBITS_MQ_HOST}:{RABBITS_MQ_PORT}//"
CELERY_RESULT_BACKEND = f"rpc://guest:guest@{RABBITS_MQ_HOST}:{RABBITS_MQ_PORT}//"
CELERY_WORKER_CONCURRENCY = 8
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1
CRAWL_PAGES = 1
CELERY_BEAT_SCHEDULE = {
    "run_copart_spider_task": {
        "task": "celery_worker.scrape_auctions_task_copart",
        "schedule": crontab(minute=0, hour=1) #utc
    },
    "run_iaai_spider_task": {
        "task": "celery_worker.scrape_auctions_task",
        "schedule": crontab(minute=0, hour=0) #utc
    },
}

""" Celery Settings End """

RECAPTCHA_SECRET = "6LfCq9YgAAAAAKc9AdSnVVaX9gIY5wA62FVA4Vxi"
