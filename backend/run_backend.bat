@echo off
echo Starting BlockHire Backend in Virtual Environment...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run Django server
python manage.py runserver

pause
