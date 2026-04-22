#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agent import tools
from collector.aep_collector import AEPCollector


RUN_IDS = {
    "pass": "run-pass-001",
    "warn": "run-warn-001",
    "fail": "run-fail-001",
}


def project_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def run_agent(scenario: str, out_dir: Path, risk_path: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    collector = AEPCollector(
        policy_path=PROJECT_ROOT / "agent" / "policy.json",
        risk_report_path=risk_path,
        out_dir=out_dir,
        scenario=scenario,
        run_id=RUN_IDS[scenario],
    )

    input_path = PROJECT_ROOT / "demo" / "input.txt"
    text = collector.call_tool("read_file", tools.read_file, str(input_path))
    summary = collector.call_tool("summarize_text", tools.summarize_text, text)

    if scenario == "fail":
        blocked_path = out_dir / "blocked-write.txt"
        collector.call_tool("write_file", tools.write_file, str(blocked_path), summary)

    collector.write_events()
    return collector.write_bundle()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, choices=["pass", "warn", "fail"])
    parser.add_argument("--out", required=True)
    parser.add_argument("--risk", required=True)
    args = parser.parse_args()

    run_agent(args.scenario, project_path(args.out), project_path(args.risk))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
