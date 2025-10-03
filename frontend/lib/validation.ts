/**
 * Comprehensive validation utilities for BlockHire forms
 */

export interface ValidationRule {
  required?: boolean
  minLength?: number
  maxLength?: number
  pattern?: RegExp
  custom?: (value: any) => string | null
}

export interface ValidationResult {
  isValid: boolean
  errors: Record<string, string>
}

export class FormValidator {
  private rules: Record<string, ValidationRule> = {}
  
  addRule(field: string, rule: ValidationRule) {
    this.rules[field] = rule
  }
  
  validate(data: Record<string, any>): ValidationResult {
    const errors: Record<string, string> = {}
    
    for (const [field, rule] of Object.entries(this.rules)) {
      const value = data[field]
      
      // Required validation
      if (rule.required && (!value || value.toString().trim() === '')) {
        errors[field] = `${this.getFieldLabel(field)} is required`
        continue
      }
      
      // Skip other validations if field is empty and not required
      if (!value || value.toString().trim() === '') continue
      
      // Min length validation
      if (rule.minLength && value.toString().length < rule.minLength) {
        errors[field] = `${this.getFieldLabel(field)} must be at least ${rule.minLength} characters`
        continue
      }
      
      // Max length validation
      if (rule.maxLength && value.toString().length > rule.maxLength) {
        errors[field] = `${this.getFieldLabel(field)} must be no more than ${rule.maxLength} characters`
        continue
      }
      
      // Pattern validation
      if (rule.pattern && !rule.pattern.test(value.toString())) {
        errors[field] = `${this.getFieldLabel(field)} format is invalid`
        continue
      }
      
      // Custom validation
      if (rule.custom) {
        const customError = rule.custom(value)
        if (customError) {
          errors[field] = customError
        }
      }
    }
    
    return {
      isValid: Object.keys(errors).length === 0,
      errors
    }
  }
  
  private getFieldLabel(field: string): string {
    const labels: Record<string, string> = {
      email: 'Email',
      password: 'Password',
      confirmPassword: 'Confirm Password',
      firstName: 'First Name',
      lastName: 'Last Name',
      dateOfBirth: 'Date of Birth',
      mobile: 'Mobile Number',
      address: 'Address',
      jobDesignation: 'Job Designation',
      department: 'Department'
    }
    return labels[field] || field.charAt(0).toUpperCase() + field.slice(1)
  }
}

// Predefined validation rules
export const validationRules = {
  email: {
    required: true,
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    maxLength: 254
  },
  
  password: {
    required: true,
    minLength: 8,
    maxLength: 128,
    pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
    custom: (value: string) => {
      if (value.length < 8) return 'Password must be at least 8 characters'
      if (!/[a-z]/.test(value)) return 'Password must contain at least one lowercase letter'
      if (!/[A-Z]/.test(value)) return 'Password must contain at least one uppercase letter'
      if (!/\d/.test(value)) return 'Password must contain at least one number'
      if (!/[@$!%*?&]/.test(value)) return 'Password must contain at least one special character'
      return null
    }
  },
  
  confirmPassword: {
    required: true,
    custom: (value: string, formData?: any) => {
      if (formData && value !== formData.password) {
        return 'Passwords do not match'
      }
      return null
    }
  },
  
  firstName: {
    required: true,
    minLength: 2,
    maxLength: 50,
    pattern: /^[a-zA-Z\s'-]+$/
  },
  
  lastName: {
    required: true,
    minLength: 2,
    maxLength: 50,
    pattern: /^[a-zA-Z\s'-]+$/
  },
  
  dateOfBirth: {
    required: true,
    custom: (value: string) => {
      const date = new Date(value)
      const today = new Date()
      const age = today.getFullYear() - date.getFullYear()
      
      if (isNaN(date.getTime())) return 'Invalid date format'
      if (age < 16) return 'You must be at least 16 years old'
      if (age > 100) return 'Invalid age'
      if (date > today) return 'Date of birth cannot be in the future'
      
      return null
    }
  },
  
  mobile: {
    required: true,
    pattern: /^[\+]?[1-9][\d]{0,15}$/,
    custom: (value: string) => {
      const cleaned = value.replace(/[\s\-\(\)]/g, '')
      if (cleaned.length < 10) return 'Mobile number must be at least 10 digits'
      if (cleaned.length > 15) return 'Mobile number cannot exceed 15 digits'
      return null
    }
  },
  
  address: {
    required: true,
    minLength: 10,
    maxLength: 500
  },
  
  jobDesignation: {
    required: true,
    minLength: 2,
    maxLength: 100
  },
  
  department: {
    required: true,
    minLength: 2,
    maxLength: 100
  }
}

// File validation
export const fileValidation = {
  maxSize: 10 * 1024 * 1024, // 10MB
  allowedTypes: ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'],
  allowedExtensions: ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
}

export function validateFile(file: File): string | null {
  // Check file size
  if (file.size > fileValidation.maxSize) {
    return `File size must be less than ${fileValidation.maxSize / (1024 * 1024)}MB`
  }
  
  // Check file type
  if (!fileValidation.allowedTypes.includes(file.type)) {
    return `File type not supported. Allowed types: ${fileValidation.allowedExtensions.join(', ')}`
  }
  
  // Check file extension
  const extension = '.' + file.name.split('.').pop()?.toLowerCase()
  if (!fileValidation.allowedExtensions.includes(extension)) {
    return `File extension not supported. Allowed extensions: ${fileValidation.allowedExtensions.join(', ')}`
  }
  
  return null
}
