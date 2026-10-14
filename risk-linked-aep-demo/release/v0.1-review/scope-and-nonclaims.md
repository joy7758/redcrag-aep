# Scope and Non-claims

## In Scope

- minimal Agent Evidence Profile
- manifest-level AEP bundle
- event-level execution trace
- risk linkage between scanner findings and runtime events
- hash chain and event_log_hash reviewability
- simple policy decision recording
- PASS / WARN / FAIL validator
- deterministic reproducibility
- FDO/data-space evidence object shaping

## Out of Scope

- production system
- compliance system
- real scanner integration
- SARIF parser
- MCP runtime
- LLM behavior evaluation
- adversary emulation
- real FDO registry
- PID binding
- IDS connector
- data usage control
- database
- web UI
- Docker deployment
- production signing
- formal ontology
- multi-agent workflow
- attack prevention

## Non-claims

This artifact does not claim:

- production readiness
- compliance certification
- real-world benchmark validity
- attack prevention
- full security coverage
- full standards conformance
- full data-space infrastructure
- full FDO implementation

## Why the Boundary Matters

The contribution is evidence linkage and reviewability. Keeping the artifact small makes the profile inspectable. The deterministic demo shows the logic of PASS / WARN / FAIL without model randomness. Broader integrations should come after profile and paper review.
