# Merge Decision Note

## Purpose

This note records how to decide whether manual-polish should be merged into main.

## Current Facts

- `v0.1-review` tag points to the frozen artifact commit.
- `manual-polish` contains documentation-only clarifications.
- `manual-polish` does not change code, profile semantics, validator semantics, demo logic, or release tag state.
- `manual-polish` improves clarity for external review and later submission.

## Merge Options

| Option | Meaning | Recommended when |
| --- | --- | --- |
| Keep manual-polish separate | main stays closer to frozen artifact; manual-polish used for review/submission work | if the project wants a sharp distinction between frozen artifact and polished draft |
| Merge manual-polish into main | main becomes the default clearer documentation branch; v0.1-review tag still preserves frozen artifact | if the project wants the clearer paper/docs state visible by default |
| Create a separate submission copy later | main and manual-polish stay intact; a later copy handles venue formatting | if venue constraints require heavier reshaping |

## Recommendation

Merging manual-polish into main is acceptable because the changes are documentation-only and the v0.1-review tag remains the authoritative frozen artifact. However, this should be a deliberate decision after confirming no further clarification-only changes are planned.

## Do Not Do

- do not move the v0.1-review tag
- do not retag a later commit as v0.1-review
- do not merge if there are still unresolved clarification edits
- do not interpret the merge as artifact freeze replacement
