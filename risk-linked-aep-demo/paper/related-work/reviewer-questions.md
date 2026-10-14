# Reviewer Questions and Short Answers

## 1. Is this just logging?

No. The event log is part of the prototype, but AEP also binds the event log to a manifest, links events to scanner findings, records policy decisions, and produces PASS/WARN/FAIL validation outcomes. Production readiness is not claimed.

## 2. Is this just provenance?

No. AEP uses provenance-like relationships between agent execution, events, and evidence objects, but it adds explicit policy decisions, risk references, and validator results. It is narrower than general provenance and focused on risk-linked execution accountability.

## 3. Why not just use scanner output?

Scanner output describes what may go wrong. It does not prove whether a risky tool was attempted or blocked during a specific execution. AEP links scanner findings to runtime evidence.

## 4. Why does WARN matter?

WARN represents a high-risk finding that exists but was not triggered by runtime evidence. This prevents conflating potential risk with observed violation. It gives reviewers a middle state between PASS and FAIL.

## 5. Why does a blocked denied action count as FAIL?

The prototype treats attempting a denied tool as a policy violation, even if enforcement blocks actual execution. The blocked status is still valuable evidence because it shows enforcement worked. The validator separately records that the denied action was blocked cleanly.

## 6. Why is hash chaining needed?

Hash chaining makes event content and order reviewable. It helps detect changes to individual events or broken sequence links. This is not production-grade secure logging, but it gives the prototype a minimal integrity model.

## 7. Why is FDO/data-space framing relevant?

AEP is intended to shape execution evidence as an object that can be referenced, preserved, and reviewed. FDO/data-space framing is relevant because such environments use identifiers, profiles, metadata, integrity references, and relation links. The prototype does not implement an FDO registry or data-space infrastructure.

## 8. What is new beyond a policy engine?

A policy engine can allow or deny actions. AEP records those decisions as evidence, links them to risk findings, binds them into a bundle, and validates the execution result. It is an evidence-linkage profile, not a replacement policy engine.

## 9. Why not implement SARIF now?

SARIF mapping is useful future work, but Phase 5 keeps the prototype minimal. The current implementation uses normalized risk reports so the evidence model can be reviewed before adding format adapters. It does not claim implemented SARIF support.

## 10. What does the prototype actually prove?

It demonstrates that a small evidence profile can distinguish potential risk, non-triggered risk, and triggered policy violation under deterministic conditions. It also shows that a denied high-risk tool attempt can be recorded as blocked while still producing a FAIL result. It does not prove real-world security coverage.

## 11. What does the prototype not prove?

It does not prove production compliance, real scanner quality, real-world deployment robustness, or LLM-agent behavior. It does not validate SARIF, MCP, FDO registry integration, or production cryptographic signing. It remains a research prototype.

## 12. Is this production-ready?

No. Production readiness is not claimed. The prototype uses synthetic scanner reports, a deterministic non-LLM agent, simple policy lists, and demo signing.

## 13. What is the smallest useful contribution?

The smallest useful contribution is the explicit bridge between scanner risk findings and runtime execution evidence. That bridge supports reviewable PASS/WARN/FAIL conclusions without building a full platform.

## 14. What would be the next standards-facing step?

The next standards-facing step is to refine the AEP schema vocabulary and review mandatory versus optional fields. Citation curation and mappings to SARIF or FDO PID/profile mechanisms should be handled as later, manually reviewed work.
