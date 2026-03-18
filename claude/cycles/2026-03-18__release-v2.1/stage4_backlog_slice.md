**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.1
**Cycle:** 2026-03-18__release-v2.1
**Last Updated:** 2026-03-18

---

# Sprint Backlog Slice — v2.1 Alerts, Watchlists & Enhancements

---

## EPIC-01 — Notification Architecture

**Maps to:** S2-01
**Effort:** S (~4–6 hrs total)
**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Sprint:** 1 (must be first story; completion unlocks EPIC-02)

### ST-01 — Author async notification delivery ADR (BLG-TECH-08)

**Type:** Architecture Decision Record
**Effort:** S (~4–6 hrs)
**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Delegation:** Delegated (architecture decision within Head of Engineering domain)

**Description:** Author the Architecture Decision Record for notification delivery architecture. Evaluate: (a) synchronous inline delivery (email sent on the API response path — simpler, no infrastructure change), and (b) asynchronous delivery via background worker + task queue (Celery + Redis or equivalent — more scalable but adds worker infrastructure). Decision must be grounded in current single-user, self-hosted deployment context. The ADR decision directly controls how ST-02 (Alerts spec) is written — the spec cannot be stable without it.

**Acceptance Criteria**
- ADR file created: `docs/adr/ADR-003-notification-delivery-architecture.md` (or next available ADR number)
- ADR covers: problem statement, options considered (sync vs async), decision, rationale, consequences, trade-offs
- Rationale is appropriate to current scale (single-user, self-hosted)
- If async decided: spike or proof of concept for worker setup confirmed feasible in staging — output documented in ADR
- `docs/specs/api_contracts/backend_engineering_patterns.md` updated with decision reference
- Head of Engineering sign-off obtained and recorded
- Sprint Planning Engine verifies this item is Complete (signed off) before sealing any EPIC-02 sprint story

---

## EPIC-02 — Alerts & Notifications

**Maps to:** S2-02
**Effort:** M–H (~34–60 hrs total)
**Owner:** Head of Engineering + Base44 Frontend + Director of Quality
**Sprint:** 2–3 (conditional — EPIC-01 ST-01 must be Complete before any ST-02–ST-07 sprint story seals)
**Condition:** ST-01 (BLG-TECH-08 ADR) must be Complete with Head of Engineering sign-off before sprint planning seals any story in this EPIC.

### ST-02 — Spec: alerts endpoint + notification preference model

**Type:** Spec
**Effort:** M (~6–10 hrs)
**Owner:** Head of Specs Team + Head of Engineering
**Delegation:** Delegated (spec authoring under Head of Specs Team authority)
**Depends on:** ST-01 complete (ADR decision must be known before spec is stable)

**Description:** Author the alerts endpoint spec and notification preference model. Define: alert rule types (stop loss approach, grace period warning days 8–9, market regime change to risk-off, daily portfolio summary), endpoint paths for alert rules CRUD, notification preference schema (per-user, per-alert-type on/off, email + SMS flags), and database schema extensions required.

**Acceptance Criteria**
- `docs/specs/api_contracts/alerts_endpoints.md` created with full endpoint definitions
- Alert rule types defined per roadmap description; database schema specified in `docs/specs/data_model.md`
- Notification preference model defined (per-user, per-type configuration)
- `openapi.yaml` updated in same commit as endpoint spec
- Registered in `docs/specs/Specs_Index.md`
- Head of Specs Team sign-off obtained
- Architecture mode (sync/async) per ADR is reflected in the spec

---

### ST-03 — Backend: alert rules engine

**Type:** Backend implementation
**Effort:** M–H (~10–18 hrs)
**Owner:** Head of Engineering
**Delegation:** Delegated
**Depends on:** ST-02 (spec must be signed off)

**Description:** Implement the alert rules evaluation engine per ST-02 spec. For each alert type, implement the triggering logic: (a) stop loss approach — trigger when current stop is within N% of price; (b) grace period warning — trigger on days 8–9; (c) market regime change — trigger on risk-off transition; (d) daily portfolio summary — scheduled trigger. Engine must be testable in isolation.

