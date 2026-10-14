# Risk-linked Agent Evidence Profile Demo

## Project Status

**v0.1-review frozen artifact**  
Tag: `v0.1-review`  
Commit: `841f7d6`  
Demo: PASS / WARN / FAIL reproducible  
Acceptance: PASS  

This repository contains a minimal research prototype for a **Risk-linked Agent Evidence Profile (AEP)**. It links pre-execution risk findings with runtime execution evidence and validates executions as PASS, WARN, or FAIL.

Not a production system. Not a compliance tool. Not a real scanner, SARIF, MCP, FDO registry, or data-space implementation.

Recommended entry points:

- `REVIEW_HANDOFF.md`
- `release/v0.1-review/README.md`
- `paper/aep-profile-v0.1.md`
- `paper/draft/full-paper-draft.md`

## Problem

Security scanners can identify potential risks, but they do not prove what actually happened during an agent execution.

## Contribution

This demo links pre-execution risk findings with runtime execution evidence and validator conclusions. A scanner report says what may go wrong, the AEP event log records what actually happened, and the validator decides whether the execution is acceptable.

## Architecture

```text
Scanner risk report
      ↓
Demo agent runtime
      ↓
AEP collector
      ↓
AEP bundle + event log
      ↓
AEP validator
      ↓
PASS / WARN / FAIL
```

## Run

```bash
python3 demo/run_all.py
```

You can also use the Makefile targets:

```bash
make demo
make acceptance
```

If the local system maps `python` to Python 3, `python demo/run_all.py` may also work.

## Expected Results

PASS:
- no high-risk scanner finding
- only allowed tools used

WARN:
- high-risk `write_file` finding exists
- `write_file` was not attempted

FAIL:
- high-risk `write_file` finding exists
- `write_file` was attempted
- collector blocked execution
- attempt still counts as violation

## Why This Matters

Scanner tells what may go wrong. AEP records what actually happened. Validator determines whether execution is acceptable. FDO/data-space environments can preserve and reference the resulting evidence object as an evidence profile for accountable agent execution.

## Paper-facing materials

The `paper/` directory contains research-facing notes for contribution framing, profile description, validator rules, evaluation, and scope control.

The `paper/draft/` directory contains a controlled paper skeleton for later manuscript development.

The `paper/related-work/` directory contains terminology and related-work positioning notes.

The `paper/references/` directory contains source inventory and claim-to-source mapping notes.

- `paper/contribution-statement.md`
- `paper/aep-profile-v0.1.md`
- `paper/validator-rules.md`
- `paper/evaluation-section.md`
- `paper/research-scope.md`
- `paper/abstract-draft.md`

## v0.1 review release

Review-release materials are available in `release/v0.1-review/`.

Freeze guidance is available in `FREEZE.md` and `release/v0.1-review/freeze-checklist.md`.
Manual review handoff is available in `REVIEW_HANDOFF.md`.

- `release/v0.1-review/README.md`
- `release/v0.1-review/artifact-manifest.md`
- `release/v0.1-review/reproducibility-instructions.md`
- `release/v0.1-review/review-checklist.md`
- `release/v0.1-review/paper-draft-index.md`
- `release/v0.1-review/release-notes-v0.1.md`
- `release/v0.1-review/scope-and-nonclaims.md`

## Scope Limits

- no real scanner integration
- no real FDO registry
- no production cryptographic signing
- no LLM runtime
- no MCP integration

The signature is a demo HMAC-SHA256 value using a fixed secret in source code. It is not production key management and must not be treated as a real trust mechanism.
