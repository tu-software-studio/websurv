from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3)

SECRET_KEY = 'ea+sg5filpj)308_9t2tzuoay6u=p1cdmqt!!s@=tfsunoybf$'

TEMPLATE_CONTEXT_PROCESSORS = (
        "websurv.context_processors.ProjectList",
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.contrib.messages.context_processors.messages",
        )

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
    'south',
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

LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('home')