**Acceptance Criteria**
- Alert rules engine implemented per ST-02 spec for all 4 alert types
- Alert evaluation can be triggered programmatically (for testing)
- Unit tests for each alert trigger condition
- No test failures on CI
- Head of Engineering sign-off on implementation

---

### ST-04 — Backend: notification delivery (email)

**Type:** Backend implementation
**Effort:** M (~8–12 hrs)
**Owner:** Head of Engineering
**Delegation:** Delegated
**Depends on:** ST-02 (spec), ST-01 (architecture decision determines delivery approach)

**Description:** Implement notification delivery per the architecture decision in ST-01 ADR. If sync: implement inline email sending triggered by alert evaluation on API response path. If async: implement background worker + task queue integration (Celery+Redis or equivalent per ADR PoC). Email format: clear subject, relevant alert data, user-readable message.

**Acceptance Criteria**
- Email notification delivered for each of the 4 alert types when triggered
- Implementation follows architecture decision (sync/async per ST-01 ADR)
- Email delivery confirmed in staging (integration test or manual verification)
- If async: worker infrastructure provisioned in staging and confirmed operational
- Director of Quality sign-off (delivery confirmed in staging)

---

### ST-05 — Frontend: notification preferences page

**Type:** Frontend implementation
**Effort:** S–M (~4–8 hrs)
**Owner:** Base44 Frontend
**Delegation:** Delegated
**Depends on:** ST-02 (spec must define preference model)

**Description:** Implement the notification preferences page per ST-02 spec. Allow users to configure which alerts they receive and via which channels (email, SMS if applicable). Settings persisted via API endpoints defined in ST-02.

**Acceptance Criteria**
- Notification preferences page implemented per spec
- Per-user, per-alert-type toggles rendered correctly
- Settings changes persisted via API (confirmed in staging)
- Page spec cross-referenced (`docs/specs/frontend/pages/notifications.md` or equivalent — author or reference if not yet existing)
- Director of Quality sign-off

---

### ST-06 — Frontend: in-app notification feed

**Type:** Frontend implementation
**Effort:** S–M (~4–8 hrs)
**Owner:** Base44 Frontend
**Delegation:** Delegated
**Depends on:** ST-02 (spec must define notification feed schema)

**Description:** Implement the in-app notification feed per spec. Display recent notifications in a feed view. Support mark-as-read. Integrate with the notifications endpoint defined in ST-02.

**Acceptance Criteria**
- In-app notification feed rendered per spec
- Notifications displayed on page load (or real-time if async architecture supports it)
- Mark-as-read functionality implemented
- Empty state handled gracefully
- Director of Quality sign-off

---

### ST-07 — QA: notification delivery test scenarios

**Type:** QA / Test Documentation
**Effort:** S (~2–4 hrs)
**Owner:** QA & Testing Owner + Director of Quality
**Delegation:** Delegated

**Description:** Author test scenarios for the complete notifications feature. Cover: each alert trigger condition, notification preference settings, email delivery, in-app feed, and integration between the alert rules engine and delivery mechanism.

**Acceptance Criteria**
- `docs/testing/notifications_scenarios.md` created
- Scenarios cover: all 4 alert trigger conditions, preference configuration (on/off per type), email delivery confirmed, in-app feed displays, mark-as-read
- Director of Quality sign-off on scenario coverage

---

## EPIC-03 — Watchlists & Screening

**Maps to:** S2-03
**Effort:** M (~20–36 hrs total)
**Owner:** Head of Engineering + Base44 Frontend + Data Model & Domain Schema Owner
**Sprint:** 3 (Next-horizon initiative; starts after EPIC-02 Phase 1 in Sprint 2)

### ST-08 — Spec: watchlist data model + API endpoints

**Type:** Spec
**Effort:** S–M (~4–8 hrs)
**Owner:** Head of Specs Team + Data Model & Domain Schema Owner
**Delegation:** Delegated (spec authoring)

**Description:** Author the watchlist spec. Define: watchlist data model tables (ticker, target_entry, stop_fields, signal_status_link), API endpoints (GET/POST/PATCH/DELETE /watchlist), signal integration (how entry signal status is surfaced for watchlist tickers), and the quick-add-to-position-entry-modal interface contract.

