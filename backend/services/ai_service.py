"""
AI Service

Provides journal summarisation, daily briefing, and chat advisory via Anthropic.
AI output is display-only — must NOT be used in any signal, scoring,
or recommendation pipeline. SRB-v1.7 CONDITIONALLY COMPLIANT.

Contract: docs/specs/api_contracts/ai_endpoints.md v1.31

Post-generation stop-time check (ST-04, BLG-AI-10, v9.12; AI Compliance &
Governance Officer ruling, ESC-EXEC-20261013-01): when a briefing or chat
response cites a position's stop without its recalculation time, code
appends "(<TICKER> <_stop_recalculated_label()>)" after the model's text in
that field. This is a deterministic, code-authored addition built only from
the context the model was given: model text is never edited, reordered or
removed, and the boundary-sample hook receives the raw model output.
Every miss is logged and counted in claude_audit_log.compliance_check_result.

Summary ticker check (ST-17, BLG-AI-16, v9.13; ruling ESC-EXEC-20261027-02):
a ticker named in the briefing summary that is outside the context gets a
code-written caveat appended the same way, logged and counted.
"""

import hashlib
import logging
import os
import json
import re
import time
import anthropic
from datetime import datetime
from typing import Optional

from fastapi import HTTPException

from strategy_parameters import GRACE_PERIOD_DAYS
from utils.calculations import live_holding_days
from utils.ai_sampling import sample_ai_output
from ai_models import CLAUDE_HAIKU_4_5, CLAUDE_SONNET_4_6
from utils.upstream_call import anthropic_retryable_exceptions, bounded_upstream_call, get_timeout

logger = logging.getLogger(__name__)

# ST-13 (BLG-BE-122, EPIC-03, v9.6): this module's 3 Anthropic call sites
# (summarise_journal_notes, generate_daily_briefing, ai_chat) previously
# each made a single, unretried anthropic.Anthropic().messages.create()
# call with no explicit timeout (SDK default). _create_message() below
# centralises the fix -- same retry budget and exception set already
# proven safe in services/gemini_service.py and services/debrief_service.py
# (BLG-BE-89, v8.7), reused here via utils.upstream_call rather than
# re-derived a third time.
_RETRYABLE_ANTHROPIC_EXCEPTIONS = anthropic_retryable_exceptions()


@bounded_upstream_call("anthropic", retryable_exceptions=_RETRYABLE_ANTHROPIC_EXCEPTIONS)
def _create_message(api_key: str, **create_kwargs):
    """Shared, retried Anthropic messages.create() call. Each call site's
    own existing broad try/except still wraps this and returns its
    graceful-degradation response once retries are exhausted -- unchanged
    behaviour there; this only adds bounded retry + an explicit timeout
    underneath it."""
    client = anthropic.Anthropic(api_key=api_key, timeout=get_timeout("anthropic"))
    return client.messages.create(**create_kwargs)


MODEL_VERSION = CLAUDE_HAIKU_4_5
MODEL_BRIEFING = CLAUDE_SONNET_4_6

# Prompt template versions, logged to claude_audit_log and pinned by
# tests/fixtures/ai_prompt_template_golden_fixtures.json. Bump the matching
# constant whenever that system_prompt's text changes.
# Briefing v1.1 (ST-07, BLG-AI-09, v9.11): states advisory-only / no
# execution and frames actions as recommendations.
# Briefing v1.2 / chat v1.1 (ST-08, BLG-BE-141, v9.11): each quoted stop
# carries its recalculation time, and the model is told to state it.
# Briefing v1.3 (ST-02 + ST-03, BLG-AI-11/12, v9.12, one combined bump):
# actions may name only tickers from the snapshot; the context labels
# available cash and starting capital separately.
# Chat v1.2 (ST-19, BLG-AI-14, v9.13): the chat context labels cash the same way.
BRIEFING_PROMPT_VERSION = "v1.3"
CHAT_PROMPT_VERSION = "v1.2"
# Journal summary v1.0 (ST-06, BLG-OPS-183, v9.12): first recorded version of
# the existing, unchanged prompt, now that its calls are logged to
# claude_audit_log.
# Journal summary v1.1 (ST-18, BLG-AI-15, v9.13): the prompt says not to
# suggest changing stops, position sizing or setups.
JOURNAL_SUMMARY_PROMPT_VERSION = "v1.1"
# Haiku 4.5 list pricing, the same rates as gemini_service.CLAUDE_COST_PER_*_TOKEN.
_HAIKU_COST_PER_INPUT_TOKEN = 1.00 / 1_000_000
_HAIKU_COST_PER_OUTPUT_TOKEN = 5.00 / 1_000_000

