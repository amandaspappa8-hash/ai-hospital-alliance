import type { AuthUser } from "@/types/auth"

const TOKEN_KEY = "aiha_token"
const USER_KEY = "aiha_user"

function safeGet(key: string): string | null {
  try { return localStorage.getItem(key) } catch { return null }
}
function safeSet(key: string, value: string) {
  try { localStorage.setItem(key, value) } catch {}
}
function safeRemove(key: string) {
  try { localStorage.removeItem(key) } catch {}
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
  try { return JSON.parse(raw) as AuthUser } catch { return null }
}

export function clearAuth() {
  safeRemove(TOKEN_KEY)
  safeRemove(USER_KEY)
}
