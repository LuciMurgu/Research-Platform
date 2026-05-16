# Architecture

## Overview

The Research Workbench is a **local-first modular monolith**. All layers run on the researcher's machine. The system is organized as a set of modules with strict dependency boundaries — not as separate deployable services.

The researcher remains in control at every step. The platform records, computes, and presents — it does not decide.

---

## Layering

All code respects a single dependency direction:

```
UI → API → CommandBus → Orchestrators → Compute Kernels → Storage / Provenance
```

### Layer responsibilities

| Layer | Role | May call |
|-------|------|----------|
| **UI** (React/TS) | Present research state, accept researcher input | API only |
| **API** (FastAPI) | Accept commands, serve queries, enforce auth/validation | CommandBus, query handlers |
| **CommandBus** | Dispatch validated commands to the correct orchestrator | Orchestrators |
| **Orchestrators** | Coordinate multi-step research workflows | Compute ports, validators, repositories, artifact store, provenance ledger |
| **Compute Kernels** | Execute deterministic scientific computation | Nothing — pure functions in, results out |
| **Storage / Provenance** | Persist experiments, artifacts, metrics, provenance | Filesystem, SQLite |

### What each layer must NOT do

- **UI** must not import backend modules.
- **API** must not contain scientific computation logic.
- **Compute kernels** must not import API, storage adapters, or agent modules.
- **Agents** must not mutate experiments, artifacts, provenance, or code.

---

## Three graphs

The platform works with three distinct graph structures. They are related but not the same.

### 1. Architecture graph

The static dependency structure of the codebase. Defined above. Enforced by import rules and architecture tests.

**Purpose:** Ensure modules remain decoupled and boundaries are respected.

### 2. Pipeline graph

A directed acyclic graph (DAG) of compute steps within a single run.

```
Parameters → Kernel A → StateFrames → Kernel B → Artifacts → Metrics
```

**Purpose:** Define how a computation flows from input parameters to output artifacts within one execution.

### 3. Provenance / lineage graph

A historical graph connecting runs, experiments, artifacts, and hypotheses across time.

```
Experiment → Run 1 → Artifacts → (used by) → Run 2 → Artifacts → ...
```

**Purpose:** Answer "where did this result come from?" and "what was tried before?"

---

## Key roles

### Orchestrators execute

Orchestrators coordinate the pipeline graph. They call compute kernels through ports, collect results, store artifacts, emit provenance events, and report metrics and warnings.

Orchestrators do not compute scientific results directly. They delegate to kernels.

### Compute kernels produce truth-bearing results

Kernels are deterministic, pure functions. Given identical parameters, they produce identical results. They have no side effects, no network access, and no awareness of the platform infrastructure around them.

The results of deterministic kernels — together with saved parameters, content-hashed artifacts, and provenance records — constitute the platform's scientific truth.

### Agents assist

Agents (LLM-powered or otherwise) may read approved context and produce labeled suggestions, explanations, or summaries. They are assistants, not authorities.

- Agent output is always **labeled** — never presented as validated scientific fact.
- Agents never mutate experiments, artifacts, code, or provenance.
- Agents occupy a **side channel**. They are not part of the main data path.

### Provenance records what happened

Every experiment-producing operation emits provenance events. These events form the lineage graph. They record:

- What was run, with which parameters.
- What artifacts were produced, with content hashes.
- What metrics and warnings were generated.
- What the researcher approved or rejected.

Provenance is append-only for finished runs. It cannot be silently altered.

### The researcher remains in control

The platform does not make autonomous decisions about research direction. It presents evidence, records history, and surfaces suggestions — but the researcher decides what to run, what to trust, and what to pursue next.

---

## External tools are adapters

Technologies like Julia, Three.js, React Flow, or future visualization libraries are accessed through adapter interfaces — not imported as core dependencies.

If an adapter is removed, the core platform continues to function. Adapters extend capability; they do not define architecture.
