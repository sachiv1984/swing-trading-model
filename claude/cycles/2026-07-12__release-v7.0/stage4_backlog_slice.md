Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Committed
Release: v7.0
Cycle: 2026-07-12__release-v7.0
Last Updated: 2026-07-12

# Release Backlog Slice — v7.0

## EPIC-01 — Positions Grid View Parity
Maps to: S2-01
Owner: Head of Engineering

### ST-01 (BLG-SPEC-80) — `positions.md` Grid View badge placement subsection
Priority: P2 | Effort: S
Problem: `positions.md` documents the Alerts column as canonical for Table View; Grid View badge placement was never separately specified — the root cause behind `BLG-FE-102`.
Acceptance Criteria:
- `positions.md` updated with an explicit Grid View badge-placement subsection
- `BLG-FE-102` implementation can cite the spec directly

### ST-02 (BLG-FE-102) — Positions Grid View missing RISK OFF badge
Priority: P2 | Effort: S (~0.25-0.5 day)
Problem: `PositionCard.js` (Grid View) shows the GAP RISK badge but no RISK OFF badge, despite `positions.md` requiring one when `risk_off_exit = true`; Table View already implements it.
Acceptance Criteria:
- Grid View position cards show a RISK OFF badge when `risk_off_exit = true`, matching Table View's condition logic
- Visual treatment matches spec (deep blue `#1E40AF`, "RISK OFF" label)
- Badge coexists cleanly with the GAP RISK badge when both apply to the same position
- No change to Table View behaviour

### ST-03 (BLG-FE-97) — Positions Grid View missing trailing-stop value and breach indicator
Priority: P2 | Effort: S (~0.5 day)
Problem: `PositionCard.js` shows only a generic "Stop" value with no `current_trailing_stop` display or breach indicator; Grid View users lack trailing-stop visibility that Table View users already have.
Acceptance Criteria:
- Grid View position cards show both Initial Stop and current trailing stop values
- Breach state shown via icon only (not a full badge/pill), matching Table View's breach condition logic
- No change to Table View behaviour

### ST-04 (BLG-QA-95) — Positions Grid View badge parity Playwright coverage
Priority: P2 | Effort: S
Problem: `qa_evidence_EPIC-02.md` (v6.9) confirms `SC-RO-*` verifies Alerts-column badges via Table View only; no Grid View Playwright equivalent exists.
Acceptance Criteria:
- Grid View badge scenarios pass in CI for both RISK OFF and GAP RISK badge types
- Parity with existing `SC-RO-*` Table View coverage confirmed

### ST-05 (BLG-FE-104) — GAP RISK / RISK OFF combined-badge visual differentiation review
Priority: P2 | Effort: S
Problem: v6.9 added a second badge type (GAP RISK) into the same Alerts column as RISK OFF; no design review confirmed the two remain visually distinguishable when both fire simultaneously — safety-relevant, not cosmetic.
Acceptance Criteria:
- Combined-badge state reviewed and confirmed distinguishable, or a fix is specified and implemented

---

## EPIC-02 — v6.9 Carryover Fixes & Reconciliation
Maps to: S2-02
Owner: Head of Engineering

