# Risk-linked Agent Evidence Profile for Verifiable Agent Execution Accountability

This is a controlled full-paper assembly draft. Source IDs and repository references are placeholders for later manual citation and artifact formatting. This draft must not be read as claiming production readiness, compliance, real-world security coverage, or full standards integration.

## Abstract

Agent security scanners can identify potential risks in tools, configurations, and runtime settings, but scanner output alone does not prove what happened during concrete execution. Runtime logs can record behavior, yet they may lack integrity structure, policy context, and explicit linkage to pre-execution findings. This paper introduces the Risk-linked Agent Evidence Profile (AEP), a minimal profile for connecting scanner findings with runtime execution evidence. AEP separates a manifest-level bundle from an event-level execution trace: the bundle records execution, policy, risk, evidence, and lightweight FDO-style metadata, while the event log records tool-call attempts, policy decisions, execution status, and risk references. The prototype uses hash-chain integrity over events, an event-log hash in the bundle, and `risk_links` / `risk_refs` to relate scanner findings to runtime events. A validator consumes the bundle, event log, and risk report to produce PASS, WARN, or FAIL conclusions. A deterministic prototype evaluates safe execution, potential-but-untriggered risk, and attempted denied high-risk action. The work positions AEP for future FDO/data-space evidence object preservation and reference, while making no claim of production readiness or full scanner, SARIF, FDO, MCP, or data-space integration.

## Keywords

- agent execution evidence
- accountability
- risk linkage
- FDO
- data spaces
- validation
- provenance

## 1. Introduction

### 1.1 Motivation

Agentic and tool-using systems increasingly perform concrete operations rather than only generating text. A tool-using agent may read files, summarize content, call external services, write artifacts, or invoke other operational capabilities. Once such systems act through tools, review questions become more concrete: what action was attempted, what policy applied, whether the action was allowed or blocked, and what evidence remains after the execution.

These questions matter because agentic and AI-enabled systems introduce risks that require threat modeling and risk management. Existing agentic threat and AI risk management sources can motivate why automated operations need more structured review, especially when tool use creates side effects or interacts with governed environments [SRC-OWASP-AGENTIC] [SRC-MITRE-ATLAS] [SRC-NIST-AI-RMF-GENAI]. This paper does not claim that the prototype performs agent security scanning, adversary emulation, or AI RMF compliance.

The accountability problem is narrower than general AI risk management. It asks how a reviewer can inspect a concrete run after it happens. In such a review, a scanner report is useful because it describes what may go wrong, but the reviewer also needs execution evidence that records what actually happened. A useful evidence object should connect the pre-execution risk context to runtime behavior without claiming to be a full security platform.

This paper therefore treats accountability as an evidence-linkage problem. The relevant question is not only whether a capability exists, but whether the capability was attempted, how policy responded, and whether the resulting trace can be reviewed. This framing keeps the contribution focused on concrete execution evidence.

### 1.2 Problem Gap

Security scanners can identify potential risks before execution. For an agentic or tool-using system, a scanner may report risky tools, risky permissions, problematic configuration, or other potential concerns. Static analysis and related results formats are relevant to this pre-execution side of the problem [SRC-SARIF]. However, scanner findings alone do not prove what happened during a specific execution.

Runtime logs provide another part of the picture. Audit logging and log management are established practices for recording events that may be reviewed later [SRC-NIST-800-92]. Provenance models are also relevant because they describe relationships among entities, activities, and agents [SRC-PROV-DM]. Policy and authorization models provide background for decisions about allowed and denied actions [SRC-XACML] [SRC-NIST-800-162].

These areas are related, but none of them by itself defines the bridge addressed in this prototype. A log may record events without linking them to pre-execution risk findings. A scanner may identify potential risk without proving runtime behavior. A policy engine may allow or deny an action without preserving a manifest-level evidence object. A provenance model may describe relationships without defining AEP-specific policy decisions, risk references, or PASS/WARN/FAIL validator outcomes.

The gap is therefore the missing link between potential risk and actual execution evidence. Runtime logs alone may be insufficient when they lack integrity structure, policy linkage, and risk linkage. AEP is positioned as a minimal evidence profile for this bridge, not as a replacement for scanners, logging systems, provenance models, SARIF, XACML, ABAC, or any production infrastructure.

### 1.3 Research Question

How can agent execution evidence be linked with pre-execution security findings to support verifiable accountability in FDO and data-space environments?

The question focuses on linkage rather than scanning. The prototype assumes that a scanner or other pre-execution process can produce risk findings, but it does not attempt to build that scanner. Its focus is the evidence profile that preserves those findings and connects them to concrete execution events.

The question also focuses on concrete execution evidence rather than only potential risk. A high-risk finding matters, but the accountability conclusion depends on whether the relevant target was attempted during the run, whether policy allowed or denied it, and whether the collector executed or blocked it. This distinction makes it possible to treat potential-but-untriggered risk differently from observed violation.

FDO and data-space contexts matter because evidence may need to be preserved, referenced, and exchanged as an object. FDO-style framing is relevant for identifiers, profile declarations, metadata, object typing, and integrity references [SRC-FDOF] [SRC-FDO-REQ]. Data-space framing is relevant for controlled and trustworthy exchange contexts [SRC-IDS-RAM]. The current prototype does not implement an FDO registry, PID binding, IDS, or a data-space connector.

### 1.4 Proposed Approach

Risk-linked AEP introduces a minimal evidence profile for agent execution accountability. The AEP bundle is the manifest-level evidence object. It records the profile version, bundle identifier, lightweight FDO-style reference fields, agent metadata, execution metadata, policy, risk links, evidence references, and integrity metadata [Repository: paper/aep-profile-v0.1.md].

