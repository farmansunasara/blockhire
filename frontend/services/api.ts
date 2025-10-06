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
  private baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api'
  
  // Helper function to check if token is expired
  private isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const exp = payload.exp * 1000 // Convert to milliseconds
      return Date.now() >= exp
    } catch {
      return true // If we can't parse it, consider it expired
    }
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<APIResponse<T>> {
    try {
      const url = `${this.baseURL}${endpoint}`
      
      // Get access token from localStorage
      let accessToken = localStorage.getItem('accessToken')
      
      // Check if token is expired before using it
      if (accessToken && this.isTokenExpired(accessToken)) {
        console.log('Access token is expired, clearing tokens')
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        accessToken = null
      }
      
      console.log('API Request:', { url, accessToken: accessToken ? 'Present' : 'Missing', options })
      
      let response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...(accessToken && { 'Authorization': `Bearer ${accessToken}` }),
          ...options.headers,
        },
        ...options,
      })

      // If token expired (401), try to refresh
      if (response.status === 401 && accessToken) {
        console.log('Token expired, attempting refresh...')
        const refreshSuccess = await this.refreshAccessToken()
        
        if (refreshSuccess) {
          // Retry the request with new token
          accessToken = localStorage.getItem('accessToken')
          response = await fetch(url, {
            headers: {
              'Content-Type': 'application/json',
              ...(accessToken && { 'Authorization': `Bearer ${accessToken}` }),
              ...options.headers,
            },
            ...options,
          })
        }
      }

      console.log('API Response status:', response.status, response.statusText)
      const data = await response.json()
      console.log('API Response data:', data)
      
      if (!response.ok) {
        console.error('API Response Error:', {
          status: response.status,
          statusText: response.statusText,
          data: data,
          url: url
        })
        throw new Error(data.error || data.message || `Request failed with status ${response.status}`)
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

  private async refreshAccessToken(): Promise<boolean> {
    try {
      const refreshToken = localStorage.getItem('refreshToken')
      if (!refreshToken) {
        console.log('No refresh token available')
        return false
      }

      const response = await fetch(`${this.baseURL}/auth/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success && data.data) {
          localStorage.setItem('accessToken', data.data.access)
          console.log('Token refreshed successfully')
          return true
        }
      }
      
      console.log('Token refresh failed, clearing tokens')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      return false
    } catch (error) {
      console.error('Token refresh error:', error)
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      return false
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
    console.log('API Service: Login request for:', email)
    const response = await this.request<{ user: any, tokens: any }>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    console.log('API Service: Login response:', response)
    return response
  }

  async logout(): Promise<APIResponse<null>> {
    return this.request<null>('/auth/logout/', {
      method: 'POST',
    })
  }

  // Profile endpoints
  async getProfile(): Promise<APIResponse<UserProfile>> {
    const response = await this.request<any>('/profile/')
    
    if (response.success && response.data) {
      // Convert snake_case to camelCase for frontend compatibility
      const profileData = {
        ...response.data,
        firstName: response.data.first_name,
        lastName: response.data.last_name,
        dateOfBirth: response.data.date_of_birth,
        jobDesignation: response.data.job_designation,
        docHash: response.data.doc_hash,
        docHistory: response.data.doc_history || [],
        storagePath: response.data.storage_path,
        isProfileComplete: response.data.is_profile_complete,
        createdAt: response.data.created_at,
        updatedAt: response.data.updated_at,
        // Add credential fields
        userHash: response.data.user_hash,
        empId: response.data.emp_id,
      }
      
      return {
        ...response,
        data: profileData
      }
    }
    
    return response
  }

  async updateProfile(data: Partial<ProfileFormData>): Promise<APIResponse<UserProfile>> {
    // Convert camelCase to snake_case for backend compatibility
    const backendData = {
      first_name: data.firstName,
      last_name: data.lastName,
      date_of_birth: data.dateOfBirth,
      mobile: data.mobile,
      address: data.address,
      job_designation: data.jobDesignation,
      department: data.department,
    }
    
    return this.request<UserProfile>('/profile/update/', {
      method: 'PUT',
      body: JSON.stringify(backendData),
    })
  }

  // Document endpoints
  async uploadDocument(file: File): Promise<APIResponse<DocumentRecord>> {
    const formData = new FormData()
    formData.append('file', file)
    
    // Get access token for authentication
    const accessToken = localStorage.getItem('accessToken')
    
    if (!accessToken) {
      throw new Error('No access token found. Please login again.')
    }
    
    return this.request<DocumentRecord>('/documents/upload/', {
      method: 'POST',
      headers: {
        // Don't set Content-Type, let browser set it for FormData
        'Authorization': `Bearer ${accessToken}`,
      },
      body: formData,
    })
  }

  async getDocumentHistory(): Promise<APIResponse<DocumentRecord[]>> {
    const response = await this.request<any[]>('/documents/history/')
    
    if (response.success === false) {
      return response as APIResponse<DocumentRecord[]>
    }
    
    // Transform snake_case to camelCase for frontend compatibility
    const transformedData = response.map((doc: any) => ({
      docHash: doc.doc_hash,
      uploadDate: doc.upload_date,
      fileName: doc.file_name,
      fileSize: doc.file_size,
      isOriginal: doc.is_original,
      storagePath: doc.storage_path
    }))
    
    return {
      success: true,
      data: transformedData
    }
  }

  async downloadDocument(docHash: string): Promise<APIResponse<Blob>> {
    const response = await fetch(`${this.baseURL}/documents/download/${docHash}/`)
    if (!response.ok) throw new Error('Download failed')
    return { success: true, data: await response.blob() }
  }

  // Verification endpoints
  async verifyDocument(request: VerificationRequest): Promise<APIResponse<VerificationResult>> {
    // Convert camelCase to snake_case for backend compatibility
    const backendData = {
      emp_id: request.empId,
      doc_hash: request.docHash,
    }
    
    return this.request<VerificationResult>('/verify/', {
      method: 'POST',
      body: JSON.stringify(backendData),
    })
  }

  // Issuer endpoints
  async authorizeEmployee(request: AuthorizationRequest): Promise<APIResponse<IssuerAuthorization>> {
    // Convert camelCase to snake_case for backend compatibility
    const backendData = {
      emp_id: request.empId,
      user_hash: request.userHash,
    }
    
    return this.request<IssuerAuthorization>('/issuer/authorize/', {
      method: 'POST',
      body: JSON.stringify(backendData),
    })
  }

  async getEmployeeDetails(request: AuthorizationRequest): Promise<APIResponse<UserProfile>> {
    try {
      // Convert camelCase to snake_case for backend compatibility
      const backendData = {
        emp_id: request.empId,
        user_hash: request.userHash,
      }
      
      return await this.request<UserProfile>('/issuer/employee-details/', {
        method: 'POST',
        body: JSON.stringify(backendData),
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


  private async generateHash(input: string): Promise<string> {
    // Use Web Crypto API for proper SHA-256 hashing
    const encoder = new TextEncoder()
    const data = encoder.encode(input)
    const hashBuffer = await crypto.subtle.digest('SHA-256', data)
    const hashArray = Array.from(new Uint8Array(hashBuffer))
    return '0x' + hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
  }

  private generateHashSync(input: string): string {
    // Fallback hash function
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
