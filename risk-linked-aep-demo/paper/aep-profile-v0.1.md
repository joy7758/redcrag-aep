# Agent Evidence Profile v0.1

## Purpose

Agent Evidence Profile (AEP) v0.1 defines the minimum structure of an evidence object that records an agent execution, links it to policy constraints, and preserves references to pre-execution risk findings.

The profile separates manifest-level evidence from event-level execution evidence. The bundle object contains identifiers, policy context, risk references, and integrity metadata. The event log records tool-call evidence as a hash-chained sequence.

## Scope

AEP v0.1 is a minimal profile for deterministic review of agent execution accountability. It defines the required shape of:
- an AEP bundle manifest
- an AEP event log
- risk linkage between scanner findings and runtime events
- integrity references between the manifest and event trace
- validator-relevant policy and execution fields

AEP v0.1 does not define a full policy language, scanner format, ontology, registry protocol, or production trust framework.

## Bundle Model

The bundle object is the manifest-level evidence object. It identifies the execution, binds the event log by hash, preserves risk findings, and records the policy context used for validation.

| Field | Purpose | Why it matters | Current limitation |
| --- | --- | --- | --- |
| `aep_version` | Declares the AEP profile version used by the bundle. | Allows validators and reviewers to interpret the object against a known profile version. | Only `0.1` is defined. |
| `bundle_id` | Identifies the evidence bundle. | Allows the execution evidence object to be referenced. | Not yet bound to a real PID or registry identifier. |
| `fdo` | Contains lightweight FDO-style reference metadata. | Provides a place for object reference, profile declaration, and version metadata. | No FDO registry, PID binding, or lifecycle operation is implemented. |
| `agent` | Identifies the agent associated with the execution. | Connects evidence to an agent identifier, name, and version. | Does not define a decentralized agent identity model. |
| `execution` | Describes the concrete execution instance. | Distinguishes one run from another and records task, scenario, timing, and environment hash. | Does not define distributed execution context or external timestamping. |
| `policy` | Records the policy constraints relevant to tool use. | Makes validator conclusions reviewable against the policy in force. | Limited to simple allowed and denied tool lists. |
| `risk_links` | Preserves normalized scanner findings. | Connects potential risks to runtime evidence through target references. | Only supports simple target matching to tool names. |
| `evidence` | Records event log reference metadata. | Links the bundle manifest to the event trace through path, count, and hash. | Uses a local event log reference and no external storage binding. |
| `integrity` | Records bundle authenticity metadata. | Provides a profile location for signature method, key identifier, and signature value. | Uses demo HMAC only; no production key management is defined. |

## Event Model

The event model records execution-level evidence. Each event represents a tool-call attempt and its policy and execution outcome. The event log is serialized as JSONL.

| Field | Purpose | Why it matters |
| --- | --- | --- |
| `event_id` | Identifies the event within the run. | Enables stable reference to a specific evidence item. |
| `run_id` | Identifies the execution run associated with the event. | Links event-level evidence to the bundle execution object. |
| `timestamp` | Records the event timestamp. | Supports event ordering and review of execution sequence. |
| `actor` | Identifies the acting agent. | Associates the event with the agent identity recorded in the bundle. |
| `action` | Declares the event action type. | Allows validators to distinguish tool-call events from possible future event classes. |
| `tool` | Names the attempted tool. | Provides the key field for policy checks and risk target matching. |
| `input_hash` | Records a hash of the tool input. | Preserves evidence of input identity without storing full input content. |
| `output_hash` | Records a hash of tool output, or `null` when no output exists. | Distinguishes executed calls from blocked calls without storing full output content. |
| `policy_decision` | Records the policy decision for the tool attempt. | Makes enforcement evidence explicit as `allow` or `deny`. |
| `execution_status` | Records whether the attempt was executed, blocked, or errored. | Separates attempted actions from completed execution. |
| `risk_refs` | Lists risk finding identifiers touched by the event. | Connects event-level execution evidence to scanner findings. |
| `prev_event_hash` | Records the previous event hash, or `null` for the first event. | Establishes event ordering and chain continuity. |
| `event_hash` | Records the hash of the current event excluding `event_hash`. | Supports detection of event tampering or inconsistent serialization. |

## Integrity Model

`event_hash` is computed over canonical JSON for an event with `event_hash` excluded. `prev_event_hash` links each event to the previous event hash, and the first event has `prev_event_hash` set to `null`.

`event_log_hash` is recorded in the bundle evidence object. It is the SHA-256 hash of the event log file and binds the manifest-level evidence object to the event-level trace.

The bundle includes `integrity.signature`, `integrity.signing_key_id`, and `integrity.signature_method`. The current HMAC signature is only a demo authenticity marker and not production-grade key management.

## Risk Linkage Model

A normalized scanner finding contains a `target` field. In AEP v0.1, this target maps to `event.tool`.

When an event touches a risk target, the corresponding risk identifiers are recorded in `event.risk_refs`. At the manifest level, `bundle.risk_links` preserves the scanner findings used for validation.

This linkage allows a validator to distinguish:
- no high-risk finding
- high-risk finding present but not triggered
- high-risk finding target attempted during execution

## FDO / Data-space Interpretation

| AEP element | FDO/data-space interpretation |
| --- | --- |
| `bundle_id` | Evidence object identifier |
| `fdo.object_id` | Lightweight object reference |
| `fdo.profile_type` | Profile declaration |
| `fdo.profile_version` | Profile version |
| `event_log_hash` | Integrity reference to execution trace |
| `risk_links` | Related risk objects or scanner findings |
| `policy.policy_id` | Governance or policy object reference |
| `integrity.signature` | Authenticity evidence |

This prototype does not implement an FDO registry. It only shapes the AEP bundle as a future FDO-style evidence object.

## Version Boundary

AEP v0.1 includes:
- bundle manifest
- event log
- hash chain
- risk linkage
- minimal validator
- deterministic demo

AEP v0.1 excludes:
- formal ontology
- real PID registry
- real scanner integration
- SARIF mapping
- MCP runtime
- multi-agent workflow
- production signing

## Known Limitations

AEP v0.1 is intentionally small. It does not define semantic policy evaluation, temporal policy logic, multi-agent causality, privacy-preserving disclosure, external timestamping, revocation, registry binding, or production cryptographic key management.

The current risk linkage model assumes direct matching between scanner finding targets and event tool names. More expressive mappings, including SARIF-derived locations or capability identifiers, are outside the current version boundary.