The AEP event log is the event-level execution trace. Each event records a tool-call attempt, including the tool name, input hash, output hash, policy decision, execution status, risk references, previous event hash, and event hash. `risk_links` preserve scanner findings at the bundle level, while `risk_refs` connect event-level evidence to findings touched by execution.

The integrity model is intentionally small. `event_hash` and `prev_event_hash` form a hash chain over event records. `event_log_hash` binds the bundle to the JSONL event log. The current demo signature is only a demo authenticity marker and is not production signing.

The validator applies a small set of rules over the bundle, event log, and risk report [Repository: paper/validator-rules.md]. The validator preserves three accountability states. PASS means no observed warning or violation. WARN means potential risk exists but was not triggered. FAIL means a violation, integrity failure, or high-risk target was attempted.

### 1.5 Contributions

1. A minimal Risk-linked Agent Evidence Profile that connects pre-execution risk findings with runtime execution evidence.
2. A validator model that distinguishes PASS, WARN, and FAIL accountability states based on integrity, policy, and risk-trigger checks.
3. A deterministic prototype demonstrating safe execution, potential-but-untriggered risk, and attempted denied high-risk action.

These contributions are intentionally narrow. The work does not claim production readiness, full compliance automation, real scanner integration, SARIF parsing, MCP runtime support, FDO registry implementation, IDS connector implementation, or production signing. The scope is a minimal research prototype for evidence linkage and accountability review [Repository: paper/research-scope.md].

### 1.6 Prototype and Results Summary

The prototype uses a deterministic non-LLM demo agent. It provides three tools: `read_file`, `summarize_text`, and `write_file`. The policy allows `read_file` and `summarize_text`, and denies `write_file`. The collector records the execution evidence and blocks denied tool execution.

The evaluation uses three scenarios. PASS has no high-risk scanner finding and uses only allowed tools. WARN has a high-risk `write_file` finding, but `write_file` is not attempted. FAIL has a high-risk `write_file` finding and an attempted `write_file` call; the collector blocks execution, but the attempt still counts as a violation [Repository: paper/evaluation-section.md].

| Scenario | Expected | Actual | Status |
| --- | --- | --- | --- |
| PASS | PASS | PASS | OK |
| WARN | WARN | WARN | OK |
| FAIL | FAIL | FAIL | OK |

The results show the intended distinction among safe execution, potential-but-untriggered risk, and attempted denied high-risk action. The prototype demonstrates the evidence-linkage mechanism under deterministic conditions. It does not demonstrate production deployment, real-world scanner coverage, or general agent behavior.

### 1.7 Paper Structure

The rest of the paper is organized as follows. Section 2 discusses background and related work. Section 3 introduces the Risk-linked AEP model. Section 4 describes the prototype implementation. Section 5 presents the evaluation. Sections 6 and 7 discuss implications and limitations. Section 8 scopes future work. Section 9 concludes.

## 2. Background and Related Work

### 2.1 Positioning

Risk-linked AEP is positioned between pre-execution risk identification and post-execution accountability. The starting point is that a scanner can report what may go wrong, but this does not establish what actually happened during a concrete execution. The AEP contribution is to record runtime execution evidence, preserve the relation to pre-execution risk findings, and support a validator conclusion about whether the run is acceptable.

This positioning is deliberately narrow. AEP does not replace scanners, provenance models, audit logs, policy engines, FDO infrastructure, or data-space infrastructure. It defines a minimal evidence profile and validator path for linking risk findings to concrete execution evidence. The current prototype demonstrates that path under deterministic conditions rather than claiming production compliance, real deployment coverage, or complete standards integration.

The related-work framing therefore treats neighboring areas as inputs, contexts, or comparison points. Scanner and static-analysis outputs motivate the `risk_links` side of the profile. Logging, provenance, and policy enforcement motivate the execution-evidence side. FDO and data-space work motivate the object-shaping and preservation context. The draft keeps these roles separate so that AEP is presented as a bridge layer rather than a replacement for any of them.

### 2.2 Provenance

Provenance models are relevant because they describe relationships among entities, activities, and agents. This makes provenance a natural neighboring area for AEP: an agent execution can be viewed as an activity, the event log and bundle can be viewed as evidence entities, and the demo agent is the actor associated with the run. PROV-DM is therefore a useful background source for discussing the broad provenance framing [SRC-PROV-DM].

AEP overlaps with provenance by recording execution evidence and preserving relationships among an agent run, event records, and evidence artifacts. However, AEP is not a general provenance model. It is narrower and more operational: each event records a tool-call attempt, `policy_decision`, `execution_status`, `risk_refs`, and a hash-chain position. The bundle records `risk_links` and validator-relevant evidence metadata.

The main distinction is that AEP adds accountability-oriented validation on top of provenance-like relationships. PROV-DM should not be presented as providing AEP policy decisions, `risk_links`, or PASS/WARN/FAIL validation. AEP uses a provenance-adjacent evidence structure, but its contribution is the link between possible risk, concrete execution, and validator outcome.

### 2.3 Audit Logging and Secure Logging

Audit logging and log management are established security practices for recording events for later review. They provide a background vocabulary for why event records matter, why logs need to be preserved, and why recorded activity may become evidence during later inspection [SRC-NIST-800-92]. Security and privacy control vocabularies also provide useful context for auditability and accountability discussions [SRC-NIST-800-53].

AEP overlaps with logging through its event records. The prototype writes `aep-events.jsonl`, records tool attempts, and uses `event_hash`, `prev_event_hash`, and `event_log_hash` to make the trace reviewable. These mechanisms give the event log a minimal integrity structure, but they should not be described as a full secure logging system.

The difference is that AEP does not stop at event recording. It links event records to scanner findings, records policy decisions and execution status, and produces validator outcomes. The prototype should not be claimed as an enterprise log management system or a NIST-compliant control implementation. Its purpose is to show how logged execution evidence can be structured and risk-linked for accountability review.

