#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

cat > .env.production <<'ENVEOF'
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_APP_ENV=production
VITE_ENABLE_MONITORING=false
ENVEOF

npm run build
python3 -m http.server 4173 --directory dist
