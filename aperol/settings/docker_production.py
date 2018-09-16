from aperol.settings.production import *
from aperol.settings.docker import *
import os

ALLOWED_HOSTS = ['*']

# Beanstalk does not pass the env. variables during "docker build" phase as the
# build command does not accept such arguments.
# (http://docs.docker.io/reference/commandline/cli/#build).
