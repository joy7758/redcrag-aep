# Claim-to-Source Map

Purpose:
This file maps paper claims to verified source candidates. It helps prevent unsupported claims and overclaiming.

| Claim | Supported by | How to use | Boundary |
| --- | --- | --- | --- |
| Provenance models describe relationships among entities, activities, and agents. | SRC-PROV-DM | Use as background for provenance concepts and to explain why AEP is related to provenance. | Do not claim provenance alone provides AEP risk linkage or validator outcomes. |
| Static analysis tools can produce standardized result output. | SRC-SARIF | Use as background for future mapping from scanner results to `risk_links`. | Do not claim the prototype implements SARIF. |
| FDO framing is relevant for evidence objects that need identifiers, metadata, types, and resolution behavior. | SRC-FDOF, SRC-FDO-REQ | Use to frame AEP bundle as a future FDO-style evidence object and to discuss possible future alignment. | Do not claim the prototype implements an FDO registry or PID binding. |
| Data-space contexts emphasize controlled and trustworthy data exchange. | SRC-IDS-RAM | Use as context for accountable exchange and data-space framing. | Do not claim the prototype implements a data-space connector or usage control. |
| Audit logging and log management are established security practices. | SRC-NIST-800-92, SRC-NIST-800-53 | Use as background for event recording, auditability, and control vocabulary. | Do not claim the prototype is a full log management system or NIST-compliant control implementation. |
| Access control and policy decision models exist as established policy enforcement background. | SRC-XACML, SRC-NIST-800-162 | Use as background for authorization and policy decision terminology. | Do not claim the prototype implements XACML or ABAC. |
| Agentic and AI-enabled systems introduce security risks requiring threat modeling. | SRC-OWASP-AGENTIC, SRC-MITRE-ATLAS, SRC-NIST-AI-RMF-GENAI | Use as motivation for linking agent risks to execution evidence. | Do not claim the prototype performs full agent security scanning or adversary emulation. |
| AEP connects potential risk findings to concrete execution evidence. | Repository materials: `paper/aep-profile-v0.1.md`, `paper/validator-rules.md`, `paper/evaluation-section.md`, `paper/draft/argument-flow.md` | Present as the prototype contribution. | This is the prototype contribution, not a claim from external sources. |
| WARN differs from FAIL because potential risk is not the same as triggered violation. | Repository materials: `paper/evaluation-section.md`, `paper/draft/argument-flow.md`, `validator/rules.py` | Use to explain the accountability-state distinction. | Do not present this as an established external standard. |
| The prototype demonstrates a deterministic evidence-linkage mechanism, not production compliance. | Repository materials: `paper/research-scope.md`, `paper/draft/paper-skeleton.md`, `REVIEW_PACK.md` | Use to keep claims bounded to the research prototype. | Do not claim production readiness. |
