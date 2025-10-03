@echo off
cd /d D:\projects\Blockhire\backend
call venv\Scripts\activate
python manage.py runserver
pause