# BLG-SEC-01: context_opts.ticker is interpolated into the ai_chat() system prompt.
# Reject anything outside this charset (in particular \n / \r, which could otherwise
# forge additional system-prompt lines) before it reaches the prompt.
_CONTEXT_TICKER_PATTERN = re.compile(r'[A-Z0-9.:/-]{1,20}')


def _prompt_hash(system_prompt: str, user_message: str) -> str:
    """ST-06 (BLG-AI-08, v9.11): SHA-256 of the system prompt plus the user
    message, first 16 hex characters. Non-reversible, the same form as
    gemini_audit_log.input_hash (claude_api_log_hygiene_policy.md §3.2)."""
    return hashlib.sha256(f"{system_prompt}\n{user_message}".encode()).hexdigest()[:16]


def _audit_failed_model_call(create_claude_audit_entry, endpoint: str, prompt_version: str,
                             prompt_hash: str, t0: float) -> None:
    """ST-06 (BLG-AI-08, v9.11): a model call that fails after retries still
    writes an audit row, marked compliance_check_result='model_call_failed'.
    Never raises: the endpoint's own fallback path continues."""
    try:
        create_claude_audit_entry(
            endpoint=endpoint,
            model_id=MODEL_BRIEFING,
            prompt_version=prompt_version,
            compliance_check_result="model_call_failed",
            latency_ms=int((time.time() - t0) * 1000),
            prompt_hash=prompt_hash,
        )
    except Exception:
        logger.warning("failed-call audit row not written for %s", endpoint, exc_info=True)


def _stop_recalculated_label(position: dict) -> str:
    """ST-08 (BLG-BE-141, v9.11): when the quoted stop was last recalculated
    (`positions.stop_calculated_at`, DS-22). NULL means the stop has not
    been recalculated since entry (for example, during the grace period)."""
    ts = position.get("stop_calculated_at")
    if not ts:
        return "stop not recalculated since entry"
    if isinstance(ts, str):
        try:
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            return f"stop last recalculated {ts}"
    return f"stop last recalculated {ts.strftime('%Y-%m-%d %H:%M')} UTC"



def _normalise_ticker(ticker) -> Optional[str]:
    """ST-15 (BLG-AI-17, v9.13): upper case with a trailing ".L" removed, so a
    UK ticker matches with or without its suffix (as the trade-plan lookup in
    database.py already does). None for a non-string or empty ticker."""
    if not isinstance(ticker, str):
        return None
    t = ticker.strip().upper()
    if t.endswith(".L"):
        t = t[:-2]
    return t or None


def _filter_actions_to_context(actions, allowed_tickers: set) -> list:
    """ST-02 (BLG-AI-11, v9.12): keep only briefing actions whose ticker is a
    held position or one of the signals given to the model. The model once
    returned ENTER for the placeholder ticker NEW_SIGNAL. Dropped actions are
    logged (ticker and type only). Both sides are normalised (ST-15), so
    `VOD` matches a held `VOD.L` and the reverse."""
    if not isinstance(actions, list):
        return []
    allowed = {_normalise_ticker(t) for t in allowed_tickers} - {None}
    kept = []
    for action in actions:
        ticker = action.get("ticker") if isinstance(action, dict) else None
        if _normalise_ticker(ticker) in allowed:
            kept.append(action)
        else:
            logger.warning(
                "daily briefing: dropped action naming a ticker outside the context "
                "(type=%s, ticker=%r, prompt_version=%s)",
                action.get("type") if isinstance(action, dict) else None,
                ticker, BRIEFING_PROMPT_VERSION,
            )
    return kept


