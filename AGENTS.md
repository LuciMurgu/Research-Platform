# AGENTS.md — Coding Agent Constitution

This file contains strict, non-negotiable instructions for any coding agent (LLM, copilot, or automated system) working on this repository.

**Read this file completely before writing any code.**

---

## 1. Project mission

Build a local-first scientific visual research workbench for fractal geometry, nonlinear dynamical systems, chaos, higher-dimensional geometry, and optional morphogenesis simulations.

The platform serves a single researcher. It must help them understand mathematical processes at the level of intermediate state, whole process, and research history.

---

## 2. Non-negotiable architecture rules

### Layering

All code must respect this dependency direction:

```
UI → API → CommandBus → Orchestrators → Compute Kernels → Storage / Provenance
```

- **UI** may call the **API**.
- **API** may call **application services** (CommandBus, query handlers).
- **Application services** may call **orchestrators**.
- **Orchestrators** may call **compute ports**, **validators**, **repositories**, **artifact store**, and **provenance ledger**.
- **Compute kernels** must be deterministic and isolated. They receive parameters and return results. Nothing else.
- **Agents** may only read approved context and write labeled suggestions or explanations. They occupy a side channel — never the main data path.

### Forbidden dependencies

| From | Must NOT import | Reason |
|------|----------------|--------|
| Compute kernels | API modules | Compute must remain pure and portable |
| Compute kernels | Agent modules | Compute must not depend on AI assistance |
| Compute kernels | Storage adapters | Compute receives data via ports, not direct DB access |
| Frontend | Backend modules | Frontend communicates only via API |
| Agents | — (must not mutate) | Agents must not mutate experiments, artifacts, code, or provenance |

---

## 3. Scientific-truth rule

Deterministic computation, saved parameters, artifacts, metrics, warnings, and provenance are the source of scientific truth.

- AI agents may assist, explain, summarize, and suggest.
- AI agents **do not** produce scientific truth by themselves.
- The platform must never confuse visualization, explanation, hypothesis, and proof.

---

## 4. Local-first rule

- All computation runs locally.
- All storage is local.
- No cloud services may be added.
- No telemetry, analytics, or external calls unless the researcher explicitly opts in.

---

## 5. Agent safety rules

Agents (LLM-powered or otherwise) are **assistants**, not authorities.

- Agents must **not** mutate experiments, artifacts, code, or provenance records.
- Agents must **not** produce outputs that could be mistaken for validated scientific results.
- Agent outputs must always be **labeled** as suggestions, explanations, or summaries — never as facts or proofs.
- Finished runs are **immutable**. No agent or user action may silently alter a completed run's data.

---

## 6. Testing rule

- Every compute kernel must have deterministic unit tests.
- Every orchestrator must have integration tests with known inputs and expected outputs.
- Tests must not require network access.
- Tests must not require GPU (unless explicitly marked as GPU tests).

---

## 7. Provenance and artifact rules

- Every future experiment-producing feature must emit provenance records.
- Every future artifact must have a content hash.
- Finished runs must be treated as immutable.

---

## 8. Scope-control rule

When working on a ticket:

- **Do not** expand scope beyond the ticket.
- **Do not** add dependencies unless the ticket explicitly requests them.
- **Do not** add cloud services.
- **Do not** add LLM runtime code unless the ticket explicitly requests it.
- **Do not** add Julia, MLflow, DVC, Prefect, or Dagster unless the ticket explicitly requests it.
- **Do not** let API routes contain scientific computation logic.
- **Do not** let compute kernels import API, storage adapters, or agents.
- **Do not** let agents mutate experiments, artifacts, code, or provenance.

---

## 9. Stop-after-ticket rule

When the ticket's acceptance criteria are met: **stop**.

Do not refactor unrelated code. Do not add bonus features. Do not reorganize the project structure beyond what the ticket requires. Report what was done, note any assumptions, and stop.
