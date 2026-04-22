# Review Checklist

## Artifact Review

- [ ] Repository can run `python3 demo/run_all.py`.
- [ ] Repository can run `python3 scripts/acceptance_check.py`.
- [ ] PASS scenario returns PASS.
- [ ] WARN scenario returns WARN.
- [ ] FAIL scenario returns FAIL.
- [ ] FAIL scenario records `write_file` as blocked.
- [ ] `runs/fail/blocked-write.txt` is absent.

## Profile Review

- [ ] `paper/aep-profile-v0.1.md` reads as a profile/specification note.
- [ ] Bundle model is understandable.
- [ ] Event model is understandable.
- [ ] Integrity model is understandable.
- [ ] Risk linkage model is understandable.
- [ ] FDO/data-space interpretation is clearly bounded.
- [ ] Version boundary is explicit.

## Validator Review

- [ ] All six validator rules are documented.
- [ ] PASS/WARN/FAIL aggregation is understandable.
- [ ] WARN is clearly distinguished from FAIL.
- [ ] Blocked denied action still counts as FAIL.
- [ ] Validator output is machine-readable.

## Paper Review

- [ ] `paper/draft/full-paper-draft.md` contains all major sections.
- [ ] `paper/draft/full-paper-consistency-audit.md` reports PASS or PASS WITH MINOR FIXES.
- [ ] Source IDs are clearly placeholders.
- [ ] Repository references are traceable.
- [ ] No final bibliography is claimed.

## Scope Review

- [ ] No production readiness claim.
- [ ] No compliance certification claim.
- [ ] No real-world benchmark claim.
- [ ] No real scanner integration claim.
- [ ] No SARIF implementation claim.
- [ ] No MCP runtime claim.
- [ ] No FDO registry claim.
- [ ] No IDS connector claim.
- [ ] No production signing claim.
- [ ] No platform claim.
