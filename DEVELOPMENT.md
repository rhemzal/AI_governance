# Development Guide

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Testing Quickstart

This section provides a concise reference for running tests in repositories that adopt this governance kit.

### Virtual Environment Setup

Before running tests, ensure you have a repository-local virtual environment:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -e .[dev]      # or pip install -r requirements-dev.txt
```

### Canonical Test Commands

Use these commands in order of preference:

1. **Make targets** (if available):
   ```bash
   make test              # Run all tests
   make test-unit         # Run unit tests only
   make test-integration  # Run integration tests only
   ```

2. **Repo-local virtual environment** (Python projects):
   ```bash
   .venv/bin/python -m pytest           # Run all tests
   .venv/bin/python -m pytest tests/    # Run specific directory
   .venv/bin/python -m pytest -v        # Verbose output
   ```

3. **Docker fallback** (if provided):
   ```bash
   docker compose run --rm test
   ```

### Important Notes

- **Never assume global pytest or global test runners.** Always use repo-local commands.
- **Check the project README or CONTRIBUTING.md** for project-specific test instructions.
- **Prefer make targets** when available—they provide a stable interface.

### For More Details

For detailed testing guidance, architecture gates, and enforcement principles, see:
- [usage/HOW_TO_USE_WITH_COPILOT.md](usage/HOW_TO_USE_WITH_COPILOT.md) — Test execution canonical path
- [ci/TEST_GATES.md](ci/TEST_GATES.md) — Test CI gates and principles
- [constitution/AI_ENFORCEMENT_DAILY.md](constitution/AI_ENFORCEMENT_DAILY.md) — Daily AI enforcement checklist
