"""
Gemini Flash base service (ST-12/ST-07/ST-08, EPIC-03, v4.0)

Provides generate_setup_thesis() using gemini-1.5-flash.
Returns gracefully when GEMINI_API_KEY is absent or the call fails.

ST-07: Audit trail — each call writes a row to gemini_audit_log (fire-and-forget).
ST-08: Cost tracking — token usage logged; estimated_cost_usd computed at
       $0.075/1M input tokens and $0.30/1M output tokens (Gemini 1.5 Flash free-tier rates).
       Monthly free-tier limit: 1,500 RPD / 1M tokens/month. Alert threshold: 800,000 tokens/month.
"""
import os
import hashlib
import json
from typing import Optional

GEMINI_COST_PER_INPUT_TOKEN = 0.10 / 1_000_000
GEMINI_COST_PER_OUTPUT_TOKEN = 0.40 / 1_000_000
GEMINI_MONTHLY_FREE_TIER_TOKEN_LIMIT = 1_000_000
GEMINI_ALERT_THRESHOLD = 800_000

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_VERSION = "gemini-2.0-flash"
PROMPT_VERSION = "v1.0"

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
    Generate a setup thesis using Gemini Flash.

    Returns:
        {
            "thesis": str,
            "model_version": str,
            "prompt_version": str,
            "input_hash": str,
            "output_hash": str,
            "available": bool,
        }

    When GEMINI_API_KEY is absent or the call fails, returns
    {"available": False, "error": str} so callers can degrade gracefully.
    """
    if not GEMINI_API_KEY:
        return {"available": False, "error": "GEMINI_API_KEY not configured"}

    try:
        import google.generativeai as genai
    except ImportError:
        return {"available": False, "error": "google-generativeai package not installed"}

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
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(MODEL_VERSION)
        response = model.generate_content(prompt)
        thesis = response.text.strip()
    except Exception as exc:
        return {"available": False, "error": f"Gemini API error: {str(exc)[:120]}"}

    output_hash = hashlib.sha256(thesis.encode()).hexdigest()[:16]

    prompt_tokens = None
    completion_tokens = None
    total_tokens = None
    estimated_cost_usd = None
    try:
        usage = getattr(response, "usage_metadata", None)
        if usage:
            prompt_tokens = getattr(usage, "prompt_token_count", None)
            completion_tokens = getattr(usage, "candidates_token_count", None)
            if prompt_tokens is not None and completion_tokens is not None:
                total_tokens = prompt_tokens + completion_tokens
                estimated_cost_usd = round(
                    prompt_tokens * GEMINI_COST_PER_INPUT_TOKEN
                    + completion_tokens * GEMINI_COST_PER_OUTPUT_TOKEN,
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
