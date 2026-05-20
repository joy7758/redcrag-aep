from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from redcrag_aep.signer import verify_bundle
from redcrag_aep.validator import validate_bundle

ROOT = Path(__file__).resolve().parents[1]
SPECIMENS = ROOT / "specimens" / "contract_review"
RULES = ROOT / "rules" / "contract_review_rules.json"
DEMO_KEY = "redcrag-demo-key"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = load_json(RULES)

    def validate_specimen(self, name: str) -> dict:
        return validate_bundle(load_json(SPECIMENS / name), rules=self.rules, signing_key=DEMO_KEY)

    def test_valid_bundle_passes(self) -> None:
        result = self.validate_specimen("valid_bundle.json")
        self.assertTrue(result["passed"], result)

    def test_missing_receipt_fails(self) -> None:
        result = self.validate_specimen("invalid_missing_receipt.json")
        self.assertFalse(result["passed"])
        self.assertIn("policy.required_receipts", {check["id"] for check in result["checks"] if not check["passed"]})

    def test_missing_human_review_fails(self) -> None:
        result = self.validate_specimen("invalid_missing_human_review.json")
        self.assertFalse(result["passed"])
        self.assertIn("policy.high_risk_human_review", {check["id"] for check in result["checks"] if not check["passed"]})

    def test_tampered_hash_fails(self) -> None:
        result = self.validate_specimen("invalid_tampered_hash.json")
        self.assertFalse(result["passed"])
        self.assertIn("privacy.content_hash_targets", {check["id"] for check in result["checks"] if not check["passed"]})

    def test_full_contract_leak_fails(self) -> None:
        result = self.validate_specimen("invalid_full_contract_leak.json")
        self.assertFalse(result["passed"])
        self.assertIn("privacy.forbidden_field_names", {check["id"] for check in result["checks"] if not check["passed"]})

    def test_signature_modification_fails(self) -> None:
        bundle = load_json(SPECIMENS / "valid_bundle.json")
        passed, message = verify_bundle(bundle, DEMO_KEY)
        self.assertTrue(passed, message)

        tampered = copy.deepcopy(bundle)
        tampered["run_id"] = "redcrag-contract-demo-run-tampered"
        passed, message = verify_bundle(tampered, DEMO_KEY)
        self.assertFalse(passed, message)


if __name__ == "__main__":
    unittest.main()
