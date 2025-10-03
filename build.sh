#!/bin/bash
# Build script for Render deployment

echo "Starting build process..."
pip install -r requirements.txt

echo "Dependencies installed, now collecting static files..."
cd backend

echo "Using build settings..."
DJANGO_SETTINGS_MODULE=blockhire.settings_build python manage.py collectstatic --noinput

echo "Build completed successfully!"
