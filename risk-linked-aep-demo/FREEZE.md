# Repository Freeze: v0.1 Review Release

## Freeze Status

The repository is frozen for v0.1 review release.

This means:
- implementation behavior should not change
- AEP v0.1 profile semantics should not change
- demo scenarios should not change
- validator rules should not change
- paper assembly draft should not be rewritten
- release review package should remain stable

## Frozen Core

- `profile/`
- `agent/`
- `collector/`
- `validator/`
- `demo/`
- `scripts/`
- `paper/aep-profile-v0.1.md`
- `paper/draft/full-paper-draft.md`
- `paper/draft/full-paper-consistency-audit.md`
- `release/v0.1-review/`

## Allowed Changes After Freeze

- typo fixes
- broken internal link fixes
- formatting fixes that do not change meaning
- reproducibility bug fixes
- documentation corrections for factual inconsistency
- citation formatting work after manual source verification
- venue-specific paper formatting in a later branch or copy

## Not Allowed After Freeze

- adding new features
- changing demo scenario logic
- changing PASS / WARN / FAIL semantics
- changing validator rule meaning
- changing AEP v0.1 field semantics
- adding real scanner integration
- adding SARIF parser
- adding MCP runtime
- adding FDO registry
- adding IDS connector
- adding LLM agent
- adding database
- adding web UI
- adding Docker deployment
- adding production signing
- adding compliance claims
- adding production-readiness claims
- adding new future-work items outside the approved five

## Freeze Verification Commands

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

## Current Known Git State

At the time of Phase 16, this directory was not a git worktree. Git initialization or tagging should be a separate explicit decision and should not be performed automatically.
