"""
Regression tests for scripts/check_api_performance_baseline_drift.py's
find_missing_endpoints()/_is_documented() (ST-17, BLG-OPS-142, EPIC-06,
v8.7).

Prior to this story, "documented" was decided by a bare whole-document
substring match, which produced false negatives (the script wrongly
concluded an endpoint WAS documented) for endpoints mentioned only in
passing prose -- e.g. the real case that motivated this fix,
`GET /trade-plans/tags`, which appeared only inside one explanatory
sentence about a different endpoint, with no table row or heading of its
own. Fixed by requiring table-row or heading context. This closes a fix
carried across 3 consecutive Post-Ship Closures (v8.4→v8.5→v8.6) per this
story's own AC framing.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import check_api_performance_baseline_drift as drift_check  # noqa: E402


class TestIsDocumented:
    def test_prose_only_mention_is_not_documented(self):
        """The real BLG-OPS-142 case: an endpoint named only inside a
        sentence about a DIFFERENT endpoint must not count as documented."""
        baseline_lines = [
            "- `GET /watchlist/tags`: single `SELECT DISTINCT unnest(tags)` on "
            "`watchlist` — no path parameters, consistent with `GET /trade-plans/tags` "
            "(§ existing pattern).",
        ]
        assert drift_check._is_documented("GET /trade-plans/tags", baseline_lines) is False

    def test_table_row_mention_is_documented(self):
        baseline_lines = [
            "| GET /analytics/trade-plan-completion-rate | v8.6 | Read — pending live timing run | 150–300ms (est.) |",
        ]
        assert drift_check._is_documented("GET /analytics/trade-plan-completion-rate", baseline_lines) is True

    def test_dedicated_heading_is_documented(self):
        baseline_lines = [
            "### POST /ai/check-daily-cost Latency Profile",
        ]
        assert drift_check._is_documented("POST /ai/check-daily-cost", baseline_lines) is True

    def test_numbered_heading_with_trailing_context_is_documented(self):
        baseline_lines = [
            "### 4.1 POST /test/endpoints Auth Bug (BLG-OPS-12)",
        ]
        assert drift_check._is_documented("POST /test/endpoints", baseline_lines) is True

    def test_substring_prefix_does_not_false_positive(self):
        """"GET /positions" must not be considered documented merely because
        a table row for the longer path "GET /positions/{id}" exists."""
        baseline_lines = [
            "| GET /positions/{id} | v2.4 | Read | 200ms |",
        ]
        assert drift_check._is_documented("GET /positions", baseline_lines) is False
        assert drift_check._is_documented("GET /positions/{id}", baseline_lines) is True

    def test_plain_paragraph_endpoint_mention_not_documented_even_if_frequent(self):
        """Multiple prose mentions still don't count -- only structural
        (table/heading) context does."""
        baseline_lines = [
            "GET /notifications/preferences (p50=4.6s) is an outlier warranting investigation.",
            "PATCH /notifications/preferences shares the same slow code path.",
            "Both GET /notifications/preferences and PATCH /notifications/preferences call ensure_alerts_tables().",
        ]
        assert drift_check._is_documented("PATCH /notifications/preferences", baseline_lines) is False


class TestFindMissingEndpointsAgainstRealFiles:
    def test_no_drift_against_current_repo_files(self):
        """Runs the real check against this repo's actual openapi.yaml and
        api_performance_baseline.md — the same invocation quality_gate.yml's
        CI job performs. Confirms the KNOWN_GAPS grandfathering (including
        this story's own 3 newly-surfaced entries) keeps the check green."""
        missing = drift_check.find_missing_endpoints(drift_check.OPENAPI_PATH, drift_check.BASELINE_PATH)
        assert missing == [], f"Unexpected undocumented endpoints: {missing}"
