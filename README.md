# Research Workbench

A local-first scientific visual research workbench for exploring fractal geometry, nonlinear dynamical systems, chaos, higher-dimensional geometry, and — eventually — biological morphogenesis simulations.

> **Status: early foundation phase.**  
> The project has completed its constitution and initial repository skeleton.  

### Current implemented pieces:
- project constitution
- repository skeleton
- architecture docs
- backend package skeleton
- local FastAPI health endpoint
- pytest/Ruff setup
- architecture boundary test skeleton

### Not yet implemented:
- core schemas
- CommandBus
- experiment registry
- artifact store
- provenance ledger
- CLI
- compute kernels
- frontend UI
- agents
- Julia bridge
- MLflow/DVC/Prefect/Dagster adapters

---

## Purpose

This platform helps a single researcher understand mathematical processes across three levels:

1. **Intermediate state** — inspect any frame of a running computation.
2. **Whole process** — see how a system evolves from parameters to final artifacts.
3. **Research history** — trace lineage across experiments, compare runs, and build on prior work.

### Core epistemic rule

The platform must never confuse **visualization**, **explanation**, **hypothesis**, and **proof**.

- A visualization shows data; it does not validate a claim.
- An explanation narrates a process; it does not prove correctness.
- A hypothesis proposes a relationship; it is not evidence.
- Proof or validation requires explicit, reproducible evidence grounded in deterministic computation.

### Architectural truth rule

Deterministic computation, saved parameters, artifacts, metrics, warnings, and provenance are the source of scientific truth.

AI agents may assist, explain, summarize, and suggest — but they do not produce scientific truth by themselves.

---

## The core chain

Every research act flows through a single chain:

```
idea → command → parameters → job → pipeline → StateFrames
  → artifacts → metrics → warnings → provenance
  → explanation → lineage → new hypothesis
```

Each link is recorded. Nothing is thrown away silently.

---

## Planned stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend API | Python / FastAPI | Command ingestion, job management, provenance queries |
| Frontend | React / TypeScript | Visual research interface |
| Registry | SQLite | Experiment, run, and artifact metadata |
| Artifact storage | Content-addressed store | Immutable, hash-verified research outputs |
| Schemas | Pydantic | Strict domain models for commands, parameters, results |
| CLI | Python CLI | Headless operation and scripting |
| Graph UI | React Flow | Pipeline and lineage visualization |
| 3D rendering | Three.js | Fractal and higher-dimensional geometry visualization |
| High-performance compute | Julia bridge | Numerically intensive kernels (optional, later) |
| Morphogenesis | TBD | Optional later morphogenesis module, limited to mathematical/computational pattern-formation models and not part of the MVP. Must not introduce heavy external engines, medical claims, biological truth claims, or speculative interpretations without explicit future approval. |

---

## Local-first

All computation, storage, and provenance run on the researcher's own machine. No cloud account is required. No data leaves the local environment unless the researcher explicitly chooses to export it.

---

## License

TBD.
