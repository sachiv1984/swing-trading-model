import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict
from datetime import datetime
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
                    entry_note, tags, user_fill_price
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s
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
                position_data.get('user_fill_price')
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
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM trade_history
                   WHERE portfolio_id = %s
                   AND exit_date BETWEEN %s AND %s
                   ORDER BY exit_date ASC""",
                (portfolio_id, year_start, year_end)
            )
            return cur.fetchall()


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
# SIGNALS FUNCTIONS
# ============================================================================

def create_signal(portfolio_id: str, signal_data: Dict) -> Dict:
    """Create or update a signal"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO signals (
                    portfolio_id, ticker, market, signal_date, rank,
                    momentum_percent, current_price, price_gbp, atr_value,
                    volatility, initial_stop, suggested_shares, allocation_gbp,
                    total_cost, status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                    updated_at = NOW()
                RETURNING *
            """, (
                portfolio_id,
                signal_data['ticker'],
                signal_data['market'],
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
                signal_data.get('status', 'new')
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


def update_signal(signal_id: str, updates: Dict) -> Dict:
    """Update a signal"""
    with get_db() as conn:
        with conn.cursor() as cur:
            set_parts = []
            values = []
            
            for key, value in updates.items():
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

def get_all_tickers() -> List[str]:
    """Get list of all tickers in universe"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT ticker FROM tickers ORDER BY ticker")
            results = cur.fetchall()
            return [row['ticker'] for row in results]


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
                    pre_entry_override_acknowledged BOOLEAN
                )
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trade_plans_portfolio ON trade_plans(portfolio_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trade_plans_position ON trade_plans(position_id) WHERE position_id IS NOT NULL")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trade_plans_status ON trade_plans(status)")
        conn.commit()
    ensure_regime_context_text_column()


def create_trade_plan(portfolio_id: str, data: dict) -> dict:
    with get_db() as conn:
        with conn.cursor() as cur:
            _json = __import__("json").dumps
            cur.execute(
                """INSERT INTO trade_plans
                   (portfolio_id, position_id, ticker, market, setup_type, setup_thesis, entry_rationale,
                    regime_context_at_entry, r_target, early_exit_conditions, confirmation_criteria,
                    checklist_completed, checklist_items, status, pre_entry_override_acknowledged,
                    signal_id, risk_percent_used, portfolio_value_at_entry,
                    pre_entry_validation_snapshot, effective_settings_snapshot)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb)
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
                    data.get("signal_id"),
                    data.get("risk_percent_used"),
                    data.get("portfolio_value_at_entry"),
                    _json(data["pre_entry_validation_snapshot"]) if data.get("pre_entry_validation_snapshot") is not None else None,
                    _json(data["effective_settings_snapshot"]) if data.get("effective_settings_snapshot") is not None else None,
                ),
            )
            row = cur.fetchone()
        conn.commit()
        return dict(row)


def get_trade_plans(portfolio_id: str, status: str = None, ticker: str = None) -> list:
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
            where = " AND ".join(clauses)
            cur.execute(
                f"SELECT * FROM trade_plans WHERE {where} ORDER BY created_at DESC",
                params,
            )
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
        "pre_entry_override_acknowledged",
    }
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return get_trade_plan_by_id(trade_plan_id, portfolio_id)
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
        return dict(row) if row else None


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


def get_trade_by_id(trade_id: str) -> Optional[Dict]:
    """Fetch a single trade_history record by its UUID."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM trade_history WHERE id = %s", (trade_id,))
            row = cur.fetchone()
            return dict(row) if row else None


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


def query_claude_audit_log(limit: int = 50) -> list[dict]:
    """Return the most recent rows from claude_audit_log, newest first."""
    try:
        ensure_claude_audit_log_table()
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, endpoint, model_id, prompt_version,
                           input_tokens, output_tokens, cost_usd, generated_at
                    FROM claude_audit_log
                    ORDER BY generated_at DESC
                    LIMIT %s
                    """,
                    (limit,),
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
