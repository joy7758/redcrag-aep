# Do Not Change During v0.1 Freeze

## Frozen Semantics

- AEP v0.1 field meanings
- PASS / WARN / FAIL meanings
- validator rule semantics
- risk_links / risk_refs core semantics
- hash chain model
- event_log_hash binding
- deterministic scenario design
- FAIL blocked action evidence meaning

## Frozen Implementation

- `agent/`
- `collector/`
- `validator/`
- `demo/`
- `scripts/`
- `profile/*.schema.json`
- generated demo behavior

## Do Not Add

- real scanner integration
- SARIF parser
- MCP runtime
- FDO registry
- PID binding
- IDS connector
- LLM agent
- LLM benchmark
- database
- web UI
- Docker deployment
- production signing
- compliance claims
- production-readiness claims
- platform claims
- new Future Work items outside the approved five

## Approved Future Work List

1. Refine AEP schema vocabulary.
2. Define a SARIF-to-risk_links mapping.
3. Add optional FDO PID binding.
4. Write a full paper draft.
5. Prepare a small standards discussion note.

## If a Reviewer Requests Expansion

Classify the request as out of scope for v0.1 unless it directly affects reproducibility, correctness, or overclaim correction.
