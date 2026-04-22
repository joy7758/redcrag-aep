# Risk-linked AEP Model Draft

This is a controlled model-section draft based on `paper/aep-profile-v0.1.md`. It should remain consistent with the AEP v0.1 profile and must not introduce new profile requirements without later review.

## 3. Risk-linked AEP Model

Risk-linked AEP defines a minimal evidence profile for agent execution accountability. It separates manifest-level evidence from event-level execution evidence, and it links pre-execution risk findings to runtime tool-call evidence. The model is intentionally small and reviewable: its purpose is to support evidence linkage and validation, not to define a complete platform or production trust framework [Repository: paper/aep-profile-v0.1.md].

## 3.1 Design Goals

The first design goal is minimality. AEP v0.1 defines only the fields needed for a reviewable evidence object: a bundle manifest, an event log, risk linkage, integrity references, policy context, and validator-facing execution fields. It does not define a full ontology, registry protocol, scanner format, policy language, or production trust framework.

The second design goal is execution accountability. The profile records what was attempted, what was allowed or denied, what was executed or blocked, and what evidence remains after the run. This makes the execution reviewable as a concrete sequence of tool-call evidence rather than as a general statement about system capability.

The third design goal is risk linkage. Scanner findings represent potential risk. AEP connects those findings to runtime events through `risk_links` at the bundle level and `risk_refs` at the event level. This allows a reviewer to ask whether a reported risk was absent, present but not triggered, or attempted during execution.

The fourth design goal is reviewability. The bundle, event log, hash chain, event log hash, and validator outputs provide a compact structure for post-execution review. The current version does not claim production readiness. Its purpose is to demonstrate an evidence-linkage profile that can be inspected, reproduced, and refined.

## 3.2 Bundle Model

The AEP bundle is the manifest-level evidence object. It identifies the execution, records the agent and policy context, preserves risk findings, binds the event log by hash, and stores integrity metadata. In the prototype, the bundle is written as `aep-bundle.json`.

The bundle acts as the review entry point. A reviewer can inspect the bundle to identify the run, locate the event log, see which policy was in force, and see which scanner findings were preserved as risk links. The bundle does not store full tool inputs or outputs; those appear only as hashes in event records.

The bundle also includes lightweight FDO-style reference metadata. This allows the object to be discussed as a future evidence object shape, while keeping the current prototype independent of any real registry or PID binding. The field is intentionally limited to object reference and profile declaration metadata.

The following table summarizes the bundle fields and their review role.

| Field | Role in the model | Review purpose |
| --- | --- | --- |
| `aep_version` | Declares the profile version. | Allows validators and reviewers to interpret the bundle consistently. |
| `bundle_id` | Identifies the evidence bundle. | Enables reference to a specific evidence object. |
| `fdo` | Holds lightweight FDO-style object metadata. | Supports future object framing without implementing a registry. |
| `agent` | Identifies the agent associated with the execution. | Links evidence to an agent identity and version. |
| `execution` | Describes the concrete run. | Distinguishes one execution instance from another. |
| `policy` | Records tool-use constraints. | Makes policy-based validation reviewable. |
| `risk_links` | Preserves scanner findings. | Connects potential risks to execution evidence. |
| `evidence` | References the event log and its hash. | Binds manifest-level evidence to event-level trace. |
| `integrity` | Records signature metadata. | Provides a location for authenticity evidence. |

`risk_links` preserve normalized scanner findings at the bundle level. This keeps the pre-execution risk context with the evidence object and avoids relying on an external scanner report alone during review. `evidence.event_log_hash` binds the bundle to the event log. `integrity.signature` is demo HMAC only and is not production key management [Repository: paper/aep-profile-v0.1.md].

AEP v0.1 treats the bundle and event fields described in the profile as required for the deterministic validator used in this prototype. Future versions may distinguish required, recommended, and optional fields more formally, but v0.1 uses a minimal required shape to keep validation reviewable.

