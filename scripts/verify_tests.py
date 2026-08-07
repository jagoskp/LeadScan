import os


def verify() -> dict[str, int]:
    """Verify test suite file structure and return files count."""
    res = {}
    for d in os.listdir("tests"):
        path = os.path.join("tests", d)
        if os.path.isdir(path):
            count = len(
                [f for f in os.listdir(path) if f.startswith("test_")]
            )
            res[d] = count
    return res


if __name__ == "__main__":
    test_counts = verify()
    for suite, count in test_counts.items():
        print(f"Suite '{suite}': {count} test files")
