# Validator Rules

## Rule Summary Table

| Rule ID | Rule name | Purpose | Pass condition | Warn condition | Fail condition |
| --- | --- | --- | --- | --- | --- |
| `V1_SCHEMA_MINIMAL` | Minimal schema checks | Verify required bundle and event fields exist. | Required fields are present and event count matches. | None. | Required fields are missing or event count mismatches. |
| `V2_HASH_CHAIN` | Event hash chain | Verify event hashes and previous-event links. | All event hashes and links verify. | None. | Any event hash or chain link is invalid. |
| `V3_EVENT_LOG_HASH` | Event log hash | Verify bundle evidence points to the exact event log. | Event log file hash matches bundle value. | None. | Event log hash mismatches. |
| `V4_POLICY_ATTEMPT` | Denied tool attempt | Detect attempted denied tools. | No event has `policy_decision` equal to `deny`. | None. | Any denied tool was attempted. |
| `V5_RISK_TRIGGER` | High-risk trigger | Compare high/critical scanner findings with runtime events. | No high/critical risk exists. | High/critical risk exists but target was not attempted. | High/critical risk target was attempted. |
| `V6_DENIED_TOOL_BLOCKED` | Denied tool blocked | Verify denied attempts did not execute. | Denied events are absent or blocked with `output_hash` equal to `null`. | None. | A denied event was not blocked cleanly. |

## Aggregation Logic

The validator returns `FAIL` if any rule fails. It returns `WARN` if no rule fails but at least one rule warns. It returns `PASS` if all rules pass.

## Rule Details

### V1_SCHEMA_MINIMAL

Input: AEP bundle and event log.

Logic: Check required top-level bundle fields, required event fields, and agreement between bundle event count and parsed event count.

Output: `pass` or `fail`.

Rationale: Validation should fail early if the evidence object is structurally incomplete.

### V2_HASH_CHAIN

Input: AEP event log.

Logic: Recompute each event hash from event content excluding `event_hash`. Verify the first `prev_event_hash` is `null` and every later `prev_event_hash` matches the previous event hash.

Output: `pass` or `fail`.

Rationale: The event trace should expose tampering or broken event ordering.

### V3_EVENT_LOG_HASH

Input: AEP bundle and event log file.

Logic: Compute the SHA-256 hash of the event log file and compare it with `bundle.evidence.event_log_hash`.

Output: `pass` or `fail`.

Rationale: The manifest-level evidence object must bind to the exact event-level trace being reviewed.

### V4_POLICY_ATTEMPT

Input: AEP event log.

Logic: Find events where `policy_decision` is `deny`.

Output: `pass` if none are found, otherwise `fail`.

Rationale: Attempting a denied tool is itself a policy violation, even if enforcement blocks execution.

### V5_RISK_TRIGGER

Input: AEP event log and normalized risk report.

Logic: Select scanner findings with severity `high` or `critical`. If no such findings exist, pass. If a high-risk target appears in any event tool, fail. Otherwise warn.

Output: `pass`, `warn`, or `fail`.

Rationale: The validator must distinguish absent risk, potential-but-untriggered risk, and triggered high-risk execution evidence.

### V6_DENIED_TOOL_BLOCKED

Input: AEP event log.

Logic: For every denied event, require `execution_status` equal to `blocked` and `output_hash` equal to `null`.

Output: `pass` or `fail`.

Rationale: Policy enforcement evidence should show that denied tools did not actually run.

## Interpretation

`PASS` means no high-risk finding was triggered and no policy violation was observed. `WARN` means potential risk exists but runtime evidence did not trigger it. `FAIL` means execution evidence shows a policy violation or integrity failure.

## Known Limits

- manual schema checks only
- no third-party JSON Schema validation
- no semantic policy language
- no temporal policy logic
- no multi-agent reasoning
