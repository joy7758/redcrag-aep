"""OpenTelemetry-style trace to RedCrag AEP demo converter.

This is a v0.2-alpha mapping demo. It handles a small OpenTelemetry-style
trace shape and does not claim full OpenTelemetry compatibility.
"""

from __future__ import annotations

from typing import Any

from .canonical import sha256_hex

FORBIDDEN_ATTR_NAMES = {
    "full_contract_text",
    "raw_medical_record",
    "customer_secret",
    "private_key",
    "api_key",
}


def _attr(attributes: dict[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in attributes:
            return attributes[name]
    return default


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes", "approved"}
    return bool(value)


def _as_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return str(value)


def _is_tool_span(name: str, attributes: dict[str, Any]) -> bool:
    return name.startswith("tool.") or bool(_attr(attributes, "tool.name", "tool_name"))


def _hash_entry(hash_id: str, target_path: str, value: Any) -> dict[str, str]:
    return {
        "hash_id": hash_id,
        "target_path": target_path,
        "sha256": sha256_hex(_as_text(value)),
    }


def _preserve_sensitive_attributes(span: dict[str, Any], attributes: dict[str, Any]) -> list[dict[str, Any]]:
    preserved: list[dict[str, Any]] = []
    for key, value in attributes.items():
        if str(key).lower() in FORBIDDEN_ATTR_NAMES:
            preserved.append(
                {
                    "span_id": str(span.get("span_id") or ""),
                    key: value,
                }
            )
    return preserved


def convert_otel_trace_to_aep(trace: dict[str, Any]) -> dict[str, Any]:
    """Convert a small OpenTelemetry-style trace dict into an unsigned AEP bundle."""
    spans = trace.get("spans", trace if isinstance(trace, list) else [])
    if not isinstance(spans, list):
        spans = []

    tool_calls: list[dict[str, Any]] = []
    input_refs: list[dict[str, Any]] = []
    output_refs: list[dict[str, Any]] = []
    receipt_refs: list[dict[str, Any]] = []
    content_hashes: list[dict[str, str]] = []
    policy_results: list[dict[str, Any]] = []
    approved = False
    reviewers: list[str] = []
    sensitive_trace_attributes: list[dict[str, Any]] = []

    for span in spans:
        if not isinstance(span, dict):
            continue
        attributes = span.get("attributes") if isinstance(span.get("attributes"), dict) else {}
        name = str(span.get("name", ""))
        span_id = str(span.get("span_id") or f"span-{len(tool_calls) + len(input_refs) + len(output_refs) + 1}")
        start_time = span.get("start_time")
        end_time = span.get("end_time")

        sensitive_trace_attributes.extend(_preserve_sensitive_attributes(span, attributes))

        input_ref = _attr(attributes, "input.ref")
        if input_ref is not None:
            input_record: dict[str, Any] = {
                "input_id": f"input-{len(input_refs) + 1}",
                "kind": "otel_trace_input_ref",
                "ref": _as_text(input_ref),
                "span_id": span_id,
            }
            content_sha256 = _attr(attributes, "content.sha256")
            if content_sha256 is not None:
                input_record["source_sha256"] = _as_text(content_sha256)
            input_refs.append(input_record)
            content_hashes.append(_hash_entry(f"hash-input-{len(input_refs)}-ref", f"/input_refs/{len(input_refs) - 1}/ref", input_record["ref"]))

        output_ref_value = _attr(attributes, "output.ref")
        output_summary = _attr(attributes, "output.summary")
        source_clause_ref = _attr(attributes, "source_clause_ref")
        source_location = _attr(attributes, "source_location")
        if output_ref_value is not None or output_summary is not None or source_clause_ref is not None or source_location is not None:
            output_record: dict[str, Any] = {
                "output_id": f"output-{len(output_refs) + 1}",
                "kind": "otel_trace_output_ref",
                "span_id": span_id,
            }
            if output_ref_value is not None:
                output_record["ref"] = _as_text(output_ref_value)
            if output_summary is not None:
                output_record["summary"] = _as_text(output_summary)
            else:
                output_record["summary"] = name
            if source_clause_ref is not None:
                output_record["source_clause_ref"] = _as_text(source_clause_ref)
            if source_location is not None:
                output_record["source_location"] = _as_text(source_location)
            output_refs.append(output_record)
            output_index = len(output_refs) - 1
            if "ref" in output_record:
                content_hashes.append(_hash_entry(f"hash-output-{len(output_refs)}-ref", f"/output_refs/{output_index}/ref", output_record["ref"]))
            if "summary" in output_record:
                content_hashes.append(
                    _hash_entry(f"hash-output-{len(output_refs)}-summary", f"/output_refs/{output_index}/summary", output_record["summary"])
                )

        if not _is_tool_span(name, attributes):
            continue

        tool_name = _attr(attributes, "tool.name", "tool_name", default=name.replace("tool.", "", 1))
        risk_level = _attr(attributes, "tool.risk_level", "risk_level")
        requires_receipt_value = _attr(attributes, "tool.requires_receipt", "requires_receipt")
        requires_receipt = _as_bool(requires_receipt_value) if requires_receipt_value is not None else False
        receipt_id = _attr(attributes, "tool.receipt_id", "receipt_id")

        tool_call: dict[str, Any] = {
            "tool_call_id": span_id,
            "tool_name": _as_text(tool_name),
            "started_at": start_time,
            "completed_at": end_time,
            "purpose": _as_text(_attr(attributes, "tool.purpose", "purpose", default=name)),
        }
        if risk_level is not None:
            tool_call["risk_level"] = _as_text(risk_level)
        if requires_receipt:
            tool_call["requires_receipt"] = True
        if receipt_id is not None:
            tool_call["receipt_id"] = _as_text(receipt_id)
            if requires_receipt_value is None:
                tool_call["requires_receipt"] = True
            receipt_refs.append(
                {
                    "receipt_id": _as_text(receipt_id),
                    "tool_call_id": span_id,
                    "kind": "otel_trace_receipt_ref",
                    "summary": f"Receipt imported from span {span_id}.",
                }
            )
        tool_calls.append(tool_call)

        span_approved = _attr(attributes, "human_review.approved")
        if span_approved is not None and _as_bool(span_approved):
            approved = True
        reviewer = _attr(attributes, "human_review.reviewer")
        if reviewer is not None:
            reviewers.append(_as_text(reviewer))

    start_times = [span.get("start_time") for span in spans if isinstance(span, dict) and span.get("start_time")]
    end_times = [span.get("end_time") for span in spans if isinstance(span, dict) and span.get("end_time")]
    trace_attrs = trace.get("attributes") if isinstance(trace.get("attributes"), dict) else {}
    workflow = trace.get("workflow") or _attr(trace_attrs, "workflow", default="otel_import")
    actor = trace.get("actor") if "actor" in trace else _attr(trace_attrs, "actor", default="unknown_agent")
    task = trace.get("task") or _attr(trace_attrs, "task", default="trace import")

    if receipt_refs:
        policy_results.append(
            {
                "policy_id": "otel_receipts_mapped",
                "passed": True,
                "summary": f"Mapped {len(receipt_refs)} receipt reference(s) from trace.",
            }
        )

    metadata: dict[str, Any] = {
        "source": "otel_to_aep_demo_converter",
        "otel_compatibility": "OpenTelemetry-style mapping demo only; not full OpenTelemetry compatibility.",
        "span_count": len(spans),
    }
    if sensitive_trace_attributes:
        metadata["sensitive_trace_attributes"] = sensitive_trace_attributes

    return {
        "schema_version": "aep-0.1",
        "run_id": str(trace.get("trace_id") or trace.get("run_id") or "otel-trace"),
        "workflow": workflow,
        "actor": actor,
        "task": task,
        "started_at": min(start_times) if start_times else None,
        "completed_at": max(end_times) if end_times else None,
        "tool_calls": tool_calls,
        "input_refs": input_refs,
        "output_refs": output_refs,
        "receipt_refs": receipt_refs,
        "human_review": {
            "approved": approved,
            "reviewers": sorted(set(reviewers)),
        },
        "policy_results": policy_results,
        "content_hashes": content_hashes,
        "signature": {},
        "metadata": metadata,
    }
