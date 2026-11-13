"""
ST-16 (BLG-OPS-195, EPIC-06, v9.17): weekly market-data volume check.

scripts/check_market_data_volume.py compares GET /ops/api-call-attribution's
weekly report with docs/ops/data_pipeline_cost_baseline.md §4 and prints a
Telegram advisory when any figure is more than 2x baseline (§5).

AC 1: a report over 2x baseline produces the advisory message; one under it
      produces none.
AC 2: a failed report call fails the workflow loudly (as ai-daily-cost-check.yml
      does): the script exits 2, never 0, and the workflow fails the job and
      sends a Telegram failure message.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_market_data_volume as cmv  # noqa: E402

WORKFLOW = REPO_ROOT / ".github" / "workflows" / "market-data-volume-check.yml"

BASELINE_MD = """
## 4. Weekly Baseline

| Source | Calls per week | Failures per week | Cost per week |
|--------|---------------|-------------------|---------------|
| Alpaca data (`alpaca_data`) | 2,616 | 0 | $0.00 |
| Alpaca news (`alpaca_news`) | 1 | 0 | $0.00 |
| Yahoo Finance (`yahoo`) | 4,488 | 665 | $0.00 |
| **Combined** | **7,105** | **665** | **$0.00** |

**Recorded:** 2026-11-11.

