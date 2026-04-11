#!/usr/bin/env bash
set -e

echo "======================================"
echo "AI Hospital - Production Readiness Check"
echo "======================================"

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo
echo "[1/6] Frontend install check"
test -f package.json && echo "OK: package.json found"

echo
echo "[2/6] Frontend build"
npm run build

echo
echo "[3/6] Backend entry check"
test -f backend/app/main.py && echo "OK: backend/app/main.py found"

echo
echo "[4/6] Required docs check"
test -f docs/production/PRODUCTION_READINESS_LAYER.md && echo "OK: readiness doc found"

echo
echo "[5/6] Environment sample check"
test -f .env.example && echo "OK: .env.example found" || echo "WARN: .env.example missing"

echo
echo "[6/6] Quick route grep"
grep -n 'health\|ready' backend/app/main.py backend/app/api/health.py 2>/dev/null || true

echo
echo "Readiness check completed."
