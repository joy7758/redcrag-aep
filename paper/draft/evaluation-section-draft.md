# Evaluation Section Draft

This is a controlled evaluation-section draft based on the deterministic repository demo. It documents what the prototype demonstrates under controlled conditions and must not be read as a real-world benchmark or production validation.

Citation and artifact note: repository references in this draft are placeholders for review. They should be converted into final artifact citations, appendix references, or supplementary-material references before submission.

## 5. Evaluation

The evaluation checks whether the prototype distinguishes three accountability states: safe execution, potential-but-untriggered risk, and triggered violation. The evaluation is deterministic and reproducible. It is not a real-world deployment benchmark, and it does not measure scanner quality, model quality, performance, or scalability [Repository: paper/evaluation-section.md].

## 5.1 Evaluation Goal

The goal is to evaluate the evidence-linkage path rather than system performance. The path under test is: scanner finding -> runtime evidence -> validator conclusion. The prototype succeeds if the same deterministic implementation can produce PASS, WARN, and FAIL outcomes from different combinations of scanner findings and runtime behavior.

The evaluation asks whether AEP evidence can distinguish three cases. The first case has no relevant high-risk finding and no policy violation. The second case has a high-risk finding, but runtime evidence shows that the risk target was not attempted. The third case has a high-risk target attempted during execution and a policy violation observed.

The key distinction is that potential risk is not the same as triggered violation. A scanner report can say that `write_file` is risky, but the accountability conclusion depends on whether `write_file` appears in the event log and how policy handled the attempt.

This evaluation supports the research question by showing a minimal accountability mechanism. It does not prove that the scanner is complete, that the tool set is representative, or that the same behavior would hold in a deployed agent platform. Its purpose is to show that evidence linkage can be made explicit and reproducible [Repository: paper/draft/argument-flow.md] [Repository: paper/evaluation-section.md].

## 5.2 Experimental Setup

The experiment uses a deterministic non-LLM demo agent. The agent executes fixed tool sequences for the PASS, WARN, and FAIL scenarios. This removes model randomness from the evaluation and makes the generated artifacts repeatable.

The prototype includes three tools: `read_file`, `summarize_text`, and `write_file`. The first two tools are allowed by policy. `write_file` is denied by policy and is used to represent a risky tool whose attempted use can be observed and blocked.

The policy allows `read_file` and `summarize_text`. It denies `write_file`, `shell_exec`, and `send_email`. The evaluation uses two scanner risk inputs: `no-risk.json`, which has an empty findings list, and `write-file-risk.json`, which contains a high-risk finding targeting `write_file`.

For each scenario, the AEP collector generates `aep-events.jsonl` and `aep-bundle.json`. The validator reads the bundle, event log, and risk report, then writes `validation-report.json`.

| Component | Configuration in evaluation | Purpose |
| --- | --- | --- |
| Demo agent | Deterministic non-LLM agent | Removes model randomness from evaluation. |
| Allowed tools | `read_file`, `summarize_text` | Represents permitted execution behavior. |
| Denied tools | `write_file`, `shell_exec`, `send_email` | Represents policy-constrained actions. |
| No-risk report | Empty findings list | Supports PASS scenario. |
| Write-file risk report | High-risk finding targeting `write_file` | Supports WARN and FAIL scenarios. |
| AEP collector | Wraps tool calls and records evidence | Produces event log and bundle. |
| Validator | Applies six validation rules | Produces PASS/WARN/FAIL result. |

[Repository: agent/demo_agent.py] [Repository: agent/tools.py] [Repository: agent/policy.json] [Repository: scanner-output/no-risk.json] [Repository: scanner-output/write-file-risk.json]

## 5.3 Scenario Design

The PASS scenario represents acceptable execution under the current rules. The scanner report has no high-risk finding. The agent calls only `read_file` and `summarize_text`, both of which are allowed. The expected validator result is PASS.

The WARN scenario represents potential risk that is not triggered. The scanner report contains a high-risk finding for `write_file`. The agent still calls only the allowed tools and does not attempt `write_file`. The expected validator result is WARN, meaning that potential risk exists but runtime evidence does not show the target being attempted.

The FAIL scenario represents an observed attempted violation. The scanner report contains the same high-risk `write_file` finding. The agent attempts `write_file` through the collector. The collector denies and blocks actual execution, but the attempt is recorded as evidence. The expected validator result is FAIL.

These scenarios are designed to isolate the main claim: a risk-linked evidence profile can distinguish no high-risk condition, untriggered high-risk condition, and attempted denied high-risk action.

| Scenario | Scanner finding | Runtime behavior | Expected result | Accountability meaning |
| --- | --- | --- | --- | --- |
| PASS | No high-risk finding. | Only allowed tools are used. | PASS | Execution acceptable under current rules. |
| WARN | High-risk `write_file` finding exists. | `write_file` is not attempted. | WARN | Potential risk exists but is not triggered. |
| FAIL | High-risk `write_file` finding exists. | `write_file` is attempted and blocked. | FAIL | Attempted denied high-risk action is observed. |

[Repository: paper/evaluation-section.md] [Repository: demo/run_all.py]

## 5.4 Validator Rules Used in Evaluation

The same validator is used for all scenarios. It reads the AEP bundle, the event log, and the risk report. It then applies a fixed set of rules to produce a machine-readable validation report.

The validator checks schema minimality, hash-chain continuity, event-log hash binding, policy attempts, risk triggers, and blocked denied tools. These checks cover the minimum properties needed by this evaluation.

Result aggregation is simple. The validator returns FAIL if any rule fails. It returns WARN if no rule fails but at least one rule warns. It returns PASS if all rules pass.

