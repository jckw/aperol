from aperol.settings.local import *

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",
        "PORT": "5432",
    }
}
