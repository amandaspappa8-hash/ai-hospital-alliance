import { useEffect, useRef } from "react"
import { useNavigate, useLocation } from "react-router-dom"
import { getToken, getUser } from "@/lib/auth-storage"
import { hasAccess } from "@/lib/rbac"

export default function ProtectedRoute({ children, routeKey }: { children: React.ReactNode, routeKey?: string }) {
  const navigate = useNavigate()
  const location = useLocation()
  const redirected = useRef(false)

  const token = getToken()
  const user = getUser()

  useEffect(() => {
    if (redirected.current) return
    if (!token || !user) {
      redirected.current = true
      navigate("/login", { replace: true, state: { from: location } })
    } else if (routeKey && !hasAccess(user.role as any, routeKey as any)) {
      redirected.current = true
      navigate("/dashboard", { replace: true })
    }
  }, [token])

  if (!token || !user) return null
  return <>{children}</>
}
