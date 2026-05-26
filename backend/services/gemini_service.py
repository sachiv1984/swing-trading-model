"""
AI thesis generation service (EPIC-03, v4.0)

Provides generate_setup_thesis() and generate_full_plan() using Claude Haiku 4.5.
Returns gracefully when ANTHROPIC_API_KEY is absent or the call fails.

ST-07: Audit trail — each call writes a row to gemini_audit_log (fire-and-forget).
ST-08: Cost tracking — token usage logged; estimated_cost_usd computed at
       $1.00/1M input tokens and $5.00/1M output tokens (Claude Haiku 4.5 rates).
"""
import os
import hashlib
import json
import re
from typing import Optional

CLAUDE_COST_PER_INPUT_TOKEN = 1.00 / 1_000_000
CLAUDE_COST_PER_OUTPUT_TOKEN = 5.00 / 1_000_000

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL_VERSION = "claude-haiku-4-5"
PROMPT_VERSION = "v3.0"

_FULL_PLAN_PROMPT = """You are a systematic swing trader. Given the trade context below, fill in all sections of a trade plan.

Ticker: {ticker}
Market: {market}
Setup type: {setup_type}
Signal data: {signal_summary}

Return ONLY a JSON object with exactly these keys (no markdown, no preamble):
{{
  "regime_context_at_entry": "1 sentence on current market regime — risk-on/off, trend, sector strength.",
  "setup_thesis": "2-3 sentence thesis explaining why this setup is valid now. Under 100 words.",
  "entry_rationale": "1-2 sentences on the specific reason to enter — what technical or fundamental condition makes this a candidate.",
  "confirmation_criteria": "1-2 sentences on what must be true at entry — price action, volume, regime.",
  "early_exit_conditions": "1-2 sentences on conditions that would invalidate the thesis before the stop is hit.",
  "r_target": <number between 1.5 and 4.0 based on setup quality, or null if unknown>
}}"""

_THESIS_PROMPT_TEMPLATE = """You are a systematic swing trader. Generate a concise setup thesis (2-3 sentences) for the following trade context.

Ticker: {ticker}
Market: {market}
Setup type: {setup_type}
Signal data: {signal_summary}
Additional context: {plan_summary}

Respond with ONLY the thesis text — no preamble, no labels, no markdown. Keep it under 100 words."""


def _build_signal_summary(signal_data: Optional[dict]) -> str:
    if not signal_data:
        return "None"
    parts = []
    if signal_data.get("signal_type"):
        parts.append(f"type={signal_data['signal_type']}")
    if signal_data.get("momentum_percent") is not None:
        parts.append(f"momentum={signal_data['momentum_percent']}%")
    if signal_data.get("atr_multiple") is not None:
        parts.append(f"ATR_multiple={signal_data['atr_multiple']}")
    if signal_data.get("r_target") is not None:
        parts.append(f"R_target={signal_data['r_target']}")
    if signal_data.get("price_vs_50d_ma") is not None:
        parts.append(f"vs_200MA={signal_data['price_vs_50d_ma']}%")
    if signal_data.get("regime") is not None:
        parts.append(f"regime={'on' if signal_data['regime'] else 'off'}")
    if signal_data.get("signal_score") is not None:
        parts.append(f"score={signal_data['signal_score']}")
    return ", ".join(parts) if parts else "provided"


def _call_claude(prompt: str, max_tokens: int = 256) -> tuple:
    """Returns (text, usage) or raises."""
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=MODEL_VERSION,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip(), response.usage


def _log_audit(plan_id, input_hash, output_hash, usage):
    try:
        prompt_tokens = getattr(usage, "input_tokens", None)
        completion_tokens = getattr(usage, "output_tokens", None)
        total_tokens = None
        estimated_cost_usd = None
        if prompt_tokens is not None and completion_tokens is not None:
            total_tokens = prompt_tokens + completion_tokens
            estimated_cost_usd = round(
                prompt_tokens * CLAUDE_COST_PER_INPUT_TOKEN
                + completion_tokens * CLAUDE_COST_PER_OUTPUT_TOKEN,
                8,
            )
        from database import create_gemini_audit_entry
        create_gemini_audit_entry(
            plan_id=plan_id,
            model_version=MODEL_VERSION,
            prompt_version=PROMPT_VERSION,
            input_hash=input_hash,
            output_hash=output_hash,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=estimated_cost_usd,
        )
    except Exception:
        pass


