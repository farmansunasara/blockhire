#!/bin/bash
# Production startup script for BlockHire

# Install dependencies
pip install -r requirements.txt

# Change to backend directory
cd backend

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@blockhire.com', 'BlockHire@2024')
    print('Superuser created')
else:
    print('Superuser already exists')
"

# Collect static files
python manage.py collectstatic --noinput

# Start the application with Gunicorn
exec gunicorn blockhire.wsgi:application --bind 0.0.0.0:$PORT --workers 3
