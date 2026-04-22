#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "runs/pass/aep-events.jsonl",
    "runs/pass/aep-bundle.json",
    "runs/pass/validation-report.json",
    "runs/warn/aep-events.jsonl",
    "runs/warn/aep-bundle.json",
    "runs/warn/validation-report.json",
    "runs/fail/aep-events.jsonl",
    "runs/fail/aep-bundle.json",
    "runs/fail/validation-report.json",
]

EXPECTED_RESULTS = {
    "runs/pass/validation-report.json": "PASS",
    "runs/warn/validation-report.json": "WARN",
    "runs/fail/validation-report.json": "FAIL",
}


def run_demo() -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "demo" / "run_all.py")],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    return result.returncode == 0, output


def generated_files_ok() -> tuple[bool, str]:
    missing = [path for path in REQUIRED_FILES if not (PROJECT_ROOT / path).is_file()]
    if missing:
        return False, "missing files: " + ", ".join(missing)
    return True, "OK"


def validation_results_ok() -> tuple[bool, str]:
    failures = []
    for path, expected in EXPECTED_RESULTS.items():
        report = json.loads((PROJECT_ROOT / path).read_text(encoding="utf-8"))
        actual = report.get("result")
        if actual != expected:
            failures.append(f"{path} expected {expected} got {actual}")
    if failures:
        return False, "; ".join(failures)
    return True, "OK"


def fail_scenario_blocked_write_file_ok() -> tuple[bool, str]:
    events_path = PROJECT_ROOT / "runs" / "fail" / "aep-events.jsonl"
    events = [
        json.loads(line)
        for line in events_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    for event in events:
        if (
            event.get("tool") == "write_file"
            and event.get("policy_decision") == "deny"
            and event.get("execution_status") == "blocked"
            and event.get("output_hash") is None
            and "RISK-001" in event.get("risk_refs", [])
        ):
            return True, "OK"
    return False, "required blocked write_file event not found"


def blocked_write_absent_ok() -> tuple[bool, str]:
    blocked_path = PROJECT_ROOT / "runs" / "fail" / "blocked-write.txt"
    if blocked_path.exists():
        return False, "runs/fail/blocked-write.txt exists"
    return True, "OK"


def main() -> int:
    demo_ok, demo_output = run_demo()
    checks = []
    if not demo_ok:
        print("Acceptance check: FAIL")
        print("- demo run: FAIL")
        print(demo_output, end="")
        return 1

    checks.append(("generated files", *generated_files_ok()))
    checks.append(("validation results", *validation_results_ok()))
    checks.append(("fail scenario blocked write_file", *fail_scenario_blocked_write_file_ok()))
    checks.append(("blocked-write.txt absent", *blocked_write_absent_ok()))

    all_ok = all(ok for _, ok, _ in checks)
    print(f"Acceptance check: {'PASS' if all_ok else 'FAIL'}")
    for label, ok, message in checks:
        print(f"- {label}: {'OK' if ok else 'FAIL'}" + ("" if ok else f" - {message}"))

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
