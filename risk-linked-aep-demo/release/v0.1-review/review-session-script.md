# Review Session Script

## Purpose

This script gives a reviewer or collaborator a 30-60 minute review path.

## 10-minute Quick Check

1. Read `release/v0.1-review/external-reviewer-brief.md`.
2. Run `python3 demo/run_all.py`.
3. Run `python3 scripts/acceptance_check.py`.
4. Confirm PASS / WARN / FAIL.
5. Inspect `runs/fail/aep-events.jsonl`.

## 30-minute Review

1. Complete the 10-minute quick check.
2. Read `paper/aep-profile-v0.1.md`.
3. Read `paper/validator-rules.md`.
4. Inspect `runs/*/validation-report.json`.
5. Read `release/v0.1-review/scope-and-nonclaims.md`.
6. Record feedback in `reviewer-feedback-template.md`.

## 60-minute Review

1. Complete the 30-minute review.
2. Read `paper/draft/full-paper-consistency-audit.md`.
3. Skim `paper/draft/full-paper-draft.md`.
4. Check whether related-work positioning is clear.
5. Check whether Future Work is bounded.
6. Fill the priority issue table in the feedback template.

## Evidence Inspection Commands

```bash
cat runs/pass/validation-report.json
cat runs/warn/validation-report.json
cat runs/fail/validation-report.json
cat runs/fail/aep-events.jsonl
```

## What Not to Review Yet

- final citation formatting
- final venue formatting
- production security hardening
- real scanner integration
- SARIF parser
- FDO registry implementation
- dashboard or platform design
