# Section Source Map

| Paper section | Main source file(s) | Repository artifact(s) | Notes |
| --- | --- | --- | --- |
| Full Paper Assembly | `paper/draft/full-paper-draft.md` plus all section drafts | `paper/draft/*`, `paper/references/*`, repository artifacts | Controlled assembly draft; final citations and venue formatting remain pending. |
| Abstract | `paper/abstract-draft.md`, `paper/draft/introduction-draft.md`, `paper/draft/evaluation-section-draft.md` | `paper/draft/*` | Refined abstract; final citation formatting not included. |
| Introduction | `paper/contribution-statement.md`, `paper/draft/argument-flow.md`, `paper/draft/introduction-draft.md` | `README.md`, `REVIEW_PACK.md`, demo outputs | Controlled Introduction draft; final citations require manual completion. |
| Background and Motivation | `paper/contribution-statement.md`, `paper/research-scope.md` | `scanner-output/*.json`, `profile/*.schema.json` | Do not invent external citations in the skeleton. |
| Related Work | `paper/related-work/*`, `paper/references/*`, `paper/draft/related-work-draft.md` | `paper/references/source-inventory.md` | Controlled draft using source IDs only; final citations require manual completion. |
| Risk-linked AEP Model | `paper/aep-profile-v0.1.md`, `paper/validator-rules.md`, `paper/draft/model-section-draft.md` | `profile/*.schema.json`, `validator/rules.py`, `runs/*/aep-bundle.json`, `runs/*/aep-events.jsonl` | Controlled model-section draft; profile note remains source of truth. |
| Prototype Implementation | `README.md`, `REVIEW_PACK.md`, `paper/draft/prototype-implementation-draft.md` | `agent/`, `collector/`, `validator/`, `demo/`, `scripts/`, `scanner-output/`, `runs/` | Controlled implementation-section draft; implementation remains deterministic and minimal. |
| Evaluation | `paper/evaluation-section.md`, `paper/evaluation-notes.md`, `paper/draft/evaluation-section-draft.md` | `demo/`, `scripts/`, `validator/`, `runs/*/validation-report.json`, `runs/*/aep-events.jsonl` | Controlled evaluation-section draft; results remain deterministic. |
| Discussion | `paper/draft/discussion-limitations-draft.md`, `paper/draft/argument-flow.md`, `paper/draft/evaluation-section-draft.md` | `runs/*/validation-report.json`, `runs/*/aep-events.jsonl` | Controlled discussion draft; interpretation remains bounded. |
| Limitations | `paper/draft/discussion-limitations-draft.md`, `paper/research-scope.md`, `paper/aep-profile-v0.1.md` | `README.md`, `REVIEW_PACK.md` | Controlled limitations draft; no production readiness claim. |
| Future Work | `paper/research-scope.md` | `profile/*.schema.json` | Use only the five scoped future-work items. |
| Conclusion | `paper/draft/conclusion-draft.md`, `paper/draft/discussion-limitations-draft.md`, `paper/research-scope.md` | demo outputs, `runs/*/validation-report.json` | Controlled conclusion draft; no production readiness claim. |
