"""
Tests for the AI-assisted Monthly P&L narrative — ST-25, EPIC-04, v9.11, BLG-FEAT-59

§13 determination: docs/product/decisions/decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md
Security checklist: docs/design/2026-10-08__release-v9.11/monthly-pnl-ai-narrative/ai_endpoint_security_checklist.md

The §13 determination requires backend tests, before DoQ, for every
output-side control: a pass and a fail case for the value check, the
direction check and the prescriptive/forward/tax scan, the regenerate-once
path, and a both-attempts-fail -> fallback case. The security checklist adds
the daily cap and its fail-closed path. The design record adds stored-text
reuse and invalidation, and that no export or snapshot carries the text.

CI-safe: every database and model call is mocked.
"""
import inspect
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from main import app  # noqa: E402
import services.monthly_pnl_narrative_service as svc  # noqa: E402
from services.monthly_pnl_narrative_service import (  # noqa: E402
    DAILY_CALL_CAP,
    ENDPOINT,
    NarrativeCapReached,
    NarrativeUnavailable,
    NoMonthsInRange,
    build_fallback_text,
    build_inputs,
    check_output,
    direction_check,
    generate_narrative,
    get_stored_narrative,
    input_hash,
    scan_language,
    source_values,
)

CLIENT = TestClient(app, raise_server_exceptions=False)

MONTHS = [
    {"year": 2025, "month": 5, "realised_pnl_gbp": 300.25, "trade_count": 4, "null_fee_trade_count": 0,
     "restated": False, "restated_diff_gbp": None},
    {"year": 2025, "month": 6, "realised_pnl_gbp": -120.40, "trade_count": 3, "null_fee_trade_count": 1,
     "restated": True, "restated_diff_gbp": -15.00},
    {"year": 2025, "month": 4, "realised_pnl_gbp": 80.00, "trade_count": 2, "null_fee_trade_count": 0,
     "restated": False, "restated_diff_gbp": None},
]
YEAR = 2025
TODAY = date(2026, 7, 1)  # the 2025/26 tax year has ended
INPUTS = build_inputs(YEAR, MONTHS, today=TODAY)

GOOD_TEXT = (
    "In the 2025/26 tax year you closed 9 trades with realised P&L of £259.85 across 3 months. "
    "May 2025 was the highest month at £300.25, and June 2025 was the lowest, a loss of £120.40."
)


def _usage():
    u = MagicMock()
    u.input_tokens = 1500
    u.output_tokens = 120
    return u


# ─── Inputs (Condition 2) ────────────────────────────────────────────────

class TestInputs:
    def test_only_the_fixed_aggregate_fields_reach_the_prompt(self):
        assert set(INPUTS) == {"tax_year", "tax_year_in_progress", "basis", "months", "range"}
        assert set(INPUTS["months"][0]) == {
            "month", "realised_pnl_gbp", "trade_count", "null_fee_trade_count", "restated", "restated_diff_gbp"}

    def test_months_ordered_oldest_first_with_their_year(self):
        assert [m["month"] for m in INPUTS["months"]] == ["April 2025", "May 2025", "June 2025"]

    def test_range_figures(self):
        r = INPUTS["range"]
        assert r["total_realised_pnl_gbp"] == 259.85
        assert r["total_trades"] == 9
        assert (r["best_month"], r["best_month_pnl_gbp"]) == ("May 2025", 300.25)
        assert (r["worst_month"], r["worst_month_pnl_gbp"]) == ("June 2025", -120.40)
        assert (r["profitable_months"], r["losing_months"], r["month_count"]) == (2, 1, 3)
        assert r["trades_without_fees"] == 1

    def test_two_aprils_in_one_tax_year_are_named_apart(self):
        rows = MONTHS + [{"year": 2026, "month": 4, "realised_pnl_gbp": 10.0, "trade_count": 1,
                          "null_fee_trade_count": 0, "restated": False, "restated_diff_gbp": None}]
        labels = [m["month"] for m in build_inputs(YEAR, rows, today=TODAY)["months"]]
        assert labels[0] == "April 2025" and labels[-1] == "April 2026"

    def test_hash_changes_when_a_figure_is_restated(self):
        restated = [dict(m) for m in MONTHS]
        restated[0]["realised_pnl_gbp"] = 301.00
        assert input_hash(build_inputs(YEAR, restated, today=TODAY)) != input_hash(INPUTS)

    def test_hash_ignores_the_in_progress_flag(self):
        assert input_hash(build_inputs(YEAR, MONTHS, today=date(2026, 1, 1))) == input_hash(INPUTS)


