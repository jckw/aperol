#!/bin/sh
echo "🛠 Starting migrations..."
python manage.py migrate --noinput
echo "🤙 Done migrating!"

# Heroku times out deployment here.. 
# Have to ssh into it to do this. It sucks! 
# echo "📸 Collecting static assets..."
# python manage.py collectstatic --noinput
# echo "🤙 Done collecting static assets!"

echo "Running server..."
# $PORT is set by Heroku
uwsgi --http 0.0.0.0:$PORT --protocol uwsgi --wsgi main:application --module aperol.wsgi --uid uwsgi