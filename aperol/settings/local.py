from aperol.settings.base import *

DEBUG = True

SECRET_KEY = "ds-^=q4i@z@mo4q#ve-k9u@u&)#!m14owx*^*45q0kr#jg9hr="

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ["jacks-macbook-pro.local", "localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "movemaison",
        "USER": "aperol",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}
