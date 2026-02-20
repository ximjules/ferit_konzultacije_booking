LOGOUT_REDIRECT_URL = '/'

from django.utils import timezone
from django.db import models
from django.conf import settings

from config.settings import BASE_DIR

INSTALLED_APPS = [
    # ...existing apps...
    'django.contrib.staticfiles',  # potrebno za development static serving
    'booking',  # osiguraj da je tu
    # 'accounts',  # odkomentiraj ako koristiš vlastitu accounts aplikaciju
]

# Osiguraj da TEMPLATES ima DIRS koji uključuje templates folder u rootu
TEMPLATES = [
    # ...existing config...
    {
        # ...existing settings...
        "DIRS": [BASE_DIR / "templates"],  # dodaj ako nije tamo
        # ...existing settings...
    },
]

# Statics (development)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # dodaj ako već nije
]

# ...existing code...