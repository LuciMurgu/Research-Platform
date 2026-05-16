# Roadmap

> **This roadmap defines phases, not deadlines.** Each phase builds on the previous one. A phase is complete when its acceptance criteria are met and its architecture tests pass.

---

## Phase 0 — Foundation

Establish the project constitution, repository skeleton, architecture documentation, and development tooling.

**Includes:**

- Project charter (README, AGENTS.md, Cursor rules)
- Repository directory structure
- Architecture and data model documentation
- Development environment setup (Python, Node, linting, formatting)
- CI skeleton (lint, type-check, architecture boundary tests)
- Base Pydantic schemas for core domain types

**Does not include:** Runnable compute, API, or frontend.

---

## Phase 1 — Mandelbrot vertical slice

Build a complete end-to-end path from command to artifact for a single compute kernel: the Mandelbrot set.

**Includes:**

- Mandelbrot compute kernel (pure, deterministic, tested)
- Parameter schema for Mandelbrot generation
- Orchestrator that invokes the kernel and stores results
- Content-addressed artifact storage (write and verify)
- Provenance event emission for the run
- Minimal API endpoint to submit a Mandelbrot command and retrieve results
- Minimal CLI command to run a Mandelbrot computation
- Basic test coverage: kernel unit tests, orchestrator integration test

**Does not include:** Frontend, experiment registry, or agent features.

---

## Phase 2 — Experiment registry and replay

Add the ability to register experiments, record runs, and replay past computations.

**Includes:**

- SQLite-backed experiment and run registry
- Run metadata storage (parameters, status, timestamps)
- Artifact linking (runs → artifacts via content hash)
- Provenance ledger (append-only event log)
- Query API for experiments, runs, and lineage
- Replay: re-run a past computation with identical parameters and verify output matches

**Does not include:** Frontend or new compute kernels.

---

## Phase 3 — Dynamics

Add compute kernels for nonlinear dynamical systems and chaos.

**Includes:**

- Logistic map kernel
- Hénon map kernel
- Lorenz system kernel (ODE integration)
- Bifurcation diagram generation
- Lyapunov exponent estimation
- StateFrame capture for intermediate iteration states
- Metrics: convergence, periodicity, divergence detection
- Warnings: numerical precision loss, parameter boundary proximity

---

## Phase 4 — Geometry

Add compute kernels for higher-dimensional geometry and fractal analysis.

**Includes:**

- Julia set kernel (generalized)
- IFS (Iterated Function System) kernel
- Fractal dimension estimation (box-counting, correlation dimension)
- 3D fractal generation (Mandelbulb or similar)
- Higher-dimensional projection and slicing utilities
- Three.js adapter for 3D rendering (adapter, not core dependency)

---

## Phase 5 — Visual graphs

Build the frontend and graph-based visualization layer.

**Includes:**

- React/TypeScript frontend shell
- Pipeline graph visualization (React Flow)
- Provenance/lineage graph visualization
- Artifact viewer (images, data tables, 3D renders)
- Experiment browser and run comparison
- StateFrame inspector (step through intermediate computation states)

---

## Phase 6 — Read-only agents

Add AI agent integration as a read-only assistant layer.

**Includes:**

- Agent context reader (approved read-only access to runs, artifacts, metrics)
- Explanation generation (labeled as agent output, not scientific fact)
- Suggested command generation (requires researcher approval)
- Approval workflow with provenance recording
- Agent output labeling and display in the frontend

**Constraints:**

- Agents must not mutate experiments, artifacts, or provenance.
- Agent outputs are always labeled as suggestions/explanations.
- No autonomous execution — researcher approves every action.

---

## Phase 7 — Optional advanced adapters

Add optional adapters for high-performance and specialized use cases.

**May include:**

- Julia bridge for numerically intensive kernels
- GPU compute adapter (CUDA/OpenCL)
- Advanced visualization adapters
- Export adapters (PDF reports, data packages)
- Backup and restore tooling

**Constraints:**

- These are adapters, not core dependencies.
- Removing an adapter must not break the core platform.
- Each adapter must be independently testable.
