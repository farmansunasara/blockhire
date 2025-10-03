"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import ProtectedRoute from "../../components/ProtectedRoute"

export default function ProfileIndexRedirect() {
  const router = useRouter()

  useEffect(() => {
    const saved = typeof window !== "undefined" ? localStorage.getItem("profile") : null
    if (saved) {
      router.replace("/profile/info")
    } else {
      router.replace("/profile/edit")
    }
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
