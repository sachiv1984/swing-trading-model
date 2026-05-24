"""
Gemini Flash base service (ST-12, EPIC-03, v4.0)

Provides generate_setup_thesis() using gemini-1.5-flash.
Returns gracefully when GEMINI_API_KEY is absent or the call fails.

Audit trail and cost tracking are implemented in ST-07 and ST-08.
"""
import os
import hashlib
import json
from typing import Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_VERSION = "gemini-1.5-flash"
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

    return {
        "thesis": thesis,
        "model_version": MODEL_VERSION,
        "prompt_version": PROMPT_VERSION,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "available": True,
    }
