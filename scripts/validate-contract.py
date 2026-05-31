#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    file_path = ROOT / path
    if not file_path.exists():
        fail(f"missing required file: {path}")
    return file_path.read_text(encoding="utf-8")


def read_json(path: str) -> dict:
    file_path = ROOT / path
    if not file_path.exists():
        fail(f"missing required file: {path}")
    with file_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_contains(text: str, needle: str, path: str) -> None:
    require(needle in text, f"{path} must contain {needle!r}")


def require_not_contains(text: str, needle: str, path: str) -> None:
    require(needle not in text, f"{path} must not contain stale text {needle!r}")


def validate_contract_source() -> dict:
    contract = read_json("contracts/contract.v0.2.json")
    require(contract.get("contract_version") == "v0.2", "contract version must be v0.2")
    require(contract.get("status") == "finalized", "contract status must be finalized")
    require(set(contract.get("modules", {})) == {"firmware", "vision", "display"}, "contract modules must be firmware, vision, display")

    events = {event.get("name"): event for event in contract.get("events", [])}
    require(set(events) == {"user_detected", "recognition_result"}, "contract must define user_detected and recognition_result")

    expected = {
        "user_detected": {
            "queue": "q_detected",
            "direction": "firmware->vision",
            "required_fields": {"event", "distance_cm", "ts"},
        },
        "recognition_result": {
            "queue": "q_result",
            "direction": "vision->display",
            "required_fields": {"event", "class", "confidence", "num_objects", "snapshot_path", "ts"},
        },
    }

    for event_name, spec in expected.items():
        event = events[event_name]
        require(event.get("queue") == spec["queue"], f"{event_name} queue drifted")
        require(event.get("direction") == spec["direction"], f"{event_name} direction drifted")
        require(set(event.get("required_fields", [])) == spec["required_fields"], f"{event_name} required fields drifted")

    invariants = contract.get("behavioral_invariants", {})
    require(invariants.get("fully_automatic") is True, "fully_automatic invariant must be true")
    require(invariants.get("user_button") is False, "user_button invariant must be false")
    require(invariants.get("lid_mechanism") is False, "lid_mechanism invariant must be false")
    require(invariants.get("display_to_firmware_public_flow") is False, "display_to_firmware_public_flow invariant must be false")
    require(invariants.get("class_values") == ["accept", "reject"], "class values must be accept/reject")
    return contract


def validate_docs(contract: dict) -> None:
    api = read_text("docs/api-contract.md")
    fact_map = read_text("docs/fact-map.md")
    decisions = read_text("docs/decision-log.md")
    readme = read_text("README.md")
    system_design = read_text("docs/03-system-design.md")

    for path, text in {
        "docs/api-contract.md": api,
        "docs/fact-map.md": fact_map,
        "docs/decision-log.md": decisions,
    }.items():
        require_contains(text, "v0.2", path)
        require_contains(text, "q_detected", path)
        require_contains(text, "q_result", path)
        require_contains(text, "user_detected", path)
        require_contains(text, "recognition_result", path)

    for event in contract["events"]:
        for field in event["required_fields"]:
            require_contains(api, field, "docs/api-contract.md")
            require_contains(fact_map, field, "docs/fact-map.md")

    require_contains(api, "不再有 display → firmware", "docs/api-contract.md")
    require_contains(api, "無使用者按鈕", "docs/api-contract.md")
    require_contains(api, "無蓋子機構", "docs/api-contract.md")
    require_contains(readme, "無使用者按鈕", "README.md")
    require_contains(readme, "不做蓋子機構", "README.md")
    require_contains(readme, "multiprocessing.Queue", "README.md")
    require_contains(system_design, '"event": "recognition_result"', "docs/03-system-design.md")

    require_not_contains(readme, "互動 Option 按鈕", "README.md")
    require_not_contains(readme, "讓使用者選擇 / 確認", "README.md")
    require_not_contains(readme, "依辨識結果觸發對應動作", "README.md")


def validate_subrepo_locks(contract: dict) -> None:
    expected = {
        "firmware": {
            "owned_events": ["user_detected"],
            "consumed_events": [],
        },
        "vision": {
            "owned_events": ["recognition_result"],
            "consumed_events": ["user_detected"],
        },
        "display": {
            "owned_events": [],
            "consumed_events": ["recognition_result"],
        },
    }

    required_keys = {
        "contract_version",
        "source_repo",
        "source_commit",
        "module",
        "owned_events",
        "consumed_events",
        "forbidden_cross_repo_changes",
    }

    for module, spec in expected.items():
        path = f"contracts/subrepo-locks/{module}.contract.lock.json"
        lock = read_json(path)
        require(set(lock) == required_keys, f"{path} must use the fixed lock schema")
        require(lock["contract_version"] == contract["contract_version"], f"{path} contract_version drifted")
        require(lock["module"] == module, f"{path} module drifted")
        require(lock["owned_events"] == spec["owned_events"], f"{path} owned_events drifted")
        require(lock["consumed_events"] == spec["consumed_events"], f"{path} consumed_events drifted")
        require(lock["forbidden_cross_repo_changes"], f"{path} must list forbidden_cross_repo_changes")


def main() -> None:
    contract = validate_contract_source()
    validate_docs(contract)
    validate_subrepo_locks(contract)
    print("[OK] center contract, docs, and subrepo lock sources are consistent")


if __name__ == "__main__":
    main()
