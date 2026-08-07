#!/usr/bin/env bash
# Script to deploy LeadScan AI manifests onto a Kubernetes cluster
set -euo pipefail

NAMESPACE="leadscan"

echo "==========================================="
echo "Deploying LeadScan AI onto Kubernetes"
echo "==========================================="

echo "1. Asserting namespace exists..."
kubectl apply -f kubernetes/namespace.yaml

echo "2. Applying configmaps and secrets templates..."
kubectl apply -f kubernetes/configmap.yaml
if ! kubectl get secret leadscan-secrets -n "${NAMESPACE}" >/dev/null 2>&1; then
    echo "WARNING: leadscan-secrets not found. Applying secret.example.yaml placeholder..."
    kubectl apply -f kubernetes/secret.example.yaml
fi

echo "3. Applying services and ingress..."
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml

echo "4. Deploying core components..."
kubectl apply -f kubernetes/deployment-api.yaml
kubectl apply -f kubernetes/deployment-worker.yaml
kubectl apply -f kubernetes/deployment-ocr.yaml

echo "5. Applying horizontal autoscalers and policies..."
kubectl apply -f kubernetes/hpa.yaml
kubectl apply -f kubernetes/network-policy.yaml

echo "==========================================="
echo "Deployments applied. Check statuses with: kubectl get pods -n ${NAMESPACE}"
echo "==========================================="
