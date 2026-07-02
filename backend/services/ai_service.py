"""
AI Service

Provides journal summarisation, daily briefing, and chat advisory via Anthropic.
AI output is display-only — must NOT be used in any signal, scoring,
or recommendation pipeline. SRB-v1.7 CONDITIONALLY COMPLIANT.

Contract: docs/specs/api_contracts/ai_endpoints.md v1.4
"""

import logging
import os
import json
import re
import time
import anthropic
from datetime import datetime
from typing import Optional

from fastapi import HTTPException

logger = logging.getLogger(__name__)


MODEL_VERSION = "claude-haiku-4-5-20251001"
MODEL_BRIEFING = "claude-sonnet-4-6"

# BLG-SEC-01: context_opts.ticker is interpolated into the ai_chat() system prompt.
# Reject anything outside this charset (in particular \n / \r, which could otherwise
# forge additional system-prompt lines) before it reaches the prompt.
_CONTEXT_TICKER_PATTERN = re.compile(r'[A-Z0-9.:/-]{1,20}')


def _validate_context_ticker(context_opts: Optional[dict]) -> None:
    """Validate context_opts['ticker'] before it is interpolated into the system prompt (BLG-SEC-01)."""
    if not context_opts:
        return
    ticker = context_opts.get("ticker")
    if ticker is None:
        return
    if not isinstance(ticker, str) or not _CONTEXT_TICKER_PATTERN.fullmatch(ticker):
        raise HTTPException(
            status_code=422,
            detail=(
                "context.ticker is invalid — must be 1-20 characters matching "
                "[A-Z0-9.:/-] with no newlines or other special characters"
            ),
        )


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
    model = model or MODEL_VERSION

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
    except Exception as exc:
        logger.error("summarise_journal_notes failed: %s", exc, exc_info=True)
        return {
            "summary": None,
            "model": None,
            "message": "AI summarisation is currently unavailable. Please try again later.",
        }


# ---------------------------------------------------------------------------
# ST-06 — Daily briefing (POST /ai/daily-briefing)
# ---------------------------------------------------------------------------

