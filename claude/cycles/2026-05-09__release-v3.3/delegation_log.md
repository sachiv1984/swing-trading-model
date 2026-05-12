**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-12

---

# Delegation Log — 2026-05-09__release-v3.3

---

## DEL-20260510-01

- **ST Item:** ST-03 — Position lifecycle state: frontend display
- **EPIC:** EPIC-01
- **Classification:** delegated_frontend
- **Assigned to:** Frontend Developer
- **GitHub Issue:** #352
- **Branch:** exec/2026-05-09__release-v3.3/EPIC-01
- **Delegated at:** 2026-05-10T00:00:00Z
- **What is needed:** Implement position lifecycle state badge on the Positions page, gated behind the `arc3_lifecycle_display` feature flag (installed in ST-16). Badge must display GRACE / PROFITABLE / LOSING / EXIT ZONE / UNKNOWN with colour coding per UX spec. Show `days_in_state` alongside badge. Playwright E2E scenario required. Human staging sign-off required for badge states not covered by Playwright.
- **Spec reference:** `docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md`, `docs/specs/frontend/pages/positions.md`
- **Unblock criteria:** PR includes React badge component (or equivalent), feature flag guard, days_in_state display, Playwright scenario passing, and DoQ sign-off on `qa_evidence_EPIC-01.md` ST-03 section.
- **Commit format required:** `[EPIC-01][ST-03] <description>` pushed to `exec/2026-05-09__release-v3.3/EPIC-01`
- **Status:** Cancelled — returned to backlog at sprint close 2026-05-12. Frontend delivery deferred per PO acceptance; item carried to next sprint. Backlog reference: ST-03 returned per cycle 2026-05-09__release-v3.3.
- **Completed at:** —
- **Completed by:** —
- **Outcome:** Returned to backlog. Frontend badge implementation pending next frontend sprint window.

---

## DEL-20260510-02

- **ST Item:** ST-05 — Grace Period Decision Support frontend (IT-02)
- **EPIC:** EPIC-02
- **Classification:** delegated_frontend
- **Assigned to:** Frontend Developer
- **GitHub Issue:** null
- **Branch:** exec/2026-05-09__release-v3.3/EPIC-02
- **Delegated at:** 2026-05-10T00:00:00Z
- **What is needed:** Implement grace period alert card on Positions/Dashboard page. The card is triggered when `GET /positions/grace-period-alerts` returns results. Alert must be dismissible (localStorage). Each alert links to the associated trade plan. Per §13: system presents, human decides — no automated action. Playwright E2E scenario required.
- **Spec reference:** `docs/specs/api_contracts/grace_period_alert_endpoint.md`, `docs/qa/acceptance_protocols/research_view_protocol.md`
- **Unblock criteria:** React alert card component rendering `GET /positions/grace-period-alerts` data, dismissible state persisted in localStorage, trade plan link functional, Playwright scenario passing, DoQ sign-off on `qa_evidence_EPIC-02.md` ST-05 section.
- **Commit format required:** `[EPIC-02][ST-05] <description>` pushed to `exec/2026-05-09__release-v3.3/EPIC-02`
- **Status:** Cancelled — returned to backlog at sprint close 2026-05-12. Frontend grace period alert card deferred. Backlog reference: ST-05 returned per cycle 2026-05-09__release-v3.3.
- **Completed at:** —
- **Completed by:** —
- **Outcome:** Returned to backlog. Backend endpoint (GET /positions/grace-period-alerts) live on main; frontend display pending.

---

## DEL-20260510-03

