import type { AuthUser } from "@/types/auth"

const TOKEN_KEY = "aiha_token"
const USER_KEY = "aiha_user"
const ROLES = new Set<AuthUser["role"]>(["Admin", "Doctor", "Radiology"])

function safeGet(key: string): string | null {
  try { return localStorage.getItem(key) } catch { return null }
}
function safeSet(key: string, value: string) {
  try { localStorage.setItem(key, value) } catch {
    console.warn("[auth] unable to persist auth state")
  }
}
function safeRemove(key: string) {
  try { localStorage.removeItem(key) } catch {
    console.warn("[auth] unable to clear auth state")
  }
}

export function saveAuth(token: string, user: AuthUser) {
  safeSet(TOKEN_KEY, token)
  safeSet(USER_KEY, JSON.stringify(user))
}

export function getToken() {
  return safeGet(TOKEN_KEY)
}

export function getUser(): AuthUser | null {
  const raw = safeGet(USER_KEY)
  if (!raw) return null
  try {
    const parsed = JSON.parse(raw) as Partial<AuthUser>

    if (
      typeof parsed.username === "string" &&
      typeof parsed.name === "string" &&
      parsed.role &&
      ROLES.has(parsed.role)
    ) {
      return parsed as AuthUser
    }
  } catch {
    // Invalid persisted auth state is handled below.
  }

  clearAuth()
  return null
}

export function clearAuth() {
  safeRemove(TOKEN_KEY)
  safeRemove(USER_KEY)
}

export function getAuthState() {
  const token = getToken()
  const user = getUser()

  if (token && user) {
    return { token, user }
  }

  if (token || user) {
    clearAuth()
  }

  return null
}
