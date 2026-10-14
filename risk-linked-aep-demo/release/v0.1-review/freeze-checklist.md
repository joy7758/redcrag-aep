# v0.1 Freeze Checklist

## Implementation Freeze

- [ ] `python3 demo/run_all.py` passes.
- [ ] `python3 scripts/acceptance_check.py` passes.
- [ ] `make demo` passes.
- [ ] `make acceptance` passes.
- [ ] PASS scenario remains PASS.
- [ ] WARN scenario remains WARN.
- [ ] FAIL scenario remains FAIL.
- [ ] FAIL scenario still records blocked `write_file`.
- [ ] `runs/fail/blocked-write.txt` remains absent.

## Profile Freeze

- [ ] `paper/aep-profile-v0.1.md` is not modified.
- [ ] AEP bundle fields remain unchanged.
- [ ] AEP event fields remain unchanged.
- [ ] risk_links / risk_refs semantics remain unchanged.
- [ ] hash-chain semantics remain unchanged.
- [ ] FDO/data-space interpretation remains bounded.

## Paper Freeze

- [ ] `paper/draft/full-paper-draft.md` remains present.
- [ ] `paper/draft/full-paper-consistency-audit.md` remains present.
- [ ] Research question remains exact.
- [ ] Contributions remain exactly three.
- [ ] Future Work remains exactly five items.
- [ ] No References section is added before manual citation work.
- [ ] Source IDs remain placeholders until manually converted.

## Release Package Freeze

- [ ] `release/v0.1-review/README.md` exists.
- [ ] `release/v0.1-review/artifact-manifest.md` exists.
- [ ] `release/v0.1-review/reproducibility-instructions.md` exists.
- [ ] `release/v0.1-review/review-checklist.md` exists.
- [ ] `release/v0.1-review/paper-draft-index.md` exists.
- [ ] `release/v0.1-review/release-notes-v0.1.md` exists.
- [ ] `release/v0.1-review/scope-and-nonclaims.md` exists.

## Scope Freeze

- [ ] No production-readiness claim.
- [ ] No compliance certification claim.
- [ ] No real-world benchmark claim.
- [ ] No attack-prevention claim.
- [ ] No real scanner integration claim.
- [ ] No SARIF implementation claim.
- [ ] No MCP runtime claim.
- [ ] No FDO registry claim.
- [ ] No IDS connector claim.
- [ ] No production signing claim.
- [ ] No platform claim.
