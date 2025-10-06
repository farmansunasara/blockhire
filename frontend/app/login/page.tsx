"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "../../contexts/AuthContext"
import Layout from "../../components/Layout"
import { FormValidator, validationRules } from "../../lib/validation"

export default function LoginPage() {
  const [activeTab, setActiveTab] = useState<"login" | "register">("login")
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")
  const [errors, setErrors] = useState<Record<string, string>>({})
  const router = useRouter()
  const { user, login, register } = useAuth()
  
  // Initialize validator - will be updated when tab changes
  const validator = new FormValidator()
  
  // Update validator rules when tab changes
  useEffect(() => {
    validator.addRule('email', validationRules.email)
    
    if (activeTab === 'login') {
      validator.addRule('password', {
        required: true,
        minLength: 1 // Just require non-empty for login
      })
    } else {
      validator.addRule('password', validationRules.password)
      validator.addRule('confirmPassword', {
        ...validationRules.confirmPassword,
        custom: (value: string) => {
          if (activeTab === 'register' && value !== formData.password) {
            return 'Passwords do not match'
          }
          return null
        }
      })
    }
  }, [activeTab, formData.password])

  useEffect(() => {
    if (user) {
      router.push("/profile")
    }
  }, [user, router])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Form submitted, activeTab:", activeTab)
    console.log("Form data:", formData)
    
    setLoading(true)
    setMessage("")
    setErrors({})

    // Validate form
    const validation = validator.validate(formData)
    console.log("Validation result:", validation)
    
    if (!validation.isValid) {
      console.log("Validation failed:", validation.errors)
      setErrors(validation.errors)
      setLoading(false)
      return
    }

    try {
      if (activeTab === "register") {
        console.log("Attempting registration...")
        await register(formData.email, formData.password)
        setMessage("Registration successful!")
      } else {
        console.log("Attempting login...")
        await login(formData.email, formData.password)
        setMessage("Login successful!")
      }

      setTimeout(() => {
        console.log("Redirecting to profile/info...")
        router.push("/profile/info")
      }, 1500)
    } catch (error: any) {
      console.error("Authentication error:", error)
      setMessage(error.message || "Authentication failed")
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  if (user) {
    return null
  }

  return (
    <Layout>
      <div className="container" style={{ maxWidth: "500px", margin: "4rem auto" }}>
        <div className="alert alert-info" style={{ marginBottom: "2rem" }}>
          Ready for Django backend integration.
        </div>

        <div className="card">
          <div className="tabs">
            <button className={`tab ${activeTab === "login" ? "active" : ""}`} onClick={() => setActiveTab("login")}>
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="currentColor"
                style={{ marginRight: "0.5rem", verticalAlign: "middle" }}
              >
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
              </svg>
              Login
            </button>
            <button
              className={`tab ${activeTab === "register" ? "active" : ""}`}
              onClick={() => setActiveTab("register")}
            >
              Register
            </button>
          </div>

          {message && (
            <div className={`alert ${message.includes("successful") ? "alert-success" : "alert-error"}`}>{message}</div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                className={errors.email ? 'error' : ''}
              />
              {errors.email && <span className="error-message">{errors.email}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                required
                className={errors.password ? 'error' : ''}
              />
              {errors.password && <span className="error-message">{errors.password}</span>}
            </div>

            {activeTab === "register" && (
              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  required
                  className={errors.confirmPassword ? 'error' : ''}
                />
                {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
              </div>
            )}

            <button 
              type="submit" 
              className="btn btn-primary" 
              style={{ width: "100%" }} 
              disabled={loading}
              onClick={(e) => {
                console.log("Button clicked!")
                console.log("Loading state:", loading)
                console.log("Active tab:", activeTab)
              }}
            >
              {loading && <span className="spinner"></span>}
              {activeTab === "login" ? "Login" : "Register"}
            </button>
          </form>

          <div
            style={{
              textAlign: "center",
              marginTop: "2rem",
              padding: "1rem",
              background: "#f7fafc",
              borderRadius: "4px",
            }}
          >
            <p style={{ marginBottom: "1rem" }}>Or connect with MetaMask</p>
            <button className="btn btn-secondary" style={{ width: "100%" }}>
              🦊 Connect MetaMask (Coming Soon)
            </button>
          </div>
        </div>
      </div>
    </Layout>
  )
}