### 2.4 Static Analysis and SARIF

Static analysis and related tools identify potential issues before execution. This is close to the scanner side of the AEP pipeline: scanner output can identify risky tools, configurations, or patterns that may matter during an agent run. SARIF is relevant as a standardized static analysis results interchange format and can support future discussion of scanner result representation [SRC-SARIF].

The current AEP prototype does not implement or parse SARIF. It uses normalized risk reports with fields such as `risk_id`, `severity`, `target`, and `message`. That normalized form is sufficient for the current research goal because the prototype focuses on the evidence profile and validator behavior rather than scanner-format coverage.

Future work may define a SARIF-to-`risk_links` mapping. Such a mapping would be a format adapter from standardized static analysis output into the AEP risk linkage model. It should not be presented as current functionality, and SARIF itself should not be described as proving runtime execution behavior. AEP uses scanner-style findings as inputs, then asks whether runtime evidence shows that a risk target was attempted.

### 2.5 Agentic AI Security and Agent Scanning

Agentic and AI-enabled systems introduce risks that motivate threat modeling, runtime review, and security scanning. Sources on agentic threats, AI-enabled adversary techniques, and AI risk management can support the broad motivation that agent systems require careful risk framing [SRC-OWASP-AGENTIC] [SRC-MITRE-ATLAS] [SRC-NIST-AI-RMF-GENAI].

Agent security scanning is related because scanners can identify risky tools, permissions, configurations, or deployment settings. In the AEP prototype, the scanner side is represented by deterministic normalized risk reports, including a high-risk `write_file` finding. This captures the role of scanner output as a statement about what may go wrong.

AEP differs from scanning because scanner output alone does not prove what happened in a specific run. AEP complements scanner output by preserving execution evidence and risk-trigger linkage. The prototype should not be described as performing full agent security scanning, adversary emulation, OWASP mitigation implementation, or AI RMF compliance. Its narrower claim is that risk findings can be linked to execution evidence and validator outcomes.

### 2.6 Policy Enforcement

Policy enforcement and authorization models provide background for decisions about whether actions are allowed or denied. XACML and ABAC-related materials are useful as context for policy decision terminology and access control concepts [SRC-XACML] [SRC-NIST-800-162]. They help situate the AEP fields `policy_decision` and `execution_status`.

The current AEP prototype records policy decisions, but it does not define a full policy language. The policy model is intentionally simple: `allowed_tools` and `denied_tools`. This is enough to demonstrate the evidence path for allowed calls, denied attempts, blocked execution, and validator conclusions.

AEP is therefore not a replacement for a policy engine. A policy engine can decide whether an action is allowed; AEP records that decision as evidence, links it to risk context, and validates the resulting execution trace. The prototype should not be described as implementing XACML, ABAC, obligations, attribute-based evaluation, or temporal policy logic.

### 2.7 FDO and FAIR Digital Objects

FDO-style framing is relevant because evidence objects may need identifiers, profile declarations, metadata, integrity references, and relation links. The AEP bundle has fields that align with this style of thinking: `bundle_id`, `fdo.object_id`, `fdo.profile_type`, `fdo.profile_version`, `event_log_hash`, `risk_links`, `policy.policy_id`, and integrity metadata. The FAIR Digital Object Framework and FDO requirement materials can support discussion of this object-oriented framing [SRC-FDOF] [SRC-FDO-REQ].

The AEP bundle can be interpreted as a future FDO-style evidence object shape. This means the bundle is organized so that later work could bind it to persistent identifiers, profile mechanisms, metadata services, or object lifecycle processes. In the current prototype, those integrations are not implemented.

The boundary is important. AEP does not claim to satisfy all FDO requirements, implement an FDO registry, perform PID binding, or support lifecycle operations. It only provides a profile-shaped evidence object that can be discussed in relation to FDO and later refined for standards-facing alignment.

### 2.8 Data Spaces and Accountable Exchange

Data-space contexts emphasize controlled and trustworthy data exchange. In such settings, automated operations may need evidence that can be preserved, referenced, and reviewed after execution. The IDS Reference Architecture Model is relevant background for discussing controlled exchange and data-space framing [SRC-IDS-RAM].

AEP contributes an evidence object shape that could support accountable review of agent operations in data-space contexts. The bundle records execution identity, policy context, risk links, and integrity references. The event log records the concrete tool attempts and outcomes that support later review.

The current prototype is not a data-space implementation. It does not implement IDS, a connector, data usage control, contract negotiation, or infrastructure-level trust services. Its relation to data spaces is that AEP evidence could become a preserved and referenced artifact in future accountable exchange workflows.

### 2.9 Summary of Distinction

AEP does not replace provenance, logging, secure logging, SARIF, scanners, policy systems, FDO, or data spaces. Each neighboring area provides part of the context: provenance helps describe relationships, logging records events, static analysis reports potential issues, policy systems decide allow or deny, and FDO/data-space frameworks provide object and exchange context. AEP is positioned as a bridge across these concerns.

The core contribution is the connection between potential risk reports and actual execution evidence. The profile defines a manifest-level bundle and event-level trace, the risk linkage connects scanner findings to tool attempts, and the validator turns the evidence into PASS, WARN, or FAIL [Repository: paper/aep-profile-v0.1.md] [Repository: paper/validator-rules.md].

The key distinction is that potential risk is not the same as triggered violation. WARN represents potential but untriggered risk: the scanner finding exists, but runtime evidence does not show the risky tool being attempted. FAIL represents an observed violation or attempted high-risk denied action, even when the collector blocks actual execution. This distinction is central to the evaluation and to the accountability claim [Repository: paper/evaluation-section.md].

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

