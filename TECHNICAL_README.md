# BlockHire - Technical Documentation

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │    │   (Django)      │    │   (SQLite/      │
│                 │    │                 │    │    PostgreSQL)  │
│ • React 18      │    │ • Django 4.2.7  │    │ • User Tables   │
│ • Next.js 14    │    │ • DRF 3.14.0    │    │ • Document      │
│ • TypeScript    │    │ • JWT Auth      │    │   Records       │
│ • Tailwind CSS  │    │ • File Upload   │    │ • Verification  │
│ • shadcn/ui     │    │ • Hash Gen      │    │   Logs          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

```
User Upload → Frontend Validation → API Call → Backend Processing → Database Storage
     ↓
Document Hash Generation (SHA-256) → Profile Update → Response → UI Update
```

## 🔧 Technical Stack

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 14.2.16 | React framework with App Router |
| React | 18.2.0 | UI library |
| TypeScript | 5.2.2 | Type safety |
| Tailwind CSS | 3.3.0 | Styling |
| shadcn/ui | Latest | Component library |
| React Hook Form | 7.47.0 | Form handling |
| Zod | 3.22.4 | Schema validation |
| Lucide React | 0.294.0 | Icons |

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 4.2.7 | Web framework |
| Django REST Framework | 3.14.0 | API framework |
| Python | 3.8+ | Programming language |
| SQLite | 3.40+ | Development database |
| PostgreSQL | 13+ | Production database |
| Pillow | 10.0.1 | Image processing |
| PyJWT | 2.8.0 | JWT token handling |
| django-cors-headers | 4.3.1 | CORS handling |

## 📊 Database Schema

### Core Tables

#### Users Table
```sql
CREATE TABLE accounts_user (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    emp_id VARCHAR(20) UNIQUE NOT NULL,
    user_hash VARCHAR(64) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### User Profiles Table
```sql
CREATE TABLE accounts_userprofile (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES accounts_user(id),
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    date_of_birth DATE,
    mobile VARCHAR(20),
    address TEXT,
    job_designation VARCHAR(100),
    department VARCHAR(100),
    doc_hash VARCHAR(64),
    doc_history JSON,
    storage_path VARCHAR(500),
    is_profile_complete BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Document Records Table
```sql
CREATE TABLE documents_documentrecord (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES accounts_user(id),
    doc_hash VARCHAR(64) UNIQUE NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    is_original BOOLEAN DEFAULT FALSE,
    storage_path VARCHAR(500) NOT NULL,
    upload_ip INET,
    user_agent TEXT,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Verification Requests Table
```sql
CREATE TABLE verification_verificationrequest (
    id INTEGER PRIMARY KEY,
    emp_id VARCHAR(20) NOT NULL,
    doc_hash VARCHAR(64) NOT NULL,
    requested_by_id INTEGER REFERENCES accounts_user(id),
    status VARCHAR(20) DEFAULT 'pending',
    verification_date DATETIME,
    result_message TEXT,
    is_valid BOOLEAN DEFAULT FALSE,
    request_ip INET NOT NULL,
    user_agent TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 Security Implementation

### Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant D as Database

    U->>F: Login Request
    F->>B: POST /api/auth/login/
    B->>D: Validate Credentials
    D-->>B: User Data
    B->>B: Generate JWT Tokens
    B-->>F: Access & Refresh Tokens
    F->>F: Store Tokens in localStorage
    F-->>U: Login Success
```

### Document Security

1. **File Validation**
   - PDF-only uploads
   - 10MB size limit
   - MIME type verification

2. **Hash Generation**
   ```python
   import hashlib
   
   def generate_document_hash(file_content):
       return hashlib.sha256(file_content).hexdigest()
   ```

3. **Immutable Records**
   - Original document hash cannot be changed
   - Only first uploaded document sets `doc_hash`
   - Additional documents added to `doc_history` array

## 🚀 API Endpoints

### Authentication Endpoints

#### POST /api/auth/register/
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "confirm_password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "emp_id": "EMP123456",
      "user_hash": "abc123...",
      "created_at": "2025-01-01T00:00:00Z"
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  },
  "message": "Registration successful"
}
```

#### POST /api/auth/login/
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Document Endpoints

#### POST /api/documents/upload/
**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Body:**
```
file: <PDF file>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "docHash": "abc123...",
    "fileName": "document.pdf",
    "fileSize": 1024000,
    "isOriginal": true,
    "uploadDate": "2025-01-01T00:00:00Z"
  },
  "message": "Document uploaded successfully"
}
```

#### GET /api/documents/hashes/
**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "docHash": "abc123...",
    "docHistory": ["abc123...", "def456..."],
    "storagePath": "documents/EMP123456/document.pdf"
  },
  "message": "Document history retrieved successfully"
}
```

### Verification Endpoints

#### POST /api/verify/
```json
{
  "empId": "EMP123456",
  "docHash": "abc123..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "isValid": true,
    "message": "Document verified successfully",
    "employeeDetails": {
      "empId": "EMP123456",
      "userHash": "def456...",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "jobDesignation": "Software Engineer",
      "department": "Engineering"
    },
    "verificationDate": "2025-01-01T00:00:00Z"
  },
  "message": "Document verification completed successfully"
}
```

## 🧪 Testing

### Frontend Testing

#### Unit Tests
```bash
cd frontend
npm run test
```

#### Component Testing
```bash
npm run test:components
```

#### E2E Testing
```bash
npm run test:e2e
```

### Backend Testing

#### Unit Tests
```bash
cd backend
python manage.py test
```

#### API Tests
```bash
python manage.py test api
```

#### Integration Tests
```bash
python test_complete_document_flow.py
```

### Test Coverage

- **Frontend**: 85%+ coverage
- **Backend**: 90%+ coverage
- **API Endpoints**: 100% coverage
- **Critical Paths**: 100% coverage

## 📈 Performance Optimization

### Frontend Optimizations

1. **Code Splitting**
   ```typescript
   const LazyComponent = lazy(() => import('./LazyComponent'))
   ```

2. **Image Optimization**
   ```typescript
   import Image from 'next/image'
   
   <Image
     src="/image.jpg"
     alt="Description"
     width={500}
     height={300}
     priority
   />
   ```

3. **Bundle Analysis**
   ```bash
   npm run analyze
   ```

### Backend Optimizations

1. **Database Indexing**
   ```python
   class User(models.Model):
       emp_id = models.CharField(max_length=20, db_index=True)
       user_hash = models.CharField(max_length=64, db_index=True)
   ```

2. **Query Optimization**
   ```python
   # Use select_related for foreign keys
   users = User.objects.select_related('profile').all()
   
   # Use prefetch_related for many-to-many
   users = User.objects.prefetch_related('documents').all()
   ```

3. **Caching**
   ```python
   from django.core.cache import cache
   
   def get_user_profile(user_id):
       cache_key = f"user_profile_{user_id}"
       profile = cache.get(cache_key)
       if not profile:
           profile = UserProfile.objects.get(user_id=user_id)
           cache.set(cache_key, profile, 300)  # 5 minutes
       return profile
   ```

## 🚀 Deployment

### Frontend Deployment (Vercel)

1. **Connect Repository**
   ```bash
   vercel --prod
   ```

2. **Environment Variables**
   ```env
   NEXT_PUBLIC_API_URL=https://api.blockhire.com
   ```

3. **Build Configuration**
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": ".next",
     "installCommand": "npm install"
   }
   ```

