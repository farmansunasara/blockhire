"use client"

import type React from "react"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useAuth } from "../contexts/AuthContext"
import ProfileDropdown from "./ProfileDropdown"
import Breadcrumbs from "./Breadcrumbs"
import NavigationProgress from "./NavigationProgress"

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const pathname = usePathname()
  const { user, logout } = useAuth()

  const handleLogout = async () => {
    try {
      await logout()
    } catch (error) {
      console.error("Logout error:", error)
    }
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <header className="header">
        <div className="container">
          <div className="header-content">
            <Link href="/" className="logo">
              BlockHire
            </Link>
            <nav>
              <ul className="nav-links">
                <li>
                  <Link href="/">Home</Link>
                </li>
                {user && (
                  <>
                    <li>
                      <Link href="/verify">Verify</Link>
                    </li>
                    <li>
                      <Link href="/issuer">Issuer</Link>
                    </li>
                  </>
                )}
                {user ? (
                  <li>
                    <ProfileDropdown />
                  </li>
                ) : (
                  <li>
                    <Link href="/login" aria-label="Login" className="icon-link">
                      <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                        <path d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4s-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
                      </svg>
                    </Link>
                  </li>
                )}
              </ul>
            </nav>
          </div>
        </div>
      </header>

      <main style={{ flex: 1 }}>
        <NavigationProgress />
        <div className="container" style={{ paddingTop: '1rem', paddingBottom: '1rem' }}>
          <Breadcrumbs />
        </div>
        {children}
      </main>

      <footer className="footer">
        <div className="container">
          <div className="footer-links">
            <Link href="/privacy">Privacy</Link>
            <Link href="/terms">Terms</Link>
            <a href="#" target="_blank" rel="noreferrer">
              Twitter
            </a>
            <a href="#" target="_blank" rel="noreferrer">
              LinkedIn
            </a>
          </div>
          <p>&copy; 2025 BlockHire. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
