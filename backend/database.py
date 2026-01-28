import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

@contextmanager
def get_db():
    """Database connection context manager"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()
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
    """Update a position"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Build dynamic UPDATE query
            set_parts = []
            values = []
            for key, value in updates.items():
                set_parts.append(f"{key} = %s")
                values.append(value)
            
            values.append(position_id)
            
            query = f"UPDATE positions SET {', '.join(set_parts)}, updated_at = NOW() WHERE id = %s RETURNING *"
            cur.execute(query, values)
            return cur.fetchone()


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