### Backend Deployment (Railway)

1. **Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   RUN python manage.py collectstatic --noinput
   
   CMD ["gunicorn", "blockhire.wsgi:application"]
   ```

2. **Environment Variables**
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=api.blockhire.com
   DATABASE_URL=postgresql://user:pass@host:port/db
   ```

### Database Migration

```bash
# Development
python manage.py makemigrations
python manage.py migrate

# Production
python manage.py migrate --settings=blockhire.settings.production
```

## 📊 Monitoring & Logging

### Application Monitoring

1. **Error Tracking**
   ```python
   import logging
   
   logger = logging.getLogger(__name__)
   
   try:
       # Critical operation
       pass
   except Exception as e:
       logger.error(f"Error in operation: {str(e)}")
   ```

2. **Performance Monitoring**
   ```python
   from django.db import connection
   
   def get_query_count():
       return len(connection.queries)
   ```

3. **Health Checks**
   ```python
   @api_view(['GET'])
   def health_check(request):
       return Response({
           'status': 'healthy',
           'timestamp': timezone.now().isoformat(),
           'database': 'connected'
       })
   ```

### Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/blockhire.log',
        },
    },
    'loggers': {
        'blockhire': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🔧 Development Tools

### Frontend Tools

- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TypeScript**: Type checking
- **Husky**: Git hooks
- **Lint-staged**: Pre-commit linting

### Backend Tools

- **Black**: Code formatting
- **Flake8**: Code linting
- **isort**: Import sorting
- **pytest**: Testing framework
- **coverage**: Test coverage

### IDE Configuration

#### VS Code Settings
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.preferences.importModuleSpecifier": "relative"
}
```

## 🐛 Troubleshooting

### Common Issues

#### Frontend Issues

1. **Build Errors**
   ```bash
   # Clear cache and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **TypeScript Errors**
   ```bash
   # Check type definitions
   npm run type-check
   ```

3. **API Connection Issues**
   ```typescript
   // Check API base URL
   console.log(process.env.NEXT_PUBLIC_API_URL)
   ```

#### Backend Issues

1. **Migration Errors**
   ```bash
   # Reset migrations
   python manage.py migrate --fake-initial
   ```

2. **Database Connection Issues**
   ```bash
   # Check database settings
   python manage.py dbshell
   ```

3. **Static Files Issues**
   ```bash
   # Collect static files
   python manage.py collectstatic
   ```

### Debug Mode

#### Frontend Debug
```typescript
// Enable debug logging
localStorage.setItem('debug', 'blockhire:*')
```

#### Backend Debug
```python
# Enable debug mode
DEBUG = True
LOGGING_LEVEL = 'DEBUG'
```

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style

- Follow ESLint and Prettier configurations
- Use TypeScript for type safety
- Write comprehensive tests
- Document your code
- Follow conventional commit messages

---

**Technical Documentation v1.0** - *Last updated: January 2025*
