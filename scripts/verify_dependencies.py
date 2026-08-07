import os

from scripts.verify_imports import get_imports_from_file


def verify() -> dict[str, str]:
    """Verify that repositories do not depend on services.

    Enforces Clean Architecture.
    """
    violations = {}
    for root, _, files in os.walk("services/api/src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                # Enforce rule: repository layers should never import service layers
                if "repository.py" in file:
                    imps = get_imports_from_file(path)
                    for imp in imps:
                        if ".service" in imp or "Service" in imp:
                            violations[path] = (
                                f"Repository imports service layer: {imp}"
                            )
    return violations


if __name__ == "__main__":
    viols = verify()
    if not viols:
        print("Dependency layers check: PASS")
    else:
        for p, v in viols.items():
            print(f"{p}: {v}")
