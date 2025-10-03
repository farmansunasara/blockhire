#!/bin/bash
# Production startup script for BlockHire backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the application with Gunicorn
exec gunicorn blockhire.wsgi:application --bind 0.0.0.0:$PORT --workers 3
