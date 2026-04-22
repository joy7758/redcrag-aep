from __future__ import annotations

import copy
import hmac
import hashlib

from collector.hash_chain import canonical_json


def sign_bundle(bundle: dict, secret: str = "demo-aep-secret") -> str:
    payload = copy.deepcopy(bundle)
    payload.get("integrity", {}).pop("signature", None)
    message = canonical_json(payload).encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()
    return f"hmac-sha256:{digest}"
