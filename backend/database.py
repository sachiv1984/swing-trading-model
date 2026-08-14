import os
import re
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict
from datetime import datetime, timezone
import pandas as pd
import time
import requests
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")


def _clean_db_url(url: str) -> str:
    """Strip Supabase-specific params (e.g. pgbouncer) not supported by libpq."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    params.pop("pgbouncer", None)
    new_query = urlencode({k: v[0] for k, v in params.items()})
    return urlunparse(parsed._replace(query=new_query))


@contextmanager
def get_db():
    """Database connection context manager"""
    conn = psycopg2.connect(_clean_db_url(DATABASE_URL), cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()  # CRITICAL: Ensure commit happens
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_portfolio(conn=None) -> Optional[Dict]:
    """Get the main portfolio (assumes single portfolio).

    If conn is provided, reuses it instead of opening a new connection.
    """
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM portfolios LIMIT 1")
            return cur.fetchone()
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM portfolios LIMIT 1")
            return cur.fetchone()


def update_portfolio_cash(portfolio_id: str, cash: float):
    """Update portfolio cash balance"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE portfolios SET cash = %s, last_updated = NOW() WHERE id = %s",
                (cash, portfolio_id)
            )


def get_positions(portfolio_id: str, status: str = None, conn=None) -> List[Dict]:
    """Get positions, optionally filtered by status.

    If conn is provided, reuses it instead of opening a new connection.
    """
    def _run(cur):
        if status:
            cur.execute(
                "SELECT * FROM positions WHERE portfolio_id = %s AND status = %s ORDER BY entry_date DESC",
                (portfolio_id, status)
            )
        else:
            cur.execute(
                "SELECT * FROM positions WHERE portfolio_id = %s ORDER BY entry_date DESC",
                (portfolio_id,)
            )
        return cur.fetchall()

    if conn is not None:
        with conn.cursor() as cur:
            return _run(cur)
    with get_db() as conn:
        with conn.cursor() as cur:
            return _run(cur)


def create_position(portfolio_id: str, position_data: Dict) -> Dict:
    """Create a new position"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO positions (
                    portfolio_id, ticker, market, entry_date, entry_price,
                    fill_price, fill_currency, fx_rate, shares, total_cost,
                    fees_paid, fee_type, initial_stop, current_stop, current_price,
                    atr, holding_days, pnl, pnl_pct, status,
                    entry_note, tags, user_fill_price, strategy_version_at_entry
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                RETURNING *
            """, (
                portfolio_id,
                position_data.get('ticker'),
                position_data.get('market'),
                position_data.get('entry_date'),
                position_data.get('entry_price'),
                position_data.get('fill_price'),
                position_data.get('fill_currency'),
                position_data.get('fx_rate'),
                position_data.get('shares'),
                position_data.get('total_cost'),
                position_data.get('fees_paid'),
                position_data.get('fee_type'),
                position_data.get('initial_stop'),
                position_data.get('current_stop'),
                position_data.get('current_price'),
                position_data.get('atr'),
                position_data.get('holding_days', 0),
                position_data.get('pnl', 0),
                position_data.get('pnl_pct', 0),
                position_data.get('status', 'open'),
                position_data.get('entry_note'),
                position_data.get('tags'),
                position_data.get('user_fill_price'),
                position_data.get('strategy_version_at_entry'),
            ))
            return cur.fetchone()


def update_position(position_id: str, updates: Dict):
    """Update a position - FIXED VERSION with explicit commit and debugging"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Build dynamic UPDATE query
            set_parts = []
            values = []
            
            for key, value in updates.items():
                set_parts.append(f"{key} = %s")
                values.append(value)
            
            # Add position_id for WHERE clause
            values.append(position_id)
            
            # Build and execute query
            query = f"""
                UPDATE positions 
                SET {', '.join(set_parts)}, updated_at = NOW() 
                WHERE id = %s 
                RETURNING *
            """
            
            print(f"🔍 DEBUG: Executing update_position")
            print(f"   Position ID: {position_id}")
            print(f"   Updates: {updates}")
            print(f"   Query: {query}")
            print(f"   Values: {values}")
            
            cur.execute(query, values)
            result = cur.fetchone()
            
            if result:
                print(f"✅ Position updated successfully")
                print(f"   New status: {result.get('status')}")
                print(f"   Exit date: {result.get('exit_date')}")
            else:
                print(f"❌ WARNING: update_position returned None!")
                print(f"   This means no rows were updated")
                print(f"   Position ID might not exist: {position_id}")
            
            # CRITICAL: Ensure the transaction commits
            conn.commit()
            print(f"✅ Transaction committed")
            
            return result


def delete_position(position_id: str):
    """Delete a position"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM positions WHERE id = %s", (position_id,))


def get_trade_history(portfolio_id: str) -> List[Dict]:
    """Get trade history"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM trade_history WHERE portfolio_id = %s ORDER BY exit_date DESC",
                (portfolio_id,)
            )
            return cur.fetchall()


def get_trade_history_by_tax_year(portfolio_id: str, year_start, year_end) -> List[Dict]:
    """Get trade history filtered to trades whose exit_date falls within [year_start, year_end] inclusive.

    Used by GET /reports/tax-year.
    Spec: docs/specs/api_contracts/reports_endpoints.md §Tax year attribution.

    ST-31 (BLG-FEAT-78, EPIC-01, v8.4): each row also carries a `trade_origin`
    column — "Signal" if the trade's linked trade_plan (if any) has a non-null
    signal_id (momentum screener signal), else "Manual". Derived via the
    documented two-hop relationship trade_history.position_id = positions.id
    AND trade_plans.position_id = positions.id (data_model.md §Trade Plan to
    Position Relationship) -- since a trade_plan's position_id and a
    trade_history row's position_id both reference the same positions.id when
    linked, trade_plans.position_id = trade_history.position_id is a valid
    direct equijoin without needing to name positions explicitly. Cardinality
    is one trade_plan to zero-or-one positions, so this LEFT JOIN cannot
    duplicate trade_history rows. Trades with no linked plan, or a plan whose
    signal_id is null, are "Manual" -- there is no separate schema linkage for
    the unrelated price_alerts (BLG-FE-116) feature (see ESC-EXEC-20260807-01).
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT th.*,
                          CASE WHEN tp.signal_id IS NOT NULL THEN 'Signal' ELSE 'Manual' END AS trade_origin
                   FROM trade_history th
                   LEFT JOIN trade_plans tp ON tp.position_id = th.position_id
                   WHERE th.portfolio_id = %s
                   AND th.exit_date BETWEEN %s AND %s
                   ORDER BY th.exit_date ASC""",
                (portfolio_id, year_start, year_end)
            )
            return cur.fetchall()


def get_trade_history_pnl_sum_by_tax_year(portfolio_id: str, year_start, year_end) -> Dict:
    """Independently re-derive the realised P&L total for a tax year via a
    server-side SUM, as a separate query path from get_trade_history_by_tax_year
    (which fetches full rows for the Tax Year report/CSV export).

    Returns {"total": float, "trade_count": int}.

    Used by GET /reports/reconciliation (ST-01, EPIC-01, v8.2, BLG-FEAT-88) so a
    divergence between the system total and the export total is meaningful
    rather than definitionally impossible (docs/design/2026-08-04__release-v8.2/
    pnl-reconciliation-report/decision_record.md §4).
    Spec: docs/specs/api_contracts/reports_endpoints.md §GET /reports/reconciliation.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT COALESCE(SUM(pnl), 0)::float AS total, COUNT(*)::int AS trade_count
                   FROM trade_history
                   WHERE portfolio_id = %s
                   AND exit_date BETWEEN %s AND %s""",
                (portfolio_id, year_start, year_end)
            )
            row = cur.fetchone()
            return row


def get_monthly_pnl(portfolio_id: str) -> List[Dict]:
    """Aggregate realised P&L by calendar month for the current and prior year.

    Used by GET /reports/monthly-pnl.
    Spec: docs/specs/api_contracts/reports_endpoints.md §GET /reports/monthly-pnl
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT
                   EXTRACT(YEAR FROM exit_date)::int AS year,
                   EXTRACT(MONTH FROM exit_date)::int AS month,
                   COALESCE(SUM(pnl), 0)::float AS realised_pnl_gbp,
                   COUNT(*)::int AS trade_count
                   FROM trade_history
                   WHERE portfolio_id = %s
                   AND exit_date >= date_trunc('year', CURRENT_DATE - INTERVAL '1 year')
                   GROUP BY year, month
                   ORDER BY year DESC, month DESC""",
                (portfolio_id,)
            )
            return cur.fetchall()


def get_daily_pnl(portfolio_id: str, year: int, month: int) -> List[Dict]:
    """Aggregate realised P&L by calendar day for a single given month (ST-04, BLG-FE-118, v7.5).

    Day-granularity sibling of get_monthly_pnl — identical grouping logic,
    narrower window and finer bucket, per readiness pass AC-02.
    Used by GET /reports/daily-pnl.
    Spec: docs/specs/api_contracts/reports_endpoints.md §GET /reports/daily-pnl
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT
                   EXTRACT(DAY FROM exit_date)::int AS day,
                   COALESCE(SUM(pnl), 0)::float AS realised_pnl_gbp,
                   COUNT(*)::int AS trade_count
                   FROM trade_history
                   WHERE portfolio_id = %s
                   AND EXTRACT(YEAR FROM exit_date)::int = %s
                   AND EXTRACT(MONTH FROM exit_date)::int = %s
                   GROUP BY day
                   ORDER BY day ASC""",
                (portfolio_id, year, month)
            )
            return cur.fetchall()


def create_trade_history(portfolio_id: str, trade_data: Dict) -> Dict:
    """Add a trade to history"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO trade_history (
                    portfolio_id, position_id, ticker, market, entry_date, exit_date,
                    shares, entry_price, exit_price, total_cost, gross_proceeds,
                    net_proceeds, entry_fees, exit_fees, pnl, pnl_pct,
                    holding_days, exit_reason, entry_fx_rate, exit_fx_rate,
                    entry_note, exit_note, tags, fill_price, planned_entry_price
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                RETURNING *
            """, (
                portfolio_id,
                trade_data.get('position_id'),
                trade_data.get('ticker'),
                trade_data.get('market'),
                trade_data.get('entry_date'),
                trade_data.get('exit_date'),
                trade_data.get('shares'),
                trade_data.get('entry_price'),
                trade_data.get('exit_price'),
                trade_data.get('total_cost'),
                trade_data.get('gross_proceeds'),
                trade_data.get('net_proceeds'),
                trade_data.get('entry_fees'),
                trade_data.get('exit_fees'),
                trade_data.get('pnl'),
                trade_data.get('pnl_pct'),
                trade_data.get('holding_days'),
                trade_data.get('exit_reason'),
                trade_data.get('entry_fx_rate'),
                trade_data.get('exit_fx_rate'),
                trade_data.get('entry_note'),
                trade_data.get('exit_note'),
                trade_data.get('tags'),
                trade_data.get('fill_price'),
                trade_data.get('planned_entry_price'),
            ))
            return cur.fetchone()


def get_settings():
    """Get all settings"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM settings ORDER BY created_at DESC LIMIT 1")
            result = cur.fetchone()
            if result:
                return [dict(result)]
            return []


def create_settings(data):
    """Create new settings record"""
    with get_db() as conn:
        with conn.cursor() as cur:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO settings ({columns}) VALUES ({placeholders}) RETURNING *"
            
            cur.execute(query, list(data.values()))
            result = cur.fetchone()
            return dict(result)


def update_settings(settings_id: str, data: dict) -> dict:
    """Update existing settings"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Filter out None values
            filtered_data = {k: v for k, v in data.items() if v is not None}
            
            if not filtered_data:
                cur.execute("SELECT * FROM settings WHERE id = %s", (settings_id,))
                result = cur.fetchone()
                if not result:
                    raise ValueError(f"Settings with id {settings_id} not found")
                return dict(result)
            
            # Build SET clause
            set_parts = [f"{k} = %s" for k in filtered_data.keys()]
            set_clause = ', '.join(set_parts)
            query = f"UPDATE settings SET {set_clause}, updated_at = NOW() WHERE id = %s RETURNING *"
            
            # Execute
            values = list(filtered_data.values()) + [settings_id]
            cur.execute(query, values)
            result = cur.fetchone()
            
            if not result:
                raise ValueError(f"Settings with id {settings_id} not found")
            
            return dict(result)

def download_ticker_data(ticker: str, start_date: str, end_date: str = None):
    """Download historical data for a single ticker using Yahoo API"""
    try:
        time.sleep(0.1)  # Rate limiting
        
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Convert dates to timestamps
        start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
        
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "period1": start_ts,
            "period2": end_ts
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            # Get timestamps
            if "timestamp" not in result:
                return None
                
            timestamps = result["timestamp"]
            dates = [datetime.fromtimestamp(ts) for ts in timestamps]
            
            # Get price data
            if "indicators" not in result or "quote" not in result["indicators"]:
                return None
                
            quote = result["indicators"]["quote"][0]
            
            # Use adjusted close if available, otherwise close
            if "adjclose" in result["indicators"] and result["indicators"]["adjclose"]:
                closes = result["indicators"]["adjclose"][0]["adjclose"]
            else:
                closes = quote.get("close", [])
            
            highs = quote.get("high", [])
            lows = quote.get("low", [])
            volumes = quote.get("volume", [])

            # Create DataFrame
            df_data = {
                'date': dates,
                'close': closes,
                'high': highs,
                'low': lows,
            }
            # Include volume when available (used by ST-09 supplementary indicators)
            if volumes:
                df_data['volume'] = volumes

            df = pd.DataFrame(df_data)
            
            # Remove None values
            df = df.dropna()
            
            if len(df) < 50:  # Minimum data requirement
                return None
            
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            
            return df
            
        return None
        
    except Exception as e:
        print(f"  ⚠️  Error fetching {ticker}: {str(e)[:50]}")
        return None


def compute_atr_simple(prices: pd.Series, period: int = 14):
    """Calculate ATR using close-to-close approximation (simpler)"""
    close_to_close = prices.diff().abs()
    atr = close_to_close.rolling(window=period, min_periods=period).mean()
    return atr


# ============================================================================
# CASH TRANSACTION FUNCTIONS
# ============================================================================

def create_cash_transaction(portfolio_id: str, transaction_data: Dict) -> Dict:
    """Create a cash transaction (deposit or withdrawal)"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cash_transactions 
                (portfolio_id, type, amount, date, note)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                portfolio_id,
                transaction_data['type'],
                transaction_data['amount'],
                transaction_data.get('date', datetime.now().date()),
                transaction_data.get('note', '')
            ))
            return cur.fetchone()


def get_cash_transactions(portfolio_id: str, order_by: str = 'DESC') -> List[Dict]:
    """Get all cash transactions for a portfolio"""
    with get_db() as conn:
        with conn.cursor() as cur:
            query = f"""
                SELECT * FROM cash_transactions
                WHERE portfolio_id = %s
                ORDER BY date {order_by}, created_at {order_by}
            """
            cur.execute(query, (portfolio_id,))
            return cur.fetchall()


