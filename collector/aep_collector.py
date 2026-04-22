from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from collector.hash_chain import (
    canonical_json,
    compute_event_hash,
    sha256_file,
    sha256_text,
)
from collector.signer import sign_bundle


class AEPCollector:
    def __init__(
        self,
        policy_path: Path,
        risk_report_path: Path,
        out_dir: Path,
        scenario: str,
        run_id: str,
    ) -> None:
        self.policy_path = Path(policy_path)
        self.risk_report_path = Path(risk_report_path)
        self.out_dir = Path(out_dir)
        self.scenario = scenario
        self.run_id = run_id
        self.events: list[dict[str, Any]] = []

        self.policy = self._load_json(self.policy_path)
        self.risk_report = self._load_json(self.risk_report_path)
        self.allowed_tools = set(self.policy.get("allowed_tools", []))
        self.denied_tools = set(self.policy.get("denied_tools", []))

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def call_tool(self, tool_name: str, func: Callable[..., str], *args: Any, **kwargs: Any) -> str | None:
        event_index = len(self.events) + 1
        risk_refs = self._risk_refs_for_tool(tool_name)
        allowed = tool_name in self.allowed_tools and tool_name not in self.denied_tools
        input_hash = sha256_text(canonical_json({"args": args, "kwargs": kwargs, "tool": tool_name}))

        output: str | None = None
        if allowed:
            output = func(*args, **kwargs)
            output_hash = sha256_text(output)
            policy_decision = "allow"
            execution_status = "executed"
        else:
            output_hash = None
            policy_decision = "deny"
            execution_status = "blocked"

        event_without_hash = {
            "event_id": f"evt-{event_index:03d}",
            "run_id": self.run_id,
            "timestamp": f"2026-01-01T00:00:{event_index:02d}Z",
            "actor": "demo-agent-001",
            "action": "tool_call",
            "tool": tool_name,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "policy_decision": policy_decision,
            "execution_status": execution_status,
            "risk_refs": risk_refs,
            "prev_event_hash": self.events[-1]["event_hash"] if self.events else None,
        }
        event = dict(event_without_hash)
        event["event_hash"] = compute_event_hash(event_without_hash)
        self.events.append(event)
        return output

    def _risk_refs_for_tool(self, tool_name: str) -> list[str]:
        refs = [
            finding["risk_id"]
            for finding in self.risk_report.get("findings", [])
            if finding.get("target") == tool_name
        ]
        return sorted(refs)

    def write_events(self) -> Path:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        event_path = self.out_dir / "aep-events.jsonl"
        with event_path.open("w", encoding="utf-8") as handle:
            for event in self.events:
                handle.write(canonical_json(event) + "\n")
        return event_path

    def write_bundle(self) -> Path:
        event_path = self.out_dir / "aep-events.jsonl"
        if not event_path.exists():
            self.write_events()

        bundle = {
            "aep_version": "0.1",
            "bundle_id": f"bundle-{self.scenario}-001",
            "fdo": {
                "object_id": f"fdo:demo:{self.run_id}",
                "profile_type": "risk-linked-aep",
                "profile_version": "0.1",
                "pid_like_id": f"pid:demo:{self.run_id}",
            },
            "agent": {
                "agent_id": "demo-agent-001",
                "agent_name": "Deterministic Demo Agent",
                "agent_version": "0.1",
            },
            "execution": {
                "run_id": self.run_id,
                "scenario": self.scenario,
                "task_id": "task-demo-001",
                "started_at": "2026-01-01T00:00:00Z",
                "ended_at": f"2026-01-01T00:00:{len(self.events) + 1:02d}Z",
                "environment_hash": sha256_text("python-stdlib-aep-demo"),
            },
            "policy": self.policy,
            "risk_links": self.risk_report.get("findings", []),
            "evidence": {
                "event_log": "aep-events.jsonl",
                "event_log_hash": sha256_file(event_path),
                "event_count": len(self.events),
                "previous_bundle_hash": None,
            },
            "integrity": {
                "signature": "",
                "signing_key_id": "demo-hmac-key-001",
                "signature_method": "demo-hmac-sha256",
            },
        }
        bundle["integrity"]["signature"] = sign_bundle(bundle)

        bundle_path = self.out_dir / "aep-bundle.json"
        bundle_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return bundle_path