**Acceptance Criteria**
- `docs/specs/api_contracts/watchlist_endpoints.md` created with full endpoint definitions
- `docs/specs/data_model.md` updated with watchlist tables and migration note
- `openapi.yaml` updated in same commit as endpoint spec
- Registered in `docs/specs/Specs_Index.md`
- Head of Specs Team + Data Model & Domain Schema Owner sign-off obtained

---

### ST-09 — Backend: watchlist implementation

**Type:** Backend implementation
**Effort:** M (~10–16 hrs)
**Owner:** Head of Engineering
**Delegation:** Delegated
**Depends on:** ST-08 (spec + data model must be signed off)

**Description:** Implement watchlist backend per ST-08 spec. Include: new database tables (with migration), CRUD endpoints, signal status integration (surfacing entry signal for each watchlist ticker), and unit + integration tests.

**Acceptance Criteria**
- GET/POST/PATCH/DELETE /watchlist endpoints implemented per spec
- Database migration authored and documented
- Signal status correctly surfaced for each watchlist ticker (integration with existing signals logic)
- Integration tests passing
- `openapi.yaml` updated in same commit as implementation (if not already done in ST-08)
- Head of Engineering sign-off

---

### ST-10 — Frontend: watchlist UI

**Type:** Frontend implementation
**Effort:** M (~8–14 hrs)
**Owner:** Base44 Frontend
**Delegation:** Delegated
**Depends on:** ST-08 (spec), ST-09 (backend endpoints live in staging)

**Description:** Implement the watchlist UI per spec. Display: monitored tickers with entry signal status, target entry price, stop fields. Provide quick-add mechanism from the position entry modal. New watchlist items can be added and removed.

**Acceptance Criteria**
- Watchlist page implemented per spec
- Each ticker shows: entry signal status, target entry, stop fields
- Quick-add to watchlist from position entry modal functional
- Add/edit/remove watchlist entries functional
- Empty state handled gracefully
- Director of Quality sign-off (QA against staging)

---

## EPIC-04 — Chart Interactivity Enhancements

**Maps to:** S2-04
**Effort:** S–M (~5–10 hrs total)
**Owner:** Base44 Frontend
**Sprint:** 1 (independent; quick win)

### ST-11 — Implement chart interactivity (CHART-IX)

**Type:** Frontend implementation
**Effort:** S–M (~5–10 hrs)
**Owner:** Base44 Frontend
**Delegation:** Delegated (UI enhancement within existing analytics page)

**Description:** Add interactivity to the 3 existing analytics page charts: (1) underwater equity curve, (2) monthly heatmap, (3) R-multiple distribution chart. Add: hover tooltips (showing data point values on mouse-over), zoom functionality (where applicable), drill-down (where applicable — e.g., clicking a monthly heatmap cell could filter the trade list). No new indicators, no new data, no recalculation on the frontend. All values must remain consistent with canonical backend response — no client-side re-derivation.

**Acceptance Criteria**
- Hover tooltips functional on all 3 charts (show data point values on hover)
- Zoom implemented on at least 1 chart (equity curve is the primary candidate)
- Drill-down implemented where applicable (at minimum: monthly heatmap cell shows filtered view)
- All displayed values match canonical backend response exactly (no client-side re-derivation)
- No new technical indicators introduced
- Director of Quality sign-off (evidence method must be stated — local run or staging)

---

## EPIC-05 — Financial Reporting Exports & Feature Enhancements

**Maps to:** S2-05
**Effort:** M (~18–32 hrs total)
**Owner:** Head of Engineering + Base44 Frontend + Financial Reporting & Records Owner + Infrastructure & Operations Owner
**Sprint:** 1–2 (distributed; PDF export in Sprint 1, remainder in Sprint 2)

### ST-12 — BLG-FR-01: Tax Year P&L PDF Export

**Type:** Backend + Frontend
**Effort:** M (~8–12 hrs)
**Owner:** Head of Engineering + Base44 Frontend + Financial Reporting & Records Owner
**Delegation:** Delegated
**Backlog item:** BLG-FR-01 (IDEA-financial-reporting-20260317-01)