- **ST Item:** ST-07 — Stop Management Workflow frontend (IT-03)
- **EPIC:** EPIC-02
- **Classification:** delegated_frontend
- **Assigned to:** Frontend Developer
- **GitHub Issue:** null
- **Branch:** exec/2026-05-09__release-v3.3/EPIC-02
- **Delegated at:** 2026-05-10T00:00:00Z
- **What is needed:** Implement "Trail Stop" button per position row (visible for PROFITABLE and EXIT ZONE positions with `current_stop` set). Button opens a guided panel displaying: current stop, ATR trail stop (from `GET /positions/{id}/stop-trail`), trail difference in price and R-terms, and a confirmation button "Update stop". Cancel/dismiss must be available. Button disabled with tooltip when `current_stop` is null. Per §13: system presents; human confirms; no automated action. Playwright scenario required.
- **Spec reference:** `docs/reference/openapi.yaml#/paths/~1positions~1{position_id}~1stop-trail`
- **Unblock criteria:** Trail Stop button per row, guided panel with all fields, confirm/cancel interaction, Playwright scenario passing, DoQ sign-off on `qa_evidence_EPIC-02.md` ST-07 section.
- **Commit format required:** `[EPIC-02][ST-07] <description>` pushed to `exec/2026-05-09__release-v3.3/EPIC-02`
- **Status:** Cancelled — returned to backlog at sprint close 2026-05-12. Frontend Trail Stop panel deferred. Backlog reference: ST-07 returned per cycle 2026-05-09__release-v3.3.
- **Completed at:** —
- **Completed by:** —
- **Outcome:** Returned to backlog. Backend endpoint (GET /positions/{id}/stop-trail) live on main; frontend display pending.

---

## DEL-20260510-04

- **ST Item:** ST-17 — Trade plan abandonment + status badges + frontend quick wins
- **EPIC:** EPIC-04
- **Classification:** delegated_frontend
- **Assigned to:** Frontend Developer
- **GitHub Issue:** null
- **Branch:** exec/2026-05-09__release-v3.3/EPIC-04
- **Delegated at:** 2026-05-10T00:00:00Z
- **What is needed (5 frontend sub-deliverables):**
  1. **BLG-FE-30** — Trade plan status badge: display status (Draft/Active/Abandoned/Completed) as a colour-coded badge on Trade Plans page and Trade Plan detail. Abandoned status must show abandonment_reason on hover/expand.
  2. **BLG-FE-23** — Research page UK ticker suffix strip: strip `.L` suffix from UK tickers when displaying symbol on Research page (display `BARC` not `BARC.L`).
  3. **BLG-FE-24** — Negative earnings days display: if earnings_days_ago is negative (earnings in the future), display as "Earnings in N days" not "-N days ago".
  4. **BLG-FE-25** — Signals page default to most recent day: on Signals page initial load, default the date filter to the most recent available date rather than requiring manual selection.
  5. **BLG-FE-29** — Watchlist research status indicator: add a visual indicator on the Watchlist page showing whether a research view entry exists for each ticker.
  Each sub-deliverable requires its own Playwright test scenario or human staging sign-off.
- **Spec reference:** `docs/specs/frontend/pages/trade_plan.md`, `docs/specs/data_model.md#DS-06`
- **Unblock criteria:** All 5 sub-deliverables implemented, each with Playwright scenario or staging sign-off, DoQ sign-off on `qa_evidence_EPIC-04.md` ST-17 section.
- **Commit format required:** `[EPIC-04][ST-17] <description>` pushed to `exec/2026-05-09__release-v3.3/EPIC-04`
- **Status:** Cancelled — backend delivery accepted by Product Owner 2026-05-12 (commit e3a834d1). Frontend sub-deliverables (BLG-FE-30, BLG-FE-23, BLG-FE-24, BLG-FE-25, BLG-FE-29) carried to post-sprint and remain in backlog.
- **Completed at:** 2026-05-12T00:00:00Z (backend only)
- **Completed by:** Sprint Execution Engine (backend); Frontend Developer (pending)
- **Outcome:** Backend AC met and merged. Frontend sub-deliverables tracked in backlog as BLG-FE-30, BLG-FE-23, BLG-FE-24, BLG-FE-25, BLG-FE-29.

---
