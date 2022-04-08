#!/bin/bash
set -e

python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear

gunicorn app.wsgi:application --bind 0.0.0.0:8000
