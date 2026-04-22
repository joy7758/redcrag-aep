from __future__ import annotations

from pathlib import Path


def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def summarize_text(text: str) -> str:
    words = text.split()
    return "Summary: " + " ".join(words[:20])


def write_file(path: str, text: str) -> str:
    Path(path).write_text(text, encoding="utf-8")
    return "written"
