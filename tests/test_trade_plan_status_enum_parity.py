"""
ST-31 (BLG-SPEC-177, EPIC-05, v9.11) — every TradePlan status enum in
openapi.yaml matches the live trade_plans_status_check constraint documented
in data_model.md DS-21 (7 values).
"""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _ds21_values():
    text = (ROOT / "docs" / "specs" / "data_model.md").read_text()
    section = text[text.index("## DS-21"):text.index("## DS-22")]
    check = re.search(r"CHECK \(status IN \((.*?)\)\)", section, re.S).group(1)
    return re.findall(r"'([a-z_]+)'", check)


def _status_enums(node, out):
    if isinstance(node, dict):
        if "status" in node and isinstance(node["status"], dict) and "draft" in (node["status"].get("enum") or []):
            out.append(node["status"]["enum"])
        if node.get("name") == "status" and "draft" in ((node.get("schema") or {}).get("enum") or []):
            out.append(node["schema"]["enum"])
        for v in node.values():
            _status_enums(v, out)
    elif isinstance(node, list):
        for v in node:
            _status_enums(v, out)
    return out


def test_ds21_lists_seven_statuses():
    assert _ds21_values() == ["draft", "research_pending", "research_complete",
                              "entry_conditions_set", "active", "closed", "abandoned"]


def test_every_trade_plan_status_enum_matches_ds21():
    spec = yaml.safe_load((ROOT / "docs" / "reference" / "openapi.yaml").read_text())
    enums = _status_enums(spec, [])
    assert len(enums) >= 4
    for enum in enums:
        assert sorted(enum) == sorted(_ds21_values())
