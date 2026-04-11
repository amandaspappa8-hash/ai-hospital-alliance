# Dockerization + Nginx Reverse Proxy Layer

## Goal
Run AI Hospital Assistant Alliance as containerized services behind Nginx.

## Services
- backend (FastAPI)
- frontend (Vite build served by nginx)
- nginx reverse proxy

## Ports
- Nginx: 80
- Backend internal: 8000
- Frontend internal: 80

## Routing
- `/` -> frontend
- `/api/*` -> backend
- `/health` -> backend health
- `/ready` -> backend readiness

## Files
- `backend/Dockerfile`
- `Dockerfile.frontend`
- `docker-compose.yml`
- `deploy/nginx/nginx.conf`
- `.dockerignore`

## Acceptance Criteria
- `docker compose up --build` succeeds
- opening `http://127.0.0.1` loads frontend
- `http://127.0.0.1/health` works
- login works through `/api/auth/login`
