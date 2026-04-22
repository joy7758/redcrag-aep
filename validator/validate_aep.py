#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from validator.rules import validate


def project_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def print_summary(report: dict) -> None:
    print(f"AEP validation result: {report['result']}")
    for item in report["checks"]:
        print(f"- {item['id']}: {item['status']} - {item['message']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--events", required=True)
    parser.add_argument("--risk", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    report = validate(project_path(args.bundle), project_path(args.events), project_path(args.risk))
    out_path = project_path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print_summary(report)
    return 0 if report["result"] in {"PASS", "WARN", "FAIL"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
