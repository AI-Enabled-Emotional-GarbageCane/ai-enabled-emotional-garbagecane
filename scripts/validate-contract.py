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
    contract = read_json("contracts/contract.v0.3.json")
    require(contract.get("contract_version") == "v0.3", "contract version must be v0.3")
    require(contract.get("status") == "finalized", "contract status must be finalized")
    require(set(contract.get("modules", {})) == {"firmware", "vision", "display"}, "contract modules must be firmware, vision, display")
    require(contract.get("hardware", {}).get("rgb_depth_camera") == "Intel RealSense L515", "hardware target must be Intel RealSense L515")
    require(contract.get("vision_model", {}).get("family") == "YOLOv11n", "vision model family must be YOLOv11n")

    modules = contract["modules"]
    require("l515_depth_distance_detection" in modules["firmware"].get("owns", []), "firmware must own l515_depth_distance_detection")
    require("l515_rgb_capture" in modules["vision"].get("owns", []), "vision must own l515_rgb_capture")
    require("l515_depth_distance_detection" in modules["display"].get("must_not_own", []), "display must not own l515_depth_distance_detection")

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
    require(invariants.get("num_objects_policy") == "vision_v1_fixed_1", "v0.3 must document vision v1 num_objects policy")
    return contract


def validate_docs(contract: dict) -> None:
    api = read_text("docs/api-contract.md")
    fact_map = read_text("docs/fact-map.md")
    decisions = read_text("docs/decision-log.md")
    agents = read_text("AGENTS.md")
    readme = read_text("README.md")
    docs_readme = read_text("docs/README.md")
    report = read_text("docs/00-report.md")
    system_design = read_text("docs/03-system-design.md")
    interaction_design = read_text("docs/04-interaction-design.md")
    team_plan = read_text("docs/05-team-and-plan.md")

    searchable = {
        "contracts/contract.v0.3.json": json.dumps(contract, ensure_ascii=False),
        "README.md": readme,
        "AGENTS.md": agents,
        "docs/README.md": docs_readme,
        "docs/api-contract.md": api,
        "docs/fact-map.md": fact_map,
        "docs/decision-log.md": decisions,
        "docs/00-report.md": report,
        "docs/03-system-design.md": system_design,
        "docs/04-interaction-design.md": interaction_design,
        "docs/05-team-and-plan.md": team_plan,
    }
    for path, text in searchable.items():
        for stale in ["D435", "d435", "YOLOv8n", "YOLOv8"]:
            require_not_contains(text, stale, path)

    for path, text in {
        "docs/api-contract.md": api,
        "docs/fact-map.md": fact_map,
        "docs/decision-log.md": decisions,
        "AGENTS.md": agents,
        "docs/03-system-design.md": system_design,
    }.items():
        require_contains(text, "v0.3", path)
        require_contains(text, "q_detected", path)
        require_contains(text, "q_result", path)
        require_contains(text, "user_detected", path)
        require_contains(text, "recognition_result", path)
        require_contains(text, "L515", path)
        require_contains(text, "YOLOv11n", path)

    for path, text in {
        "README.md": readme,
        "docs/README.md": docs_readme,
        "docs/00-report.md": report,
        "docs/04-interaction-design.md": interaction_design,
        "docs/05-team-and-plan.md": team_plan,
    }.items():
        require_contains(text, "v0.3", path)
        require_contains(text, "L515", path)
        require_contains(text, "YOLOv11n", path)

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
    require_contains(readme, "L515", "README.md")
    require_contains(readme, "YOLOv11n", "README.md")
    require_contains(system_design, '"event": "recognition_result"', "docs/03-system-design.md")
    require_contains(system_design, "num_objects=1", "docs/03-system-design.md")

    require_not_contains(readme, "互動 Option 按鈕", "README.md")
    require_not_contains(readme, "讓使用者選擇 / 確認", "README.md")
    require_not_contains(readme, "依辨識結果觸發對應動作", "README.md")


def validate_harness_files() -> None:
    validate_ps1 = ROOT / "validate.ps1"
    require(validate_ps1.exists(), "missing Windows validation entrypoint: validate.ps1")

    agents = read_text("AGENTS.md")
    docs_readme = read_text("docs/README.md")
    trace_readme = read_text("docs/implementation-traces/README.md")
    trace_template = read_text("docs/implementation-traces/TEMPLATE.md")
    require_contains(agents, "Windows", "AGENTS.md")
    require_contains(agents, "PowerShell", "AGENTS.md")
    require_contains(agents, ".\\validate.ps1", "AGENTS.md")
    require_contains(agents, "Implementation Trace Protocol", "AGENTS.md")
    require_contains(agents, "docs/implementation-traces/TEMPLATE.md", "AGENTS.md")
    require_contains(docs_readme, "Implementation Trace", "docs/README.md")
    require_contains(docs_readme, "implementation-traces/README.md", "docs/README.md")

    for path, text in {
        "docs/implementation-traces/README.md": trace_readme,
        "docs/implementation-traces/TEMPLATE.md": trace_template,
    }.items():
        for heading in [
            "Goal",
            "Scope",
            "Implementation Steps",
            "Problems Encountered",
            "Verification",
            "Follow-up",
            "Revision Notes",
        ]:
            require_contains(text, heading, path)


def validate_presentation_script() -> None:
    path = ROOT / "AI-情緒垃圾筒-講稿.md"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    for stale in ["D435", "YOLOv8n", "6 週", "自訓 TTS"]:
        require_not_contains(text, stale, "AI-情緒垃圾筒-講稿.md")
    require_contains(text, "L515", "AI-情緒垃圾筒-講稿.md")
    require_contains(text, "YOLOv11n", "AI-情緒垃圾筒-講稿.md")
    require_contains(text, "8 週", "AI-情緒垃圾筒-講稿.md")


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
    validate_harness_files()
    validate_presentation_script()
    print("[OK] center contract, docs, and subrepo lock sources are consistent")


if __name__ == "__main__":
    main()
