# Auth Contract

## Purpose
Provide a shared authentication and authorization contract for:
- Web
- App
- Platform/API
- Roles/Permissions
- Future database-backed auth

## Login Endpoint
- Method: POST
- Path: /auth/login

## Request
```json
{
  "username": "admin",
  "password": "admin123"
}
BOF
