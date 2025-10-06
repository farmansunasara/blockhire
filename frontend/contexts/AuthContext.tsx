"use client"

import type React from "react"
import { createContext, useContext, useEffect, useState } from "react"
import { UserCredentials, UserProfile } from "@/types/api"
import { apiService } from "@/services/api"

interface User {
  email: string
  uid: string
}

interface AuthContextType {
  user: User | null
  userProfile: UserProfile | null
  credentials: UserCredentials | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshProfile: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null)
  const [credentials, setCredentials] = useState<UserCredentials | null>(null)
  const [loading, setLoading] = useState(true)


  const loadUserProfile = async (user: User) => {
    try {
      // Load from API
      const response = await apiService.getProfile()
      
      if (response.success && response.data) {
        setUserProfile(response.data)
        
        // Set credentials from profile data
        console.log("Profile data received:", response.data)
        console.log("userHash:", response.data.userHash)
        console.log("empId:", response.data.empId)
        
        if (response.data.userHash && response.data.empId) {
          const credentialsData = {
            userHash: response.data.userHash,
            empId: response.data.empId,
            email: response.data.email
          }
          console.log("Setting credentials:", credentialsData)
          setCredentials(credentialsData)
        } else {
          console.log("Missing credential data - userHash or empId not found")
        }
      } else {
        console.error("Failed to load profile:", response.error)
        // If profile loading fails due to auth issues, clear tokens
        if (response.error?.includes('Token') || response.error?.includes('Authentication')) {
          localStorage.removeItem("accessToken")
          localStorage.removeItem("refreshToken")
        }
      }
    } catch (error) {
      console.error("Error loading user profile:", error)
    }
  }

  // Helper function to check if token is expired
  const isTokenExpired = (token: string): boolean => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const exp = payload.exp * 1000 // Convert to milliseconds
      return Date.now() >= exp
    } catch {
      return true // If we can't parse it, consider it expired
    }
  }

  useEffect(() => {
    // Check localStorage for existing tokens
    const accessToken = localStorage.getItem("accessToken")
    
    console.log("AuthContext useEffect - accessToken:", accessToken ? "present" : "missing")
    
    if (accessToken) {
      // Check if token is expired before using it
      if (isTokenExpired(accessToken)) {
        console.log("Access token is expired, clearing tokens")
        localStorage.removeItem("accessToken")
        localStorage.removeItem("refreshToken")
        setLoading(false)
        return
      }
      
      console.log("Loading profile from valid token...")
      // If we have a valid token, try to load the profile
      apiService.getProfile().then(response => {
        console.log("Profile response:", response)
        if (response.success && response.data) {
          setUserProfile(response.data)
          // Create a minimal user object
          const user: User = {
            email: response.data.email,
            uid: response.data.id?.toString() || 'unknown'
          }
          console.log("Setting user from profile:", user)
          setUser(user)
          
          // Also set credentials from profile data
          if (response.data.userHash && response.data.empId) {
            const credentialsData = {
              userHash: response.data.userHash,
              empId: response.data.empId,
              email: response.data.email
            }
            console.log("Setting credentials from profile:", credentialsData)
            setCredentials(credentialsData)
          }
          setLoading(false)
        } else {
          console.log("Profile loading failed:", response.error)
          setLoading(false)
        }
      }).catch(error => {
        console.error("Error loading profile from token:", error)
        // Clear invalid tokens
        localStorage.removeItem("accessToken")
        localStorage.removeItem("refreshToken")
        setLoading(false)
      })
    } else {
      console.log("No authentication data found")
      setLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    try {
      console.log("Starting login process for:", email)
      
      
      console.log("Calling API service login...")
      const response = await apiService.login(email, password)
      console.log("Login response:", response)
      
      if (response.success && response.data) {
        const { user: userData, tokens } = response.data
        console.log("Login successful, user data:", userData)
        console.log("Tokens:", tokens)
        
        // Store tokens
        localStorage.setItem("accessToken", tokens.access)
        localStorage.setItem("refreshToken", tokens.refresh)
        
        // Create user object
        const user: User = {
          email: userData.email,
          uid: userData.id.toString()
        }
        
        console.log("Setting user:", user)
        setUser(user)
        setCredentials({
          userHash: userData.user_hash,
          empId: userData.emp_id,
          email: userData.email
        })
        
        // Load profile
        console.log("Loading user profile...")
        await loadUserProfile(user)
        console.log("Login process completed successfully")
        
        // Ensure loading is set to false after login
        setLoading(false)
      } else {
        console.error("Login failed:", response.error)
        throw new Error(response.error || "Login failed")
      }
    } catch (error) {
      console.error("Login error:", error)
      throw error
    }
  }

  const register = async (email: string, password: string) => {
    try {
      
      const response = await apiService.register({
        email,
        password,
        confirmPassword: password
      })
      
      if (response.success && response.data) {
        const { user: userData, tokens } = response.data
        
        // Store tokens
        localStorage.setItem("accessToken", tokens.access)
        localStorage.setItem("refreshToken", tokens.refresh)
        
        // Create user object
        const user: User = {
          email: userData.email,
          uid: userData.id.toString()
        }
        
        setUser(user)
        setCredentials({
          userHash: userData.user_hash,
          empId: userData.emp_id,
          email: userData.email
        })
        
        // Load profile
        await loadUserProfile(user)
      } else {
        throw new Error(response.error || "Registration failed")
      }
    } catch (error) {
      console.error("Registration error:", error)
      throw error
    }
  }

  const logout = async () => {
    try {
      console.log("AuthContext: Starting logout process")
      // Call logout API
      await apiService.logout()
      console.log("AuthContext: Logout API call successful")
    } catch (error) {
      console.error("AuthContext: Logout error:", error)
    } finally {
      console.log("AuthContext: Clearing localStorage and state")
      // Clear ALL localStorage data to prevent data leakage between users
      localStorage.removeItem("accessToken")
      localStorage.removeItem("refreshToken")
      localStorage.removeItem("userProfile")
      localStorage.removeItem("profile")
      localStorage.removeItem("documentHistory")
      localStorage.removeItem("documentHash")
      localStorage.removeItem("userHash")
      localStorage.removeItem("empId")
      localStorage.removeItem("userCredentials")
      
      // Clear all state
      setUser(null)
      setUserProfile(null)
      setCredentials(null)
      console.log("AuthContext: Logout process completed")
    }
  }

  const refreshProfile = async () => {
    if (user) {
      await loadUserProfile(user)
    }
  }

  const value = {
    user,
    userProfile,
    credentials,
    loading,
    login,
    register,
    logout,
    refreshProfile,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
