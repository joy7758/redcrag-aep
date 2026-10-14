# Terminology Glossary

| Term | Working definition in this prototype | Related terms | Boundary / non-claim |
| --- | --- | --- | --- |
| Agent | The deterministic demo actor that invokes tools through the collector. | actor, runtime subject | Not a full autonomous LLM agent in this version. |
| Execution | One concrete run of the demo agent under a selected scenario. | run, task execution | Not a distributed or multi-agent workflow. |
| Execution evidence | Recorded evidence of tool-call attempts, policy decisions, execution outcomes, and hashes. | trace, audit evidence, provenance record | Not full semantic proof of intent. |
| AEP bundle | Manifest-level evidence object that identifies the run, policy, risk links, event log hash, and integrity metadata. | manifest, evidence object | Not a full registry object. |
| AEP event | Event-level evidence record for a tool-call attempt. | trace event, audit event | Does not encode arbitrary runtime semantics. |
| Event log | JSONL sequence of AEP events for one run. | audit log, execution trace | Not a general logging framework. |
| Hash chain | Linkage where each event records the previous event hash and its own event hash. | tamper-evident log, integrity chain | No external timestamping or production key management. |
| Risk finding | Normalized scanner finding with severity, target, category, and message. | scanner result, risk report item | Synthetic in this prototype. |
| Risk link | Connection between scanner finding and runtime event. | risk reference, finding reference | Currently target-to-tool matching only. |
| Scanner | Source of pre-execution risk findings. | static analyzer, agent scanner | The prototype does not implement a real scanner. |
| Policy | Simple allow/deny tool policy used by the collector and validator. | authorization policy, governance rule | Not a semantic or temporal policy language. |
| Policy decision | Recorded decision for a tool attempt, either `allow` or `deny`. | authorization decision | Does not model complex obligations or conditions. |
| Execution status | Recorded outcome such as `executed`, `blocked`, or `error`. | runtime status, enforcement outcome | Does not represent full process state. |
| Validator | Rule-based checker that returns PASS, WARN, or FAIL from bundle, event log, and risk report evidence. | verifier, evidence checker | Not a compliance automation system. |
| PASS | Overall result when there is no rule failure and no warning. | acceptable result | Does not imply production certification. |
| WARN | Overall result when there is no rule failure, but a high-risk finding exists and was not triggered. | caution, non-triggered risk | Does not mean the scanner finding is false. |
| FAIL | Overall result for policy violation, integrity failure, or high-risk target attempted. | violation, unacceptable result | Does not prove malicious intent. |
| Accountability | Ability to review what happened against policy and risk context. | responsibility, answerability | Not full legal or regulatory compliance. |
| Auditability | Ability to inspect evidence records and validation outcomes after execution. | reviewability, audit trail | Not a complete audit management system. |
| Provenance | Broader concept for relationships among entities, activities, and agents. | lineage, derivation | AEP uses provenance-like ideas but adds policy/risk validation fields. |
| FDO-style evidence object | Bundle shaped for future FDO/data-space interpretation. | FAIR Digital Object, evidence object | No real FDO registry implemented. |
| Data-space context | Setting where evidence may support controlled and accountable data exchange. | data governance, trusted exchange | No full data-space infrastructure implemented. |
