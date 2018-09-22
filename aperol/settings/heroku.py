from aperol.settings.production import *
import django_heroku

django_heroku.settings(locals(), staticfiles=False)
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
