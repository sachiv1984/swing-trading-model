**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-21
**Cycle:** 2026-03-18__release-v2.1
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Delegation Log — 2026-03-18__release-v2.1

This file is append-only. Do not edit previous entries.

---

## DEL-20260318-01 — ST-01: Author async notification delivery ADR

**Date:** 2026-03-18
**Item:** EPIC-01 / ST-01
**Classification:** delegated_decision
**Assigned to:** Head of Engineering + Backend Engineering Patterns Owner
**GitHub issue:** #91
**Branch:** exec/2026-03-18__release-v2.1/EPIC-01

**What was delegated:** Author ADR-003 evaluating sync vs async notification delivery. Decision gates EPIC-02 spec authoring.

**Spec reference:** docs/specs/api_contracts/backend_engineering_patterns.md

**Unblock criteria:** Head of Engineering sign-off on ADR decision; ADR committed.

**Status:** Unblocked
**Resolved:** 2026-03-18T11:04:06Z
**Commit SHA:** 9ce7f86
**Resolution:** Decision taken — FastAPI BackgroundTasks (sync post-response). No Redis/Celery required. ADR-003 committed to main as governance action pre-sprint. Issue #91 closed automatically.

---

## DEL-20260318-02 — ST-11: Chart interactivity implementation

**Date:** 2026-03-18
**Item:** EPIC-04 / ST-11
**Classification:** delegated_frontend
**Assigned to:** Base44 Frontend
**GitHub issue:** #103
**Branch:** exec/2026-03-18__release-v2.1/EPIC-04

**What was delegated:** Implement chart interactivity on 3 analytics charts: MonthlyHeatmap drill-down modal, UnderwaterChart zoom/pan, RMultipleDistribution custom tooltip.

**Spec reference:** docs/specs/frontend/pages/analytics.md, docs/design/2026-03-18__release-v2.1/chart-interactivity/ux_spec.md

**Unblock criteria:** All AC met; Director of Quality sign-off; Product Owner acceptance.

