"""
AI Audit Log Service (BLG-AI-01 — ST-14)

Records each AI summary run in a persistent DB table for governance tracking.

Fields logged per run:
  - run_id (UUID)
  - invoked_at (timestamp)
  - trade_ids (array of IDs included, or null if date-range query)
  - date_from / date_to (when trade_ids not used)
  - trade_count (number of trades included)
  - model_version (LLM model used — see docs/specs/ai_journal_model_contract.md)
  - output_hash (SHA-256 of summary text; null if summary=None)
  - summary_produced (bool — True if non-null summary returned)

Queryable by trade_id (array contains) and by date range (invoked_at).

Model version contract: docs/specs/ai_journal_model_contract.md (BLG-AI-02).
The model_version field records the actual Claude model used per run; the
contract document is the canonical source for the current configured version.
"""
import hashlib
import uuid
from datetime import datetime, date
from typing import Optional, List
from database import get_db


def ensure_ai_audit_table() -> None:
    """Create the ai_audit_log table if it does not already exist."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ai_audit_log (
                    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    invoked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    trade_ids INTEGER[],
                    date_from DATE,
                    date_to DATE,
                    trade_count INTEGER NOT NULL DEFAULT 0,
                    model_version VARCHAR(100),
                    output_hash VARCHAR(64),
                    summary_produced BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_ai_audit_invoked
                ON ai_audit_log (invoked_at DESC)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_ai_audit_trade_ids
                ON ai_audit_log USING GIN (trade_ids)
            """)
        conn.commit()


def log_ai_summary_run(
    trade_ids: Optional[List[int]],
    date_from: Optional[date],
    date_to: Optional[date],
    trade_count: int,
    model_version: Optional[str],
    summary_text: Optional[str],
) -> str:
    """
    Write one audit record for an AI summary invocation.
    Returns the run_id UUID string.
    """
    output_hash = None
    if summary_text:
        output_hash = hashlib.sha256(summary_text.encode()).hexdigest()

    run_id = str(uuid.uuid4())

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ai_audit_log
                  (run_id, invoked_at, trade_ids, date_from, date_to,
                   trade_count, model_version, output_hash, summary_produced)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    run_id,
                    datetime.utcnow(),
                    trade_ids,
                    date_from,
                    date_to,
                    trade_count,
                    model_version,
                    output_hash,
                    summary_text is not None,
                ),
            )
        conn.commit()

    return run_id


def query_audit_log(
    trade_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = 50,
) -> List[dict]:
    """
    Query the audit log. Filters:
      - trade_id: returns runs where trade_ids contains this value
      - date_from / date_to: filter by invoked_at range
    Returns list of audit record dicts, newest first.
    """
    filters = []
    params = []

    if trade_id is not None:
        filters.append("%s = ANY(trade_ids)")
        params.append(trade_id)
    if date_from is not None:
        filters.append("invoked_at >= %s")
        params.append(datetime.combine(date_from, datetime.min.time()))
    if date_to is not None:
        filters.append("invoked_at <= %s")
        params.append(datetime.combine(date_to, datetime.max.time()))

    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    params.append(limit)

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT run_id, invoked_at, trade_ids, date_from, date_to,
                       trade_count, model_version, output_hash, summary_produced
                FROM ai_audit_log
                {where}
                ORDER BY invoked_at DESC
                LIMIT %s
                """,
                params,
            )
            rows = cur.fetchall()

    return [dict(r) for r in rows]
