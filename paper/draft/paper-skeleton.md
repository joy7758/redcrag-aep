# Risk-linked Agent Evidence Profile for Verifiable Agent Execution Accountability

Full assembly draft available in `paper/draft/full-paper-draft.md`.

# Title

Risk-linked Agent Evidence Profile for Verifiable Agent Execution Accountability

# Abstract

Updated abstract available in `paper/abstract-draft.md`.

Agent security scanners can identify potential risks in tools, configurations, and runtime settings, but scanner output alone does not prove what happened during a concrete execution. This paper introduces a Risk-linked Agent Evidence Profile (AEP), a minimal evidence structure for linking pre-execution security findings with runtime execution evidence. The prototype records an event-level evidence trace for tool-call attempts and a manifest-level bundle that references the trace, the policy, and normalized scanner findings. It uses hash-chain integrity over events, an event log hash in the bundle, and explicit risk linkage from scanner finding targets to executed or attempted tools. A validator consumes the bundle, event log, and risk report to produce PASS, WARN, or FAIL conclusions. PASS indicates acceptable execution, WARN indicates potential risk that was not triggered, and FAIL indicates observed violation or integrity failure. The work is positioned for FDO and data-space accountability contexts, where evidence objects may need to be preserved, referenced, and reviewed. A deterministic prototype evaluates three scenarios: no high-risk finding, high-risk `write_file` finding without execution, and attempted `write_file` execution blocked by policy.

# Keywords

- agent execution evidence
- accountability
- risk linkage
- FDO
- data spaces
- validation
- provenance

# 1. Introduction

Expanded draft available in `paper/draft/introduction-draft.md`.

## 1. Introduction

### 1.1 Motivation

- Draft point: Agent systems require evidence that can be reviewed after execution, especially when tool use may affect local files or external resources.
- Evidence/source: `paper/contribution-statement.md`, `REVIEW_PACK.md`
- Expansion needed: Add concise context about why agent execution accountability matters in evidence-preserving environments.

### 1.2 Problem Gap

- Draft point: Scanner findings describe possible risks, while runtime logs describe behavior; neither alone provides a risk-linked, integrity-aware execution evidence object.
- Evidence/source: `paper/contribution-statement.md`
- Expansion needed: Clarify the gap between potential risk, actual execution evidence, and validator conclusions.

### 1.3 Research Question

How can agent execution evidence be linked with pre-execution security findings to support verifiable accountability in FDO and data-space environments?

### 1.4 Contributions

1. A minimal Risk-linked Agent Evidence Profile.
2. A validator that distinguishes PASS, WARN, and FAIL accountability states.
3. A deterministic prototype showing potential risk, untriggered risk, and triggered violation.

### 1.5 Paper Structure

The paper first motivates the gap between scanner findings and execution evidence. It then defines the Risk-linked AEP model, describes the deterministic prototype implementation, evaluates the PASS/WARN/FAIL scenarios, and discusses limitations and future work.

# 2. Background and Motivation

## 2. Background and Motivation

### 2.1 Agent Security Scanning

Security scanners identify potential risks in agent configurations, tools, or runtime settings. These findings describe what may go wrong, but scanner findings alone do not prove concrete execution behavior. This prototype uses normalized scanner reports as inputs and does not claim real scanner integration.

### 2.2 Execution Evidence and Accountability

Runtime logs alone are often insufficient for accountability because they may lack integrity structure, policy linkage, and risk linkage. Execution evidence needs to show what was attempted, how policy responded, whether execution occurred, and which pre-execution risks were touched.

### 2.3 FDO and Data-space Context

Evidence objects in FDO and data-space contexts need identifiers, profile declarations, integrity references, and relation links. This prototype shapes the AEP bundle as a future FDO-style evidence object. No FDO registry is implemented.

# 3. Risk-linked AEP Model

Expanded draft available in `paper/draft/model-section-draft.md`.

## 3. Risk-linked AEP Model

### 3.1 Design Goal

The design goal is a minimal evidence structure for deterministic review of agent execution accountability. The model links pre-execution risk findings to runtime evidence while keeping the bundle and event log small enough for profile review.

### 3.2 Bundle Model

The bundle model includes `aep_version`, `bundle_id`, `fdo`, `agent`, `execution`, `policy`, `risk_links`, `evidence`, and `integrity`. These fields identify the profile version, evidence object, lightweight FDO-style reference, agent, execution, policy context, scanner findings, event log reference, and integrity metadata.

[Table 1: AEP bundle fields]

### 3.3 Event Model

The event model includes `event_id`, `run_id`, `timestamp`, `actor`, `action`, `tool`, `input_hash`, `output_hash`, `policy_decision`, `execution_status`, `risk_refs`, `prev_event_hash`, and `event_hash`. Each event represents a tool-call attempt and records policy, execution, risk-linkage, and hash-chain evidence.

[Table 2: AEP event fields]

### 3.4 Integrity Model

`event_hash` is computed from canonical event JSON excluding `event_hash`. `prev_event_hash` links each event to the previous event. `event_log_hash` binds the manifest-level bundle to the JSONL event trace. The demo HMAC signature is an authenticity marker only and is not production key management.