**Description:** Implement server-side PDF generation for the tax year P&L report. Endpoint: `GET /reports/tax-year?format=pdf`. All data fields in the PDF must match the JSON response exactly — no client-side re-derivation. PDF must include: report title, tax year period (e.g., "6 April 2024 – 5 April 2025"), generation timestamp. Browser-print remains available as fallback.

**Acceptance Criteria**
- `GET /reports/tax-year?format=pdf` returns a PDF response
- PDF formatting is consistent across browsers (no browser-print inconsistency)
- PDF contains: report title, tax year period, generation date, all trade rows with P&L figures
- All data fields in PDF match the JSON response exactly
- `openapi.yaml` updated in same commit as endpoint change
- Financial Reporting & Records Owner sign-off
- Director of Quality sign-off (PDF format verified against staging)

---

### ST-13 — BLG-FR-02: Tax Year P&L CSV Export

**Type:** Backend
**Effort:** S (~3–5 hrs)
**Owner:** Head of Engineering
**Delegation:** Delegated
**Backlog item:** BLG-FR-02 (IDEA-financial-reporting-20260317-02)

**Description:** Implement CSV export for the tax year P&L report. Endpoint: `GET /reports/tax-year?format=csv`. Format conversion of the existing endpoint response — minimal infrastructure. CSV must have human-readable column headers (not internal field names).

**Acceptance Criteria**
- `GET /reports/tax-year?format=csv` returns a well-formed CSV with headers
- All data fields match the JSON response exactly
- Column headers are human-readable
- No schema migration required
- `openapi.yaml` updated in same commit as endpoint change
- Head of Engineering sign-off

---

### ST-14 — BLG-FEAT-03: Slippage Tracking

**Type:** Backend + Frontend (data model + implementation)
**Effort:** S–M (~6–10 hrs)
**Owner:** Head of Engineering + Data Model & Domain Schema Owner + Base44 Frontend
**Delegation:** Delegated
**Backlog item:** BLG-FEAT-03

**Description:** Track and display trade slippage per trade and as a portfolio average. Formula: `(Fill Price - Market Price) / Market Price`. Requires data model update — Fill Price must be captured at trade entry (not currently stored). This story covers: (1) spec the Fill Price field in `data_model.md`, (2) database migration to add Fill Price, (3) capture Fill Price at trade entry, (4) compute and display slippage per trade + portfolio average.

**Acceptance Criteria**
- `data_model.md` updated to define Fill Price field and migration path (Data Model Owner + Head of Specs Team sign-off required before implementation begins)
- Database migration authored
- Fill Price captured at trade entry
- Slippage computed per trade: `(Fill Price - Market Price) / Market Price`
- Portfolio average slippage displayed
- Director of Quality sign-off

---

### ST-15 — BLG-OPS-03: Render PR Preview Environments

**Type:** Infrastructure
**Effort:** S (~2–4 hrs)
**Owner:** Infrastructure & Operations Owner
**Delegation:** Delegated (infrastructure configuration within Infrastructure Owner domain)
**Backlog item:** BLG-OPS-03

**Description:** Enable Render Preview Environments on the existing Render Blueprint. Each PR against main automatically gets a unique preview URL. Preview environments share the staging Supabase DB (acceptable at current scale). Document the preview URL pattern and add to DoQ sign-off checklist.

