#!/bin/bash

# Set the DJANGO_SETTINGS_MODULE to use settings_local
export DJANGO_SETTINGS_MODULE=app.settings_local

# Wait for PostgreSQL to be ready
./wait-for-postgres.sh &&

# Run migrations to create tables
python manage.py migrate &&

# Start the Django development server
python manage.py runserver 0.0.0.0:8081