The prototype assumes that tool calls are mediated by the AEP collector. It does not address bypass resistance, collector compromise, or enforcement outside the instrumented runtime. These assumptions are acceptable for the deterministic prototype but must be revisited before deployment-oriented use.

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

## 5. Evaluation

The evaluation checks whether the prototype distinguishes three accountability states: safe execution, potential-but-untriggered risk, and triggered violation. The evaluation is deterministic and reproducible. It is not a real-world deployment benchmark, and it does not measure scanner quality, model quality, performance, or scalability [Repository: paper/evaluation-section.md].

## 5.1 Evaluation Goal

The goal is to evaluate the evidence-linkage path rather than system performance. The path under test is: scanner finding -> runtime evidence -> validator conclusion. The prototype succeeds if the same deterministic implementation can produce PASS, WARN, and FAIL outcomes from different combinations of scanner findings and runtime behavior.

The evaluation asks whether AEP evidence can distinguish three cases. The first case has no relevant high-risk finding and no policy violation. The second case has a high-risk finding, but runtime evidence shows that the risk target was not attempted. The third case has a high-risk target attempted during execution and a policy violation observed.

The key distinction is that potential risk is not the same as triggered violation. A scanner report can say that `write_file` is risky, but the accountability conclusion depends on whether `write_file` appears in the event log and how policy handled the attempt.

This evaluation supports the research question by showing a minimal accountability mechanism. It does not prove that the scanner is complete, that the tool set is representative, or that the same behavior would hold in a deployed agent platform. Its purpose is to show that evidence linkage can be made explicit and reproducible [Repository: paper/draft/argument-flow.md] [Repository: paper/evaluation-section.md].

## 5.2 Experimental Setup

The experiment uses a deterministic non-LLM demo agent. The agent executes fixed tool sequences for the PASS, WARN, and FAIL scenarios. This removes model randomness from the evaluation and makes the generated artifacts repeatable.

The prototype includes three tools: `read_file`, `summarize_text`, and `write_file`. The first two tools are allowed by policy. `write_file` is denied by policy and is used to represent a risky tool whose attempted use can be observed and blocked.

The policy allows `read_file` and `summarize_text`. It denies `write_file`, `shell_exec`, and `send_email`. The evaluation uses two scanner risk inputs: `no-risk.json`, which has an empty findings list, and `write-file-risk.json`, which contains a high-risk finding targeting `write_file`.

For each scenario, the AEP collector generates `aep-events.jsonl` and `aep-bundle.json`. The validator reads the bundle, event log, and risk report, then writes `validation-report.json`.

| Component | Configuration in evaluation | Purpose |
| --- | --- | --- |
| Demo agent | Deterministic non-LLM agent | Removes model randomness from evaluation. |
| Allowed tools | `read_file`, `summarize_text` | Represents permitted execution behavior. |
| Denied tools | `write_file`, `shell_exec`, `send_email` | Represents policy-constrained actions. |
| No-risk report | Empty findings list | Supports PASS scenario. |
| Write-file risk report | High-risk finding targeting `write_file` | Supports WARN and FAIL scenarios. |
| AEP collector | Wraps tool calls and records evidence | Produces event log and bundle. |
| Validator | Applies six validation rules | Produces PASS/WARN/FAIL result. |

[Repository: agent/demo_agent.py] [Repository: agent/tools.py] [Repository: agent/policy.json] [Repository: scanner-output/no-risk.json] [Repository: scanner-output/write-file-risk.json]

## 5.3 Scenario Design

The PASS scenario represents acceptable execution under the current rules. The scanner report has no high-risk finding. The agent calls only `read_file` and `summarize_text`, both of which are allowed. The expected validator result is PASS.

The WARN scenario represents potential risk that is not triggered. The scanner report contains a high-risk finding for `write_file`. The agent still calls only the allowed tools and does not attempt `write_file`. The expected validator result is WARN, meaning that potential risk exists but runtime evidence does not show the target being attempted.

The FAIL scenario represents an observed attempted violation. The scanner report contains the same high-risk `write_file` finding. The agent attempts `write_file` through the collector. The collector denies and blocks actual execution, but the attempt is recorded as evidence. The expected validator result is FAIL.

These scenarios are designed to isolate the main claim: a risk-linked evidence profile can distinguish no high-risk condition, untriggered high-risk condition, and attempted denied high-risk action.

| Scenario | Scanner finding | Runtime behavior | Expected result | Accountability meaning |
| --- | --- | --- | --- | --- |
| PASS | No high-risk finding. | Only allowed tools are used. | PASS | Execution acceptable under current rules. |
| WARN | High-risk `write_file` finding exists. | `write_file` is not attempted. | WARN | Potential risk exists but is not triggered. |
| FAIL | High-risk `write_file` finding exists. | `write_file` is attempted and blocked. | FAIL | Attempted denied high-risk action is observed. |

[Repository: paper/evaluation-section.md] [Repository: demo/run_all.py]

## 5.4 Validator Rules Used in Evaluation

The same validator is used for all scenarios. It reads the AEP bundle, the event log, and the risk report. It then applies a fixed set of rules to produce a machine-readable validation report.

The validator checks schema minimality, hash-chain continuity, event-log hash binding, policy attempts, risk triggers, and blocked denied tools. These checks cover the minimum properties needed by this evaluation.

Result aggregation is simple. The validator returns FAIL if any rule fails. It returns WARN if no rule fails but at least one rule warns. It returns PASS if all rules pass.

In the WARN scenario, the warning comes primarily from a high-risk finding that is not triggered. In the FAIL scenario, failure comes from attempted denied tool use and a high-risk target attempt.

A denied tool attempt is treated as a policy violation even when the enforcement layer successfully blocks side effects. The reason is that the attempt itself is part of the execution evidence and is relevant to accountability.

