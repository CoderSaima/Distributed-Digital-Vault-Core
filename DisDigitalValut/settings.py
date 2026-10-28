import os
from pathlib import Path
import environ

# 1. Path Definitions & Environment Initialization
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
# Read from the root directory .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 2. Critical Security Settings
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG', default=False)
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

# 3. Application Registry Matrix
INSTALLED_APPS = [
    'corsheaders',
    'Digital_app',
    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 4. Middleware Routing Pipelines
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DisDigitalValut.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DisDigitalValut.wsgi.application'

# 5. Database Connection Router Configuration
# Open your settings.py and change this configuration block:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'digital_legacy_db',       # Replace with your PostgreSQL Database Name
        'USER': 'postgres',                 # Replace with your PostgreSQL DB Username
        'PASSWORD': 'laptop123',     # Replace with your real DB user password
        'HOST': 'localhost',                # Keeps connection routed to your local server
        'PORT': '5432',                     # Standard default PostgreSQL port mapping
    }
}

DATABASES = {
    'default': env.db('DATABASE_URL')
}

# 6. Cryptographic Password Validation Controls
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 7. Localization & Timezone Rules
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 8. Static File Configurations
STATIC_URL = 'static/'

# 9. Asynchronous Distributed Mailer Layouts
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# 10. Cross-Origin Resource Sharing (CORS) Security Overrides
CORS_ALLOW_ALL_ORIGINS = True