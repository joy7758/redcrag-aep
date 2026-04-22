# Prototype Implementation Draft

This is a controlled implementation-section draft based on the current repository. It documents the deterministic research prototype and must not be read as a production architecture or deployment guide.

## 4. Prototype Implementation

The prototype implements the minimum path from scanner finding to execution evidence to validator result. It is deterministic, uses Python standard library only, and does not call an LLM. It does not implement real scanner integration, SARIF parsing, MCP runtime, FDO registry, IDS connector, or production signing. Its purpose is to make the AEP model reviewable and reproducible [Repository: README.md] [Repository: REVIEW_PACK.md].

## 4.1 Repository Structure

The repository is organized around the evidence pipeline. Profile artifacts define the intended evidence shapes. Scanner-output fixtures provide pre-execution risk inputs. The agent and collector generate runtime evidence, and the validator turns that evidence into PASS, WARN, or FAIL.

The structure also separates implementation from paper-facing material. Runtime code is contained in `agent/`, `collector/`, `validator/`, `demo/`, and `scripts/`. Research notes and draft sections live under `paper/`, while generated run artifacts live under `runs/`.

This organization keeps the prototype auditable. A reviewer can inspect the profile, run the deterministic scenarios, examine generated artifacts, and compare validator reports with the intended accountability states.

| Path | Role in prototype | Paper relevance |
| --- | --- | --- |
| `profile/` | Contains AEP and risk report schemas and examples. | Defines profile artifacts used by the model section. |
| `scanner-output/` | Contains deterministic risk reports and a simple normalizer. | Provides pre-execution risk inputs. |
| `agent/` | Contains deterministic demo agent, tools, and policy. | Provides controlled runtime behavior. |
| `collector/` | Contains event collection, hash chaining, and demo signing logic. | Produces AEP event logs and bundles. |
| `validator/` | Contains validation CLI and rule logic. | Produces PASS/WARN/FAIL conclusions. |
| `demo/` | Contains input data and demo runner. | Reproduces the three scenarios. |
| `runs/` | Contains generated execution artifacts. | Stores reproducible evidence outputs. |
| `scripts/` | Contains acceptance checker. | Supports artifact-level validation. |
| `paper/` | Contains research and draft materials. | Supports paper development and review. |

[Repository: README.md] [Repository: REVIEW_PACK.md]

## 4.2 Deterministic Demo Agent

The demo agent is deterministic and non-LLM. It executes a fixed sequence of tool calls for each scenario and uses fixed run identifiers. This removes randomness from the evaluation and makes the generated evidence repeatable.

The agent supports three scenarios: `pass`, `warn`, and `fail`. The PASS scenario uses a scanner report with no high-risk finding. The WARN scenario uses a high-risk `write_file` finding but does not attempt `write_file`. The FAIL scenario uses the same high-risk finding and attempts `write_file` through the collector.

In the FAIL scenario, actual `write_file` execution is blocked by the collector. The blocked attempt is still recorded as evidence. This design is central to the prototype because it distinguishes enforcement success from execution acceptability.

[Repository: agent/demo_agent.py] [Repository: paper/evaluation-section.md]

## 4.3 Demo Tools and Policy

The prototype exposes three tools. `read_file` reads deterministic input text from `demo/input.txt`. `summarize_text` produces a deterministic summary by selecting the first words of the input. `write_file` is included as a risky tool because it can modify local files.

Policy is represented as a simple JSON allow/deny list. The policy allows `read_file` and `summarize_text`. It denies `write_file`, `shell_exec`, and `send_email`. This is sufficient for the prototype, but it is not a full policy language.

The simple policy model supports the three accountability states. PASS and WARN use only allowed tools. FAIL attempts a denied tool and is blocked by the collector.

| Tool | Purpose | Policy status | Role in scenarios |
| --- | --- | --- | --- |
| `read_file` | Reads demo input text. | Allowed | Used in all scenarios. |
| `summarize_text` | Produces deterministic summary. | Allowed | Used in all scenarios. |
| `write_file` | Writes output to a file. | Denied | Not attempted in PASS/WARN; attempted and blocked in FAIL. |