def generate_daily_briefing() -> dict:
    """
    Assembles portfolio context and calls claude-sonnet-4-6 to produce a
    plain-English daily briefing with ordered action list.
    Returns: { summary, actions, generated_at, advisory, model }
    Advisory-only — SRB-v1.7.
    """
    from database import get_portfolio, get_positions, get_signals, create_claude_audit_entry

    api_key = os.getenv("ANTHROPIC_API_KEY")
    now = datetime.utcnow()

    portfolio = get_portfolio()
    if not portfolio:
        return _briefing_error("Portfolio not found", now)

    portfolio_id = str(portfolio["id"])
    positions = get_positions(portfolio_id, status="open")
    all_signals = get_signals(portfolio_id)

    regime = _get_regime_data()

    try:
        from services.signal_service import _is_last_trading_day_of_month
        is_month_end = _is_last_trading_day_of_month(datetime.now())
    except Exception:
        is_month_end = False

    # Top-5 signals from the most recent signal date
    top_signals = []
    if all_signals:
        latest_date = max((s["signal_date"] for s in all_signals if s.get("signal_date")), default=None)
        if latest_date:
            top_signals = sorted(
                [s for s in all_signals if s.get("signal_date") == latest_date and s.get("status") == "new"],
                key=lambda s: s.get("rank", 99),
            )[:5]

    if regime:
        regime_lines = [
            f"Market regime: {regime['label']}",
            f"  SPY: {regime['spy_price']:.2f} vs MA200 {regime['spy_ma200']:.2f} → {'Risk-On' if regime['spy_risk_on'] else 'Risk-Off'}",
            f"  FTSE: {regime['ftse_price']:.2f} vs MA200 {regime['ftse_ma200']:.2f} → {'Risk-On' if regime['ftse_risk_on'] else 'Risk-Off'}",
        ]
    else:
        regime_lines = ["Market regime: Unknown (data unavailable)"]

    context_lines = [
        f"Today: {now.strftime('%Y-%m-%d')}",
        *regime_lines,
        f"Month-end rebalance due today: {'Yes' if is_month_end else 'No'}",
        "",
        f"Portfolio: {len(positions)} open positions, "
        f"cash £{portfolio.get('cash', 0):,.0f} of £{portfolio.get('initial_cash', 0):,.0f}",
        "",
    ]

    if positions:
        context_lines.append("Open positions:")
        for p in positions:
            ticker = p.get("ticker", "?")
            market = p.get("market", "?")
            price = p.get("current_price", 0) or 0
            stop = p.get("current_stop", 0) or 0
            pnl_pct = p.get("pnl_pct", 0) or 0
            holding_days = p.get("holding_days", 0) or 0
            risk_off = bool(p.get("risk_off_exit", False))
            grace = holding_days > 0 and holding_days < 10
            grace_days_left = max(0, 10 - holding_days) if grace else None
            breach = stop > 0 and price > 0 and price <= stop
            alerts = []
            if breach:
                if grace:
                    alerts.append(f"STOP BREACH (grace {grace_days_left}d remaining — do not force exit yet)")
                else:
                    alerts.append("STOP BREACH")
            if risk_off:
                alerts.append("RISK-OFF-EXIT-FLAGGED")
            alert_str = f" [{', '.join(alerts)}]" if alerts else ""
            context_lines.append(
                f"  - {ticker} ({market}): price £{price:.2f}, trailing stop £{stop:.2f},"
                f" P&L {pnl_pct:+.1f}%{alert_str}"
            )
    else:
        context_lines.append("No open positions.")

    context_lines.append("")
    if top_signals:
        context_lines.append("Top momentum signals today:")
        for s in top_signals:
            context_lines.append(
                f"  #{s.get('rank', '?')} {s.get('ticker', '?')} ({s.get('market', '?')}): "
                f"momentum {s.get('momentum_percent', 0):.1f}%"
            )
    else:
        context_lines.append("No new signals today.")

    context = "\n".join(context_lines)

    if not api_key:
        return _briefing_error("AI briefing unavailable — ANTHROPIC_API_KEY not configured", now)

    system_prompt = (
        "You are a trading assistant for a disciplined momentum strategy. "
        "You receive a daily portfolio snapshot and must produce: "
        "(1) a plain-English summary (2-4 sentences) of the key portfolio state, "
        "(2) an ordered action list in JSON. "
        "Action types: EXIT for stop breach or risk-off regime, ENTER for strong new signals, "
        "MONITOR for near-stop positions, HOLD for stable positions. "
        "Respond with JSON only, no markdown fences, in this exact shape: "
        '{"summary": "...", "actions": [{"type": "EXIT|ENTER|MONITOR|HOLD", "ticker": "...", "description": "..."}]}'
    )

    try:
        t0 = time.time()
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL_BRIEFING,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": context}],
        )
        elapsed_ms = int((time.time() - t0) * 1000)

        content = response.content[0].text if response.content else "{}"
        usage = response.usage
        input_tokens = usage.input_tokens if usage else None
        output_tokens = usage.output_tokens if usage else None

        try:
            cost_usd = None
            if input_tokens and output_tokens:
                cost_usd = (input_tokens * 3.0 + output_tokens * 15.0) / 1_000_000
            create_claude_audit_entry(
                endpoint="POST /ai/daily-briefing",
                model_id=MODEL_BRIEFING,
                prompt_version="v1.0",
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd,
            )
        except Exception:
            pass

        parsed = json.loads(content)
        return {
            "summary": parsed.get("summary", ""),
            "actions": parsed.get("actions", []),
            "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "advisory": True,
            "model": MODEL_BRIEFING,
        }
    except Exception:
        return _briefing_error("AI briefing temporarily unavailable. Please try again.", now)


def _briefing_error(message: str, now: datetime) -> dict:
    return {
        "summary": None,
        "actions": [],
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "advisory": True,
        "model": None,
        "error": message,
    }


def _get_regime_data() -> Optional[dict]:
    try:
        from utils.pricing import check_market_regime
        r = check_market_regime()
        spy_on = r.get("spy_risk_on", False)
        ftse_on = r.get("ftse_risk_on", False)
        if spy_on and ftse_on:
            label = "Risk-On (SPY and FTSE both above MA200)"
        elif not spy_on and not ftse_on:
            label = "Risk-Off (both markets below MA200)"
        else:
            label = f"Neutral ({'SPY on' if spy_on else 'SPY off'}, {'FTSE on' if ftse_on else 'FTSE off'})"
        return {
            "label": label,
            "spy_price": r.get("spy_price", 0),
            "spy_ma200": r.get("spy_ma200", 0),
            "spy_risk_on": spy_on,
            "ftse_price": r.get("ftse_price", 0),
            "ftse_ma200": r.get("ftse_ma200", 0),
            "ftse_risk_on": ftse_on,
        }
    except Exception:
        return None


