from main.settings.settings import *

SECRET_KEY = '77777777777777777777777777777777777777777777777777'

# ALLOWED_HOSTS = ['*',]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'test_observa',
#         'USER': 'observa',
#         'PASSWORD': 'observa',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
        'NAME': ":memory:",
    }
}


print(DATABASES)

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "public", "test_media"))

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