# ─── Value check (Condition 3) ────────────────────────────────────────────

class TestValueCheck:
    def test_text_using_only_given_numbers_passes(self):
        assert "numeric_cross_check_failed" not in check_output(GOOD_TEXT, YEAR, INPUTS)

    def test_a_computed_number_fails(self):
        text = "The average month made £86.62."  # not a given figure
        assert "numeric_cross_check_failed" in check_output(text, YEAR, INPUTS)

    def test_tax_year_label_and_boundary_days_are_allowed(self):
        values = source_values(YEAR, INPUTS)
        from services.debrief_service import numeric_cross_check
        assert numeric_cross_check("The 2025/26 tax year runs from 6 April 2025 to 5 April 2026.", values)


# ─── Direction check (Condition 3) ────────────────────────────────────────

SIGNED = [300.25, -120.40, 80.0, -15.0, 259.85]


class TestDirectionCheck:
    def test_loss_described_as_loss_passes(self):
        assert direction_check("June 2025 was a loss of £120.40.", SIGNED)

    def test_loss_with_minus_sign_passes(self):
        assert direction_check("June 2025 closed at -£120.40.", SIGNED)

    def test_loss_described_as_gain_fails(self):
        assert not direction_check("June 2025 was a gain of £120.40.", SIGNED)

    def test_negative_with_no_sign_and_no_loss_wording_fails(self):
        assert not direction_check("June 2025 came in at £120.40.", SIGNED)

    def test_gain_described_as_loss_fails(self):
        assert not direction_check("May 2025 was a loss of £300.25.", SIGNED)

    def test_positive_with_minus_sign_fails(self):
        assert not direction_check("May 2025 closed at -£300.25.", SIGNED)

    def test_gain_and_loss_in_one_sentence_judged_by_clause(self):
        assert direction_check("May 2025 gained £300.25, while June 2025 lost £120.40.", SIGNED)

    def test_rounded_magnitude_still_checked(self):
        assert not direction_check("June 2025 was a profit of £120.", SIGNED)

    def test_ambiguous_magnitude_is_not_judged(self):
        assert direction_check("A month was down £50.00.", [50.0, -50.0])


# ─── Language scan (Condition 4) ──────────────────────────────────────────

class TestLanguageScan:
    def test_descriptive_text_passes(self):
        assert scan_language(GOOD_TEXT) == []

    @pytest.mark.parametrize("text", [
        "You should trade less in volatile months.",
        "Consider reducing size after a losing month.",
    ])
    def test_prescriptive(self, text):
        assert "prescriptive" in scan_language(text)

    @pytest.mark.parametrize("text", [
        "At this rate the year will end positive.",
        "You are on track for a profitable year.",
        "Next month is likely to be stronger.",
        "If this trend continues, the total grows.",
    ])
    def test_forward_looking(self, text):
        assert "forward_looking" in scan_language(text)

    @pytest.mark.parametrize("text", [
        "These losses can be offset against gains for HMRC.",
        "Your capital gains are below the annual exempt amount.",
        "This is taxable income.",
        "You may carry losses forward.",
    ])
    def test_tax_advice(self, text):
        assert "tax_advice" in scan_language(text)

    def test_tax_year_as_a_label_is_allowed(self):
        assert scan_language("In the 2025/26 tax year you closed 9 trades.") == []


# ─── Fallback template ────────────────────────────────────────────────────

