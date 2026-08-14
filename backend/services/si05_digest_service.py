"""
SI-05 Phase 1 — Strategy Integrity Digest Service

Generates and delivers the weekly strategy integrity digest via Telegram.
Format spec: docs/product/decisions/si05-telegram-message-format-spec.md (BLG-GOV-86)
Data source: GET /analytics/arc5-compliance?period=7d (SI-01 + SI-03)
Delivery: Telegram MarkdownV2 (existing v2.4 infrastructure)

ST-01 (EPIC-01, v5.1 cycle 2026-06-21__release-v5.1)
"""

import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 4096


_RETRY_DELAYS = (30, 60)  # seconds: wait after attempt 1, then attempt 2


def _send_telegram_request(url: str, payload: dict, sleep_fn=None) -> Optional[str]:
    """
    Send a Telegram API request via POST+JSON with exponential backoff retry.

    Uses POST with a JSON body rather than GET with query params — required for
    MarkdownV2 messages where URL-encoding of escape sequences can corrupt the
    request path and cause spurious 404 responses from Telegram's API.

    Retry policy: up to 2 retries after the initial attempt, with delays of
    30 s and 60 s respectively. Total maximum wait before final failure: 90 s.
    If all three attempts fail, the last exception is re-raised.

    sleep_fn is injectable for testing to avoid real sleep delays.

    Returns:
        The Telegram-assigned message_id (as a str) parsed from the
        successful response's `{"ok": true, "result": {"message_id": N, ...}}`
        body (ST-10, BLG-BE-85), or None if the response could not be parsed
        as expected (e.g. a test double that doesn't simulate the real
        Telegram API shape) — parsing failure here is non-fatal and does not
        affect send success; it only means telegram_message_id is logged as
        NULL for that attempt, same as before this story.
    """
    import json
    import urllib.request
    _sleep = sleep_fn or time.sleep
    last_exc: Exception = RuntimeError("unreachable")
    body = json.dumps(payload).encode("utf-8")
    for attempt, delay in enumerate(((None,) + _RETRY_DELAYS), start=1):
        try:
            req = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
                message_id = None
                try:
                    resp_data = json.loads(resp.read())
                    message_id = resp_data.get("result", {}).get("message_id")
                except Exception:
                    pass
            return str(message_id) if message_id is not None else None
        except Exception as exc:
            last_exc = exc
            if delay is not None:
                logger.warning(
                    "SI-05 Telegram send attempt %d failed: %s — retrying in %ds",
                    attempt, exc, delay,
                )
                _sleep(delay)
    logger.error("SI-05 Telegram send failed after all retries: %s", last_exc)
    raise last_exc