In v0.1, `policy.policy_id` is recorded as review context for validator interpretation. It is not bound to an externally registered, signed, or independently resolvable policy object. Future work may bind policy references to governance objects or registry-managed identifiers.

## 3.3 Event Model

The event log is the event-level execution evidence. Each event represents a tool-call attempt and records both the policy decision and the execution outcome. In the prototype, the event log is serialized as JSONL in `aep-events.jsonl`.

The event model is designed to distinguish attempted actions from completed actions. A denied tool call can still be recorded as an event even when the collector blocks actual execution. This is important because an attempted denied action is itself relevant evidence, while the blocked status shows that enforcement prevented the tool from running.

Inputs and outputs are represented by hashes rather than full content. `input_hash` records the identity of the tool input, and `output_hash` records the identity of the output when execution occurs. For blocked events, `output_hash` is `null`. This keeps the event trace compact and avoids storing full input or output content in the event log.

The following table summarizes event fields and their review purpose.

| Field | Role in the model | Review purpose |
| --- | --- | --- |
| `event_id` | Identifies an event. | Enables reference to a specific execution evidence item. |
| `run_id` | Links the event to a run. | Connects event evidence to the bundle execution object. |
| `timestamp` | Records event time. | Supports ordering and review. |
| `actor` | Identifies the acting agent. | Associates event evidence with agent identity. |
| `action` | Declares action type. | Allows future event classes while current demo uses tool calls. |
| `tool` | Names the attempted tool. | Supports policy checks and risk target matching. |
| `input_hash` | Hashes the tool input. | Preserves input identity without storing full input. |
| `output_hash` | Hashes output or records null. | Distinguishes executed and blocked attempts. |
| `policy_decision` | Records allow or deny. | Makes enforcement evidence explicit. |
| `execution_status` | Records executed, blocked, or error. | Separates attempted actions from completed execution. |
| `risk_refs` | Lists touched risk identifiers. | Links events to scanner findings. |
| `prev_event_hash` | Links to previous event. | Supports hash-chain continuity. |
| `event_hash` | Hashes current event content. | Supports tamper-evidence for event content. |

The event model is deliberately narrow. It records tool-call evidence for the current prototype and leaves richer runtime semantics, multi-agent causality, privacy-preserving disclosure, and external timestamping outside the v0.1 boundary [Repository: paper/aep-profile-v0.1.md].

## 3.4 Integrity Model

The integrity model gives the event trace a minimal tamper-evident structure. `event_hash` is computed over canonical event JSON with `event_hash` excluded. This makes each event hash dependent on the event content that is being reviewed.

`prev_event_hash` links each event to the previous event. The first event has `prev_event_hash = null`. Later events record the previous event hash, creating a simple chain across the event log. If an event changes or if the sequence is broken, the validator can detect the mismatch.

`event_log_hash` binds the bundle to the complete event log file. It is recorded in the bundle evidence object and compared with the hash of the JSONL event log during validation. This connects the manifest-level evidence object to the event-level trace.

The bundle also contains demo HMAC signature metadata. This signature is an authenticity marker only. The current version does not claim production-grade cryptography, external timestamping, registry-backed integrity, or production key management [Repository: paper/aep-profile-v0.1.md].

Hashing inputs and outputs reduces the amount of raw content stored in the event log, but it is not a privacy-preserving disclosure mechanism. Hashes may still reveal equality, support guessing in small input spaces, or require additional controls such as salting, redaction, or selective disclosure in future versions.

## 3.5 Risk Linkage Model

Scanner findings describe potential risks. In AEP v0.1, normalized scanner findings include a target field. The current prototype maps that target to `event.tool`, which is sufficient to demonstrate whether a risk target was attempted during execution.

When an event touches a risk target, the event records the finding identifier in `risk_refs`. At the manifest level, the bundle preserves the scanner findings in `risk_links`. Together, these fields connect scanner-side potential risk to runtime-side execution evidence.

This linkage supports the central distinction in the prototype. A high-risk finding may exist without being triggered. In that case, runtime evidence shows that the risky target was not attempted. Conversely, if a high-risk target is attempted, the execution evidence can support a FAIL result even if the collector blocks actual tool execution.

