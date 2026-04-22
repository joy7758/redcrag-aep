# Reviewer Feedback Template

## Reviewer Information

- Name:
- Affiliation:
- Review date:
- Review role:
  - profile reviewer
  - implementation reviewer
  - paper reviewer
  - standards reviewer
  - other

## Reproducibility Check

- [ ] I ran `python3 demo/run_all.py`.
- [ ] I ran `python3 scripts/acceptance_check.py`.
- [ ] PASS returned PASS.
- [ ] WARN returned WARN.
- [ ] FAIL returned FAIL.
- [ ] I inspected the FAIL blocked `write_file` event.
- [ ] I could reproduce the expected result table.

Notes:

## Profile Review

Questions:

1. Is the AEP bundle model clear?
2. Is the event model clear?
3. Is the risk linkage model clear?
4. Is the integrity model clear?
5. Are mandatory vs future fields sufficiently clear?
6. What profile fields should be renamed, removed, or clarified?

Feedback:

## Validator Review

Questions:

1. Are the six validator rules understandable?
2. Is WARN clearly distinct from FAIL?
3. Is it reasonable that blocked denied action still counts as FAIL?
4. Are the rule outputs useful for review?
5. Which validator rule needs stronger justification?

Feedback:

## Paper Review

Questions:

1. Is the research gap clear?
2. Are the contributions narrow and defensible?
3. Does the paper overclaim anywhere?
4. Is the FDO/data-space framing clear but bounded?
5. Is the evaluation convincing for a minimal prototype?
6. What should be shortened, expanded, or moved to appendix?

Feedback:

## Scope and Non-claims Review

- [ ] No production readiness claim.
- [ ] No compliance certification claim.
- [ ] No real-world benchmark claim.
- [ ] No attack prevention claim.
- [ ] No full scanner integration claim.
- [ ] No SARIF implementation claim.
- [ ] No MCP runtime claim.
- [ ] No FDO registry claim.
- [ ] No IDS connector claim.
- [ ] No production signing claim.
- [ ] No platform claim.

Feedback:

## Priority Issues

| Priority | Issue | Suggested action |
| -------- | ----- | ---------------- |
| High     |       |                  |
| Medium   |       |                  |
| Low      |       |                  |

## Overall Recommendation

- [ ] Ready for manual paper polishing
- [ ] Needs minor clarification
- [ ] Needs profile revision
- [ ] Needs implementation fix
- [ ] Needs substantial rework

Comments:
