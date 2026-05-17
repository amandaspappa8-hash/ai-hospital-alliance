import { useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { clearAuth } from "@/lib/auth-storage"

export default function LogoutPage() {
  const navigate = useNavigate()

  useEffect(() => {
    clearAuth()
    const timeout = window.setTimeout(() => {
      navigate("/login", { replace: true })
    }, 500)

    return () => window.clearTimeout(timeout)
  }, [navigate])

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", background: "#020817", color: "white", fontFamily: "Inter,Arial,sans-serif", gap: 16 }}>
      <div style={{ fontSize: 48 }}>👋</div>
      <div style={{ fontSize: 20, fontWeight: 700 }}>Logging out...</div>
      <div style={{ color: "#64748b", fontSize: 13 }}>Redirecting to login page</div>
    </div>
  )
}
