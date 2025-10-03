# 🔐 BlockHire - Tamper-Proof Document Verification System

A blockchain-inspired employment verification platform that prevents resume fraud through cryptographic document verification.

## 🌟 Features

- **🔒 Tamper-Proof Documents**: SHA-256 cryptographic hashing ensures document integrity
- **⚡ Instant Verification**: Real-time document verification API
- **🌍 Global Access**: Web-based verification system accessible worldwide
- **🔐 Privacy-First**: Only hash comparison for verification, no personal data exposure
- **📱 Modern UI**: Responsive Next.js frontend with beautiful design
- **🛡️ Enterprise Security**: JWT authentication, CORS protection, security headers

## 🏗️ Architecture

### Backend (Django REST API)
- **Framework**: Django 4.2.7 + Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Custom JWT implementation
- **Security**: CORS, CSRF protection, security headers
- **File Storage**: Secure document storage with hash verification

### Frontend (Next.js)
- **Framework**: Next.js 14 with TypeScript
- **UI**: Tailwind CSS + Radix UI components
- **State Management**: React Context API
- **Authentication**: JWT token-based auth
- **Responsive**: Mobile-first design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL (for production)

### Local Development

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd blockhire
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api

## 🚀 Production Deployment

### Render Deployment
See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete deployment instructions.

**Quick Deploy:**
1. Connect GitHub repository to Render
2. Deploy backend with PostgreSQL database
3. Deploy frontend with environment variables
4. Configure CORS and security settings

## 📖 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Token refresh

### Document Endpoints
- `POST /api/documents/upload/` - Upload document
- `GET /api/documents/history/` - Document history
- `POST /api/verify/` - Verify document

### Profile Endpoints
- `GET /api/profile/` - Get user profile
- `PUT /api/profile/update/` - Update profile
- `POST /api/profile/complete/` - Complete profile

## 🔧 Configuration

### Environment Variables

**Backend:**
```env
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/db
CORS_ALLOWED_ORIGINS=https://your-frontend-url.com
JWT_SECRET_KEY=your-jwt-secret
```

**Frontend:**
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com/api
```

## 🛡️ Security Features

- **Cryptographic Hashing**: SHA-256 for document integrity
- **JWT Authentication**: Secure token-based auth
- **CORS Protection**: Configured for production
- **Security Headers**: XSS, CSRF, HSTS protection
- **Input Validation**: Comprehensive data validation
- **Rate Limiting**: API rate limiting (configurable)

## 📊 System Requirements

### Minimum Requirements
- **Backend**: 512MB RAM, 1 CPU core
- **Frontend**: 256MB RAM, 1 CPU core
- **Database**: PostgreSQL 12+

### Recommended for Production
- **Backend**: 1GB RAM, 2 CPU cores
- **Frontend**: 512MB RAM, 1 CPU core
- **Database**: PostgreSQL 14+ with connection pooling

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment help
- **Issues**: Create GitHub issue for bugs or feature requests
- **Security**: Report security issues privately

## 🎯 Project Goals

✅ **Prevent Resume Fraud** - Cryptographic verification system  
✅ **Instant Verification** - Real-time document validation  
✅ **Global Access** - Worldwide verification capability  
✅ **Privacy Protection** - Hash-only verification process  
✅ **Enterprise Ready** - Production-grade security and performance  

---

**BlockHire** - Making employment verification tamper-proof and instant! 🚀