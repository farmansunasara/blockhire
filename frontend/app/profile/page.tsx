"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import ProtectedRoute from "../../components/ProtectedRoute"

export default function ProfileIndexRedirect() {
  const router = useRouter()

  useEffect(() => {
    // Always redirect to edit page to prevent localStorage-based routing
    // The edit page will handle profile completion logic properly
    router.replace("/profile/edit")
  }, [router])

  return (
    <ProtectedRoute>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "50vh" }}>
        <div className="spinner"></div>
        <span style={{ marginLeft: "0.75rem" }}>Loading profile…</span>
      </div>
    </ProtectedRoute>
  )
}