| Rule | Role in evaluation |
| --- | --- |
| `V1_SCHEMA_MINIMAL` | Confirms required bundle and event fields exist. |
| `V2_HASH_CHAIN` | Confirms event hash chain continuity. |
| `V3_EVENT_LOG_HASH` | Confirms bundle hash matches event log. |
| `V4_POLICY_ATTEMPT` | Marks denied tool attempts as policy violations. |
| `V5_RISK_TRIGGER` | Distinguishes untriggered high-risk findings from attempted targets. |
| `V6_DENIED_TOOL_BLOCKED` | Confirms denied tools were blocked and did not produce output hashes. |

[Repository: paper/validator-rules.md] [Repository: validator/rules.py]

## 5.5 Results

All three scenarios matched the expected result. The PASS scenario produced acceptable execution under the current rules. The WARN scenario preserved a distinction between possible risk and observed behavior. The FAIL scenario recorded attempted `write_file` and confirmed that the attempted tool call was blocked.

| Scenario | Expected | Actual | Status |
| --- | --- | --- | --- |
| PASS | PASS | PASS | OK |
| WARN | WARN | WARN | OK |
| FAIL | FAIL | FAIL | OK |

The FAIL event has the expected blocked-tool evidence. It contains `tool = "write_file"`, `policy_decision = "deny"`, `execution_status = "blocked"`, `output_hash = null`, and `risk_refs` includes `"RISK-001"`. This confirms that the denied call was attempted, linked to the scanner finding, and blocked before actual file-writing execution.

The validation reports also show the rule-level difference among scenarios. PASS has no high-risk findings and no denied tool attempts. WARN has a high-risk finding that is not triggered. FAIL has both a denied tool attempt and a high-risk target attempt [Repository: runs/pass/validation-report.json] [Repository: runs/warn/validation-report.json] [Repository: runs/fail/validation-report.json] [Repository: runs/fail/aep-events.jsonl].

## 5.6 Interpretation

PASS demonstrates normal evidence generation. The collector records allowed tool calls, the bundle binds the event log, and the validator finds no warning or failure. This confirms the baseline path from execution to evidence to validation result.

WARN demonstrates that potential risk and actual execution should not be conflated. The scanner finding exists, but the event log does not show `write_file` being attempted. The validator therefore preserves the distinction between a risk that may matter and a risk that was triggered in a concrete run.

FAIL demonstrates that a denied high-risk action can be recorded as an attempted violation even when blocked. The collector prevents actual `write_file` execution, but the event log still records the attempt, the deny decision, the blocked status, and the risk reference.

This is why the FAIL scenario is not reduced to WARN. WARN indicates that a high-risk finding exists without a runtime trigger; FAIL indicates that the denied high-risk target was attempted, even though side effects were blocked.

The evaluation demonstrates the value of linking scanner findings to runtime evidence. Without this linkage, a reviewer would see either a scanner finding or a runtime trace, but not the relationship between them. With AEP, the reviewer can inspect event-level and bundle-level evidence together.

The evaluation does not prove real-world security coverage, scanner quality, or production compliance. It demonstrates a minimal evidence-linkage mechanism under controlled conditions [Repository: paper/draft/argument-flow.md] [Repository: paper/aep-profile-v0.1.md].

## 5.7 Threats to Validity

Internal validity is limited by the synthetic nature of the scanner reports and the small fixed tool set. The experiment is designed to test evidence linkage, not scanner discovery quality. The direct target-to-tool matching model is sufficient for the current scenarios but does not represent complex risk mappings.

External validity is limited by the deterministic non-LLM agent and the absence of real deployment noise. The prototype does not evaluate autonomous LLM behavior, multi-agent workflows, production tool ecosystems, or live infrastructure. Results should not be generalized to operational deployments without further study.

Construct validity is limited by the simple allow/deny policy and minimal validator. The evaluation does not include a formal policy language, SARIF parser, MCP runtime, real FDO registry, IDS connector, production signing, or comparison against alternative evidence models. It also does not measure performance or scalability.

Reproducibility limits are narrower. The evaluation is intentionally reproducible in the local repository, but generated hashes depend on the generated event log contents. The artifact-level behavior, expected results, and fail-event properties are checked by the acceptance script. These limitations are intentional for a minimal research prototype [Repository: paper/research-scope.md].

## 5.8 Reproducibility

The evaluation is reproducible using existing commands. `python3 demo/run_all.py` regenerates the three scenarios and validates them. It produces event logs, bundles, and validation reports under `runs/`.

`python3 scripts/acceptance_check.py` checks generated files, expected validation results, and key FAIL behavior. In particular, it verifies that the FAIL event contains a blocked `write_file` attempt and that `blocked-write.txt` is absent.

The Makefile provides wrappers for the same workflow. `make demo` runs the demo, and `make acceptance` runs the acceptance checks. Generated run artifacts are reproducible and normally ignored by git.

| Command | Purpose |
| --- | --- |
| `python3 demo/run_all.py` | Regenerates PASS/WARN/FAIL runs and validator reports. |
| `python3 scripts/acceptance_check.py` | Checks generated files, expected results, and blocked fail behavior. |
| `make demo` | Runs the demo through Makefile. |
| `make acceptance` | Runs acceptance checks through Makefile. |

[Repository: demo/run_all.py] [Repository: scripts/acceptance_check.py] [Repository: Makefile]

## 6. Discussion

The prototype demonstrates a minimal evidence-linkage mechanism. It connects scanner findings, runtime event evidence, policy decisions, integrity checks, and validator outcomes. It does not demonstrate a full security platform, real scanner integration, production compliance, or real FDO/data-space infrastructure [Repository: paper/contribution-statement.md] [Repository: paper/draft/evaluation-section-draft.md].