class TestFallback:
    def test_matches_the_spec_template(self):
        assert build_fallback_text(INPUTS) == (
            "2025/26: realised P&L of £259.85 across 9 closed trades in 3 months. "
            "Highest month: May 2025, £300.25. Lowest month: June 2025, -£120.40. "
            "2 months ended above zero and 1 below. "
            "1 closed trade has no fees recorded, so these figures may not reflect its costs."
        )

    def test_so_far_for_the_in_progress_year_and_plural_fees_caveat(self):
        rows = [dict(m, null_fee_trade_count=2) for m in MONTHS]
        text = build_fallback_text(build_inputs(YEAR, rows, today=date(2026, 1, 1)))
        assert text.startswith("2025/26 so far:")
        assert text.endswith("6 closed trades have no fees recorded, so these figures may not reflect their costs.")

    def test_fallback_itself_passes_the_language_scan(self):
        assert scan_language(build_fallback_text(INPUTS)) == []


# ─── generate_narrative flow ──────────────────────────────────────────────

REPORT = {"months": MONTHS, "estimated_unrealised_pnl": None, "unrealised_note": ""}


@pytest.fixture
def flow():
    with patch.object(svc, "get_portfolio", return_value={"id": "p1"}), \
         patch.object(svc, "get_monthly_pnl_report", return_value=REPORT), \
         patch.object(svc, "build_inputs", side_effect=lambda y, m: build_inputs(y, m, today=TODAY)), \
         patch.object(svc, "get_monthly_pnl_narrative", return_value=None) as get_stored, \
         patch.object(svc, "upsert_monthly_pnl_narrative",
                      side_effect=lambda pid, y, d: {**d, "generated_at": datetime(2026, 7, 1, tzinfo=timezone.utc)}) as upsert, \
         patch.object(svc, "count_claude_audit_entries_today", return_value=0) as count, \
         patch.object(svc, "create_claude_audit_entry") as audit, \
         patch.object(svc, "ANTHROPIC_API_KEY", "fake-key"), \
         patch("services.ai_output_sampling_service.maybe_sample_output"):
        yield {"get_stored": get_stored, "upsert": upsert, "count": count, "audit": audit}