### 3.5 Risk Linkage Model

The scanner finding target maps to `event.tool`. `risk_refs` connect event-level evidence to touched findings. `risk_links` preserve scanner findings at bundle level. This enables distinguishing:
- no high-risk finding
- high-risk finding present but not triggered
- high-risk target attempted

### 3.6 FDO / Data-space Interpretation

[Table 3: AEP-to-FDO/data-space mapping]

This prototype does not implement an FDO registry. It only shapes the AEP bundle as a future FDO-style evidence object.

# 4. Prototype Implementation

Expanded draft available in `paper/draft/prototype-implementation-draft.md`.

## 4. Prototype Implementation

### 4.1 Repository Structure

The repository separates profile artifacts, scanner inputs, agent behavior, collection, validation, demonstration, generated runs, and paper materials:
- `profile/`
- `scanner-output/`
- `agent/`
- `collector/`
- `validator/`
- `demo/`
- `runs/`
- `paper/`

### 4.2 Demo Agent

The prototype uses a deterministic non-LLM agent. It exposes three tools: `read_file`, `summarize_text`, and `write_file`. Policy allows `read_file` and `summarize_text`, and denies `write_file`.

### 4.3 AEP Collector

The AEP collector wraps tool calls, records event evidence, enforces allowed and denied tool decisions, blocks denied tool execution, and generates `aep-events.jsonl` and `aep-bundle.json`.

### 4.4 Validator

The validator applies six rules:
- `V1_SCHEMA_MINIMAL`
- `V2_HASH_CHAIN`
- `V3_EVENT_LOG_HASH`
- `V4_POLICY_ATTEMPT`
- `V5_RISK_TRIGGER`
- `V6_DENIED_TOOL_BLOCKED`

[Table 4: Validator rules]

# 5. Evaluation

Expanded draft available in `paper/draft/evaluation-section-draft.md`.

## 5. Evaluation

### 5.1 Evaluation Goal

The evaluation checks whether the prototype can distinguish three accountability states: safe execution, potential-but-untriggered risk, and triggered violation.

### 5.2 Scenarios

[Table 5: Evaluation scenarios]

PASS:
- no high-risk finding
- only allowed tools used
- result PASS
- execution acceptable

WARN:
- high-risk `write_file` finding exists
- `write_file` not attempted
- result WARN
- potential risk present but not triggered

FAIL:
- high-risk `write_file` finding exists
- `write_file` attempted and blocked
- result FAIL
- attempted denied high-risk action observed

### 5.3 Results

| Scenario | Expected | Actual | Status |
| --- | --- | --- | --- |
| PASS | PASS | PASS | OK |
| WARN | WARN | WARN | OK |
| FAIL | FAIL | FAIL | OK |

### 5.4 Interpretation

PASS demonstrates normal evidence generation. WARN demonstrates the distinction between potential risk and actual execution. FAIL demonstrates attempted denied action can be captured and judged as violation even if blocked.

### 5.5 Reproducibility

```bash
make demo
make acceptance
```

Direct commands:

```bash
python3 demo/run_all.py
python3 scripts/acceptance_check.py
```

# 6. Discussion

Expanded draft available in `paper/draft/discussion-limitations-draft.md`.

## 6. Discussion

### 6.1 Why Risk Linkage Matters

Scanner findings become more useful when linked to concrete execution evidence. Potential risk and triggered violation should not be conflated, because a high-risk capability may exist without being attempted in a particular run.

### 6.2 Why Integrity Matters

The hash chain makes the event sequence reviewable. `event_log_hash` binds the manifest to the event trace. The demo signature marks authenticity but is not production-grade.

### 6.3 Role in FDO/Data-space Environments

The AEP bundle can be treated as an evidence object shape. Profile declaration, identifier, integrity reference, policy reference, and risk references support future preservation and exchange. No registry is implemented.

### 6.4 What the Prototype Demonstrates

The prototype demonstrates a minimal evidence-linkage mechanism under deterministic conditions. It does not demonstrate production compliance or real-world scanner coverage.

# 7. Limitations

Expanded draft available in `paper/draft/discussion-limitations-draft.md`.

- synthetic scanner reports
- deterministic non-LLM agent
- small tool set
- simple allow/deny policy model
- simple target-to-tool risk matching
- no SARIF mapping
- no MCP runtime
- no real FDO registry
- no production cryptographic signing
- no formal ontology
- no multi-agent workflow

# 8. Future Work

1. Refine AEP schema vocabulary.
2. Define a SARIF-to-risk_links mapping.
3. Add optional FDO PID binding.
4. Write a full paper draft.
5. Prepare a small standards discussion note.

# 9. Conclusion

Expanded draft available in `paper/draft/conclusion-draft.md`.

This paper skeleton centers on the distinction between potential risk and actual execution evidence. Scanners identify potential risk, AEP records actual execution evidence, and the validator distinguishes PASS, WARN, and FAIL outcomes. The prototype supports discussion of verifiable accountability in FDO and data-space contexts while remaining a minimal research artifact rather than a production compliance system.
