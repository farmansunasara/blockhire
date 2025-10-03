// Core data types for the BlockHire system

export interface UserCredentials {
  userHash: string        // Immutable, auto-generated
  empId: string          // Immutable, auto-generated
  email: string          // Immutable after first save
}

export interface DocumentRecord {
  docHash: string
  uploadDate: string
  fileName: string
  fileSize: number
  isOriginal: boolean
  storagePath: string
}

export interface UserProfile extends UserCredentials {
  // Personal Info
  firstName: string
  lastName: string
  dateOfBirth: string
  mobile: string
  address: string
  
  // Employment Info
  jobDesignation: string
  department: string
  
  // Document Info
  docHash: string        // Original valid hash
  docHistory: DocumentRecord[]
  storagePath: string
  isProfileComplete: boolean
  createdAt: string
  updatedAt: string
}

export interface VerificationResult {
  isValid: boolean
  message: string
  employeeDetails?: UserProfile
  documentPreview?: string
  downloadLink?: string
  verificationDate: string
}

export interface IssuerAuthorization {
  issuerId: string
  empId: string
  userHash: string
  permissionGranted: boolean
  timestamp: string
  issuerName?: string
}

export interface APIResponse<T> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

// Form data types
export interface RegistrationData {
  email: string
  password: string
  confirmPassword: string
}

export interface ProfileFormData {
  firstName: string
  lastName: string
  dateOfBirth: string
  mobile: string
  address: string
  jobDesignation: string
  department: string
}

export interface DocumentUploadData {
  file: File
  isOriginal: boolean
}

export interface VerificationRequest {
  empId: string
  docHash: string
}

export interface AuthorizationRequest {
  empId: string
  userHash: string
}
