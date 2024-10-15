import os
from .settings import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "HOST": os.environ.get("PG_HOST"),
        "NAME": os.environ.get("PG_NAME"),
        "USER": os.environ.get("PG_USER"),
        "PASSWORD": os.environ.get("PG_PASSWORD"),
        'PORT': '5432',
    }
}
