"""
AI Service

Provides journal summarisation via external LLM API (Anthropic).
AI output is display-only — must NOT be used in any signal, scoring,
or recommendation pipeline. SRB-v1.7 CONDITIONALLY COMPLIANT.

Contract: docs/specs/api_contracts/ai_endpoints.md v1.0
"""

import os
import anthropic
from typing import Optional


_DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def summarise_journal_notes(
    notes: list[str],
    model: Optional[str] = None,
) -> dict:
    """
    Call the Anthropic API to summarise a list of journal note strings.

    Returns a dict with keys: summary (str|None), model (str|None), message (str|None).
    On LLM unavailability, returns summary=None with an informational message — never raises.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = model or os.getenv("AI_MODEL", _DEFAULT_MODEL)

    if not api_key:
        return {
            "summary": None,
            "model": None,
            "message": "AI summarisation is currently unavailable. Please try again later.",
        }

    if not notes:
        return {
            "summary": None,
            "model": None,
            "message": "No journal notes found for the selected trades.",
        }

    combined = "\n\n".join(f"- {n}" for n in notes if n and n.strip())
    if not combined.strip():
        return {
            "summary": None,
            "model": None,
            "message": "No journal notes found for the selected trades.",
        }

    prompt = (
        "You are reviewing a trader's journal entries. "
        "Summarise the key themes, patterns, and observations across these notes in 2–4 concise paragraphs. "
        "Focus on trading behaviour, decision-making patterns, and recurring themes. "
        "Do not make investment recommendations.\n\n"
        f"Journal entries:\n{combined}"
    )

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        summary_text = response.content[0].text if response.content else None
        return {"summary": summary_text, "model": model, "message": None}
    except Exception:
        return {
            "summary": None,
            "model": None,
            "message": "AI summarisation is currently unavailable. Please try again later.",
        }