def _clean_db_url(url: str) -> str:
    """Strip Supabase-specific params not supported by libpq."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    params.pop("pgbouncer", None)
    new_query = urlencode({k: v[0] for k, v in params.items()})
    return urlunparse(parsed._replace(query=new_query))


def fetch_arc5_data_for_digest() -> Optional[dict]:
    """
    Query the database directly for SI-05 digest fields (7-day window).

    Returns a dict with:
      - validation_pass_rate: float | None (0.0–1.0 fraction, overall 7d)
      - events_per_week: float (red flag events in last 7 days)
      - override_rate: float | None (override_count / total_validations, 7d, 0.0–1.0)
      - top_rule_breach: str | None

    Returns None if DATABASE_URL is not set or connection fails.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return None

    since_7d = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

    try:
        conn = psycopg2.connect(_clean_db_url(database_url))
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            # Overall validation pass rate (7d)
            validation_pass_rate = None
            validation_na_reason = "data_unavailable"
            try:
                cursor.execute("""
                    SELECT
                        COUNT(*) FILTER (WHERE status = 'pass') AS pass_count,
                        COUNT(*) AS total
                    FROM pre_entry_validation_log
                    WHERE validated_at >= %s::timestamptz
                """, (since_7d,))
                row = cursor.fetchone()
                if row and int(row["total"]) > 0:
                    validation_pass_rate = round(int(row["pass_count"]) / int(row["total"]), 4)
                    validation_na_reason = None
                else:
                    validation_na_reason = "no_events"
            except psycopg2.errors.UndefinedTable:
                cursor.connection.rollback()

            # Red flag events (last 7 days) — events_per_week equivalent
            events_per_week = 0.0
            try:
                cursor.execute("""
                    SELECT COUNT(*) AS cnt
                    FROM red_flag_events
                    WHERE created_at >= %s::timestamptz
                """, (since_7d,))
                row = cursor.fetchone()
                if row:
                    events_per_week = float(row["cnt"])
            except psycopg2.errors.UndefinedTable:
                cursor.connection.rollback()

            # Override rate (override events / total validations, 7d)
            override_rate = None
            override_na_reason = "data_unavailable"
            try:
                cursor.execute("""
                    SELECT COUNT(*) AS override_count
                    FROM red_flag_events
                    WHERE created_at >= %s::timestamptz
                      AND event_type = 'pre_entry_override'
                """, (since_7d,))
                override_row = cursor.fetchone()
                override_count = int(override_row["override_count"]) if override_row else 0

                cursor.execute("""
                    SELECT COUNT(*) AS total
                    FROM pre_entry_validation_log
                    WHERE validated_at >= %s::timestamptz
                """, (since_7d,))
                total_row = cursor.fetchone()
                total_validations = int(total_row["total"]) if total_row else 0

                if total_validations > 0:
                    override_rate = round(override_count / total_validations, 4)
                    override_na_reason = None
                else:
                    override_na_reason = "no_events"
            except psycopg2.errors.UndefinedTable:
                cursor.connection.rollback()

            # Top rule breach (most frequent failing rule, 7d)
            top_rule_breach = None
            try:
                cursor.execute("""
                    SELECT rule_type, COUNT(*) AS fail_count
                    FROM pre_entry_validation_log
                    WHERE validated_at >= %s::timestamptz
                      AND status = 'fail'
                    GROUP BY rule_type
                    ORDER BY fail_count DESC
                    LIMIT 1
                """, (since_7d,))
                row = cursor.fetchone()
                if row:
                    top_rule_breach = row["rule_type"]
            except psycopg2.errors.UndefinedTable:
                cursor.connection.rollback()

            return {
                "validation_pass_rate": validation_pass_rate,
                "validation_na_reason": validation_na_reason,
                "events_per_week": events_per_week,
                "override_rate": override_rate,
                "override_na_reason": override_na_reason,
                "top_rule_breach": top_rule_breach,
            }

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error("SI-05 data fetch failed: %s", e)
        return None


def _format_pass_rate(rate: Optional[float], na_reason: Optional[str] = None) -> str:
    """Format pass rate (0.0–1.0) as percentage string or 'N/A' with optional reason."""
    if rate is None:
        if na_reason == "no_events":
            return r"N/A \(no validation events this week\)"
        if na_reason == "data_unavailable":
            return r"N/A \(data unavailable\)"
        return "N/A"
    return f"{rate * 100:.1f}%".replace(".", "\\.")


def _format_override_rate(rate: Optional[float], na_reason: Optional[str] = None) -> str:
    """Format override rate (0.0–1.0) as percentage string or 'N/A' with optional reason."""
    if rate is None:
        if na_reason == "no_events":
            return r"N/A \(no validation events this week\)"
        if na_reason == "data_unavailable":
            return r"N/A \(data unavailable\)"
        return "N/A"
    return f"{rate * 100:.1f}%".replace(".", "\\.")


def _format_top_rule_breach(rule: Optional[str]) -> str:
    """Title-case snake_case rule name, or 'None'."""
    if not rule:
        return "None"
    return rule.replace("_", " ").title()


def _escape_mdv2(text: str) -> str:
    """Escape MarkdownV2 special characters in a plain-text value."""
    special = r"_*[]()~`>#+-=|{}.!"
    for ch in special:
        text = text.replace(ch, f"\\{ch}")
    return text


