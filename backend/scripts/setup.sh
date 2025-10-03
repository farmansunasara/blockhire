#!/bin/bash

# BlockHire Backend Setup Script

echo "🚀 Setting up BlockHire Backend..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
echo "⚙️ Setting up environment..."
cp env.example .env

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python manage.py create_superuser --email admin@blockhire.com --password admin123 --first-name Admin --last-name User

# Generate demo data
echo "🎭 Generating demo data..."
python manage.py generate_demo_data --users 5 --issuers 2

echo "✅ Setup complete!"
echo ""
echo "To start the development server:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run server: python manage.py runserver"
echo ""
echo "Admin panel: http://localhost:8000/admin/"
echo "API endpoints: http://localhost:8000/api/"
