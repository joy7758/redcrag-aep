#!/usr/bin/env python3
"""Convert the fake HackMyAgent sample into the normalized risk format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def normalize(native_report: dict) -> dict:
    scan = native_report["tool_risk_scan"]
    findings = []
    for issue in scan.get("issues", []):
        findings.append(
            {
                "risk_id": issue["id"],
                "source": scan["scanner_name"],
                "severity": issue["level"],
                "category": issue["kind"],
                "target": issue["tool_name"],
                "message": issue["detail"],
            }
        )
    return {
        "scanner": "demo-scanner",
        "scan_id": scan["scan_id"],
        "generated_at": scan["generated_at"],
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_path", default="hackmyagent-sample.json")
    parser.add_argument("--out", dest="output_path")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    input_path = Path(args.input_path)
    if not input_path.is_absolute():
        input_path = base / input_path

    with input_path.open("r", encoding="utf-8") as handle:
        normalized = normalize(json.load(handle))

    text = json.dumps(normalized, indent=2, ensure_ascii=False) + "\n"
    if args.output_path:
        output_path = Path(args.output_path)
        if not output_path.is_absolute():
            output_path = base / output_path
        output_path.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
