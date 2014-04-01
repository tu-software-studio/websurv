from .base import *

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR.child("db.sqlite3")
    }
}

INSTALLED_APPS += ('debug_toolbar', 'django_extensions')
