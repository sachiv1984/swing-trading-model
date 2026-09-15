"""
Generation-time opt-in sampling hook for AI-output boundary-language
audits (ST-23, BLG-AI-06, EPIC-05, v9.4).

Lets scripts/run_ai_output_boundary_sample_audit.py draw a genuine,
non-illustrative sample of real AI-generated output text, instead of the
hand-authored illustrative examples used for the Q3 2026 audit
(docs/ops/ai_output_boundary_sample_audit_20260910.md).

Design constraints (from this story's own AC):
  - Default OFF. Sampling only happens when AI_OUTPUT_SAMPLING_ENABLED is
    explicitly set to a truthy value.
  - Rate-bounded, not full-content logging of every response. Even when
    enabled, only a fraction of calls (AI_OUTPUT_SAMPLING_RATE, default
    0.1 = 10%) are actually written to the store.
  - Never breaks the caller. All failures inside maybe_sample_output()
    are swallowed -- the same fail-safe convention already used by
    database.create_gemini_audit_entry()/create_claude_audit_entry(), so
    a sampling-store outage can never turn into a user-facing AI-response
    failure.
"""
import os
import random

_TRUTHY = {"1", "true", "yes", "on"}


def is_sampling_enabled() -> bool:
    """Reads AI_OUTPUT_SAMPLING_ENABLED fresh on every call (not cached at
    import time) so a test or an ops toggle takes effect immediately."""
    return os.environ.get("AI_OUTPUT_SAMPLING_ENABLED", "").strip().lower() in _TRUTHY


def sampling_rate() -> float:
    """Reads AI_OUTPUT_SAMPLING_RATE, clamped to [0.0, 1.0]. Defaults to
    0.1 (10%) -- enough to accumulate a real sample within a reasonable
    number of calls, far short of full-content logging of every response."""
    raw = os.environ.get("AI_OUTPUT_SAMPLING_RATE", "0.1")
    try:
        rate = float(raw)
    except (TypeError, ValueError):
        rate = 0.1
    return max(0.0, min(1.0, rate))


def maybe_sample_output(feature: str, output_text: str, model_version: str | None = None) -> bool:
    """Call this immediately after a successful AI generation call, passing
    the actual generated text. Attempts a write to ai_output_boundary_samples
    only if sampling is enabled AND this call wins the rate-bounded coin
    flip. Returns True if a write was attempted (disabled or not-selected ->
    False; enabled and selected -> True), NOT whether the underlying DB
    write actually succeeded -- database.create_ai_output_boundary_sample()
    is deliberately fire-and-forget (same convention as
    create_gemini_audit_entry/create_claude_audit_entry: it swallows its
    own failures and never signals them back), so a downstream store outage
    is invisible here by design, exactly like those two functions. This
    function's own try/except only guards the selection logic above (env
    var parsing, the random() call) -- it is not a second layer of DB-
    failure detection.
    """
    try:
        if not output_text:
            return False
        if not is_sampling_enabled():
            return False
        if random.random() >= sampling_rate():
            return False
        from database import create_ai_output_boundary_sample
        create_ai_output_boundary_sample(
            feature=feature,
            output_text=output_text,
            model_version=model_version,
        )
        return True
    except Exception:
        return False
