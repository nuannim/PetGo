#!/bin/sh
set -e

# Wait for Postgres
if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for Postgres at $POSTGRES_HOST..."
  until nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}"; do
    sleep 1
  done
fi

python manage.py migrate --noinput || true
python manage.py collectstatic --noinput || true

exec gunicorn StarGo.wsgi:application --bind 0.0.0.0:8000 --workers 3