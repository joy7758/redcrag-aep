# Citation Conversion Plan

## Purpose

Source IDs in the current paper draft are placeholders and must be converted manually to final citation format after source verification.

## Current Placeholder Types

| Placeholder type | Example | Current meaning | Final action needed |
| --- | --- | --- | --- |
| Source ID | `[SRC-SARIF]` | Points to verified source inventory entry. | Convert to final bibliography citation. |
| Repository reference | `[Repository: paper/aep-profile-v0.1.md]` | Points to local artifact. | Convert to artifact citation, appendix entry, or supplementary reference. |
| Local draft reference | `[Repository: paper/research-scope.md]` | Internal draft support. | Resolve into final manuscript prose or artifact appendix reference. |

## Conversion Rules

- Do not convert placeholders without manual source verification.
- Use `paper/references/source-inventory.md` as source of truth.
- Use `paper/references/claim-to-source-map.md` to confirm claim alignment.
- Do not fabricate authors, years, DOIs, or BibTeX.
- Prefer primary standards/source documents for standards claims.
- Distinguish literature citations from artifact citations.

## Open Decisions

- Final citation style depends on venue.
- Repository references may become appendix citations or supplementary artifact references.
- Some internal draft references may disappear after final prose integration.
