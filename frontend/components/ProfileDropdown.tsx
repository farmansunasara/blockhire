"use client"

import { useState, useRef, useEffect } from "react"
import Link from "next/link"
import { useAuth } from "../contexts/AuthContext"
import { useRouter } from "next/navigation"
import { User, LogOut, Edit3 } from "lucide-react"

export default function ProfileDropdown() {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const { user, logout } = useAuth()
  const router = useRouter()

  const handleLogout = async () => {
    try {
      await logout()
      router.push("/")
    } catch (error) {
      console.error("Logout error:", error)
    }
  }

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [])

  if (!user) return null

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="icon-link"
        aria-label="Profile menu"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <User size={20} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-200 z-50 overflow-hidden">
          <div className="py-2">
            {/* User Info Header */}
            <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
              <p className="text-sm font-semibold text-gray-900">
                {user.displayName || "User"}
              </p>
              <p className="text-xs text-gray-600 truncate mt-1">
                {user.email}
              </p>
            </div>

            {/* Menu Items */}
            <Link
              href="/profile/info"
              className="flex items-center px-4 py-3 text-sm transition-all duration-200 border-l-2 border-transparent"
              style={{ 
                color: '#374151', 
                backgroundColor: 'transparent'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#eff6ff'
                e.currentTarget.style.color = '#1d4ed8'
                e.currentTarget.style.borderLeftColor = '#3b82f6'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent'
                e.currentTarget.style.color = '#374151'
                e.currentTarget.style.borderLeftColor = 'transparent'
              }}
              onClick={() => setIsOpen(false)}
            >
              <User size={16} className="mr-3" style={{ color: '#6b7280' }} />
              View Profile
            </Link>

            <Link
              href="/profile/edit"
              className="flex items-center px-4 py-3 text-sm transition-all duration-200 border-l-2 border-transparent"
              style={{ 
                color: '#374151', 
                backgroundColor: 'transparent'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#eff6ff'
                e.currentTarget.style.color = '#1d4ed8'
                e.currentTarget.style.borderLeftColor = '#3b82f6'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent'
                e.currentTarget.style.color = '#374151'
                e.currentTarget.style.borderLeftColor = 'transparent'
              }}
              onClick={() => setIsOpen(false)}
            >
              <Edit3 size={16} className="mr-3" style={{ color: '#6b7280' }} />
              Edit Profile
            </Link>

            <div className="border-t border-gray-200 my-1">
              <button
                onClick={handleLogout}
                className="flex items-center w-full px-4 py-3 text-sm transition-all duration-200 border-l-2 border-transparent"
                style={{ 
                  color: '#dc2626', 
                  backgroundColor: 'transparent'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#fef2f2'
                  e.currentTarget.style.color = '#991b1b'
                  e.currentTarget.style.borderLeftColor = '#ef4444'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'transparent'
                  e.currentTarget.style.color = '#dc2626'
                  e.currentTarget.style.borderLeftColor = 'transparent'
                }}
              >
                <LogOut size={16} className="mr-3" style={{ color: '#dc2626' }} />
                Logout
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
