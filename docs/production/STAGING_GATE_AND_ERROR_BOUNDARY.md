# Staging Gate and Error Boundary

## Goal
Add frontend protection and deployment awareness through:
- React Error Boundary
- Environment Gate
- Staging Banner

## Components
- `src/components/system/ErrorBoundary.tsx`
- `src/components/system/EnvGate.tsx`
- `src/components/system/StagingBanner.tsx`

## Behavior

### ErrorBoundary
Catches React rendering/runtime UI errors and shows a safe fallback screen.

### EnvGate
Validates frontend environment variables.
- In production: blocks unsafe startup when env is invalid
- In non-production: logs warnings and allows startup

### StagingBanner
Displays a visible banner when:
- `VITE_APP_ENV=staging`

## Acceptance Criteria
- UI does not fully white-screen on React component crash
- staging banner appears only in staging
- invalid production env is blocked by EnvGate
