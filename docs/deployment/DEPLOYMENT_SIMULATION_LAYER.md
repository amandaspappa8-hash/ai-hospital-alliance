# Deployment Simulation Layer

## Goal
Run AI Hospital Assistant Alliance locally in a production-like mode.

## What this layer adds
- frontend production build
- static frontend hosting on port 4173
- backend production-like startup on port 8000
- smoke test script
- deployment run scripts

## Scripts
- `scripts/run-prod-backend.sh`
- `scripts/run-prod-frontend.sh`
- `scripts/run-prod-stack.sh`
- `scripts/prod-smoke-test.sh`

## Local Production Simulation
### Backend
Runs on:
- `http://127.0.0.1:8000`

### Frontend
Served from `dist/` on:
- `http://127.0.0.1:4173`

## Production-like Environment
Frontend:
- `VITE_API_BASE_URL=http://127.0.0.1:8000`
- `VITE_APP_ENV=production`

Backend:
- `APP_ENV=production`
- `ENABLE_DOCS=false`

## Acceptance Criteria
- frontend builds successfully
- backend starts on port 8000
- frontend served from dist on port 4173
- `/health` works
- `/ready` works
- login works
- smoke test passes
