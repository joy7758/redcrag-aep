"""Validator for the RedCrag AEP minimal profile."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .canonical import hash_json, sha256_hex
from .signer import verify_bundle

DEFAULT_REQUIRED_FIELDS = [
    "schema_version",
    "run_id",
    "workflow",
    "actor",
    "task",
    "started_at",
    "completed_at",
    "tool_calls",
    "input_refs",
    "output_refs",
    "receipt_refs",
    "human_review",
    "policy_results",
    "content_hashes",
    "signature",
    "metadata",
]

CORE_REQUIRED_FIELDS = [
    "run_id",
    "workflow",
    "actor",
    "task",
    "tool_calls",
    "content_hashes",
    "signature",
]

FORBIDDEN_FIELD_NAMES = {
    "full_contract_text",
    "raw_medical_record",
    "customer_secret",
    "private_key",
    "api_key",
}


def _check(checks: list[dict[str, Any]], check_id: str, name: str, passed: bool, message: str, severity: str) -> None:
    checks.append(
        {
            "id": check_id,
            "name": name,
            "passed": bool(passed),
            "message": message,
            "severity": severity,
        }
    )


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _receipt_ids(bundle: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for receipt in _as_list(bundle.get("receipt_refs")):
        if isinstance(receipt, dict):
            receipt_id = receipt.get("receipt_id") or receipt.get("id")
            if receipt_id:
                ids.add(str(receipt_id))
    return ids


def _tool_call_id(tool_call: dict[str, Any], index: int) -> str:
    return str(tool_call.get("tool_call_id") or tool_call.get("id") or f"tool_call_{index}")


def _approved_tool_ids_from_review(review: dict[str, Any]) -> set[str] | None:
    id_fields = ("approved_tool_call_ids", "reviewed_tool_call_ids", "tool_call_ids")
    ids: set[str] = set()
    for field in id_fields:
        value = review.get(field)
        if isinstance(value, list):
            ids.update(str(item) for item in value)
    if review.get("tool_call_id"):
        ids.add(str(review["tool_call_id"]))
    return ids or None


def _human_review_approved_for(bundle: dict[str, Any], tool_call: dict[str, Any], index: int) -> bool:
    target_id = _tool_call_id(tool_call, index)
    review = bundle.get("human_review")
    if isinstance(review, dict):
        if review.get("approved") is True:
            approved_ids = _approved_tool_ids_from_review(review)
            return approved_ids is None or target_id in approved_ids
        reviews = review.get("reviews")
        if isinstance(reviews, list):
            return any(
                isinstance(item, dict)
                and item.get("approved") is True
                and (_approved_tool_ids_from_review(item) is None or target_id in (_approved_tool_ids_from_review(item) or set()))
                for item in reviews
            )
    if isinstance(review, list):
        return any(
            isinstance(item, dict)
            and item.get("approved") is True
            and (_approved_tool_ids_from_review(item) is None or target_id in (_approved_tool_ids_from_review(item) or set()))
            for item in review
        )
    return False


def _iter_forbidden_fields(obj: Any, path: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}"
            if str(key).lower() in FORBIDDEN_FIELD_NAMES:
                yield current_path, str(key)
            yield from _iter_forbidden_fields(value, current_path)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            yield from _iter_forbidden_fields(item, f"{path}[{index}]")


def _json_pointer_get(obj: Any, pointer: str) -> tuple[bool, Any]:
    if pointer in ("", "/"):
        return True, obj
    if pointer.startswith("/"):
        current = obj
        for raw_part in pointer.lstrip("/").split("/"):
            part = raw_part.replace("~1", "/").replace("~0", "~")
            if isinstance(current, list):
                try:
                    current = current[int(part)]
                except (ValueError, IndexError):
                    return False, None
            elif isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False, None
        return True, current
    return _dotted_path_get(obj, pointer)


def _dotted_path_get(obj: Any, path: str) -> tuple[bool, Any]:
    current = obj
    for part in path.split("."):
        if isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return False, None
        elif isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


def _hash_value(value: Any) -> str:
    if isinstance(value, bytes):
        return sha256_hex(value)
    if isinstance(value, str):
        return sha256_hex(value)
    return hash_json(value)


def _is_contract_review(bundle: dict[str, Any]) -> bool:
    text = f"{bundle.get('workflow', '')} {bundle.get('task', '')}".lower()
    return "contract" in text or "合同" in text


def _load_rule_list(rules: dict[str, Any] | None, key: str, default: list[str]) -> list[str]:
    if isinstance(rules, dict) and isinstance(rules.get(key), list):
        return [str(item) for item in rules[key]]
    return default


def validate_bundle(
    bundle: dict[str, Any],
    rules: dict[str, Any] | None = None,
    signing_key: str | None = None,
) -> dict[str, Any]:
    """Validate a RedCrag AEP bundle and return structured check results."""
    checks: list[dict[str, Any]] = []
    required_fields = _load_rule_list(rules, "required_fields", DEFAULT_REQUIRED_FIELDS)
    core_required = _load_rule_list(rules, "core_required_fields", CORE_REQUIRED_FIELDS)

    missing_required = [field for field in required_fields if field not in bundle]
    _check(
        checks,
        "schema.required_fields",
        "AEP required fields",
        not missing_required,
        "all minimal AEP fields are present" if not missing_required else f"missing fields: {', '.join(missing_required)}",
        "error",
    )

    missing_core = [field for field in core_required if field not in bundle]
    _check(
        checks,
        "policy.core_required_fields",
        "Core evidence fields",
        not missing_core,
        "core evidence fields are present" if not missing_core else f"missing core fields: {', '.join(missing_core)}",
        "error",
    )

    list_fields = ["tool_calls", "input_refs", "output_refs", "receipt_refs", "policy_results", "content_hashes"]
    bad_list_fields = [field for field in list_fields if field in bundle and not isinstance(bundle[field], list)]
    _check(
        checks,
        "schema.list_fields",
        "List-shaped fields",
        not bad_list_fields,
        "list fields have list values" if not bad_list_fields else f"not lists: {', '.join(bad_list_fields)}",
        "error",
    )

    missing_tool_fields: list[str] = []
    for index, tool_call in enumerate(_as_list(bundle.get("tool_calls"))):
        if not isinstance(tool_call, dict):
            missing_tool_fields.append(f"tool_calls[{index}] is not an object")
            continue
        missing = [field for field in ("tool_name", "started_at", "completed_at", "purpose") if field not in tool_call]
        if missing:
            missing_tool_fields.append(f"{_tool_call_id(tool_call, index)} missing {', '.join(missing)}")
    _check(
        checks,
        "policy.tool_call_required_fields",
        "Tool call audit fields",
        not missing_tool_fields,
        "all tool calls include tool_name, started_at, completed_at, and purpose"
        if not missing_tool_fields
        else "; ".join(missing_tool_fields),
        "error",
    )

    high_risk_failures: list[str] = []
    for index, tool_call in enumerate(_as_list(bundle.get("tool_calls"))):
        if isinstance(tool_call, dict) and str(tool_call.get("risk_level", "")).lower() == "high":
            if not _human_review_approved_for(bundle, tool_call, index):
                high_risk_failures.append(_tool_call_id(tool_call, index))
    _check(
        checks,
        "policy.high_risk_human_review",
        "High-risk human review",
        not high_risk_failures,
        "high-risk tool calls have approved human review"
        if not high_risk_failures
        else f"missing approved human review for: {', '.join(high_risk_failures)}",
        "error",
    )

    available_receipts = _receipt_ids(bundle)
    receipt_failures: list[str] = []
    for index, tool_call in enumerate(_as_list(bundle.get("tool_calls"))):
        if not isinstance(tool_call, dict) or tool_call.get("requires_receipt") is not True:
            continue
        receipt_id = tool_call.get("receipt_id")
        if not receipt_id:
            receipt_failures.append(f"{_tool_call_id(tool_call, index)} has no receipt_id")
        elif str(receipt_id) not in available_receipts:
            receipt_failures.append(f"{_tool_call_id(tool_call, index)} references missing receipt {receipt_id}")
    _check(
        checks,
        "policy.required_receipts",
        "Required external-action receipts",
        not receipt_failures,
        "all receipt-required tool calls have matching receipt_refs"
        if not receipt_failures
        else "; ".join(receipt_failures),
        "error",
    )

    output_refs = _as_list(bundle.get("output_refs"))
    has_clause_source = any(
        isinstance(output_ref, dict) and (output_ref.get("source_clause_ref") or output_ref.get("source_location"))
        for output_ref in output_refs
    )
    is_contract = _is_contract_review(bundle)
    _check(
        checks,
        "policy.contract_output_source",
        "Contract conclusion source reference",
        (not is_contract) or (bool(output_refs) and has_clause_source),
        "contract review output_refs include source_clause_ref or source_location"
        if (not is_contract) or (bool(output_refs) and has_clause_source)
        else "contract review requires at least one sourced output_ref",
        "error",
    )

    forbidden = list(_iter_forbidden_fields(bundle))
    _check(
        checks,
        "privacy.forbidden_field_names",
        "Privacy-minimized field names",
        not forbidden,
        "no forbidden raw-data or secret field names found"
        if not forbidden
        else "forbidden fields: " + ", ".join(f"{path} ({key})" for path, key in forbidden),
        "error",
    )

    hash_failures: list[str] = []
    for index, entry in enumerate(_as_list(bundle.get("content_hashes"))):
        if not isinstance(entry, dict) or not entry.get("target_path"):
            continue
        found, value = _json_pointer_get(bundle, str(entry["target_path"]))
        expected = entry.get("sha256") or entry.get("value")
        if not found:
            hash_failures.append(f"content_hashes[{index}] target not found: {entry['target_path']}")
        elif not expected:
            hash_failures.append(f"content_hashes[{index}] missing sha256")
        elif _hash_value(value) != expected:
            hash_failures.append(f"content_hashes[{index}] mismatch at {entry['target_path']}")
    _check(
        checks,
        "privacy.content_hash_targets",
        "Content hash target verification",
        not hash_failures,
        "target_path content hashes match actual bundle values" if not hash_failures else "; ".join(hash_failures),
        "error",
    )

    if signing_key is None:
        _check(
            checks,
            "signature.demo_hmac",
            "Demo HMAC signature verification",
            True,
            "signature verification skipped because no signing_key was provided",
            "warning",
        )
    else:
        verified, message = verify_bundle(bundle, signing_key)
        _check(checks, "signature.demo_hmac", "Demo HMAC signature verification", verified, message, "error")

    failed = [check for check in checks if not check["passed"]]
    blocking_failed = [check for check in failed if check["severity"] in {"error", "critical"}]
    summary = {
        "total_checks": len(checks),
        "passed_checks": len(checks) - len(failed),
        "failed_checks": len(failed),
        "blocking_failed_checks": len(blocking_failed),
        "errors": sum(1 for check in checks if not check["passed"] and check["severity"] == "error"),
        "warnings": sum(1 for check in checks if not check["passed"] and check["severity"] == "warning"),
    }
    return {"passed": not blocking_failed, "checks": checks, "summary": summary}
