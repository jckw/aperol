FROM python:3.6

# Environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'aperol.settings.docker_production'

# Create non-su user
RUN groupadd -g 999 uwsgi && \
    useradd -r -u 999 -g uwsgi uwsgi 

RUN apt-get update
RUN apt-get -y install binutils libproj-dev gdal-bin

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code

RUN pip install -r requirements.txt

ADD . /code/

EXPOSE 5000

RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

USER uwsgi 

CMD [ "uwsgi", "--socket", "0.0.0.0:5000", \
               "--protocol", "uwsgi", \
               "--wsgi", "main:application", \
               "--module", "aperol.wsgi" ]
