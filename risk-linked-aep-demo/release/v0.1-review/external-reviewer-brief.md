# External Reviewer Brief

## One-paragraph Summary

Security scanners identify potential risk, but they do not prove what happened during a concrete execution. AEP records what happened during execution by producing a manifest-level bundle and event-level trace. The validator turns the generated evidence into PASS, WARN, or FAIL. The prototype demonstrates three deterministic scenarios and is intended for research review, not production deployment.

## One-sentence Contribution

This artifact introduces a minimal Risk-linked Agent Evidence Profile that links pre-execution risk findings with runtime execution evidence to support reviewable accountability in FDO and data-space contexts.

## What This Artifact Demonstrates

- deterministic PASS / WARN / FAIL demo
- AEP bundle generation
- hash-chained event log generation
- risk linkage through `risk_links` and `risk_refs`
- validator rule execution
- machine-readable validation reports
- reproducibility via demo and acceptance commands

## What This Artifact Does Not Demonstrate

- production readiness
- compliance certification
- real-world benchmark validity
- attack prevention
- real scanner integration
- SARIF parser
- MCP runtime
- LLM behavior evaluation
- FDO registry
- IDS connector
- production signing
- full platform capability

## Suggested Review Path

1. Run the demo.
2. Inspect `runs/fail/aep-events.jsonl`.
3. Inspect `runs/*/validation-report.json`.
4. Read `paper/aep-profile-v0.1.md`.
5. Read `paper/draft/full-paper-consistency-audit.md`.
6. Skim `paper/draft/full-paper-draft.md`.
7. Fill out `reviewer-feedback-template.md`.

## Key Evidence to Inspect

- `runs/pass/validation-report.json`
- `runs/warn/validation-report.json`
- `runs/fail/validation-report.json`
- `runs/fail/aep-events.jsonl`
- `profile/aep-profile.schema.json`
- `profile/aep-event.schema.json`
- `paper/aep-profile-v0.1.md`
