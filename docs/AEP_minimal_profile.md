# AEP Minimal Profile

RedCrag AEP (Agent Execution Profile) is a compact evidence record for an agent run. The minimal profile keeps the parts needed for audit without storing sensitive source content.

## Minimal Fields

- `schema_version`: profile version, for example `aep-0.1`.
- `run_id`: stable identifier for the agent run.
- `workflow`: workflow name, for example `contract_review_demo`.
- `actor`: agent or system actor that performed the run.
- `task`: short task description.
- `started_at`: run start time.
- `completed_at`: run completion time.
- `tool_calls`: audited tool/action calls with `tool_name`, `started_at`, `completed_at`, and `purpose`.
- `input_refs`: input references only. Store summaries, hashes, source locations, or record IDs, not full contract text.
- `output_refs`: output references and conclusions. For contract review, each conclusion should include `source_clause_ref` or `source_location`.
- `receipt_refs`: receipts proving external actions happened, such as approval receipts or delivery receipts.
- `human_review`: human approval state for high-risk actions.
- `policy_results`: policy checks or rule outcomes recorded during execution.
- `content_hashes`: SHA-256 hashes for referenced content or selected bundle fields.
- `signature`: demo signature metadata and value.
- `metadata`: non-sensitive implementation notes.

## Privacy Boundary

The bundle should not include full contracts, medical records, customer secrets, private keys, API keys, or raw regulated content. Store pointers, clause references, summaries, and hashes instead.

## Signing Boundary

The current implementation uses `HMAC-SHA256-DEMO` for local demonstration. It is not a production legal signature. Production deployments can replace it with Sigstore, Cosign, or an enterprise key-management and signing system.