## 6.1 Why Risk Linkage Matters

Scanner findings identify potential risks. They can indicate that a tool, permission, or configuration may be dangerous before execution. However, potential risk alone does not prove that the risk was triggered during a concrete run.

Runtime event evidence provides the other side of the picture. It can show which tools were attempted, allowed, denied, executed, or blocked. Yet without risk linkage, the reviewer still has to manually connect runtime behavior to known pre-execution findings.

AEP links scanner findings to runtime events through `risk_links` and `risk_refs`. `risk_links` preserve normalized scanner findings at the bundle level. `risk_refs` connect individual events to findings touched by execution.

This linkage enables the distinction among no relevant high-risk finding, high-risk finding present but not triggered, and high-risk target attempted. That distinction is the core reason the prototype has PASS, WARN, and FAIL rather than only pass/fail.

Risk linkage also changes the review question. Without linkage, a reviewer may ask only whether a risky capability exists or whether a log line appears. With linkage, the reviewer can ask whether a specific pre-execution finding was touched by a concrete runtime attempt. This is a narrower and more evidence-oriented question. It supports accountability because the conclusion is grounded in both the scanner input and the execution trace.

The WARN scenario is important because it prevents conflating possible risk with observed violation. The scanner reports a high-risk `write_file` finding, but runtime evidence shows that `write_file` was not attempted. The FAIL scenario is important because an attempted denied high-risk action is captured even if blocked [Repository: paper/aep-profile-v0.1.md] [Repository: paper/draft/argument-flow.md] [Repository: paper/evaluation-section.md].

## 6.2 Why Integrity Matters

Accountability depends not only on recording events, but also on making event evidence reviewable. If event content or ordering cannot be checked, then the evidence object is harder to interpret after execution.

The AEP event model uses `event_hash` to support checking event content. Each event hash is computed over canonical event JSON excluding `event_hash` itself. This makes the hash dependent on the event fields that are reviewed.

The field `prev_event_hash` links events into a hash chain. The first event has no previous hash, and each later event points to the hash of the prior event. This allows the validator to detect broken chain continuity.

The bundle-level `event_log_hash` binds the manifest to the event log. A reviewer can compare the bundle reference with the event log file hash to confirm that the manifest and trace match.

This distinction between event-level and bundle-level integrity is important for the model. The hash chain supports review of the sequence of events, while the event log hash supports review of the relationship between the event log and the bundle that claims to describe it. Neither mechanism alone is a complete trust system, but together they make the generated evidence more structured than an ordinary unbound runtime log.

The demo HMAC signature provides a placeholder for authenticity evidence. It is not production cryptography. The current prototype does not provide external timestamping, key lifecycle management, registry-backed integrity, secure storage, or production-grade trust infrastructure. Integrity in this prototype is therefore review-oriented, not production-grade trust infrastructure [Repository: paper/aep-profile-v0.1.md] [Repository: paper/draft/model-section-draft.md].

## 6.3 Why PASS / WARN / FAIL Matters

The validator turns evidence into reviewable conclusions. It does not replace human judgment or provide compliance certification. Its role is to interpret the bundle, event log, and risk report under explicit rules.

PASS means that no rule failed and no warning was produced under the current rules. WARN means that potential risk exists but was not triggered. FAIL means that a rule failure occurred, such as a denied tool attempt, high-risk target attempt, or integrity failure.

The three-state result is intentionally simple. The goal is interpretability and reproducibility, not full compliance automation. This simplicity makes the distinction between potential risk and observed violation visible in the evaluation.

The WARN state is especially useful for avoiding unnecessary escalation from scanner output alone. A high-risk finding remains relevant, but the execution evidence can show that the risk target was not attempted in that run. The FAIL state captures the opposite case: the evidence shows an attempted denied action or another rule failure. The validator therefore separates evidence interpretation from both scanner reporting and policy enforcement.

A denied tool attempt is treated as a policy violation even when the enforcement layer successfully blocks side effects. The attempt itself is part of the execution evidence and is relevant to accountability, while the blocked status records that the side effect did not occur.

| Result | Meaning in this prototype | What it does not mean |
| --- | --- | --- |
| PASS | No rule failure or warning under the current validator rules. | Not a guarantee of safety in real deployments. |
| WARN | Potential high-risk finding exists but was not triggered. | Not evidence of an observed violation. |
| FAIL | A rule failure occurred, such as denied tool attempt or high-risk target attempt. | Not a full incident analysis or root-cause assessment. |

[Repository: paper/validator-rules.md] [Repository: paper/draft/evaluation-section-draft.md]

## 6.4 FDO / Data-space Relevance

The AEP bundle can be interpreted as a future FDO-style evidence object shape. It contains identifiers, profile declarations, integrity references, risk references, and policy references.

This structure is relevant to FDO/data-space contexts because evidence objects may need to be preserved, referenced, exchanged, and reviewed. A bundle that records profile metadata and evidence references is easier to discuss as an object than an unstructured set of logs.

The current contribution is object shaping and evidence linkage, not infrastructure implementation. AEP does not implement an FDO registry, PID binding, IDS connector, data usage control, or data-space infrastructure.

This boundary keeps the FDO/data-space discussion at the level of evidence-object shape. The prototype shows which fields might be useful for later preservation and exchange: an identifier, profile declaration, event-log integrity reference, risk references, policy reference, and authenticity placeholder. It does not define how such an object would be registered, resolved, governed, or exchanged in an operational data space.

The policy reference has the same boundary. In v0.1, `policy.policy_id` is review context for validator interpretation, not a binding to an externally registered, signed, or independently resolvable policy object.

