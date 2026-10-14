# Reproducibility Instructions

## Environment

- Python 3.11+ compatible.
- Python standard library only.
- No third-party dependencies are required.
- Network access is not required.

## Primary Commands

| Command | Purpose | Expected outcome |
| --- | --- | --- |
| `python3 demo/run_all.py` | Runs PASS/WARN/FAIL scenarios and validation. | Prints all scenarios as OK. |
| `python3 scripts/acceptance_check.py` | Verifies generated artifacts and key fail evidence. | Prints `Acceptance check: PASS`. |
| `make demo` | Makefile wrapper for the demo. | Prints all scenarios as OK. |
| `make acceptance` | Makefile wrapper for acceptance checks. | Prints `Acceptance check: PASS`. |
| `make clean` | Removes generated scenario artifacts. | Leaves the repository ready for regeneration. |

## Step-by-step Reproduction

1. From the repository root, run `python3 demo/run_all.py`.
2. Confirm PASS / WARN / FAIL table.
3. Run `python3 scripts/acceptance_check.py`.
4. Confirm acceptance output.
5. Optionally run `make demo` and `make acceptance`.

## Expected Demo Output

| Scenario | Expected | Actual | Status |
| -------- | -------- | ------ | ------ |
| PASS     | PASS     | PASS   | OK     |
| WARN     | WARN     | WARN   | OK     |
| FAIL     | FAIL     | FAIL   | OK     |

## Expected Acceptance Output

```text
Acceptance check: PASS
- generated files: OK
- validation results: OK
- fail scenario blocked write_file: OK
- blocked-write.txt absent: OK
```

## FAIL Scenario Evidence Check

The FAIL scenario must contain an event with:

- `tool = "write_file"`
- `policy_decision = "deny"`
- `execution_status = "blocked"`
- `output_hash = null`
- `risk_refs` includes `"RISK-001"`

`runs/fail/blocked-write.txt` must not exist.

## Reproducibility Boundary

The demo is deterministic and synthetic. It is not a real-world benchmark, performance test, security evaluation, or production validation.