def _briefing_cash_line(portfolio: dict, position_count: int) -> str:
    """ST-03 (BLG-AI-12, v9.12): "cash £X of £Y" read as a target cash level
    (on staging, "£15,006 against a £0 target"). Label each figure, and omit
    starting capital when it is 0 or missing."""
    line = f"Portfolio: {position_count} open positions, available cash £{portfolio.get('cash', 0) or 0:,.0f}"
    initial_cash = portfolio.get("initial_cash") or 0
    if initial_cash > 0:
        line += f"; starting capital £{initial_cash:,.0f}"
    return line


# ─── ST-04 (BLG-AI-10, v9.12): post-generation stop-time check ─────────────
_STOP_WORD_RE = re.compile(r"\bstops?\b", re.IGNORECASE)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n")
_NOT_RECALCULATED_RE = re.compile(r"not recalculated since entry", re.IGNORECASE)


def _stop_time_date(position: dict) -> Optional[str]:
    """`stop_calculated_at` as YYYY-MM-DD, or None when it is NULL/unparseable."""
    ts = position.get("stop_calculated_at")
    if not ts:
        return None
    if isinstance(ts, str):
        try:
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            return None
    return ts.strftime("%Y-%m-%d")


def _ticker_in(ticker: str, sentence: str) -> bool:
    """Whole-word match of the ticker's normalised form, with or without a
    ".L" suffix (ST-15): a held `VOD.L` is cited by "VOD" and the reverse."""
    bare = _normalise_ticker(ticker)
    if not bare:
        return False
    return re.search(rf"(?<![A-Za-z0-9.]){re.escape(bare)}(?:\.L)?(?![A-Za-z0-9])", sentence) is not None


def _stop_time_present(text: str, position: dict) -> bool:
    date = _stop_time_date(position)
    if date:
        return date in text
    raw = position.get("stop_calculated_at")
    if isinstance(raw, str) and raw:
        # Unparseable timestamp: the label quotes it raw, so look for it raw.
        return raw in text
    return _NOT_RECALCULATED_RE.search(text) is not None


def _append_missing_stop_times(text, positions: list, endpoint: str, field: str,
                               prompt_version: str, own_ticker: Optional[str] = None,
                               focus_ticker: Optional[str] = None):
    """Return (text, outcome) for one response field. outcome is None (no
    miss), "appended" or "unattributed". Per the ESC-EXEC-20261013-01 ruling:
    a sentence containing the word "stop" or "stops" cites a stop; it is attributed to every
    open-position ticker it names (whole word), plus `own_ticker` for an
    action. Tickers are compared in normalised form (ST-15: upper case, ".L"
    folded). For chat, `focus_ticker` (context.ticker) takes a stop sentence
    that names no held ticker, if it is itself held (ST-16, BLG-AI-18; ruling
    ESC-EXEC-20261027-01 (B)); a sentence naming a held ticker is attributed
    only to the tickers it names. A cited position whose stop_calculated_at date (or "not
    recalculated since entry", when NULL) appears nowhere in the field gets
    its label appended after the model's text. Fails open."""
    if not isinstance(text, str) or not text:
        return text, None
    try:
        by_ticker, by_normalised = {}, {}
        for p in positions or []:
            t = p.get("ticker")
            n = _normalise_ticker(t)
            if n and n not in by_normalised:
                by_ticker[t] = p
                by_normalised[n] = t
        own = by_normalised.get(_normalise_ticker(own_ticker))
        focus = by_normalised.get(_normalise_ticker(focus_ticker))
        missing, via_focus, unattributed = [], set(), False
        for sentence in _SENTENCE_SPLIT_RE.split(text):
            if not _STOP_WORD_RE.search(sentence):
                continue
            cited = [t for t in by_ticker if _ticker_in(t, sentence)]
            if own and own not in cited:
                cited.append(own)
            if not cited and focus:
                cited.append(focus)
                if focus not in missing and not _stop_time_present(text, by_ticker[focus]):
                    via_focus.add(focus)
            if not cited:
                unattributed = True
            for t in cited:
                if t not in missing and not _stop_time_present(text, by_ticker[t]):
                    missing.append(t)
        for t in missing:
            logger.warning("stop-time check: endpoint=%s field=%s ticker=%s action=appended prompt_version=%s%s",
                           endpoint, field, t, prompt_version, " attribution=focus" if t in via_focus else "")
        if unattributed:
            logger.warning("stop-time check: endpoint=%s field=%s ticker=unattributed action=unattributed_no_append "
                           "prompt_version=%s", endpoint, field, prompt_version)
        if missing:
            notes = " ".join(f"({t} {_stop_recalculated_label(by_ticker[t])})" for t in missing)
            return f"{text} {notes}", "appended"
        return text, "unattributed" if unattributed else None
    except Exception:
        logger.error("stop-time check failed for %s %s; response returned unchanged", endpoint, field, exc_info=True)
        return text, "error"