| AEP element | Discussion relevance |
| --- | --- |
| `bundle_id` | Gives the evidence bundle a referenceable identity. |
| `fdo.profile_type` | Indicates how the object should be interpreted. |
| `fdo.profile_version` | Supports versioned profile interpretation. |
| `event_log_hash` | Links manifest-level evidence to event-level trace. |
| `risk_links` | Preserves relations to scanner findings. |
| `policy.policy_id` | Records the governance context used for validation. |
| `integrity.signature` | Provides a placeholder for authenticity evidence. |

This interpretation keeps the research path open for future standards discussion while preserving the current implementation boundary [Repository: paper/aep-profile-v0.1.md] [Repository: paper/draft/model-section-draft.md].

## 6.5 What the Prototype Demonstrates

The prototype demonstrates that a small evidence profile can distinguish potential risk, untriggered risk, and triggered violation under deterministic conditions. It demonstrates the feasibility of linking normalized scanner findings to runtime tool-call evidence.

The prototype also demonstrates that a denied tool attempt can be recorded and judged even when blocked. In the FAIL scenario, the attempted `write_file` call is denied and blocked, but the attempt remains evidence of a policy violation.

The validation path is reproducible. Generated evidence leads to PASS, WARN, and FAIL under a fixed validator. This supports reviewability because the reviewer can inspect event-level evidence, bundle-level evidence, and validator reports together.

The demonstration is therefore strongest as an argument about structure and interpretation. It shows that a small profile can carry enough information for a validator to distinguish the three intended accountability states. It does not show that the chosen fields are complete for every agent system, nor that the rules are sufficient for deployment. Those questions remain outside the current prototype.

| Demonstrated | Not demonstrated |
| --- | --- |
| Risk finding to runtime evidence linkage. | Full scanner coverage. |
| Hash-chained event trace. | Production-grade trust infrastructure. |
| PASS/WARN/FAIL validation. | Compliance certification. |
| Deterministic reproducibility. | Real-world deployment robustness. |
| FDO-style evidence object shaping. | Real FDO registry or PID operation. |

The result should be interpreted as a controlled demonstration of evidence linkage, not as a production security evaluation [Repository: paper/draft/evaluation-section-draft.md] [Repository: paper/research-scope.md].

## 7. Limitations

The limitations are intentional and reflect the narrow scope of the research prototype. The prototype is designed to make the evidence-linkage concept reviewable, not to provide a complete operational system [Repository: paper/research-scope.md].

Manual polishing note: repeated non-claims should be compressed before submission. Keep one concise non-claim statement in the introduction, preserve the detailed boundary discussion in the limitations section, and use only a short reminder in the conclusion.

## 7.1 Implementation Limits

The implementation uses a deterministic non-LLM agent and a small tool set. It includes `read_file`, `summarize_text`, and `write_file`. This is sufficient for the PASS/WARN/FAIL scenarios but does not represent the range of tools available to deployed agents.

The policy model is a simple allow/deny list. It does not implement a semantic policy language, temporal policy logic, XACML, ABAC, or obligations. The risk linkage model is direct target-to-tool matching between a normalized scanner finding target and `event.tool`. It does not implement general capability, permission, endpoint, or SARIF-location mapping.

The scanner reports are synthetic. The implementation includes no real scanner integration, no SARIF parser, and no scanner quality evaluation. It also includes no MCP runtime, database, web UI, Docker deployment, or production signing.

These limits keep the prototype understandable and reproducible, but restrict generality. The implementation should be read as a controlled demonstration of the evidence path [Repository: paper/draft/prototype-implementation-draft.md] [Repository: paper/research-scope.md].

The implementation also avoids features that would make the evidence path harder to inspect. For example, a database or distributed service could obscure where generated evidence is stored. A live LLM agent would introduce behavioral variability that is not needed for this phase. The narrow implementation lets reviewers focus on whether the bundle, event log, risk linkage, and validator rules are coherent.

## 7.2 Evaluation Limits

The evaluation has no real deployment noise and no LLM behavior variability. It uses only three deterministic scenarios and a limited set of policy and risk conditions.

The evaluation does not measure performance or scalability. It does not compare AEP against alternative evidence models. It does not include a user study or operational incident dataset.

The evaluation checks logical separation of accountability states, not external performance or deployment effectiveness. PASS, WARN, and FAIL show that the prototype can distinguish specific controlled cases.

These limitations are acceptable for the current research stage because the evaluation is designed to test whether the evidence-linkage mechanism is coherent and reproducible [Repository: paper/draft/evaluation-section-draft.md].

The evaluation should therefore not be interpreted as evidence that AEP improves security outcomes in deployed systems. It only shows that, for the controlled cases in the repository, the evidence generated by the agent and collector is sufficient for the validator to produce the intended conclusions. A broader evaluation would require real scanner outputs, varied runtime behavior, operational workflows, and comparison baselines.

## 7.3 Standards and Integration Limits

AEP v0.1 does not define a formal ontology. It does not implement a real PID registry, FDO registry, PID binding, IDS connector, data usage control, SARIF mapping, XACML, ABAC, MCP integration, or multi-agent workflow.

The prototype shapes a possible evidence object but does not claim standards conformance or infrastructure integration. Its FDO/data-space interpretation is a mapping for discussion, not a deployed registry or connector.

This boundary matters because adding integrations too early would obscure the core profile. The current goal is to make the evidence object and validation logic reviewable before adding external protocols [Repository: paper/aep-profile-v0.1.md] [Repository: paper/research-scope.md].

The standards-facing interpretation is therefore provisional. It identifies the parts of the AEP bundle that resemble future evidence-object requirements, but it does not assert that AEP v0.1 is already a standardized profile. Further work would need to define mandatory and optional fields, versioning language, relation semantics, and any binding to external identifier or profile mechanisms.

## 7.4 Security and Trust Limits

