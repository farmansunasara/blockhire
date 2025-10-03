# BlockHire Backend

Django REST API backend for the BlockHire employment verification system.

## Features

- **User Authentication**: JWT-based authentication
- **Profile Management**: Complete user profile CRUD operations
- **Document Management**: PDF upload with SHA-256 hash generation
- **Verification System**: Document authenticity verification
- **Issuer Management**: Employee authorization and verification
- **File Storage**: AWS S3 integration for document storage
- **Rate Limiting**: API rate limiting for security
- **CORS Support**: Frontend integration ready

## Tech Stack

- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT tokens
- **File Storage**: AWS S3 / Local storage
- **Cache**: Redis
- **Task Queue**: Celery
- **Security**: CORS, Rate limiting, Input validation

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh JWT token

### Profile Management
- `GET /api/profile/` - Get user profile
- `PUT /api/profile/` - Update user profile
- `POST /api/profile/complete/` - Mark profile as complete

### Document Management
- `POST /api/documents/upload/` - Upload document
- `GET /api/documents/history/` - Get document history
- `GET /api/documents/download/{doc_hash}/` - Download document
- `DELETE /api/documents/{doc_hash}/` - Delete document

### Verification
- `POST /api/verify/` - Verify document authenticity
- `GET /api/verify/status/{emp_id}/` - Get verification status

### Issuer Operations
- `POST /api/issuer/authorize/` - Authorize employee
- `POST /api/issuer/employee-details/` - Get employee details
- `GET /api/issuer/authorized/` - Get authorized employees
- `DELETE /api/issuer/authorize/{emp_id}/` - Revoke authorization

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/blockhire

# Security
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=86400

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=blockhire-documents
AWS_S3_REGION_NAME=us-east-1

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Database Models

### User Model
- `user_hash` (Primary Key) - Immutable user identifier
- `emp_id` - Employee ID (immutable)
- `email` - Email address (immutable)
- `first_name`, `last_name` - Personal information
- `date_of_birth`, `mobile`, `address` - Contact details
- `job_designation`, `department` - Employment details
- `doc_hash` - Original document hash
- `is_profile_complete` - Profile completion status
- `created_at`, `updated_at` - Timestamps

### DocumentRecord Model
- `user` - Foreign key to User
- `doc_hash` - Document hash (unique)
- `upload_date` - Upload timestamp
- `file_name` - Original filename
- `file_size` - File size in bytes
- `is_original` - Whether this is the original document
- `storage_path` - Cloud storage path

### IssuerAuthorization Model
- `issuer_id` - Issuer identifier
- `emp_id` - Employee ID
- `user_hash` - User hash
- `permission_granted` - Authorization status
- `timestamp` - Authorization timestamp
- `issuer_name` - Issuer name

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- Rate limiting on API endpoints
- Input validation and sanitization
- File type validation for uploads
- SQL injection protection

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

### Database Migrations
```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate
```

## Production Deployment

1. Set `DEBUG=False`
2. Configure production database
3. Set up AWS S3 for file storage
4. Configure Redis for caching
5. Set up Celery for background tasks
6. Use Gunicorn as WSGI server
7. Configure Nginx as reverse proxy

## API Documentation

API documentation is available at `/api/docs/` when running the development server.

## License

This project is part of the BlockHire employment verification system.
