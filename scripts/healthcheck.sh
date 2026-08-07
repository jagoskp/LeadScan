#!/usr/bin/env bash
# Script to verify health check liveness and readiness response codes
set -euo pipefail

TARGET_URL=${1:-"http://localhost:8000"}

echo "==========================================="
echo "Verifying Health Check probes on: ${TARGET_URL}"
echo "==========================================="

echo "1. Checking liveness probe..."
LIVE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${TARGET_URL}/health/live" || echo "000")
if [ "${LIVE_STATUS}" -eq 200 ]; then
    echo "Liveness: PASS (200 OK)"
else
    echo "Liveness: FAIL (${LIVE_STATUS})"
    exit 1
fi

echo "2. Checking readiness probe..."
READY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${TARGET_URL}/health/ready" || echo "000")
if [ "${READY_STATUS}" -eq 200 ]; then
    echo "Readiness: PASS (200 OK)"
else
    echo "Readiness: FAIL (${READY_STATUS})"
    exit 1
fi

echo "==========================================="
echo "All health diagnostics passed!"
echo "==========================================="
