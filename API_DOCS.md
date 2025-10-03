# BlockHire API Documentation

## 🔗 Base URL

```
Development: http://127.0.0.1:8000/api
Production: https://api.blockhire.com/api
```

## 🔐 Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

## 📚 API Endpoints

### Authentication

#### Register User
```http
POST /auth/register/
```

**Request Body:**
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
      "user_hash": "a1b2c3d4e5f6...",
      "first_name": "",
      "last_name": "",
      "is_active": true,
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  },
  "message": "Registration successful"
}
```

**Status Codes:**
- `201` - Created successfully
- `400` - Validation error
- `409` - User already exists

#### Login User
```http
POST /auth/login/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
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
      "user_hash": "a1b2c3d4e5f6...",
      "first_name": "John",
      "last_name": "Doe",
      "is_active": true,
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  },
  "message": "Login successful"
}
```

**Status Codes:**
- `200` - Login successful
- `400` - Invalid credentials
- `401` - Authentication failed

#### Logout User
```http
POST /auth/logout/
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

#### Refresh Token
```http
POST /auth/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "message": "Token refreshed successfully"
}
```

### Profile Management

#### Get User Profile
```http
GET /profile/
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "userHash": "a1b2c3d4e5f6...",
    "empId": "EMP123456",
    "firstName": "John",
    "lastName": "Doe",
    "fullName": "John Doe",
    "dateOfBirth": "1990-01-01",
    "mobile": "+1234567890",
    "address": "123 Main St, City, State",
    "jobDesignation": "Software Engineer",
    "department": "Engineering",
    "docHash": "b2c3d4e5f6g7...",
    "docHistory": ["b2c3d4e5f6g7...", "c3d4e5f6g7h8..."],
    "storagePath": "documents/EMP123456/document.pdf",
    "isProfileComplete": true,
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:00:00Z"
  },
  "message": "Profile retrieved successfully"
}
```

#### Update User Profile
```http
PUT /profile/update/
```

**Headers:**
```
Authorization: Bearer <access-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "dateOfBirth": "1990-01-01",
  "mobile": "+1234567890",
  "address": "123 Main St, City, State",
  "jobDesignation": "Software Engineer",
  "department": "Engineering"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "userHash": "a1b2c3d4e5f6...",
    "empId": "EMP123456",
    "firstName": "John",
    "lastName": "Doe",
    "fullName": "John Doe",
    "dateOfBirth": "1990-01-01",
    "mobile": "+1234567890",
    "address": "123 Main St, City, State",
    "jobDesignation": "Software Engineer",
    "department": "Engineering",
    "docHash": "b2c3d4e5f6g7...",
    "docHistory": ["b2c3d4e5f6g7..."],
    "storagePath": "documents/EMP123456/document.pdf",
    "isProfileComplete": true,
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:00:00Z"
  },
  "message": "Profile updated successfully"
}
```

### Document Management

#### Upload Document
```http
POST /documents/upload/
```

**Headers:**
```
Authorization: Bearer <access-token>
Content-Type: multipart/form-data
```

**Request Body:**
```
file: <PDF file>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "docHash": "b2c3d4e5f6g7...",
    "uploadDate": "2025-01-01T00:00:00Z",
    "fileName": "document.pdf",
    "fileSize": 1024000,
    "fileSizeMb": 1.0,
    "isOriginal": true,
    "storagePath": "documents/EMP123456/document.pdf",
    "fileType": "pdf",
    "downloadUrl": "/api/documents/download/b2c3d4e5f6g7.../",
    "userName": "John Doe"
  },
  "message": "Document uploaded successfully"
}
```

**Status Codes:**
- `201` - Upload successful
- `400` - Validation error
- `413` - File too large
- `415` - Unsupported file type

#### Get Document History
```http
GET /documents/history/
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "docHash": "b2c3d4e5f6g7...",
      "uploadDate": "2025-01-01T00:00:00Z",
      "fileName": "document.pdf",
      "fileSize": 1024000,
      "fileSizeMb": 1.0,
      "isOriginal": true,
      "storagePath": "documents/EMP123456/document.pdf",
      "fileType": "pdf",
      "downloadUrl": "/api/documents/download/b2c3d4e5f6g7.../",
      "userName": "John Doe"
    }
  ],
  "message": "Document history retrieved successfully"
}
```

#### Get Document Hashes
```http
GET /documents/hashes/
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "docHash": "b2c3d4e5f6g7...",
    "docHistory": ["b2c3d4e5f6g7...", "c3d4e5f6g7h8..."],
    "storagePath": "documents/EMP123456/document.pdf"
  },
  "message": "Document history retrieved successfully"
}
```

#### Download Document
```http
GET /documents/download/{doc_hash}/
```

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
- File download (PDF)

### Document Verification

#### Verify Document
```http
POST /verify/
```

**Request Body:**
```json
{
  "empId": "EMP123456",
  "docHash": "b2c3d4e5f6g7..."
}
```

