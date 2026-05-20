"""Run the RedCrag contract review AEP demo from the repository root."""

from __future__ import annotations

import json
from pathlib import Path

from redcrag_aep.cli import _build_demo_bundle, _demo_key, _load_rules
from redcrag_aep.signer import sign_bundle
from redcrag_aep.validator import validate_bundle


def main() -> None:
    key, default_key_used = _demo_key()
    bundle = sign_bundle(_build_demo_bundle(), key)
    output_path = Path("outputs/redcrag_aep_contract_review_demo_bundle.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = validate_bundle(bundle, rules=_load_rules(), signing_key=key)
    report = {
        "bundle_path": str(output_path),
        "validation_passed": result["passed"],
        "checks": result["checks"],
        "what_this_proves": [
            "The evidence package has the minimal AEP fields.",
            "The demo signature matches the bundle content.",
            "Receipt and human-review rules can be checked.",
            "Contract output can cite a source clause without storing full contract text.",
        ],
        "what_this_does_not_prove": [
            "It does not prove the model is correct.",
            "It does not prove external facts are true.",
            "It is not production legal signing or full compliance certification.",
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
