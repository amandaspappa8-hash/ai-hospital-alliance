import { useMemo } from "react"
import { Navigate, useLocation } from "react-router-dom"
import { getToken, getUser } from "@/lib/auth-storage"
import { hasAccess, type AppRoute } from "@/lib/rbac"

type ProtectedRouteProps = {
  children: React.ReactNode
  routeKey?: AppRoute
}

export default function ProtectedRoute({ children, routeKey }: ProtectedRouteProps) {
  const location = useLocation()

  const token = useMemo(() => getToken(), [])
  const user = useMemo(() => getUser(), [])

  if (!token || !user) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }

  if (routeKey && !hasAccess(user.role, routeKey)) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}
