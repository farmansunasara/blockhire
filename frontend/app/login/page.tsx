"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "../../contexts/AuthContext"
import Layout from "../../components/Layout"

export default function LoginPage() {
  const [activeTab, setActiveTab] = useState<"login" | "register">("login")
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")
  const router = useRouter()
  const { user, login, register } = useAuth()

  useEffect(() => {
    if (user) {
      router.push("/profile")
    }
  }, [user, router])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage("")

    try {
      if (activeTab === "register") {
        if (formData.password !== formData.confirmPassword) {
          setMessage("Passwords do not match")
          setLoading(false)
          return
        }
        await register(formData.email, formData.password)
        setMessage("Registration successful!")
      } else {
        await login(formData.email, formData.password)
        setMessage("Login successful!")
      }

      setTimeout(() => {
        router.push("/profile")
      }, 1000)
    } catch (error: any) {
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
          <strong>Demo Mode:</strong> Using localStorage for data persistence. Ready for Django backend integration.
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
              />
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
              />
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
                />
              </div>
            )}

            <button type="submit" className="btn btn-primary" style={{ width: "100%" }} disabled={loading}>
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
