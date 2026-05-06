import { apiGet, apiPost } from "@/lib/api"
import type { AuthUser, LoginResponse } from "@/types/auth"

export function login(username: string, password: string) {
  return apiPost<LoginResponse>("/auth/login", { username, password })
}

export function getMe(token: string) {
  return apiGet<AuthUser>(`/auth/me?token=${encodeURIComponent(token)}`)
}