[Repository: agent/tools.py] [Repository: agent/policy.json]

## 4.4 Scanner Output and Normalized Risk Reports

The prototype does not implement a real scanner. It uses deterministic JSON files to represent scanner output. This keeps the implementation focused on evidence linkage rather than scanner construction.

`no-risk.json` represents a scan with an empty findings list. `write-file-risk.json` represents one high-risk finding targeting `write_file`. These two inputs are sufficient to exercise the PASS, WARN, and FAIL scenarios.

`hackmyagent-sample.json` and `normalize_risk_report.py` illustrate the adapter boundary. The normalizer converts a fake scanner-native sample into the normalized risk format. The current prototype does not parse SARIF and does not claim SARIF support.

| File | Meaning | Used by scenario |
| --- | --- | --- |
| `scanner-output/no-risk.json` | Empty findings list. | PASS |
| `scanner-output/write-file-risk.json` | High-risk finding targeting `write_file`. | WARN and FAIL |
| `scanner-output/hackmyagent-sample.json` | Fake scanner-native example. | Normalization illustration |
| `scanner-output/normalize_risk_report.py` | Simple deterministic normalizer. | Demonstrates adapter boundary |

[Repository: scanner-output/no-risk.json] [Repository: scanner-output/write-file-risk.json] [Repository: scanner-output/normalize_risk_report.py]

## 4.5 AEP Collector

The AEP collector is the implementation bridge between runtime behavior and the AEP evidence model. It wraps tool calls, loads the policy and risk report, and decides whether each tool attempt is allowed or denied.

For allowed tools, the collector executes the tool and records the output hash. For denied tools, it does not execute the tool. Instead, it records `policy_decision` as `deny`, `execution_status` as `blocked`, and `output_hash` as `null`.

The collector hashes inputs and outputs rather than storing full content in the event log. It attaches `risk_refs` by matching a risk finding target to `event.tool`. This implements the current target-to-tool risk linkage model.

The collector also maintains the event hash chain. Each event records `prev_event_hash`, and the event itself receives an `event_hash`. After tool calls finish, the collector writes `aep-events.jsonl` and generates `aep-bundle.json`.

[Repository: collector/aep_collector.py] [Repository: collector/hash_chain.py] [Repository: paper/aep-profile-v0.1.md]

## 4.6 Hash Chain and Demo Signing

The hash-chain logic uses canonical JSON for event hashing. Canonicalization sorts keys, uses compact separators, and preserves Unicode text. `event_hash` is computed from the event content with `event_hash` itself excluded.

`prev_event_hash` links events in order. The first event has `prev_event_hash` set to `null`, and each later event points to the previous event hash. This gives the event log a minimal integrity structure.

`event_log_hash` binds the bundle to the complete event log file. The collector computes the hash after writing the event log and stores it under `bundle.evidence.event_log_hash`.

The signing helper uses demo HMAC-SHA256 over the bundle payload with `integrity.signature` excluded. This signature is a demonstration marker only. No external timestamping, registry-backed signing, production key lifecycle, or production cryptographic signing is implemented.

[Repository: collector/hash_chain.py] [Repository: collector/signer.py] [Repository: paper/aep-profile-v0.1.md]

## 4.7 Validator Implementation

The validator reads the bundle, event log, and risk report. It performs manual minimal checks and does not use third-party JSON Schema validation. This keeps the prototype dependency-free while still checking the evidence properties needed by the demo.

The validator implements six rules. These rules check structure, hash-chain continuity, event log hash binding, policy attempts, high-risk trigger status, and whether denied tools were blocked.

Aggregation is simple. The result is FAIL if any rule fails. If no rule fails but at least one rule warns, the result is WARN. If all rules pass, the result is PASS.

The validator writes a machine-readable `validation-report.json`. The CLI also prints a concise human-readable summary for review.

