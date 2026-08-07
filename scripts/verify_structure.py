import os


def verify() -> dict[str, bool]:
    """Verify that required workspace directories and package structures exist."""
    targets = [
        "services/api/src/auth",
        "services/api/src/users",
        "services/api/src/organization",
        "services/api/src/documents",
        "services/api/src/ocr",
        "services/api/src/ai",
        "services/api/src/workflow",
        "services/api/src/search",
        "services/api/src/reports",
        "services/api/src/notifications",
        "services/api/src/audit",
        "services/api/src/storage",
        "services/api/src/integration",
        "services/api/src/database",
        "services/api/src/config",
        "services/api/src/monitoring",
        "services/worker/src",
        "kubernetes",
        "docker",
        "scripts",
    ]
    res = {}
    for t in targets:
        res[t] = os.path.exists(t)
    return res


if __name__ == "__main__":
    results = verify()
    for path, exists in results.items():
        print(f"{path}: {'PASS' if exists else 'FAIL'}")
