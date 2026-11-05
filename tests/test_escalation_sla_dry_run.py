"""
ST-43 (BLG-GOV-193, EPIC-07, v9.15) — the escalation SLA-breach dry run
(scripts/escalation_sla_dry_run.py) on a scratch copy of the state files.

A synthetic Open escalation 8h past its 72h SLA must trigger the
BLOCKED_SLA_BREACH notice (shared_standards.md §4/§16.4) and Release
Planning's SLA_BREACH_CARRIED halt (release_planning_prompt.md STEP -1.6),
and the reminder workflow's own Python must open an issue. The live
.claude_current_state.json must be unchanged. Record:
docs/ops/escalation_sla_breach_dry_run_2026-11-05.md.
"""
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("sla_dry_run", ROOT / "scripts" / "escalation_sla_dry_run.py")
dry = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dry)

NOW = datetime(2026, 11, 5, 15, 0, tzinfo=timezone.utc)


def _result():
    return dry.dry_run(NOW)


def test_both_breach_checks_fire_for_the_synthetic_open_escalation():
    s = _result()["synthetic"]
    for esc in ("ESC-EXEC-DRYRUN-01", "ESC-EXEC-DRYRUN-02"):
        assert esc in s["blocked_sla_breach"]
        assert esc in s["notices_in_scratch_escalations"]
        assert esc in s["sla_breach_carried"]
        assert esc in s["step_minus_1_2a_advisory"]
    assert s["blocked_sla_breached_written"] is True


def test_controls_are_not_selected():
    s = _result()["synthetic"]
    for key in ("blocked_sla_breach", "sla_breach_carried", "step_minus_1_2a_advisory"):
        assert "ESC-EXEC-DRYRUN-04" not in s[key]  # Resolved
        assert "ESC-EXEC-DRYRUN-05" not in s[key]  # inside its SLA


def test_reminder_workflow_python_opens_then_comments():
    s = _result()["synthetic"]
    created = s["workflow"]
    assert created["returncode"] == 0, created["stderr"]
    assert [c[:2] for c in created["gh_calls"]] == [["issue", "list"], ["issue", "create"]]
    body = created["gh_calls"][1][created["gh_calls"][1].index("--body") + 1]
    assert "ESC-EXEC-DRYRUN-01" in body and "ESC-EXEC-DRYRUN-05" not in body
    commented = s["workflow_with_existing_issue"]
    assert [c[:3] for c in commented["gh_calls"]] == [["issue", "list", "--repo"], ["issue", "comment", "1"]]


def test_live_state_file_is_never_written():
    result = _result()
    assert result["live_state_unchanged"] is True
    assert not Path(result["scratch_dir"]).exists()  # temporary copy removed