class TestGenerateFlow:
    def test_compliant_first_attempt_is_stored_as_ai(self, flow):
        with patch.object(svc, "_call_claude", return_value=(GOOD_TEXT, _usage())) as call:
            out = generate_narrative(YEAR)
        assert call.call_count == 1
        assert out["source"] == "ai" and out["narrative"] == GOOD_TEXT and out["advisory"] is True
        assert out["year"] == YEAR
        assert flow["audit"].call_args.kwargs["compliance_check_result"] == "pass"
        assert flow["audit"].call_args.kwargs["endpoint"] == ENDPOINT

    def test_regenerate_once_then_pass(self, flow):
        responses = iter([("You should trade less. £300.25", _usage()), (GOOD_TEXT, _usage())])
        with patch.object(svc, "_call_claude", side_effect=lambda *a, **k: next(responses)) as call:
            out = generate_narrative(YEAR)
        assert call.call_count == 2
        assert out["source"] == "ai"
        results = [c.kwargs["compliance_check_result"] for c in flow["audit"].call_args_list]
        assert results[0].startswith("fail_regenerate:") and "prescriptive_language" in results[0]
        assert results[1] == "pass_on_regenerate"

    def test_both_attempts_fail_shows_the_fallback(self, flow):
        bad = "June 2025 was a gain of £120.40, and next month will be better."
        with patch.object(svc, "_call_claude", return_value=(bad, _usage())) as call:
            out = generate_narrative(YEAR)
        assert call.call_count == 2  # one regeneration covers every failure type
        assert out["source"] == "fallback"
        assert out["narrative"] == build_fallback_text(INPUTS)
        last = flow["audit"].call_args_list[-1].kwargs["compliance_check_result"]
        assert last.startswith("fail_fallback:")
        assert "direction_check_failed" in last and "forward_looking_language" in last
        stored = flow["upsert"].call_args.args[2]
        assert stored["narrative_text"] != bad

    def test_stored_narrative_is_returned_without_a_model_call_or_cap_check(self, flow):
        flow["get_stored"].return_value = {"narrative_text": "stored", "source": "ai",
                                           "generated_at": "2026-07-01T00:00:00+00:00"}
        with patch.object(svc, "_call_claude") as call:
            out = generate_narrative(YEAR)
        assert out["narrative"] == "stored"
        call.assert_not_called()
        flow["count"].assert_not_called()

    def test_regenerate_ignores_the_stored_narrative(self, flow):
        flow["get_stored"].return_value = {"narrative_text": "stored", "source": "ai", "generated_at": None}
        with patch.object(svc, "_call_claude", return_value=(GOOD_TEXT, _usage())) as call:
            out = generate_narrative(YEAR, regenerate=True)
        assert call.call_count == 1 and out["narrative"] == GOOD_TEXT

    def test_stored_lookup_uses_the_current_input_hash(self, flow):
        with patch.object(svc, "_call_claude", return_value=(GOOD_TEXT, _usage())):
            generate_narrative(YEAR)
        assert flow["get_stored"].call_args.args == ("p1", YEAR, input_hash(INPUTS))
        assert flow["upsert"].call_args.args[2]["input_hash"] == input_hash(INPUTS)

    def test_daily_cap_reached_makes_no_model_call(self, flow):
        flow["count"].return_value = DAILY_CALL_CAP
        with patch.object(svc, "_call_claude") as call, pytest.raises(NarrativeCapReached):
            generate_narrative(YEAR)
        call.assert_not_called()

    def test_cap_count_failure_fails_closed(self, flow):
        flow["count"].side_effect = Exception("db down")
        with patch.object(svc, "_call_claude") as call, pytest.raises(NarrativeUnavailable):
            generate_narrative(YEAR)
        call.assert_not_called()

    def test_model_failure_is_audited_and_nothing_is_stored(self, flow):
        with patch.object(svc, "_call_claude", side_effect=RuntimeError("boom")), \
             pytest.raises(NarrativeUnavailable):
            generate_narrative(YEAR)
        assert flow["audit"].call_args.kwargs["compliance_check_result"] == "model_call_failed"
        flow["upsert"].assert_not_called()

    def test_no_api_key_is_unavailable(self, flow):
        with patch.object(svc, "ANTHROPIC_API_KEY", ""), pytest.raises(NarrativeUnavailable):
            generate_narrative(YEAR)

    def test_no_months_raises(self, flow):
        with patch.object(svc, "get_monthly_pnl_report", return_value={"months": []}), \
             pytest.raises(NoMonthsInRange):
            generate_narrative(YEAR)

    def test_get_never_calls_the_model(self, flow):
        with patch.object(svc, "_call_claude") as call:
            out = get_stored_narrative(YEAR)
        call.assert_not_called()
        assert out == {"year": YEAR, "narrative": None, "source": None, "generated_at": None, "advisory": True}


# ─── Kept out of the record (Condition 5) ─────────────────────────────────

class TestKeptOutOfTheRecord:
    def test_narrative_path_never_touches_snapshots(self):
        src = inspect.getsource(svc).replace(svc.__doc__, "")  # code only, not the docstring
        for name in ("monthly_pnl_snapshots", "insert_monthly_pnl_snapshot", "_snapshot_month"):
            assert name not in src

    def test_exports_never_reference_the_narrative(self):
        import services.reports_service as rs
        for fn in (rs.build_monthly_pnl_csv, rs.build_tax_year_csv, rs.build_tax_year_pdf):
            assert "narrative" not in inspect.getsource(fn)
        assert "monthly_pnl_narrative" not in inspect.getsource(rs)

    def test_monthly_csv_carries_no_narrative_text(self):
        from services.reports_service import build_monthly_pnl_csv
        csv_text = build_monthly_pnl_csv(MONTHS)
        assert GOOD_TEXT not in csv_text and "narrative" not in csv_text.lower()

    def test_section13_comment_present(self):
        doc = svc.__doc__
        assert "§13 CONDITIONAL" in doc
        assert "decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md" in doc
        assert "direction" in doc


# ─── Routes ───────────────────────────────────────────────────────────────

ROUTE_SVC = "services.monthly_pnl_narrative_service"