**Acceptance Criteria**
- Render Preview Environments enabled (one-click configuration in Render dashboard)
- Opening a PR against main automatically provisions a preview environment
- Preview URL pattern is `https://trading-assistant-api-pr-{N}.onrender.com` (or Render's assigned pattern)
- `OPERATIONAL_GUIDE.md §8` updated to document preview URL pattern
- DoQ sign-off checklist updated to reference preview URL for frontend verification
- Infrastructure & Operations Owner sign-off

---

## EPIC-06 — Spec Debt & QA Coverage

**Maps to:** S2-06
**Effort:** S–M (~13–23 hrs total)
**Owner:** Head of Specs Team + QA & Testing Owner + PMO Lead
**Sprint:** 1 (parallel track; independent of product delivery)

### ST-16 — BLG-SPEC-D12: Bulk lifecycle header remediation

**Type:** Spec Governance
**Effort:** S–M (~6–10 hrs)
**Owner:** Head of Specs Team
**Delegation:** Delegated (spec compliance work under Head of Specs Team authority)
**Backlog item:** BLG-SPEC-D12

**Description:** Add compliant `Class` and `**Lifecycle Guide:**` headers to all 28 non-compliant spec documents listed in `docs/specs/spec_coverage_inventory.md §9`. Header-only changes — no content modifications. All documents pre-date lifecycle guide adoption.

**Acceptance Criteria**
- All 28 listed documents carry compliant lifecycle headers: `Class: [Canonical Specification (Class 1) | Supporting (Class 2)]` and `**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md`
- Version bumped on each document modified
- `docs/specs/spec_coverage_inventory.md §9` compliance count updated to 38/38
- No content changes — header compliance only
- Head of Specs Team sign-off

---

### ST-17 — Spec maintenance batch (BLG-SPEC-D13 + BLG-SPEC-G6 + BLG-SPEC-D10 + BLG-SPEC-D11)

**Type:** Spec Maintenance (batch)
**Effort:** S (~3–5 hrs)
**Owner:** Head of Specs Team + Metrics Definitions & Analytics Canonical Owner + Head of Engineering
**Delegation:** Delegated

**Description:** Batch of 4 spec maintenance items:
- **BLG-SPEC-D13:** `metrics_definitions.md` Owner field updated from "Analytics Team" to governance role "Metrics Definitions & Analytics Canonical Owner"; version bumped.
- **BLG-SPEC-G6:** `GET /analytics/metrics` updated to return `total_return_pct` per formula (`total_pnl / net_cash_flow × 100`); `analytics_endpoints.md` "not yet returned" note removed; `openapi.yaml` updated.
- **BLG-SPEC-D10:** `docs/specs/frontend/patterns/api_dependencies.md` updated to include Reports page (`GET /reports/tax-year`) and updated Signals page endpoint mappings; version bumped.
- **BLG-SPEC-D11:** `docs/specs/data_model.md §501` trade_reflections entry updated to reflect implemented status (v1.9 Sprint 1); version bumped.

**Acceptance Criteria**
- All 4 items resolved as described above
- All modified documents have version bumps and updated Last Updated dates
- `openapi.yaml` updated in same commit as BLG-SPEC-G6 backend change
- Head of Specs Team sign-off on spec changes; Head of Engineering sign-off on BLG-SPEC-G6 implementation

---

### ST-18 — Author missing test scenario documents (TEST-GAP-SIG-01 + TEST-GAP-TAX-01)

**Type:** QA / Test Documentation
**Effort:** S (~3–5 hrs)
**Owner:** QA & Testing Owner
**Delegation:** Delegated
**Backlog items:** TEST-GAP-SIG-01, TEST-GAP-TAX-01

**Description:** Author 2 test scenario documents that were flagged as coverage gaps in v2.0 delivery verification.

**Acceptance Criteria**
- `docs/testing/signals_scenarios.md` created covering SC-SIG-01/02/03 as specified in TEST-GAP-SIG-01 backlog entry
- `docs/testing/reports_scenarios.md` created covering SC-TAX-01/02/03 as specified in TEST-GAP-TAX-01 backlog entry
- QA & Testing Owner sign-off on scenario coverage
- Director of Quality review completed

---

### ST-19 — BLG-PROC-01: Cross-EPIC branch process compliance check

**Type:** Process Verification
**Effort:** S (~1–2 hrs)
**Owner:** PMO Lead
**Delegation:** Delegated (process governance under PMO Lead authority)
**Backlog item:** BLG-PROC-01

**Description:** CLAUDE.md §2 action-now patch "Story commits must land on the branch matching their EPIC prefix" was applied in v2.0. This item tracks compliance at next sprint execution. At v2.1 sprint close, PMO Lead confirms: (a) no cross-EPIC commits occurred, or (b) any occurring were escalated and documented.

**Acceptance Criteria**
- At v2.1 sprint close, PMO Lead reviews commit history for cross-EPIC violations
- Outcome recorded in qa_evidence log: either "zero cross-EPIC commits (pattern established)" or list of any deviations + escalation references
- If zero recurrence across this sprint: item can be closed as pattern established
- PMO Lead sign-off recorded

---