## 5. Advisory Threshold
"""


def _baseline():
    return cmv.parse_baseline(BASELINE_MD)


def _report(services, features=None, cost=0.0):
    """services: {name: (calls, failures)}; features: [(feature, {service: calls})]."""
    by_service = [{"service": s, "total_calls": c, "failure_count": f, "estimated_cost_usd": 0.0}
                  for s, (c, f) in services.items()]
    by_feature = [{"feature": name, "total_calls": sum(m.values()), "failure_count": 0,
                   "estimated_cost_usd": 0.0, "by_service": m}
                  for name, m in (features or [])]
    return {
        "window": "weekly",
        "total_calls": sum(c for c, _ in services.values()),
        "estimated_cost_usd": cost,
        "by_service": by_service,
        "by_feature": by_feature,
        "top_contributors": [name for name, _ in (features or [])][:3],
    }


# ---------------------------------------------------------------------------
# Baseline parsing — the §4 table is the only copy of the figures
# ---------------------------------------------------------------------------

def test_parse_baseline_reads_rows_and_combined():
    b = _baseline()
    assert b["yahoo"] == {"calls": 4488, "failures": 665, "cost_usd": 0.0}
    assert b["alpaca_data"]["calls"] == 2616
    assert b["combined"] == {"calls": 7105, "failures": 665, "cost_usd": 0.0}


def test_real_baseline_document_is_readable():
    """The committed §4 table parses, so the scheduled run will not fail on it."""
    b = cmv.load_baseline()
    assert "combined" in b and "yahoo" in b and "alpaca_data" in b
    assert b["combined"]["calls"] > 0


def test_baseline_without_combined_row_fails_loudly():
    broken = BASELINE_MD.replace("| **Combined** | **7,105** | **665** | **$0.00** |\n", "")
    with pytest.raises(cmv.CheckError):
        cmv.parse_baseline(broken)


def test_baseline_without_section_fails_loudly():
    with pytest.raises(cmv.CheckError):
        cmv.parse_baseline("## 3. How Volume Is Measured\n\nnothing here\n## 5. x\n")


# ---------------------------------------------------------------------------
# AC 1 — over 2x produces the advisory; under produces none
# ---------------------------------------------------------------------------

def test_report_under_2x_baseline_produces_no_message():
    report = _report({"alpaca_data": (2616, 0), "alpaca_news": (2, 0), "yahoo": (8000, 1200)},
                     [("POST /screener/run", {"alpaca_data": 2500, "yahoo": 500})])
    assert cmv.find_exceedances(report, _baseline()) == []
    assert cmv.build_message([], report) is None


def test_exactly_2x_baseline_is_not_an_advisory():
    report = _report({"alpaca_data": (2616, 0), "yahoo": (8976, 1330)})  # yahoo exactly 2x
    assert cmv.find_exceedances(report, _baseline()) == []


def test_source_calls_over_2x_baseline_names_source_and_top_features():
    report = _report(
        {"alpaca_data": (2600, 0), "yahoo": (9500, 600)},
        [("POST /signals/generate", {"yahoo": 6100}),
         ("POST /screener/run", {"alpaca_data": 2500, "yahoo": 900}),
         ("GET /earnings/{ticker}", {"yahoo": 2000}),
         ("GET /positions", {"yahoo": 500}),
         ("GET /news/{ticker}", {"alpaca_news": 1})],
    )
    found = cmv.find_exceedances(report, _baseline())
    assert {"source": "yahoo", "measure": "calls", "actual": 9500, "baseline": 4488} in found
    message = cmv.build_message(found, report)
    assert message is not None
    assert "yahoo: calls 9,500 vs baseline 4,488" in message
    # Top 3 features by calls to yahoo, in order; the 4th is left out.
    assert ("Top features: POST /signals/generate (6,100 calls), GET /earnings/{ticker} (2,000 calls), "
            "POST /screener/run (900 calls).") in message
    assert "GET /positions (500 calls)" not in message.split("yahoo:")[1].split("\n")[0]


def test_failures_over_2x_baseline_produce_advisory():
    report = _report({"alpaca_data": (2616, 0), "yahoo": (4488, 1400)},
                     [("GET /earnings/{ticker}", {"yahoo": 427})])
    found = cmv.find_exceedances(report, _baseline())
    measures = {(f["source"], f["measure"]) for f in found}
    assert ("yahoo", "failures") in measures
    assert ("combined", "failures") in measures
    assert "failures 1,400 vs baseline 665" in cmv.build_message(found, report)


def test_combined_calls_over_2x_produces_advisory_naming_all_sources():
    """The §4 source rows sum to the Combined row, so combined calls exceed 2x
    only alongside a source; both lines are reported, combined with the
    report's top_contributors."""
    report = _report({"alpaca_data": (5232, 0), "alpaca_news": (2, 0), "yahoo": (9100, 0)},
                     [("POST /screener/run", {"alpaca_data": 5232, "yahoo": 1000}),
                      ("POST /signals/generate", {"yahoo": 8100})])
    found = cmv.find_exceedances(report, _baseline())
    assert found == [
        {"source": "yahoo", "measure": "calls", "actual": 9100, "baseline": 4488},
        {"source": "combined", "measure": "calls", "actual": 14334, "baseline": 7105},
    ]
    message = cmv.build_message(found, report)
    assert "all sources: calls 14,334 vs baseline 7,105. Top features: POST /screener/run, POST /signals/generate." in message


def test_any_non_zero_cost_exceeds_a_zero_cost_baseline():
    report = _report({"alpaca_data": (2616, 0)}, cost=0.01)
    found = cmv.find_exceedances(report, _baseline())
    assert found == [{"source": "combined", "measure": "cost_usd", "actual": 0.01, "baseline": 0.0}]
    assert "estimated cost $0.01 vs baseline $0.00" in cmv.build_message(found, report)


def test_zero_baseline_failure_and_unlisted_source_exceed_on_any_use():
    report = _report({"alpaca_data": (2616, 1), "twelve_data": (3, 0)},
                     [("GET /prices/{ticker}", {"twelve_data": 3})])
    found = cmv.find_exceedances(report, _baseline())
    assert {"source": "alpaca_data", "measure": "failures", "actual": 1, "baseline": 0} in found
    assert {"source": "twelve_data", "measure": "calls", "actual": 3, "baseline": 0} in found
    assert "GET /prices/{ticker} (3 calls)" in cmv.build_message(found, report)


def test_empty_report_produces_no_message():
    report = _report({})
    assert cmv.find_exceedances(report, _baseline()) == []


