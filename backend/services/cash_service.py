"""
Cash Service

Business logic for cash management including:
- Deposit and withdrawal transactions
- Transaction history retrieval
- Cash flow summary calculations

All functions are independent of FastAPI for maximum testability.
"""

from typing import Dict, List
from datetime import datetime

from database import (
    get_portfolio,
    update_portfolio_cash,
    create_cash_transaction as db_create_cash_transaction,
    get_cash_transactions as db_get_cash_transactions,
    get_total_deposits_withdrawals
)

from utils.formatting import decimal_to_float


def create_transaction(
    transaction_type: str,
    amount: float,
    date: str = None,
    note: str = None
) -> Dict:
    """
    Create a cash transaction (deposit or withdrawal)
    
    Args:
        transaction_type: "deposit" or "withdrawal"
        amount: Amount in GBP (must be positive)
        date: Transaction date (YYYY-MM-DD), defaults to today
        note: Optional note/description
    
    Returns:
        Dictionary with:
            - transaction: Created transaction record
            - new_balance: Portfolio cash balance after transaction
    
    Raises:
        ValueError: If portfolio not found, invalid type, invalid amount,
                   or insufficient funds for withdrawal
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    current_cash = float(portfolio['cash'])
    
    # Validate transaction type
    if transaction_type not in ['deposit', 'withdrawal']:
        raise ValueError("Invalid transaction type. Must be 'deposit' or 'withdrawal'")
    
    # Validate amount
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    
    # For withdrawals, check if there's enough cash
    if transaction_type == 'withdrawal' and amount > current_cash:
        raise ValueError(
            f"Insufficient funds. Available cash: £{current_cash:.2f}, withdrawal: £{amount:.2f}"
        )
    
    # Create transaction record
    transaction_data = {
        'type': transaction_type,
        'amount': amount,
        'date': date or datetime.now().strftime('%Y-%m-%d'),
        'note': note or ''
    }
    
    transaction = db_create_cash_transaction(portfolio_id, transaction_data)
    
    # Update portfolio cash balance
    if transaction_type == 'deposit':
        new_cash = current_cash + amount
        print(f"💰 Deposit: £{amount:,.2f}")
    else:  # withdrawal
        new_cash = current_cash - amount
        print(f"💸 Withdrawal: £{amount:,.2f}")
    
    update_portfolio_cash(portfolio_id, new_cash)
    
    print(f"✓ Cash transaction created:")
    print(f"   Type: {transaction_type.upper()}")
    print(f"   Amount: £{amount:,.2f}")
    print(f"   Date: {transaction_data['date']}")
    print(f"   Old balance: £{current_cash:,.2f}")
    print(f"   New balance: £{new_cash:,.2f}")
    if note:
        print(f"   Note: {note}")
    print()
    
    return {
        "transaction": decimal_to_float(transaction),
        "new_balance": new_cash
    }


def get_transaction_history(order: str = "DESC") -> List[Dict]:
    """
    Get all cash transactions for the portfolio
    
    Args:
        order: Sort order - "ASC" or "DESC" (default DESC = newest first)
    
    Returns:
        List of transaction dictionaries with:
            - id: Transaction UUID
            - type: "deposit" or "withdrawal"
            - amount: Transaction amount (GBP)
            - date: Transaction date
            - note: Optional note
            - created_at: When transaction was recorded
    
    Raises:
        ValueError: If portfolio not found
    
    Note:
        - Returns empty list if no transactions exist
        - Sorted by date according to order parameter
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    
    # Validate order parameter
    if order.upper() not in ['ASC', 'DESC']:
        order = 'DESC'
    
    transactions = db_get_cash_transactions(portfolio_id, order.upper())
    
    # Format for frontend
    formatted = []
    for tx in transactions:
        formatted.append({
            'id': str(tx['id']),
            'type': tx['type'],
            'amount': float(tx['amount']),
            'date': str(tx['date']),
            'note': tx['note'] or '',
            'created_at': str(tx['created_at'])
        })
    
    print(f"✓ Retrieved {len(formatted)} cash transactions")
    
    return formatted


def get_summary() -> Dict:
    """
    Get cash flow summary (deposits, withdrawals, net flow)
    
    Returns:
        Dictionary with:
            - total_deposits: Sum of all deposits (GBP)
            - total_withdrawals: Sum of all withdrawals (GBP)
            - net_cash_flow: Deposits - withdrawals (GBP)
            - current_cash: Current cash balance (GBP)
    
    Raises:
        ValueError: If portfolio not found
    
    Note:
        - Used for accurate P&L calculation
        - Net cash flow = total invested in portfolio
        - Portfolio P&L = current value - net cash flow
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    summary = get_total_deposits_withdrawals(portfolio_id)
    
    current_cash = float(portfolio['cash'])
    
    print(f"💰 Cash Summary:")
    print(f"   Total deposits: £{summary['total_deposits']:,.2f}")
    print(f"   Total withdrawals: £{summary['total_withdrawals']:,.2f}")
    print(f"   Net cash flow: £{summary['net_cash_flow']:,.2f}")
    print(f"   Current cash: £{current_cash:,.2f}")
    print()
    
    return {
        "total_deposits": round(summary['total_deposits'], 2),
        "total_withdrawals": round(summary['total_withdrawals'], 2),
        "net_cash_flow": round(summary['net_cash_flow'], 2),
        "current_cash": current_cash
    }