In the WARN scenario, the warning comes primarily from a high-risk finding that is not triggered. In the FAIL scenario, failure comes from attempted denied tool use and a high-risk target attempt.

A denied tool attempt is treated as a policy violation even when the enforcement layer successfully blocks side effects. The reason is that the attempt itself is part of the execution evidence and is relevant to accountability.

| Rule | Role in evaluation |
| --- | --- |
| `V1_SCHEMA_MINIMAL` | Confirms required bundle and event fields exist. |
| `V2_HASH_CHAIN` | Confirms event hash chain continuity. |
| `V3_EVENT_LOG_HASH` | Confirms bundle hash matches event log. |
| `V4_POLICY_ATTEMPT` | Marks denied tool attempts as policy violations. |
| `V5_RISK_TRIGGER` | Distinguishes untriggered high-risk findings from attempted targets. |
| `V6_DENIED_TOOL_BLOCKED` | Confirms denied tools were blocked and did not produce output hashes. |

[Repository: paper/validator-rules.md] [Repository: validator/rules.py]

## 5.5 Results

All three scenarios matched the expected result. The PASS scenario produced acceptable execution under the current rules. The WARN scenario preserved a distinction between possible risk and observed behavior. The FAIL scenario recorded attempted `write_file` and confirmed that the attempted tool call was blocked.

| Scenario | Expected | Actual | Status |
| --- | --- | --- | --- |
| PASS | PASS | PASS | OK |
| WARN | WARN | WARN | OK |
| FAIL | FAIL | FAIL | OK |

The FAIL event has the expected blocked-tool evidence. It contains `tool = "write_file"`, `policy_decision = "deny"`, `execution_status = "blocked"`, `output_hash = null`, and `risk_refs` includes `"RISK-001"`. This confirms that the denied call was attempted, linked to the scanner finding, and blocked before actual file-writing execution.

The validation reports also show the rule-level difference among scenarios. PASS has no high-risk findings and no denied tool attempts. WARN has a high-risk finding that is not triggered. FAIL has both a denied tool attempt and a high-risk target attempt [Repository: runs/pass/validation-report.json] [Repository: runs/warn/validation-report.json] [Repository: runs/fail/validation-report.json] [Repository: runs/fail/aep-events.jsonl].

## 5.6 Interpretation

PASS demonstrates normal evidence generation. The collector records allowed tool calls, the bundle binds the event log, and the validator finds no warning or failure. This confirms the baseline path from execution to evidence to validation result.

WARN demonstrates that potential risk and actual execution should not be conflated. The scanner finding exists, but the event log does not show `write_file` being attempted. The validator therefore preserves the distinction between a risk that may matter and a risk that was triggered in a concrete run.

FAIL demonstrates that a denied high-risk action can be recorded as an attempted violation even when blocked. The collector prevents actual `write_file` execution, but the event log still records the attempt, the deny decision, the blocked status, and the risk reference.

This is why the FAIL scenario is not reduced to WARN. WARN indicates that a high-risk finding exists without a runtime trigger; FAIL indicates that the denied high-risk target was attempted, even though side effects were blocked.

The evaluation demonstrates the value of linking scanner findings to runtime evidence. Without this linkage, a reviewer would see either a scanner finding or a runtime trace, but not the relationship between them. With AEP, the reviewer can inspect event-level and bundle-level evidence together.

The evaluation does not prove real-world security coverage, scanner quality, or production compliance. It demonstrates a minimal evidence-linkage mechanism under controlled conditions [Repository: paper/draft/argument-flow.md] [Repository: paper/aep-profile-v0.1.md].

## 5.7 Threats to Validity

Internal validity is limited by the synthetic nature of the scanner reports and the small fixed tool set. The experiment is designed to test evidence linkage, not scanner discovery quality. The direct target-to-tool matching model is sufficient for the current scenarios but does not represent complex risk mappings.

External validity is limited by the deterministic non-LLM agent and the absence of real deployment noise. The prototype does not evaluate autonomous LLM behavior, multi-agent workflows, production tool ecosystems, or live infrastructure. Results should not be generalized to operational deployments without further study.

Construct validity is limited by the simple allow/deny policy and minimal validator. The evaluation does not include a formal policy language, SARIF parser, MCP runtime, real FDO registry, IDS connector, production signing, or comparison against alternative evidence models. It also does not measure performance or scalability.

Reproducibility limits are narrower. The evaluation is intentionally reproducible in the local repository, but generated hashes depend on the generated event log contents. The artifact-level behavior, expected results, and fail-event properties are checked by the acceptance script. These limitations are intentional for a minimal research prototype [Repository: paper/research-scope.md].

## 5.8 Reproducibility

The evaluation is reproducible using existing commands. `python3 demo/run_all.py` regenerates the three scenarios and validates them. It produces event logs, bundles, and validation reports under `runs/`.

`python3 scripts/acceptance_check.py` checks generated files, expected validation results, and key FAIL behavior. In particular, it verifies that the FAIL event contains a blocked `write_file` attempt and that `blocked-write.txt` is absent.

The Makefile provides wrappers for the same workflow. `make demo` runs the demo, and `make acceptance` runs the acceptance checks. Generated run artifacts are reproducible and normally ignored by git.

| Command | Purpose |
| --- | --- |
| `python3 demo/run_all.py` | Regenerates PASS/WARN/FAIL runs and validator reports. |
| `python3 scripts/acceptance_check.py` | Checks generated files, expected results, and blocked fail behavior. |
| `make demo` | Runs the demo through Makefile. |
| `make acceptance` | Runs acceptance checks through Makefile. |

[Repository: demo/run_all.py] [Repository: scripts/acceptance_check.py] [Repository: Makefile]
