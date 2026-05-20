"""Canonical JSON helpers for RedCrag AEP demo bundles."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_dumps(obj: Any) -> str:
    """Return stable JSON with sorted keys and no insignificant whitespace."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_hex(data: str | bytes) -> str:
    """Return a SHA-256 hex digest for UTF-8 text or bytes."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def hash_json(obj: Any) -> str:
    """Hash an object after canonical JSON serialization."""
    return sha256_hex(canonical_dumps(obj))
