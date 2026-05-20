"""Demonstrate OpenTelemetry-style trace to RedCrag AEP conversion."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from redcrag_aep.cli import _demo_key, _load_rules
from redcrag_aep.otel_to_aep import convert_otel_trace_to_aep
from redcrag_aep.signer import sign_bundle
from redcrag_aep.validator import validate_bundle


def main() -> None:
    trace_path = Path("fixtures/otel_traces/valid_contract_review_trace.json")
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    key, default_key_used = _demo_key()
    bundle = sign_bundle(convert_otel_trace_to_aep(trace), key)
    validation = validate_bundle(bundle, rules=_load_rules(), signing_key=key)

    report = {
        "trace_id": trace.get("trace_id"),
        "run_id": bundle.get("run_id"),
        "tool_calls": len(bundle.get("tool_calls", [])),
        "receipt_refs": len(bundle.get("receipt_refs", [])),
        "human_review": bundle.get("human_review"),
        "validation_passed": validation["passed"],
        "what_this_proves": [
            "An OpenTelemetry-style trace can be mapped into the AEP minimal profile.",
            "Mapped tool calls, receipts, human review, output references, and content hashes can be validated.",
            "The converted bundle can be signed with the demo signer.",
        ],
        "what_this_does_not_prove": [
            "It does not prove full OpenTelemetry compatibility.",
            "It does not prove model correctness or external-world truth.",
            "It does not replace real platform or customer feedback.",
        ],
        "demo_key_warning": (
            "REDCRAG_DEMO_SIGNING_KEY is not set; using redcrag-demo-key for demo use only."
            if default_key_used
            else "REDCRAG_DEMO_SIGNING_KEY was used; still demo-grade HMAC, not production signing."
        ),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
