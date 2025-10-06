# BlockHire Backend Setup Guide

## Quick Start

### Option 1: Using Batch File (Windows)
```bash
# Double-click run_backend.bat or run from command line:
run_backend.bat
```

### Option 2: Using Shell Script (Linux/Mac)
```bash
# Make executable and run:
chmod +x run_backend.sh
./run_backend.sh
```

### Option 3: Manual Setup

#### 1. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2. Run Django Server
```bash
python manage.py runserver
```

## Environment Setup

### 1. Create Virtual Environment (if not exists)
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the backend directory with:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Start Server
```bash
python manage.py runserver
```

## Access Points

- **Backend API**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/

## Troubleshooting

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove and recreate virtual environment
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
python -m venv venv
```

### Database Issues
```bash
# Reset database
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows
python manage.py migrate
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

## Development Commands

```bash
# Check Django setup
python manage.py check

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Create new app
python manage.py startapp app_name
```

## File Structure
```
backend/
├── venv/                 # Virtual environment
├── blockhire/           # Django project
├── accounts/            # User management app
├── documents/           # Document handling app
├── verification/        # Document verification app
├── profiles/            # User profiles app
├── media/               # Media files (local storage)
├── db.sqlite3          # SQLite database
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── run_backend.bat    # Windows startup script
├── run_backend.sh     # Linux/Mac startup script
└── SETUP_GUIDE.md    # This file
```