def _integrity_summary_line(
    pass_rate: Optional[float],
    red_flag_count: int,
    override_rate: Optional[float],
    validation_na_reason: Optional[str] = None,
) -> str:
    """
    Rule-based summary line per BLG-GOV-86 §4.2.
    Returns MarkdownV2-escaped italic text. Rules evaluated in order 1–5.
    """
    if pass_rate is None:
        if validation_na_reason == "no_events":
            return r"_No pre\-entry validation events this week\._"
        return r"_No pre\-entry validation data available this week\._"
    if pass_rate * 100 < 70:
        return r"_Pass rate below threshold — review pre\-entry rule compliance\._"
    if red_flag_count > 5:
        return r"_Elevated red flag activity this week — check the journal\._"
    if override_rate is not None and override_rate > 0.30:
        return r"_High override rate — consider reviewing override decisions\._"
    return r"_Strategy integrity healthy this week\._"


def _format_deep_links(frontend_url: Optional[str]) -> str:
    """
    Format deep link footer pointing to relevant app screens (BLG-FE-73).
    Returns empty string if FRONTEND_URL env var is not configured.
    In MarkdownV2 inline links only ) and backslash need escaping in the URL part.
    """
    if not frontend_url:
        return ""
    base = frontend_url.rstrip("/")
    risk_url = f"{base}/#/RiskDashboard"
    rfj_url = f"{base}/#/RedFlagJournal"
    return f"🔗 [Risk Dashboard]({risk_url}) · [Red Flag Journal]({rfj_url})"


def format_si05_section(data: dict) -> str:
    """
    Format the SI-05 strategy integrity section per BLG-GOV-86 §4.

    Args:
        data: dict with keys validation_pass_rate, events_per_week,
              override_rate, top_rule_breach.
              Optional: validation_na_reason, override_na_reason (BLG-FE-74).

    Returns:
        MarkdownV2-formatted section string.
    """
    pass_rate = data.get("validation_pass_rate")
    events_per_week = data.get("events_per_week", 0.0) or 0.0
    override_rate = data.get("override_rate")
    top_rule_breach = data.get("top_rule_breach")
    validation_na_reason = data.get("validation_na_reason")
    override_na_reason = data.get("override_na_reason")

    red_flag_count = round(events_per_week * 7)

    pass_rate_fmt = _format_pass_rate(pass_rate, validation_na_reason)
    override_rate_fmt = _format_override_rate(override_rate, override_na_reason)
    top_rule_fmt = _escape_mdv2(_format_top_rule_breach(top_rule_breach))
    summary_line = _integrity_summary_line(pass_rate, red_flag_count, override_rate, validation_na_reason)

    section = (
        "\\-\\-\\-\n"
        "*📋 Strategy Integrity*\n\n"
        f"✅ Pre\\-entry pass rate \\(7d\\): {pass_rate_fmt}\n"
        f"🚨 Red flag events \\(7d\\): {red_flag_count}\n"
        f"⚠️ Override rate \\(7d\\): {override_rate_fmt}\n"
        f"🔍 Top rule breach: {top_rule_fmt}\n\n"
        f"{summary_line}"
    )

    frontend_url = os.getenv("FRONTEND_URL", "")
    deep_links = _format_deep_links(frontend_url)
    if deep_links:
        section += f"\n\n{deep_links}"

    return section