class TestRoutes:
    def test_get_returns_data_with_advisory(self):
        payload = {"year": YEAR, "narrative": None, "source": None, "generated_at": None, "advisory": True}
        with patch(f"{ROUTE_SVC}.get_stored_narrative", return_value=payload):
            r = CLIENT.get(f"/reports/monthly-pnl/narrative?year={YEAR}")
        assert r.status_code == 200 and r.json() == {"status": "ok", "data": payload}

    def test_post_ok(self):
        payload = {"year": YEAR, "narrative": GOOD_TEXT, "source": "ai",
                   "generated_at": "2026-07-01T00:00:00+00:00", "advisory": True}
        with patch(f"{ROUTE_SVC}.generate_narrative", return_value=payload) as gen:
            r = CLIENT.post("/reports/monthly-pnl/narrative", json={"year": YEAR, "regenerate": True})
        assert r.status_code == 200 and r.json()["data"]["advisory"] is True
        gen.assert_called_once_with(YEAR, regenerate=True)

    def test_post_cap_reached_is_429_with_retry_after_and_no_narrative(self):
        with patch(f"{ROUTE_SVC}.generate_narrative", side_effect=NarrativeCapReached()):
            r = CLIENT.post("/reports/monthly-pnl/narrative", json={"year": YEAR})
        assert r.status_code == 429
        assert r.json() == {"status": "error", "message": "Daily limit for AI summaries reached. Try again tomorrow."}
        assert 0 < int(r.headers["Retry-After"]) <= 86401

    def test_post_unavailable_is_503(self):
        with patch(f"{ROUTE_SVC}.generate_narrative", side_effect=NarrativeUnavailable("x")):
            r = CLIENT.post("/reports/monthly-pnl/narrative", json={"year": YEAR})
        assert r.status_code == 503
        assert r.json()["message"] == "AI summary is unavailable right now."

    def test_post_no_months_is_404(self):
        with patch(f"{ROUTE_SVC}.generate_narrative", side_effect=NoMonthsInRange()):
            r = CLIENT.post("/reports/monthly-pnl/narrative", json={"year": YEAR})
        assert r.status_code == 404

    def test_post_future_tax_year_is_400(self):
        with patch(f"{ROUTE_SVC}.generate_narrative", side_effect=ValueError("tax year has not started yet")):
            r = CLIENT.post("/reports/monthly-pnl/narrative", json={"year": YEAR})
        assert r.status_code == 400

    def test_bad_year_is_400(self):
        assert CLIENT.get("/reports/monthly-pnl/narrative?year=99").status_code == 400

    def test_post_rate_limited_after_ten_a_minute(self):
        from services.rate_limiter import _ai_limiter
        _ai_limiter._windows.clear()
        with patch(f"{ROUTE_SVC}.generate_narrative", return_value={"year": YEAR}):
            codes = [CLIENT.post("/reports/monthly-pnl/narrative", json={"year": YEAR}).status_code for _ in range(11)]
        _ai_limiter._windows.clear()
        assert codes[:10] == [200] * 10 and codes[10] == 429


# ─── §13 boundary suite (docs/specs/qa/ai_s13_boundary_test_suite.md, B-MPN-0x) ─

