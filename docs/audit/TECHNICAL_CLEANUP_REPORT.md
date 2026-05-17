# AI Hospital Alliance Technical Cleanup Report

Date: 2026-05-16

## Scope

Audited the web application boot path, routing, auth guard flow, TypeScript/JavaScript source duplication, lint scope, and production build behavior.

## Key Findings

- The repository contained generated JavaScript files beside TypeScript source files under `src/`.
- `tsc -b` was regenerating those stale `src/**/*.js` files because the root `tsconfig.json` did not set `noEmit`.
- `vite.config.js` was a generated duplicate of `vite.config.ts`, creating potential config drift.
- Stale service worker registration referenced `/sw.js`, while the current public assets do not provide that file.
- Auth guard logic only checked persisted token/user values directly and did not normalize corrupt partial auth state.
- Login always redirected to `/dashboard`, losing the originally requested protected route.
- Logout used full page reloads instead of router navigation.
- ESLint was scanning non-web snapshot/prototype areas (`mobile`, `backend`, `milestones`) with browser React rules, producing noisy failures unrelated to the production web build.

## Fixes Applied

- Removed stale generated JavaScript duplicates from `src/`.
- Removed stale JS backup folders:
  - `backup_js_conflicts/`
  - `backup_js_duplicates_20260510_1824/`
  - `backup_old_js_files/`
- Removed duplicate generated `vite.config.js`.
- Added `noEmit: true` to `tsconfig.json` so future builds do not recreate JS artifacts inside `src`.
- Kept Vite TypeScript-first module resolution in `vite.config.ts`.
- Replaced service worker registration with cleanup of existing stale registrations.
- Added a visible root mount failure if `#root` is missing.
- Added `getAuthState()` to validate persisted auth state and clear partial/corrupt credentials.
- Updated protected route redirects to preserve `pathname + search`.
- Updated login to return users to their originally requested route.
- Updated logout/sidebar logout to use React Router navigation instead of `window.location`.
- Updated API wrapper to clear auth on `401` and safely handle `204 No Content`.
- Wired previously unused patient profile actions:
  - Official report draft generation.
  - PACS opening from radiology orders.
- Cleaned stale imports, unused variables, and empty catch blocks in the web app.
- Scoped ESLint to production web sources and ignored non-web/generated/snapshot areas.

## Routing And Auth Notes

- `BrowserRouter` remains mounted once in `src/main.tsx`.
- Application routes remain centralized in `src/App.tsx`.
- Protected routes still wrap page components with `ProtectedRoute` and `AppLayout`.
- The previous dev proxy pattern for frontend route prefixes such as `/patients`, `/labs`, and `/ai` should not be restored in the frontend Vite config because it conflicts with BrowserRouter routes. Backend URLs should be supplied with `VITE_API_BASE_URL`.

## Validation

- `npm run lint`: passed.
- `npm run build`: passed.
- Verified no `src/**/*.js` files exist after build.
- Verified `vite.config.js` is not regenerated after build.

## Remaining Production Notes

- Build reports large chunks, especially `PatientProfilePage`. This is not a correctness failure, but future optimization should split heavy PDF/reporting dependencies and large page modules.
- Mobile/backend lint debt is outside the production web ESLint scope after this cleanup. They should have dedicated lint/typecheck configs if they are intended to be shipped independently.
