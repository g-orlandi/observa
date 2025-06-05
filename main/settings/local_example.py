from main.settings.settings import *

SECRET_KEY = '=v$r5+y8cu&+1c=1q*i9ix8fm0xyb9npj^_=so*#4gok^63xk3'

DEBUG = True

ALLOWED_HOSTS = ['*',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': PROJECT_INSTANCE,
        'USER': PROJECT_INSTANCE,
        'PASSWORD': 'w5vMG7EYz2oSd8B5H3GfULVTS',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

PROMETHEUS_URL = "http://prometheus.brainstorm.it/api/v1/query?query="
PROMETHEUS_RANGE_URL = "http://prometheus.brainstorm.it/api/v1/query_range?query="
PROMETHEUS_USER = 'USER'
PROMETHEUS_PWD = 'PASSWORD'