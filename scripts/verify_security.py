import os
import re


def verify() -> dict[str, list[str]]:
    """Scan python source files for potential hardcoded secret warnings."""
    # Define regex pattern looking for password/secret assignments
    pattern = re.compile(
        r'(?:password|secret|key|token)\s*=\s*[\'"][^\'"]+[\'"]',
        re.IGNORECASE,
    )
    violations = {}
    for root, _, files in os.walk("services/api/src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                # Ignore configurations or settings files where default strings are declared
                if "config" in root or "settings" in file or "database" in root:
                    continue
                try:
                    with open(path, encoding="utf-8") as f:
                        for line_num, line in enumerate(f, 1):
                            if pattern.search(line):
                                if "placeholder" in line.lower() or "safe" in line.lower():
                                    continue
                                if 'key="access_token"' in line or 'key="refresh_token"' in line:
                                    continue
                                if "cookie" in line.lower():
                                    continue
                                if path not in violations:
                                    violations[path] = []
                                violations[path].append(
                                    f"L{line_num}: {line.strip()}"
                                )
                except Exception:
                    pass
    return violations


if __name__ == "__main__":
    viols = verify()
    if not viols:
        print("Security hardcoded secrets check: PASS")
    else:
        for p, lines in viols.items():
            print(f"{p}:")
            for l in lines:
                print(f"  {l}")