**Status:** Unblocked
**Resolved:** 2026-03-19T00:00:00Z
**Commit SHA:** 4b78867 (final; PRs #111, #112, #113 all merged)
**Resolution:** Implementation complete. All 16 SC-CHART-IX sub-scenarios verified on staging 2026-03-19. Two post-merge bugs fixed (PR #112 zoom-out edge, PR #113 tooltip % of total). DoQ and PO signed off.

---

## DEL-20260318-03 — ST-15: Render PR Preview Environments

**Date:** 2026-03-18
**Item:** EPIC-05 / ST-15
**Classification:** delegated_decision
**Assigned to:** Infrastructure & Operations Owner
**GitHub issue:** #110 (also #105 — duplicate; #110 closed by governance_sync)
**Branch:** exec/2026-03-18__release-v2.1/EPIC-05

**What was delegated:** Document Render PR preview environment setup in OPERATIONAL_GUIDE.md §8. Infrastructure configuration.

**Spec reference:** claude/system/OPERATIONAL_GUIDE.md#8

**Unblock criteria:** OPERATIONAL_GUIDE.md §8 updated; Infrastructure & Operations Owner sign-off.

**Status:** Unblocked
**Resolved:** 2026-03-18T21:18:06Z
**Commit SHA:** b478600
**Resolution:** OPERATIONAL_GUIDE.md §8 updated with PR preview URL pattern and limitation note (CRA build-time env var prevents per-PR frontend preview). Issue #110 closed. Sprint 2 item — implemented early alongside EPIC-04 work.

---

## DEL-20260318-04 — ST-16: Bulk lifecycle header remediation

**Date:** 2026-03-18
**Item:** EPIC-06 / ST-16
**Classification:** delegated_decision
**Assigned to:** Head of Specs Team
**GitHub issue:** #104
**Branch:** exec/2026-03-18__release-v2.1/EPIC-06

**What was delegated:** Add compliant lifecycle headers (Class + Lifecycle Guide) to 28 non-compliant spec documents.

**Spec reference:** docs/specs/spec_coverage_inventory.md#Section 9

**Unblock criteria:** All 28 listed documents updated; spec_coverage_inventory.md §9 count updated; Head of Specs Team sign-off.

**Status:** Unblocked
**Resolved:** 2026-03-18T20:37:07Z
**Commit SHA:** 143c5df
**Resolution:** 24 documents updated; 2 found already compliant. spec_coverage_inventory.md updated to 36/36 (100%). Note: AC specified 38/38 target but inventory reconciled to 36/36 — deviation documented in qa_evidence_EPIC-06.md. Issue #104 closed.

---

## DEL-20260318-05 — ST-17: Spec maintenance batch

**Date:** 2026-03-18
**Item:** EPIC-06 / ST-17
**Classification:** delegated_decision
**Assigned to:** Head of Specs Team + Metrics Definitions & Analytics Canonical Owner + Head of Engineering
**GitHub issue:** #109
**Branch:** exec/2026-03-18__release-v2.1/EPIC-06

**What was delegated:** 4-item spec maintenance batch: D13 (metrics owner field), G6 (total_return_pct active), D10 (api_dependencies.md), D11 (trade_reflections status).

**Spec references:** docs/specs/api_contracts/analytics_endpoints.md, docs/specs/frontend/patterns/api_dependencies.md, docs/specs/data_model.md#501, docs/specs/metrics_definitions.md

**Unblock criteria:** All 4 items resolved; openapi.yaml updated for G6; Head of Specs Team + Head of Engineering sign-off.

**Status:** Unblocked
**Resolved:** 2026-03-18T20:14:12Z
**Commit SHA:** 7f961f0
**Resolution:** All 4 items complete. openapi.yaml updated for G6. Issue #109 closed.

---

## DEL-20260318-06 — ST-18: Author missing test scenario documents

**Date:** 2026-03-18
**Item:** EPIC-06 / ST-18
**Classification:** delegated_qa
**Assigned to:** QA & Testing Owner
**GitHub issue:** #108
**Branch:** exec/2026-03-18__release-v2.1/EPIC-06

**What was delegated:** Author signals_scenarios.md (SC-SIG-01/02/03) and reports_scenarios.md (SC-TAX-01/02/03).

**Spec references:** docs/testing/signals_scenarios.md, docs/testing/reports_scenarios.md

**Unblock criteria:** Both scenario docs created; QA & Testing Owner sign-off; Director of Quality review.

**Status:** Unblocked (pending formal DoQ acceptance_verified)
**Resolved:** 2026-03-18T20:22:17Z
**Commit SHA:** 62fcf03
**Resolution:** signals_scenarios.md and reports_scenarios.md created on EPIC-06 branch. Issue #108 closed. Director of Quality formal review captured in qa_evidence_EPIC-06.md.

---

## DEL-20260318-07 — ST-19: Cross-EPIC branch process compliance check

**Date:** 2026-03-18
**Item:** EPIC-06 / ST-19
**Classification:** delegated_decision
**Assigned to:** PMO Lead
**GitHub issue:** #107
**Branch:** exec/2026-03-18__release-v2.1/EPIC-06

**What was delegated:** PMO Lead reviews v2.1 Sprint 1 commit history for cross-EPIC violations. Outcome recorded in qa_evidence_EPIC-06.md.

**Spec reference:** CLAUDE.md §2 (cross-EPIC branch rule), qa_evidence_EPIC-06.md

**Unblock criteria:** PMO Lead reviews commit history at Sprint 1 close; records outcome (zero violations or list of deviations + escalation refs); PMO Lead sign-off.

**Status:** Unblocked
**Resolved:** 2026-03-19T00:00:00Z
**Resolution:** PMO Lead reviewed commit history. Zero cross-EPIC violations across all Sprint 1 branches (EPIC-01, EPIC-04, EPIC-05, EPIC-06). One observation noted (BLG-OPS-03 backlog touch on EPIC-04 branch — compliant with CLAUDE.md §2 rule). Pattern established. PMO Lead signed off.

---

## DEL-20260319-01 — ST-12: Tax Year P&L PDF Export (Sprint 1)

**Date:** 2026-03-19
**Item:** EPIC-05 / ST-12
**Classification:** delegated_backend (primary) + delegated_frontend (Download PDF button UX)
**Assigned to:** Head of Engineering (backend) + Base44 Frontend (button UX)
**GitHub issue:** #102
**Branch:** exec/2026-03-18__release-v2.1/EPIC-05

**What is needed:**

### Backend — Head of Engineering

Extend `GET /reports/tax-year` to support a `format` query parameter:

- `format=pdf` → server-side PDF generation; `Content-Type: application/pdf`, `Content-Disposition: attachment; filename="tax-year-{year}-pnl.pdf"`
- Default (omitted) → existing JSON response unchanged

**PDF content (all sourced from existing endpoint — no new data):**
- Report title: `"Tax Year P&L — {tax_year_label}"`
- Generation timestamp (UTC)
- Summary bar values (total_realised_pnl, gross_profit, gross_loss, win_rate, total_closed_trades)
- Trades table: all columns from `trades[]` array
- Disclaimer text verbatim
- Empty year is valid — PDF renders with summary zeros and no trade rows

Suggested library: `reportlab` or `weasyprint` (Head of Engineering's choice).

**Spec updates required in same commit:**
- `docs/specs/api_contracts/reports_endpoints.md` — add `format` query parameter + PDF response schema
- `docs/reference/openapi.yaml` — add `format` enum `[pdf]` to `GET /reports/tax-year`; add `application/pdf` 200 response

**Commit format:** `[EPIC-05][ST-12] Implement GET /reports/tax-year?format=pdf`

### Frontend — Base44 Frontend

Add "Download PDF" button to the Reports page header per `docs/specs/frontend/pages/reports.md` v0.2 and `docs/design/2026-03-18__release-v2.1/pdf-export/ux_spec.md`.

- Secondary button, right-aligned in header alongside year selector
- On click: fires `GET /reports/tax-year?format=pdf&year={currentYear}`
- States: Idle → "Generating…" (spinner, disabled) → Success (download begins, idle) → Error (toast: "PDF generation failed. Please try again.", 5s auto-dismiss)
- Button enabled for empty years

**Commit format:** `[EPIC-05][ST-12] Add Download PDF button to Reports page`

**Spec references:**
- `docs/specs/api_contracts/reports_endpoints.md` (extend with format param)
- `docs/specs/frontend/pages/reports.md` v0.2
- `docs/design/2026-03-18__release-v2.1/pdf-export/ux_spec.md`
- `docs/reference/openapi.yaml` (must update in same commit as backend)

**Unblock criteria:**
- `GET /reports/tax-year?format=pdf` returns valid PDF for populated and empty years; reports_endpoints.md + openapi.yaml updated in same commit; Financial Reporting & Records Owner sign-off; Director of Quality staging sign-off
- Download PDF button functional per all 4 states; Director of Quality sign-off

**Status:** Unblocked
**Resolved:** 2026-03-19T00:00:00Z
**Commit SHAs:** 511f4a4 (frontend), 569d231 (backend)
**Resolution:** Both frontend and backend implemented on EPIC-05 branch. Frontend: Download PDF button with 4 states (idle/generating/success/error) using useToast. Backend: GET /reports/tax-year?format=pdf returning reportlab-generated PDF; reports_endpoints.md v0.2 and openapi.yaml updated in same commit as backend. QA signed off (qa_evidence_EPIC-05.md). Merged via PR #115.

---

## DEL-20260319-02 — ST-02: Spec: alerts endpoint + notification preference model

- **ST Item:** ST-02 — Spec: alerts endpoint + notification preference model
- **EPIC:** EPIC-02
- **Classification:** delegated_decision
- **Assigned to:** Head of Specs Team + Head of Engineering
- **GitHub Issue:** #93
- **Branch:** exec/2026-03-18__release-v2.1/EPIC-02
- **Delegated at:** 2026-03-19T00:00:00Z
- **What is needed:**

  Author the alerts endpoint spec (`docs/specs/api_contracts/alerts_endpoints.md`) and update the notification preference model. This spec gates ST-03 (backend alert rules engine), ST-04 (email delivery), and ST-05 (frontend preferences page) — nothing downstream may be delegated until this is signed off.

  **Architecture context:** ST-01 ADR-003 decided sync-style delivery via FastAPI BackgroundTasks (no Redis/Celery). All endpoint patterns must reflect this.

  **Required outputs in a single commit to `exec/2026-03-18__release-v2.1/EPIC-02`:**

  1. **`docs/specs/api_contracts/alerts_endpoints.md`** (create) — must define:
     - Alert rule types: (a) stop loss approach — trigger when current stop ≤ N% of price; (b) grace period warning — trigger on days 8–9; (c) market regime change — trigger on risk-off transition; (d) daily portfolio summary — scheduled daily trigger
     - CRUD endpoints for alert rules: GET/POST/PATCH/DELETE `/alert-rules`
     - Notification preference schema (per-user, per-alert-type on/off, email flag): GET `/notifications/preferences` + PATCH `/notifications/preferences`
     - Notifications feed endpoints: GET `/notifications`, PATCH `/notifications/{id}` (mark read), POST `/notifications/mark-all-read`
     - Database schema extensions: `alert_rules` table, `notification_preferences` table, `notifications` table
     - Response schemas for all endpoints (exact field names, types, nullable flags)

  2. **`docs/specs/data_model.md`** — add alert_rules, notification_preferences, and notifications table definitions

  3. **`docs/reference/openapi.yaml`** — add all new endpoints from alerts_endpoints.md in same commit

  4. **`docs/specs/Specs_Index.md`** — register alerts_endpoints.md

- **Spec reference:** docs/adr/ADR-003-notification-delivery-architecture.md (architecture decision to reflect), docs/specs/frontend/pages/notifications.md v0.1 (frontend spec already drafted — API contract must be compatible)
- **Unblock criteria:** alerts_endpoints.md created and signed off by Head of Specs Team; openapi.yaml updated in same commit; Specs_Index.md updated; data_model.md updated; ADR-003 sync architecture reflected throughout
- **Commit format required:** `[EPIC-02][ST-02] Author alerts endpoints spec and notification preference model` pushed to `exec/2026-03-18__release-v2.1/EPIC-02`
- **Status:** Unblocked — commit 2b93a36 on 2026-03-20. ST-02 done.

**On completion:** Re-invoke `run sprint --cycle 2026-03-18__release-v2.1` so the engine can detect ST-02 is done and create delegation records for ST-03 (backend), ST-04 (email delivery), and ST-05 (frontend preferences — Base44 prompt will be issued at that point with exact API field names).

---

## DEL-20260319-03 — ST-13: Tax Year P&L CSV Export (Sprint 2)

- **ST Item:** ST-13 — BLG-FR-02: Tax Year P&L CSV Export
- **EPIC:** EPIC-05
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #101
- **Branch:** exec/2026-03-18__release-v2.1/EPIC-05
- **Delegated at:** 2026-03-19T00:00:00Z
- **What is needed:**

  Extend `GET /reports/tax-year` to support `format=csv` — a CSV export of the same data already returned by the JSON endpoint. Pattern is identical to the `format=pdf` extension implemented in ST-12.

  **⚠ Branch setup required first:** The EPIC-05 branch (`exec/2026-03-18__release-v2.1/EPIC-05`) is currently behind main (last commit was the pre-PR-#115 state). Before committing, run:
  ```
  git checkout exec/2026-03-18__release-v2.1/EPIC-05
  git merge main   # (or git rebase main)
  git push origin exec/2026-03-18__release-v2.1/EPIC-05
  ```

  **Implementation — router layer (`backend/main.py` or equivalent):**
  - Extend `GET /reports/tax-year` with `format=csv` support alongside existing `format=pdf`
  - `format=csv` → call new `build_tax_year_csv(report_data: dict) -> str` service function
  - Return: `Response(content=csv_str, media_type="text/csv", headers={"Content-Disposition": 'attachment; filename="tax-year-{year}-pnl.csv"'})`

  **Implementation — service layer (`backend/services/reports_service.py`):**
  - Add `build_tax_year_csv(report_data: dict) -> str`
  - CSV must have human-readable column headers (not internal field names)
  - All `trades[]` fields exported: ticker, market, entry_date, exit_date, holding_days, entry_price_native, exit_price_native, entry_fx_rate, exit_fx_rate, shares, total_cost_gbp, exit_proceeds_gbp, realised_pnl_gbp, pnl_pct, currency, tags
  - Empty year: valid — exports header row only (no data rows)
  - No new library needed (use Python's built-in `csv` module)
  - No schema migration required

  **Spec updates in same commit:**
  - `docs/specs/api_contracts/reports_endpoints.md` — update `format` parameter to `enum: [pdf, csv]`; add CSV response schema (200 — Content-Type: text/csv)
  - `docs/reference/openapi.yaml` — add `csv` to `format` enum; add `text/csv` 200 response alongside existing `application/json` and `application/pdf` responses

- **Spec reference:** docs/specs/api_contracts/reports_endpoints.md v0.2 (reports_endpoints.md#GET-/reports/tax-year — extend format param)
- **Unblock criteria:** GET /reports/tax-year?format=csv returns valid CSV with human-readable headers for populated and empty years; reports_endpoints.md + openapi.yaml updated in same commit; Head of Engineering sign-off; commit on exec/2026-03-18__release-v2.1/EPIC-05
- **Commit format required:** `[EPIC-05][ST-13] Implement GET /reports/tax-year?format=csv` pushed to `exec/2026-03-18__release-v2.1/EPIC-05`
- **Status:** Unblocked — commit 9d75c96. ST-13 done. PR #117 merged 2026-03-20.

---

## DEL-20260319-04 — ST-14: Slippage Tracking — Data Model Gate

- **ST Item:** ST-14 — BLG-FEAT-03: Slippage Tracking
- **EPIC:** EPIC-05
- **Classification:** delegated_decision (data model gate — must resolve before backend implementation is delegated)
- **Assigned to:** Data Model & Domain Schema Owner + Head of Specs Team
- **GitHub Issue:** #106
- **Branch:** exec/2026-03-18__release-v2.1/EPIC-05
- **Delegated at:** 2026-03-19T00:00:00Z
- **What is needed:**

  ST-14 requires a Fill Price field to be added to the trade data model. This field does not currently exist. Before any backend implementation begins, Data Model & Domain Schema Owner and Head of Specs Team must sign off on the field definition and migration path.

  **Required output — update `docs/specs/data_model.md`:**
  - Define `fill_price` field on the `trade_history` (or equivalent) table:
    - Type: float, nullable
    - Description: The actual price at which the trade was filled (may differ from the ordered entry_price due to slippage)
    - Nullable: Yes (null for historical trades where fill price was not captured)
  - Document migration path: ALTER TABLE to add `fill_price` column (nullable), default null for existing rows
  - Note: slippage formula is `(fill_price - entry_price_native) / entry_price_native` — both fields required in the service layer

  **On sign-off:**
  - Commit the data_model.md update to `exec/2026-03-18__release-v2.1/EPIC-05`
  - Then re-invoke `run sprint --cycle 2026-03-18__release-v2.1` — the engine will detect the gate is resolved, re-classify ST-14 to `delegated_backend`, and create the full implementation delegation record for Head of Engineering

  **Commit format for data model gate commit:** `[EPIC-05][ST-14] Spec Fill Price field in data_model.md — slippage tracking data model gate`

- **Spec reference:** docs/specs/data_model.md (section to update), docs/design/2026-03-18__release-v2.1/slippage-tracking/ux_spec.md (display context)
- **Unblock criteria:** data_model.md updated with Fill Price field definition and migration path; Data Model & Domain Schema Owner sign-off; Head of Specs Team sign-off; commit on EPIC-05 branch
- **Commit format required:** `[EPIC-05][ST-14] Spec Fill Price field in data_model.md — slippage tracking data model gate` pushed to `exec/2026-03-18__release-v2.1/EPIC-05`
- **Status:** Unblocked — data model gate cleared; commit a202d07. ST-14 done. PR #117 merged 2026-03-20.

---

## DEL-20260320-01 — ST-05: Notification Preferences Page

**Date:** 2026-03-20
**Item:** EPIC-02 / ST-05
**Classification:** delegated_frontend
**Assigned to:** Base44 Frontend
**GitHub issue:** #97
**Branch:** exec/2026-03-18__release-v2.1/EPIC-02

**What is needed:**

### Frontend — Base44 Frontend

Implement the **Notification Preferences** page per `docs/specs/frontend/pages/notifications.md` v0.1.

---

#### Route

`/notifications/preferences`

---

#### Sub-navigation

Both `/notifications` and `/notifications/preferences` share a tab bar immediately below the page header:

| Tab | Route | Active? |
|-----|-------|---------|
| Feed | `/notifications` | No (on this page) |
| Preferences | `/notifications/preferences` | Yes |

---

#### Page header

- H1: **"Notification Preferences"**
- Subtitle: `"Configure which alerts you receive."`

---

#### Preferences list

On page load: call `GET /notifications/preferences`.

Response shape:
```json
{
  "status": "ok",
  "data": {
    "preferences": [
      { "alert_type": "stop_loss_approach", "email_enabled": true },
      { "alert_type": "grace_period_warning", "email_enabled": true },
      { "alert_type": "market_regime_change", "email_enabled": true },
      { "alert_type": "daily_portfolio_summary", "email_enabled": true }
    ]
  }
}
```

Render one row per alert type with a toggle switch for `email_enabled`:

| Alert Type key | Display label | Description |
|----------------|---------------|-------------|
| `stop_loss_approach` | Stop Loss Approach | Notify when current stop is within threshold % of price |
| `grace_period_warning` | Grace Period Warning | Notify on days 8–9 of the grace period |
| `market_regime_change` | Market Regime Change | Notify when market regime transitions to risk-off |
| `daily_portfolio_summary` | Daily Portfolio Summary | Receive a daily digest of portfolio status |

---

#### Toggle behaviour

No Save button — each toggle persists immediately.

On toggle:
1. Optimistic update: flip the toggle immediately.
2. Fire `PATCH /notifications/preferences` with 150ms debounce.

Request body (send only the toggled type):
```json
{ "stop_loss_approach": { "email_enabled": false } }
```

3. On success: show brief inline **"Saved"** label adjacent to the toggle (fade out after 2s).
4. On error: revert toggle to prior state + inline error `"Failed to save preference. Please try again."` below the row.

---

#### Loading state

Skeleton rows (4 rows at preference-row height) while `GET /notifications/preferences` resolves.

#### Error state (load failure)

Inline error panel: `"Unable to load preferences. Please refresh."`

---

#### Channel scope

Email is the only delivery channel for v2.1. Do not render SMS or any other channel toggle.

---

#### Commit format

`[EPIC-02][ST-05] Implement notification preferences page`

**Spec references:**
- `docs/specs/frontend/pages/notifications.md` v0.1 — Page 2 (Notification Preferences)
- `docs/specs/api_contracts/alerts_endpoints.md` — `GET /notifications/preferences`, `PATCH /notifications/preferences`

**Staging API:** `https://trading-assistant-api-staging.onrender.com`

**Unblock criteria:**
- Preferences page renders at `/notifications/preferences`
- Sub-navigation tab bar present and correct on both `/notifications` and `/notifications/preferences`
- All 4 alert types listed with correct display labels and descriptions
- Toggle persists via `PATCH /notifications/preferences` (confirmed in staging)
- Loading and error states implemented
- Director of Quality sign-off

**Status:** Resolved
**Resolved:** 2026-03-20
**Commit SHA:** 9c4813d (integration); post-fix commits 17d5e26, 2804f5f, 2d63ef9
**Resolution:** Page integrated from Base44 files. Three post-commit fixes required: Body(...) annotation on PATCH, route ordering (preferences before wildcard), and startup race (ensure_alerts_tables). DoQ sign-off 2026-03-20: toggle saves, Saved confirmation visible, Feed tab no longer 404s.

---

## DEL-20260320-02 — ST-06: In-App Notification Feed

**Date:** 2026-03-20
**Item:** EPIC-02 / ST-06
**Classification:** delegated_frontend
**Assigned to:** Base44 Frontend
**GitHub issue:** #96
**Branch:** main

**What was delegated:** Implement the in-app notification feed page per `docs/specs/frontend/pages/notifications.md` v0.1. Feed at `/notifications` displaying recent notifications with mark-as-read and load more.

**Spec reference:** docs/specs/frontend/pages/notifications.md, docs/specs/api_contracts/alerts_endpoints.md

**Unblock criteria:** Feed renders at `/notifications`; mark-as-read (per-item + mark all) functional; empty state handled; nav highlights on both feed and preferences; Director of Quality staging sign-off.

**Status:** Resolved
**Resolved:** 2026-03-20
**Commit SHA:** 47efe4b
**Resolution:** NotificationRow.js (row component) provided by Base44; Notifications.js (feed page) built from spec. All AC verified in staging 2026-03-20: feed shows in staging, empty state visible in live, nav item highlights on both tabs. Director of Quality sign-off 2026-03-20.

---

## DEL-20260321-01 — ST-08: Watchlist spec — data model + API endpoints

**Date:** 2026-03-21
**Item:** EPIC-03 / ST-08
**Classification:** delegated_decision
**Assigned to:** Head of Specs Team + Data Model & Domain Schema Owner
**GitHub issue:** #98
**Branch:** exec/2026-03-18__release-v2.1/EPIC-03

**What was delegated:** Author the watchlist spec. Define: watchlist data model table, API endpoints (GET/POST/PATCH/DELETE /watchlist), signal status derivation (join-on-read from signals table), and the "Add to Position" integration contract. Gates ST-09 (backend) and ST-10 (frontend).

**Spec reference:** docs/specs/api_contracts/watchlist_endpoints.md, docs/specs/data_model.md, docs/reference/openapi.yaml

**Unblock criteria:** watchlist_endpoints.md created with full endpoint definitions; data_model.md updated with watchlist table and migration v2.0→v2.1; openapi.yaml updated in same commit; Specs_Index.md registered; Head of Specs Team + Data Model & Domain Schema Owner sign-off.

**Status:** Resolved
**Resolved:** 2026-03-21
**Commit SHA:** e6eb45f
**Resolution:** watchlist_endpoints.md v0.1 authored (4 endpoints). Signal status architecture: join-on-read via LEFT JOIN LATERAL on signals table — no stored signal_status column. data_model.md v2.1 (watchlist table + migration v2.0→v2.1). openapi.yaml v2.2.0 (Watchlist tag, 4 paths, 3 schemas). Specs_Index.md registered. api_changelog.md v2.2.0 entry. Dual sign-off: Head of Specs Team + Data Model & Domain Schema Owner 2026-03-21.

---
