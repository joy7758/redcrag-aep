"""Command line interface for the RedCrag AEP demo package."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from .canonical import sha256_hex
from .otel_to_aep import convert_otel_trace_to_aep
from .signer import sign_bundle, verify_bundle
from .validator import validate_bundle

DEFAULT_DEMO_KEY = "redcrag-demo-key"
OTEL_FIXTURE_EXPECTATIONS = {
    "valid_contract_review_trace.json": True,
    "invalid_missing_receipt_trace.json": False,
    "invalid_missing_human_review_trace.json": False,
    "invalid_full_contract_leak_trace.json": False,
    "valid_customer_service_trace.json": True,
}


def _demo_key() -> tuple[str, bool]:
    value = os.environ.get("REDCRAG_DEMO_SIGNING_KEY")
    return (value, False) if value else (DEFAULT_DEMO_KEY, True)


def _read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _write_json(path: str | Path, data: dict[str, Any]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def _load_rules() -> dict[str, Any] | None:
    rules_path = Path("rules/contract_review_rules.json")
    if not rules_path.exists():
        return None
    return _read_json(rules_path)


def _build_demo_bundle() -> dict[str, Any]:
    output_summary = "识别到责任限制条款缺少间接损失上限，建议进入人工复核。"
    clause_quote_hash = sha256_hex("第12.3条：责任限制与间接损失排除。")
    bundle = {
        "schema_version": "aep-0.1",
        "run_id": "redcrag-contract-demo-run-001",
        "workflow": "contract_review_demo",
        "actor": "redcrag_contract_review_agent",
        "task": "Review a contract clause reference without storing the full contract text.",
        "started_at": "2026-05-20T09:00:00Z",
        "completed_at": "2026-05-20T09:04:00Z",
        "tool_calls": [
            {
                "tool_call_id": "tool-001",
                "tool_name": "clause_retriever",
                "started_at": "2026-05-20T09:00:20Z",
                "completed_at": "2026-05-20T09:00:50Z",
                "purpose": "Retrieve clause reference and hash only.",
                "risk_level": "low",
            },
            {
                "tool_call_id": "tool-002",
                "tool_name": "risk_opinion_generator",
                "started_at": "2026-05-20T09:01:00Z",
                "completed_at": "2026-05-20T09:02:20Z",
                "purpose": "Generate a risk opinion from the referenced clause.",
                "risk_level": "medium",
            },
            {
                "tool_call_id": "tool-003",
                "tool_name": "high_risk_clause_escalation",
                "started_at": "2026-05-20T09:02:30Z",
                "completed_at": "2026-05-20T09:03:10Z",
                "purpose": "Escalate a high-risk clause conclusion for human review.",
                "risk_level": "high",
                "requires_receipt": True,
                "receipt_id": "receipt-hr-001",
            },
        ],
        "input_refs": [
            {
                "input_id": "input-contract-001",
                "kind": "contract_clause_reference",
                "source_location": "contract://demo-contract#clause-12.3",
                "summary": "Liability limitation clause reference only; no full contract text stored.",
                "sha256": clause_quote_hash,
            }
        ],
        "output_refs": [
            {
                "output_id": "output-risk-001",
                "kind": "contract_review_conclusion",
                "summary": output_summary,
                "source_clause_ref": "clause-12.3",
                "risk_level": "high",
            }
        ],
        "receipt_refs": [
            {
                "receipt_id": "receipt-hr-001",
                "tool_call_id": "tool-003",
                "kind": "human_review_receipt",
                "summary": "Legal reviewer approved escalation record for demo clause.",
                "issued_at": "2026-05-20T09:03:40Z",
            }
        ],
        "human_review": {
            "approved": True,
            "reviewer": "demo_legal_reviewer",
            "reviewed_at": "2026-05-20T09:03:45Z",
            "reviewed_tool_call_ids": ["tool-003"],
            "decision": "approve_with_follow_up",
        },
        "policy_results": [
            {
                "policy_id": "contract_high_risk_requires_review",
                "passed": True,
                "summary": "High-risk conclusion has human review approval.",
            }
        ],
        "content_hashes": [
            {
                "hash_id": "hash-output-risk-summary",
                "target_path": "/output_refs/0/summary",
                "sha256": sha256_hex(output_summary),
            }
        ],
        "signature": {},
        "metadata": {
            "demo": True,
            "privacy_boundary": "No full contract text is stored in this AEP bundle.",
        },
    }
    return bundle


def _command_validate(args: argparse.Namespace) -> None:
    key, default_key_used = _demo_key()
    bundle = _read_json(args.bundle)
    result = validate_bundle(bundle, rules=_load_rules(), signing_key=key)
    result["demo_key_warning"] = (
        "REDCRAG_DEMO_SIGNING_KEY is not set; using redcrag-demo-key for demo use only."
        if default_key_used
        else "REDCRAG_DEMO_SIGNING_KEY was used; still demo-grade HMAC, not production signing."
    )
    _print_json(result)


def _command_sign(args: argparse.Namespace) -> None:
    key, default_key_used = _demo_key()
    bundle = _read_json(args.bundle)
    signed = sign_bundle(bundle, key)
    result = {
        "signed_bundle": signed,
        "demo_key_warning": (
            "REDCRAG_DEMO_SIGNING_KEY is not set; using redcrag-demo-key for demo use only."
            if default_key_used
            else "REDCRAG_DEMO_SIGNING_KEY was used; still demo-grade HMAC, not production signing."
        ),
    }
    if args.out:
        _write_json(args.out, signed)
        result["out"] = args.out
        result.pop("signed_bundle")
    _print_json(result)


def _command_verify(args: argparse.Namespace) -> None:
    key, default_key_used = _demo_key()
    bundle = _read_json(args.bundle)
    passed, message = verify_bundle(bundle, key)
    _print_json(
        {
            "passed": passed,
            "message": message,
            "demo_key_warning": (
                "REDCRAG_DEMO_SIGNING_KEY is not set; using redcrag-demo-key for demo use only."
                if default_key_used
                else "REDCRAG_DEMO_SIGNING_KEY was used; still demo-grade HMAC, not production signing."
            ),
        }
    )


def _command_demo(_: argparse.Namespace) -> None:
    key, default_key_used = _demo_key()
    signed = sign_bundle(_build_demo_bundle(), key)
    output_path = Path("outputs/redcrag_aep_contract_review_demo_bundle.json")
    _write_json(output_path, signed)
    validation = validate_bundle(signed, rules=_load_rules(), signing_key=key)
    _print_json(
        {
            "bundle_path": str(output_path),
            "validation_passed": validation["passed"],
            "checks": validation["checks"],
            "what_this_proves": [
                "The evidence record has the minimal AEP structure.",
                "The demo signature matches the current bundle content.",
                "Receipt-required and high-risk tool calls can be checked.",
                "Contract conclusions can point back to clause references without storing full text.",
            ],
            "what_this_does_not_prove": [
                "It does not prove the model conclusion is legally correct.",
                "It does not prove external-world facts are true.",
                "It is not a production compliance or legal-signature system.",
            ],
            "demo_key_warning": (
                "REDCRAG_DEMO_SIGNING_KEY is not set; using redcrag-demo-key for demo use only."
                if default_key_used
                else "REDCRAG_DEMO_SIGNING_KEY was used; still demo-grade HMAC, not production signing."
            ),
        }
    )


def _failed_checks(validation: dict[str, Any]) -> list[dict[str, Any]]:
    return [check for check in validation.get("checks", []) if not check.get("passed")]


def _command_convert_otel(args: argparse.Namespace) -> None:
    key, default_key_used = _demo_key()
    trace = _read_json(args.trace)
    bundle = convert_otel_trace_to_aep(trace)
    if args.sign:
        bundle = sign_bundle(bundle, key)
    _write_json(args.out, bundle)
    validation = validate_bundle(bundle, rules=_load_rules(), signing_key=key if args.sign else None)
    _print_json(
        {
            "input_trace": args.trace,
            "output_bundle": args.out,
            "signed": bool(args.sign),
            "validation_passed": validation["passed"],
            "failed_checks": _failed_checks(validation),
            "demo_key_warning": (
                "REDCRAG_DEMO_SIGNING_KEY is not set; using redcrag-demo-key for demo use only."
                if default_key_used
                else "REDCRAG_DEMO_SIGNING_KEY was used; still demo-grade HMAC, not production signing."
            ),
        }
    )


def _command_selfcheck_otel(_: argparse.Namespace) -> None:
    key, default_key_used = _demo_key()
    fixture_dir = Path("fixtures/otel_traces")
    cases: list[dict[str, Any]] = []
    passed_cases: list[str] = []
    failed_cases: list[str] = []
    unexpected_results: list[dict[str, Any]] = []

    for filename, expected_passed in OTEL_FIXTURE_EXPECTATIONS.items():
        trace_path = fixture_dir / filename
        trace = _read_json(trace_path)
        bundle = sign_bundle(convert_otel_trace_to_aep(trace), key)
        validation = validate_bundle(bundle, rules=_load_rules(), signing_key=key)
        actual_passed = bool(validation["passed"])
        failed = _failed_checks(validation)
        case_result = {
            "case": filename,
            "expected_passed": expected_passed,
            "actual_passed": actual_passed,
            "failed_checks": [check["id"] for check in failed],
        }
        cases.append(case_result)
        if actual_passed:
            passed_cases.append(filename)
        else:
            failed_cases.append(filename)
        if actual_passed != expected_passed:
            unexpected_results.append(case_result)

    _print_json(
        {
            "passed_cases": passed_cases,
            "failed_cases": failed_cases,
            "unexpected_results": unexpected_results,
            "overall_passed": not unexpected_results,
            "cases": cases,
            "demo_key_warning": (
                "REDCRAG_DEMO_SIGNING_KEY is not set; using redcrag-demo-key for demo use only."
                if default_key_used
                else "REDCRAG_DEMO_SIGNING_KEY was used; still demo-grade HMAC, not production signing."
            ),
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RedCrag AEP minimal demo CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate an AEP bundle")
    validate_parser.add_argument("bundle")
    validate_parser.set_defaults(func=_command_validate)

    sign_parser = subparsers.add_parser("sign", help="Sign an AEP bundle with demo HMAC")
    sign_parser.add_argument("bundle")
    sign_parser.add_argument("--out")
    sign_parser.set_defaults(func=_command_sign)

    verify_parser = subparsers.add_parser("verify", help="Verify an AEP demo signature")
    verify_parser.add_argument("bundle")
    verify_parser.set_defaults(func=_command_verify)

    demo_parser = subparsers.add_parser("demo", help="Run the contract review evidence demo")
    demo_parser.set_defaults(func=_command_demo)

    convert_otel_parser = subparsers.add_parser("convert-otel", help="Convert an OpenTelemetry-style trace to AEP")
    convert_otel_parser.add_argument("trace")
    convert_otel_parser.add_argument("--out", required=True)
    convert_otel_parser.add_argument("--sign", action="store_true")
    convert_otel_parser.set_defaults(func=_command_convert_otel)

    selfcheck_otel_parser = subparsers.add_parser("selfcheck-otel", help="Run OpenTelemetry-style trace self-check fixtures")
    selfcheck_otel_parser.set_defaults(func=_command_selfcheck_otel)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
