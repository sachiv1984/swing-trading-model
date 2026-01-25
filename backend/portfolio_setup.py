"""
=====================================================================
PORTFOLIO SETUP - Initialize or Update Portfolio
=====================================================================
Use this to:
- Create a new portfolio
- Manually add positions you've already entered
- Update cash balance
- Properly handles UK stamp duty and US fees
- Currency conversion for US stocks
=====================================================================
"""

import json
import os
from datetime import datetime
import pandas as pd

# Use relative path for API compatibility
BASE_DIR = os.path.dirname(__file__)
PORTFOLIO_FILE = os.path.join(BASE_DIR, "current_portfolio.json")

# Fee structure
UK_STAMP_DUTY = 0.005  # 0.5% on purchases
US_TRADE_FEE = 0.0015  # 0.15% on purchases


def create_new_portfolio(cash=20000.0):
    """Create a fresh portfolio programmatically"""
    portfolio = {
        "cash": cash,
        "positions": {},
        "trade_history": [],
        "pending_orders": [],
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_portfolio(portfolio)
    print(f"\n✓ New portfolio created with £{cash:,.2f} cash")
    return portfolio


def load_portfolio():
    """Load existing portfolio"""
    if not os.path.exists(PORTFOLIO_FILE):
        print(f"No portfolio file found at {PORTFOLIO_FILE}")
        return None

    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)


def save_portfolio(portfolio):
    """Save portfolio to file"""
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)
    print(f"✓ Portfolio saved to {PORTFOLIO_FILE}")


def add_position_programmatic(
    portfolio,
    ticker,
    entry_date,
    shares,
    fill_price,
    fill_currency="GBP",
    fx_rate=None,
    atr_value=None,
    custom_stop=None
):
    """
    Add a position programmatically (for API use)
    
    Args:
        portfolio: Portfolio dict
        ticker: Ticker symbol (e.g., "AAPL" or "FRES.L")
        entry_date: Entry date string (YYYY-MM-DD)
        shares: Number of shares
        fill_price: Fill price in fill_currency
        fill_currency: "GBP" or "USD"
        fx_rate: GBP/USD rate (required if USD)
        atr_value: ATR value for stop calculation
        custom_stop: Optional custom stop price
    
    Returns:
        Updated portfolio and position details
    """
    
    if ticker in portfolio["positions"]:
        raise ValueError(f"{ticker} already exists in portfolio")
    
    is_uk = fill_currency == "GBP" or ticker.endswith(".L")
    market = "UK" if is_uk else "US"
    
    # Calculate costs
    if is_uk:
        gross_cost = shares * fill_price
        stamp_duty = gross_cost * UK_STAMP_DUTY
        total_cost = gross_cost + stamp_duty
        entry_price_with_fees = total_cost / shares
        fees_paid = stamp_duty
        
    else:
        if fx_rate is None:
            raise ValueError("fx_rate required for US stocks")
        
        fill_price_gbp = fill_price / fx_rate
        gross_cost_gbp = shares * fill_price_gbp
        trading_fee = gross_cost_gbp * US_TRADE_FEE
        total_cost = gross_cost_gbp + trading_fee
        entry_price_with_fees = total_cost / shares
        fees_paid = trading_fee
    
    # Calculate initial stop
    if custom_stop:
        initial_stop = custom_stop
    elif atr_value:
        initial_stop = entry_price_with_fees - (5 * atr_value)
    else:
        initial_stop = entry_price_with_fees * 0.90  # Default 10% stop
    
    # Add to portfolio
    portfolio["positions"][ticker] = {
        "entry_date": entry_date,
        "entry_price": round(entry_price_with_fees, 4),
        "fill_price": round(fill_price, 4),
        "fill_currency": fill_currency,
        "fx_rate": fx_rate if not is_uk else None,
        "shares": shares,
        "total_cost": round(total_cost, 2),
        "fees_paid": round(fees_paid, 2),
        "fee_type": "stamp_duty" if is_uk else "trading_fee",
        "initial_stop": round(initial_stop, 2),
        "current_stop": round(initial_stop, 2),
        "current_price": round(entry_price_with_fees, 4),
        "holding_days": 0,
        "pnl": 0.0,
        "pnl_pct": 0.0,
        "market": market,
    }
    
    # Deduct from cash
    portfolio["cash"] -= total_cost
    portfolio["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return portfolio, {
        "ticker": ticker,
        "total_cost": round(total_cost, 2),
        "fees_paid": round(fees_paid, 2),
        "entry_price": round(entry_price_with_fees, 4),
        "initial_stop": round(initial_stop, 2),
        "remaining_cash": round(portfolio["cash"], 2)
    }


