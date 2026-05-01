import { safeStorage } from "./safe-storage"

const TOKEN_KEY = "aiha_token"
const USER_KEY = "aiha_user"

import type { AuthUser } from "@/types/auth"

export function getToken(): string | null {
  return safeStorage.get(TOKEN_KEY)
}

export function setToken(token: string): void {
  safeStorage.set(TOKEN_KEY, token)
}

export function getUser(): AuthUser | null {
  const raw = safeStorage.get(USER_KEY)
  if (!raw) return null
  try { return JSON.parse(raw) as AuthUser } catch { return null }
}

export function setUser(user: AuthUser): void {
  safeStorage.set(USER_KEY, JSON.stringify(user))
}

export function saveAuth(token: string, user: AuthUser): void {
  setToken(token)
  setUser(user)
}

export function clearToken(): void {
  safeStorage.remove(TOKEN_KEY)
}

export function clearAuth(): void {
  safeStorage.remove(TOKEN_KEY)
  safeStorage.remove(USER_KEY)
}

export function logout(): void {
  clearAuth()
}
