"""Minimal OpenTelemetry-style trace to RedCrag AEP converter."""

from __future__ import annotations

from typing import Any


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


def convert_otel_trace_to_aep(trace: dict[str, Any]) -> dict[str, Any]:
    """Convert a small OpenTelemetry-like trace dict into an unsigned AEP bundle."""
    spans = trace.get("spans", trace if isinstance(trace, list) else [])
    if not isinstance(spans, list):
        spans = []

    tool_calls: list[dict[str, Any]] = []
    receipt_refs: list[dict[str, Any]] = []
    output_refs: list[dict[str, Any]] = []
    approved_tool_ids: list[str] = []

    for span in spans:
        if not isinstance(span, dict):
            continue
        attributes = span.get("attributes") if isinstance(span.get("attributes"), dict) else {}
        name = str(span.get("name", ""))
        tool_name = _attr(attributes, "tool.name", "tool_name")
        is_tool = "tool" in name.lower() or bool(tool_name)
        if not is_tool:
            continue

        tool_call_id = str(span.get("span_id") or f"span_{len(tool_calls) + 1}")
        receipt_id = _attr(attributes, "receipt_id")
        tool_call = {
            "tool_call_id": tool_call_id,
            "tool_name": str(tool_name or name),
            "started_at": span.get("start_time"),
            "completed_at": span.get("end_time"),
            "purpose": str(_attr(attributes, "purpose", default=name)),
        }
        risk_level = _attr(attributes, "risk_level")
        if risk_level:
            tool_call["risk_level"] = risk_level
        if receipt_id:
            tool_call["requires_receipt"] = True
            tool_call["receipt_id"] = receipt_id
            receipt_refs.append(
                {
                    "receipt_id": str(receipt_id),
                    "tool_call_id": tool_call_id,
                    "kind": str(_attr(attributes, "receipt.kind", default="external_action_receipt")),
                    "summary": str(_attr(attributes, "receipt.summary", default="receipt imported from trace")),
                }
            )
        tool_calls.append(tool_call)

        approved = _attr(attributes, "human_review.approved")
        if approved is not None and _as_bool(approved):
            approved_tool_ids.append(tool_call_id)

        source_clause_ref = _attr(attributes, "source_clause_ref")
        if source_clause_ref:
            output_refs.append(
                {
                    "output_id": f"output_{tool_call_id}",
                    "kind": "trace_mapped_conclusion",
                    "summary": str(_attr(attributes, "output.summary", default=name)),
                    "source_clause_ref": str(source_clause_ref),
                }
            )

    start_times = [span.get("start_time") for span in spans if isinstance(span, dict) and span.get("start_time")]
    end_times = [span.get("end_time") for span in spans if isinstance(span, dict) and span.get("end_time")]
    trace_attrs = trace.get("attributes") if isinstance(trace.get("attributes"), dict) else {}

    return {
        "schema_version": "aep-0.1",
        "run_id": str(trace.get("trace_id") or trace.get("run_id") or "otel-trace"),
        "workflow": str(_attr(trace_attrs, "workflow", default="otel_import")),
        "actor": str(_attr(trace_attrs, "actor", default="unknown_agent")),
        "task": str(_attr(trace_attrs, "task", default="trace import")),
        "started_at": min(start_times) if start_times else None,
        "completed_at": max(end_times) if end_times else None,
        "tool_calls": tool_calls,
        "input_refs": [],
        "output_refs": output_refs,
        "receipt_refs": receipt_refs,
        "human_review": {"approved": bool(approved_tool_ids), "reviewed_tool_call_ids": approved_tool_ids},
        "policy_results": [],
        "content_hashes": [],
        "signature": {},
        "metadata": {
            "source": "otel_to_aep_demo_converter",
            "otel_compatibility": "minimal-demo-mapping-only",
        },
    }
