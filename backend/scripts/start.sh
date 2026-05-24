#!/usr/bin/env sh
set -eu

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
WORKERS="${WEB_CONCURRENCY:-1}"

echo "[busgpt] Starting backend"
echo "[busgpt] host=${HOST} port=${PORT} workers=${WORKERS}"
echo "[busgpt] environment=${ENVIRONMENT:-unset}"
echo "[busgpt] python=$(python --version 2>&1)"

exec uvicorn app.main:app \
  --host "${HOST}" \
  --port "${PORT}" \
  --workers "${WORKERS}" \
  --proxy-headers \
  --forwarded-allow-ips "*"
