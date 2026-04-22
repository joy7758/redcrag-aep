# Related-work Source Notes

Purpose:
This file records how each related-work area should use the verified sources.

## Provenance

Use:
- SRC-PROV-DM

Draft note:
PROV-DM can support the background claim that provenance describes relations among entities, activities, and agents. AEP is related to provenance because it records execution evidence, but AEP adds `policy_decision`, `execution_status`, `risk_refs`, `risk_links`, and validator outcomes.

## Audit Logging and Secure Logging

Use:
- SRC-NIST-800-92
- SRC-NIST-800-53

Draft note:
Audit logging and security controls provide background for recording and reviewing events. AEP overlaps with logging through event records and integrity checks, but differs by linking scanner findings and policy decisions to validator outcomes.

## Static Analysis and SARIF

Use:
- SRC-SARIF

Draft note:
SARIF can support the claim that static analysis results have a standardized interchange format. Current AEP uses normalized risk reports only; SARIF-to-`risk_links` mapping is future work.

## Agentic AI Security

Use:
- SRC-OWASP-AGENTIC
- SRC-MITRE-ATLAS
- SRC-NIST-AI-RMF-GENAI

Draft note:
These sources support the motivation that agentic or AI-enabled systems have security risks requiring threat modeling and risk management. AEP does not replace threat models or scanners; it links risk findings to runtime evidence.

## Policy Enforcement

Use:
- SRC-XACML
- SRC-NIST-800-162

Draft note:
Policy enforcement and authorization models provide background for policy decisions. AEP records simple allow/deny decisions but does not define a full policy language.

## FDO and Data Spaces

Use:
- SRC-FDOF
- SRC-FDO-REQ
- SRC-IDS-RAM

Draft note:
These sources support the framing of AEP bundle as a future FDO-style evidence object in data-space settings. The prototype does not implement an FDO registry, PID binding, IDS connector, or data usage control.
