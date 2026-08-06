"""
Weekly Trading Digest Router

GET /digest/weekly — 7-day summary of realised P&L, unrealised P&L delta,
alert activity, compliance score, and staleness.

POST /digest/si05/send — Trigger the SI-05 Phase 1 strategy integrity digest
via Telegram. Intended for weekly cron/scheduled invocation.

Contracts: docs/specs/api_contracts/digest_endpoints.md v0.4
ST-08 (BLG-FEAT-14 BE component, v2.4) / ST-01 (SI-05 Phase 1, v5.1)
ST-08 (BLG-BE-35, v5.3) — API key auth on POST /digest/si05/send
"""

import os
import logging
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse


def _verify_api_key(x_api_key: str = Header(default=None)) -> bool:
    """
    Require X-API-Key header matching API_KEY env var.
    When API_KEY is not set the dependency is a no-op (local dev parity with
    the global middleware in main.py).

    Returns True when authorised, False otherwise — the caller endpoint
    returns the canonical error envelope itself (ST-08, BLG-BE-69) rather
    than this dependency raising HTTPException directly, since a FastAPI
    Depends() callable cannot itself produce a JSONResponse body: an
    exception raised here propagates straight to FastAPI's default handler
    (the {"detail": ...} shape this story exists to eliminate), bypassing any
    try/except the endpoint function might otherwise use to translate it.
    """
    expected = os.environ.get("API_KEY")
    return not (expected and x_api_key != expected)


