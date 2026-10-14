# Architecture Figure

The prototype separates potential risk, runtime evidence, and validation.

```text
Scanner risk report
  - normalized finding targets write_file
  - severity is info, low, medium, high, or critical

Demo agent runtime
  - calls tools only through the AEP collector
  - does not call an LLM

AEP collector
  - checks policy before execution
  - blocks denied tools
  - writes hash-chained JSONL events

AEP bundle
  - references the scanner findings
  - references the event log hash
  - includes a lightweight FDO-style identifier block

AEP validator
  - checks minimal structure
  - verifies the event hash chain
  - verifies the event log hash
  - distinguishes PASS, WARN, and FAIL
```

The bundle is intended to behave like a small evidence object that can be preserved or referenced by future FDO and data-space workflows.
