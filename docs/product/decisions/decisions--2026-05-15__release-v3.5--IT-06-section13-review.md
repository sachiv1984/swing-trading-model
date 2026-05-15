**Owner:** Strategy Rules & System Intent Owner
**Class:** Operational Record (Class 3)
**Status:** Draft — Awaiting Strategy Rules & System Intent Owner Sign-off
**Last Updated:** 2026-05-15
**Cycle:** 2026-05-15__release-v3.5
**Story:** ST-01 (EPIC-01, v3.5)

---

# §13 Boundary Review — IT-06: Alpaca Paper Trading Integration

**Feature:** IT-06 — Alpaca Paper Trading Sync Service + Paper Account Display Panel
**Review type:** §13 System Boundary Compliance Review
**Cycle:** 2026-05-15__release-v3.5
**Governance reference:** `claude/strategy/strategy_rules.md §13`
**UX spec:** `docs/ux_specs/paper-trading/ux_spec.md` v1.0

---

## Review Summary

This record documents the formal §13 boundary review required before IT-06 implementation stories (ST-02 — backend sync service, ST-03 — frontend panel) may proceed. Per sprint planning decisions, ST-01 (this review) must produce a PASS or FAIL determination before any IT-06 implementation begins.

---

## §13 Boundary Criteria (from strategy_rules.md §13)

### §13.1 — This system IS:
- A deterministic decision-support engine
- A risk-managed momentum framework
- A single, explicit, human-designed strategy
- Human-in-the-loop by design

### §13.2 — This system is NOT:
- An automated trading bot
- A broker execution engine
- A discretionary or adaptive rule system
- A multi-strategy or configurable strategy platform
- A machine-learning or AI-driven prediction system
- An options or futures trading system
- A real-time streaming or execution system

---

## IT-06 Feature Description

IT-06 implements two components:

**ST-02 — Backend Sync Service:**
- New endpoint: `GET /portfolio/paper-positions`
- Reads positions from an Alpaca paper (simulation) account linked via API key
- Returns paper position data for display: entry price, current market price, P&L comparison, date opened, size
- When credentials absent: returns `{"paper_tracking_enabled": false}` — panel is hidden
- No POST/PUT/DELETE operations against Alpaca — read-only sync

**ST-03 — Frontend Display Panel:**
- Read-only panel on the Positions page (Table View only)
- Displays paper account positions alongside real positions
- No action buttons (no exit, no plan, no order submission)
- Panel hidden when credentials not configured
- US-market tickers only

**§13 compliance statement from UX spec §5:**
> "Positions created only by human action via the primary system workflow (human-initiated position open). This panel is display-only — no automated recommendation or order execution. Hypothetical P&L shown is for tracking purposes only; no signal is generated from it."

---

## §13 Compliance Assessment

### Compliance criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| Feature provides information only — no automated decision | ✅ COMPLIANT | Panel is display-only; P&L comparison is factual, not advisory |
| No automated order execution | ✅ COMPLIANT | Backend sync is GET-only; no orders placed against Alpaca API |
| No real capital involved | ✅ COMPLIANT | Alpaca paper account is a simulation account; no real funds |
| Human-in-the-loop preserved | ✅ COMPLIANT | User manages paper account independently; system only reads from it |
| No automated advisory generated | ✅ COMPLIANT | P&L display shows facts; no recommendation or signal generated from paper data |
| Not a broker execution engine | ✅ COMPLIANT | System does not place, modify, or cancel any orders (paper or real); read-only sync only |
| Not a real-time streaming system | ✅ COMPLIANT | Sync is request-driven (page load / refresh); no persistent streaming connection |
| No cross-contamination with real position logic | ✅ COMPLIANT | Paper panel is isolated display; no paper P&L fed into signals, screener, or position-sizing logic |

### Critical §13 boundary — paper order creation

The most sensitive §13 question for IT-06 is: **does the system create paper orders in Alpaca as part of the position-open workflow?**

Based on the IT-06 spec:
- The backend implements `GET /portfolio/paper-positions` only — no write endpoints against Alpaca
- UX spec §4: "No interaction with real positions: the panel is read-only display."
- Sprint backlog ST-02 notes: single endpoint `GET /portfolio/paper-positions`

**Assessment:** The system does NOT create or place paper orders. It reads an Alpaca paper account that the user manages independently. The UX spec §5 note "Positions created only by human action via the primary system workflow" is interpreted as: the user independently manages their Alpaca paper account; the sync service reads the positions they have opened there. This is consistent with the read-only backend implementation.

This interpretation must be confirmed by the Strategy Rules & System Intent Owner before sign-off. If the implementation requires the backend to CREATE paper positions in Alpaca (as opposed to read them), this determination must be re-evaluated.

### Gate status (preliminary)

**Preliminary determination: PASS** — subject to Strategy Rules & System Intent Owner sign-off confirming:
1. The backend sync service is read-only (GET operations against Alpaca API only; no order placement)
2. The Alpaca paper account is managed independently by the user; the system does not place, modify, or cancel any paper orders
3. No paper P&L data is fed into real-system signals, screener logic, or position-sizing calculations
4. Any future extension to IT-06 that introduces automated paper order creation requires a new §13 review

---

## §13 Conditions for Implementation

If PASS is confirmed, the following conditions apply to ST-02 and ST-03 implementation:

1. **Read-only Alpaca API access only:** Implementation must not include any POST, PUT, PATCH, or DELETE calls to the Alpaca API. If order placement is needed in any future extension, a new §13 review is required.
2. **No automated paper order generation:** No paper position may be created, modified, or closed by the system automatically. The Alpaca paper account reflects only positions the user has established independently.
3. **Paper data isolation:** Paper account P&L and position data must not be used as an input to signals, screener scoring, regime detection, or position-sizing logic.
4. **Display-only panel:** The frontend panel must remain read-only with no action buttons that interact with the Alpaca API.
5. **§13 compliance note required in service file:** Per sprint backlog ST-02 notes — a §13 compliance comment must appear in the backend sync service file.

---

## FAIL Implications (if applicable)

If the Strategy Rules & System Intent Owner determines this is a FAIL:
- ST-02 and ST-03 are removed from Sprint 2 scope
- A closure note is added to the IT-06 roadmap entry
- The freed Sprint 2 capacity (~4–5 days) is reallocated to EPIC-02 (Arc 4 Foundation) per sprint planning notes
- PMO Lead is notified for capacity re-assessment

---

## Sign-Off

**Signed off by:** —
**Date:** —
**Determination:** PASS / FAIL (delete as applicable)
**Comments:** —
