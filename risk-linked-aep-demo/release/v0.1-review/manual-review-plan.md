# Manual Review Plan

Reviewer-facing handoff materials are listed in `REVIEW_HANDOFF.md`.

## Review Order

1. `release/v0.1-review/README.md`
2. `release/v0.1-review/reproducibility-instructions.md`
3. `paper/aep-profile-v0.1.md`
4. `paper/draft/full-paper-consistency-audit.md`
5. `paper/draft/full-paper-draft.md`
6. `release/v0.1-review/review-checklist.md`
7. `release/v0.1-review/scope-and-nonclaims.md`

## Reviewer Questions to Answer

- Is the AEP profile understandable?
- Is the distinction between potential risk, WARN, and FAIL clear?
- Is the validator logic reviewable?
- Is the FDO/data-space framing bounded?
- Are the non-claims explicit enough?
- Are source IDs and repository references traceable?
- Is the reproducibility path clear?
- Does the paper overclaim anywhere?

## Manual Paper Polishing Tasks

- reduce repeated caveats
- improve transitions between sections
- convert source IDs to final citation format
- decide whether repository references become appendix entries or artifact citations
- align terminology with target venue
- shorten if required by venue limit
- decide final figure and table numbering

## Manual Artifact Review Tasks

- run reproduction commands on a clean machine
- inspect FAIL event manually
- inspect validation reports
- inspect AEP bundle and event log examples
- verify release package links
- decide whether to include generated `runs/` artifacts in an external artifact package
