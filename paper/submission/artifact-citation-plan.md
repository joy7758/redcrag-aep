# Artifact Citation Plan

## Purpose

Repository references in the current draft identify internal artifacts that support the argument. They must later be converted into a consistent artifact citation or appendix treatment.

## Artifact Types

| Artifact type | Example | Suggested final treatment |
| --- | --- | --- |
| Profile note | `paper/aep-profile-v0.1.md` | Appendix / supplementary artifact citation. |
| Validator rules note | `paper/validator-rules.md` | Appendix / supplementary artifact citation. |
| Review pack | `REVIEW_PACK.md` | Artifact appendix or supplementary material. |
| Generated validator report | `runs/fail/validation-report.json` | Artifact evidence example, not normal bibliography. |
| Generated event log | `runs/fail/aep-events.jsonl` | Artifact evidence example, not normal bibliography. |
| Release package docs | `release/v0.1-review/*` | Review appendix or supplementary package. |
| Polish plans | `paper/polish/*` | Normally not cited in final submission, internal preparation only. |

## Recommended Treatment

- Keep artifact citations separate from literature citations.
- Use appendix or supplementary section for local artifact references.
- Avoid citing internal planning files in final paper body unless necessary.
- Generated run artifacts should be treated as reproducible evidence examples, not standard references.

## Open Decisions

- Whether the target venue supports artifact appendices.
- Whether repository references should be footnotes, appendix labels, or supplementary links.
- Whether generated runs should be included in supplementary material or reproduced on demand.
