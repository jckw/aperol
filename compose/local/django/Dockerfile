FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'aperol.settings.docker_local'

RUN apt-get update
RUN apt-get -y install binutils libproj-dev gdal-bin

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code

RUN pip install -r requirements.txt

COPY ./compose/local/django/start /start
RUN chmod +x /start

ADD . /code/