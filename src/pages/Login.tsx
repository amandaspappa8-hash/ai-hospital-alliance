import { useState, useMemo } from "react"
import { Navigate, useNavigate, Link } from "react-router-dom"
import { clearAuth, getToken, saveAuth } from "@/lib/auth-storage"
import { login } from "@/services/auth"

export default function Login() {
  // useMemo يمنع إعادة قراءة localStorage عند كل render
  const existingToken = useMemo(() => getToken(), [])
  const navigate = useNavigate()

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  // إذا كان مسجلاً مسبقاً، وجّهه مباشرة
  if (existingToken) return <Navigate to="/dashboard" replace />

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError("")

    try {
      clearAuth()
      const data = await login(username.trim(), password.trim())
      saveAuth(data.access_token, data.user)
      // navigate بدلاً من window.location لتجنب إعادة mount كاملة
      navigate("/dashboard", { replace: true })
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight: "100vh", display: "grid", placeItems: "center", background: "#030712", color: "white", padding: 24 }}>
      <form onSubmit={handleLogin} style={{ width: "100%", maxWidth: 420, background: "#111827", border: "1px solid #374151", borderRadius: 16, padding: 24 }}>
        <h1 style={{ fontSize: 28, marginBottom: 8 }}>AI Hospital Alliance</h1>
        <p style={{ opacity: 0.8, marginBottom: 20 }}>Medical platform login</p>

        <label>Username</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} style={s} />

        <label style={{ marginTop: 12, display: "block" }}>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={s} />

        <button type="submit" disabled={loading} style={{ width: "100%", padding: 12, marginTop: 16, borderRadius: 10 }}>
          {loading ? "Signing in..." : "Login"}
        </button>

        {error && <div style={{ color: "#fca5a5", marginTop: 14 }}>{error}</div>}

        <div style={{ textAlign: "center", marginTop: 20, paddingTop: 16, borderTop: "1px solid #374151" }}>
          <span style={{ color: "#6B7280", fontSize: 14 }}>New hospital? </span>
          <Link to="/register" style={{ color: "#3B82F6", fontSize: 14, fontWeight: 600, textDecoration: "none" }}>
            Register here →
          </Link>
        </div>
      </form>
    </div>
  )
}

const s: React.CSSProperties = {
  width: "100%",
  padding: "10px 12px",
  marginTop: 6,
  borderRadius: 10,
  border: "1px solid #374151",
  background: "#030712",
  color: "white",
}