def get_total_deposits_withdrawals(portfolio_id: str, conn=None) -> Dict:
    """Get total deposits and withdrawals for a portfolio.

    If conn is provided, reuses it instead of opening a new connection.
    """
    def _run(cur):
        cur.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END), 0) as total_deposits,
                COALESCE(SUM(CASE WHEN type = 'withdrawal' THEN amount ELSE 0 END), 0) as total_withdrawals
            FROM cash_transactions
            WHERE portfolio_id = %s
        """, (portfolio_id,))
        result = cur.fetchone()
        return {
            'total_deposits': float(result['total_deposits']),
            'total_withdrawals': float(result['total_withdrawals']),
            'net_cash_flow': float(result['total_deposits']) - float(result['total_withdrawals'])
        }

    if conn is not None:
        with conn.cursor() as cur:
            return _run(cur)
    with get_db() as conn:
        with conn.cursor() as cur:
            return _run(cur)


# ============================================================================
# PORTFOLIO HISTORY FUNCTIONS
# ============================================================================

def create_portfolio_snapshot(snapshot_data: Dict) -> Dict:
    """Create a portfolio snapshot (or update if exists for that date)"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO portfolio_history 
                (portfolio_id, snapshot_date, total_value, cash_balance, 
                 positions_value, total_pnl, position_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (portfolio_id, snapshot_date) 
                DO UPDATE SET
                    total_value = EXCLUDED.total_value,
                    cash_balance = EXCLUDED.cash_balance,
                    positions_value = EXCLUDED.positions_value,
                    total_pnl = EXCLUDED.total_pnl,
                    position_count = EXCLUDED.position_count,
                    created_at = CURRENT_TIMESTAMP
                RETURNING *;
            """, (
                snapshot_data['portfolio_id'],
                snapshot_data['snapshot_date'],
                snapshot_data['total_value'],
                snapshot_data['cash_balance'],
                snapshot_data['positions_value'],
                snapshot_data['total_pnl'],
                snapshot_data.get('position_count', 0)
            ))
            return cur.fetchone()


def get_portfolio_snapshots(portfolio_id: str, days: int = 30) -> List[Dict]:
    """Get portfolio history for last N days"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    snapshot_date,
                    total_value,
                    cash_balance,
                    positions_value,
                    total_pnl,
                    position_count,
                    created_at
                FROM portfolio_history
                WHERE portfolio_id = %s
                AND snapshot_date >= CURRENT_DATE - INTERVAL '%s days'
                ORDER BY snapshot_date ASC
            """, (portfolio_id, days))
            return cur.fetchall()


def get_latest_snapshot(portfolio_id: str) -> Optional[Dict]:
    """Get the most recent snapshot"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM portfolio_history
                WHERE portfolio_id = %s
                ORDER BY snapshot_date DESC
                LIMIT 1
            """, (portfolio_id,))
            return cur.fetchone()


# ============================================================================
# SECTOR/REGIME HISTORY (ST-02, EPIC-02, v7.9, BLG-FEAT-67)
# ============================================================================
#
# No historical sector or regime data existed anywhere before this table —
# GET /portfolio/sector-weights and GET /market/status both compute their
# figures live from current data on every call, with no persisted daily/
# weekly record. This table starts capturing that going forward only; no
# retroactive backfill is attempted (there is no reliable way to reconstruct
# past sector allocations or regime status from current live-computed data
# without fabricating history). See docs/specs/data_model.md's migration
# entry for this table and the Metrics Definitions & Analytics Owner's
# scope decision recorded in execution_state.json for this story.

def ensure_sector_regime_history_table() -> None:
    """Create sector_regime_history table if it does not yet exist (idempotent)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sector_regime_history (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
                    snapshot_date DATE NOT NULL,
                    sectors JSONB NOT NULL DEFAULT '[]',
                    regime_us BOOLEAN,
                    regime_uk BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (portfolio_id, snapshot_date)
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_sector_regime_history_portfolio_date
                    ON sector_regime_history (portfolio_id, snapshot_date DESC)
            """)


def create_sector_regime_snapshot(portfolio_id: str, snapshot_date, sectors: list, regime_us, regime_uk) -> Dict:
    """Create (or upsert, idempotent per day like create_portfolio_snapshot) today's
    sector/regime snapshot row."""
    ensure_sector_regime_history_table()
    with get_db() as conn:
        with conn.cursor() as cur:
            _json = __import__("json").dumps
            cur.execute("""
                INSERT INTO sector_regime_history
                    (portfolio_id, snapshot_date, sectors, regime_us, regime_uk)
                VALUES (%s, %s, %s::jsonb, %s, %s)
                ON CONFLICT (portfolio_id, snapshot_date)
                DO UPDATE SET
                    sectors = EXCLUDED.sectors,
                    regime_us = EXCLUDED.regime_us,
                    regime_uk = EXCLUDED.regime_uk,
                    created_at = CURRENT_TIMESTAMP
                RETURNING *;
            """, (portfolio_id, snapshot_date, _json(sectors), regime_us, regime_uk))
            return cur.fetchone()


def get_sector_regime_history(portfolio_id: str, weeks: int = 12) -> List[Dict]:
    """Return the last `weeks * 7` days of raw snapshot rows, oldest first.
    Weekly bucketing (one row per ISO week, per §8b.1 design) is applied by
    the service layer, not here — this returns the raw daily rows only."""
    ensure_sector_regime_history_table()
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT snapshot_date, sectors, regime_us, regime_uk
                FROM sector_regime_history
                WHERE portfolio_id = %s
                AND snapshot_date >= CURRENT_DATE - (%s || ' days')::interval
                ORDER BY snapshot_date ASC
            """, (portfolio_id, weeks * 7))
            return cur.fetchall()


# ============================================================================
# SIGNALS FUNCTIONS
# ============================================================================

# BLG-SEC-02: ticker/market strings are interpolated into AI prompts (daily
# briefing, chat) downstream of signal writes. Sanitise at write time so no
# unvalidated value from an upstream data source (screener, ticker universe)
# reaches the signals table. Allow '.', '-', '/', ':' for international
# ticker formats (e.g. "VOD.L"); strip everything else; cap at 12 chars.
_SIGNAL_STRING_DISALLOWED = re.compile(r'[^A-Za-z0-9.\-/:]')
_SIGNAL_STRING_MAX_LEN = 12


def _sanitize_signal_string(value: str) -> str:
    if value is None:
        return value
    cleaned = _SIGNAL_STRING_DISALLOWED.sub('', str(value))
    return cleaned[:_SIGNAL_STRING_MAX_LEN]


def create_signal(portfolio_id: str, signal_data: Dict) -> Dict:
    """Create or update a signal"""
    ticker = _sanitize_signal_string(signal_data['ticker'])
    market = _sanitize_signal_string(signal_data['market'])
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO signals (
                    portfolio_id, ticker, market, signal_date, rank,
                    momentum_percent, current_price, price_gbp, atr_value,
                    volatility, initial_stop, suggested_shares, allocation_gbp,
                    total_cost, status, reason
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (portfolio_id, ticker, signal_date)
                DO UPDATE SET
                    rank = EXCLUDED.rank,
                    momentum_percent = EXCLUDED.momentum_percent,
                    current_price = EXCLUDED.current_price,
                    price_gbp = EXCLUDED.price_gbp,
                    atr_value = EXCLUDED.atr_value,
                    volatility = EXCLUDED.volatility,
                    initial_stop = EXCLUDED.initial_stop,
                    suggested_shares = EXCLUDED.suggested_shares,
                    allocation_gbp = EXCLUDED.allocation_gbp,
                    total_cost = EXCLUDED.total_cost,
                    reason = EXCLUDED.reason,
                    updated_at = NOW()
                RETURNING *
            """, (
                portfolio_id,
                ticker,
                market,
                signal_data['signal_date'],
                signal_data['rank'],
                signal_data['momentum_percent'],
                signal_data['current_price'],
                signal_data['price_gbp'],
                signal_data['atr_value'],
                signal_data['volatility'],
                signal_data['initial_stop'],
                signal_data['suggested_shares'],
                signal_data['allocation_gbp'],
                signal_data['total_cost'],
                signal_data.get('status', 'new'),
                signal_data.get('reason')
            ))
            return cur.fetchone()


def get_signals(portfolio_id: str, status: str = None) -> List[Dict]:
    """Get signals, optionally filtered by status"""
    with get_db() as conn:
        with conn.cursor() as cur:
            if status:
                cur.execute(
                    "SELECT * FROM signals WHERE portfolio_id = %s AND status = %s ORDER BY signal_date DESC, rank ASC",
                    (portfolio_id, status)
                )
            else:
                cur.execute(
                    "SELECT * FROM signals WHERE portfolio_id = %s ORDER BY signal_date DESC, rank ASC",
                    (portfolio_id,)
                )
            return cur.fetchall()


def get_signals_for_ticker(portfolio_id: str, ticker: str) -> List[Dict]:
    """Get signals for one portfolio+ticker, most recent first (ST-12,
    BLG-BE-94, EPIC-02, v8.8 — Pre-Trade Research View query-latency review).

    Targeted variant of get_signals() — avoids fetching every signal ever
    generated for the portfolio just to filter to one ticker in Python
    (routers/research.py's per-page-load lookup does exactly this today, an
    unbounded-growth query cost as the signals table accumulates history
    across screener runs). Uses idx_signals_portfolio for the portfolio_id
    predicate; the UPPER(ticker) predicate requires the functional index
    idx_signals_ticker_upper (added alongside this function, correcting
    this docstring's original — incorrect — claim that the existing plain
    idx_signals_ticker would serve: a plain index cannot satisfy a
    predicate that wraps the column in a function, per this codebase's own
    ST-10/BLG-BE-82 precedent for trade_plans/red_flag_events).
    Same ordering as get_signals() so callers that re-sort the result the
    same way select the identical row — this only reduces I/O, it does not
    change selection semantics.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM signals WHERE portfolio_id = %s AND UPPER(ticker) = UPPER(%s) "
                "ORDER BY signal_date DESC, rank ASC",
                (portfolio_id, ticker)
            )
            return cur.fetchall()


# BLG-SEC-08: dict keys passed to update_signal() are spliced directly into the
# SQL UPDATE statement as column names (parameterization only covers values,
# not identifiers) — an unvalidated key is a SQL-injection-adjacent arbitrary
# column write. This is the full set of signals columns a client update may
# legitimately target; id/portfolio_id/created_at/updated_at are excluded.
SIGNAL_UPDATABLE_COLUMNS = frozenset({
    "ticker", "market", "signal_date", "rank", "momentum_percent",
    "current_price", "price_gbp", "atr_value", "volatility", "initial_stop",
    "suggested_shares", "allocation_gbp", "total_cost", "status", "reason",
})


def update_signal(signal_id: str, updates: Dict) -> Dict:
    """Update a signal.

    Raises:
        ValueError: If `updates` contains a key outside SIGNAL_UPDATABLE_COLUMNS
            (BLG-SEC-08 — see module-level comment above).
    """
    unknown_keys = set(updates) - SIGNAL_UPDATABLE_COLUMNS
    if unknown_keys:
        raise ValueError(f"Unrecognised signal field(s): {sorted(unknown_keys)}")

    with get_db() as conn:
        with conn.cursor() as cur:
            set_parts = []
            values = []

            for key, value in updates.items():
                # BLG-SEC-02: PATCH /signals/{id} is a second signal write path — ticker/market
                # must be sanitised here too, or the INSERT-time protection in create_signal()
                # is bypassed entirely.
                if key in ("ticker", "market"):
                    value = _sanitize_signal_string(value)
                set_parts.append(f"{key} = %s")
                values.append(value)
            
            values.append(signal_id)
            
            query = f"""
                UPDATE signals 
                SET {', '.join(set_parts)}, updated_at = NOW() 
                WHERE id = %s 
                RETURNING *
            """
            
            cur.execute(query, values)
            conn.commit()
            return cur.fetchone()


def delete_signal(signal_id: str):
    """Delete a signal"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM signals WHERE id = %s", (signal_id,))

def update_position_note(position_id: str, entry_note: str) -> Dict:
    """Update entry note for a position"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE positions 
                SET entry_note = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id, ticker, entry_note
            """, (entry_note, position_id))
            
            result = cur.fetchone()
            
            if not result:
                raise ValueError(f"Position {position_id} not found")
            
            return {
                "id": str(result['id']),
                "ticker": result['ticker'],
                "entry_note": result['entry_note'],
                "updated_at": datetime.now().isoformat()
            }


def update_position_tags(position_id: str, tags: List[str]) -> Dict:
    """Update tags for a position"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE positions 
                SET tags = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id, ticker, tags
            """, (tags, position_id))
            
            result = cur.fetchone()
            
            if not result:
                raise ValueError(f"Position {position_id} not found")
            
            return {
                "id": str(result['id']),
                "ticker": result['ticker'],
                "tags": result['tags'] or [],
                "updated_at": datetime.now().isoformat()
            }


def get_all_tags(portfolio_id: str) -> List[str]:
    """Get all unique tags used across positions and trade history"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT unnest(tags) as tag
                FROM (
                    SELECT tags FROM positions WHERE portfolio_id = %s
                    UNION ALL
                    SELECT tags FROM trade_history WHERE portfolio_id = %s
                ) combined
                WHERE tags IS NOT NULL
                ORDER BY tag
            """, (portfolio_id, portfolio_id))
            
            tags = [row['tag'] for row in cur.fetchall()]
            return tags


def search_positions_by_tags(portfolio_id: str, tags: List[str]) -> List[Dict]:
    """Search positions by tags (OR logic - any tag match)"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM positions
                WHERE portfolio_id = %s 
                AND tags && %s
                ORDER BY entry_date DESC
            """, (portfolio_id, tags))
            
            positions = cur.fetchall()
            return [dict(p) for p in positions]

# ---------------------------------------------------------------------------
# Current Drawdown: peak portfolio value query
# ---------------------------------------------------------------------------

def get_peak_portfolio_value(portfolio_id: str, conn=None) -> float:
    """
    Return the all-time peak total_value from portfolio_history for
    this portfolio. Returns 0.0 when no snapshots exist.

    All-time means across ALL portfolio_history records — not
    period-scoped. This is the correct behaviour per
    metrics_definitions.md v1.5.8 §Implementation Note and
    portfolio_endpoints.md v1.8.2 §peak_portfolio_value field note.

    If conn is provided, reuses it instead of opening a new connection.

    Returns:
        float: Peak total_value in GBP. 0.0 if no records exist.
    """
    def _run(cur):
        cur.execute(
            """
            SELECT COALESCE(MAX(total_value), 0.0) AS peak_value
            FROM portfolio_history
            WHERE portfolio_id = %s
            """,
            (portfolio_id,),
        )
        result = cur.fetchone()
        return float(result['peak_value'])

    if conn is not None:
        with conn.cursor() as cur:
            return _run(cur)
    with get_db() as conn:
        with conn.cursor() as cur:
            return _run(cur)


# ---------------------------------------------------------------------------
# CSV export: closed trade history query
# ---------------------------------------------------------------------------

def get_all_closed_trades_for_csv_export(portfolio_id: str) -> list:
    """
    Return all closed trades for the CSV export endpoint, ordered
    by exit_date descending (newest first).

    Selects exactly the 14 fields required by the CSV column spec in
    trade_endpoints.md v1.8.4. No business logic — caller handles
    serialisation.

    Returns:
        list[dict]: List of trade dicts. Empty list if no closed trades.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ticker,
                    market,
                    entry_date,
                    exit_date,
                    shares,
                    entry_price,
                    exit_price,
                    pnl,
                    pnl_pct,
                    holding_days,
                    exit_reason,
                    tags,
                    entry_note,
                    exit_note
                FROM trade_history
                WHERE portfolio_id = %s
                ORDER BY exit_date DESC
                """,
                (portfolio_id,),
            )
            rows = cur.fetchall()
            return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# Trade reflections — ST-02, EPIC-01, v1.9
# Spec: docs/specs/frontend/pages/trade_reflection.md §7
# Schema: docs/specs/data_model.md §v1.8
# ---------------------------------------------------------------------------

def get_trade_reflection(trade_id: str) -> Optional[Dict]:
    """
    Retrieve an existing reflection for a closed trade.

    Returns:
        dict with reflection fields, or None if no reflection saved yet.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, trade_id, trade_rationale, what_worked,
                       what_didnt_work, discipline_assessment, key_takeaway,
                       created_at, updated_at
                FROM trade_reflections
                WHERE trade_id = %s
                """,
                (trade_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def upsert_trade_reflection(trade_id: str, data: Dict) -> Dict:
    """
    Create or update a trade reflection (upsert on trade_id unique constraint).

    Args:
        trade_id: UUID of the trade_history record.
        data: dict with any subset of the five reflection text fields.

    Returns:
        The full reflection row after upsert.

    Raises:
        ValueError: if trade_id does not exist in trade_history.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            # Guard: confirm the trade record exists before writing reflection
            cur.execute(
                "SELECT id FROM trade_history WHERE id = %s",
                (trade_id,),
            )
            if cur.fetchone() is None:
                raise ValueError(f"Trade '{trade_id}' not found in trade_history")

            cur.execute(
                """
                INSERT INTO trade_reflections (
                    trade_id, trade_rationale, what_worked, what_didnt_work,
                    discipline_assessment, key_takeaway
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (trade_id) DO UPDATE SET
                    trade_rationale       = EXCLUDED.trade_rationale,
                    what_worked           = EXCLUDED.what_worked,
                    what_didnt_work       = EXCLUDED.what_didnt_work,
                    discipline_assessment = EXCLUDED.discipline_assessment,
                    key_takeaway          = EXCLUDED.key_takeaway,
                    updated_at            = NOW()
                RETURNING id, trade_id, trade_rationale, what_worked,
                          what_didnt_work, discipline_assessment, key_takeaway,
                          created_at, updated_at
                """,
                (
                    trade_id,
                    data.get("trade_rationale"),
                    data.get("what_worked"),
                    data.get("what_didnt_work"),
                    data.get("discipline_assessment"),
                    data.get("key_takeaway"),
                ),
            )
            return dict(cur.fetchone())


# ---------------------------------------------------------------------------
# Trade Plans (DS-04 / ST-02, v3.1)
# ---------------------------------------------------------------------------

def ensure_trade_plans_table():
    """Create trade_plans table if it does not exist (idempotent)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trade_plans (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL,
                    position_id UUID,
                    ticker VARCHAR(20) NOT NULL,
                    market VARCHAR(10) NOT NULL CHECK (market IN ('US', 'UK')),
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    setup_type VARCHAR(50),
                    setup_thesis TEXT,
                    entry_rationale TEXT,
                    regime_context_at_entry TEXT,
                    r_target NUMERIC(8,2),
                    early_exit_conditions TEXT,
                    confirmation_criteria TEXT,
                    checklist_completed BOOLEAN NOT NULL DEFAULT FALSE,
                    checklist_items JSONB NOT NULL DEFAULT '[]'::JSONB,
                    status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'closed')),
                    pre_entry_override_acknowledged BOOLEAN,
                    thesis_feedback VARCHAR(20) CHECK (thesis_feedback IN ('useful', 'not_useful'))
                )
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trade_plans_portfolio ON trade_plans(portfolio_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trade_plans_position ON trade_plans(position_id) WHERE position_id IS NOT NULL")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trade_plans_status ON trade_plans(status)")
            # ST-10 (BLG-BE-82, EPIC-03, v8.4): functional index matching get_trade_plans()'s
            # actual WHERE UPPER(ticker)=%s predicate. The plain (non-functional) idx_trade_plans_ticker
            # documented in data_model.md's canonical schema would not be used by this predicate --
            # matches the sibling red_flag_events.idx_rfe_ticker pattern (also UPPER(ticker)).
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trade_plans_ticker_upper ON trade_plans (UPPER(ticker))")
        conn.commit()
    ensure_regime_context_text_column()
    ensure_trade_plan_tags_column()
    ensure_thesis_provenance_columns()
    ensure_invalidation_condition_column()
    ensure_is_ai_draft_column()


def create_trade_plan(portfolio_id: str, data: dict) -> dict:
    with get_db() as conn:
        with conn.cursor() as cur:
            _json = __import__("json").dumps
            cur.execute(
                """INSERT INTO trade_plans
                   (portfolio_id, position_id, ticker, market, setup_type, setup_thesis, entry_rationale,
                    regime_context_at_entry, r_target, early_exit_conditions, confirmation_criteria,
                    checklist_completed, checklist_items, status, pre_entry_override_acknowledged,
                    thesis_feedback,
                    planned_quantity, planned_entry_price, planned_stop_price,
                    signal_id, risk_percent_used, portfolio_value_at_entry,
                    pre_entry_validation_snapshot, effective_settings_snapshot, trade_tags,
                    strategy_version_at_entry, thesis_model_version, thesis_prompt_version,
                    invalidation_condition, is_ai_draft, triggered_by_price_alert_id)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb,%s,%s,%s,%s,%s,%s,%s)
                   RETURNING *""",
                (
                    portfolio_id,
                    data.get("position_id"),
                    data["ticker"],
                    data["market"],
                    data.get("setup_type"),
                    data.get("setup_thesis"),
                    data.get("entry_rationale"),
                    data.get("regime_context_at_entry"),
                    data.get("r_target"),
                    data.get("early_exit_conditions"),
                    data.get("confirmation_criteria"),
                    data.get("checklist_completed", False),
                    _json(data.get("checklist_items", [])),
                    data.get("status", "draft"),
                    data.get("pre_entry_override_acknowledged"),
                    data.get("thesis_feedback"),
                    data.get("planned_quantity"),
                    data.get("planned_entry_price"),
                    data.get("planned_stop_price"),
                    data.get("signal_id"),
                    data.get("risk_percent_used"),
                    data.get("portfolio_value_at_entry"),
                    _json(data["pre_entry_validation_snapshot"]) if data.get("pre_entry_validation_snapshot") is not None else None,
                    _json(data["effective_settings_snapshot"]) if data.get("effective_settings_snapshot") is not None else None,
                    data.get("trade_tags") or [],
                    data.get("strategy_version_at_entry"),
                    # ST-12 (BLG-BE-70, EPIC-03, v8.4): frontend-passed, nullable -- present only
                    # when setup_thesis/entry_rationale etc. were populated from the
                    # generate-plan/generate-thesis AI response and saved as-is (not user-edited).
                    data.get("thesis_model_version"),
                    data.get("thesis_prompt_version"),
                    data.get("invalidation_condition"),
                    bool(data.get("is_ai_draft")),
                    data.get("triggered_by_price_alert_id"),
                ),
            )
            row = cur.fetchone()
        conn.commit()
        return dict(row)


def get_trade_plans(
    portfolio_id: str, status: str = None, ticker: str = None,
    cursor: str = None, limit: int = None,
) -> list:
    """cursor/limit are additive and opt-in (ST-17, BLG-BE-47 — canonical
    cursor pagination pattern, backend_engineering_patterns.md). When both
    are None (the default), behaviour is byte-for-byte identical to before
    this pattern existed: no LIMIT clause, full result set, unchanged query
    shape. When limit is provided, fetches limit + 1 rows so the caller
    (via utils/pagination.py::paginate_results) can determine whether a
    next page exists without a separate COUNT query."""
    from utils.pagination import cursor_where_clause

    with get_db() as conn:
        with conn.cursor() as cur:
            clauses = ["portfolio_id=%s"]
            params = [portfolio_id]
            if status:
                clauses.append("status=%s")
                params.append(status)
            if ticker:
                clauses.append("UPPER(ticker)=%s")
                params.append(ticker.upper())
            if limit is not None:
                cursor_clause, cursor_params = cursor_where_clause(cursor)
                if cursor_clause:
                    clauses.append(cursor_clause)
                    params.extend(cursor_params)
            where = " AND ".join(clauses)
            order_by = "created_at DESC, id DESC" if limit is not None else "created_at DESC"
            query = f"SELECT * FROM trade_plans WHERE {where} ORDER BY {order_by}"
            if limit is not None:
                query += " LIMIT %s"
                params.append(limit + 1)
            cur.execute(query, params)
            return [dict(r) for r in cur.fetchall()]


def get_trade_plan_by_id(trade_plan_id: str, portfolio_id: str) -> dict:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM trade_plans WHERE id=%s AND portfolio_id=%s",
                (trade_plan_id, portfolio_id),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def update_trade_plan(trade_plan_id: str, portfolio_id: str, data: dict) -> dict:
    allowed = {
        "position_id", "setup_type", "setup_thesis", "entry_rationale", "regime_context_at_entry",
        "r_target", "early_exit_conditions", "confirmation_criteria",
        "checklist_completed", "checklist_items", "status", "abandonment_reason",
        "pre_entry_override_acknowledged", "thesis_feedback",
        "planned_quantity", "planned_entry_price", "planned_stop_price",
        "trade_tags", "thesis_model_version", "thesis_prompt_version",
        "invalidation_condition", "is_ai_draft",
    }
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return get_trade_plan_by_id(trade_plan_id, portfolio_id)

    # ST-13 (BLG-BE-77, EPIC-03, v8.4): capture before-state so post-entry
    # edits can be audit-logged. Cheap single-row lookup; None if the plan
    # doesn't exist (the UPDATE below then affects 0 rows, unchanged
    # behaviour from before this story).
    before_plan = get_trade_plan_by_id(trade_plan_id, portfolio_id)

    set_clauses = []
    values = []
    for k, v in fields.items():
        if k == "checklist_items":
            set_clauses.append(f"{k} = %s::jsonb")
            values.append(__import__("json").dumps(v))
        else:
            set_clauses.append(f"{k} = %s")
            values.append(v)
    set_clauses.append("updated_at = NOW()")
    values.extend([trade_plan_id, portfolio_id])
    sql = f"UPDATE trade_plans SET {', '.join(set_clauses)} WHERE id=%s AND portfolio_id=%s RETURNING *"
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, values)
            row = cur.fetchone()
        conn.commit()
        after_plan = dict(row) if row else None

    # ST-13 (BLG-BE-77, EPIC-03, v8.4): audit-trail pattern extended from
    # position_audit_log (BLG-BE-73) to trade plan mutations post-entry —
    # "post-entry" means the plan is linked to a position (position_id set).
    # Pre-entry edits to a draft plan are ordinary iterative authoring, not
    # logged. Non-blocking: a logging failure never affects the edit itself.
    if after_plan and before_plan and (before_plan.get("position_id") or after_plan.get("position_id")):
        for field_name in fields:
            if field_name == "checklist_items":
                continue  # structural field, not a meaningful single-value diff
            before_val = before_plan.get(field_name)
            after_val = after_plan.get(field_name)
            if before_val != after_val:
                create_trade_plan_audit_log_entry(
                    trade_plan_id, "post-entry-edit", field_name, before_val, after_val,
                )

    return after_plan


def delete_trade_plan(trade_plan_id: str, portfolio_id: str) -> bool:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM trade_plans WHERE id=%s AND portfolio_id=%s",
                (trade_plan_id, portfolio_id),
            )
            deleted = cur.rowcount > 0
        conn.commit()
        return deleted


def get_trade_plans_by_position(position_id: str, portfolio_id: str) -> list:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM trade_plans WHERE position_id=%s AND portfolio_id=%s ORDER BY created_at DESC",
                (position_id, portfolio_id),
            )
            return [dict(r) for r in cur.fetchall()]


_TRADE_PLAN_BULK_MAX_IDS = 100


def bulk_tag_trade_plans(portfolio_id: str, ids: list, tags: list) -> dict:
    """
    Add tags to each selected trade plan's existing trade_tags (union, not replace).
    Returns {succeeded: [ids], failed: [{id, reason}]} (ST-03, BLG-FE-117, EPIC-03, v7.5).
    Caller (router) is responsible for validating/cleaning `tags` via _validate_trade_tags.
    """
    if not ids:
        raise ValueError("ids must be a non-empty array")
    if len(ids) > _TRADE_PLAN_BULK_MAX_IDS:
        raise ValueError(f"ids exceeds the maximum batch size ({_TRADE_PLAN_BULK_MAX_IDS})")

    succeeded, failed = [], []
    with get_db() as conn:
        with conn.cursor() as cur:
            for plan_id in ids:
                cur.execute(
                    "SELECT trade_tags FROM trade_plans WHERE id = %s AND portfolio_id = %s",
                    (plan_id, portfolio_id),
                )
                row = cur.fetchone()
                if not row:
                    failed.append({"id": plan_id, "reason": "not_found"})
                    continue
                existing = list(row["trade_tags"]) if row.get("trade_tags") else []
                merged = existing[:]
                for t in tags:
                    if t not in merged:
                        merged.append(t)
                merged = merged[:10]
                cur.execute(
                    "UPDATE trade_plans SET trade_tags = %s, updated_at = NOW() WHERE id = %s AND portfolio_id = %s",
                    (merged, plan_id, portfolio_id),
                )
                succeeded.append(plan_id)
        conn.commit()

    return {"succeeded": succeeded, "failed": failed}


def bulk_archive_trade_plans(portfolio_id: str, ids: list, abandonment_reason: str) -> dict:
    """
    Archive (abandon) each selected trade plan. Plans with status='active' are
    excluded (mirrors the single-item Abandon button's hide rule, trade_plan.md
    §8.1) and reported in `failed` with reason 'active_status_excluded'.
    Returns {succeeded: [ids], failed: [{id, reason}]}.
    """
    if not ids:
        raise ValueError("ids must be a non-empty array")
    if len(ids) > _TRADE_PLAN_BULK_MAX_IDS:
        raise ValueError(f"ids exceeds the maximum batch size ({_TRADE_PLAN_BULK_MAX_IDS})")

    succeeded, failed = [], []
    with get_db() as conn:
        with conn.cursor() as cur:
            for plan_id in ids:
                cur.execute(
                    "SELECT status FROM trade_plans WHERE id = %s AND portfolio_id = %s",
                    (plan_id, portfolio_id),
                )
                row = cur.fetchone()
                if not row:
                    failed.append({"id": plan_id, "reason": "not_found"})
                    continue
                if row["status"] == "active":
                    failed.append({"id": plan_id, "reason": "active_status_excluded"})
                    continue
                cur.execute(
                    """UPDATE trade_plans
                       SET status = 'abandoned', abandonment_reason = %s, updated_at = NOW()
                       WHERE id = %s AND portfolio_id = %s""",
                    (abandonment_reason, plan_id, portfolio_id),
                )
                succeeded.append(plan_id)
        conn.commit()

    return {"succeeded": succeeded, "failed": failed}


def bulk_delete_trade_plans(portfolio_id: str, ids: list) -> dict:
    """Delete each selected trade plan. Returns {succeeded, failed} per-row."""
    if not ids:
        raise ValueError("ids must be a non-empty array")
    if len(ids) > _TRADE_PLAN_BULK_MAX_IDS:
        raise ValueError(f"ids exceeds the maximum batch size ({_TRADE_PLAN_BULK_MAX_IDS})")

    succeeded, failed = [], []
    with get_db() as conn:
        with conn.cursor() as cur:
            for plan_id in ids:
                cur.execute(
                    "DELETE FROM trade_plans WHERE id = %s AND portfolio_id = %s RETURNING id",
                    (plan_id, portfolio_id),
                )
                if cur.fetchone() is None:
                    failed.append({"id": plan_id, "reason": "not_found"})
                else:
                    succeeded.append(plan_id)
        conn.commit()

    return {"succeeded": succeeded, "failed": failed}


def get_unlinked_trade_plan_for_entry(portfolio_id: str, ticker: str, market: str) -> Optional[Dict]:
    """Find the most recent not-yet-linked trade plan for a ticker/market (BLG-BE-46).

    Used by add_position() to auto-link a newly entered position back to the
    draft plan it was entered from — the pre-trade planning flow (TradePlan.js)
    and the position-entry flow (TradeEntry.js) are separate pages with no
    explicit hand-off, so position_id was never populated on trade_plans in
    production. Matches on ticker+market with position_id still NULL and status
    still in a pre-entry state; excludes 'active', 'closed', 'abandoned' plans.
    """
    ticker_upper = ticker.upper()
    ticker_bare = ticker_upper[:-2] if ticker_upper.endswith(".L") else ticker_upper
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM trade_plans
                   WHERE portfolio_id=%s
                     AND (UPPER(ticker)=%s OR UPPER(ticker)=%s)
                     AND market=%s
                     AND position_id IS NULL
                     AND status NOT IN ('active', 'closed', 'abandoned')
                   ORDER BY created_at DESC LIMIT 1""",
                (portfolio_id, ticker_bare, ticker_bare + ".L", market),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def get_position_by_id(position_id: str) -> Optional[Dict]:
    """Fetch a single position by its UUID."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM positions WHERE id = %s", (position_id,))
            row = cur.fetchone()
            return dict(row) if row else None


def update_position_lifecycle_state(
    position_id: str,
    state: str,
    entered_at,
    history: list,
) -> Optional[Dict]:
    """Persist a lifecycle state transition on a position.

    Uses %s::jsonb cast because psycopg2 does not auto-cast list → JSONB.
    """
    import json as _json
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE positions
                   SET position_state = %s,
                       state_entered_at = %s,
                       state_history = %s::jsonb,
                       updated_at = NOW()
                   WHERE id = %s
                   RETURNING *""",
                (state, entered_at, _json.dumps(history), position_id),
            )
            row = cur.fetchone()
        conn.commit()
        return dict(row) if row else None


