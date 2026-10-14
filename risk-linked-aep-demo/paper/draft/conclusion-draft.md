# Conclusion Draft

This is a controlled Conclusion draft based on the current repository and paper drafts. It summarizes the contribution without claiming production readiness, compliance, or real-world security coverage.

## 9. Conclusion

Agentic systems can perform concrete tool-mediated operations, and those operations raise accountability questions after execution. Security scanners can identify potential risks before execution, but scanner findings alone do not prove what happened during a specific run. Runtime logs can record behavior, but logs alone may lack integrity structure, policy context, and explicit linkage to known pre-execution risk findings. This paper addresses that gap by focusing on the connection between what may go wrong and what actually happened.

Risk-linked AEP provides a minimal evidence profile for that connection. The AEP bundle acts as manifest-level evidence: it identifies the execution, records lightweight profile and FDO-style metadata, preserves policy context, references normalized risk findings, and binds to the event trace. The event log acts as event-level execution evidence: it records tool-call attempts, policy decisions, execution status, input and output hashes, risk references, and hash-chain fields. Together, `risk_links` and `risk_refs` connect pre-execution findings to runtime events, while `event_hash`, `prev_event_hash`, and `event_log_hash` support reviewable integrity [Repository: paper/aep-profile-v0.1.md].

The validator interprets this evidence rather than replacing the evidence itself. It checks minimal structure, hash-chain continuity, event-log hash binding, policy attempts, risk triggers, and blocked denied tools. Its PASS, WARN, and FAIL outcomes make the evidence reviewable in a small but explicit way. PASS indicates no rule failure or warning under the current rules. WARN indicates that potential risk exists but was not triggered. FAIL indicates that a rule failure occurred, such as a denied tool attempt, high-risk target attempt, or integrity failure.

The deterministic evaluation shows the intended distinction across three scenarios. PASS uses a scanner report with no high-risk finding and an execution that calls only allowed tools. WARN uses a high-risk `write_file` finding but runtime evidence shows that `write_file` was not attempted. FAIL uses the same high-risk `write_file` finding, but the agent attempts `write_file`; the collector blocks actual execution, and the attempted denied high-risk action is still judged as a violation. The observed results matched the expected PASS, WARN, and FAIL outcomes [Repository: paper/evaluation-section.md].

The research meaning of the prototype is therefore narrow but concrete. It demonstrates that potential risk, untriggered risk, and triggered violation can be distinguished under deterministic conditions. The core value is evidence linkage and reviewability, not scanner replacement, general agent safety, production compliance, or real-world benchmark performance. AEP does not replace scanners, provenance models, audit logs, policy engines, FDO infrastructure, or data-space infrastructure. It provides a small bridge between risk reports and execution evidence [Repository: paper/draft/discussion-limitations-draft.md].

The FDO/data-space relevance is also intentionally bounded. The AEP bundle can be shaped as a future FDO-style evidence object because it contains an evidence identifier, profile declarations, integrity references, risk links, and policy references. These elements support later discussion of preservation, reference, exchange, and review of agent execution evidence. The current prototype does not implement an FDO registry, PID binding, IDS connector, data usage control, or lifecycle operation.

The current version has clear boundaries. It has no real scanner integration, no SARIF parser, no MCP runtime, no LLM agent, no production signing, no compliance claim, and no real-world benchmark. These limits are intentional because AEP v0.1 is a reviewable profile and prototype, not an operational platform. The next steps remain limited to:

1. Refine AEP schema vocabulary.
2. Define a SARIF-to-risk_links mapping.
3. Add optional FDO PID binding.
4. Write a full paper draft.
5. Prepare a small standards discussion note.

This staged path keeps the contribution centered on the main research question: how agent execution evidence can be linked with pre-execution security findings to support verifiable accountability in FDO and data-space environments [Repository: paper/research-scope.md].
