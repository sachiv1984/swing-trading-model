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
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 4096


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
                "events_per_week": events_per_week,
                "override_rate": override_rate,
                "top_rule_breach": top_rule_breach,
            }

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error("SI-05 data fetch failed: %s", e)
        return None


def _format_pass_rate(rate: Optional[float]) -> str:
    """Format pass rate (0.0–1.0) as percentage string or 'N/A'."""
    if rate is None:
        return "N/A"
    return f"{rate * 100:.1f}%"


def _format_override_rate(rate: Optional[float]) -> str:
    """Format override rate (0.0–1.0) as percentage string or 'N/A'."""
    if rate is None:
        return "N/A"
    return f"{rate * 100:.1f}%"


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
) -> str:
    """
    Rule-based summary line per BLG-GOV-86 §4.2.
    Returns MarkdownV2-escaped italic text. Rules evaluated in order 1–5.
    """
    if pass_rate is None:
        return r"_No pre\-entry validation data available this week\._"
    if pass_rate * 100 < 70:
        return r"_Pass rate below threshold — review pre\-entry rule compliance\._"
    if red_flag_count > 5:
        return r"_Elevated red flag activity this week — check the journal\._"
    if override_rate is not None and override_rate > 0.30:
        return r"_High override rate — consider reviewing override decisions\._"
    return r"_Strategy integrity healthy this week\._"


def format_si05_section(data: dict) -> str:
    """
    Format the SI-05 strategy integrity section per BLG-GOV-86 §4.

    Args:
        data: dict with keys validation_pass_rate, events_per_week,
              override_rate, top_rule_breach

    Returns:
        MarkdownV2-formatted section string.
    """
    pass_rate = data.get("validation_pass_rate")
    events_per_week = data.get("events_per_week", 0.0) or 0.0
    override_rate = data.get("override_rate")
    top_rule_breach = data.get("top_rule_breach")

    red_flag_count = round(events_per_week * 7)

    pass_rate_fmt = _format_pass_rate(pass_rate)
    override_rate_fmt = _format_override_rate(override_rate)
    top_rule_fmt = _escape_mdv2(_format_top_rule_breach(top_rule_breach))
    summary_line = _integrity_summary_line(pass_rate, red_flag_count, override_rate)

    return (
        "---\n"
        "*📋 Strategy Integrity*\n\n"
        f"✅ Pre\\-entry pass rate \\(7d\\): {pass_rate_fmt}\n"
        f"🚨 Red flag events \\(7d\\): {red_flag_count}\n"
        f"⚠️ Override rate \\(7d\\): {override_rate_fmt}\n"
        f"🔍 Top rule breach: {top_rule_fmt}\n\n"
        f"{summary_line}"
    )


def send_si05_digest() -> dict:
    """
    Fetch arc5-compliance data, format the SI-05 section, and send via Telegram.

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
    message_length = len(message)

    # Truncate to summary line if over budget (BLG-GOV-86 §7)
    if message_length > MAX_MESSAGE_LENGTH:
        pass_rate = data.get("validation_pass_rate")
        events_per_week = data.get("events_per_week", 0.0) or 0.0
        override_rate = data.get("override_rate")
        summary_line = _integrity_summary_line(pass_rate, round(events_per_week * 7), override_rate)
        message = f"---\n*📋 Strategy Integrity*\n\n{summary_line}"
        message_length = len(message)
        logger.warning("SI-05 message truncated to summary line (%d chars)", message_length)

    try:
        params = urlencode({
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "MarkdownV2",
        })
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?{params}"
        import urllib.request
        urllib.request.urlopen(url, timeout=10)  # noqa: S310
        logger.info("SI-05 digest sent (%d chars)", message_length)
        return {"sent": True, "message_length": message_length, "error": None}
    except Exception as e:
        logger.error("SI-05 Telegram send failed: %s", e)
        return {"sent": False, "message_length": message_length, "error": str(e)}