def ensure_lifecycle_columns():
    """Add position_state, state_entered_at, state_history columns to positions (idempotent).

    v2.6 migration — DS-05. All nullable except state_history which defaults to '[]'.
    Reversible: DROP COLUMN IF EXISTS position_state, state_entered_at, state_history.
    Spec: docs/specs/data_model.md §Migration v2.6
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE positions ADD COLUMN IF NOT EXISTS position_state VARCHAR(20)"
            )
            cur.execute(
                "ALTER TABLE positions ADD COLUMN IF NOT EXISTS state_entered_at TIMESTAMP WITHOUT TIME ZONE"
            )
            cur.execute(
                "ALTER TABLE positions ADD COLUMN IF NOT EXISTS state_history JSONB NOT NULL DEFAULT '[]'::JSONB"
            )
        conn.commit()


def ensure_last_reviewed_at_column():
    """Add last_reviewed_at column to positions (idempotent).

    ST-15 (BLG-FEAT-68, EPIC-03, v7.0) — position review cadence nudge.
    Nullable TIMESTAMP WITH TIME ZONE; null means "never reviewed".
    Reversible: DROP COLUMN IF EXISTS last_reviewed_at.
    Spec: docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE positions ADD COLUMN IF NOT EXISTS last_reviewed_at TIMESTAMP WITH TIME ZONE"
            )
        conn.commit()


