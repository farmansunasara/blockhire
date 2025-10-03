@echo off

REM BlockHire Backend Development Server Start Script

echo 🚀 Starting BlockHire Backend Development Server...

REM Activate virtual environment
call venv\Scripts\activate

REM Start development server
python manage.py runserver 0.0.0.0:8000

pause