# ---------------------------------------------------------------------------
# AC 2 — a failed report call fails loudly
# ---------------------------------------------------------------------------

def _run_main(tmp_path, response=None, exc=None):
    baseline = tmp_path / "baseline.md"
    baseline.write_text(BASELINE_MD, encoding="utf-8")
    message_file = tmp_path / "msg.txt"
    getter = MagicMock(side_effect=exc) if exc else MagicMock(return_value=response)
    with patch.object(cmv.requests, "get", getter), \
         patch.dict("os.environ", {"API_URL": "https://api.example", "API_KEY": "k"}):
        code = cmv.main(["--baseline", str(baseline), "--message-file", str(message_file)])
    return code, message_file, getter


def _response(status, body):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = body
    resp.text = str(body)
    return resp


def test_503_report_call_exits_2(tmp_path, capsys):
    body = {"status": "error", "error": "attribution_query_failed", "message": "db down"}
    code, message_file, _ = _run_main(tmp_path, _response(503, body))
    assert code == 2
    assert not message_file.exists()
    assert "HTTP 503" in capsys.readouterr().err


def test_unreachable_api_exits_2(tmp_path):
    code, _, _ = _run_main(tmp_path, exc=requests.ConnectionError("refused"))
    assert code == 2


def test_unexpected_body_exits_2_not_zero_calls(tmp_path):
    code, _, _ = _run_main(tmp_path, _response(200, {"status": "ok", "data": {}}))
    assert code == 2


def test_missing_credentials_exit_2(tmp_path):
    with patch.dict("os.environ", {"API_URL": "", "API_KEY": ""}):
        assert cmv.main(["--baseline", str(tmp_path / "none.md")]) == 2


def test_main_advisory_exits_1_and_writes_message(tmp_path):
    report = _report({"alpaca_data": (2616, 0), "yahoo": (9500, 600)},
                     [("POST /signals/generate", {"yahoo": 9500})])
    code, message_file, getter = _run_main(tmp_path, _response(200, {"status": "ok", "data": report}))
    assert code == 1
    assert "yahoo: calls 9,500" in message_file.read_text(encoding="utf-8")
    args, kwargs = getter.call_args
    assert args[0] == "https://api.example/ops/api-call-attribution"
    assert kwargs["params"] == {"window": "weekly"}
    assert kwargs["headers"] == {"X-API-Key": "k"}


def test_main_within_baseline_exits_0(tmp_path):
    report = _report({"alpaca_data": (2616, 0), "yahoo": (4488, 665)})
    code, message_file, _ = _run_main(tmp_path, _response(200, {"status": "ok", "data": report}))
    assert code == 0
    assert not message_file.exists()


# ---------------------------------------------------------------------------
# Workflow wiring
# ---------------------------------------------------------------------------

def _workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_workflow_is_weekly_and_runs_the_script():
    wf = _workflow()
    on = wf.get("on", wf.get(True))
    assert on["schedule"][0]["cron"] == "0 8 * * 1"
    steps = wf["jobs"]["check-market-data-volume"]["steps"]
    check = next(s for s in steps if s.get("id") == "check")
    assert "python3 scripts/check_market_data_volume.py" in check["run"]
    # Missing secrets fail the job rather than skipping it.
    assert 'exit 1' in check["run"].split("python3")[0]
    # Exit codes other than 0 and 1 fail the step.
    assert '[ "$code" -ne 0 ] && [ "$code" -ne 1 ]' in check["run"]


def test_workflow_sends_advisory_on_exit_1_and_alerts_on_failure():
    steps = _workflow()["jobs"]["check-market-data-volume"]["steps"]
    advisory = next(s for s in steps if s.get("if") == "steps.check.outputs.exit_code == '1'")
    assert "advisory_message.txt" in advisory["run"]
    assert "api.telegram.org" in advisory["run"]
    failure = next(s for s in steps if s.get("if") == "failure()")
    assert "api.telegram.org" in failure["run"]
    assert "FAILED" in failure["run"]
    assert steps[-1] is failure