def mark_position_reviewed(position_id: str) -> dict:
    """Set last_reviewed_at = NOW() for the given position (ST-15, BLG-FEAT-68).

    Returns the updated position row, or None if the position does not exist.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE positions SET last_reviewed_at = NOW() WHERE id = %s RETURNING id, last_reviewed_at",
                (position_id,),
            )
            row = cur.fetchone()
        conn.commit()
    return dict(row) if row else None


def ensure_plan_vs_reality_columns():
    """Add plan_vs_reality JSONB to trade_history and planned_stop_price to trade_plans (idempotent).

    PO-01 migration — ST-05 (EPIC-02, v3.5).
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS plan_vs_reality JSONB"
            )
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS planned_stop_price NUMERIC(20, 6)"
            )
        conn.commit()


def ensure_setup_type_column():
    """Add setup_type VARCHAR(50) to trade_plans table (idempotent).

    ST-06 (EPIC-03, v3.8) — BLG-FEAT-23.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS setup_type VARCHAR(50)"
            )
        conn.commit()


def ensure_triggered_by_price_alert_id_column():
    """Add triggered_by_price_alert_id UUID to trade_plans table (idempotent).

    ST-09 (BLG-BE-84, EPIC-02, v8.8) — real alert-to-trade provenance.
    Nullable; set only when a trade plan is created via the
    alert-notification-to-trade-plan UI path (routers/trade_plans.py
    create_plan()). No FK constraint — matches this codebase's existing
    convention for optional linkage columns (e.g. signal_id) of not
    cascading, so a plan's provenance record survives independently of the
    price_alerts row's own lifecycle. Reporting treatment: a separate field
    rather than a third trade_origin value — see data_model.md DS-14 for
    the reasoning.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS triggered_by_price_alert_id UUID"
            )
        conn.commit()


def ensure_override_acknowledged_column():
    """Add pre_entry_override_acknowledged BOOLEAN to trade_plans table (idempotent).

    ST-03 (EPIC-01, v3.8) — SI-01 pre-entry advisory panel override flag.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS pre_entry_override_acknowledged BOOLEAN"
            )
        conn.commit()


def ensure_regime_context_text_column():
    """Widen regime_context_at_entry from VARCHAR(50) to TEXT (idempotent).

    AI-generated regime context is a full sentence; VARCHAR(50) is too short.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ALTER COLUMN regime_context_at_entry TYPE TEXT"
            )
        conn.commit()


def ensure_thesis_provenance_columns():
    """Add thesis_model_version/thesis_prompt_version to trade_plans (idempotent).

    ST-12 (BLG-BE-70, EPIC-03, v8.4) -- AI Compliance & Governance Officer
    finding: gemini_service.generate_full_plan()/generate_setup_thesis()
    already return model_version/prompt_version to the caller and log them
    to gemini_audit_log keyed by plan_id, but the *stored* trade_plans row
    itself carried no provenance -- retroactive audit required a fragile
    join via plan_id (often null at generate-plan time, before a plan
    exists). Nullable, no backfill -- existing rows unaffected.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS thesis_model_version VARCHAR(50)"
            )
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS thesis_prompt_version VARCHAR(20)"
            )
        conn.commit()


def ensure_invalidation_condition_column():
    """Add invalidation_condition TEXT to trade_plans (idempotent).

    ST-01 (BLG-FEAT-84, EPIC-01, v8.7) -- optional, manually-authored
    "what would prove this thesis wrong?" field, trade_plan.md §5.1.
    Nullable, no backfill -- existing rows unaffected.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS invalidation_condition TEXT"
            )
        conn.commit()


def ensure_is_ai_draft_column():
    """Add is_ai_draft BOOLEAN to trade_plans (idempotent).

    ST-03 (BLG-BE-95, EPIC-01, v8.7) -- persists the AI-origin flag server-side
    so TradeEntry.js's Setup Thesis Digest panel (trade_plan.md §10.5) can show
    the "AI draft" badge for a *linked* plan, not just the plan's own editor
    session (client-only isAiDraft state was never persisted -- DEV-v8.6-ST02-01).
    Default false, nullable-equivalent, no backfill -- existing rows read false.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS is_ai_draft BOOLEAN NOT NULL DEFAULT FALSE"
            )
        conn.commit()


def ensure_thesis_feedback_column():
    """Add thesis_feedback VARCHAR(20) to trade_plans table (idempotent).

    ST-07 (EPIC-03, v6.5, BLG-FE-46) — Claude thesis generation feedback mechanism.
    Nullable; 'useful' | 'not_useful'. Feeds ST-08's thesis_adoption_rate metric.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS thesis_feedback VARCHAR(20)"
            )
        conn.commit()


def ensure_signals_ticker_upper_index():
    """Add a functional index on UPPER(ticker) to signals (idempotent).

    ST-12 (BLG-BE-94, EPIC-02, v8.8) — Head-of-Engineering-review correction
    (agent-mediated §5.3): get_signals_for_ticker()'s query predicate is
    `WHERE ... AND UPPER(ticker) = UPPER(%s)`. The existing idx_signals_ticker
    is a plain (non-functional) index on the bare ticker column and is not
    usable by a predicate that wraps the column in UPPER() — same class of
    gap already documented and fixed for trade_plans/red_flag_events
    (ST-10, BLG-BE-82, EPIC-03, v8.4 — see idx_trade_plans_ticker_upper
    above and idx_rfe_ticker below). Without this, get_signals_for_ticker()
    still requires a scan filtered row-by-row on UPPER(ticker) rather than
    an index scan, undermining the point of the targeted query.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_signals_ticker_upper ON signals (UPPER(ticker))"
            )
        conn.commit()


def ensure_signals_watchlisted_status():
    """Extend signals_status_check constraint to include 'watchlisted' (idempotent).

    ST-01 (EPIC-01, v3.7) — BLG-FE-33. Drops the existing CHECK constraint and
    recreates it with 'watchlisted' added. Safe to run multiple times.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE signals DROP CONSTRAINT IF EXISTS signals_status_check"
            )
            cur.execute(
                "ALTER TABLE signals ADD CONSTRAINT signals_status_check "
                "CHECK (status IN ('new', 'entered', 'dismissed', 'expired', 'already_held', 'watchlisted'))"
            )
        conn.commit()


def ensure_signals_allocation_insufficient_status():
    """Extend signals_status_check to include 'allocation_insufficient' (idempotent).

    ST-06 (EPIC-03, v5.0) — BLG-FEAT-43. Drops the existing CHECK constraint and
    recreates it with 'allocation_insufficient' added. Safe to run multiple times.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE signals DROP CONSTRAINT IF EXISTS signals_status_check"
            )
            cur.execute(
                "ALTER TABLE signals ADD CONSTRAINT signals_status_check "
                "CHECK (status IN ('new', 'entered', 'dismissed', 'expired', "
                "'already_held', 'watchlisted', 'allocation_insufficient'))"
            )
        conn.commit()


def ensure_signals_reason_column():
    """Add nullable reason column to signals table (idempotent).

    ST-06 (EPIC-03, v5.0) — BLG-FEAT-43. Stores human-readable explanation
    for allocation_insufficient signals. Nullable; existing rows default NULL.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE signals ADD COLUMN IF NOT EXISTS reason TEXT"
            )
        conn.commit()


def ensure_positions_user_fill_price_column():
    """Add user_fill_price to positions (idempotent).

    Slippage tracking migration — stores the user-provided actual fill price.
    Nullable; existing records default null.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE positions ADD COLUMN IF NOT EXISTS user_fill_price NUMERIC(10, 4)"
            )
        conn.commit()


def ensure_trade_history_fill_price_column():
    """Add fill_price to trade_history (idempotent).

    v1.9→v2.0 migration — slippage tracking. Copied from positions.user_fill_price at exit.
    Nullable; existing records default null.
    Spec: docs/specs/data_model.md §Migration v2.0
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS fill_price NUMERIC(10, 4)"
            )
        conn.commit()


def ensure_planned_entry_price_column():
    """Add planned_entry_price to trade_history (idempotent).

    Arc 4 PO-01 migration — ST-01 (EPIC-01, v3.6). Nullable; existing records default null.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS planned_entry_price NUMERIC(20, 6)"
            )
        conn.commit()


def ensure_trade_plan_pre_entry_columns():
    """Add planned_quantity and planned_entry_price to trade_plans (idempotent).

    Persists pre-entry check inputs so they survive save/reload cycles.
    planned_stop_price already exists (ensure_plan_vs_reality_columns).
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS planned_quantity INTEGER"
            )
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS planned_entry_price NUMERIC(20, 6)"
            )
        conn.commit()


def ensure_settings_concentration_columns():
    """Add concentration threshold columns to settings (idempotent).

    Allows users to configure position and sector concentration limits
    via the Settings page rather than relying on hardcoded defaults.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE settings ADD COLUMN IF NOT EXISTS "
                "concentration_position_threshold_pct NUMERIC(5, 2)"
            )
            cur.execute(
                "ALTER TABLE settings ADD COLUMN IF NOT EXISTS "
                "concentration_sector_threshold_pct NUMERIC(5, 2)"
            )
        conn.commit()


def get_trade_by_id(trade_id: str) -> Optional[Dict]:
    """Fetch a single trade_history record by its UUID."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM trade_history WHERE id = %s", (trade_id,))
            row = cur.fetchone()
            return dict(row) if row else None


