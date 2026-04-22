# Release Notes v0.1 Review

## Release Type

This is a source-tree review release for a research prototype.

## Included Capabilities

- deterministic PASS / WARN / FAIL demo
- AEP bundle and event log generation
- hash-chained event records
- normalized risk report inputs
- risk linkage through `risk_links` and `risk_refs`
- minimal validator with six rules
- machine-readable validation reports
- acceptance checker
- full paper assembly draft
- consistency audit

## Demonstrated Scenarios

| Scenario | Demonstrated behavior | Expected validator result |
| --- | --- | --- |
| PASS | No high-risk finding; allowed tools only. | PASS |
| WARN | High-risk `write_file` finding exists; `write_file` not attempted. | WARN |
| FAIL | High-risk `write_file` finding exists; `write_file` attempted and blocked. | FAIL |

## Not Included

- real scanner integration
- SARIF parser
- MCP runtime
- LLM agent
- FDO registry
- PID binding
- IDS connector
- data usage control
- database
- web UI
- Docker deployment
- production signing
- compliance certification
- real-world benchmark

## Known Limitations

- synthetic scanner reports
- deterministic non-LLM agent
- simple allow/deny policy
- simple target-to-tool risk matching
- local hash checks only
- source IDs not yet converted to final citations
- paper draft not yet venue formatted
