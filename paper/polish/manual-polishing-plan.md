# Manual Polishing Plan

## Purpose

This plan translates simulated review feedback into manual polishing tasks. It does not modify the frozen v0.1 artifact and does not authorize implementation, profile semantic, validator, or demo changes.

## Polishing Status

Current status: ready for manual polishing planning.
High issues: 0.
Implementation changes required: 0.
Profile semantic changes required: 0.
Validator semantic changes required: 0.

## Polishing Priorities

| Priority | Issues | Goal |
| --- | --- | --- |
| Medium | M1-M8 | Clarify profile, security assumptions, validator rationale, and citation/artifact handling. |
| Low | L1-L4 | Improve formatting, examples, and concision. |
| Out of scope | platform / scanner / SARIF parser / MCP / FDO registry / LLM / production signing | Do not implement during v0.1. |

## Recommended Manual Polishing Order

1. Clarify blocked action as FAIL.
2. Clarify collector trust assumption.
3. Clarify direct target-to-tool matching.
4. Clarify mandatory/optional field boundary.
5. Clarify policy_id trust and binding boundary.
6. Add privacy non-claim for input/output hashes.
7. Compress repeated caveats.
8. Convert source IDs and repository references.
9. Unify figure/table numbering.
10. Shorten artifact appendix if needed.

## Files to Edit Later

- `paper/draft/full-paper-draft.md`
- `paper/draft/model-section-draft.md`
- `paper/draft/evaluation-section-draft.md`
- `paper/draft/discussion-limitations-draft.md`
- `paper/draft/prototype-implementation-draft.md`
- `paper/abstract-draft.md`
- `paper/references/source-inventory.md`
- final bibliography file, only after manual verification

These files should not be edited in Phase 20.

## Files Not to Edit During v0.1 Freeze

- `paper/aep-profile-v0.1.md`
- `profile/*.schema.json`
- `agent/`
- `collector/`
- `validator/`
- `demo/`
- `scripts/`
- generated validator behavior
- PASS / WARN / FAIL semantics

## Recommended Next Decision

After Phase 20, choose one:
A. Share the frozen v0.1 review release as-is.
B. Create a separate manual-polish copy or branch.
C. Initialize git manually, commit v0.1-review, then open a manual-polish branch.

Do not perform any of these actions automatically.