def ensure_trade_cost_columns() -> None:
    """Add commission_gbp and spread_cost_gbp columns to trade_history (idempotent).

    ST-03 (EPIC-02, v6.0) — BLG-FEAT-20. Optional cost fields for net-of-costs
    R-multiple tracking. Nullable; existing records default NULL (backward-compatible).
    Spec: docs/specs/data_model.md §Migration v6.0
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS commission_gbp NUMERIC(10, 2)"
            )
            cur.execute(
                "ALTER TABLE trade_history ADD COLUMN IF NOT EXISTS spread_cost_gbp NUMERIC(10, 2)"
            )
        conn.commit()


def update_trade_costs(trade_id: str, portfolio_id: str, commission_gbp: Optional[float], spread_cost_gbp: Optional[float]) -> bool:
    """Update commission_gbp and spread_cost_gbp for a trade_history record.

    Returns True if a row was updated, False if trade not found.
    ST-03 (EPIC-02, v6.0) — BLG-FEAT-20.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE trade_history
                   SET commission_gbp = %s, spread_cost_gbp = %s
                   WHERE id = %s AND portfolio_id = %s""",
                (commission_gbp, spread_cost_gbp, trade_id, portfolio_id)
            )
            updated = cur.rowcount > 0
        conn.commit()
    return updated


def get_trade_history_with_stops(portfolio_id: str) -> List[Dict]:
    """Get trade history joined with positions.initial_stop for net-R computation.

    LEFT JOINs positions on position_id to add stop_price_at_entry.
    Records without a linked position have stop_price_at_entry = NULL.
    ST-03 (EPIC-02, v6.0) — BLG-FEAT-20.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT th.*, p.initial_stop AS stop_price_at_entry
                   FROM trade_history th
                   LEFT JOIN positions p ON th.position_id = p.id
                   WHERE th.portfolio_id = %s
                   ORDER BY th.exit_date DESC""",
                (portfolio_id,)
            )
            return cur.fetchall()


def get_database_size_bytes() -> int:
    """Return the current database size in bytes.

    Uses PostgreSQL's pg_database_size() to query the size of the current
    database. Called by the DB size monitoring service (BLG-OPS-09).
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pg_database_size(current_database()) AS size_bytes")
            row = cur.fetchone()
            return int(row["size_bytes"])


# ---------------------------------------------------------------------------
# Red Flag Events (SI-03 / ST-07, EPIC-03, v3.9)
# ---------------------------------------------------------------------------

_VALID_EVENT_TYPES = frozenset({
    "pre_entry_override",
    "checklist_skipped",
    "stop_prompt_dismissed",
    "drawdown_prompt_dismissed",
})


def ensure_red_flag_events_table() -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS red_flag_events (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    event_type TEXT NOT NULL,
                    ticker TEXT NOT NULL,
                    position_id UUID,
                    context JSONB,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )"""
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_rfe_event_type ON red_flag_events (event_type)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_rfe_ticker ON red_flag_events (UPPER(ticker))"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_rfe_created_at ON red_flag_events (created_at DESC)"
            )
        conn.commit()


def ensure_red_flag_events_severity_column() -> None:
    """Add severity column to red_flag_events and backfill defaults (idempotent).

    ST-09 (EPIC-03, v4.6) — BLG-BE-16. Adds severity VARCHAR(20) with values:
    info / warning / critical. Backfills: pre_entry_override events → 'warning';
    all other existing events → 'info'. Future SI-02 drift events → 'critical'
    (set at creation time, not backfilled here).
    Spec: docs/specs/api_contracts/portfolio_endpoints.md §GET /portfolio/red-flag-journal
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE red_flag_events ADD COLUMN IF NOT EXISTS severity VARCHAR(20) DEFAULT 'info'"
            )
            cur.execute(
                "UPDATE red_flag_events SET severity = 'warning' WHERE event_type = 'pre_entry_override' AND severity IS NULL"
            )
            cur.execute(
                "UPDATE red_flag_events SET severity = 'info' WHERE severity IS NULL"
            )
        conn.commit()


def ensure_pre_entry_validation_log_table() -> None:
    """Create pre_entry_validation_log table for ST-01 arc5-compliance metrics."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pre_entry_validation_log (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    ticker TEXT NOT NULL,
                    market TEXT NOT NULL DEFAULT 'US',
                    rule_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    validated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
            """)
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_pevl_rule_type ON pre_entry_validation_log (rule_type)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_pevl_validated_at ON pre_entry_validation_log (validated_at DESC)"
            )
        conn.commit()


def log_pre_entry_validation_results(
    ticker: str, market: str, checks: list
) -> None:
    """Log individual rule results to pre_entry_validation_log (fire-and-forget)."""
    try:
        ensure_pre_entry_validation_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                for check in checks:
                    rule_type = check.get("rule")
                    status = check.get("status")
                    if not rule_type or not status or status == "skipped":
                        continue
                    cur.execute(
                        """INSERT INTO pre_entry_validation_log (ticker, market, rule_type, status)
                           VALUES (%s, %s, %s, %s)""",
                        (ticker.upper(), market.upper(), rule_type, status),
                    )
            conn.commit()
    except Exception:
        pass  # fire-and-forget — never block the validation response


def ensure_trailing_stop_recommendation_log_table() -> None:
    """Create trailing_stop_recommendation_log table (ST-07, BLG-BE-50, v7.0).

    Captures every ATR-based trail-stop recommendation shown to the user
    (GET /positions/{id}/stop-trail), so trailing_stop_action_rate
    (docs/specs/metrics_definitions.md #Trailing Stop Action Rate) is
    computable — numerator/denominator joins each row here to the earliest
    subsequent PATCH /positions/{id} that set positions.stop_price >=
    recommended_stop within the capture window (24h, Product Owner-confirmed
    at sprint planning), using positions.updated_at as the PATCH timestamp.
    Same pattern as pre_entry_validation_log above.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trailing_stop_recommendation_log (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    position_id UUID NOT NULL REFERENCES positions(id),
                    current_stop_at_recommendation DECIMAL(10,4),
                    recommended_stop DECIMAL(10,4) NOT NULL,
                    recommended_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
            """)
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_tsrl_position_id ON trailing_stop_recommendation_log (position_id)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_tsrl_recommended_at ON trailing_stop_recommendation_log (recommended_at DESC)"
            )
        conn.commit()


def log_trailing_stop_recommendation(
    position_id: str, current_stop_at_recommendation, recommended_stop: float
) -> None:
    """Log one trail-stop recommendation event (fire-and-forget, ST-07/BLG-BE-50).

    Called once per GET /positions/{id}/stop-trail response — never blocks or
    fails the recommendation response itself.
    """
    try:
        ensure_trailing_stop_recommendation_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO trailing_stop_recommendation_log
                       (position_id, current_stop_at_recommendation, recommended_stop)
                       VALUES (%s, %s, %s)""",
                    (position_id, current_stop_at_recommendation, recommended_stop),
                )
            conn.commit()
    except Exception:
        pass  # fire-and-forget — never block the recommendation response


def create_red_flag_event(
    event_type: str,
    ticker: str,
    position_id: Optional[str] = None,
    context: Optional[dict] = None,
    severity: Optional[str] = None,
) -> dict:
    """Create a red flag event. severity defaults: pre_entry_override → 'warning'; others → 'info'."""
    import json as _json
    if severity is None:
        severity = "warning" if event_type == "pre_entry_override" else "info"
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO red_flag_events (event_type, ticker, position_id, context, severity)
                   VALUES (%s, %s, %s, %s::jsonb, %s)
                   RETURNING *""",
                (
                    event_type,
                    ticker.upper(),
                    position_id,
                    _json.dumps(context) if context is not None else None,
                    severity,
                ),
            )
            row = cur.fetchone()
        conn.commit()
        return dict(row)


def get_red_flag_events(
    page: int = 1,
    page_size: int = 20,
    event_type: Optional[str] = None,
    ticker: Optional[str] = None,
    since: Optional[str] = None,
    severity: Optional[str] = None,
) -> dict:
    """Fetch paginated red flag events. severity filter: info / warning / critical."""
    clauses = []
    params: list = []
    if event_type:
        clauses.append("event_type = %s")
        params.append(event_type)
    if ticker:
        clauses.append("UPPER(ticker) = %s")
        params.append(ticker.upper())
    if since:
        clauses.append("created_at >= %s::timestamptz")
        params.append(since)
    if severity:
        clauses.append("severity = %s")
        params.append(severity)
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    offset = (page - 1) * page_size
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) AS cnt FROM red_flag_events {where}", params)
            total = cur.fetchone()["cnt"]
            cur.execute(
                f"SELECT * FROM red_flag_events {where} ORDER BY created_at DESC LIMIT %s OFFSET %s",
                params + [page_size, offset],
            )
            items = [dict(r) for r in cur.fetchall()]
    return {"total": total, "page": page, "page_size": page_size, "items": items}


def ensure_gemini_audit_log_table() -> None:
    """Create gemini_audit_log table for ST-07 AI compliance audit trail."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS gemini_audit_log (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    plan_id UUID,
                    model_version TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    input_hash TEXT NOT NULL,
                    output_hash TEXT NOT NULL,
                    generated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    prompt_tokens INTEGER,
                    completion_tokens INTEGER,
                    total_tokens INTEGER,
                    estimated_cost_usd NUMERIC(12, 8)
                )
            """)
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_gal_generated_at ON gemini_audit_log (generated_at DESC)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_gal_plan_id ON gemini_audit_log (plan_id)"
            )
        conn.commit()


def create_gemini_audit_entry(
    plan_id: Optional[str],
    model_version: str,
    prompt_version: str,
    input_hash: str,
    output_hash: str,
    prompt_tokens: Optional[int] = None,
    completion_tokens: Optional[int] = None,
    total_tokens: Optional[int] = None,
    estimated_cost_usd: Optional[float] = None,
) -> None:
    """Append audit record for a Gemini thesis generation call (ST-07)."""
    try:
        ensure_gemini_audit_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO gemini_audit_log
                       (plan_id, model_version, prompt_version, input_hash, output_hash,
                        prompt_tokens, completion_tokens, total_tokens, estimated_cost_usd)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        plan_id,
                        model_version,
                        prompt_version,
                        input_hash,
                        output_hash,
                        prompt_tokens,
                        completion_tokens,
                        total_tokens,
                        estimated_cost_usd,
                    ),
                )
            conn.commit()
    except Exception:
        pass


def purge_gemini_audit_log_older_than_90_days() -> int:
    """Delete gemini_audit_log rows older than 90 days. Returns rows deleted."""
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM gemini_audit_log WHERE generated_at < NOW() - INTERVAL '90 days'"
                )
                deleted = cur.rowcount
            conn.commit()
        return deleted
    except Exception:
        return 0


def get_daily_ai_cost() -> dict:
    """Return today's Claude API spend total from gemini_audit_log."""
    try:
        ensure_gemini_audit_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        COALESCE(SUM(estimated_cost_usd), 0.0) AS total_cost,
                        COUNT(*) AS request_count
                    FROM gemini_audit_log
                    WHERE generated_at >= CURRENT_DATE
                """)
                row = cur.fetchone()
                return {
                    "total_cost_usd": float(row["total_cost"]),
                    "request_count": int(row["request_count"])
                }
    except Exception:
        return {"total_cost_usd": 0.0, "request_count": 0}


# ---------------------------------------------------------------------------
# claude_audit_log — immutable audit trail for Claude API calls
# ---------------------------------------------------------------------------

def ensure_claude_audit_log_table() -> None:
    """Create claude_audit_log table if it does not exist."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS claude_audit_log (
                    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    endpoint        TEXT NOT NULL,
                    model_id        TEXT NOT NULL,
                    prompt_version  TEXT NOT NULL,
                    input_tokens    INTEGER,
                    output_tokens   INTEGER,
                    cost_usd        NUMERIC(12, 8),
                    generated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
        conn.commit()


def create_claude_audit_entry(
    endpoint: str,
    model_id: str,
    prompt_version: str,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    cost_usd: float | None = None,
) -> None:
    """Insert one row into claude_audit_log. Non-blocking on failure."""
    try:
        ensure_claude_audit_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO claude_audit_log
                        (endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd),
                )
            conn.commit()
    except Exception:
        pass