def _stop_time_check_result(outcomes) -> str:
    """claude_audit_log.compliance_check_result for one briefing/chat call."""
    outcomes = set(outcomes)
    if "appended" in outcomes:
        return "stop_time_missing_appended"
    if "unattributed" in outcomes:
        return "stop_time_missing_unattributed"
    if "error" in outcomes:
        return "stop_time_check_error"
    return "pass"


def _check_briefing_stop_times(parsed: dict, positions: list):
    """Apply the stop-time check to the briefing summary and each action
    description. Returns (summary, actions, compliance_check_result)."""
    endpoint = "POST /ai/daily-briefing"
    summary, outcome = _append_missing_stop_times(parsed.get("summary", ""), positions, endpoint,
                                                  "summary", BRIEFING_PROMPT_VERSION)
    outcomes = [outcome]
    actions = []
    for i, action in enumerate(parsed.get("actions", []) or []):
        if isinstance(action, dict) and isinstance(action.get("description"), str):
            desc, outcome = _append_missing_stop_times(
                action["description"], positions, endpoint, f"actions[{i}].description",
                BRIEFING_PROMPT_VERSION, own_ticker=action.get("ticker"))
            outcomes.append(outcome)
            if desc != action["description"]:
                action = {**action, "description": desc}
        actions.append(action)
    return summary, actions, _stop_time_check_result(outcomes)


# ─── ST-17 (BLG-AI-16, v9.13): briefing summary tickers outside the context ─
# AI Compliance & Governance Officer ruling ESC-EXEC-20261027-02 (B): a
# ticker-like token in the raw summary that is not an open position or a
# context signal (ST-15 normalised), does not appear in the context sent to
# the model, and is not a known non-ticker word gets a code-written caveat
# appended after the model's text (and after any stop-time notes). Logged and
# counted; model text is never edited; fails open.
_TICKER_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_.&$£])[A-Z][A-Z0-9_]{1,14}(?:\.[A-Z]{1,2})?(?![A-Za-z0-9_&])")
_NON_TICKER_WORDS = frozenset({
    "UK", "US", "USD", "GBP", "GBX", "EXIT", "ENTER", "MONITOR", "HOLD", "ATR", "MA", "ETF", "AI", "UTC",
    "SPY", "FTSE", "RISK", "ON", "OFF", "STOP", "BREACH", "OK", "YTD",
})


def _word_in(token: str, text: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_.]){re.escape(token)}(?![A-Za-z0-9_])", text) is not None


def _summary_ticker_caveat(summary, context_tickers, context: str):
    """Return (caveat, outcome) for the raw briefing summary. caveat is the
    text to append (or None); outcome is None (no hit), "appended" or "error"."""
    if not isinstance(summary, str) or not summary:
        return None, None
    try:
        known = {_normalise_ticker(t) for t in context_tickers} - {None}
        unknown = []
        for m in _TICKER_TOKEN_RE.finditer(summary):
            token = m.group(0)
            if (token in unknown or token in _NON_TICKER_WORDS or _normalise_ticker(token) in known
                    or _word_in(token, context)):
                continue
            unknown.append(token)
        if not unknown:
            return None, None
        for token in unknown:
            logger.warning("ticker check: endpoint=POST /ai/daily-briefing field=summary ticker=%s "
                           "action=caveat_appended prompt_version=%s", token, BRIEFING_PROMPT_VERSION)
        if len(unknown) == 1:
            return f"(Note: {unknown[0]} is not one of your open positions or today's top signals.)", "appended"
        return f"(Note: {', '.join(unknown)} are not among your open positions or today's top signals.)", "appended"
    except Exception:
        logger.error("ticker check failed for the briefing summary; summary returned unchanged", exc_info=True)
        return None, "error"


