# LeadScan AI Deployment Checklist

Step-by-step guide for deploying LeadScan AI onto production Kubernetes clusters.

---

## Pre-Deployment Verification
- [ ] Run test suite locally: `pytest tests/` and verify all tests pass.
- [ ] Verify Docker images compile: `bash scripts/build.sh`.
- [ ] Verify Kubernetes YAML configs for syntax errors.

## Execution Steps
1. **Apply Namespace**:
   ```bash
   kubectl apply -f kubernetes/namespace.yaml
   ```
2. **Apply ConfigMaps & Secrets**:
   - Ensure you encode connection strings to base64.
   ```bash
   kubectl apply -f kubernetes/configmap.yaml
   kubectl apply -f kubernetes/secret.example.yaml
   ```
3. **Apply Services & Ingress**:
   ```bash
   kubectl apply -f kubernetes/service.yaml
   kubectl apply -f kubernetes/ingress.yaml
   ```
4. **Deploy Pods**:
   ```bash
   kubectl apply -f kubernetes/deployment-api.yaml
   kubectl apply -f kubernetes/deployment-worker.yaml
   kubectl apply -f kubernetes/deployment-ocr.yaml
   ```
5. **Apply Autoscaling & Policies**:
   ```bash
   kubectl apply -f kubernetes/hpa.yaml
   kubectl apply -f kubernetes/network-policy.yaml
   ```
