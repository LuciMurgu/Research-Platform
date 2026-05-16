# Workbench API

Backend package for the Research Workbench.

> **Status: Skeleton only.** No routes, no compute, no storage implementation. This package exists to establish the module structure and dependency boundaries.

## Package structure

```
src/workbench/
├── api/            # FastAPI routes (calls application services only)
├── application/    # CommandBus, query handlers (calls orchestrators)
├── modules/        # Domain orchestrators (calls compute, storage, provenance)
├── compute/        # Deterministic compute kernels (pure, no imports from other layers)
├── core/           # Shared domain types and constants
├── storage/        # Persistence adapters (filesystem, SQLite)
├── provenance/     # Append-only provenance ledger
├── agents/         # Read-only agent side-channel (never mutates scientific records)
├── observability/  # Logging, metrics, health checks
└── main.py         # FastAPI application entry point
```

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/ tests/
```