def query_claude_audit_log(
    limit: int = 50,
    endpoint: str = None,
    date_from: str = None,
    date_to: str = None,
) -> list[dict]:
    """Return the most recent rows from claude_audit_log, newest first.

    ST-11 (BLG-BE-51, v7.0): optional server-side filters — `endpoint` (exact
    match) and `date_from`/`date_to` (inclusive, YYYY-MM-DD, applied to
    `generated_at`) — independently or combined. Existing unfiltered callers
    are unaffected (all three params default to None).
    """
    try:
        ensure_claude_audit_log_table()
        where_clauses = []
        params: list = []
        if endpoint is not None:
            where_clauses.append("endpoint = %s")
            params.append(endpoint)
        if date_from is not None:
            where_clauses.append("generated_at >= %s")
            params.append(date_from)
        if date_to is not None:
            where_clauses.append("generated_at < (%s::date + INTERVAL '1 day')")
            params.append(date_to)
        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
        params.append(limit)

        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT id, endpoint, model_id, prompt_version,
                           input_tokens, output_tokens, cost_usd, generated_at
                    FROM claude_audit_log
                    {where_sql}
                    ORDER BY generated_at DESC
                    LIMIT %s
                    """,
                    tuple(params),
                )
                rows = cur.fetchall()
                return [
                    {
                        "id": str(r["id"]),
                        "endpoint": r["endpoint"],
                        "model_id": r["model_id"],
                        "prompt_version": r["prompt_version"],
                        "input_tokens": r["input_tokens"],
                        "output_tokens": r["output_tokens"],
                        "cost_usd": float(r["cost_usd"]) if r["cost_usd"] is not None else None,
                        "generated_at": r["generated_at"].isoformat() if r["generated_at"] else None,
                    }
                    for r in rows
                ]
    except Exception:
        return []


# ---------------------------------------------------------------------------
# position_audit_log — audit trail for manual position overrides (ST-06,
# EPIC-06, v7.9, BLG-BE-73). Distinct from claude_audit_log (Claude API call
# accounting) and the AI-journal-generation audit trail (BLG-SEC-14, a
# different write path) — this table covers the three genuinely manual,
# user-initiated position edits that sit outside the automated trade
# lifecycle: note edit, tag edit, and mark-reviewed. Core trade/financial
# fields (entry_price, shares, stop, etc.) have no manual-override endpoint
# in this product and are out of scope — see decision record cited in
# data_model.md's migration entry for this table.
#
# No "who" column: this is a single-user product (no per-user identity
# concept exists anywhere else in this codebase — same precedent as
# claude_audit_log above, which also carries no user/actor field).
# ---------------------------------------------------------------------------

def ensure_position_audit_log_table() -> None:
    """Create position_audit_log table if it does not exist."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS position_audit_log (
                    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    position_id  UUID NOT NULL,
                    source       TEXT NOT NULL,
                    field        TEXT NOT NULL,
                    before_value TEXT,
                    after_value  TEXT,
                    changed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_position_audit_log_position_id
                ON position_audit_log(position_id)
            """)
        conn.commit()


def create_position_audit_log_entry(
    position_id: str,
    source: str,
    field: str,
    before_value,
    after_value,
) -> None:
    """Insert one row into position_audit_log. Non-blocking on failure —
    an audit-log write failure must never break the underlying position
    edit it is recording (same fail-open convention as
    create_claude_audit_entry above)."""
    try:
        ensure_position_audit_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO position_audit_log
                        (position_id, source, field, before_value, after_value)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (position_id, source, field, str(before_value), str(after_value)),
                )
            conn.commit()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# position_state_history — append-only log of lifecycle state transitions
# (ST-08, EPIC-02, v8.8, BLG-BE-58). Extends the position_audit_log pattern
# (above) to lifecycle state changes specifically. Complements — does not
# replace — the existing state_history JSONB column on positions
# (ensure_lifecycle_columns, v2.6 DS-05): the JSONB column is untouched (no
# behavioural change to compute_position_state()/refresh_position_lifecycle()'s
# existing logic) and this table is written alongside it on every genuine
# transition, giving a normalized, independently-queryable history separate
# from the per-row JSONB blob. Same no-"who"-column rationale (single-user
# product), same fail-open non-blocking write convention.
# ---------------------------------------------------------------------------

def ensure_position_state_history_table() -> None:
    """Create position_state_history table if it does not exist."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS position_state_history (
                    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    position_id  UUID NOT NULL,
                    from_state   VARCHAR(20),
                    to_state     VARCHAR(20) NOT NULL,
                    entered_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_position_state_history_position_id
                ON position_state_history(position_id)
            """)
        conn.commit()


def create_position_state_history_entry(
    position_id: str,
    from_state,
    to_state: str,
    entered_at,
) -> None:
    """Insert one row into position_state_history. Non-blocking on failure —
    an audit-log write failure must never break the underlying lifecycle
    state update it is recording (same fail-open convention as
    create_position_audit_log_entry above)."""
    try:
        ensure_position_state_history_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO position_state_history
                        (position_id, from_state, to_state, entered_at)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (position_id, from_state, to_state, entered_at),
                )
            conn.commit()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# trade_plan_audit_log — audit trail for trade plan edits post-entry (ST-13,
# EPIC-03, v8.4, BLG-BE-77). Extends the position_audit_log pattern
# (BLG-BE-73, above) to trade_plans: "post-entry" means the plan is linked
# to a position (position_id is set) at the time of the edit — pre-entry
# edits to a draft plan are ordinary, expected iterative authoring, not an
# audit-worthy mutation. Same schema shape, same no-"who"-column rationale
# (single-user product), same fail-open non-blocking write convention.
# ---------------------------------------------------------------------------

def ensure_trade_plan_audit_log_table() -> None:
    """Create trade_plan_audit_log table if it does not exist."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trade_plan_audit_log (
                    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    trade_plan_id UUID NOT NULL,
                    source        TEXT NOT NULL,
                    field         TEXT NOT NULL,
                    before_value  TEXT,
                    after_value   TEXT,
                    changed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_trade_plan_audit_log_trade_plan_id
                ON trade_plan_audit_log(trade_plan_id)
            """)
        conn.commit()


def create_trade_plan_audit_log_entry(
    trade_plan_id: str,
    source: str,
    field: str,
    before_value,
    after_value,
) -> None:
    """Insert one row into trade_plan_audit_log. Non-blocking on failure —
    an audit-log write failure must never break the underlying trade plan
    edit it is recording (same fail-open convention as
    create_position_audit_log_entry above)."""
    try:
        ensure_trade_plan_audit_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO trade_plan_audit_log
                        (trade_plan_id, source, field, before_value, after_value)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (trade_plan_id, source, field, str(before_value), str(after_value)),
                )
            conn.commit()
    except Exception:
        pass


def get_monthly_claude_cost() -> dict:
    """Return the current calendar month's Claude API spend total from claude_audit_log.

    ST-07 (EPIC-07, v7.6, BLG-FEAT-77 — reframed per ESC-EXEC-20260720-01):
    Claude is the only AI provider integrated in this codebase (see
    docs/specs/pnl_export_reconciliation.md-adjacent finding — no
    google-generativeai package, no GEMINI_API_KEY, gemini_service.py calls
    only the Anthropic API). claude_audit_log is the immutable audit trail
    and the authoritative cost source going forward.
    """
    try:
        ensure_claude_audit_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        COALESCE(SUM(cost_usd), 0.0) AS total_cost,
                        COUNT(*) AS request_count
                    FROM claude_audit_log
                    WHERE generated_at >= date_trunc('month', NOW())
                """)
                row = cur.fetchone()
                return {
                    "total_cost_usd": float(row["total_cost"]),
                    "request_count": int(row["request_count"]),
                }
    except Exception:
        return {"total_cost_usd": 0.0, "request_count": 0}


def get_claude_spend_between(start_date: str, end_date: str | None = None) -> float:
    """Sum claude_audit_log.cost_usd for [start_date, end_date) -- or
    [start_date, NOW()) when end_date is None (used for the most recent,
    still-open window).

    ST-06 (EPIC-06, v7.8, BLG-FEAT-82): backs the AI spend trend chart's
    per-release-cycle bucketing. start_date/end_date are 'YYYY-MM-DD' strings.
    """
    try:
        ensure_claude_audit_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                if end_date is not None:
                    cur.execute(
                        """
                        SELECT COALESCE(SUM(cost_usd), 0.0) AS total_cost
                        FROM claude_audit_log
                        WHERE generated_at >= %s AND generated_at < %s
                        """,
                        (start_date, end_date),
                    )
                else:
                    cur.execute(
                        """
                        SELECT COALESCE(SUM(cost_usd), 0.0) AS total_cost
                        FROM claude_audit_log
                        WHERE generated_at >= %s
                        """,
                        (start_date,),
                    )
                row = cur.fetchone()
                return float(row["total_cost"])
    except Exception:
        return 0.0


# ============================================================================
# DS-07 — SI-02 SCHEMA ADDITIONS (v4.6 ST-01)
# ============================================================================

def ensure_si02_trade_plans_columns():
    """Add 5 SI-02 nullable columns + P1 index to trade_plans (idempotent).

    DS-07 migration — v4.6 ST-01. All columns nullable; no backfill required.
    Reversible: DROP COLUMN signal_id, risk_percent_used, portfolio_value_at_entry,
    pre_entry_validation_snapshot, effective_settings_snapshot; DROP INDEX idx_trade_plans_signal.
    Note: idx_trade_plans_signal uses CREATE INDEX IF NOT EXISTS (not CONCURRENTLY) to allow
    execution inside a transaction at current data volumes. Use CONCURRENTLY outside a transaction
    in production for zero-downtime creation on large datasets.
    Spec: docs/specs/data_model/si02_data_schema.md §4–§5
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS signal_id UUID REFERENCES signals(id) ON DELETE SET NULL"
            )
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS risk_percent_used NUMERIC(4,2)"
            )
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS portfolio_value_at_entry NUMERIC(12,2)"
            )
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS pre_entry_validation_snapshot JSONB"
            )
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS effective_settings_snapshot JSONB"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_trade_plans_signal "
                "ON trade_plans(signal_id) WHERE signal_id IS NOT NULL"
            )
        conn.commit()


def ensure_strategy_version_at_entry_columns():
    """Add strategy_version_at_entry VARCHAR(10) to trade_plans and positions (idempotent).

    DS-11 migration — v8.0 ST-01 (EPIC-01, BLG-SPEC-78). Forward-only: populated by
    the caller at row-creation time from strategy_version_registry.get_current_strategy_version().
    No backfill of existing rows — historical attribution for trade_history remains the
    derived-window approach in strategy_version_registry.py (SI-04, v7.7 ST-01); this field
    is a direct, unambiguous stamp for rows created from v8.0 onward only.
    Spec: docs/specs/data_model.md DS-11.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS strategy_version_at_entry VARCHAR(10)"
            )
            cur.execute(
                "ALTER TABLE positions ADD COLUMN IF NOT EXISTS strategy_version_at_entry VARCHAR(10)"
            )
        conn.commit()


def ensure_trade_plan_tags_column():
    """Add trade_tags TEXT[] column to trade_plans (idempotent).

    ST-05 (BLG-FEAT-52) migration — v6.8 EPIC-02. Independent, data-only field
    from the existing positions.tags / trade_history.tags columns (no FK, no
    shared service). Nullable-equivalent default '{}'; no backfill required.
    Reversible: DROP COLUMN trade_tags.
    Spec: docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans ADD COLUMN IF NOT EXISTS trade_tags TEXT[] NOT NULL DEFAULT '{}'"
            )
        conn.commit()


def get_all_trade_plan_tags(portfolio_id: str) -> List[str]:
    """Get all unique tags used across trade_plans.trade_tags for a portfolio (ST-05)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT unnest(trade_tags) as tag
                FROM trade_plans
                WHERE portfolio_id = %s AND trade_tags IS NOT NULL
                ORDER BY tag
                """,
                (portfolio_id,),
            )
            return [row['tag'] for row in cur.fetchall()]


def get_tag_performance(portfolio_id: str, tags: List[str]) -> List[Dict]:
    """Win rate and average R-multiple per requested trade-plan tag (ST-05 AC-02).

    Joins trade_plans (trade_tags) to trade_history via position_id, then to
    positions for initial_stop to compute R-multiple using the same formula as
    GET /analytics/r-multiple-distribution: R = (exit - entry) / (entry - stop).
    Only closed trades (trade_history rows) linked to a plan carrying the tag
    are counted. No dependency on trade_annotations/PO-02 (ST-05 AC-04).
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tp.trade_tags, th.pnl, th.entry_price, th.exit_price, p.initial_stop
                FROM trade_plans tp
                JOIN trade_history th ON th.position_id = tp.position_id
                LEFT JOIN positions p ON p.id = th.position_id
                WHERE tp.portfolio_id = %s
                  AND tp.position_id IS NOT NULL
                  AND tp.trade_tags && %s
                """,
                (portfolio_id, tags),
            )
            rows = cur.fetchall()

    per_tag: Dict[str, Dict] = {tag: {"wins": 0, "count": 0, "r_values": []} for tag in tags}
    for row in rows:
        row_tags = set(row["trade_tags"] or [])
        pnl = float(row["pnl"]) if row["pnl"] is not None else 0.0
        entry = float(row["entry_price"]) if row["entry_price"] is not None else None
        exit_ = float(row["exit_price"]) if row["exit_price"] is not None else None
        stop = float(row["initial_stop"]) if row["initial_stop"] is not None else None
        r_value = None
        if entry is not None and exit_ is not None and stop is not None and entry > stop:
            r_value = (exit_ - entry) / (entry - stop)
        for tag in tags:
            if tag in row_tags:
                bucket = per_tag[tag]
                bucket["count"] += 1
                if pnl > 0:
                    bucket["wins"] += 1
                if r_value is not None:
                    bucket["r_values"].append(r_value)

    result = []
    for tag in tags:
        bucket = per_tag[tag]
        count = bucket["count"]
        win_rate = round(bucket["wins"] / count * 100, 1) if count else 0.0
        avg_r = round(sum(bucket["r_values"]) / len(bucket["r_values"]), 2) if bucket["r_values"] else None
        result.append({
            "tag": tag,
            "win_rate": win_rate,
            "avg_r_multiple": avg_r,
            "trade_count": count,
        })
    return result


def get_trade_plan_completion_rate(portfolio_id: str) -> Dict:
    """Trade plan completion rate (ST-01, BLG-FEAT-32, EPIC-01, v8.6).

    plans_created: all trade_plans rows for this portfolio.
    plans_completed: plans linked to a position (tp.position_id) with at
      least one closed trade_history row for that position — the same
      trade_plans.position_id = trade_history.position_id equijoin already
      used by get_trade_history_by_tax_year() and get_tag_performance().
    plans_abandoned: plans with status = 'abandoned'.
    completion_rate: plans_completed / plans_created (percentage, None if
      plans_created is 0 — the empty state is handled by the caller, not by
      returning 0%).

    Design source: docs/design/2026-08-11__release-v8.6/trade-plan-completion-rate-metric/decision_record.md
    Spec: docs/specs/frontend/pages/analytics.md §21
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    COUNT(*) AS plans_created,
                    COUNT(*) FILTER (WHERE status = 'abandoned') AS plans_abandoned,
                    COUNT(DISTINCT tp.id) FILTER (
                        WHERE tp.position_id IS NOT NULL AND th.position_id IS NOT NULL
                    ) AS plans_completed
                FROM trade_plans tp
                LEFT JOIN trade_history th ON th.position_id = tp.position_id
                WHERE tp.portfolio_id = %s
                """,
                (portfolio_id,),
            )
            row = cur.fetchone()

    plans_created = int(row["plans_created"] or 0)
    plans_abandoned = int(row["plans_abandoned"] or 0)
    plans_completed = int(row["plans_completed"] or 0)
    completion_rate = round(plans_completed / plans_created * 100, 1) if plans_created else None

    return {
        "plans_created": plans_created,
        "plans_completed": plans_completed,
        "plans_abandoned": plans_abandoned,
        "completion_rate": completion_rate,
    }


def ensure_si02_trade_history_indexes():
    """Add P2 indexes to trade_history for SI-02 drift analysis queries (idempotent).

    DS-07 / SI-02 sprint migration — v4.6 ST-01. Separate from column additions per
    si02_data_schema.md §5.2 (P2 indexes). Uses CREATE INDEX IF NOT EXISTS inside a
    transaction at current data volumes. Use CONCURRENTLY outside a transaction in
    production for zero-downtime creation on large datasets.
    Spec: docs/specs/data_model/si02_data_schema.md §5.2
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_trade_history_exit_date "
                "ON trade_history(portfolio_id, exit_date DESC)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_trade_history_entry_date "
                "ON trade_history(portfolio_id, entry_date DESC)"
            )
        conn.commit()


def ensure_si05_digest_log_table() -> None:
    """Create si05_digest_log table if it does not exist (idempotent).

    Records each SI-05 weekly digest delivery attempt (success and failure).
    Spec: delegation DEL-20260608-02 (BLG-BE-33, v5.2 ST-06)
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS si05_digest_log (
                    id SERIAL PRIMARY KEY,
                    sent_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    status VARCHAR(10) NOT NULL CHECK (status IN ('sent', 'failed')),
                    event_count INTEGER,
                    telegram_message_id VARCHAR(100),
                    error_message TEXT,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
            """)
        conn.commit()