def _with_ticker_result(stop_time_result: str, outcome: Optional[str]) -> str:
    """Combine the stop-time result with the ST-17 ticker result (ruling condition 5)."""
    if outcome == "appended":
        if stop_time_result == "pass":
            return "ticker_outside_context_appended"
        return f"{stop_time_result}+ticker_outside_context_appended"
    if outcome == "error":
        return f"{stop_time_result}+ticker_check_error"
    return stop_time_result


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


def _audit_journal_summary_call(create_claude_audit_entry, model: str, prompt_hash: str, t0: float,
                                usage=None, response_text: Optional[str] = None,
                                compliance_check_result: Optional[str] = None) -> None:
    """One claude_audit_log row per journal-summary model call (ST-06). Never raises."""
    try:
        input_tokens = getattr(usage, "input_tokens", None) if usage else None
        output_tokens = getattr(usage, "output_tokens", None) if usage else None
        cost_usd = None
        if input_tokens is not None and output_tokens is not None:
            cost_usd = round(input_tokens * _HAIKU_COST_PER_INPUT_TOKEN
                             + output_tokens * _HAIKU_COST_PER_OUTPUT_TOKEN, 8)
        create_claude_audit_entry(
            endpoint="POST /ai/journal-summary",
            model_id=model,
            prompt_version=JOURNAL_SUMMARY_PROMPT_VERSION,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd,
            latency_ms=int((time.time() - t0) * 1000),
            prompt_hash=prompt_hash,
            response_length=len(response_text) if response_text else (None if compliance_check_result else 0),
            compliance_check_result=compliance_check_result,
        )
    except Exception:
        logger.warning("journal-summary audit row not written", exc_info=True)


# ─── ST-18 (BLG-AI-15, v9.13): journal-summary output-language check ───────
# AI Compliance & Governance Officer ruling ESC-EXEC-20261027-03 (A): a
# summary fails on the debrief's prescriptive scan or on wording that
# suggests changing stops, sizing or setups (subject, then a present-tense or
# modal word, then a change verb, within one sentence; past tense such as
# "needed" is descriptive and passes). Regenerate once, then return the
# code-written fallback, as the debrief and monthly narrative do.
_TRADING_CHANGE_RE = re.compile(
    r"\b(?:stop[- ]loss(?:es)?|stop (?:placement|level|distance)s?|stops?"
    r"|position siz(?:e|es|ing)|sizing|setups?)\b"
    r"[^.!?\n]{0,40}?\b(?:needs?|should|ought|requires?|warrants?|may need|might need|could use)\b"
    r"[^.!?\n]{0,25}?\b(?:adjust|chang|tighten|widen|loosen|revis|revisit|reconsider|rethink|review"
    r"|modif|refin|mov|reduc|increas|cut|lower|rais)\w*",
    re.IGNORECASE,
)
JOURNAL_SUMMARY_WITHHELD_MESSAGE = (
    "The AI summary was withheld because it did not pass the advisory-language check. "
    "Your journal notes are unchanged; please try again later."
)


