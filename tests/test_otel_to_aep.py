from __future__ import annotations

import json
import unittest
from pathlib import Path

from redcrag_aep.otel_to_aep import convert_otel_trace_to_aep
from redcrag_aep.signer import sign_bundle, verify_bundle
from redcrag_aep.validator import validate_bundle

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "otel_traces"
RULES = ROOT / "rules" / "contract_review_rules.json"
DEMO_KEY = "redcrag-demo-key"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class OtelToAepTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = load_json(RULES)

    def convert_sign_validate(self, fixture_name: str) -> tuple[dict, dict]:
        trace = load_json(FIXTURES / fixture_name)
        bundle = sign_bundle(convert_otel_trace_to_aep(trace), DEMO_KEY)
        return bundle, validate_bundle(bundle, rules=self.rules, signing_key=DEMO_KEY)

    def failed_ids(self, validation: dict) -> set[str]:
        return {check["id"] for check in validation["checks"] if not check["passed"]}

    def test_valid_contract_review_trace_passes(self) -> None:
        _, validation = self.convert_sign_validate("valid_contract_review_trace.json")
        self.assertTrue(validation["passed"], validation)

    def test_missing_receipt_trace_fails(self) -> None:
        _, validation = self.convert_sign_validate("invalid_missing_receipt_trace.json")
        self.assertFalse(validation["passed"])
        self.assertIn("policy.required_receipts", self.failed_ids(validation))

    def test_missing_human_review_trace_fails(self) -> None:
        _, validation = self.convert_sign_validate("invalid_missing_human_review_trace.json")
        self.assertFalse(validation["passed"])
        self.assertIn("policy.high_risk_human_review", self.failed_ids(validation))

    def test_full_contract_leak_trace_fails(self) -> None:
        _, validation = self.convert_sign_validate("invalid_full_contract_leak_trace.json")
        self.assertFalse(validation["passed"])
        self.assertIn("privacy.forbidden_field_names", self.failed_ids(validation))

    def test_valid_customer_service_trace_passes(self) -> None:
        _, validation = self.convert_sign_validate("valid_customer_service_trace.json")
        self.assertTrue(validation["passed"], validation)

    def test_converted_bundle_has_required_mapping_fields(self) -> None:
        trace = load_json(FIXTURES / "valid_contract_review_trace.json")
        bundle = convert_otel_trace_to_aep(trace)
        for field in ("run_id", "workflow", "tool_calls", "receipt_refs", "content_hashes"):
            self.assertIn(field, bundle)
        self.assertEqual(bundle["run_id"], "trace-contract-review-valid-001")
        self.assertGreaterEqual(len(bundle["tool_calls"]), 3)
        self.assertGreaterEqual(len(bundle["receipt_refs"]), 1)
        self.assertGreaterEqual(len(bundle["content_hashes"]), 1)

    def test_signed_converted_bundle_verifies(self) -> None:
        trace = load_json(FIXTURES / "valid_contract_review_trace.json")
        bundle = sign_bundle(convert_otel_trace_to_aep(trace), DEMO_KEY)
        passed, message = verify_bundle(bundle, DEMO_KEY)
        self.assertTrue(passed, message)


if __name__ == "__main__":
    unittest.main()
