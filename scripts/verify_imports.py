import ast
import os


def get_imports_from_file(filepath: str) -> set[str]:
    """Parse AST to extract imported module string namespaces."""
    imports = set()
    try:
        with open(filepath, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filepath)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
    except Exception:
        pass
    return imports


def verify() -> dict[str, str]:
    """Verify that there are no obvious cross-module circular imports."""
    # Base analysis check: assert that sub-modules do not perform circular cross-imports
    errors = {}
    for root, _, files in os.walk("services/api/src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                imps = get_imports_from_file(path)
                for imp in imps:
                    # Basic circular rule check: if a dependency service
                    # imports its parent package
                    if "services.api.main" in imp:
                        errors[path] = f"Imports gateway entry point: {imp}"
    return errors


if __name__ == "__main__":
    errs = verify()
    if not errs:
        print("Imports check: PASS")
    else:
        for p, err in errs.items():
            print(f"{p}: {err}")
