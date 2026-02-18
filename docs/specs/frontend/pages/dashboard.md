# dashboard.md

**Owner:** Frontend Specifications & UX Documentation Owner  
**Status:** Canonical  
**Version:** 1.0
**Last Updated:** February 18, 2026

## Purpose & User Goals
The Dashboard provides a high‑level overview of the user’s portfolio and current market conditions.  
It serves as the primary entry point for daily monitoring and quick navigation to key workflows.

Users should be able to quickly understand:
- Total portfolio performance  
- Current cash and position values  
- Recent performance trends  
- Market regime signals  
- What actions they should take next (e.g., review positions, enter a new trade)

---

## Layout Structure

### Header (global)
- App name/logo  
- Navigation: Dashboard, Positions, Trade Entry, Trade History, Settings  
- Theme toggle (Dark/Light)

### Main Content

#### Portfolio Summary Cards
- **Total portfolio value**  
- **Cash balance** (clickable → opens cash management modal)  
- **Open positions value**  
- **Total P&L**

#### Market Status
- Displays market regime indicator (e.g., SPY / FTSE risk on/off)
- Clear visual status indicator (color-coded)

#### Performance Chart
- 30‑day portfolio performance trend
- Line or area chart (implementation choice, UX intent is trend visibility)

#### Quick Actions
- **Go to Positions**  
- **Enter New Position**  
- **Daily Monitor** (runs automated position analysis)

---

## Key Components Used
- Summary value cards  
- Performance chart component  
- Link/button group for quick actions  
- Cash Management Modal (triggered from cash balance)  
- Global navigation header  

---

## States

### Loading State
- Skeleton or spinner while:  
  - Portfolio summary loads  
  - Performance chart loads  

### Empty State
Occurs when:
- No portfolio exists  
- No positions have been added  

Display:
- Friendly message explaining the next step  
- Action: “Enter New Position”

### Error State
- Global error banner for API failures  
- Retry option for failed data fetches

---

## Responsive Behavior
- Cards stack vertically on small screens  
- Chart becomes smaller or scrollable horizontally if needed  
- Quick actions wrap into two rows  
- Cash modal becomes full‑screen on mobile  

---

## UX Notes
- The Dashboard should answer “How am I doing today?” instantly.  
- Important numeric values must be readable at a glance.  
- Market regime and total P&L should be visually distinct.  
- Quick actions should be high‑visibility and require minimal cognitive load.  
- Cash balance being clickable must feel discoverable (use affordances like underlined text, icon, or card hover state).  

---
