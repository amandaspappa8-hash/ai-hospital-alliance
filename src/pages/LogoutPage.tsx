import { Navigate } from "react-router-dom"
import { clearAuth } from "@/lib/auth-storage"

export default function LogoutPage() {
  clearAuth()
  return <Navigate to="/login" replace />
}