def _fetch_trade_count_for_digest() -> Optional[int]:
    """Return total closed trades count for the active portfolio, or None on error.

    Uses a direct psycopg2 connection consistent with the service's existing pattern.
    ST-05, EPIC-02, v5.5.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return None
    try:
        conn = psycopg2.connect(_clean_db_url(database_url), cursor_factory=RealDictCursor)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM portfolios ORDER BY created_date DESC LIMIT 1"
                )
                row = cur.fetchone()
                if not row:
                    return None
                portfolio_id = row["id"]
                cur.execute(
                    "SELECT COUNT(*)::int AS cnt FROM trade_history WHERE portfolio_id = %s",
                    (portfolio_id,),
                )
                result = cur.fetchone()
                return result["cnt"] if result else 0
        finally:
            conn.close()
    except Exception as exc:
        logger.warning("Could not fetch trade count for digest (non-fatal): %s", exc)
        return None


def _format_data_density_line(closed_trades_count: Optional[int]) -> str:
    """Format the data density progress line for the SI-05 digest.

    Returns a MarkdownV2-escaped line like:
      📊 Closed trades: 12 / Gate 1: 20 / Gate 2: 50 / Gate 3: 100
    Returns empty string if count is unavailable.
    ST-05, EPIC-02, v5.5.
    """
    if closed_trades_count is None:
        return ""
    count_str = _escape_mdv2(str(closed_trades_count))
    return (
        f"📊 Closed trades: {count_str} "
        "/ Gate 1: 20 / Gate 2: 50 / Gate 3: 100\n"
    )


def _write_delivery_log(
    status: str,
    event_count: Optional[int],
    telegram_message_id: Optional[str],
    error_message: Optional[str],
) -> None:
    """
    Write a row to si05_digest_log after each send attempt (success or failure).
    Table is created at startup via ensure_si05_digest_log_table() in database.py.
    Errors here are logged and swallowed — delivery log failures must not abort the digest job.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return
    try:
        conn = psycopg2.connect(_clean_db_url(database_url))
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO si05_digest_log
                        (status, event_count, telegram_message_id, error_message)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (status, event_count, telegram_message_id, error_message),
                )
            conn.commit()
        finally:
            conn.close()
    except Exception as log_err:
        logger.warning("SI-05 delivery log write failed (non-fatal): %s", log_err)


def send_si05_digest(*, _sleep_fn=None) -> dict:
    """
    Fetch arc5-compliance data, format the SI-05 section, and send via Telegram.

    Retry policy: up to 2 retries with 30 s / 60 s backoff on Telegram API failure.
    Each send attempt (success or failure) is logged to si05_digest_log (BLG-BE-33).

    Args:
        _sleep_fn: injectable sleep callable for testing (default: time.sleep)

    Returns:
        dict with keys: sent (bool), message_length (int), error (str | None)
    """
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    if not telegram_token or not telegram_chat_id:
        logger.warning("TELEGRAM credentials not set — skipping SI-05 digest")
        return {"sent": False, "message_length": 0, "error": "Telegram credentials not configured"}

    data = fetch_arc5_data_for_digest()
    if data is None:
        logger.warning("arc5-compliance data unavailable — omitting SI-05 digest")
        return {"sent": False, "message_length": 0, "error": "arc5-compliance data unavailable"}

    message = format_si05_section(data)

    # Append data density line (ST-05, EPIC-02, v5.5) — non-fatal if unavailable
    trade_count = _fetch_trade_count_for_digest()
    density_line = _format_data_density_line(trade_count)
    if density_line:
        message = message + "\n" + density_line
    message_length = len(message)

    # Truncate to summary line if over budget (BLG-GOV-86 §7)
    if message_length > MAX_MESSAGE_LENGTH:
        pass_rate = data.get("validation_pass_rate")
        events_per_week = data.get("events_per_week", 0.0) or 0.0
        override_rate = data.get("override_rate")
        summary_line = _integrity_summary_line(pass_rate, round(events_per_week * 7), override_rate)
        message = f"\\-\\-\\-\n*📋 Strategy Integrity*\n\n{summary_line}"
        message_length = len(message)
        logger.warning("SI-05 message truncated to summary line (%d chars)", message_length)

    event_count = round((data.get("events_per_week") or 0.0) * 7)

    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message,
        "parse_mode": "MarkdownV2",
    }

    try:
        telegram_message_id = _send_telegram_request(url, payload, sleep_fn=_sleep_fn)
        logger.info("SI-05 digest sent (%d chars)", message_length)
        _write_delivery_log("sent", event_count, telegram_message_id, None)
        return {"sent": True, "message_length": message_length, "error": None}
    except Exception as e:
        logger.error("SI-05 Telegram send failed: %s", e)
        _write_delivery_log("failed", event_count, None, str(e))
        return {"sent": False, "message_length": message_length, "error": str(e)}
