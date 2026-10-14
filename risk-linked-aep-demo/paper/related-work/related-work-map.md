# Related Work Map

## Purpose

This document maps neighboring research and standards areas to the Risk-linked AEP contribution. It is not a final Related Work section and does not include invented citations.

## Core Position

Risk-linked AEP is positioned between pre-execution risk identification and post-execution accountability. It does not replace scanners, provenance models, policy engines, or FDO infrastructure. It defines a minimal evidence profile and validator path for linking risk findings to concrete execution evidence.

## Related Areas

### 1. Provenance

Provenance helps describe how entities, activities, and agents are related. AEP overlaps with provenance by recording execution evidence and preserving relationships between an agent run, event records, and evidence artifacts. AEP differs by emphasizing tool-call attempts, policy decisions, risk references, and validation outcomes.

[Needs citation: W3C PROV]

### 2. Audit Logging and Secure Logging

Audit logs record events for later review. Secure logging emphasizes integrity and tamper evidence. AEP overlaps through hash-chained event logs and `event_log_hash`. AEP differs by explicitly linking scanner findings, policy decisions, and validator outcomes.

[Needs citation: audit logging / secure logging]

### 3. Static Analysis and SARIF

Static analysis reports potential defects or risks before execution. SARIF can represent scanner outputs in a standardized form. AEP currently uses normalized risk reports. Future work may define SARIF-to-`risk_links` mapping. AEP does not implement SARIF in the current prototype.

[Needs citation: OASIS SARIF]

### 4. Agent Security Scanning

Agent scanners can identify risky tools, configurations, permissions, or deployment settings. Scanner output alone does not prove what happened during a specific run. AEP complements scanners by preserving execution evidence and risk-trigger linkage.

[Needs citation: agent security scanning literature]

### 5. Policy Enforcement

Policy systems decide whether actions are allowed or denied. AEP records `policy_decision` and `execution_status`. AEP does not define a full policy language. The current prototype only supports simple `allowed_tools` and `denied_tools`.

[Needs citation: policy enforcement literature]

### 6. FAIR Digital Objects / FDO

FDO-style framing is relevant because evidence objects need identifiers, profile declarations, metadata, integrity references, and relation links. The AEP bundle can be shaped as a future FDO-style evidence object. The current prototype does not implement a real FDO registry or PID binding.

[Needs citation: FAIR Digital Object Framework]

### 7. Data Spaces and Accountable Data Exchange

Data spaces emphasize controlled and trusted data exchange. Accountable agent execution evidence may support review of automated operations in such environments. AEP provides an evidence object shape, not a full data-space infrastructure.

[Needs citation: IDS / data spaces]

## Summary

The contribution of Risk-linked AEP is not to replace these areas, but to provide a minimal bridge between potential risk reports and actual execution evidence.