def ensure_trade_plans_active_requires_position_constraint() -> None:
    """DB-level safeguard against new orphaned trade_plans rows (ST-03,
    BLG-BE-91, EPIC-02, v8.6) -- idempotent.

    `position_id` remains nullable by design (a plan may legitimately exist
    pre-entry, or be abandoned, with no position ever attached) -- a hard
    NOT NULL constraint is not viable. The actual integrity risk is narrower
    and precise: `status = 'active'` is meant to mean "this plan is backing
    a live position" (position_service.py::add_position()'s auto-link step
    sets `position_id` and `status = 'active'` together, in the same
    UPDATE, and is the ONLY code path that ever sets status to 'active').
    But `PUT /trade-plans/{id}` (routers/trade_plans.py::update_plan())
    accepts an arbitrary `status` string with no such guard -- a client
    could set `status = 'active'` directly via that endpoint without ever
    supplying a `position_id`, producing exactly the "active but orphaned"
    row this story exists to prevent. This CHECK constraint is the
    database-layer backstop for that gap (the router-level guard in
    `update_plan()` is the primary defense; this is defense-in-depth in
    case a future code path bypasses the router, e.g. a direct DB write or
    a new endpoint that forgets the check).

    Added `NOT VALID` deliberately: this only enforces the rule on rows
    inserted/updated going forward (matching the story's own "going
    forward" framing) -- it does NOT retroactively validate the 11
    legacy pre-BLG-BE-46 (v6.8) trade_plans rows already known to carry
    `position_id IS NULL` (data_model.md's Table: trade_plans section),
    avoiding a migration failure risk from historical data this routine
    cannot inspect directly. A future `VALIDATE CONSTRAINT` pass (a cheap,
    online-safe operation in Postgres once run) can retroactively confirm
    the full table if ever needed -- not required for this story's AC.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans DROP CONSTRAINT IF EXISTS trade_plans_active_requires_position_check"
            )
            cur.execute(
                "ALTER TABLE trade_plans ADD CONSTRAINT trade_plans_active_requires_position_check "
                "CHECK (status != 'active' OR position_id IS NOT NULL) NOT VALID"
            )
        conn.commit()


def ensure_trade_plans_extended_status() -> None:
    """Extend trade_plans_status_check to include workflow statuses (idempotent).

    The original constraint only allowed ('draft', 'active', 'closed').
    The frontend workflow uses additional statuses: research_pending,
    research_complete, entry_conditions_set, abandoned.
    """
    full_statuses = (
        "'draft', 'research_pending', 'research_complete', "
        "'entry_conditions_set', 'active', 'closed', 'abandoned'"
    )
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE trade_plans DROP CONSTRAINT IF EXISTS trade_plans_status_check"
            )
            cur.execute(
                f"ALTER TABLE trade_plans ADD CONSTRAINT trade_plans_status_check "
                f"CHECK (status IN ({full_statuses}))"
            )
        conn.commit()


def get_behavioural_drift_data(portfolio_id: str, window_days: int = 90) -> dict:
    """Fetch all data needed for SI-02 drift metric computation.

    Returns a dict with:
    - trade_count: closed trades in window
    - trades: list of trade records (pnl, entry_date, risk_percent_used, regime_context_at_entry, signal_id)
    - settings: current settings dict (for default_risk_percent)
    Spec: docs/specs/metrics/si02_drift_score.md §2–§4
    """
    result = {"trade_count": 0, "trades": [], "settings": None, "signal_timing": []}
    with get_db() as conn:
        with conn.cursor() as cur:
            # Closed trades in window with plan data
            cur.execute(
                """
                SELECT
                    th.id,
                    th.pnl,
                    p.entry_date,
                    p.exit_date,
                    tp.risk_percent_used,
                    tp.regime_context_at_entry,
                    tp.signal_id,
                    tp.effective_settings_snapshot
                FROM trade_history th
                JOIN positions p ON p.id = th.position_id
                LEFT JOIN trade_plans tp ON tp.position_id = p.id
                WHERE p.portfolio_id = %s
                  AND th.pnl IS NOT NULL
                  AND p.entry_date >= NOW() - INTERVAL '%s days'
                ORDER BY p.entry_date ASC
                """,
                (portfolio_id, window_days),
            )
            result["trades"] = [dict(r) for r in cur.fetchall()]
            result["trade_count"] = len(result["trades"])

            # Signal timing data (for entry_timing_drift) — only trades with signal_id
            cur.execute(
                """
                SELECT
                    p.entry_date,
                    s.signal_date
                FROM trade_history th
                JOIN positions p ON p.id = th.position_id
                JOIN trade_plans tp ON tp.position_id = p.id
                JOIN signals s ON s.id = tp.signal_id
                WHERE p.portfolio_id = %s
                  AND th.pnl IS NOT NULL
                  AND tp.signal_id IS NOT NULL
                  AND p.entry_date >= NOW() - INTERVAL '%s days'
                """,
                (portfolio_id, window_days),
            )
            result["signal_timing"] = [dict(r) for r in cur.fetchall()]

            # Current settings
            cur.execute("SELECT * FROM settings ORDER BY created_at DESC LIMIT 1")
            row = cur.fetchone()
            result["settings"] = dict(row) if row else None
    return result


def get_closed_trade_entry_dates(portfolio_id: str, since_days: int) -> List:
    """Return closed trade entry_dates (ascending) within the last `since_days` days.

    Used by the SI-02 insufficient_data streak metric (ST-05, EPIC-01, v8.2,
    BLG-FEAT-86) to walk backward day-by-day and determine how long the
    rolling 90-day window has held fewer than the minimum trade count —
    a wider lookback than get_behavioural_drift_data's own 90-day window,
    since the streak computation needs to look further back in time.
    Filters by entry_date (not exit_date) to match get_behavioural_drift_data's
    own windowing field, so the streak reflects the same trade_count_in_window
    definition compute_drift() uses.
    Spec: docs/specs/metrics/si02_drift_score.md §3 (insufficient_data_streak_days).
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT p.entry_date
                   FROM trade_history th
                   JOIN positions p ON p.id = th.position_id
                   WHERE p.portfolio_id = %s
                     AND th.pnl IS NOT NULL
                     AND p.entry_date >= NOW() - INTERVAL '%s days'
                   ORDER BY p.entry_date ASC""",
                (portfolio_id, since_days)
            )
            return [row["entry_date"] for row in cur.fetchall()]


# ---------------------------------------------------------------------------
# Gate Metrics (ST-04, EPIC-02, v5.5)
# ---------------------------------------------------------------------------

def get_gate_metrics(portfolio_id: str) -> Dict:
    """Return trade count and gate progress metrics for a portfolio.

    Used by GET /portfolio/gate-metrics and the SI-05 weekly digest to surface
    data density progress toward the 20/50/100 closed-trade gates.

    Returns:
        dict with keys:
          closed_trades_count (int)
          closed_trades_with_plans (int)
          active_positions_count (int)
          ai_journal_entry_count (int | None — None if table absent)
          oldest_trade_date (str ISO-8601 | None)
          newest_trade_date (str ISO-8601 | None)
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            # Closed trades total
            cur.execute(
                "SELECT COUNT(*)::int AS cnt FROM trade_history WHERE portfolio_id = %s",
                (portfolio_id,),
            )
            closed_trades_count = cur.fetchone()["cnt"]

            # Closed trades that have at least one associated trade plan
            cur.execute(
                """
                SELECT COUNT(DISTINCT th.id)::int AS cnt
                FROM trade_history th
                WHERE th.portfolio_id = %s
                  AND EXISTS (
                      SELECT 1 FROM trade_plans tp
                      WHERE tp.position_id = th.position_id
                  )
                """,
                (portfolio_id,),
            )
            closed_trades_with_plans = cur.fetchone()["cnt"]

            # Active positions
            cur.execute(
                "SELECT COUNT(*)::int AS cnt FROM positions WHERE portfolio_id = %s AND status = 'open'",
                (portfolio_id,),
            )
            active_positions_count = cur.fetchone()["cnt"]

            # Oldest and newest trade dates
            cur.execute(
                """
                SELECT
                    MIN(exit_date)::text AS oldest,
                    MAX(exit_date)::text AS newest
                FROM trade_history
                WHERE portfolio_id = %s
                """,
                (portfolio_id,),
            )
            row = cur.fetchone()
            oldest_trade_date = row["oldest"] if row else None
            newest_trade_date = row["newest"] if row else None

            # ai_journal_entry_count — only if table exists
            ai_journal_entry_count = None
            cur.execute(
                """
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_name = 'ai_journal_entries'
                ) AS tbl_exists
                """
            )
            if cur.fetchone()["tbl_exists"]:
                cur.execute(
                    "SELECT COUNT(*)::int AS cnt FROM ai_journal_entries WHERE portfolio_id = %s",
                    (portfolio_id,),
                )
                ai_journal_entry_count = cur.fetchone()["cnt"]

    return {
        "closed_trades_count": closed_trades_count,
        "closed_trades_with_plans": closed_trades_with_plans,
        "active_positions_count": active_positions_count,
        "ai_journal_entry_count": ai_journal_entry_count,
        "oldest_trade_date": oldest_trade_date,
        "newest_trade_date": newest_trade_date,
    }


# ============================================================================
# ST-03 (BLG-FEAT-47) — Rebalance exit signal support
# ============================================================================

def ensure_signals_exit_rebalance_status():
    """Extend signals_status_check constraint to include 'exit_rebalance' (idempotent).

    ST-03 (EPIC-01, v6.2) — BLG-FEAT-47. Month-end rebalance exit signals need
    a dedicated status value distinct from momentum signal statuses.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE signals DROP CONSTRAINT IF EXISTS signals_status_check"
            )
            cur.execute(
                "ALTER TABLE signals ADD CONSTRAINT signals_status_check "
                "CHECK (status IN ('new', 'entered', 'dismissed', 'expired', "
                "'already_held', 'watchlisted', 'allocation_insufficient', 'exit_rebalance'))"
            )
        conn.commit()


def create_rebalance_exit_signal(portfolio_id: str, ticker: str, market: str,
                                  current_price: float, price_gbp: float,
                                  signal_date: str, reason: str) -> Dict:
    """Insert an exit_rebalance signal for a position not in top-5 momentum list.

    Uses the existing signals table with non-applicable sizing fields set to 0/null.
    The UNIQUE(portfolio_id, ticker, signal_date) constraint prevents duplicates.
    """
    ticker = _sanitize_signal_string(ticker)
    market = _sanitize_signal_string(market)
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO signals (
                    portfolio_id, ticker, market, signal_date, rank,
                    momentum_percent, current_price, price_gbp, atr_value,
                    volatility, initial_stop, suggested_shares, allocation_gbp,
                    total_cost, status, reason
                ) VALUES (
                    %s, %s, %s, %s, 0,
                    0, %s, %s, 0,
                    0, 0, 0, 0,
                    0, 'exit_rebalance', %s
                )
                ON CONFLICT (portfolio_id, ticker, signal_date) DO UPDATE SET
                    status = 'exit_rebalance',
                    reason = EXCLUDED.reason,
                    updated_at = NOW()
                RETURNING *
            """, (portfolio_id, ticker, market, signal_date,
                  current_price, price_gbp, reason))
            conn.commit()
            return cur.fetchone()


# ============================================================================
# ST-05 (BLG-FEAT-49) — Risk-off exit alert column
# ============================================================================

def ensure_risk_off_exit_column():
    """Add risk_off_exit boolean column to positions table (idempotent).

    ST-05 (EPIC-01, v6.2) — BLG-FEAT-49. Per-position flag set by the nightly
    risk-off alert job. Cleared automatically when the index recovers.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE positions ADD COLUMN IF NOT EXISTS risk_off_exit BOOLEAN NOT NULL DEFAULT FALSE"
            )
        conn.commit()


def update_positions_risk_off_exit(position_id: str, risk_off_exit: bool) -> None:
    """Set or clear the risk_off_exit flag for a single position."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE positions SET risk_off_exit = %s WHERE id = %s",
                (risk_off_exit, position_id)
            )


# ============================================================================
# ST-11 (BLG-FEAT-53) — Strategy Benchmark: backtest vs live comparison
# ============================================================================

