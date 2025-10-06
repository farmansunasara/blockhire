#!/bin/bash
echo "Starting BlockHire Backend in Virtual Environment..."
echo

# Activate virtual environment
source venv/bin/activate

# Run Django server
python manage.py runserver
