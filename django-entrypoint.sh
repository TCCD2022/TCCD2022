#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

echo "Make migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Load implemented methods in the database
echo "Update methods"
python manage.py loaddata datafiles/fixtures/models.json

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
