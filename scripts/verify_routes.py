import os


def verify() -> dict[str, str]:
    """Verify that routing files contain expected router instances."""
    errors = {}
    for root, _, files in os.walk("services/api/src"):
        for file in files:
            if file == "router.py":
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()
                    if "APIRouter(" not in content:
                        errors[path] = "APIRouter instance is missing"
                except Exception as exc:
                    errors[path] = str(exc)
    return errors


if __name__ == "__main__":
    errs = verify()
    if not errs:
        print("Routes check: PASS")
    else:
        for p, err in errs.items():
            print(f"{p}: {err}")
