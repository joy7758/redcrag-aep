"""Demo-grade HMAC signatures for RedCrag AEP bundles.

This module intentionally implements a low-risk local demo signature, not a
production legal signing system.
"""

from __future__ import annotations

import copy
import hmac
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any

from .canonical import canonical_dumps

ALGORITHM = "HMAC-SHA256-DEMO"
DEFAULT_KEY_HINT = "demo-key"


def _unsigned_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    unsigned = copy.deepcopy(bundle)
    unsigned.pop("signature", None)
    return unsigned


def _signature_value(bundle: dict[str, Any], key: str) -> str:
    payload = canonical_dumps(_unsigned_bundle(bundle)).encode("utf-8")
    return hmac.new(key.encode("utf-8"), payload, sha256).hexdigest()


def sign_bundle(bundle: dict[str, Any], key: str) -> dict[str, Any]:
    """Return a signed copy of an AEP bundle using demo HMAC-SHA256."""
    signed = copy.deepcopy(bundle)
    signed["signature"] = {
        "algorithm": ALGORITHM,
        "key_hint": DEFAULT_KEY_HINT,
        "signed_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "value": _signature_value(signed, key),
    }
    return signed


def verify_bundle(bundle: dict[str, Any], key: str) -> tuple[bool, str]:
    """Verify the demo signature on an AEP bundle."""
    signature = bundle.get("signature")
    if not isinstance(signature, dict):
        return False, "signature is missing or is not an object"
    if signature.get("algorithm") != ALGORITHM:
        return False, f"unsupported signature algorithm: {signature.get('algorithm')!r}"
    value = signature.get("value")
    if not isinstance(value, str) or not value:
        return False, "signature.value is missing"
    expected = _signature_value(bundle, key)
    if not hmac.compare_digest(value, expected):
        return False, "signature mismatch"
    return True, "signature valid for demo HMAC-SHA256"