### ST-06 (BLG-SPEC-71) — Reports.js Tax Year P&L tab spec reconciliation
Priority: P2 | Effort: S (~0.5 day)
Problem: `reports.md` §Arc 5 Compliance Summary and §Gross vs Net Comparison both carry changelog entries implying these sections were added to the Tax Year P&L tab; neither is actually rendered in `Reports.js`. Confirmed spec-only (never implemented), not a regression.
Acceptance Criteria:
- AC-01: `reports.md`'s description of the Tax Year P&L tab matches what `Reports.js` actually renders
- AC-02: If sections are subsequently implemented (as new `BLG-FEAT` items), Playwright coverage added per the CLAUDE.md frontend-visible-change rule
- AC-03: Root cause documented (spec-authoring stories' changelog entries indistinguishable from shipped-feature entries)

### ST-07 (BLG-BE-50) — Instrument trailing-stop recommendation capture for `trailing_stop_action_rate` metric
Priority: P2 | Effort: S (~1 day)
Problem: `metrics_definitions.md` §Trailing Stop Action Rate cannot be computed — neither the `GET /positions/{id}/stop-trail` recommendation nor its potential follow-up `PATCH` is currently logged/linked.
Acceptance Criteria:
- `trailing_stop_recommendation_log` table created and populated on every `GET /positions/{id}/stop-trail` call
- `trailing_stop_action_rate` computable via the query approach documented in `metrics_definitions.md`
- Capture window (24-hour proposal) confirmed by Product Owner

### ST-08 (BLG-FE-95) — Dashboard/StrategyBenchmark page-title light-theme contrast gap
Priority: P3 | Effort: XS (<1h)
Problem: Primary page headings use bare `text-white` with no light-theme value — insufficient contrast on light theme. Same defect class as BLG-FE-87/88 (fixed v6.7).
Acceptance Criteria:
- Both named headings pass WCAG AA contrast (≥4.5:1) against both light and dark backgrounds
- No visual change on dark theme

### ST-09 (BLG-FE-96) — Positions Table View breach badge does not match approved spec colour/label
Priority: P3 | Effort: XS (<1h)
Problem: Shipped breach badge uses `bg-rose-800/80 text-rose-200`/"Breach" instead of the approved spec's orange `#EA580C`/"⚠ BREACH", undermining the spec's stated visual-distinctness rationale.
Acceptance Criteria:
- Breach badge renders with `#EA580C` background and "⚠ BREACH" label, matching `positions.md` §Trailing Stop Column
- No other Table View styling changed

### ST-10 (BLG-SPEC-73) — Gate Progress Indicator copy divergence
Priority: P3 | Effort: XS (<1h)
Problem: `dashboard.md` §6 and shipped `GateProgressStrip.js` disagree on Gate Progress Indicator copy; unclear which is canonical.
Acceptance Criteria:
- `dashboard.md` §6 and `GateProgressStrip.js` use identical copy
- Known Deviations note in `dashboard.md` §6 removed once resolved
- Wording-only AC — code review of static JSX/text may substitute for staging sign-off per CLAUDE.md FI-P3-02 exception (no visual/colour/layout change)

### ST-11 (BLG-BE-51) — Add endpoint and date-range filters to `GET /ai/claude-audit-log`
Priority: P3 | Effort: XS (<1h)
Problem: Endpoint only accepts `limit`; no server-side filter by `endpoint` or date range, forcing over-fetch for cost-trend analysis.
Acceptance Criteria:
- `GET /ai/claude-audit-log?endpoint=POST%20/ai/daily-briefing` returns only matching rows
- `date_from`/`date_to` filters work independently and combined with `endpoint`
- Existing unfiltered behaviour unchanged
- `docs/specs/api_contracts/ai_endpoints.md` and `docs/reference/openapi.yaml` updated in the same commit (no new endpoint, but per CLAUDE.md contract-currency practice for parameter additions)

### ST-12 (BLG-BE-38) — Sector Concentration: join `ticker_universe` for sector data
Priority: P2 | Effort: XS (~2 hours)
Problem: `GET /portfolio/sector-weights` never joins `ticker_universe`, so every position shows "Unclassified" regardless of actual sector data.
Acceptance Criteria:
- AC-01: Sector Concentration panel shows correct sector tiles for positions whose tickers exist in `ticker_universe` with a non-null sector
- AC-02: Positions with no sector in `ticker_universe` still render as "Unclassified" (fallback preserved)
- AC-03: `GET /portfolio/concentration-status` sector breach calculation also reflects correct sectors
- AC-04: No yfinance live-call added to the hot path

---

## EPIC-03 — User-Facing Feature Enhancements
Maps to: S2-03
Owner: Financial Reporting & Records Owner

### ST-13 (BLG-FEAT-69) — Tax-year P&L CSV export
Priority: P3 | Effort: M (~2 days)
Problem: No export mechanism exists for the monthly/tax-year P&L report.
Acceptance Criteria:
- User can export a tax-year P&L as CSV
- Exported figures match the on-screen report

### ST-14 (BLG-FEAT-70) — Realized vs. unrealized gain distinction in monthly P&L
Priority: P3 | Effort: M (~2 days)
Problem: Monthly P&L report shows a single combined figure; user cannot distinguish realized (closed) from unrealized (open) gains.
Acceptance Criteria:
- Report shows realized and unrealized gain figures separately
- Figures sum to the existing combined total (regression check)

### ST-15 (BLG-FEAT-68) — Position review cadence nudge
Priority: P3 | Effort: S (~1 day)
Problem: Existing prompts (Grace Period, Drawdown) only fire on price/performance triggers; a quietly-performing position can go unreviewed indefinitely.
Acceptance Criteria:
- AC-01: Positions display days-since-last-review
- AC-02: Positions past the threshold (default 14 days) are visually flagged, independent of P&L state
- AC-03: An explicit "Mark Reviewed" action resets the counter
- AC-04: Flag does not fire for positions already flagged by Grace Period or Drawdown prompts

---

## Summary

| EPIC | Stories | Total Effort (mid-point) |
|------|---------|---------------------------|
| EPIC-01 | ST-01..ST-05 (5) | ~2.35 days |
| EPIC-02 | ST-06..ST-12 (7) | ~2.15 days |
| EPIC-03 | ST-13..ST-15 (3) | ~5 days |
| **Total** | **15** | **~9.5 days** |
