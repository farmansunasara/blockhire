import { 
  UserCredentials, 
  UserProfile, 
  DocumentRecord, 
  VerificationResult, 
  IssuerAuthorization,
  APIResponse,
  RegistrationData,
  ProfileFormData,
  VerificationRequest,
  AuthorizationRequest
} from '@/types/api'

class APIService {
  private baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
  
  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<APIResponse<T>> {
    try {
      const url = `${this.baseURL}${endpoint}`
      
      // Get access token from localStorage
      const accessToken = localStorage.getItem('accessToken')
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...(accessToken && { 'Authorization': `Bearer ${accessToken}` }),
          ...options.headers,
        },
        ...options,
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || data.message || 'Request failed')
      }

      return data
    } catch (error) {
      console.error('API Error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      }
    }
  }

  // Auth endpoints
  async register(data: RegistrationData): Promise<APIResponse<{ user: any, tokens: any }>> {
    // Convert confirmPassword to confirm_password for backend compatibility
    const backendData = {
      email: data.email,
      password: data.password,
      confirm_password: data.confirmPassword
    }
    
    return this.request<{ user: any, tokens: any }>('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(backendData),
    })
  }

  async login(email: string, password: string): Promise<APIResponse<{ user: any, tokens: any }>> {
    return this.request<{ user: any, tokens: any }>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
  }

  async logout(): Promise<APIResponse<null>> {
    return this.request<null>('/auth/logout/', {
      method: 'POST',
    })
  }

  // Profile endpoints
  async getProfile(): Promise<APIResponse<UserProfile>> {
    return this.request<UserProfile>('/profile/')
  }

  async updateProfile(data: Partial<ProfileFormData>): Promise<APIResponse<UserProfile>> {
    return this.request<UserProfile>('/profile/update/', {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  // Document endpoints
  async uploadDocument(file: File): Promise<APIResponse<DocumentRecord>> {
    const formData = new FormData()
    formData.append('file', file)
    
    // Get access token for authentication
    const accessToken = localStorage.getItem('accessToken')
    
    return this.request<DocumentRecord>('/documents/upload/', {
      method: 'POST',
      headers: {
        // Don't set Content-Type, let browser set it for FormData
        ...(accessToken && { 'Authorization': `Bearer ${accessToken}` }),
      },
      body: formData,
    })
  }

  async getDocumentHistory(): Promise<APIResponse<DocumentRecord[]>> {
    return this.request<DocumentRecord[]>('/documents/history/')
  }

  async downloadDocument(docHash: string): Promise<APIResponse<Blob>> {
    const response = await fetch(`${this.baseURL}/documents/download/${docHash}/`)
    if (!response.ok) throw new Error('Download failed')
    return { success: true, data: await response.blob() }
  }

  // Verification endpoints
  async verifyDocument(request: VerificationRequest): Promise<APIResponse<VerificationResult>> {
    return this.request<VerificationResult>('/verify/', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  // Issuer endpoints
  async authorizeEmployee(request: AuthorizationRequest): Promise<APIResponse<IssuerAuthorization>> {
    return this.request<IssuerAuthorization>('/issuer/authorize/', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  async getEmployeeDetails(request: AuthorizationRequest): Promise<APIResponse<UserProfile>> {
    try {
      return await this.request<UserProfile>('/issuer/employee-details/', {
        method: 'POST',
        body: JSON.stringify(request),
      })
    } catch (error) {
      return {
        success: false,
        error: 'Failed to fetch employee details. Please check credentials and try again.'
      }
    }
  }

  async getAuthorizedEmployees(): Promise<APIResponse<IssuerAuthorization[]>> {
    return this.request<IssuerAuthorization[]>('/issuer/authorized/')
  }

  // Utility methods for demo mode
  generateDemoCredentials(): UserCredentials {
    const timestamp = Date.now()
    const empId = `EMP${timestamp.toString().slice(-6)}`
    const userHash = this.generateHashSync(`demo@example.com${empId}${timestamp}`)
    
    return {
      userHash,
      empId,
      email: 'demo@example.com'
    }
  }

  private async generateHash(input: string): Promise<string> {
    // Use Web Crypto API for proper SHA-256 hashing
    const encoder = new TextEncoder()
    const data = encoder.encode(input)
    const hashBuffer = await crypto.subtle.digest('SHA-256', data)
    const hashArray = Array.from(new Uint8Array(hashBuffer))
    return '0x' + hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
  }

  private generateHashSync(input: string): string {
    // Fallback for demo mode - simple hash function
    let hash = 0
    for (let i = 0; i < input.length; i++) {
      const char = input.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash // Convert to 32-bit integer
    }
    return `0x${Math.abs(hash).toString(16).padStart(8, '0')}`
  }
}

export const apiService = new APIService()
export default apiService
