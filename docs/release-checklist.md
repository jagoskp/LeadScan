# LeadScan AI Release Checklist

Instructions for tagging and releasing new platform versions.

---

## 1. Version Tagging
- Follow Semantic Versioning rules: `vMAJOR.MINOR.PATCH`.
- Ensure changes are merged to the `main` branch.
- Generate version tags via git:
  ```bash
  git tag -a v1.0.0 -m "Release version 1.0.0"
  git push origin v1.0.0
  ```

## 2. Release Audits
- [ ] Run `python scripts/verify_project.py` and verify all tests pass.
- [ ] Generate database migrations: `alembic revision --autogenerate`.
- [ ] Run database migration upgrades: `alembic upgrade head`.
- [ ] Verify that liveness/readiness probes respond with 200 OK.
