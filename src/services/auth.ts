import { apiPost } from "@/lib/api"
import type { AuthUser } from "@/types/auth"

type LoginResult = {
  access_token: string
  user: AuthUser
}

export async function login(username: string, password: string): Promise<LoginResult> {
  const data = await apiPost<string | { access_token?: string; token?: string; user?: AuthUser }>(
    "/auth/dev-login",
    { username, password }
  )


  const token =
    typeof data === "string"
      ? data
      : data?.access_token || data?.token || ""

  if (!token) {
    throw new Error("Login succeeded but the backend did not return a valid access token")
  }

  return {
    access_token: token,
    user: {
      username,
      role: username === "admin" ? "Admin" : "Doctor",
      name: username,
    } as AuthUser,
  }
}
