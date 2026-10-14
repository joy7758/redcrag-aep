# Manual Review Handoff

## Purpose

This document is the top-level handoff for reviewers. The artifact is a v0.1 review release of a Risk-linked Agent Evidence Profile prototype. The review should focus on evidence linkage, profile clarity, validator logic, reproducibility, and scope boundaries. The review should not treat the project as a production system.

## Core Claim

Risk-linked AEP provides a minimal way to connect pre-execution risk findings with runtime execution evidence so that a validator can distinguish PASS, WARN, and FAIL accountability states.

## What to Review First

1. `release/v0.1-review/external-reviewer-brief.md`
2. `release/v0.1-review/reproducibility-instructions.md`
3. `paper/aep-profile-v0.1.md`
4. `paper/draft/full-paper-consistency-audit.md`
5. `paper/draft/full-paper-draft.md`
6. `release/v0.1-review/reviewer-feedback-template.md`

## Reproduction Commands

```bash
python3 demo/run_all.py
python3 scripts/acceptance_check.py
make demo
make acceptance
```

## Expected Result

| Scenario | Expected | Actual | Status |
| -------- | -------- | ------ | ------ |
| PASS     | PASS     | PASS   | OK     |
| WARN     | WARN     | WARN   | OK     |
| FAIL     | FAIL     | FAIL   | OK     |

## Main Review Questions

- Is the AEP profile understandable as a minimal profile?
- Is the distinction between potential risk, WARN, and FAIL clear?
- Is the validator logic reviewable?
- Is the FDO/data-space framing useful but bounded?
- Does the paper overclaim?
- Are the non-claims clear enough?
- Is the reproducibility path clear?

## Feedback Format

Use `release/v0.1-review/reviewer-feedback-template.md`.

A simulated review and feedback incorporation plan are available in `release/v0.1-review/simulated-review-round-1.md` and `release/v0.1-review/feedback-incorporation-plan.md`.
