#!/bin/sh
set -e

python manage.py migrate --noinput || true
python manage.py collectstatic --noinput || true

exec gunicorn storage_microservice.wsgi:application --bind 0.0.0.0:8001 --workers 2