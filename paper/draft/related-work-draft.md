# Related Work Draft

This is a controlled draft. Source IDs refer to `paper/references/source-inventory.md` and must be manually converted into final citations before submission.

## 1. Positioning

Risk-linked AEP is positioned between pre-execution risk identification and post-execution accountability. The starting point is that a scanner can report what may go wrong, but this does not establish what actually happened during a concrete execution. The AEP contribution is to record runtime execution evidence, preserve the relation to pre-execution risk findings, and support a validator conclusion about whether the run is acceptable.

This positioning is deliberately narrow. AEP does not replace scanners, provenance models, audit logs, policy engines, FDO infrastructure, or data-space infrastructure. It defines a minimal evidence profile and validator path for linking risk findings to concrete execution evidence. The current prototype demonstrates that path under deterministic conditions rather than claiming production compliance, real deployment coverage, or complete standards integration.

The related-work framing therefore treats neighboring areas as inputs, contexts, or comparison points. Scanner and static-analysis outputs motivate the `risk_links` side of the profile. Logging, provenance, and policy enforcement motivate the execution-evidence side. FDO and data-space work motivate the object-shaping and preservation context. The draft keeps these roles separate so that AEP is presented as a bridge layer rather than a replacement for any of them.

## 2. Provenance

Provenance models are relevant because they describe relationships among entities, activities, and agents. This makes provenance a natural neighboring area for AEP: an agent execution can be viewed as an activity, the event log and bundle can be viewed as evidence entities, and the demo agent is the actor associated with the run. PROV-DM is therefore a useful background source for discussing the broad provenance framing [SRC-PROV-DM].

AEP overlaps with provenance by recording execution evidence and preserving relationships among an agent run, event records, and evidence artifacts. However, AEP is not a general provenance model. It is narrower and more operational: each event records a tool-call attempt, `policy_decision`, `execution_status`, `risk_refs`, and a hash-chain position. The bundle records `risk_links` and validator-relevant evidence metadata.

The main distinction is that AEP adds accountability-oriented validation on top of provenance-like relationships. PROV-DM should not be presented as providing AEP policy decisions, `risk_links`, or PASS/WARN/FAIL validation. AEP uses a provenance-adjacent evidence structure, but its contribution is the link between possible risk, concrete execution, and validator outcome.

## 3. Audit Logging and Secure Logging

Audit logging and log management are established security practices for recording events for later review. They provide a background vocabulary for why event records matter, why logs need to be preserved, and why recorded activity may become evidence during later inspection [SRC-NIST-800-92]. Security and privacy control vocabularies also provide useful context for auditability and accountability discussions [SRC-NIST-800-53].

AEP overlaps with logging through its event records. The prototype writes `aep-events.jsonl`, records tool attempts, and uses `event_hash`, `prev_event_hash`, and `event_log_hash` to make the trace reviewable. These mechanisms give the event log a minimal integrity structure, but they should not be described as a full secure logging system.

The difference is that AEP does not stop at event recording. It links event records to scanner findings, records policy decisions and execution status, and produces validator outcomes. The prototype should not be claimed as an enterprise log management system or a NIST-compliant control implementation. Its purpose is to show how logged execution evidence can be structured and risk-linked for accountability review.

## 4. Static Analysis and SARIF

Static analysis and related tools identify potential issues before execution. This is close to the scanner side of the AEP pipeline: scanner output can identify risky tools, configurations, or patterns that may matter during an agent run. SARIF is relevant as a standardized static analysis results interchange format and can support future discussion of scanner result representation [SRC-SARIF].

The current AEP prototype does not implement or parse SARIF. It uses normalized risk reports with fields such as `risk_id`, `severity`, `target`, and `message`. That normalized form is sufficient for the current research goal because the prototype focuses on the evidence profile and validator behavior rather than scanner-format coverage.

Future work may define a SARIF-to-`risk_links` mapping. Such a mapping would be a format adapter from standardized static analysis output into the AEP risk linkage model. It should not be presented as current functionality, and SARIF itself should not be described as proving runtime execution behavior. AEP uses scanner-style findings as inputs, then asks whether runtime evidence shows that a risk target was attempted.

## 5. Agentic AI Security and Agent Scanning

Agentic and AI-enabled systems introduce risks that motivate threat modeling, runtime review, and security scanning. Sources on agentic threats, AI-enabled adversary techniques, and AI risk management can support the broad motivation that agent systems require careful risk framing [SRC-OWASP-AGENTIC] [SRC-MITRE-ATLAS] [SRC-NIST-AI-RMF-GENAI].

