#!/bin/sh
echo "Starting migrations..."
python manage.py migrate --noinput

echo "Running server..."
python manage.py runserver 0.0.0.0:8000