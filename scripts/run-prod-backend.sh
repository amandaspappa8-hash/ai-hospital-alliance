#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

source venv/bin/activate

export APP_ENV=production
export APP_NAME="AI Hospital Assistant API"
export ENABLE_DOCS=false
export LOG_LEVEL=info
export CORS_ORIGINS="http://127.0.0.1:4173,http://localhost:4173"

exec uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
