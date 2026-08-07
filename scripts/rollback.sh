#!/usr/bin/env bash
# Script to roll back deployments to the previous stable state
set -euo pipefail

NAMESPACE="leadscan"

echo "==========================================="
echo "Rolling back LeadScan AI Deployments"
echo "==========================================="

echo "1. Rolling back API Deployment..."
kubectl rollout undo deployment/leadscan-api -n "${NAMESPACE}"

echo "2. Rolling back Background Worker Deployment..."
kubectl rollout undo deployment/leadscan-worker -n "${NAMESPACE}"

echo "3. Rolling back OCR Worker Deployment..."
kubectl rollout undo deployment/leadscan-ocr -n "${NAMESPACE}"

echo "==========================================="
echo "Rollback initiated. Check statuses with: kubectl rollout status -n ${NAMESPACE}"
echo "==========================================="