def journal_summary_language_failures(text: Optional[str]) -> list:
    """The failed categories for one summary ([] means it passes)."""
    from services.debrief_service import scan_prescriptive
    if not text:
        return []
    found = []
    if scan_prescriptive(text):
        found.append("prescriptive")
    if _TRADING_CHANGE_RE.search(text):
        found.append("trading_change")
    return found


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
        "Do not make investment recommendations. "
        "Describe what the notes record; do not suggest changing stops, position sizing or setups.\n\n"
        f"Journal entries:\n{combined}"
    )

    # ST-06 (BLG-OPS-183, v9.12): the journal summary wrote no claude_audit_log
    # row, so its spend was invisible to the daily cost alert, the monthly
    # cost views and the endpoint anomaly check. Each call now writes one,
    # including a failed call (no cost). The audit write never fails the summary.
    from database import create_claude_audit_entry
    prompt_hash = _prompt_hash("", prompt)
    try:
        # ST-18: one audit row per model call, carrying that attempt's result.
        for attempt in (1, 2):
            t0 = time.time()
            try:
                response = _create_message(
                    api_key,
                    model=model,
                    max_tokens=512,
                    messages=[{"role": "user", "content": prompt}],
                )
            except Exception:
                _audit_journal_summary_call(create_claude_audit_entry, model, prompt_hash, t0,
                                            compliance_check_result="model_call_failed")
                raise
            summary_text = response.content[0].text if response.content else None
            if summary_text:
                sample_ai_output("journal-summary (POST /ai/journal-summary)", summary_text, model)
            failures = journal_summary_language_failures(summary_text)
            if not failures:
                _audit_journal_summary_call(create_claude_audit_entry, model, prompt_hash, t0,
                                            usage=response.usage, response_text=summary_text,
                                            compliance_check_result="pass" if attempt == 1 else "pass_on_regenerate")
                return {"summary": summary_text, "model": model, "message": None}
            outcome = "fail_regenerate:" if attempt == 1 else "fail_fallback:"
            _audit_journal_summary_call(create_claude_audit_entry, model, prompt_hash, t0,
                                        usage=response.usage, response_text=summary_text,
                                        compliance_check_result=outcome + "+".join(failures))
            logger.warning("journal summary failed the language check (attempt %d, categories=%s, prompt_version=%s)",
                           attempt, "+".join(failures), JOURNAL_SUMMARY_PROMPT_VERSION)
        return {"summary": None, "model": None, "message": JOURNAL_SUMMARY_WITHHELD_MESSAGE}
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
    Assembles portfolio context and calls the briefing model (MODEL_BRIEFING) to produce a
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
            _regime_context_line("SPY", regime["spy_price"], regime["spy_ma200"], regime["spy_risk_on"]),
            _regime_context_line("FTSE", regime["ftse_price"], regime["ftse_ma200"], regime["ftse_risk_on"]),
        ]
    else:
        regime_lines = ["Market regime: Unknown (data unavailable)"]

    context_lines = [
        f"Today: {now.strftime('%Y-%m-%d')}",
        *regime_lines,
        f"Month-end rebalance due today: {'Yes' if is_month_end else 'No'}",
        "",
        _briefing_cash_line(portfolio, len(positions)),
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
            # ST-12 (BLG-BE-153, v9.11): live calendar days, not the stored column.
            holding_days = live_holding_days(p)
            risk_off = bool(p.get("risk_off_exit", False))
            grace = holding_days > 0 and holding_days < GRACE_PERIOD_DAYS
            grace_days_left = max(0, GRACE_PERIOD_DAYS - holding_days) if grace else None
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
                f"  - {ticker} ({market}): price £{price:.2f}, trailing stop £{stop:.2f}"
                f" ({_stop_recalculated_label(p)}),"
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
        "Your output is advisory only: you cannot execute trades, and nothing you write is acted on automatically. "
        "The user reviews your briefing and makes every trading decision. "
        "You receive a daily portfolio snapshot and must produce: "
        "(1) a plain-English summary (2-4 sentences) of the key portfolio state, "
        "(2) an ordered list of recommended actions in JSON, each one a recommendation for the user to decide on, never an instruction. "
        "Action types: EXIT for stop breach or risk-off regime, ENTER for strong new signals, "
        "MONITOR for near-stop positions, HOLD for stable positions. "
        "Every action must name a ticker exactly as it appears in the snapshot's open positions or signals; "
        "never invent a ticker or use a placeholder. "
        "Whenever you mention a position's stop or a stop breach, state when that stop was last "
        "recalculated, using the time given for that position in the snapshot. "
        "Respond with JSON only, no markdown fences, in this exact shape: "
        '{"summary": "...", "actions": [{"type": "EXIT|ENTER|MONITOR|HOLD", "ticker": "...", "description": "..."}]}'
    )

    prompt_hash = _prompt_hash(system_prompt, context)
    try:
        t0 = time.time()
        try:
            response = _create_message(
                api_key,
                model=MODEL_BRIEFING,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": context}],
            )
        except Exception:
            _audit_failed_model_call(create_claude_audit_entry, "POST /ai/daily-briefing", BRIEFING_PROMPT_VERSION, prompt_hash, t0)
            raise
        # ST-13 (BLG-BE-128, v9.7): includes retry backoff sleep time by design -- see ai_endpoints.md Implementation constraints
        elapsed_ms = int((time.time() - t0) * 1000)

        content = response.content[0].text if response.content else "{}"
        usage = response.usage
        input_tokens = usage.input_tokens if usage else None
        output_tokens = usage.output_tokens if usage else None

        # Parsed before the audit write so the row carries the stop-time
        # result; an unparseable response still gets its audit row and then
        # takes the fallback path below, as before.
        try:
            parsed = json.loads(content)
        except ValueError:
            parsed = None
        stop_time_result = None
        if isinstance(parsed, dict):
            actions = parsed.get("actions", [])
            try:
                allowed_tickers = {str(t).strip().upper() for t in
                                   [p.get("ticker") for p in positions] + [s.get("ticker") for s in top_signals] if t}
                actions = _filter_actions_to_context(actions, allowed_tickers)
            except Exception:
                # Fail open, as the stop-time check does: never turn a valid
                # briefing into the fallback or skip its audit row.
                logger.error("daily briefing ticker filter failed; actions returned unfiltered", exc_info=True)
            summary, actions, stop_time_result = _check_briefing_stop_times(
                {"summary": parsed.get("summary", ""), "actions": actions}, positions)
            caveat, ticker_outcome = _summary_ticker_caveat(
                parsed.get("summary", ""),
                [p.get("ticker") for p in positions] + [s.get("ticker") for s in top_signals], context)
            if caveat:
                summary = f"{summary} {caveat}"
            stop_time_result = _with_ticker_result(stop_time_result, ticker_outcome)

        try:
            cost_usd = None
            if input_tokens and output_tokens:
                cost_usd = (input_tokens * 3.0 + output_tokens * 15.0) / 1_000_000
            create_claude_audit_entry(
                endpoint="POST /ai/daily-briefing",
                model_id=MODEL_BRIEFING,
                prompt_version=BRIEFING_PROMPT_VERSION,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd,
                latency_ms=elapsed_ms,
                prompt_hash=prompt_hash,
                response_length=len(content) if content else 0,
                compliance_check_result=stop_time_result,
            )
        except Exception:
            pass

        if not isinstance(parsed, dict):
            raise ValueError("daily briefing response is not a JSON object")

        # Raw model output, before any code-written addition (ST-04 Condition 2).
        if content and content != "{}":
            sample_ai_output("daily-briefing (POST /ai/daily-briefing)", content, MODEL_BRIEFING)
        return {
            "summary": summary,
            "actions": actions,
            "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "advisory": True,
            "model": MODEL_BRIEFING,
        }
    except Exception:
        # ST-03 (BLG-BE-151, v9.11): log the cause before returning the
        # fallback, so a failure is no longer hidden behind the generic text.
        logger.error("generate_daily_briefing failed; returning fallback message", exc_info=True)
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


