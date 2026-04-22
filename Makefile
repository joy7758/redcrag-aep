PYTHON ?= python3
PYTHON_ALT ?= python

.PHONY: demo demo-python clean validate-pass validate-warn validate-fail acceptance

demo:
	$(PYTHON) demo/run_all.py

demo-python:
	$(PYTHON_ALT) demo/run_all.py

clean:
	rm -rf runs/pass runs/warn runs/fail

validate-pass:
	$(PYTHON) validator/validate_aep.py --bundle runs/pass/aep-bundle.json --events runs/pass/aep-events.jsonl --risk scanner-output/no-risk.json --out runs/pass/validation-report.json

validate-warn:
	$(PYTHON) validator/validate_aep.py --bundle runs/warn/aep-bundle.json --events runs/warn/aep-events.jsonl --risk scanner-output/write-file-risk.json --out runs/warn/validation-report.json

validate-fail:
	$(PYTHON) validator/validate_aep.py --bundle runs/fail/aep-bundle.json --events runs/fail/aep-events.jsonl --risk scanner-output/write-file-risk.json --out runs/fail/validation-report.json

acceptance:
	$(PYTHON) scripts/acceptance_check.py
