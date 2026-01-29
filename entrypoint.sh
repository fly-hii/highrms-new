#!/bin/bash

set -e

echo "Waiting for database to be ready..."
# Wait for PostgreSQL to be ready
# Use a simple connection test
until python3 -c "import psycopg2; psycopg2.connect(host='db', database='horilla', user='postgres', password='postgres')" 2>/dev/null; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "Database is ready!"

echo "Running migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Creating superuser (if not exists)..."
python3 manage.py createhorillauser --first_name admin --last_name admin --username admin --password admin --email admin@example.com --phone 1234567890 || true

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 --access-logfile - --error-logfile - horilla.wsgi:application