**Response (Valid Document):**
```json
{
  "success": true,
  "data": {
    "isValid": true,
    "message": "Document verified successfully",
    "employeeDetails": {
      "empId": "EMP123456",
      "userHash": "a1b2c3d4e5f6...",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "jobDesignation": "Software Engineer",
      "department": "Engineering",
      "isProfileComplete": true
    },
    "documentPreview": "/api/documents/preview/b2c3d4e5f6g7.../",
    "downloadLink": "/api/documents/download/b2c3d4e5f6g7.../",
    "verificationDate": "2025-01-01T00:00:00Z"
  },
  "message": "Document verification completed successfully"
}
```

**Response (Invalid Document):**
```json
{
  "success": true,
  "data": {
    "isValid": false,
    "message": "Document is tampered or not the original",
    "verificationDate": "2025-01-01T00:00:00Z"
  },
  "message": "Document verification completed"
}
```

**Status Codes:**
- `200` - Verification completed
- `400` - Validation error
- `404` - Employee not found
- `500` - Server error

### Issuer Management

#### Authorize Employee
```http
POST /issuer/authorize/
```

**Headers:**
```
Authorization: Bearer <access-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "empId": "EMP123456",
  "userHash": "a1b2c3d4e5f6...",
  "reason": "Employment verification"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "issuerId": "ISSUER_1",
    "empId": "EMP123456",
    "userHash": "a1b2c3d4e5f6...",
    "permissionGranted": true,
    "reason": "Employment verification",
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:00:00Z"
  },
  "message": "Employee authorized successfully"
}
```

#### Get Employee Details
```http
POST /issuer/employee-details/
```

**Headers:**
```
Authorization: Bearer <access-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "empId": "EMP123456",
  "userHash": "a1b2c3d4e5f6..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "empId": "EMP123456",
    "userHash": "a1b2c3d4e5f6...",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "jobDesignation": "Software Engineer",
    "department": "Engineering",
    "isProfileComplete": true,
    "hasOriginalDocument": true,
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:00:00Z"
  },
  "message": "Employee details retrieved successfully"
}
```

## 🔒 Error Handling

### Standard Error Response Format

```json
{
  "success": false,
  "error": "Error message",
  "details": {
    "field_name": ["Specific error message"]
  }
}
```

### Common Error Codes

| Status Code | Description |
|-------------|-------------|
| `400` | Bad Request - Invalid input data |
| `401` | Unauthorized - Invalid or missing token |
| `403` | Forbidden - Insufficient permissions |
| `404` | Not Found - Resource not found |
| `409` | Conflict - Resource already exists |
| `413` | Payload Too Large - File size exceeded |
| `415` | Unsupported Media Type - Invalid file type |
| `500` | Internal Server Error - Server error |

### Validation Errors

```json
{
  "success": false,
  "error": "Validation failed",
  "details": {
    "email": ["This field is required."],
    "password": ["This password is too short."],
    "confirm_password": ["Passwords don't match."]
  }
}
```

## 📊 Rate Limiting

API endpoints are rate limited to prevent abuse:

- **Authentication endpoints**: 5 requests per minute per IP
- **Document upload**: 10 requests per hour per user
- **Verification endpoints**: 100 requests per hour per IP
- **Other endpoints**: 1000 requests per hour per user

## 🔐 Security Considerations

### Authentication
- JWT tokens expire after 1 hour
- Refresh tokens expire after 7 days
- Tokens are stored securely in HTTP-only cookies (recommended)

### File Upload
- Only PDF files are accepted
- Maximum file size: 10MB
- Files are scanned for malware
- Document hashes are generated using SHA-256

### Data Protection
- All sensitive data is encrypted at rest
- API communications use HTTPS
- User passwords are hashed using bcrypt
- Personal information is protected according to GDPR

## 🧪 Testing the API

### Using cURL

#### Register a User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "confirm_password": "testpass123"
  }'
```

#### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### Upload Document
```bash
curl -X POST http://127.0.0.1:8000/api/documents/upload/ \
  -H "Authorization: Bearer <your-token>" \
  -F "file=@document.pdf"
```

#### Verify Document
```bash
curl -X POST http://127.0.0.1:8000/api/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "empId": "EMP123456",
    "docHash": "b2c3d4e5f6g7..."
  }'
```

### Using Postman

1. Import the API collection
2. Set the base URL to `http://127.0.0.1:8000/api`
3. Register a user and get the access token
4. Set the Authorization header with the token
5. Test the endpoints

## 📈 API Versioning

The API uses URL versioning:

- Current version: `v1` (default)
- Future versions: `v2`, `v3`, etc.

Example:
```
http://127.0.0.1:8000/api/v1/auth/register/
```

## 🔄 Webhooks

Webhooks are available for the following events:

- `user.registered` - When a new user registers
- `document.uploaded` - When a document is uploaded
- `document.verified` - When a document is verified
- `employee.authorized` - When an employee is authorized

### Webhook Payload

```json
{
  "event": "document.verified",
  "timestamp": "2025-01-01T00:00:00Z",
  "data": {
    "empId": "EMP123456",
    "docHash": "b2c3d4e5f6g7...",
    "isValid": true,
    "verificationDate": "2025-01-01T00:00:00Z"
  }
}
```

---

**API Documentation v1.0** - *Last updated: January 2025*
