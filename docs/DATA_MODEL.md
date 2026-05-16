# Data Model (Conceptual)

> **This document is conceptual only.** No schema code exists yet. These definitions guide future Pydantic models and database tables.

---

## Core entities

### Experiment

A named research investigation. Groups related runs under a shared goal or hypothesis.

- Has a unique ID and a human-readable name.
- Contains metadata: description, creation timestamp, tags.
- References zero or more Runs.

### Run

A single execution of a pipeline within an experiment.

- Has a unique ID, a reference to its parent Experiment, and a status (pending, running, completed, failed).
- Records the full parameter set used.
- References the Jobs it spawned.
- Once completed, a Run is **immutable**.

### Job

A unit of work within a Run. Corresponds to one node in the pipeline graph.

- Has a unique ID and a reference to its parent Run.
- References the compute kernel it invokes and the parameters it passes.
- Produces StateFrames and/or Artifacts.
- Has a status and timing metadata.

### StateFrame

An intermediate snapshot of computation state captured during a Job.

- Has a unique ID and a reference to its parent Job.
- Contains structured data representing the state at a specific step or iteration.
- Used for inspection, visualization, and debugging — not necessarily persisted as a final artifact.

### ArtifactRef

A reference to an immutable output stored in the content-addressed artifact store.

- Has a unique ID, a content hash (SHA-256), a media type, and a size.
- Points to a blob in `data/blobs/`.
- Linked to the Job that produced it.
- Content hash guarantees integrity: if the hash doesn't match, the artifact is corrupt.

### Metric

A named numerical measurement produced by a Job or derived during post-processing.

- Has a name, a value, a unit (optional), and a reference to its source Job.
- Examples: iteration count, convergence error, fractal dimension estimate, elapsed time.

### WarningRecord

A structured warning emitted during computation.

- Has a severity level, a message, a reference to its source Job, and a timestamp.
- Warnings are part of the scientific record — they are not silently discarded.
- Examples: convergence not reached, numerical precision loss, parameter near boundary.

---

## Provenance and lineage

### ProvenanceEvent

An append-only record of something that happened in the system.

- Has a unique ID, a timestamp, an event type, and a reference to the entity it describes.
- Event types include: run_started, run_completed, run_failed, artifact_stored, parameter_changed, approval_granted, approval_denied.
- Forms the nodes and edges of the provenance/lineage graph.
- For finished runs, provenance events are **immutable**.

---

## Agent-related entities

### AgentOutput

A labeled suggestion, explanation, or summary produced by an AI agent.

- Has a unique ID, a timestamp, the agent identity, and the output content.
- Always labeled with its type: suggestion, explanation, summary.
- **Never** presented as validated scientific fact.
- **Never** mutates experiments, artifacts, or provenance.

### SuggestedCommand

A command proposed by an agent for the researcher to review.

- Has a unique ID, a reference to the AgentOutput that produced it, and the proposed command with parameters.
- Requires explicit Approval before execution.

### Approval

A researcher's decision to accept or reject a SuggestedCommand.

- Has a unique ID, a reference to the SuggestedCommand, a decision (approved/rejected), and a timestamp.
- Recorded as a ProvenanceEvent.

---

## Research-level entity

### ResearchClaim

A researcher-authored statement about a result, linked to supporting evidence.

- Has a unique ID, a textual claim, and references to the Artifacts, Metrics, and Runs that support it.
- Explicitly distinguishes between: observation, hypothesis, and validated claim.
- A claim without linked evidence is flagged as unsupported.
- Claims do not constitute proof by themselves — they are pointers to evidence that can be independently verified.