def ensure_backtest_tables():
    """Create backtest_trades and backtest_yearly_performance tables (idempotent).

    ST-11 (EPIC-03, v6.3) — BLG-FEAT-53. These tables store imported backtest
    results from production_strategy.py CSV outputs so they can be compared
    against live trade history on the Strategy Benchmark page.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS backtest_trades (
                    id SERIAL PRIMARY KEY,
                    ticker VARCHAR(20) NOT NULL,
                    entry_date DATE NOT NULL,
                    exit_date DATE NOT NULL,
                    holding_days INTEGER,
                    entry_price NUMERIC(12, 4),
                    exit_price NUMERIC(12, 4),
                    pnl_gbp NUMERIC(12, 2),
                    pnl_pct NUMERIC(8, 4),
                    market VARCHAR(10) NOT NULL DEFAULT 'US',
                    exit_reason VARCHAR(50),
                    was_profitable BOOLEAN,
                    entry_year INTEGER NOT NULL,
                    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    UNIQUE (ticker, entry_date, exit_date)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS backtest_yearly_performance (
                    id SERIAL PRIMARY KEY,
                    entry_year INTEGER NOT NULL,
                    num_trades INTEGER,
                    avg_pnl_gbp NUMERIC(12, 2),
                    total_pnl_gbp NUMERIC(12, 2),
                    avg_hold_days NUMERIC(8, 2),
                    win_rate_pct NUMERIC(5, 2),
                    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    UNIQUE (entry_year)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS backtest_open_positions (
                    id SERIAL PRIMARY KEY,
                    ticker VARCHAR(20) NOT NULL,
                    entry_date DATE NOT NULL,
                    entry_price NUMERIC(12, 4),
                    current_price NUMERIC(12, 4),
                    unrealized_pnl_gbp NUMERIC(12, 2),
                    unrealized_pnl_pct NUMERIC(8, 4),
                    market VARCHAR(10) NOT NULL DEFAULT 'US',
                    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    UNIQUE (ticker, entry_date)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS backtest_import_history (
                    id SERIAL PRIMARY KEY,
                    imported_at TIMESTAMPTZ NOT NULL UNIQUE,
                    trades_count INTEGER NOT NULL,
                    total_pnl_gbp NUMERIC(14, 2),
                    open_positions_count INTEGER NOT NULL,
                    total_unrealized_pnl_gbp NUMERIC(14, 2),
                    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
        conn.commit()


def upsert_backtest_data(
    trades: List[Dict],
    yearly_performance: List[Dict],
    open_positions: Optional[List[Dict]] = None,
) -> Dict:
    """Replace backtest trade, yearly performance, and open position records with a fresh snapshot.

    production_strategy.py recomputes the entire trade history from scratch on
    every run, so each import is the complete, authoritative picture rather
    than an incremental delta. Deleting existing rows first (in the same
    transaction — a failed import rolls back and leaves prior data intact)
    means a trade the model no longer produces (e.g. a stale exit invalidated
    by a bug fix) doesn't linger forever. The previous upsert-only approach
    had no way to remove rows that stopped being generated, which is exactly
    how 5 fictional trades from a fixed phantom-date bug stayed in the table.

    backtest_open_positions is replaced with the same full-wipe pattern
    (ST-08, BLG-FEAT-54, AC-03) — a position that has since closed must not
    linger in the table past the next import.

    Idempotency (ST-09, EPIC-09, v7.7): this function is safe against
    double-run/retry by design. The DELETE+INSERT sequence executes inside
    a single get_db() transaction (commit only on success, rollback on any
    exception — see get_db()'s docstring) — a retry after a failed run simply
    re-runs the full replace against whatever the current DB state is, never
    partially applying. Concurrent overlapping runs (e.g. a manual
    workflow_dispatch while the scheduled cron run is still executing) are
    additionally guarded at the CI level by backtest.yml's `concurrency:`
    group, which queues rather than runs them in parallel — but even without
    that guard, Postgres's row-level locking on DELETE would serialize two
    concurrent transactions here, with the later-committing one's snapshot
    ending up authoritative (correct "most recent computation wins"
    semantics for a full-replace design). See
    docs/product/decisions/decisions--2026-07-21__release-v7.7--nightly-backtest-idempotency-audit.md.

    Before the wipe, the about-to-be-replaced aggregate (total_pnl_gbp,
    total_unrealized_pnl_gbp) is snapshotted into backtest_import_history —
    the full-replace pattern above means the prior night's totals would
    otherwise be unrecoverable, making it impossible to tell a legitimate
    unrealized-to-realized swing apart from an unexplained jump after the
    fact. Returned as previous_total_pnl_gbp / total_pnl_gbp_delta /
    previous_total_unrealized_pnl_gbp so import_backtest.py can print it.

    Returns a dict with 'trades_imported', 'years_imported', and
    'open_positions_imported' counts (plus their _deleted counterparts).
    """
    now = datetime.utcnow()
    trades_count = 0
    years_count = 0
    open_positions_count = 0
    open_positions = open_positions or []
    new_total_pnl_gbp = sum(t.get("pnl_gbp") or 0 for t in trades)
    new_total_unrealized_pnl_gbp = sum(p.get("unrealized_pnl_gbp") or 0 for p in open_positions)
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) AS c, COALESCE(SUM(pnl_gbp), 0) AS total, MAX(imported_at) AS ts
                FROM backtest_trades
            """)
            prev_trades = cur.fetchone()
            previous_total_pnl_gbp = None
            previous_total_unrealized_pnl_gbp = None
            if prev_trades and prev_trades["c"] > 0:
                cur.execute("""
                    SELECT COUNT(*) AS c, COALESCE(SUM(unrealized_pnl_gbp), 0) AS total
                    FROM backtest_open_positions
                """)
                prev_open = cur.fetchone()
                previous_total_pnl_gbp = float(prev_trades["total"])
                previous_total_unrealized_pnl_gbp = float(prev_open["total"]) if prev_open else None
                cur.execute("""
                    INSERT INTO backtest_import_history (
                        imported_at, trades_count, total_pnl_gbp,
                        open_positions_count, total_unrealized_pnl_gbp
                    ) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (imported_at) DO NOTHING
                """, (
                    prev_trades["ts"],
                    prev_trades["c"],
                    previous_total_pnl_gbp,
                    prev_open["c"] if prev_open else 0,
                    previous_total_unrealized_pnl_gbp,
                ))

            cur.execute("DELETE FROM backtest_trades")
            trades_deleted = cur.rowcount
            cur.execute("DELETE FROM backtest_yearly_performance")
            years_deleted = cur.rowcount
            cur.execute("DELETE FROM backtest_open_positions")
            open_positions_deleted = cur.rowcount
            for trade in trades:
                cur.execute("""
                    INSERT INTO backtest_trades (
                        ticker, entry_date, exit_date, holding_days,
                        entry_price, exit_price, pnl_gbp, pnl_pct,
                        market, exit_reason, was_profitable, entry_year, imported_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (ticker, entry_date, exit_date) DO UPDATE SET
                        holding_days = EXCLUDED.holding_days,
                        entry_price = EXCLUDED.entry_price,
                        exit_price = EXCLUDED.exit_price,
                        pnl_gbp = EXCLUDED.pnl_gbp,
                        pnl_pct = EXCLUDED.pnl_pct,
                        market = EXCLUDED.market,
                        exit_reason = EXCLUDED.exit_reason,
                        was_profitable = EXCLUDED.was_profitable,
                        entry_year = EXCLUDED.entry_year,
                        imported_at = EXCLUDED.imported_at
                """, (
                    trade.get("ticker"),
                    trade.get("entry_date"),
                    trade.get("exit_date"),
                    trade.get("holding_days"),
                    trade.get("entry_price"),
                    trade.get("exit_price"),
                    trade.get("pnl_gbp"),
                    trade.get("pnl_pct"),
                    trade.get("market", "US"),
                    trade.get("exit_reason"),
                    trade.get("was_profitable"),
                    trade.get("entry_year"),
                    now,
                ))
                trades_count += 1
            for row in yearly_performance:
                cur.execute("""
                    INSERT INTO backtest_yearly_performance (
                        entry_year, num_trades, avg_pnl_gbp, total_pnl_gbp,
                        avg_hold_days, win_rate_pct, imported_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (entry_year) DO UPDATE SET
                        num_trades = EXCLUDED.num_trades,
                        avg_pnl_gbp = EXCLUDED.avg_pnl_gbp,
                        total_pnl_gbp = EXCLUDED.total_pnl_gbp,
                        avg_hold_days = EXCLUDED.avg_hold_days,
                        win_rate_pct = EXCLUDED.win_rate_pct,
                        imported_at = EXCLUDED.imported_at
                """, (
                    row.get("entry_year"),
                    row.get("num_trades"),
                    row.get("avg_pnl_gbp"),
                    row.get("total_pnl_gbp"),
                    row.get("avg_hold_days"),
                    row.get("win_rate_pct"),
                    now,
                ))
                years_count += 1
            for pos in open_positions:
                cur.execute("""
                    INSERT INTO backtest_open_positions (
                        ticker, entry_date, entry_price, current_price,
                        unrealized_pnl_gbp, unrealized_pnl_pct, market, imported_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (ticker, entry_date) DO UPDATE SET
                        entry_price = EXCLUDED.entry_price,
                        current_price = EXCLUDED.current_price,
                        unrealized_pnl_gbp = EXCLUDED.unrealized_pnl_gbp,
                        unrealized_pnl_pct = EXCLUDED.unrealized_pnl_pct,
                        market = EXCLUDED.market,
                        imported_at = EXCLUDED.imported_at
                """, (
                    pos.get("ticker"),
                    pos.get("entry_date"),
                    pos.get("entry_price"),
                    pos.get("current_price"),
                    pos.get("unrealized_pnl_gbp"),
                    pos.get("unrealized_pnl_pct"),
                    pos.get("market", "US"),
                    now,
                ))
                open_positions_count += 1
        conn.commit()
    return {
        "trades_imported": trades_count,
        "years_imported": years_count,
        "open_positions_imported": open_positions_count,
        "trades_deleted": trades_deleted,
        "years_deleted": years_deleted,
        "open_positions_deleted": open_positions_deleted,
        "imported_at": now.isoformat() + "Z",
        "previous_total_pnl_gbp": previous_total_pnl_gbp,
        "total_pnl_gbp_delta": (
            round(new_total_pnl_gbp - previous_total_pnl_gbp, 2)
            if previous_total_pnl_gbp is not None else None
        ),
        "previous_total_unrealized_pnl_gbp": previous_total_unrealized_pnl_gbp,
    }


def get_backtest_trades(
    year_filter: Optional[int] = None,
    market_filter: Optional[str] = None,
) -> List[Dict]:
    """Return backtest trades filtered by year and/or market."""
    conditions = []
    params: List = []
    if year_filter is not None:
        conditions.append("entry_year = %s")
        params.append(year_filter)
    if market_filter and market_filter.upper() != "ALL":
        conditions.append("market = %s")
        params.append(market_filter.upper())
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM backtest_trades {where} ORDER BY entry_date ASC",
                params,
            )
            return [dict(r) for r in cur.fetchall()]


def get_backtest_open_positions(market_filter: Optional[str] = None) -> Dict:
    """Return current open (unrealized) backtest positions for Panel 0.

    ST-08 (BLG-FEAT-54, EPIC-03, v6.4). No year filter — open positions are
    current-state, not historical-per-year data (per ux_spec.md "Filter
    Interaction"). days_held is derived live from entry_date rather than
    stored, so it stays correct between imports.
    """
    conditions = []
    params: List = []
    if market_filter and market_filter.upper() != "ALL":
        conditions.append("market = %s")
        params.append(market_filter.upper())
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    ticker, market, entry_date, entry_price, current_price,
                    unrealized_pnl_gbp, unrealized_pnl_pct,
                    (CURRENT_DATE - entry_date) AS days_held
                FROM backtest_open_positions
                {where}
                ORDER BY unrealized_pnl_pct DESC NULLS LAST
            """, params)
            positions = [dict(r) for r in cur.fetchall()]

            cur.execute(f"""
                SELECT
                    COUNT(*) AS count,
                    ROUND(SUM(unrealized_pnl_gbp)::numeric, 2) AS total_unrealized_pnl_gbp
                FROM backtest_open_positions
                {where}
            """, params)
            summary_row = cur.fetchone()

    return {
        "open_positions": positions,
        "summary": {
            "count": summary_row["count"] if summary_row else 0,
            "total_unrealized_pnl_gbp": summary_row["total_unrealized_pnl_gbp"] if summary_row else None,
        },
    }


def get_backtest_summary(
    year_filter: Optional[int] = None,
    market_filter: Optional[str] = None,
) -> Dict:
    """Return aggregated backtest stats and yearly breakdown for the Strategy Benchmark page.

    backtest_stats covers Panel 1 stats. yearly_breakdown covers Panel 2.
    """
    trade_conditions = []
    trade_params: List = []
    if year_filter is not None:
        trade_conditions.append("entry_year = %s")
        trade_params.append(year_filter)
    if market_filter and market_filter.upper() != "ALL":
        trade_conditions.append("market = %s")
        trade_params.append(market_filter.upper())
    where = ("WHERE " + " AND ".join(trade_conditions)) if trade_conditions else ""

    with get_db() as conn:
        with conn.cursor() as cur:
            # Panel 1 aggregated stats from backtest_trades
            cur.execute(f"""
                SELECT
                    COUNT(*) AS total_trades,
                    ROUND(
                        100.0 * SUM(CASE WHEN was_profitable THEN 1 ELSE 0 END)
                        / NULLIF(COUNT(*), 0), 1
                    ) AS win_rate_pct,
                    ROUND(AVG(pnl_gbp)::numeric, 2) AS avg_pnl_gbp,
                    ROUND(SUM(pnl_gbp)::numeric, 2) AS total_pnl_gbp,
                    ROUND(AVG(holding_days)::numeric, 1) AS avg_hold_days
                FROM backtest_trades {where}
            """, trade_params)
            row = cur.fetchone()
            backtest_stats = dict(row) if row and row["total_trades"] else None

            # Panel 2 yearly breakdown
            yearly_conditions = []
            yearly_params: List = []
            cur.execute("""
                SELECT entry_year, num_trades, avg_pnl_gbp, total_pnl_gbp,
                       avg_hold_days, win_rate_pct
                FROM backtest_yearly_performance
                ORDER BY entry_year ASC
            """)
            yearly_breakdown = [dict(r) for r in cur.fetchall()]

            # Last imported_at
            #
            # ST-03 (BLG-OPS-143, EPIC-01, v8.8): imported_at is TIMESTAMPTZ, so
            # psycopg2 returns a timezone-aware datetime whose .isoformat() already
            # ends in "+00:00" — naively appending "Z" (as elsewhere in this file,
            # where the source datetime is naive) produced a malformed double-suffixed
            # string ("...+00:00Z"), which is not valid ISO-8601 and made
            # `new Date(...)` return Invalid Date on the frontend. Strip any tzinfo
            # after normalising to UTC before appending "Z", so this always matches
            # the single-suffix format the frontend (and every other timestamp in
            # this API) expects.
            cur.execute("SELECT MAX(imported_at) AS last_imported FROM backtest_trades")
            ts_row = cur.fetchone()
            last_imported_at = None
            if ts_row and ts_row["last_imported"]:
                ts = ts_row["last_imported"]
                if ts.tzinfo is not None:
                    ts = ts.astimezone(timezone.utc).replace(tzinfo=None)
                last_imported_at = ts.isoformat() + "Z"

            # Available years for filter dropdown
            cur.execute(
                "SELECT DISTINCT entry_year FROM backtest_trades ORDER BY entry_year ASC"
            )
            available_years = [r["entry_year"] for r in cur.fetchall()]

    return {
        "last_imported_at": last_imported_at,
        "backtest_stats": backtest_stats,
        "yearly_breakdown": yearly_breakdown,
        "available_years": available_years,
    }


def get_actual_stats_for_benchmark(
    portfolio_id: str,
    year_filter: Optional[int] = None,
    market_filter: Optional[str] = None,
) -> Optional[Dict]:
    """Return live trade stats for Panel 1 comparison.

    Returns None if no live trades match the filter (frontend shows '—' per AC-03).
    """
    conditions = ["portfolio_id = %s"]
    params: List = [portfolio_id]
    if year_filter is not None:
        conditions.append("EXTRACT(YEAR FROM entry_date) = %s")
        params.append(year_filter)
    if market_filter and market_filter.upper() != "ALL":
        conditions.append("market = %s")
        params.append(market_filter.upper())
    where = "WHERE " + " AND ".join(conditions)
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    COUNT(*) AS total_trades,
                    ROUND(
                        100.0 * SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END)
                        / NULLIF(COUNT(*), 0), 1
                    ) AS win_rate_pct,
                    ROUND(AVG(pnl)::numeric, 2) AS avg_pnl_gbp,
                    ROUND(SUM(pnl)::numeric, 2) AS total_pnl_gbp,
                    ROUND(AVG(holding_days)::numeric, 1) AS avg_hold_days
                FROM trade_history {where}
            """, params)
            row = cur.fetchone()
            if row is None or row["total_trades"] == 0:
                return None
            return dict(row)
        conn.commit()


# ============================================================================
# IDEMPOTENCY KEYS (ST-03, EPIC-01, v7.10, BLG-BE-76)
# ============================================================================

def ensure_idempotency_keys_table() -> None:
    """Create idempotency_keys table if it does not exist (idempotent).

    Generic, additive, opt-in store for state-mutating POST endpoints. Only
    touched when a caller supplies an idempotency_key (see
    utils/idempotency.py::replay_or_create) — endpoints that never receive
    one never call this function, so behaviour is unchanged when the key is
    absent (RISK-02).
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS idempotency_keys (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL,
                    endpoint VARCHAR(100) NOT NULL,
                    idempotency_key VARCHAR(200) NOT NULL,
                    response_body JSONB NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    UNIQUE (portfolio_id, endpoint, idempotency_key)
                )
            """)
        conn.commit()


def get_idempotency_record(portfolio_id: str, endpoint: str, idempotency_key: str) -> Optional[Dict]:
    """Pure read — returns the cached response body dict, or None if no record exists."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT response_body FROM idempotency_keys
                   WHERE portfolio_id = %s AND endpoint = %s AND idempotency_key = %s""",
                (portfolio_id, endpoint, idempotency_key),
            )
            row = cur.fetchone()
            if row is None:
                return None
            body = row["response_body"]
            if isinstance(body, str):
                import json
                return json.loads(body)
            return body


def create_idempotency_record(portfolio_id: str, endpoint: str, idempotency_key: str, response_body: Dict) -> None:
    """Store a response body keyed by (portfolio_id, endpoint, idempotency_key).

    Concurrent duplicate inserts are safely absorbed via ON CONFLICT DO
    NOTHING — the loser of a race simply doesn't overwrite the winner's
    already-cached response.
    """
    import json
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO idempotency_keys (portfolio_id, endpoint, idempotency_key, response_body)
                   VALUES (%s, %s, %s, %s::jsonb)
                   ON CONFLICT (portfolio_id, endpoint, idempotency_key) DO NOTHING""",
                (portfolio_id, endpoint, idempotency_key, json.dumps(response_body, default=str)),
            )
        conn.commit()
