from aperol.settings.production import *
import django_heroku


django_heroku.settings(locals(), staticfiles=False)

# These are required by Heroku
GDAL_LIBRARY_PATH = os.environ.get(
    'GDAL_LIBRARY_PATH', '/app/.heroku/vendor/lib/libgdal.so')
GEOS_LIBRARY_PATH = os.environ.get(
    'GEOS_LIBRARY_PATH', '/app/.heroku/vendor/lib/libgeos_c.so')
