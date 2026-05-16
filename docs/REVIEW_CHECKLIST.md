# Review Checklist

Use this checklist when reviewing any ticket, pull request, or coding-agent output.

---

## Scope

- [ ] Did the ticket stay in scope? No unrelated refactors, bonus features, or structural changes beyond what was requested.
- [ ] Did this ticket modify only allowed files?
- [ ] Did the ticket infer future roadmap scope?
- [ ] Were dependencies added? If so, were they explicitly requested by the ticket?
- [ ] Did the ticket add dependencies?
- [ ] Are assumptions documented? Any decision not directly specified by the ticket should be noted.

## Architecture

- [ ] Were architecture boundaries respected? Check the dependency direction:
  - UI → API → CommandBus → Orchestrators → Compute Kernels → Storage/Provenance
- [ ] Do compute kernels remain pure? No imports from API, storage adapters, or agent modules.
- [ ] Does the API avoid containing scientific computation logic?
- [ ] Did API routes remain thin?
- [ ] Does the frontend communicate only via the API boundary?
- [ ] Are external tools accessed through adapters, not hard-wired as core dependencies?

## Scientific truth

- [ ] Did any code confuse visualization, explanation, hypothesis, or proof?
- [ ] Are deterministic compute results clearly distinguished from agent-generated suggestions?
- [ ] Are agent outputs labeled as suggestions, explanations, or summaries — never as facts?

## Agent safety

- [ ] Did any agent-like behavior mutate experiments, artifacts, code, or provenance?
- [ ] Do suggested commands require explicit researcher approval before execution?
- [ ] Are agent outputs stored separately from scientific records?

## Local-first

- [ ] Did any code weaken local-first behavior?
- [ ] Were cloud services, telemetry, analytics, or external calls added?
- [ ] Does all data remain on the researcher's machine unless explicitly exported?

## Immutability and provenance

- [ ] Are finished runs treated as immutable?
- [ ] Does every experiment-producing feature emit provenance records?
- [ ] Does every artifact carry a content hash?

## Data, artifacts, and caches

- [ ] Are generated artifacts ignored by Git? (Check `.gitignore` rules for `data/` directories.)
- [ ] Were generated caches committed?
- [ ] Are `.gitkeep` files preserved in otherwise-empty tracked directories?

## Documentation hygiene

- [ ] Is README status accurate?
- [ ] Did docs drift from actual implementation state?

## Testing

- [ ] Were tests added where appropriate?
- [ ] Are compute kernel tests deterministic (same input → same output)?
- [ ] Do tests avoid requiring network access?
- [ ] Do tests avoid requiring GPU (unless explicitly marked)?

## Error handling

- [ ] Are errors explicit? No silent failures, no swallowed exceptions.
- [ ] Are warnings recorded as structured WarningRecords, not printed and discarded?
