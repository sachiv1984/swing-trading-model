# Frontend Functional Specification (React SPA)

## Overview
This document defines the frontend requirements for the Position Manager Web App, a React Single Page Application (SPA).  
The frontend will connect to backend APIs (OpenAPI spec) to manage portfolio creation, position entry, daily monitoring, and trade history.

---

# 1. General Requirements

## 1.1 UI Framework
- React (SPA)
- Recommended: TypeScript
- UI library: TailwindCSS or Material UI (developer choice)
- State management: React Context or Redux (developer choice)
- Routing: React Router

## 1.2 Theme
- Default: **Dark Mode**
- Optional: Light Mode toggle
- Theme persistence: store user preference in `localStorage`

## 1.3 Authentication
- Initially no authentication required (local demo mode)
- Optionally add authentication later (OAuth or JWT)

## 1.4 Error Handling
- Global error banner for API failures
- Inline error messages for forms
- Retry button for failed API calls

---

# 2. Pages & Components

## 2.1 Global Layout
**Header**
- App name/logo
- Theme toggle (Dark/Light)
- Navigation links:
  - Dashboard
  - Positions
  - Trade Entry
  - Trade History
  - Settings

**Footer**
- Version
- Support link
- Link to documentation

---

# 3. Page Specifications

---

## 3.1 Dashboard (Home)

### Purpose
Show portfolio summary, risk status, and quick actions.

### Data Display
- Total portfolio value
- Cash balance
- Open positions value
- Total P&L
- Market status (SPY / FTSE risk on/off)

### Actions
- Button: “Go to Positions”
- Button: “Enter New Position”
- Button: “Daily Monitor” (run position manager)

### API Integration
- `GET /portfolio`
- `GET /positions/summary`
- `GET /market/regime`

---

## 3.2 Positions Page

### Purpose
List open positions with current stop levels and P&L.

### UI Elements
- Table/List of positions:
  - Ticker
  - Market
  - Entry price
  - Current price
  - Stop price
  - Shares
  - P&L
  - Days held
  - Action buttons:
    - “Edit”
    - “Exit”

### API Integration
- `GET /positions`
- `GET /positions/{ticker}`
- `POST /positions/{ticker}/exit` (manual exit)

---

## 3.3 Position Detail Modal / Page

### Purpose
Show position detail and stop logic.

### UI Elements
- Entry details
- Current price
- Stop levels
- Risk status
- Graph (optional)
- Manual stop override

### API Integration
- `GET /positions/{ticker}`
- `PUT /positions/{ticker}`

---

## 3.4 Trade Entry Page

### Purpose
Add a new position manually (manual entry).

### Inputs
- Ticker
- Market (UK/US auto-detected)
- Entry date
- Shares
- Fill price
- FX rate (if US)
- ATR value
- Initial stop (auto-calculated)

### Output
- Fee breakdown
- Total cost
- Confirmation button

### API Integration
- `POST /positions`

---

## 3.5 Trade History Page

### Purpose
View closed trades and performance metrics.

### UI Elements
- Table of trade history:
  - Ticker
  - Entry date
  - Exit date
  - P&L
  - % P&L
  - Exit reason
- Filters:
  - Date range
  - Win/Loss
  - Market

### API Integration
- `GET /trades`

---

## 3.6 Settings Page

### Purpose
Configure strategy parameters and portfolio settings.

### Settings
- Minimum hold days
- ATR multipliers
- ATR period
- Default currency
- Theme preference (Dark/Light)

### API Integration
- `GET /settings`
- `PUT /settings`

---

# 4. UI State & Flow

## 4.1 Portfolio Load Flow
1. App loads
2. Fetch portfolio data
3. If no portfolio exists → prompt user to create one
4. Redirect to Dashboard

## 4.2 Daily Monitor Flow
1. User clicks “Daily Monitor”
2. Fetch current prices + market regime
3. Display list of HOLD vs EXIT
4. User confirms exit
5. App updates portfolio

---

# 5. Accessibility
- Use semantic HTML
- Ensure keyboard navigation
- Color contrast for dark theme
- ARIA labels for tables & buttons

---

# 6. Responsive Design
- Mobile-first layout
- Table collapses into cards on mobile
- Sidebar navigation becomes hamburger menu

---

# 7. Future Enhancements
- Authentication
- Charts & visualizations
- Notifications (email/SMS)
- Export to CSV / PDF
- Multi-portfolio support

---

# 8. API Integration Map

| Page | API Endpoint | Purpose |
|------|--------------|---------|
| Dashboard | `GET /portfolio` | Get portfolio summary |
| Positions | `GET /positions` | Get open positions |
| Position Detail | `GET /positions/{ticker}` | Get position details |
| Trade Entry | `POST /positions` | Create new position |
| Trade Exit | `POST /positions/{ticker}/exit` | Exit position |
| Trade History | `GET /trades` | Get completed trades |
| Settings | `GET /settings` | Get config |
| Settings | `PUT /settings` | Update config |