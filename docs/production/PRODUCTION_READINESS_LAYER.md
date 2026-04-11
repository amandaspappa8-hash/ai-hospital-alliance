# Production Readiness Layer

## Goal
Prepare AI Hospital Assistant Alliance for staging/production deployment with:
- health checks
- env validation
- API/frontend readiness checks
- error monitoring hooks
- deployment checklist

---

## Readiness Areas

### 1) Frontend
- Production build passes
- No critical TypeScript errors
- API base URL configurable
- Global error boundary exists
- Monitoring hook exists

### 2) Backend
- `/health` endpoint
- `/ready` endpoint
- CORS controlled by env
- Required env vars validated at startup
- OpenAPI available in non-production only if desired

### 3) Deployment
- `.env.example` present
- startup check script present
- production checklist documented

### 4) Monitoring
- frontend monitoring hook
- backend logging baseline
- request failure visibility

---

## Acceptance Criteria
- `npm run build` passes
- backend starts with validated env
- `GET /health` returns service status
- `GET /ready` returns readiness payload
- frontend has production-safe API base config
- readiness script runs successfully

---

## Files Added
- `docs/production/PRODUCTION_READINESS_LAYER.md`
- `scripts/readiness-check.sh`
- `src/lib/env.ts`
- `src/lib/monitoring.ts`
- `backend/app/api/health.py`

