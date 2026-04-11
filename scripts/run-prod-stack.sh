#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "======================================"
echo "AI Hospital - Production Simulation"
echo "======================================"

if [ ! -d "venv" ]; then
  echo "ERROR: venv not found"
  exit 1
fi

if [ ! -f "package.json" ]; then
  echo "ERROR: package.json not found"
  exit 1
fi

echo
echo "[1/4] Building frontend for production..."
cat > .env.production <<'ENVEOF'
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_APP_ENV=production
VITE_ENABLE_MONITORING=false
ENVEOF
npm run build

echo
echo "[2/4] Stopping old local servers if any..."
pkill -f "http.server 4173" || true
pkill -f "uvicorn backend.app.main:app --host 127.0.0.1 --port 8000" || true

echo
echo "[3/4] Starting backend..."
gnome-terminal -- bash -lc "cd '$ROOT' && source venv/bin/activate && APP_ENV=production APP_NAME='AI Hospital Assistant API' ENABLE_DOCS=false LOG_LEVEL=info CORS_ORIGINS='http://127.0.0.1:4173,http://localhost:4173' uvicorn backend.app.main:app --host 127.0.0.1 --port 8000; exec bash" >/dev/null 2>&1 || true

echo
echo "[4/4] Starting frontend static server..."
gnome-terminal -- bash -lc "cd '$ROOT' && python3 -m http.server 4173 --directory dist; exec bash" >/dev/null 2>&1 || true

echo
echo "Open:"
echo "  Frontend: http://127.0.0.1:4173"
echo "  Backend : http://127.0.0.1:8000/health"
