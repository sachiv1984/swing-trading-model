"""
ST-33 (BLG-GOV-375, EPIC-06, v9.11) — scripts/check_sprint_backlog_owners.py
rejects any sprint_backlog.md Owner value not built from canonical role names
(shared_standards.md §16.11).
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("owners", ROOT / "scripts" / "check_sprint_backlog_owners.py")
owners = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(owners)
ROLES = owners.canonical_roles()


def test_roles_come_from_agent_files():
    assert "Metrics Definitions & Analytics Owner" in ROLES
    assert "Head of Specs Team" in ROLES
    assert "Metrics Definitions & Analytics Canonical Owner" not in ROLES


def test_canonical_single_and_shared_values_pass():
    text = "**Owner:** Head of Specs Team\n**Owner:** QA & Testing Owner; Director of Quality\n"
    assert owners.check_text(text, ROLES) == []


def test_non_canonical_values_fail():
    for bad in [
        "Metrics Definitions & Analytics Canonical Owner",          # variant spelling
        "Strategy Rules & System Intent Owner (ruling)",            # inline qualifier
        "Head of Specs Team, PMO Lead",                              # wrong separator
        "Head of Specs Team;PMO Lead",                               # missing space
        "Head of Specs",                                             # abbreviation
    ]:
        assert owners.check_text(f"**Owner:** {bad}\n", ROLES), bad


def test_v9_9_and_v9_11_sprint_backlogs_pass():
    for cycle in ["2026-09-30__release-v9.9", "2026-10-08__release-v9.11"]:
        path = ROOT / "claude" / "cycles" / cycle / "sprint_backlog.md"
        assert owners.check_text(path.read_text(), ROLES, str(path)) == [], cycle


def test_v9_10_sealed_qualifiers_are_reported():
    """v9.10's sealed sprint_backlog.md was written after the §16.11 rule landed but
    still carries 10 parenthetical qualifiers; the check reports each one."""
    path = ROOT / "claude" / "cycles" / "2026-10-06__release-v9.10" / "sprint_backlog.md"
    violations = owners.check_text(path.read_text(), ROLES, str(path))
    assert len(violations) == 10
    assert all("(" in v for v in violations)


def test_cli_exit_codes(tmp_path, capsys):
    good = tmp_path / "good.md"; good.write_text("**Owner:** PMO Lead\n")
    bad = tmp_path / "bad.md"; bad.write_text("**Owner:** PMO\n")
    assert owners.main([str(good)]) == 0
    assert owners.main([str(bad)]) == 1
    assert owners.main([]) == 2
