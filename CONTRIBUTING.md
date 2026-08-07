# Contributing to LeadScan AI

Thank you for contributing to LeadScan AI. As an enterprise project, we adhere to strict quality standards, clean architectures, and disciplined branching workflows.

## Development Workflow

### Branching Model

- Main Branch: `main` (production-ready).
- Working branches should be named as:
  - `feature/issue-id-short-description`
  - `bugfix/issue-id-short-description`
  - `chore/issue-id-short-description`

### Pull Request Guidelines

1. Open an issue describing the bug or feature request before creating a PR.
2. Ensure your branch is updated with `main` before submitting.
3. Make sure all linters, checkers, and tests pass locally.
4. Fill out the [Pull Request Template](file:///e:/Antigravity/.github/PULL_REQUEST_TEMPLATE.md) completely.
5. Code must be reviewed by at least one maintainer (matching [CODEOWNERS](file:///e:/Antigravity/.github/CODEOWNERS)).

## Coding Style Rules

### Naming Conventions

- **Python:** `snake_case` for variables and functions, `PascalCase` for classes, `UPPER_CASE` for constants.
- **React/TypeScript:** `PascalCase` for components, `camelCase` for variables and functions.
- **Directories & Files:** `kebab-case` for folder and configuration files (with exceptions for standard configurations).

### Linting and Formatting

All changes must pass local validations. Please run:
- Python formatting: `ruff format .`
- Python linting: `ruff check .`
- TypeScript static verification: `pnpm type-check`
- JS/TS formatting: `pnpm format`
- JS/TS linting: `pnpm lint`