The following table summarizes the accountability states supported by the risk linkage model and validator interpretation.

| Accountability state | Risk finding | Runtime evidence | Validator interpretation |
| --- | --- | --- | --- |
| PASS | No high-risk finding relevant to execution. | Only allowed tools are used. | Execution acceptable under current rules. |
| WARN | High-risk finding exists. | Risk target is not attempted. | Potential risk exists but is not triggered. |
| FAIL | High-risk finding exists. | Risk target is attempted or policy violation is observed. | Execution is not acceptable under current rules. |

The risk linkage model is intentionally simple. It uses direct matching between a normalized scanner finding target and `event.tool`. This is simpler than a general capability, permission, endpoint, or SARIF-location mapping. More expressive target namespaces are outside v0.1 and remain future profile work [Repository: paper/aep-profile-v0.1.md] [Repository: paper/validator-rules.md] [Repository: paper/evaluation-section.md].

## 3.6 Validator-facing Semantics

AEP itself is the evidence profile. The validator is the mechanism that interprets the evidence using explicit rules. This distinction matters: PASS, WARN, and FAIL are validation conclusions, not intrinsic raw event fields.

The validator checks minimal structure, hash-chain continuity, event log hash binding, denied policy attempts, high-risk target triggers, and blocked denied tools. These checks convert the bundle, event log, and risk report into an accountability conclusion.

The six validator rule IDs are:

- `V1_SCHEMA_MINIMAL`
- `V2_HASH_CHAIN`
- `V3_EVENT_LOG_HASH`
- `V4_POLICY_ATTEMPT`
- `V5_RISK_TRIGGER`
- `V6_DENIED_TOOL_BLOCKED`

A blocked denied action can still produce FAIL because the attempted action is evidence of policy violation. A denied tool attempt is treated as a policy violation even when the enforcement layer successfully blocks side effects. The blocked status remains important because it shows that actual execution did not occur. Thus the validator distinguishes enforcement success from execution acceptability [Repository: paper/validator-rules.md].

## 3.7 FDO / Data-space Interpretation

The AEP bundle can be interpreted as a future FDO-style evidence object shape. It contains an evidence object identifier, profile metadata, execution metadata, integrity references, policy context, and risk links. These fields allow the bundle to be discussed in FDO and data-space terms without implementing the surrounding infrastructure.

`bundle_id` can serve as an evidence object identifier. `fdo.profile_type` and `fdo.profile_version` declare profile information. `event_log_hash` provides an integrity reference to the execution trace. `risk_links` and `policy.policy_id` act as relation points to risk and governance objects.

The `policy.policy_id` relation point should be read as review context in v0.1, not as an implemented registry binding or signed policy-object reference. The current prototype records which policy context was used for validation, but it does not make that policy externally resolvable or independently authenticated.

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

The prototype does not implement an FDO registry, PID binding, IDS connector, or data usage control. The purpose of the FDO/data-space interpretation is to show how the bundle could be shaped for later preservation, reference, and exchange [Repository: paper/aep-profile-v0.1.md].

## 3.8 Version Boundary

AEP v0.1 includes a bundle manifest, event log, hash chain, risk linkage, minimal validator, and deterministic demo. These components are sufficient to demonstrate the bridge between scanner-side potential risk and runtime-side execution evidence.

AEP v0.1 excludes a formal ontology, real PID registry, real scanner integration, SARIF mapping, MCP runtime, multi-agent workflow, and production signing. It also does not define semantic policy evaluation, temporal policy logic, privacy-preserving disclosure, external timestamping, or registry-backed trust.

The narrow boundary is intentional because the current contribution is evidence linkage and reviewability, not a full platform or production compliance system. Keeping v0.1 small makes the profile easier to inspect, reproduce, and discuss before richer integrations are added [Repository: paper/aep-profile-v0.1.md] [Repository: paper/research-scope.md].