def _regime_context_line(name: str, price, ma200, risk_on) -> str:
    if risk_on is None:
        return f"  {name}: Unknown (index data unavailable)"
    return f"  {name}: {price:.2f} vs MA200 {ma200:.2f} → {'Risk-On' if risk_on else 'Risk-Off'}"


def _get_regime_data() -> Optional[dict]:
    try:
        from utils.pricing import check_market_regime
        r = check_market_regime()
        spy_on = r.get("spy_risk_on")
        ftse_on = r.get("ftse_risk_on")
        if spy_on is None or ftse_on is None:
            unknown = [n for n, v in (("SPY", spy_on), ("FTSE", ftse_on)) if v is None]
            label = f"Unknown ({' and '.join(unknown)} index data unavailable)"
        elif spy_on and ftse_on:
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
        # ST-19 (BLG-AI-14, v9.13): "Cash: £X of £Y initial capital" read as
        # a target cash level, as it did in the briefing; same labelling now.
        _briefing_cash_line(portfolio, len(positions)),
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
                f"  {ticker} ({market}): price £{price:.2f}, stop £{stop:.2f} "
                f"({_stop_recalculated_label(p)}), "
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
        "Whenever you mention a position's stop or a stop breach, state when that stop was last "
        "recalculated, using the time given for that position in the snapshot. "
        "Keep responses to 2-4 sentences unless more detail is genuinely needed.\n\n"
        f"Portfolio context:\n{portfolio_context}"
    )

    prompt_hash = _prompt_hash(system_prompt, question)
    try:
        t0 = time.time()
        try:
            response = _create_message(
                api_key,
                model=MODEL_BRIEFING,
                max_tokens=512,
                system=system_prompt,
                messages=[{"role": "user", "content": question}],
            )
        except Exception:
            _audit_failed_model_call(create_claude_audit_entry, "POST /ai/chat", CHAT_PROMPT_VERSION, prompt_hash, t0)
            raise
        # ST-13 (BLG-BE-128, v9.7): includes retry backoff sleep time by design -- see ai_endpoints.md Implementation constraints
        elapsed_ms = int((time.time() - t0) * 1000)

        content = response.content[0].text if response.content else "I was unable to generate a response."
        usage = response.usage
        input_tokens = usage.input_tokens if usage else None
        output_tokens = usage.output_tokens if usage else None

        checked, outcome = _append_missing_stop_times(content, positions, "POST /ai/chat", "response",
                                                      CHAT_PROMPT_VERSION,
                                                      focus_ticker=(context_opts or {}).get("ticker"))

        answer_id = None
        try:
            cost_usd = None
            if input_tokens and output_tokens:
                cost_usd = (input_tokens * 3.0 + output_tokens * 15.0) / 1_000_000
            # ST-22 (BLG-FE-208, v9.13): the audit row's id is the answer_id a
            # rating attaches to.
            answer_id = create_claude_audit_entry(
                endpoint="POST /ai/chat",
                model_id=MODEL_BRIEFING,
                prompt_version=CHAT_PROMPT_VERSION,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd,
                latency_ms=elapsed_ms,
                prompt_hash=prompt_hash,
                response_length=len(content) if content else 0,
                compliance_check_result=_stop_time_check_result([outcome]),
            )
        except Exception:
            pass

        # Raw model output, before any code-written addition (ST-04 Condition 2).
        model_answered = bool(content) and content != "I was unable to generate a response."
        if model_answered:
            sample_ai_output("chat (POST /ai/chat)", content, MODEL_BRIEFING)
        result = {"response": checked, "advisory": True, "model": MODEL_BRIEFING}
        # Only a model answer with a stored audit row can be rated (fixed
        # messages carry no answer_id; decision record §2.1).
        if model_answered and isinstance(answer_id, str):
            result["answer_id"] = answer_id
        return result
    except Exception:
        # ST-03 (BLG-BE-151, v9.11): log the cause before returning the fallback.
        logger.error("ai_chat failed; returning fallback message", exc_info=True)
        return {"response": "Unable to get a response. Please try again.", "advisory": True}


# ---------------------------------------------------------------------------
# ST-22 — Chat answer rating (POST /ai/chat/{answer_id}/rating)
# ---------------------------------------------------------------------------

def rate_chat_answer(answer_id: str, rating: str) -> Optional[dict]:
    """Store a useful / not-useful rating for one chat answer, once.

    Returns None when the answer does not exist, else
    {"answer_id", "rating", "rated_at", "created"}; created is False when the
    answer was already rated (the stored rating is returned, not replaced).
    The rating is a usefulness measure only: it is not an input to any
    signal, score or recommendation (decision record §3)."""
    from database import create_chat_answer_rating
    return create_chat_answer_rating(answer_id, rating)

