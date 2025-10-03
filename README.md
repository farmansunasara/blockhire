# BlockHire - Document Verification System

A comprehensive document verification system built with Next.js frontend and Django backend, designed to provide secure, tamper-proof document verification using cryptographic hashing.

## 🚀 Project Overview

BlockHire is a document verification platform that enables secure verification of employment documents using SHA-256 cryptographic hashing. The system ensures document integrity by comparing provided document hashes with stored original hashes, making tampering easily detectable.

### Key Features

- **🔐 Secure Document Upload**: PDF documents are hashed using SHA-256 for integrity verification
- **👤 User Management**: Complete user registration, authentication, and profile management
- **📄 Document History**: Track all uploaded documents with original vs. additional document indicators
- **✅ Document Verification**: Public verification system for document authenticity
- **🏢 Issuer Dashboard**: HR/Company portal for employee authorization
- **📊 Profile Management**: Comprehensive user profile with document information
- **🔒 Immutable Records**: Original document hashes are immutable and used for verification

## 🏗️ Architecture

### Frontend (Next.js 14)
- **Framework**: Next.js 14 with App Router
- **UI Library**: shadcn/ui components
- **State Management**: React Context API
- **Form Handling**: React Hook Form with Zod validation
- **Styling**: Tailwind CSS
- **TypeScript**: Full type safety

### Backend (Django)
- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT tokens
- **File Handling**: Secure file upload with validation
- **API**: RESTful API with comprehensive endpoints

## 📁 Project Structure

```
BlockHire/
├── frontend/                 # Next.js frontend application
│   ├── app/                 # App Router pages
│   │   ├── login/          # Authentication pages
│   │   ├── profile/        # Profile management
│   │   │   ├── edit/       # Profile editing
│   │   │   └── info/       # Profile viewing
│   │   ├── issuer/         # Issuer dashboard
│   │   └── verify/         # Document verification
│   ├── components/         # Reusable UI components
│   │   ├── ui/            # shadcn/ui components
│   │   ├── Layout.tsx     # Main layout component
│   │   ├── ProfileDropdown.tsx
│   │   ├── DocumentHistory.tsx
│   │   ├── EmployeeLookup.tsx
│   │   └── CredentialsDisplay.tsx
│   ├── contexts/          # React contexts
│   │   └── AuthContext.tsx
│   ├── services/          # API service layer
│   │   └── api.ts
│   ├── types/             # TypeScript type definitions
│   │   └── api.ts
│   └── lib/               # Utility functions
│       ├── utils.ts
│       └── firebase.ts
├── backend/               # Django backend application
│   ├── blockhire/        # Django project settings
│   ├── accounts/         # User management app
│   ├── profiles/         # Profile management app
│   ├── documents/        # Document handling app
│   ├── issuer/           # Issuer functionality app
│   ├── verification/     # Document verification app
│   ├── manage.py
│   └── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Git

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Access the application**
   - Open [http://localhost:3000](http://localhost:3000) in your browser

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the API**
   - API available at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
   - Admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 🔧 Configuration

### Frontend Configuration

The frontend is configured to connect to the Django backend API. Update the API base URL in `frontend/services/api.ts` if needed:

```typescript
private baseURL = "http://127.0.0.1:8000/api"
```

### Backend Configuration

Key settings in `backend/blockhire/settings.py`:

- **Database**: SQLite for development, PostgreSQL for production
- **CORS**: Configured for frontend communication
- **JWT**: Token-based authentication
- **File Upload**: 10MB limit for PDF files

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Token refresh

### Profile Endpoints

- `GET /api/profile/` - Get user profile
- `PUT /api/profile/update/` - Update user profile
- `GET /api/profile/complete/` - Check profile completion

### Document Endpoints

- `POST /api/documents/upload/` - Upload document
- `GET /api/documents/history/` - Get document history
- `GET /api/documents/hashes/` - Get document hashes
- `GET /api/documents/download/<hash>/` - Download document

### Verification Endpoints

- `POST /api/verify/` - Verify document authenticity

### Issuer Endpoints

- `POST /api/issuer/authorize/` - Authorize employee
- `POST /api/issuer/employee-details/` - Get employee details
- `GET /api/issuer/authorized/` - List authorized employees

## 🔄 Document Workflow

### 1. User Registration
1. User registers with email and password
2. System generates unique Employee ID and User Hash
3. User profile created with immutable credentials

### 2. Document Upload
1. User uploads PDF document
2. System generates SHA-256 hash of document content
3. First document becomes "original" and sets `doc_hash`
4. Additional documents added to `doc_history` array
5. Document record stored in database

### 3. Document Verification
1. Verifier enters Employee ID and Document Hash
2. System finds user by Employee ID
3. Compares provided hash with stored `doc_hash`
4. Returns verification result (Valid/Invalid)

### 4. Issuer Authorization
1. Issuer enters Employee ID and User Hash
2. System verifies employee exists
3. Authorization record created
4. Employee becomes authorized for verification

## 🎯 Key Features

### Document Security
- **SHA-256 Hashing**: All documents are hashed using SHA-256
- **Immutable Records**: Original document hashes cannot be changed
- **Tamper Detection**: Any document modification results in different hash
- **History Tracking**: Complete document upload history maintained

### User Management
- **JWT Authentication**: Secure token-based authentication
- **Profile Management**: Comprehensive user profile system
- **Role-based Access**: Different access levels for users and issuers
- **Credential Display**: Immutable Employee ID and User Hash display

### Verification System
- **Public Verification**: Anyone can verify document authenticity
- **Real-time Results**: Instant verification results
- **Employee Details**: Verified employee information display
- **Audit Trail**: Complete verification request logging

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run test
```

### Backend Testing
```bash
cd backend
python manage.py test
```

### Integration Testing
```bash
cd backend
python test_complete_document_flow.py
```

## 🚀 Deployment

### Frontend Deployment (Vercel)
1. Connect your GitHub repository to Vercel
2. Configure environment variables
3. Deploy automatically on push to main branch

### Backend Deployment (Railway/Heroku)
1. Create new project on deployment platform
2. Connect GitHub repository
3. Configure environment variables
4. Deploy automatically

### Environment Variables

#### Frontend
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com/api
```

#### Backend
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **CORS Protection**: Configured for specific origins
- **File Validation**: PDF-only uploads with size limits
- **Hash Verification**: Cryptographic document integrity
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Built-in Django security features

## 📊 Performance

- **Frontend**: Optimized with Next.js 14 and App Router
- **Backend**: Efficient Django ORM queries
- **Database**: Indexed for optimal performance
- **File Handling**: Streamlined upload and storage
- **API Response**: Average response time < 500ms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@blockhire.com or create an issue in the GitHub repository.

## 🗺️ Roadmap

- [ ] Mobile app development
- [ ] Advanced document types support
- [ ] Blockchain integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] API rate limiting
- [ ] Document versioning
- [ ] Bulk verification

## 📞 Contact

- **Project Maintainer**: BlockHire Team
- **Email**: contact@blockhire.com
- **Website**: [https://blockhire.com](https://blockhire.com)
- **GitHub**: [https://github.com/blockhire/blockhire](https://github.com/blockhire/blockhire)

---

**Built with ❤️ by the BlockHire Team**

*Secure • Reliable • Efficient Document Verification*