def _clean_db_url(url: str) -> str:
    """Strip Supabase-specific params (e.g. pgbouncer) not supported by libpq."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    params.pop("pgbouncer", None)
    new_query = urlencode({k: v[0] for k, v in params.items()})
    return urlunparse(parsed._replace(query=new_query))

logger = logging.getLogger(__name__)

from services.si05_digest_service import send_si05_digest

router = APIRouter(prefix="/digest", tags=["Digest"])


@router.get("/weekly")
def get_weekly_digest():
    """
    GET /digest/weekly

    Returns a 7-day trading digest with raw numeric/boolean fields:

    - realised_pnl_7d: sum of P&L for trades closed in the last 7 calendar days (GBP)
    - unrealised_pnl_delta_7d: change in total unrealised P&L over the last 7 days
      (current unrealised P&L minus unrealised P&L 7 days ago from portfolio snapshots)
    - alerts_fired_7d: count of notifications created in the last 7 days
    - alerts_dismissed_7d: count of notifications marked read in the last 7 days
    - compliance_score_current: journal_completion_rate from all closed trades (%)
    - compliance_score_7d_ago: journal_completion_rate for trades closed before 7 days ago (%)
    - staleness_hours: hours since last portfolio snapshot (null if no snapshots)
    - as_of_utc: UTC timestamp this response was computed

    Scope constraint: no generated text, narrative, or interpretation in any field.

    Spec: docs/specs/api_contracts/digest_endpoints.md v0.1
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return JSONResponse(status_code=500, content={"status": "error", "message": "DATABASE_URL not configured"})

    try:
        conn = psycopg2.connect(_clean_db_url(database_url))
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        now_utc = datetime.now(timezone.utc)
        cutoff_7d = now_utc - timedelta(days=7)
        cutoff_7d_date = cutoff_7d.date()

        try:
            # ----------------------------------------------------------------
            # 1. Realised P&L — trades closed in the last 7 days
            # ----------------------------------------------------------------
            cursor.execute("""
                SELECT COALESCE(SUM(pnl), 0) AS realised_pnl_7d
                FROM trade_history
                WHERE exit_date >= %s
            """, (cutoff_7d_date,))
            row = cursor.fetchone()
            realised_pnl_7d = round(float(row["realised_pnl_7d"]), 2) if row else 0.0

            # ----------------------------------------------------------------
            # 2. Unrealised P&L delta — portfolio snapshot comparison
            #    current_unrealised - unrealised_7d_ago
            # ----------------------------------------------------------------
            unrealised_pnl_delta_7d = None
            try:
                # Most recent snapshot
                cursor.execute("""
                    SELECT unrealised_pnl
                    FROM portfolio_history
                    WHERE unrealised_pnl IS NOT NULL
                    ORDER BY snapshot_date DESC
                    LIMIT 1
                """)
                latest = cursor.fetchone()

                # Snapshot closest to 7 days ago (on or before cutoff)
                cursor.execute("""
                    SELECT unrealised_pnl
                    FROM portfolio_history
                    WHERE snapshot_date <= %s
                      AND unrealised_pnl IS NOT NULL
                    ORDER BY snapshot_date DESC
                    LIMIT 1
                """, (cutoff_7d_date,))
                seven_days_ago = cursor.fetchone()

                if latest and seven_days_ago:
                    unrealised_pnl_delta_7d = round(
                        float(latest["unrealised_pnl"]) - float(seven_days_ago["unrealised_pnl"]),
                        2,
                    )
            except Exception as e:
                logger.warning("Could not compute unrealised_pnl_delta_7d: %s", e)

            # ----------------------------------------------------------------
            # 3. Alerts fired and dismissed in last 7 days
            # ----------------------------------------------------------------
            alerts_fired_7d = 0
            alerts_dismissed_7d = 0
            try:
                cursor.execute("""
                    SELECT
                        COUNT(*) AS fired,
                        COUNT(CASE WHEN read = TRUE THEN 1 END) AS dismissed
                    FROM notifications
                    WHERE created_at >= %s
                """, (cutoff_7d,))
                alert_row = cursor.fetchone()
                if alert_row:
                    alerts_fired_7d = int(alert_row["fired"])
                    alerts_dismissed_7d = int(alert_row["dismissed"])
            except Exception as e:
                logger.warning("Could not compute alert counts: %s", e)

            # ----------------------------------------------------------------
            # 4. Compliance score — journal_completion_rate
            #    current: all closed trades
            #    7d ago: trades closed BEFORE the 7-day window (baseline)
            # ----------------------------------------------------------------
            compliance_score_current = 0.0
            compliance_score_7d_ago = 0.0
            try:
                cursor.execute("""
                    SELECT
                        COUNT(*) AS total,
                        COUNT(CASE
                            WHEN (entry_note IS NOT NULL AND entry_note != '')
                              OR (exit_note  IS NOT NULL AND exit_note  != '')
                            THEN 1 END) AS with_notes
                    FROM trade_history
                """)
                comp_row = cursor.fetchone()
                if comp_row and int(comp_row["total"]) > 0:
                    compliance_score_current = round(
                        int(comp_row["with_notes"]) / int(comp_row["total"]) * 100, 1
                    )

                # Baseline: trades exited before the 7-day window
                cursor.execute("""
                    SELECT
                        COUNT(*) AS total,
                        COUNT(CASE
                            WHEN (entry_note IS NOT NULL AND entry_note != '')
                              OR (exit_note  IS NOT NULL AND exit_note  != '')
                            THEN 1 END) AS with_notes
                    FROM trade_history
                    WHERE exit_date < %s
                """, (cutoff_7d_date,))
                comp_base = cursor.fetchone()
                if comp_base and int(comp_base["total"]) > 0:
                    compliance_score_7d_ago = round(
                        int(comp_base["with_notes"]) / int(comp_base["total"]) * 100, 1
                    )
            except Exception as e:
                logger.warning("Could not compute compliance scores: %s", e)

            # ----------------------------------------------------------------
            # 5. Staleness — hours since last portfolio snapshot
            # ----------------------------------------------------------------
            staleness_hours = None
            try:
                cursor.execute("""
                    SELECT snapshot_date
                    FROM portfolio_history
                    ORDER BY snapshot_date DESC
                    LIMIT 1
                """)
                snap_row = cursor.fetchone()
                if snap_row and snap_row["snapshot_date"]:
                    snap_dt = datetime.combine(
                        snap_row["snapshot_date"],
                        datetime.min.time(),
                        tzinfo=timezone.utc,
                    )
                    delta = now_utc - snap_dt
                    staleness_hours = round(delta.total_seconds() / 3600, 1)
            except Exception as e:
                logger.warning("Could not compute staleness_hours: %s", e)

        finally:
            cursor.close()
            conn.close()

        return {
            "status": "ok",
            "data": {
                "realised_pnl_7d": realised_pnl_7d,
                "unrealised_pnl_delta_7d": unrealised_pnl_delta_7d,
                "alerts_fired_7d": alerts_fired_7d,
                "alerts_dismissed_7d": alerts_dismissed_7d,
                "compliance_score_current": compliance_score_current,
                "compliance_score_7d_ago": compliance_score_7d_ago,
                "staleness_hours": staleness_hours,
                "as_of_utc": now_utc.isoformat(),
            },
        }

    except Exception as e:
        logger.error("Weekly digest endpoint error: %s", e)
        return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to compute weekly digest"})


@router.post("/si05/send")
def send_si05_digest_endpoint(authorized: bool = Depends(_verify_api_key)):
    """
    POST /digest/si05/send

    Trigger the SI-05 Phase 1 weekly strategy integrity digest via Telegram.
    Fetches arc5-compliance data (SI-01 + SI-03) and sends a formatted MarkdownV2
    message per docs/product/decisions/si05-telegram-message-format-spec.md (BLG-GOV-86).

    Intended to be called by a weekly scheduler (Render cron or external scheduler).
    Safe to retry — idempotent per call (message reflects current DB state).

    Spec: docs/specs/api_contracts/digest_endpoints.md v0.2
    ST-01 (SI-05 Phase 1, EPIC-01, v5.1)
    """
    if not authorized:
        return JSONResponse(status_code=401, content={"status": "error", "message": "Unauthorized"})
    result = send_si05_digest()
    if result["sent"]:
        return {"status": "ok", **result}
    return {"status": "error", **result}
