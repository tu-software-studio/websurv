from django.contrib import messages

from unipath import Path
PROJECT_DIR = Path(__file__).ancestor(3)

SECRET_KEY = 'ea+sg5filpj)308_9t2tzuoay6u=p1cdmqt!!s@=tfsunoybf$'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'backend',
    'thin',
    'bootstrapform',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'websurv.urls'
WSGI_APPLICATION = 'websurv.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

MESSAGE_TAGS = {
    messages.constants.ERROR: 'danger'    # Fix up for Bootstrap.
}
