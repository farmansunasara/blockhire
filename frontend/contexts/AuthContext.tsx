"use client"

import type React from "react"
import { createContext, useContext, useEffect, useState } from "react"
import { UserCredentials, UserProfile } from "@/types/api"
import { apiService } from "@/services/api"

// Simple User type for demo mode
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
      }
    } catch (error) {
      console.error("Error loading user profile:", error)
    }
  }

  useEffect(() => {
    // Check localStorage for existing user and tokens
    const demoUser = localStorage.getItem("demoUser")
    const accessToken = localStorage.getItem("accessToken")
    
    if (demoUser) {
      const user = JSON.parse(demoUser) as User
      setUser(user)
      loadUserProfile(user)
    } else if (accessToken) {
      // If we have a token but no demo user, try to load the profile
      // This handles the case where the user logged in but the page was refreshed
      apiService.getProfile().then(response => {
        if (response.success && response.data) {
          setUserProfile(response.data)
          // Create a minimal user object
          const user: User = {
            email: response.data.email,
            uid: response.data.id?.toString() || 'unknown'
          }
          setUser(user)
        }
      }).catch(error => {
        console.error("Error loading profile from token:", error)
        // Clear invalid tokens
        localStorage.removeItem("accessToken")
        localStorage.removeItem("refreshToken")
      })
    }
    setLoading(false)
  }, [])

  const login = async (email: string, password: string) => {
    try {
      const response = await apiService.login(email, password)
      
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
      // Call logout API
      await apiService.logout()
    } catch (error) {
      console.error("Logout error:", error)
    } finally {
      // Clear localStorage
      localStorage.removeItem("accessToken")
      localStorage.removeItem("refreshToken")
      localStorage.removeItem("demoUser")
      localStorage.removeItem("userProfile")
      localStorage.removeItem("userCredentials")
      setUser(null)
      setUserProfile(null)
      setCredentials(null)
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