| Rule | Implementation purpose |
| --- | --- |
| `V1_SCHEMA_MINIMAL` | Checks required bundle and event fields. |
| `V2_HASH_CHAIN` | Recomputes event hashes and chain continuity. |
| `V3_EVENT_LOG_HASH` | Compares event log file hash with bundle reference. |
| `V4_POLICY_ATTEMPT` | Treats denied tool attempts as policy violations. |
| `V5_RISK_TRIGGER` | Distinguishes untriggered high-risk findings from attempted targets. |
| `V6_DENIED_TOOL_BLOCKED` | Confirms denied tools were blocked and produced no output hash. |

[Repository: validator/rules.py] [Repository: validator/validate_aep.py] [Repository: paper/validator-rules.md]

## 4.8 Demo Runner and Acceptance Checker

`demo/run_all.py` runs the PASS, WARN, and FAIL scenarios. It regenerates artifacts under `runs/`, validates each generated bundle, writes validation reports, and prints an expected-versus-actual table.

`scripts/acceptance_check.py` provides artifact-level checks. It runs the demo, verifies that required files exist, checks validation results, confirms that the FAIL scenario contains a blocked `write_file` event, and confirms that `blocked-write.txt` does not exist.

The Makefile exposes the main commands for reproduction. It uses `python3` as the default interpreter and includes scenario validation targets and `make clean` for generated run directories.

| Command | Purpose |
| --- | --- |
| `python3 demo/run_all.py` | Runs all three demo scenarios and validation. |
| `python3 scripts/acceptance_check.py` | Runs acceptance checks over generated artifacts. |
| `make demo` | Makefile wrapper for the demo. |
| `make acceptance` | Makefile wrapper for acceptance checks. |

[Repository: demo/run_all.py] [Repository: scripts/acceptance_check.py] [Repository: Makefile]

## 4.9 Generated Artifacts

Each scenario produces three generated artifacts: `aep-events.jsonl`, `aep-bundle.json`, and `validation-report.json`. These files are generated under `runs/pass/`, `runs/warn/`, and `runs/fail/`.

`aep-events.jsonl` is the event-level execution trace. `aep-bundle.json` is the manifest-level evidence object. `validation-report.json` records the validator result and individual rule checks.

Generated runs are reproducible and normally ignored by git. They are regenerated by the demo runner and checked by the acceptance script.

| Scenario | Risk input | Runtime behavior | Generated validator result |
| --- | --- | --- | --- |
| PASS | No high-risk finding. | Allowed tools only. | PASS |
| WARN | High-risk `write_file` finding. | `write_file` not attempted. | WARN |
| FAIL | High-risk `write_file` finding. | `write_file` attempted and blocked. | FAIL |

[Repository: runs/pass/validation-report.json] [Repository: runs/warn/validation-report.json] [Repository: runs/fail/validation-report.json] [Repository: paper/evaluation-section.md]

## 4.10 Implementation Boundaries

The current implementation has a deliberately narrow boundary. It includes no real scanner integration, no SARIF parser, no MCP runtime, no LLM agent, no FDO registry, no IDS connector, no database, no web UI, no Docker deployment, no production cryptographic signing, and no compliance claim.

This boundary is intentional. The prototype is designed to isolate the evidence-linkage mechanism: a scanner report states what may go wrong, the collector records what happened, and the validator determines whether the run is acceptable under the current rules.

Keeping the implementation small also supports reproducibility. The prototype can be reviewed as a deterministic artifact rather than as a platform. Future work may add mappings or integrations, but those are outside the current implementation.

These boundaries also make the validation result easier to interpret. PASS, WARN, and FAIL are produced by a fixed rule set over fixed artifacts, not by a changing service or model. The implementation therefore supports the paper's claim about evidence linkage while avoiding claims about production security coverage.

This is why the implementation favors explicit files, explicit rules, and deterministic inputs throughout the repository.
It also keeps reviewer replication straightforward.

[Repository: paper/research-scope.md] [Repository: README.md]
