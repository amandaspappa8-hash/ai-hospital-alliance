#!/usr/bin/env bash
set -e

echo "======================================"
echo "AI Hospital - Production Smoke Test"
echo "======================================"

echo
echo "[1/5] Backend /health"
curl -fsS http://127.0.0.1:8000/health && echo

echo
echo "[2/5] Backend /ready"
curl -fsS http://127.0.0.1:8000/ready && echo

echo
echo "[3/5] Auth login"
curl -fsS -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' && echo

echo
echo "[4/5] Patients"
curl -fsS http://127.0.0.1:8000/patients > /tmp/aiha_patients.json
python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path("/tmp/aiha_patients.json").read_text())
print(f"patients_count={len(data) if isinstance(data, list) else 'unknown'}")
PY

echo
echo "[5/5] Frontend availability"
curl -I http://127.0.0.1:4173 | head -n 5

echo
echo "Smoke test completed successfully."
