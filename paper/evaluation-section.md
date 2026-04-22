# Evaluation

## Evaluation Goal

The evaluation checks whether the prototype can distinguish three accountability states: safe execution, potential-but-untriggered risk, and triggered violation.

## Experimental Setup

The prototype uses a deterministic demo agent and three tools:
- `read_file`
- `summarize_text`
- `write_file`

The policy allows `read_file` and `summarize_text`. The policy denies `write_file`. The scanner report either contains no high-risk findings or contains a high-risk finding for `write_file`.

## Scenarios

| Scenario | Scanner finding | Runtime behavior | Expected result | Accountability meaning |
| --- | --- | --- | --- | --- |
| PASS | no high-risk finding | only allowed tools used | PASS | execution acceptable |
| WARN | high-risk `write_file` finding exists | `write_file` not attempted | WARN | potential risk present but not triggered |
| FAIL | high-risk `write_file` finding exists | `write_file` attempted and blocked | FAIL | attempted denied high-risk action observed |

## Results

| Scenario | Expected | Actual | Status |
| --- | --- | --- | --- |
| PASS | PASS | PASS | OK |
| WARN | WARN | WARN | OK |
| FAIL | FAIL | FAIL | OK |

## Interpretation

PASS demonstrates normal evidence generation. WARN demonstrates the distinction between potential risk and actual execution. FAIL demonstrates that attempted denied action can be captured and judged as violation even if blocked.

## Threats to Validity

- synthetic scanner report
- deterministic non-LLM agent
- small tool set
- no real-world deployment noise
- no formal policy language
- demo signing only

## Reproducibility

```bash
make demo
make acceptance
```

Direct commands:

```bash
python3 demo/run_all.py
python3 scripts/acceptance_check.py
```
