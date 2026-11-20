import os
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-booknest-dev-key-change-in-production-xyz123456'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*'] if DEBUG else os.environ.get('ALLOWED_HOSTS', '.vercel.app,localhost,127.0.0.1').split(',')

# Origins allowed to POST forms (login, checkout, reviews) over HTTPS.
# Defaults to any Vercel subdomain so the demo works out of the box; narrow
# it to the exact domain in production, e.g. CSRF_TRUSTED_ORIGINS=https://booknest.vercel.app
CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://*.vercel.app').split(',') if o]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'crispy_forms',
    'crispy_bootstrap5',

    'core',
    'accounts',
    'books',
    'cart',
    'orders',
    'wishlist',
    'reviews',

    #Test App
    # 'django_seed',
    # 'autofixture',
    'mathfilters',
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
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'cart.context_processors.cart_counter',
                'wishlist.context_processors.wishlist_counter',
                'core.context_processors.site_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

if os.environ.get('DATABASE_URL'):
    # Production (Vercel): PostgreSQL, e.g. a free Neon database.
    # The URL may carry ?sslmode=require; pass it through to psycopg2.
    url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
    query = urllib.parse.parse_qs(url.query)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': url.path.lstrip('/'),
            'USER': urllib.parse.unquote(url.username or ''),
            'PASSWORD': urllib.parse.unquote(url.password or ''),
            'HOST': url.hostname,
            'PORT': url.port or '',
            'OPTIONS': {'sslmode': query.get('sslmode', ['prefer'])[0]},
            # Reuse connections on warm serverless instances instead of
            # opening a new one per request (slow against hosted Postgres).
            # Health checks drop connections the database has closed.
            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,
        }
    }
else:
    # Local development falls back to SQLite.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 6}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week

CART_SESSION_ID = 'cart'
WISHLIST_SESSION_ID = 'wishlist'

SHIPPING_COST = 5.99
FREE_SHIPPING_THRESHOLD = 50.00

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

# Behind Vercel's proxy, Django must trust X-Forwarded-Proto to know the
# request arrived over HTTPS (affects CSRF, sessions and absolute URLs).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