def generate_full_plan(
    ticker: str,
    market: str = "US",
    setup_type: Optional[str] = None,
    signal_data: Optional[dict] = None,
    plan_id: Optional[str] = None,
) -> dict:
    """
    Generate all plan fields in one call: setup_thesis, entry_rationale,
    confirmation_criteria, early_exit_conditions, r_target.

    Returns {"available": True, "fields": {...}} or {"available": False, "error": str}.
    """
    if not ANTHROPIC_API_KEY:
        return {"available": False, "error": "ANTHROPIC_API_KEY not configured"}

    try:
        import anthropic  # noqa: F401
    except ImportError:
        return {"available": False, "error": "anthropic package not installed"}

    signal_summary = _build_signal_summary(signal_data)

    prompt = _FULL_PLAN_PROMPT.format(
        ticker=ticker.upper(),
        market=market,
        setup_type=setup_type or "Not specified",
        signal_summary=signal_summary,
    )

    input_payload = json.dumps(
        {"ticker": ticker, "market": market, "setup_type": setup_type, "signal_data": signal_data},
        sort_keys=True, default=str,
    )
    input_hash = hashlib.sha256(input_payload.encode()).hexdigest()[:16]

    try:
        text, usage = _call_claude(prompt, max_tokens=1024)
    except Exception as exc:
        return {"available": False, "error": f"Claude API error: {str(exc)[:120]}"}

    output_hash = hashlib.sha256(text.encode()).hexdigest()[:16]

    try:
        # Strip markdown code fences if present
        clean = re.sub(r"```(?:json)?\s*|\s*```", "", text).strip()
        fields = json.loads(clean)
    except Exception:
        return {"available": False, "error": "Claude returned non-JSON response"}

    _log_audit(plan_id, input_hash, output_hash, usage)

    return {
        "available": True,
        "fields": fields,
        "model_version": MODEL_VERSION,
        "prompt_version": PROMPT_VERSION,
    }


def generate_setup_thesis(
    ticker: str,
    market: str = "US",
    setup_type: Optional[str] = None,
    signal_data: Optional[dict] = None,
    plan_data: Optional[dict] = None,
    plan_id: Optional[str] = None,
) -> dict:
    """Legacy single-field thesis generation. Kept for backward compatibility."""
    if not ANTHROPIC_API_KEY:
        return {"available": False, "error": "ANTHROPIC_API_KEY not configured"}

    try:
        import anthropic  # noqa: F401
    except ImportError:
        return {"available": False, "error": "anthropic package not installed"}

    signal_summary = _build_signal_summary(signal_data)

    plan_summary = "None"
    if plan_data:
        parts = []
        if plan_data.get("entry_rationale"):
            parts.append(plan_data["entry_rationale"][:80])
        if plan_data.get("confirmation_criteria"):
            parts.append(plan_data["confirmation_criteria"][:60])
        plan_summary = "; ".join(parts) if parts else "provided"

    prompt = _THESIS_PROMPT_TEMPLATE.format(
        ticker=ticker.upper(),
        market=market,
        setup_type=setup_type or "Not specified",
        signal_summary=signal_summary,
        plan_summary=plan_summary,
    )

    input_payload = json.dumps(
        {"ticker": ticker, "market": market, "setup_type": setup_type,
         "signal_data": signal_data, "plan_data": plan_data},
        sort_keys=True, default=str,
    )
    input_hash = hashlib.sha256(input_payload.encode()).hexdigest()[:16]

    try:
        thesis, usage = _call_claude(prompt, max_tokens=256)
    except Exception as exc:
        return {"available": False, "error": f"Claude API error: {str(exc)[:120]}"}

    output_hash = hashlib.sha256(thesis.encode()).hexdigest()[:16]
    _log_audit(plan_id, input_hash, output_hash, usage)

    return {
        "thesis": thesis,
        "model_version": MODEL_VERSION,
        "prompt_version": PROMPT_VERSION,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "available": True,
    }
