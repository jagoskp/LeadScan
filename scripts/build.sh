#!/usr/bin/env bash
# Script to build LeadScan AI Docker images locally
set -euo pipefail

TAG=${1:-latest}

echo "==========================================="
echo "Building LeadScan AI Docker Images (Tag: ${TAG})"
echo "==========================================="

echo "1. Building api image..."
docker build -t leadscan-api:"${TAG}" -f docker/api.Dockerfile .

echo "2. Building worker image..."
docker build -t leadscan-worker:"${TAG}" -f docker/worker.Dockerfile .

echo "3. Building ocr image..."
docker build -t leadscan-ocr:"${TAG}" -f docker/ocr.Dockerfile .

echo "==========================================="
echo "Builds completed successfully!"
echo "==========================================="