The prototype uses demo HMAC only. It has no production key management, no external timestamping, no revocation, no secure storage, and no privacy-preserving disclosure.

It also performs no adversary emulation and provides no real tamper-resistance beyond local hash checks. The hash chain and event log hash support local review, but they are not a complete secure logging or trust infrastructure.

The prototype assumes that tool calls are mediated by the AEP collector. It does not address bypass resistance, collector compromise, or enforcement outside the instrumented runtime. These assumptions are acceptable for the deterministic prototype but must be revisited before deployment-oriented use.

Hashing inputs and outputs reduces the amount of raw content stored in the event log, but it is not a privacy-preserving disclosure mechanism. Hashes may still reveal equality, support guessing in small input spaces, or require additional controls such as salting, redaction, or selective disclosure in future versions.

The prototype does not claim to prevent attacks. It records and validates evidence under controlled conditions. It should not be read as a complete trust, security, or incident-response framework [Repository: paper/aep-profile-v0.1.md] [Repository: paper/research-scope.md].

This also limits how the FAIL result should be interpreted. FAIL indicates that the validator observed a rule failure in the evidence, such as a denied tool attempt or high-risk target attempt. It does not identify attacker intent, assign responsibility beyond the recorded execution context, or provide remediation guidance. Those tasks would require additional operational and security processes outside AEP v0.1.

## 8. Future Work

Future work should remain bounded. The next steps are:

1. Refine AEP schema vocabulary.
2. Define a SARIF-to-risk_links mapping.
3. Add optional FDO PID binding.
4. Write a full paper draft.
5. Prepare a small standards discussion note.

Future work should not immediately expand into a platform, dashboard, marketplace, production scanner, or full data-space infrastructure. The next step is to refine the profile and paper argument before adding implementation complexity [Repository: paper/research-scope.md] [Repository: paper/draft/open-items.md].

## 9. Conclusion

Agentic systems can perform concrete tool-mediated operations, and those operations raise accountability questions after execution. Security scanners can identify potential risks before execution, but scanner findings alone do not prove what happened during a specific run. Runtime logs can record behavior, but logs alone may lack integrity structure, policy context, and explicit linkage to known pre-execution risk findings. This paper addresses that gap by focusing on the connection between what may go wrong and what actually happened.

Risk-linked AEP provides a minimal evidence profile for that connection. The AEP bundle acts as manifest-level evidence: it identifies the execution, records lightweight profile and FDO-style metadata, preserves policy context, references normalized risk findings, and binds to the event trace. The event log acts as event-level execution evidence: it records tool-call attempts, policy decisions, execution status, input and output hashes, risk references, and hash-chain fields. Together, `risk_links` and `risk_refs` connect pre-execution findings to runtime events, while `event_hash`, `prev_event_hash`, and `event_log_hash` support reviewable integrity [Repository: paper/aep-profile-v0.1.md].

The validator interprets this evidence rather than replacing the evidence itself. It checks minimal structure, hash-chain continuity, event-log hash binding, policy attempts, risk triggers, and blocked denied tools. Its PASS, WARN, and FAIL outcomes make the evidence reviewable in a small but explicit way. PASS indicates no rule failure or warning under the current rules. WARN indicates that potential risk exists but was not triggered. FAIL indicates that a rule failure occurred, such as a denied tool attempt, high-risk target attempt, or integrity failure.

The deterministic evaluation shows the intended distinction across three scenarios. PASS uses a scanner report with no high-risk finding and an execution that calls only allowed tools. WARN uses a high-risk `write_file` finding but runtime evidence shows that `write_file` was not attempted. FAIL uses the same high-risk `write_file` finding, but the agent attempts `write_file`; the collector blocks actual execution, and the attempted denied high-risk action is still judged as a violation. The observed results matched the expected PASS, WARN, and FAIL outcomes [Repository: paper/evaluation-section.md].

The research meaning of the prototype is therefore narrow but concrete. It demonstrates that potential risk, untriggered risk, and triggered violation can be distinguished under deterministic conditions. The core value is evidence linkage and reviewability, not scanner replacement, general agent safety, production compliance, or real-world benchmark performance. AEP does not replace scanners, provenance models, audit logs, policy engines, FDO infrastructure, or data-space infrastructure. It provides a small bridge between risk reports and execution evidence [Repository: paper/draft/discussion-limitations-draft.md].

The FDO/data-space relevance is also intentionally bounded. The AEP bundle can be shaped as a future FDO-style evidence object because it contains an evidence identifier, profile declarations, integrity references, risk links, and policy references. These elements support later discussion of preservation, reference, exchange, and review of agent execution evidence. The current prototype does not implement an FDO registry, PID binding, IDS connector, data usage control, or lifecycle operation.

The current version has clear boundaries. It has no real scanner integration, no SARIF parser, no MCP runtime, no LLM agent, no production signing, no compliance claim, and no real-world benchmark. These limits are intentional because AEP v0.1 is a reviewable profile and prototype, not an operational platform. The scoped future-work path is listed in Section 8. This staged path keeps the contribution centered on the main research question: how agent execution evidence can be linked with pre-execution security findings to support verifiable accountability in FDO and data-space environments [Repository: paper/research-scope.md].

## Citation and Artifact Notes

- Source IDs such as `[SRC-SARIF]` refer to `paper/references/source-inventory.md` and require manual conversion to final citation format.
- Repository references such as `[Repository: paper/aep-profile-v0.1.md]` refer to local project artifacts and require final artifact citation or appendix treatment.
- In this draft, source IDs and repository references serve as review placeholders only; final bibliography entries and artifact citations should be added only after manual verification.
- This draft does not contain a finalized bibliography.
- No production readiness, compliance certification, real-world benchmark, or full standards integration is claimed.
