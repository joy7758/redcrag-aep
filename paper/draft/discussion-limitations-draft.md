# Discussion and Limitations Draft

This is a controlled Discussion and Limitations draft based on the current repository. It interprets the deterministic prototype and must not be read as a claim of production readiness, compliance, or real-world security coverage.

Citation and artifact note: repository references in this draft are placeholders for review. They should be converted into final artifact citations, appendix references, or supplementary-material references before submission.

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

## 7.5 Future-work Boundary

Future work should remain bounded. The next steps are:

1. Refine AEP schema vocabulary.
2. Define a SARIF-to-risk_links mapping.
3. Add optional FDO PID binding.
4. Write a full paper draft.
5. Prepare a small standards discussion note.

Future work should not immediately expand into a platform, dashboard, marketplace, production scanner, or full data-space infrastructure. The next step is to refine the profile and paper argument before adding implementation complexity [Repository: paper/research-scope.md] [Repository: paper/draft/open-items.md].
