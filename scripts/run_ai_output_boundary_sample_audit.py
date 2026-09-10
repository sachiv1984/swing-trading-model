#!/usr/bin/env python3
"""
Quarterly AI Output Sampling Audit — ST-22 (BLG-GOV-178, EPIC-05, v9.3)

Scans a sample of AI-generated output text for §13.2 boundary-language
violations (claude/strategy/strategy_rules.md §13.2 — "not an automated
trading bot... not a discretionary or adaptive rule system... not a
machine-learning or AI-driven prediction system") and for prediction-style
language that would suggest deterministic/no-prediction drift.

Two check classes:
  - Prescriptive language: directive/command phrasing ("you should",
    "you must", "we recommend", ...) — extends the pattern already
    established and in production use for post-trade debriefs
    (backend/services/debrief_service.py::scan_prescriptive), generalised
    here so it can be applied to any AI-generated text field, not just
    debriefs.
  - Prediction language: future-certainty claims ("will rise", "will fall",
    "is expected to", "predicted to reach", ...) that would suggest the
    output is forecasting rather than describing current/historical state.

Sample input: a list of (source, text) tuples. This run's sample is
documented in the audit's own report — see
docs/ops/ai_output_boundary_sample_audit_20260910.md for why this quarter's
sample uses illustrative example text from canonical AI-endpoint contract
docs rather than live production audit-log records (no live DB/API access
in this execution environment).

Usage: python3 scripts/run_ai_output_boundary_sample_audit.py
"""
import re
import sys

# Mirrors backend/services/debrief_service.py::_PRESCRIPTIVE_PATTERNS,
# generalised (not debrief-specific wording) for cross-feature use.
_PRESCRIPTIVE_PATTERNS = [
    r"\byou should\b",
    r"\byou need to\b",
    r"\byou must\b",
    r"\bconsider (doing|trying|reducing|increasing|holding|cutting|buying|selling)\b",
    r"\bnext time,?\s*(do|try|consider)\b",
    r"\btry (doing|to)\b",
    r"\b(reduce|increase|lower|raise) (your|the) (position|size|risk|stop)\b",
    r"\bmake sure to\b",
    r"\bit('|’)?s (recommended|advisable|best) (that|to)\b",
    r"\bwe recommend\b",
    r"\b(buy|sell|enter|exit) now\b",
    r"\bexecute (this|the) trade\b",
]
_PRESCRIPTIVE_RE = re.compile("|".join(_PRESCRIPTIVE_PATTERNS), re.IGNORECASE)

_PREDICTION_PATTERNS = [
    r"\bwill (rise|fall|climb|drop|reach|hit|break|surge|decline)\b",
    r"\bis expected to\b",
    r"\bpredicted to\b",
    r"\bforecast(s|ed|ing)?\b",
    r"\bis (likely|certain|guaranteed) to\b",
    r"\bshould (rise|fall|climb|drop|reach|hit)\b",
]
_PREDICTION_RE = re.compile("|".join(_PREDICTION_PATTERNS), re.IGNORECASE)


def scan_prescriptive(text: str) -> bool:
    """True if prescriptive/directive phrasing is found (a §13.2 violation)."""
    if not text:
        return False
    return bool(_PRESCRIPTIVE_RE.search(text))


def scan_prediction(text: str) -> bool:
    """True if future-prediction phrasing is found (a §13.2/determinism
    violation — the system describes current/historical state, it does not
    forecast)."""
    if not text:
        return False
    return bool(_PREDICTION_RE.search(text))


# This quarter's sample (2026-09-10) — see the audit report for provenance
# and the "why illustrative examples, not live records" disclosure.
SAMPLE = [
    ("journal-summary (POST /ai/journal-summary)", "Across the selected trades, recurring themes include..."),
    ("daily-briefing summary (POST /ai/daily-briefing)", "Your portfolio has 3 open positions. NVDA is near its trailing stop — monitor closely today. Markets are risk-on with two strong new signals."),
    ("daily-briefing action (POST /ai/daily-briefing)", "Within 3% of trailing stop — watch closely."),
    ("daily-briefing action (POST /ai/daily-briefing)", "Rank #1 momentum signal today."),
    ("chat response (POST /ai/chat)", "NVDA is currently closest to its trailing stop, sitting 2.8% above the stop level of £450.00."),
    ("debrief summary_text (POST /trades/{id}/debrief)", "Entered at 100.0, exited at 108.5. P&L: +8.50 (+8.50%). Exit reason: Target Reached. Held 12 day(s). Plan called for entry at 100.0, planned stop 95.0, R target 2.0"),
    ("debrief focus_area_text (POST /trades/{id}/debrief)", "Your exit was 3 days earlier than the 15-day median holding period across your last 5 closed trades in this setup type."),
    ("generate-plan setup_thesis (POST /trade-plans/generate-plan)", "Strong momentum breakout above the 52-week high with confirmed volume surge, supported by Risk On regime."),
    ("generate-plan entry_rationale (POST /trade-plans/generate-plan)", "Price holding above the 200 SMA with ATR expanding at 1.8x baseline; momentum at +4.2% with regime firmly Risk On."),
    ("generate-plan early_exit_conditions (POST /trade-plans/generate-plan)", "Close below 200 SMA; regime flips to Risk Off; price retraces more than 1 ATR from entry."),
]


def run_audit(sample=None):
    sample = sample if sample is not None else SAMPLE
    results = []
    for source, text in sample:
        results.append({
            "source": source,
            "text": text,
            "prescriptive_violation": scan_prescriptive(text),
            "prediction_violation": scan_prediction(text),
        })
    return results


def main():
    results = run_audit()
    violations = [r for r in results if r["prescriptive_violation"] or r["prediction_violation"]]
    print(f"AI Output Boundary Sample Audit — {len(results)} samples scanned")
    print(f"Violations found: {len(violations)}")
    for r in results:
        flag = ""
        if r["prescriptive_violation"]:
            flag += " [PRESCRIPTIVE]"
        if r["prediction_violation"]:
            flag += " [PREDICTION]"
        status = "VIOLATION" + flag if flag else "clean"
        print(f"  [{status}] {r['source']}: {r['text'][:80]}")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
