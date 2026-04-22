# Feedback Triage Guide

## Purpose

This guide helps maintainers classify reviewer feedback without breaking the v0.1 freeze boundary.

## Feedback Categories

| Category | Meaning | Allowed action before unfreeze? |
| --- | --- | --- |
| Typo / wording | Small text issue that does not change meaning. | yes, if meaning unchanged |
| Broken link | Internal path or pointer does not work. | yes |
| Reproducibility bug | Existing reproduction command fails or generated evidence is inconsistent. | yes |
| Profile clarity issue | Reviewer cannot understand an existing profile field or boundary. | maybe, requires explicit review |
| Validator logic issue | Reviewer questions rule semantics or aggregation. | no code change before unfreeze; document issue |
| Paper argument issue | Reviewer questions gap, contribution, or evaluation argument. | yes, in paper draft only if no new claims |
| Citation formatting issue | Source IDs or references need final formatting. | yes, after manual verification |
| Scope creep suggestion | Suggestion expands beyond AEP v0.1 boundary. | no, record for later |
| New feature request | Suggestion adds product or implementation capability. | no |
| Productionization request | Suggestion moves toward deployment, platform, or compliance system. | no |

## Priority Levels

- High: affects reproducibility, correctness, or major overclaim.
- Medium: affects clarity, reviewer understanding, or paper structure.
- Low: wording, formatting, or optional improvement.

## Freeze-safe Actions

- fix typo
- fix broken link
- clarify non-claim
- clarify reviewer instruction
- document issue in open-items
- update citation placeholder after verification

## Not Freeze-safe Actions

- changing validator semantics
- changing AEP profile fields
- adding demo scenario
- adding real scanner integration
- adding SARIF parser
- adding FDO registry
- adding LLM agent
- adding dashboard
- adding production signing
- expanding future work list

## Triage Output Format

```text
Issue:
Category:
Priority:
Freeze-safe action:
Decision:
Owner:
Notes:
```
