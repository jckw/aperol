from aperol.settings.base import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['app.movemaison.com',
                 'movemaison.com', 'movemaison.elasticbeanstalk.com']
