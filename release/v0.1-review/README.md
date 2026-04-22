# Risk-linked AEP v0.1 Review Release

## Purpose

This review release packages the Risk-linked Agent Evidence Profile prototype and paper draft materials. The artifact demonstrates a minimal path from scanner risk report to runtime execution evidence to validator result. It is intended for research review, profile discussion, and reproducibility checking. It is not a production system.

## Core Message

Scanner tells what may go wrong.
AEP records what actually happened.
Validator determines whether the execution is acceptable.
FDO/data-space environments can preserve and reference the resulting evidence object.

## What to Review First

1. `README.md`
2. `REVIEW_PACK.md`
3. `release/v0.1-review/artifact-manifest.md`
4. `release/v0.1-review/reproducibility-instructions.md`
5. `paper/aep-profile-v0.1.md`
6. `paper/draft/full-paper-draft.md`
7. `paper/draft/full-paper-consistency-audit.md`

## Quick Reproduction

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

## Release Contents

- artifact manifest
- reproducibility instructions
- review checklist
- paper draft index
- release notes
- scope and non-claims

## Freeze Guidance

- `FREEZE.md`
- `release/v0.1-review/freeze-checklist.md`
- `release/v0.1-review/freeze-status.md`
- `release/v0.1-review/manual-review-plan.md`
- `release/v0.1-review/git-next-steps.md`

## Manual Review Handoff

- `REVIEW_HANDOFF.md`
- `release/v0.1-review/external-reviewer-brief.md`
- `release/v0.1-review/reviewer-feedback-template.md`
- `release/v0.1-review/review-session-script.md`
- `release/v0.1-review/feedback-triage-guide.md`
- `release/v0.1-review/reviewer-nonclaims.md`

## Simulated Review and Feedback Planning

- `release/v0.1-review/simulated-review-round-1.md`
- `release/v0.1-review/feedback-incorporation-plan.md`
