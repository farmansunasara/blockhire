@echo off

REM BlockHire Backend Setup Script for Windows

echo 🚀 Setting up BlockHire Backend...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Copy environment file
echo ⚙️ Setting up environment...
copy env.example .env

REM Create logs directory
echo 📁 Creating logs directory...
mkdir logs

REM Run migrations
echo 🗄️ Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo 👤 Creating superuser...
python manage.py create_superuser --email admin@blockhire.com --password admin123 --first-name Admin --last-name User

REM Generate demo data
echo 🎭 Generating demo data...
python manage.py generate_demo_data --users 5 --issuers 2

echo ✅ Setup complete!
echo.
echo To start the development server:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run server: python manage.py runserver
echo.
echo Admin panel: http://localhost:8000/admin/
echo API endpoints: http://localhost:8000/api/
