import { useLocation, Navigate } from "react-router-dom"
import { getAuthState } from "@/lib/auth-storage"
import { hasAccess, type AppRoute } from "@/lib/rbac"

type Props = {
  children: React.ReactNode
  routeKey?: AppRoute
}

export default function ProtectedRoute({ children, routeKey }: Props) {
  const location = useLocation()
  const auth = getAuthState()

  if (!auth) {
    return <Navigate to="/ahos-login" replace state={{ from: `${location.pathname}${location.search}` }} />
  }

  if (routeKey && !hasAccess(auth.user.role, routeKey)) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}
