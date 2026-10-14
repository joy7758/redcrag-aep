# Risk-linked AEP Review Pack

## 1. Purpose

Security scanners report what may go wrong before or around an agent execution. AEP records what actually happened during the execution. The validator decides whether that execution is acceptable under policy and risk-linked evidence rules. This demo focuses on verifiable accountability for agent execution evidence. It is intended as a minimal research artifact for future FDO/data-space evidence object work.

## 2. Repository Map

- `profile/`: JSON Schema Draft 2020-12 profile documents and static illustrative bundle examples.
- `scanner-output/`: deterministic normalized risk reports and a fake scanner-native sample converter.
- `agent/`: deterministic demo agent, demo tools, and policy.
- `collector/`: AEP collector, hash-chain helpers, and demo HMAC signing.
- `validator/`: manual validator rules and CLI.
- `demo/`: input text and end-to-end runner.
- `runs/`: reproducible generated event logs, bundles, and validation reports.
- `paper/`: paper-facing materials for contribution framing, profile description, validator rules, evaluation, scope, and architecture.

## 3. Architecture

```text
Scanner risk report
      ↓
Demo agent runtime
      ↓
AEP collector
      ↓
AEP bundle + event log
      ↓
AEP validator
      ↓
PASS / WARN / FAIL
```

## 4. Evidence Model

`aep-bundle.json` is the manifest-level evidence object. `aep-events.jsonl` is the event-level execution trace. Each event includes `event_hash` and `prev_event_hash`, creating a hash chain across tool-call evidence. The bundle-level `event_log_hash` connects the manifest to the exact event log file. `risk_links` connect scanner findings to execution evidence so the validator can distinguish potential risk from triggered risk.

## 5. Validator Rules

- `V1_SCHEMA_MINIMAL`: checks required top-level bundle fields and required event fields without a third-party JSON Schema validator.
- `V2_HASH_CHAIN`: recomputes each event hash and verifies the previous-event hash chain.
- `V3_EVENT_LOG_HASH`: hashes the JSONL event log and compares it with `bundle.evidence.event_log_hash`.
- `V4_POLICY_ATTEMPT`: fails if any event attempted a denied tool.
- `V5_RISK_TRIGGER`: warns when a high/critical risk exists but was not triggered, and fails when a high/critical risk target was attempted.
- `V6_DENIED_TOOL_BLOCKED`: verifies denied tool attempts were blocked and produced no output hash.

## 6. Demo Scenarios

PASS:
- no high-risk finding
- only allowed tools used
- expected validator result: PASS

WARN:
- high-risk `write_file` finding exists
- `write_file` was not attempted
- expected validator result: WARN

FAIL:
- high-risk `write_file` finding exists
- `write_file` was attempted
- collector blocked execution
- attempt still counts as violation
- expected validator result: FAIL

## 7. FDO / Data Space Mapping

| AEP field | FDO/data-space interpretation |
| --- | --- |
| `bundle_id` | evidence object identifier |
| `fdo.object_id` | lightweight object reference |
| `fdo.profile_type` | profile declaration |
| `fdo.profile_version` | profile version |
| `event_log_hash` | integrity reference |
| `risk_links` | related risk objects |
| `policy.policy_id` | governance/policy object reference |
| `integrity.signature` | authenticity evidence |

This prototype does not implement an FDO registry. It only shows how an AEP bundle could be shaped as a future FDO-style evidence object.

## 8. How to Reproduce

```bash
make demo
make acceptance
```

Direct commands:

```bash
python3 demo/run_all.py
python3 scripts/acceptance_check.py
```

If the local environment maps `python` to Python 3, `python demo/run_all.py` may also work.

## 9. Current Limitations

- no real scanner integration
- no SARIF parser
- no MCP runtime
- no LLM agent
- no real FDO registry
- no production cryptographic signing
- no third-party JSON Schema validation
- validator performs manual minimal checks

## 10. Next Research Step

The next step should be profile refinement, schema review, validator rule documentation, and paper/demo write-up. It should not be platform construction.

For paper-facing materials, see `paper/README.md`.
