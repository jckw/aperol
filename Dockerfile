FROM python:3.6

# Environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE  'aperol.settings.heroku'

# Create non-su user
RUN groupadd -g 999 uwsgi && \
    useradd -r -u 999 -g uwsgi uwsgi 

RUN apt-get update
RUN apt-get -y install binutils libproj-dev gdal-bin libpq-dev python-dev libxml2-dev libxslt1-dev build-essential libssl-dev libffi-dev

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code

RUN pip install -r requirements.txt

ADD . /code/

# Heroku doesn't support EXPOSE
# EXPOSE 8000

RUN chmod +x /code/entrypoint.sh
CMD [ "/code/entrypoint.sh" ]