# ---------------------------------------------------------------------------
# ST-08 — Conversational AI chat (POST /ai/chat)
# ---------------------------------------------------------------------------

def ai_chat(question: str, context_opts: Optional[dict] = None) -> dict:
    """
    Stateless per-request AI chat grounded in live portfolio and signal state.
    context_opts: optional { ticker, position_id }
    Returns: { response, advisory }
    Advisory-only — SRB-v1.7.
    """
    _validate_context_ticker(context_opts)

    from database import get_portfolio, get_positions, get_signals, create_claude_audit_entry

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "response": "AI Trade Advisor is currently unavailable — ANTHROPIC_API_KEY not configured.",
            "advisory": True,
        }

    portfolio = get_portfolio()
    if not portfolio:
        return {"response": "Unable to load portfolio data.", "advisory": True}

    portfolio_id = str(portfolio["id"])
    positions = get_positions(portfolio_id, status="open")
    signals = get_signals(portfolio_id)

    context_lines = [
        f"Portfolio snapshot — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        f"Cash: £{portfolio.get('cash', 0):,.0f} of £{portfolio.get('initial_cash', 0):,.0f} initial capital",
        f"Open positions: {len(positions)}",
        "",
    ]

    if positions:
        context_lines.append("Positions:")
        for p in positions:
            ticker = p.get("ticker", "?")
            market = p.get("market", "?")
            price = p.get("current_price", 0) or 0
            stop = p.get("current_stop", 0) or 0
            risk_off = bool(p.get("risk_off_exit", False))
            pnl = p.get("pnl", 0) or 0
            context_lines.append(
                f"  {ticker} ({market}): price £{price:.2f}, stop £{stop:.2f}, "
                f"P&L £{pnl:+.0f}, risk_off={risk_off}"
            )

    latest_date = None
    if signals:
        latest_date = max((s["signal_date"] for s in signals if s.get("signal_date")), default=None)
    if latest_date:
        top = sorted(
            [s for s in signals if s.get("signal_date") == latest_date],
            key=lambda s: s.get("rank", 99),
        )[:5]
        context_lines.append("\nTop momentum signals:")
        for s in top:
            context_lines.append(
                f"  #{s.get('rank', '?')} {s.get('ticker', '?')} ({s.get('market', '?')}): "
                f"momentum {s.get('momentum_percent', 0):.1f}%"
            )

    if context_opts and context_opts.get("ticker"):
        context_lines.append(f"\nUser asking about: {context_opts['ticker']}")

    portfolio_context = "\n".join(context_lines)

    system_prompt = (
        "You are an AI trade advisor for a disciplined momentum trading strategy. "
        "You have access to the user's live portfolio snapshot below. "
        "Answer the user's question concisely and accurately based on the data provided. "
        "Do not fabricate data. Your responses are advisory only — you cannot execute trades. "
        "Keep responses to 2-4 sentences unless more detail is genuinely needed.\n\n"
        f"Portfolio context:\n{portfolio_context}"
    )

    try:
        t0 = time.time()
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL_BRIEFING,
            max_tokens=512,
            system=system_prompt,
            messages=[{"role": "user", "content": question}],
        )
        elapsed_ms = int((time.time() - t0) * 1000)

        content = response.content[0].text if response.content else "I was unable to generate a response."
        usage = response.usage
        input_tokens = usage.input_tokens if usage else None
        output_tokens = usage.output_tokens if usage else None

        try:
            cost_usd = None
            if input_tokens and output_tokens:
                cost_usd = (input_tokens * 3.0 + output_tokens * 15.0) / 1_000_000
            create_claude_audit_entry(
                endpoint="POST /ai/chat",
                model_id=MODEL_BRIEFING,
                prompt_version="v1.0",
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd,
            )
        except Exception:
            pass

        return {"response": content, "advisory": True, "model": MODEL_BRIEFING}
    except Exception:
        return {"response": "Unable to get a response. Please try again.", "advisory": True}
