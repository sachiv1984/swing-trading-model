import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict
from datetime import datetime
import pandas as pd
import time
import requests





DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

@contextmanager
def get_db():
    """Database connection context manager"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()  # CRITICAL: Ensure commit happens
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_portfolio() -> Optional[Dict]:
    """Get the main portfolio (assumes single portfolio)"""
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


def get_positions(portfolio_id: str, status: str = None) -> List[Dict]:
    """Get positions, optionally filtered by status"""
    with get_db() as conn:
        with conn.cursor() as cur:
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


def create_position(portfolio_id: str, position_data: Dict) -> Dict:
    """Create a new position"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO positions (
                    portfolio_id, ticker, market, entry_date, entry_price,
                    fill_price, fill_currency, fx_rate, shares, total_cost,
                    fees_paid, fee_type, initial_stop, current_stop, current_price,
                    atr, holding_days, pnl, pnl_pct, status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                position_data.get('status', 'open')
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


def create_trade_history(portfolio_id: str, trade_data: Dict) -> Dict:
    """Add a trade to history"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO trade_history (
                    portfolio_id, ticker, market, entry_date, exit_date,
                    shares, entry_price, exit_price, total_cost, gross_proceeds,
                    net_proceeds, entry_fees, exit_fees, pnl, pnl_pct,
                    holding_days, exit_reason, entry_fx_rate, exit_fx_rate
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING *
            """, (
                portfolio_id,
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
                trade_data.get('exit_fx_rate')
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


def update_settings(settings_id, data):
    """Update existing settings"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Build SET clause
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE settings SET {set_clause}, updated_at = NOW() WHERE id = %s RETURNING *"
            
            cur.execute(query, list(data.values()) + [settings_id])
            result = cur.fetchone()
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
            
            # Create DataFrame
            df = pd.DataFrame({
                'date': dates,
                'close': closes,
                'high': highs,
                'low': lows
            })
            
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


def get_total_deposits_withdrawals(portfolio_id: str) -> Dict:
    """Get total deposits and withdrawals for a portfolio"""
    with get_db() as conn:
        with conn.cursor() as cur:
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

