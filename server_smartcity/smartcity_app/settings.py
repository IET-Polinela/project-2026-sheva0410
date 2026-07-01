"""
Django settings for smartcity_app project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-m4arej!@fg)#sz698%uayxdgl=9i9yn$9799+u0bia=4vx__ga'

DEBUG = True

ALLOWED_HOSTS = ['*']


# APPLICATION
INSTALLED_APPS = [
    'corsheaders',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplikasi project
    'main_app',
    'about',
    'contacts',
    'usermanagement_24782071',
    'dashboard_24782071',

    # Django REST Framework
    'rest_framework',
    'rest_framework_simplejwt',

    # OpenAPI Documentation
    'drf_spectacular',
    'django_scalar',
]


# CUSTOM USER MODEL
AUTH_USER_MODEL = 'usermanagement_24782071.User'


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'


# MIDDLEWARE
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


ROOT_URLCONF = 'smartcity_app.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / 'templates'],

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


WSGI_APPLICATION = 'smartcity_app.wsgi.application'


# DATABASE (POSTGRESQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_mhs05',
        'USER': 'user_mhs05',
        'PASSWORD': 'mhs05',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# DJANGO REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    # Schema generator untuk OpenAPI 3.0
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Renderer API
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    # Autentikasi JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# OPENAPI / SWAGGER / SCALAR SETTINGS
SPECTACULAR_SETTINGS = {
    'TITLE': 'Smart City Portal API',
    'DESCRIPTION': 'Dokumentasi REST API resmi untuk Portal Pelaporan Laporan Warga',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    # Membantu pemisahan request dan response schema
    'COMPONENT_SPLIT_REQUEST': True,

    # Konfigurasi Bearer Token agar tombol Authorize/gembok muncul di Swagger UI
    'SECURITY': [
        {
            'BearerAuth': []
        }
    ],

    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'BearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'Masukkan token dengan format: Bearer <access_token>',
            }
        }
    },

    # Agar token tidak hilang saat halaman Swagger direfresh
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
}


# CORS SETTINGS
CORS_ALLOW_ALL_ORIGINS = True


# CSRF SETTINGS
CSRF_TRUSTED_ORIGINS = [
    'http://103.151.63.87:8005',
    'https://iet-polinela.github.io',
]
