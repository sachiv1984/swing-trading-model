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

A third, separate metric (ST-04, BLG-AI-10, EPIC-01, v9.12; AI Compliance &
Governance Officer ruling, ESC-EXEC-20261013-01):
  - Stop-time missing: a sentence citing a stop ("stop"/"stops") in an
    output that never states a recalculation time ("recalculated" plus a
    YYYY-MM-DD date, or "not recalculated since entry"). This is a
    correctness metric, not a §13.2 boundary breach: it is reported as its
    own [STOP-TIME-MISSING] count and does NOT affect the exit code. Samples
    are the raw model output, before ai_service's code-written note is
    appended, so this count is the model's own miss rate.

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
from pathlib import Path

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


def load_real_samples_from_store(limit: int = 10):
    """ST-23 (BLG-AI-06, EPIC-05, v9.4): return up to `limit` genuine,
    non-illustrative (source, text) tuples from the ai_output_boundary_samples
    store, newest first -- or [] if the store is empty, unreachable, or the
    backend package is not importable from this invocation context (e.g. run
    outside the backend/ virtualenv). Never raises: a store-access failure
    here means main() falls back to the illustrative SAMPLE, the same
    disclosed behaviour this script already had before this store existed.
    """
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
        from database import get_ai_output_boundary_samples
        rows = get_ai_output_boundary_samples(limit=limit)
        return [(f"{r['feature']} [real sample, {r['sampled_at']}]", r["output_text"]) for r in rows]
    except Exception:
        return []


_STOP_WORD_RE = re.compile(r"\bstops?\b", re.IGNORECASE)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n")
_RECALC_TIME_RE = re.compile(r"recalculated\b.*?\d{4}-\d{2}-\d{2}", re.IGNORECASE | re.DOTALL)
_NOT_RECALCULATED_RE = re.compile(r"not recalculated since entry", re.IGNORECASE)


def scan_stop_time_missing(text: str) -> bool:
    """True if the text cites a stop but states no recalculation time anywhere
    (ST-04). Context-free: it cannot tell which position a time belongs to,
    so any stated time clears the whole output."""
    if not text:
        return False
    if _RECALC_TIME_RE.search(text) or _NOT_RECALCULATED_RE.search(text):
        return False
    return any(_STOP_WORD_RE.search(s) for s in _SENTENCE_SPLIT_RE.split(text))


def stop_time_check_applies(source: str) -> bool:
    """The stop-time metric covers daily-briefing and chat output only (the
    two features whose context carries stop_calculated_at)."""
    return "daily-briefing" in source or "POST /ai/chat" in source


def run_audit(sample=None):
    sample = sample if sample is not None else SAMPLE
    results = []
    for source, text in sample:
        results.append({
            "source": source,
            "text": text,
            "prescriptive_violation": scan_prescriptive(text),
            "prediction_violation": scan_prediction(text),
            "stop_time_missing": stop_time_check_applies(source) and scan_stop_time_missing(text),
        })
    return results


def main():
    real_samples = load_real_samples_from_store(limit=10)
    if real_samples:
        results = run_audit(real_samples)
        sample_type = f"real (from ai_output_boundary_samples, {len(real_samples)} rows)"
    else:
        results = run_audit()
        sample_type = "illustrative (no real samples available -- see docs/ops/ai_output_boundary_sample_audit_20260910.md's disclosed environment constraint)"
    violations = [r for r in results if r["prescriptive_violation"] or r["prediction_violation"]]
    print(f"AI Output Boundary Sample Audit — {len(results)} samples scanned ({sample_type})")
    print(f"Violations found: {len(violations)}")
    stop_time_missing = [r for r in results if r["stop_time_missing"]]
    print(f"Stop-time missing (correctness metric, not a §13.2 violation; exit code unaffected): {len(stop_time_missing)}")
    for r in results:
        flag = ""
        if r["prescriptive_violation"]:
            flag += " [PRESCRIPTIVE]"
        if r["prediction_violation"]:
            flag += " [PREDICTION]"
        status = "VIOLATION" + flag if flag else "clean"
        metric = " [STOP-TIME-MISSING]" if r["stop_time_missing"] else ""
        print(f"  [{status}]{metric} {r['source']}: {r['text'][:80]}")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
