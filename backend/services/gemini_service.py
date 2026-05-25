"""
AI thesis generation service (EPIC-03, v4.0)

Provides generate_setup_thesis() using Claude Haiku 4.5 via the Anthropic SDK.
Returns gracefully when ANTHROPIC_API_KEY is absent or the call fails.

ST-07: Audit trail — each call writes a row to gemini_audit_log (fire-and-forget).
ST-08: Cost tracking — token usage logged; estimated_cost_usd computed at
       $1.00/1M input tokens and $5.00/1M output tokens (Claude Haiku 4.5 rates).
"""
import os
import hashlib
import json
from typing import Optional

CLAUDE_COST_PER_INPUT_TOKEN = 1.00 / 1_000_000
CLAUDE_COST_PER_OUTPUT_TOKEN = 5.00 / 1_000_000
GEMINI_MONTHLY_FREE_TIER_TOKEN_LIMIT = 1_000_000
GEMINI_ALERT_THRESHOLD = 800_000

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL_VERSION = "claude-haiku-4-5"
PROMPT_VERSION = "v2.0"

_THESIS_PROMPT_TEMPLATE = """You are a systematic swing trader. Generate a concise setup thesis (2-3 sentences) for the following trade context.

Ticker: {ticker}
Market: {market}
Setup type: {setup_type}
Signal data: {signal_summary}
Additional context: {plan_summary}

Respond with ONLY the thesis text — no preamble, no labels, no markdown. Keep it under 100 words."""


def generate_setup_thesis(
    ticker: str,
    market: str = "US",
    setup_type: Optional[str] = None,
    signal_data: Optional[dict] = None,
    plan_data: Optional[dict] = None,
    plan_id: Optional[str] = None,
) -> dict:
    """
    Generate a setup thesis using Claude Haiku 4.5.

    Returns:
        {
            "thesis": str,
            "model_version": str,
            "prompt_version": str,
            "input_hash": str,
            "output_hash": str,
            "available": bool,
        }

    When ANTHROPIC_API_KEY is absent or the call fails, returns
    {"available": False, "error": str} so callers can degrade gracefully.
    """
    if not ANTHROPIC_API_KEY:
        return {"available": False, "error": "ANTHROPIC_API_KEY not configured"}

    try:
        import anthropic
    except ImportError:
        return {"available": False, "error": "anthropic package not installed"}

    signal_summary = "None"
    if signal_data:
        parts = []
        if signal_data.get("signal_type"):
            parts.append(f"type={signal_data['signal_type']}")
        if signal_data.get("atr_multiple") is not None:
            parts.append(f"ATR_multiple={signal_data['atr_multiple']}")
        if signal_data.get("r_target") is not None:
            parts.append(f"R_target={signal_data['r_target']}")
        signal_summary = ", ".join(parts) if parts else "provided"

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
        sort_keys=True, default=str
    )
    input_hash = hashlib.sha256(input_payload.encode()).hexdigest()[:16]

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=MODEL_VERSION,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        thesis = response.content[0].text.strip()
    except Exception as exc:
        return {"available": False, "error": f"Claude API error: {str(exc)[:120]}"}

    output_hash = hashlib.sha256(thesis.encode()).hexdigest()[:16]

    prompt_tokens = None
    completion_tokens = None
    total_tokens = None
    estimated_cost_usd = None
    try:
        usage = response.usage
        if usage:
            prompt_tokens = getattr(usage, "input_tokens", None)
            completion_tokens = getattr(usage, "output_tokens", None)
            if prompt_tokens is not None and completion_tokens is not None:
                total_tokens = prompt_tokens + completion_tokens
                estimated_cost_usd = round(
                    prompt_tokens * CLAUDE_COST_PER_INPUT_TOKEN
                    + completion_tokens * CLAUDE_COST_PER_OUTPUT_TOKEN,
                    8,
                )
    except Exception:
        pass

    try:
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

    return {
        "thesis": thesis,
        "model_version": MODEL_VERSION,
        "prompt_version": PROMPT_VERSION,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "available": True,
    }
