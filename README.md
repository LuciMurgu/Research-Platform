# Research Workbench

A local-first scientific visual research workbench for exploring fractal geometry, nonlinear dynamical systems, chaos, higher-dimensional geometry, and — eventually — biological morphogenesis simulations.

> **Status: Early development.**  
> The project is in its constitution phase. No runnable code exists yet. The documents in this repository define the mission, architecture boundaries, and agent-safety rules that will govern all future implementation.

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

The following technologies are planned but **not yet added** — no dependencies exist today.

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

---

## Local-first

All computation, storage, and provenance run on the researcher's own machine. No cloud account is required. No data leaves the local environment unless the researcher explicitly chooses to export it.

---

## License

TBD.