def remove_position(portfolio, ticker, exit_price, exit_date=None, fx_rate=None):
    """
    Remove a position programmatically (for API use)
    
    Args:
        portfolio: Portfolio dict
        ticker: Ticker to exit
        exit_price: Exit price
        exit_date: Exit date (defaults to today)
        fx_rate: GBP/USD rate if US stock
    
    Returns:
        Updated portfolio and exit details
    """
    
    if ticker not in portfolio["positions"]:
        raise ValueError(f"{ticker} not found in portfolio")
    
    pos = portfolio["positions"][ticker]
    is_uk = pos.get("market") == "UK"
    
    if exit_date is None:
        exit_date = datetime.now().strftime("%Y-%m-%d")
    
    # Calculate proceeds
    if is_uk:
        exit_price_gbp = exit_price
        sell_fee = 0.0  # No stamp duty on sells
    else:
        if fx_rate is None:
            raise ValueError("fx_rate required for US stock exit")
        exit_price_gbp = exit_price / fx_rate
        sell_fee = exit_price_gbp * pos["shares"] * US_TRADE_FEE
    
    shares = pos["shares"]
    gross_proceeds = shares * exit_price_gbp
    net_proceeds = gross_proceeds - sell_fee
    
    # P&L calculation
    total_cost = pos.get("total_cost", shares * pos["entry_price"])
    pnl = net_proceeds - total_cost
    pnl_pct = (pnl / total_cost) * 100
    
    # Add to trade history
    if "trade_history" not in portfolio:
        portfolio["trade_history"] = []
    
    portfolio["trade_history"].append({
        "ticker": ticker,
        "market": pos.get("market", "Unknown"),
        "entry_date": pos["entry_date"],
        "exit_date": exit_date,
        "shares": shares,
        "entry_price": pos["entry_price"],
        "exit_price": exit_price_gbp,
        "total_cost": total_cost,
        "gross_proceeds": gross_proceeds,
        "net_proceeds": net_proceeds,
        "entry_fees": pos.get("fees_paid", 0),
        "exit_fees": sell_fee,
        "pnl": pnl,
        "pnl_pct": pnl_pct,
        "exit_reason": "Manual Exit",
        "entry_fx_rate": pos.get("fx_rate"),
        "exit_fx_rate": fx_rate if not is_uk else None,
    })
    
    # Add proceeds to cash
    portfolio["cash"] += net_proceeds
    
    # Remove position
    del portfolio["positions"][ticker]
    portfolio["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return portfolio, {
        "ticker": ticker,
        "net_proceeds": round(net_proceeds, 2),
        "pnl": round(pnl, 2),
        "pnl_pct": round(pnl_pct, 2),
        "new_cash_balance": round(portfolio["cash"], 2)
    }