Agent security scanning is related because scanners can identify risky tools, permissions, configurations, or deployment settings. In the AEP prototype, the scanner side is represented by deterministic normalized risk reports, including a high-risk `write_file` finding. This captures the role of scanner output as a statement about what may go wrong.

AEP differs from scanning because scanner output alone does not prove what happened in a specific run. AEP complements scanner output by preserving execution evidence and risk-trigger linkage. The prototype should not be described as performing full agent security scanning, adversary emulation, OWASP mitigation implementation, or AI RMF compliance. Its narrower claim is that risk findings can be linked to execution evidence and validator outcomes.

## 6. Policy Enforcement

Policy enforcement and authorization models provide background for decisions about whether actions are allowed or denied. XACML and ABAC-related materials are useful as context for policy decision terminology and access control concepts [SRC-XACML] [SRC-NIST-800-162]. They help situate the AEP fields `policy_decision` and `execution_status`.

The current AEP prototype records policy decisions, but it does not define a full policy language. The policy model is intentionally simple: `allowed_tools` and `denied_tools`. This is enough to demonstrate the evidence path for allowed calls, denied attempts, blocked execution, and validator conclusions.

AEP is therefore not a replacement for a policy engine. A policy engine can decide whether an action is allowed; AEP records that decision as evidence, links it to risk context, and validates the resulting execution trace. The prototype should not be described as implementing XACML, ABAC, obligations, attribute-based evaluation, or temporal policy logic.

## 7. FDO and FAIR Digital Objects

FDO-style framing is relevant because evidence objects may need identifiers, profile declarations, metadata, integrity references, and relation links. The AEP bundle has fields that align with this style of thinking: `bundle_id`, `fdo.object_id`, `fdo.profile_type`, `fdo.profile_version`, `event_log_hash`, `risk_links`, `policy.policy_id`, and integrity metadata. The FAIR Digital Object Framework and FDO requirement materials can support discussion of this object-oriented framing [SRC-FDOF] [SRC-FDO-REQ].

The AEP bundle can be interpreted as a future FDO-style evidence object shape. This means the bundle is organized so that later work could bind it to persistent identifiers, profile mechanisms, metadata services, or object lifecycle processes. In the current prototype, those integrations are not implemented.

The boundary is important. AEP does not claim to satisfy all FDO requirements, implement an FDO registry, perform PID binding, or support lifecycle operations. It only provides a profile-shaped evidence object that can be discussed in relation to FDO and later refined for standards-facing alignment.

## 8. Data Spaces and Accountable Exchange

Data-space contexts emphasize controlled and trustworthy data exchange. In such settings, automated operations may need evidence that can be preserved, referenced, and reviewed after execution. The IDS Reference Architecture Model is relevant background for discussing controlled exchange and data-space framing [SRC-IDS-RAM].

AEP contributes an evidence object shape that could support accountable review of agent operations in data-space contexts. The bundle records execution identity, policy context, risk links, and integrity references. The event log records the concrete tool attempts and outcomes that support later review.

The current prototype is not a data-space implementation. It does not implement IDS, a connector, data usage control, contract negotiation, or infrastructure-level trust services. Its relation to data spaces is that AEP evidence could become a preserved and referenced artifact in future accountable exchange workflows.

## 9. Summary of Distinction

AEP does not replace provenance, logging, secure logging, SARIF, scanners, policy systems, FDO, or data spaces. Each neighboring area provides part of the context: provenance helps describe relationships, logging records events, static analysis reports potential issues, policy systems decide allow or deny, and FDO/data-space frameworks provide object and exchange context. AEP is positioned as a bridge across these concerns.

The core contribution is the connection between potential risk reports and actual execution evidence. The profile defines a manifest-level bundle and event-level trace, the risk linkage connects scanner findings to tool attempts, and the validator turns the evidence into PASS, WARN, or FAIL [Repository: paper/aep-profile-v0.1.md] [Repository: paper/validator-rules.md].

The key distinction is that potential risk is not the same as triggered violation. WARN represents potential but untriggered risk: the scanner finding exists, but runtime evidence does not show the risky tool being attempted. FAIL represents an observed violation or attempted high-risk denied action, even when the collector blocks actual execution. This distinction is central to the evaluation and to the accountability claim [Repository: paper/evaluation-section.md].
