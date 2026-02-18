# Product Changelog — Momentum Trading Assistant

**Owner:** Product Owner  
**Class:** Planning Document (Class 4)  
**Status:** Active  
**Last Updated:** 2026-02-18

> This document is a human-maintained record of what was shipped in each product version and when. It records delivery milestones and notable decisions. It is not an immutable system record — for point-in-time system status reports, see `docs/operations/status_reports/`.

---

## v1.4 — Trade Journal & Analytics (February 2026)

### Trade Journal & Notes System ✅ Complete

- Entry notes when creating positions (500 character limit)
- Exit notes when closing positions (500 character limit)
- Tag system for categorising trades, with autocomplete from existing tags
- Tag validation: lowercase, hyphens only
- Tag filtering in trade history (OR logic)
- Expandable trade rows showing full journal entries
- Journal view mode in Positions page
- Visual entry/exit note cards with colour-coded headers
- Strategy tag pills with gradient styling
- Database schema updates: `entry_note`, `exit_note`, `tags` fields on positions and trade history
- GIN indexes on tags fields for fast filtering
- Backend endpoints: updateNote, updateTags, getTags

### Performance Analytics ⏳ In Progress

- R-multiple tracking
- Drawdown analysis
- Underwater chart visualisation

---

## v1.3 — System Health & Monitoring (February 2026)

- Health check endpoint (`GET /health`) for load balancers
- Detailed system status (`GET /health/detailed`)
- Automated endpoint testing (`POST /test/endpoints`) — 11 endpoints
- Frontend status dashboard page with real-time monitoring
- Component-level health checks: Database, Yahoo Finance, Services, Config
- One-click endpoint testing with pass/fail results
- Auto-refresh at 5-second intervals
- Response time tracking
- 100% test pass rate monitoring established

---

## v1.2 — Exit Flexibility & Backend Refactor (February 2026)

### Exit Features

- Partial exit support: specify share count to exit
- Custom exit date for backdating reconciliation
- User-provided exit price from actual broker execution
- User-provided FX rate for US stocks (from broker statement)
- Exit reason selection dropdown
- Detailed fee breakdown in exit response
- Proportional cost basis calculation for partial exits

### Backend Architecture

- Complete refactor to service layer architecture
- 67% code reduction in `main.py` (1,439 → 470 lines)
- Five service modules: position, portfolio, trade, cash, signal
- Clean separation of concerns: HTTP → Service → Utils → Database
- 100% testable business logic

---

## v1.1 — Cash Management & Portfolio History (early 2026)

- Deposit and withdrawal tracking
- Transaction history
- Accurate P&L accounting incorporating cash flows
- Cash management modal UI
- Daily portfolio snapshots
- Historical performance data
- Performance chart visualisation
- Automated snapshot creation via cron

---

## v1.0 — Initial Release

### Core Trading Features

- Portfolio management
- Manual position entry with fractional share support
- Daily position analysis
- ATR-based trailing stops
- Grace period (10 calendar days, stop calculated but not enforced)
- Market regime detection: SPY / FTSE vs 200-day moving average
- Multi-currency support: USD and GBP
- Live price fetching via Yahoo Finance
- Fee calculation: UK (commission + stamp duty), US (FX fees)

### Dashboard & UI

- Responsive dashboard with draggable widgets
- Portfolio value display
- Open positions summary
- Total P&L tracking
- Cash balance management
- Dark mode UI

### Technical Infrastructure

- PostgreSQL database
- FastAPI backend
- React frontend with TanStack Query
- Real-time FX rate conversion
- Error handling and validation
- Production deployment on Render
- Frontend hosting on GitHub Pages
