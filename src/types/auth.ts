export type UserRole = "Admin" | "Doctor" | "Radiology"

export interface AuthUser {
  username: string
  name: string
  role: UserRole
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: AuthUser
}