class TestS13BoundarySuite:
    def test_b_mpn_01_system_prompt_is_advisory_and_descriptive(self, flow):
        """D1: the system prompt sent to the model forbids advice, forecasts and tax talk."""
        with patch.object(svc, "_call_claude", return_value=(GOOD_TEXT, _usage())) as call:
            generate_narrative(YEAR)
        system_prompt = call.call_args.args[0]
        assert "Never give advice or instructions" in system_prompt
        assert "Never forecast" in system_prompt
        assert "Never discuss tax" in system_prompt
        assert "data only" in system_prompt

    def test_b_mpn_02_advisory_always_true(self, flow):
        """D3: advisory is True on the generated, fallback and empty responses."""
        with patch.object(svc, "_call_claude", return_value=(GOOD_TEXT, _usage())):
            assert generate_narrative(YEAR)["advisory"] is True
        with patch.object(svc, "_call_claude", return_value=("You should buy more.", _usage())):
            assert generate_narrative(YEAR, regenerate=True)["advisory"] is True
        assert get_stored_narrative(YEAR)["advisory"] is True

    def test_b_mpn_03_no_trade_side_effects(self):
        """D2: the service imports no write path other than its own table and the audit log."""
        import ast
        tree = ast.parse(inspect.getsource(svc))
        imported = {a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module == "database"
                    for a in n.names}
        assert imported == {"get_portfolio", "get_monthly_pnl_narrative", "upsert_monthly_pnl_narrative",
                            "count_claude_audit_entries_today", "create_claude_audit_entry"}

    @pytest.mark.parametrize("text", ["Buy AAPL now.", "You could sell them before April.", "Add to it next week."])
    def test_b_mpn_04_instrument_directives_detected(self, text):
        """D4: instrument directives are caught by the output scan."""
        assert scan_language(text) != []

    def test_b_mpn_04_representative_output_is_clean(self):
        assert scan_language(GOOD_TEXT) == [] and scan_language(build_fallback_text(INPUTS)) == []

    def test_b_mpn_05_response_schema(self, flow):
        """D1, D3 schema: every field present; advisory is True."""
        with patch.object(svc, "_call_claude", return_value=(GOOD_TEXT, _usage())):
            out = generate_narrative(YEAR)
        assert set(out) == {"year", "narrative", "source", "generated_at", "advisory"}
        assert out["advisory"] is True and out["source"] in ("ai", "fallback")


# ─── Usage count (ST-26): one counted row per completed generation ────────

class TestUsageCountRule:
    @pytest.mark.parametrize("result,counted", [
        ("pass", True), ("pass_on_regenerate", True), ("fail_fallback:numeric_cross_check_failed", True),
        ("fail_regenerate:prescriptive_language", False), ("model_call_failed", False), (None, False),
    ])
    def test_is_generation_row(self, result, counted):
        assert svc.is_generation_row(ENDPOINT, result) is counted

    def test_other_endpoints_never_count(self):
        assert not svc.is_generation_row("POST /ai/chat", "pass")
        assert not svc.is_generation_row("POST /trades/{trade_id}/debrief", "fail_fallback:x")

    @pytest.mark.parametrize("responses", [
        [GOOD_TEXT],                                            # pass first time
        ["You should trade less. £300.25", GOOD_TEXT],          # pass on regenerate
        ["June 2025 was a gain of £120.40.", "Next month will be better."],  # fallback
    ])
    def test_each_completed_request_writes_exactly_one_counted_row(self, flow, responses):
        it = iter([(t, _usage()) for t in responses])
        with patch.object(svc, "_call_claude", side_effect=lambda *a, **k: next(it)):
            generate_narrative(YEAR)
        rows = [c.kwargs for c in flow["audit"].call_args_list]
        assert len(rows) == len(responses)  # every model call is audited
        assert sum(svc.is_generation_row(r["endpoint"], r["compliance_check_result"]) for r in rows) == 1

    def test_a_failed_model_call_writes_no_counted_row(self, flow):
        with patch.object(svc, "_call_claude", side_effect=RuntimeError("x")), pytest.raises(NarrativeUnavailable):
            generate_narrative(YEAR)
        rows = [c.kwargs for c in flow["audit"].call_args_list]
        assert not any(svc.is_generation_row(r["endpoint"], r["compliance_check_result"]) for r in rows)

    def test_a_stored_return_writes_no_row(self, flow):
        flow["get_stored"].return_value = {"narrative_text": "stored", "source": "ai", "generated_at": None}
        generate_narrative(YEAR)
        flow["audit"].assert_not_called()

    def test_sql_uses_the_same_endpoint_and_results(self):
        # Read from the file: tests/conftest.py replaces the database module with stubs.
        text = (Path(__file__).parent.parent / "backend" / "database.py").read_text()
        start = text.index("def count_monthly_pnl_narrative_generations(")
        src = text[start:text.index("\ndef ", start + 1)]
        assert f"'{ENDPOINT}'" in src
        for r in svc.TERMINAL_RESULTS:
            assert f"'{r}'" in src
        assert "fail\\\\_fallback:%%" in src
