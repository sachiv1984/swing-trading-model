"""
ST-18 (BLG-OPS-179, EPIC-03, v9.11) — the post-deploy stop health check fails
on a fixture with a non-§11 multiplier or a missing post-grace stop, and the
workflow alerts through the existing Telegram path.
"""
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "tests" / "fixtures" / "post_grace_stop_health"
_spec = importlib.util.spec_from_file_location("stop_health", ROOT / "scripts" / "check_post_grace_stop_health.py")
stop_health = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stop_health)


def test_healthy_fixture_passes(capsys):
    assert stop_health.main(["--fixture", str(FIX / "healthy.json")]) == 0
    assert "OK: 2 post-grace position(s)" in capsys.readouterr().out


def test_non_s11_multiplier_fails(capsys):
    assert stop_health.main(["--fixture", str(FIX / "non_s11_multiplier.json")]) == 1
    assert "MU: active_atr_multiplier=3.0 is not a §11 value" in capsys.readouterr().out


def test_missing_post_grace_stop_fails(capsys):
    assert stop_health.main(["--fixture", str(FIX / "missing_stop.json")]) == 1
    assert "DELL: post-grace position has no stop" in capsys.readouterr().out


def test_grace_positions_are_not_checked():
    assert stop_health.find_violations([
        {"ticker": "X", "grace_period": True, "current_stop": None, "active_atr_multiplier": None}
    ]) == []


def test_missing_multiplier_on_a_post_grace_position_fails():
    v = stop_health.find_violations([{"ticker": "Y", "grace_period": False, "current_stop": 10, "active_atr_multiplier": None}])
    assert v and "not a §11 value" in v[0]


def test_allowed_set_comes_from_the_single_parameter_source():
    import sys
    sys.path.insert(0, str(ROOT / "backend"))
    import strategy_parameters as sp
    assert stop_health.ALLOWED_MULTIPLIERS == (sp.INITIAL_ATR_MULTIPLIER, sp.PROFIT_ATR_MULTIPLIER)


def test_unreadable_source_exits_2(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json")
    assert stop_health.main(["--fixture", str(bad)]) == 2


def test_workflow_alerts_through_the_existing_telegram_path():
    wf = yaml.safe_load((ROOT / ".github" / "workflows" / "post-deploy-stop-health.yml").read_text())
    steps = wf["jobs"]["stop-health"]["steps"]
    alert = next(s for s in steps if s["name"].startswith("Send alert"))
    assert alert["if"] == "steps.check.outputs.rc != '0'"
    assert alert["env"]["TELEGRAM_BOT_TOKEN"] == "${{ secrets.TELEGRAM_BOT_TOKEN }}"
    assert "api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" in alert["run"]
    run_step = next(s for s in steps if s.get("id") == "check")
    assert "scripts/check_post_grace_stop_health.py" in run_step["run"]
