#!/bin/bash
set -e  # Exit on error

cd ./django_apps

# Collect static files
echo "Collect static files..."
python manage.py collectstatic --noinput || { echo 'Failed to collect static files'; exit 1; }

# Apply database migrations
echo "Apply database migrations..."
python manage.py makemigrations
python manage.py migrate || { echo 'Failed to apply migrations'; exit 1; }

# Start server
echo "Starting Gunicorn..."
exec gunicorn django_apps.app_name.wsgi:application --bind 0.0.0.0:8080 --workers 3
