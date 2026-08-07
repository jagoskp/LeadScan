import os


def verify() -> dict[str, bool]:
    """Verify that required environment templates and configuration sources exist."""
    targets = [
        ".env.example",
        ".env.development.example",
        ".env.testing.example",
        ".env.staging.example",
        ".env.production.example",
        "services/api/src/config/loader.py",
        "services/api/src/config/base.py",
    ]
    res = {}
    for t in targets:
        res[t] = os.path.exists(t)
    return res


if __name__ == "__main__":
    results = verify()
    for path, exists in results.items():
        print(f"{path}: {'PASS' if exists else 'FAIL'}")
