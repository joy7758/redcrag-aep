#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agent.demo_agent import run_agent
from validator.rules import validate


SCENARIOS = [
    ("pass", "PASS", "scanner-output/no-risk.json"),
    ("warn", "WARN", "scanner-output/write-file-risk.json"),
    ("fail", "FAIL", "scanner-output/write-file-risk.json"),
]


def clean_run_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in path.iterdir():
        if child.name == ".gitkeep":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def write_validation_report(report: dict, out_path: Path) -> None:
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    rows = []
    for scenario, expected, risk_relative in SCENARIOS:
        out_dir = PROJECT_ROOT / "runs" / scenario
        risk_path = PROJECT_ROOT / risk_relative
        clean_run_dir(out_dir)

        run_agent(scenario, out_dir, risk_path)
        report = validate(out_dir / "aep-bundle.json", out_dir / "aep-events.jsonl", risk_path)
        write_validation_report(report, out_dir / "validation-report.json")

        actual = report["result"]
        status = "OK" if actual == expected else "MISMATCH"
        rows.append((expected, expected, actual, status))

    print("Scenario | Expected | Actual | Status")
    for scenario, expected, actual, status in rows:
        print(f"{scenario:<8} | {expected:<8} | {actual:<6} | {status}")

    return 0 if all(row[3] == "OK" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
