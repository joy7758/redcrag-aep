# Feedback Incorporation Plan

## Purpose

This document plans how to incorporate simulated review feedback without breaking the v0.1 freeze boundary. It is a planning document only. It does not authorize implementation changes, profile semantic changes, validator changes, or scope expansion.

## Incorporation Summary

| Issue ID | Category | Priority | Freeze-safe? | Implementation change? | Profile semantic change? | Planned handling |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | profile clarity | Medium | Yes | No | No | Add mandatory/optional explanation later. |
| M2 | risk linkage clarity | Medium | Yes | No | No | Clarify direct target-to-tool matching and future mapping boundary. |
| M3 | policy context clarity | Medium | Yes | No | No | Clarify policy_id is review context, not registry-bound policy object. |
| M4 | security assumption | Medium | Yes | No | No | Add collector mediation trust assumption in limitations/threat model text. |
| M5 | validator rationale | Medium | Yes | No | No | Clarify denied action attempt is violation even if blocked. |
| M6 | privacy non-claim | Medium | Yes | No | No | Clarify hashes reduce stored content but do not provide privacy-preserving disclosure. |
| M7 | paper polishing | Medium | Yes | No | No | Reduce repeated caveats during manual polishing. |
| M8 | citation/artifact formatting | Medium | Yes | No | No | Convert source IDs and repository refs during final citation work. |
| L1 | formatting | Low | Yes | No | No | Unify figure/table numbering later. |
| L2 | artifact appendix | Low | Yes | No | No | Shorten appendix during venue formatting. |
| L3 | paper clarity | Low | Yes | No | No | Optionally add WARN example. |
| L4 | paper clarity | Low | Yes | No | No | Optionally shorten FDO/data-space discussion. |

## Must Fix Before Sharing

No High issues were identified.
No must-fix implementation or profile issues are required before v0.1 research review sharing.

## Clarifications Before Submission

1. Clarify mandatory vs optional profile fields.
2. Clarify direct target-to-tool matching limit.
3. Clarify policy_id trust and binding boundary.
4. Clarify collector mediation trust assumption.
5. Clarify why blocked denied action still counts as FAIL.
6. Clarify input/output hashes are not privacy-preserving disclosure.
7. Compress repeated caveats.
8. Convert source IDs and repository references to final citation/artifact format.

## Future Work Alignment

Some feedback aligns with already scoped future work, especially:
- SARIF-to-risk_links mapping
- optional FDO PID binding
- profile vocabulary refinement

Do not add new future work items.

1. Refine AEP schema vocabulary.
2. Define a SARIF-to-risk_links mapping.
3. Add optional FDO PID binding.
4. Write a full paper draft.
5. Prepare a small standards discussion note.

## Out-of-Scope Feedback Handling

If future reviewers ask for platform, dashboard, production scanner, MCP runtime, LLM benchmark, real FDO registry, IDS connector, database, web UI, Docker deployment, or production signing, classify the request as out of scope for v0.1.

| Request type | Phase 19 decision |
| --- | --- |
| Platform / dashboard | Out of scope |
| Real scanner integration | Out of scope |
| SARIF parser implementation | Future work only, not current implementation |
| MCP runtime | Out of scope |
| LLM benchmark | Out of scope |
| FDO registry | Out of scope |
| IDS connector | Out of scope |
| Database / web UI | Out of scope |
| Production signing | Out of scope |

## Freeze-safe Changes Later

- documentation clarification
- limitation clarification
- citation formatting after manual verification
- artifact reference formatting
- typo / broken link fixes
- venue-specific paper formatting

## Not Freeze-safe

- changing AEP field semantics
- changing validator rule semantics
- changing PASS / WARN / FAIL meanings
- adding demo scenarios
- adding new implementation features
- adding new dependencies
- expanding Future Work beyond the five approved items

## Recommended Next Step

Proceed to manual paper polishing only after deciding whether to incorporate the Medium clarifications into a separate polishing branch or copy. Do not modify implementation or profile semantics during v0.1 freeze.
