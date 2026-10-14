# Introduction Draft

This is a controlled Introduction draft. Source IDs refer to `paper/references/source-inventory.md` and repository references refer to local project documents. All citations must be manually finalized before submission.

## 1. Motivation

Agentic and tool-using systems increasingly perform concrete operations rather than only generating text. A tool-using agent may read files, summarize content, call external services, write artifacts, or invoke other operational capabilities. Once such systems act through tools, review questions become more concrete: what action was attempted, what policy applied, whether the action was allowed or blocked, and what evidence remains after the execution.

These questions matter because agentic and AI-enabled systems introduce risks that require threat modeling and risk management. Existing agentic threat and AI risk management sources can motivate why automated operations need more structured review, especially when tool use creates side effects or interacts with governed environments [SRC-OWASP-AGENTIC] [SRC-MITRE-ATLAS] [SRC-NIST-AI-RMF-GENAI]. This paper does not claim that the prototype performs agent security scanning, adversary emulation, or AI RMF compliance.

The accountability problem is narrower than general AI risk management. It asks how a reviewer can inspect a concrete run after it happens. In such a review, a scanner report is useful because it describes what may go wrong, but the reviewer also needs execution evidence that records what actually happened. A useful evidence object should connect the pre-execution risk context to runtime behavior without claiming to be a full security platform.

This paper therefore treats accountability as an evidence-linkage problem. The relevant question is not only whether a capability exists, but whether the capability was attempted, how policy responded, and whether the resulting trace can be reviewed. This framing keeps the contribution focused on concrete execution evidence.

## 2. Problem Gap

Security scanners can identify potential risks before execution. For an agentic or tool-using system, a scanner may report risky tools, risky permissions, problematic configuration, or other potential concerns. Static analysis and related results formats are relevant to this pre-execution side of the problem [SRC-SARIF]. However, scanner findings alone do not prove what happened during a specific execution.

Runtime logs provide another part of the picture. Audit logging and log management are established practices for recording events that may be reviewed later [SRC-NIST-800-92]. Provenance models are also relevant because they describe relationships among entities, activities, and agents [SRC-PROV-DM]. Policy and authorization models provide background for decisions about allowed and denied actions [SRC-XACML] [SRC-NIST-800-162].

These areas are related, but none of them by itself defines the bridge addressed in this prototype. A log may record events without linking them to pre-execution risk findings. A scanner may identify potential risk without proving runtime behavior. A policy engine may allow or deny an action without preserving a manifest-level evidence object. A provenance model may describe relationships without defining AEP-specific policy decisions, risk references, or PASS/WARN/FAIL validator outcomes.

The gap is therefore the missing link between potential risk and actual execution evidence. Runtime logs alone may be insufficient when they lack integrity structure, policy linkage, and risk linkage. AEP is positioned as a minimal evidence profile for this bridge, not as a replacement for scanners, logging systems, provenance models, SARIF, XACML, ABAC, or any production infrastructure.

## 3. Research Question

How can agent execution evidence be linked with pre-execution security findings to support verifiable accountability in FDO and data-space environments?

The question focuses on linkage rather than scanning. The prototype assumes that a scanner or other pre-execution process can produce risk findings, but it does not attempt to build that scanner. Its focus is the evidence profile that preserves those findings and connects them to concrete execution events.

The question also focuses on concrete execution evidence rather than only potential risk. A high-risk finding matters, but the accountability conclusion depends on whether the relevant target was attempted during the run, whether policy allowed or denied it, and whether the collector executed or blocked it. This distinction makes it possible to treat potential-but-untriggered risk differently from observed violation.

FDO and data-space contexts matter because evidence may need to be preserved, referenced, and exchanged as an object. FDO-style framing is relevant for identifiers, profile declarations, metadata, object typing, and integrity references [SRC-FDOF] [SRC-FDO-REQ]. Data-space framing is relevant for controlled and trustworthy exchange contexts [SRC-IDS-RAM]. The current prototype does not implement an FDO registry, PID binding, IDS, or a data-space connector.

## 4. Proposed Approach

Risk-linked AEP introduces a minimal evidence profile for agent execution accountability. The AEP bundle is the manifest-level evidence object. It records the profile version, bundle identifier, lightweight FDO-style reference fields, agent metadata, execution metadata, policy, risk links, evidence references, and integrity metadata [Repository: paper/aep-profile-v0.1.md].

The AEP event log is the event-level execution trace. Each event records a tool-call attempt, including the tool name, input hash, output hash, policy decision, execution status, risk references, previous event hash, and event hash. `risk_links` preserve scanner findings at the bundle level, while `risk_refs` connect event-level evidence to findings touched by execution.

The integrity model is intentionally small. `event_hash` and `prev_event_hash` form a hash chain over event records. `event_log_hash` binds the bundle to the JSONL event log. The current demo signature is only a demo authenticity marker and is not production signing.

The validator applies a small set of rules over the bundle, event log, and risk report [Repository: paper/validator-rules.md]. The validator preserves three accountability states. PASS means no observed warning or violation. WARN means potential risk exists but was not triggered. FAIL means a violation, integrity failure, or high-risk target was attempted.

## 5. Contributions

1. A minimal Risk-linked Agent Evidence Profile that connects pre-execution risk findings with runtime execution evidence.
2. A validator model that distinguishes PASS, WARN, and FAIL accountability states based on integrity, policy, and risk-trigger checks.
3. A deterministic prototype demonstrating safe execution, potential-but-untriggered risk, and attempted denied high-risk action.

These contributions are intentionally narrow. The work does not claim production readiness, full compliance automation, real scanner integration, SARIF parsing, MCP runtime support, FDO registry implementation, IDS connector implementation, or production signing. The scope is a minimal research prototype for evidence linkage and accountability review [Repository: paper/research-scope.md].

## 6. Prototype and Results Summary

The prototype uses a deterministic non-LLM demo agent. It provides three tools: `read_file`, `summarize_text`, and `write_file`. The policy allows `read_file` and `summarize_text`, and denies `write_file`. The collector records the execution evidence and blocks denied tool execution.

The evaluation uses three scenarios. PASS has no high-risk scanner finding and uses only allowed tools. WARN has a high-risk `write_file` finding, but `write_file` is not attempted. FAIL has a high-risk `write_file` finding and an attempted `write_file` call; the collector blocks execution, but the attempt still counts as a violation [Repository: paper/evaluation-section.md].

| Scenario | Expected | Actual | Status |
| --- | --- | --- | --- |
| PASS | PASS | PASS | OK |
| WARN | WARN | WARN | OK |
| FAIL | FAIL | FAIL | OK |

The results show the intended distinction among safe execution, potential-but-untriggered risk, and attempted denied high-risk action. The prototype demonstrates the evidence-linkage mechanism under deterministic conditions. It does not demonstrate production deployment, real-world scanner coverage, or general agent behavior.

## 7. Paper Structure

The rest of the paper is organized as follows. Section 2 discusses background and related work. Section 3 introduces the Risk-linked AEP model. Section 4 describes the prototype implementation. Section 5 presents the evaluation. Section 6 discusses implications and limitations. Section 7 concludes.
