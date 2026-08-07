import os
import sys

# Append the project root to python path to resolve scripts imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import (
    verify_configs,
    verify_dependencies,
    verify_docs,
    verify_imports,
    verify_routes,
    verify_security,
    verify_structure,
    verify_tests,
)


def run_audit() -> int:
    """Run all verifications and print aggregate audit results."""
    print("==================================================")
    print("LeadScan AI final enterprise readiness audit")
    print("==================================================")

    # 1. Structure
    struct_res = verify_structure.verify()
    struct_ok = all(struct_res.values())
    print(f"Structure verification: {'PASS' if struct_ok else 'FAIL'}")

    # 2. Imports
    import_errs = verify_imports.verify()
    imports_ok = len(import_errs) == 0
    print(f"Imports verification: {'PASS' if imports_ok else 'FAIL'}")

    # 3. Dependencies
    dep_viols = verify_dependencies.verify()
    deps_ok = len(dep_viols) == 0
    print(f"Dependencies layering: {'PASS' if deps_ok else 'FAIL'}")

    # 4. Configs
    config_res = verify_configs.verify()
    configs_ok = all(config_res.values())
    print(f"Configuration templates: {'PASS' if configs_ok else 'FAIL'}")

    # 5. Routes
    route_errs = verify_routes.verify()
    routes_ok = len(route_errs) == 0
    print(f"Router APIRouter instances: {'PASS' if routes_ok else 'FAIL'}")

    # 6. Tests
    test_res = verify_tests.verify()
    print(f"Test suites verified: {len(test_res)} directories mapped.")

    # 7. Docs
    doc_res = verify_docs.verify()
    docs_ok = all(doc_res.values())
    print(f"Documentation files: {'PASS' if docs_ok else 'FAIL'}")

    # 8. Security
    sec_viols = verify_security.verify()
    sec_ok = len(sec_viols) == 0
    print(f"Hardcoded secrets scan: {'PASS' if sec_ok else 'FAIL'}")

    success = (
        struct_ok
        and imports_ok
        and deps_ok
        and configs_ok
        and routes_ok
        and docs_ok
        and sec_ok
    )

    print("==================================================")
    if success:
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("AUDIT DETECTED GAPS OR VIOLATIONS.")
        return 1


if __name__ == "__main__":
    sys.exit(run_audit())