def update_cash(portfolio, amount=None, set_to=None):
    """Update cash balance"""
    
    if set_to is not None:
        portfolio["cash"] = set_to
    elif amount is not None:
        portfolio["cash"] += amount
    else:
        raise ValueError("Provide either amount or set_to")
    
    portfolio["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return portfolio


def view_portfolio(portfolio):
    """Display current portfolio status"""
    
    print("\n" + "=" * 70)
    print("CURRENT PORTFOLIO")
    print("=" * 70)
    
    print(f"\n💷 Cash: £{portfolio['cash']:,.2f}")
    print(f"📊 Number of positions: {len(portfolio['positions'])}")
    
    if len(portfolio["positions"]) > 0:
        print("\n" + "-" * 70)
        print("POSITIONS:")
        print("-" * 70)
        
        total_value = 0
        total_pnl = 0
        total_cost = 0
        
        for ticker, pos in portfolio["positions"].items():
            value = pos["shares"] * pos.get("current_price", pos["entry_price"])
            pnl = pos.get("pnl", 0)
            cost = pos.get("total_cost", pos["shares"] * pos["entry_price"])
            
            total_value += value
            total_pnl += pnl
            total_cost += cost
            
            print(f"\n  {ticker} ({pos.get('market', 'Unknown')})")
            print(f"    Shares: {pos['shares']}")
            print(f"    Entry: £{pos['entry_price']:.4f} (incl. fees)")
            
            if pos.get("market") == "US" and pos.get("fill_price"):
                print(f"    Fill: ${pos['fill_price']:.2f} USD @ {pos.get('fx_rate', 0):.4f}")
            
            print(f"    Entry Date: {pos['entry_date']}")
            print(f"    Total Cost: £{cost:,.2f}")
            print(f"    Fees Paid: £{pos.get('fees_paid', 0):.2f} ({pos.get('fee_type', 'N/A')})")
            print(f"    Current Stop: £{pos.get('current_stop', 'N/A'):.2f}")
            print(f"    Current Value: £{value:,.2f}")
            print(f"    P&L: £{pnl:+,.2f}")
        
        print("\n" + "-" * 70)
        print(f"Total Cost: £{total_cost:,.2f}")
        print(f"Total Value: £{total_value:,.2f}")
        print(f"Total P&L: £{total_pnl:+,.2f}")
        print(f"Portfolio Value: £{portfolio['cash'] + total_value:,.2f}")
    
    if "trade_history" in portfolio and len(portfolio["trade_history"]) > 0:
        print(f"\n📜 Completed trades: {len(portfolio['trade_history'])}")
        total_realized = sum([t["pnl"] for t in portfolio["trade_history"]])
        total_fees = sum([t.get("entry_fees", 0) + t.get("exit_fees", 0) for t in portfolio["trade_history"]])
        print(f"   Total realized P&L: £{total_realized:+,.2f}")
        print(f"   Total fees paid: £{total_fees:,.2f}")
    
    print(f"\nLast updated: {portfolio.get('last_updated', 'N/A')}")


# =====================================================================
# CLI INTERFACE (Optional - for manual use)
# =====================================================================

def main_menu():
    """Interactive menu for manual portfolio management"""
    
    print("\n" + "=" * 70)
    print("PORTFOLIO SETUP & MANAGEMENT")
    print("=" * 70)
    
    # Check if portfolio exists
    portfolio = load_portfolio()
    
    if portfolio is None:
        print("\nNo portfolio found.")
        create = input("Create new portfolio? (y/n): ").lower()
        if create == "y":
            cash = float(input("Enter starting cash balance (£): "))
            portfolio = create_new_portfolio(cash)
        else:
            print("Exiting...")
            return
    
    while True:
        print("\n" + "-" * 70)
        print("OPTIONS:")
        print("  1. View portfolio")
        print("  2. Update cash balance")
        print("  3. Save and exit")
        print("  4. Exit without saving")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            view_portfolio(portfolio)
        
        elif choice == "2":
            print(f"\nCurrent cash: £{portfolio['cash']:,.2f}")
            action = input("(a)dd cash or (s)et to specific amount? (a/s): ").lower()
            
            if action == "a":
                amount = float(input("Amount to add (£): "))
                portfolio = update_cash(portfolio, amount=amount)
                print(f"✓ Added £{amount:,.2f}. New balance: £{portfolio['cash']:,.2f}")
            elif action == "s":
                amount = float(input("Set cash to (£): "))
                portfolio = update_cash(portfolio, set_to=amount)
                print(f"✓ Cash set to £{amount:,.2f}")
        
        elif choice == "3":
            save_portfolio(portfolio)
            print("\n✓ Portfolio saved. Goodbye!")
            break
        
        elif choice == "4":
            print("\nExiting without saving...")
            break
        
        else:
            print("Invalid option")


if __name__ == "__main__":
    main_menu()