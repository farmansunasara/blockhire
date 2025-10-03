# BlockHire - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you get the BlockHire project running locally in just a few minutes.

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+
- **Git**

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/blockhire.git
cd blockhire
```

## Step 2: Start the Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver
```

✅ **Backend running at:** http://127.0.0.1:8000

## Step 3: Start the Frontend

Open a new terminal and run:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

✅ **Frontend running at:** http://localhost:3000

## Step 4: Test the Application

1. **Open your browser** and go to http://localhost:3000
2. **Register a new account** with your email
3. **Complete your profile** with personal information
4. **Upload a PDF document** to test document functionality
5. **Try document verification** using the verify page

## 🎯 Quick Test Flow

### 1. User Registration
- Go to http://localhost:3000/login
- Click "Create Account"
- Enter email and password
- Note your Employee ID and User Hash

### 2. Profile Setup
- Complete your profile information
- Upload a PDF document
- View your document hash

### 3. Document Verification
- Go to http://localhost:3000/verify
- Enter your Employee ID and Document Hash
- Verify the document authenticity

### 4. Issuer Dashboard
- Go to http://localhost:3000/issuer
- Authorize an employee using their credentials
- View employee details

## 🔧 Common Issues & Solutions

### Backend Issues

**Issue:** `ModuleNotFoundError: No module named 'django'`
```bash
# Solution: Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

**Issue:** `django.db.utils.OperationalError: no such table`
```bash
# Solution: Run migrations
python manage.py makemigrations
python manage.py migrate
```

**Issue:** `Port 8000 already in use`
```bash
# Solution: Use a different port
python manage.py runserver 8001
```

### Frontend Issues

**Issue:** `npm ERR! ENOENT: no such file or directory`
```bash
# Solution: Make sure you're in the frontend directory
cd frontend
npm install
```

**Issue:** `Port 3000 already in use`
```bash
# Solution: Use a different port
npm run dev -- -p 3001
```

**Issue:** `API connection failed`
```bash
# Solution: Check if backend is running
# Make sure backend is running on http://127.0.0.1:8000
```

## 📱 Available Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Landing page |
| Login | `/login` | User authentication |
| Profile | `/profile` | User profile overview |
| Edit Profile | `/profile/edit` | Profile editing |
| View Profile | `/profile/info` | Profile details |
| Issuer Dashboard | `/issuer` | HR/Company portal |
| Verify Document | `/verify` | Document verification |

## 🔑 Default Credentials

For testing purposes, you can create accounts with any email. The system will generate unique Employee IDs and User Hashes automatically.

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | User registration |
| `/api/auth/login/` | POST | User login |
| `/api/profile/` | GET | Get user profile |
| `/api/documents/upload/` | POST | Upload document |
| `/api/verify/` | POST | Verify document |
| `/api/issuer/authorize/` | POST | Authorize employee |

## 🧪 Test Data

### Sample User Registration
```json
{
  "email": "test@example.com",
  "password": "testpass123",
  "confirm_password": "testpass123"
}
```

### Sample Document Upload
- Upload any PDF file
- File size limit: 10MB
- Only PDF files are accepted

### Sample Verification
```json
{
  "empId": "EMP123456",
  "docHash": "abc123def456..."
}
```

## 🚀 Next Steps

1. **Explore the Codebase**
   - Check out the frontend components in `frontend/components/`
   - Review the backend models in `backend/*/models.py`
   - Look at the API views in `backend/*/views.py`

2. **Run Tests**
   ```bash
   # Backend tests
   cd backend
   python manage.py test
   
   # Frontend tests
   cd frontend
   npm run test
   ```

3. **Read Documentation**
   - [Main README](README.md)
   - [Technical Documentation](TECHNICAL_README.md)
   - [API Documentation](API_DOCS.md)

4. **Customize the Application**
   - Modify the UI components
   - Add new features
   - Update the database schema

## 🆘 Need Help?

- **Check the logs** in the terminal for error messages
- **Review the documentation** for detailed explanations
- **Create an issue** on GitHub if you encounter problems
- **Join our Discord** for community support

## 🎉 You're All Set!

You now have BlockHire running locally and can start developing or testing the application. Happy coding! 🚀

---

**Quick Start Guide v1.0** - *Last updated: January 2025*
