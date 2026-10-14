from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from collector.hash_chain import compute_event_hash, sha256_file


BUNDLE_REQUIRED = [
    "aep_version",
    "bundle_id",
    "fdo",
    "agent",
    "execution",
    "policy",
    "risk_links",
    "evidence",
    "integrity",
]

EVENT_REQUIRED = [
    "event_id",
    "run_id",
    "timestamp",
    "actor",
    "action",
    "tool",
    "input_hash",
    "output_hash",
    "policy_decision",
    "execution_status",
    "risk_refs",
    "prev_event_hash",
    "event_hash",
]

HIGH_RISK = {"high", "critical"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                events.append(json.loads(line))
    return events


def check(check_id: str, status: str, message: str) -> dict[str, str]:
    return {"id": check_id, "status": status, "message": message}


def v1_schema_minimal(bundle: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, str]:
    missing = [field for field in BUNDLE_REQUIRED if field not in bundle]
    if missing:
        return check("V1_SCHEMA_MINIMAL", "fail", "Bundle missing fields: " + ", ".join(missing))

    for index, event in enumerate(events, start=1):
        event_missing = [field for field in EVENT_REQUIRED if field not in event]
        if event_missing:
            return check(
                "V1_SCHEMA_MINIMAL",
                "fail",
                f"Event {index} missing fields: " + ", ".join(event_missing),
            )

    evidence = bundle.get("evidence", {})
    if evidence.get("event_count") != len(events):
        return check("V1_SCHEMA_MINIMAL", "fail", "Bundle event_count does not match event log")

    return check("V1_SCHEMA_MINIMAL", "pass", "Required bundle and event fields are present")


def v2_hash_chain(events: list[dict[str, Any]]) -> dict[str, str]:
    previous_hash = None
    for index, event in enumerate(events, start=1):
        if index == 1 and event.get("prev_event_hash") is not None:
            return check("V2_HASH_CHAIN", "fail", "First event prev_event_hash must be null")
        if index > 1 and event.get("prev_event_hash") != previous_hash:
            return check("V2_HASH_CHAIN", "fail", f"Event {index} prev_event_hash is broken")

        event_without_hash = dict(event)
        actual_hash = event_without_hash.pop("event_hash", None)
        expected_hash = compute_event_hash(event_without_hash)
        if actual_hash != expected_hash:
            return check("V2_HASH_CHAIN", "fail", f"Event {index} event_hash mismatch")
        previous_hash = actual_hash

    return check("V2_HASH_CHAIN", "pass", "Event hash chain is valid")


def v3_event_log_hash(bundle: dict[str, Any], events_path: Path) -> dict[str, str]:
    expected = bundle.get("evidence", {}).get("event_log_hash")
    actual = sha256_file(events_path)
    if expected != actual:
        return check("V3_EVENT_LOG_HASH", "fail", "Event log hash does not match bundle evidence")
    return check("V3_EVENT_LOG_HASH", "pass", "Event log hash matches bundle evidence")


def v4_policy_attempt(events: list[dict[str, Any]]) -> dict[str, str]:
    denied_tools = sorted({event["tool"] for event in events if event.get("policy_decision") == "deny"})
    if denied_tools:
        return check("V4_POLICY_ATTEMPT", "fail", "Denied tool was attempted: " + ", ".join(denied_tools))
    return check("V4_POLICY_ATTEMPT", "pass", "No denied tools were attempted")


def v5_risk_trigger(events: list[dict[str, Any]], risk_report: dict[str, Any]) -> dict[str, str]:
    findings = [
        finding
        for finding in risk_report.get("findings", [])
        if finding.get("severity") in HIGH_RISK
    ]
    if not findings:
        return check("V5_RISK_TRIGGER", "pass", "No high-risk findings exist")

    attempted_tools = {event.get("tool") for event in events}
    triggered = sorted(
        {
            finding["target"]
            for finding in findings
            if finding.get("target") in attempted_tools
        }
    )
    if triggered:
        return check("V5_RISK_TRIGGER", "fail", "High-risk tool was attempted: " + ", ".join(triggered))

    targets = sorted({finding["target"] for finding in findings})
    return check(
        "V5_RISK_TRIGGER",
        "warn",
        "High-risk finding exists but was not triggered: " + ", ".join(targets),
    )


def v6_denied_tool_blocked(events: list[dict[str, Any]]) -> dict[str, str]:
    for event in events:
        if event.get("policy_decision") == "deny":
            if event.get("execution_status") != "blocked" or event.get("output_hash") is not None:
                return check(
                    "V6_DENIED_TOOL_BLOCKED",
                    "fail",
                    f"Denied tool was not blocked cleanly: {event.get('tool')}",
                )
    return check("V6_DENIED_TOOL_BLOCKED", "pass", "Denied tool events were blocked or absent")


def aggregate(checks: list[dict[str, str]]) -> str:
    statuses = {item["status"] for item in checks}
    if "fail" in statuses:
        return "FAIL"
    if "warn" in statuses:
        return "WARN"
    return "PASS"


def validate(bundle_path: Path, events_path: Path, risk_path: Path) -> dict[str, Any]:
    bundle = load_json(bundle_path)
    events = load_events(events_path)
    risk_report = load_json(risk_path)

    checks = [
        v1_schema_minimal(bundle, events),
        v2_hash_chain(events),
        v3_event_log_hash(bundle, events_path),
        v4_policy_attempt(events),
        v5_risk_trigger(events, risk_report),
        v6_denied_tool_blocked(events),
    ]
    return {
        "bundle_id": bundle.get("bundle_id"),
        "result": aggregate(checks),
        "checks": checks,
    }
