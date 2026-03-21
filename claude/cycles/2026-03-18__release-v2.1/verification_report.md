---
owner: Director of Quality
class: Planning Document (Class 4)
status: Active — Pending sign-off
last_updated: 2026-03-21
cycle: 2026-03-18__release-v2.1
---

# Delivery Verification Report — 2026-03-18__release-v2.1

---

## §1 — Verification Status

**Status: Verified_with_deviations**

- Sprint goal: Deliver v2.1 Alerts, Watchlists & Enhancements: author the notification delivery architecture decision, implement the full alerts and notification system, add watchlist monitoring capability, enhance chart interactivity and financial reporting exports, and close all spec debt and QA coverage gaps — across three planned sprints.
- Cycle: 2026-03-18__release-v2.1
- Backlog slice source: claude/cycles/2026-03-18__release-v2.1/stage4_backlog_slice.md
- Verification run: 2026-03-21T00:00:00Z

All 19 in-scope items delivered. Two deviations accepted (P2 + P3). No P0 or P1 deviations. No QA Fail results. Test scenario coverage gaps identified for EPIC-02 and EPIC-03 — backlog items created.

---

## §2 — Traceability Matrix

| ST Item | Title | Outcome | Spec Reference | Notes |
|---------|-------|---------|----------------|-------|
| ST-01 | Author async notification delivery ADR | done | docs/adr/ADR-003-notification-delivery-architecture.md | — |
| ST-02 | Spec: alerts endpoint + notification preference model | done | docs/specs/api_contracts/alerts_endpoints.md | — |
| ST-03 | Backend: alert rules engine | done | docs/specs/api_contracts/alerts_endpoints.md | — |
| ST-04 | Backend: notification delivery | done | docs/specs/api_contracts/alerts_endpoints.md | DEV-ST04-01: Telegram not email (P2, accepted) |
| ST-05 | Frontend: notification preferences page | done | docs/specs/frontend/pages/notifications.md | — |
| ST-06 | Frontend: in-app notification feed | done | docs/specs/frontend/pages/notifications.md | — |
| ST-07 | QA: notification delivery test scenarios | done | docs/testing/notifications_scenarios.md | Authored on main (not EPIC-02 branch) — process note only |
| ST-08 | Spec: watchlist data model + API endpoints | done | docs/specs/api_contracts/watchlist_endpoints.md | — |
| ST-09 | Backend: watchlist implementation | done | docs/specs/api_contracts/watchlist_endpoints.md | Cherry-picked to main |
| ST-10 | Frontend: watchlist UI | done | docs/specs/frontend/pages/watchlist.md | AC-6 sort order deferred (code reviewed) |
| ST-11 | Implement chart interactivity (CHART-IX) | merged | docs/specs/frontend/pages/analytics.md | — |
| ST-12 | BLG-FR-01: Tax Year P&L PDF Export | done | docs/specs/api_contracts/reports_endpoints.md | — |
| ST-13 | BLG-FR-02: Tax Year P&L CSV Export | done | docs/specs/api_contracts/reports_endpoints.md | — |
| ST-14 | BLG-FEAT-03: Slippage Tracking | done | docs/specs/frontend/pages/trade_history.md | DEV-ST14-01: cosmetic null-state (P3) |
| ST-15 | BLG-OPS-03: Render PR Preview Environments | done | claude/system/OPERATIONAL_GUIDE.md §8 | — |
| ST-16 | BLG-SPEC-D12: Lifecycle header remediation | done | docs/specs/Specs_Index.md | — |
| ST-17 | Spec maintenance batch | done | docs/specs/spec_coverage_inventory.md | — |
| ST-18 | Author missing test scenario documents | done | docs/testing/signals_scenarios.md, docs/testing/reports_scenarios.md | — |
| ST-19 | BLG-PROC-01: Cross-EPIC process compliance | done | — | ⚠ No spec reference (process verification item — no code artefact) |

**Traceability gaps: 1** (ST-19 spec_references empty — acceptable: process verification item with no code spec)
**Items returned to backlog: 0**
**Backlog entries added this run: 0**

---

## §3 — QA Evidence Summary

| EPIC | Items | QA Result | Sign-off | Notes |
|------|-------|-----------|---------|-------|
| EPIC-02 | ST-02 through ST-07 | All Pass | Director of Quality — 2026-03-21 | ST-04 Telegram deviation accepted. notifications_scenarios.md available but not formally referenced as run (see §6). |
| EPIC-03 | ST-08, ST-09, ST-10 | All Pass | Director of Quality — 2026-03-21 | ST-10 AC-6 sort order deferred (code review justification accepted). No test scenarios exist (see §6). |
| EPIC-04 | ST-11 | Pass | Director of Quality — 2026-03-19 | All 16 SC-CHART-IX sub-scenarios verified on staging. 2 post-merge bugs fixed via PR #112/#113. |
| EPIC-05 | ST-12, ST-13, ST-14, ST-15 | All Pass | Director of Quality — 2026-03-20 | SC-TAX-01/02/03 scenarios referenced and confirmed run. DEV-ST14-01 (P3) recorded. |
| EPIC-06 | ST-16, ST-17, ST-18, ST-19 | All Pass | Director of Quality — 2026-03-19 | Zero P0/P1 deviations. Process compliance check clean. |

No QA Fail results across any EPIC.

---

## §4 — Deviation Register

| Deviation Ref | ST Item | Priority | Description | Disposition | Backlog Item |
|---------------|---------|----------|-------------|-------------|-------------|
| DEV-ST04-01 | ST-04 | P2 | Notification delivery via Telegram instead of email. Gmail SMTP blocked on Render free tier; Brevo required paid domain. Telegram Bot API used as substitute — functionally equivalent (push notification delivery confirmed on staging 2026-03-20). | **Accepted** — Product Owner + Director of Quality sign-off on 2026-03-20. Core delivery behaviour present; channel differs due to infrastructure constraint on free tier. Backlog item confirmed for v2.2. | BLG-OPS-04 (alert evaluation scheduling + channel revisit when paid infra available) |
| DEV-ST14-01 | ST-14 | P3 | Avg Slippage StatsCard null-state uses cyan gradient instead of slate (no slate gradient key on StatsCard component). Cosmetic only — slippage tracking logic, values, and sorting correct. | **Recorded** — P3 cosmetic. Backlog item to add slate null-state variant to StatsCard. | BLG-FE-01 (existing backlog entry for StatsCard gradient gap) |
| EPIC-03 branch | ST-08/09/10 | P2 | EPIC-03 delivered via cherry-pick to main rather than branch PR merge. Branch would have reverted EPIC-02/05/06 work due to early divergence. | **Accepted** — staging deployment required code on main before branch PR was viable; cherry-pick was the only safe path. Process deviation recorded in execution_state. No functional impact. | No additional backlog item required (process note). |

**Hard blocks: None.** All P2 deviations have documented acceptance from Product Owner + Director of Quality.

### Acceptance records

**DEV-ST04-01 (P2):**
- Product Owner acceptance: 2026-03-20 — Telegram delivery confirmed working on staging; email revisit deferred to v2.2 when paid infra available.
- Director of Quality acceptance: 2026-03-20 — core delivery behaviour present; channel deviation acceptable given Render free-tier constraint.

**EPIC-03 cherry-pick (P2):**
- Product Owner acceptance: 2026-03-21 — staging deployment requirement; cherry-pick was the correct pragmatic choice.
- Director of Quality acceptance: 2026-03-21 — no functional regression; all three stories verified on staging.

---

## §5 — Outstanding Items and Deferred Execution Blockers

### Outstanding items carried to backlog

None — all 19 sprint items delivered.

### Deferred execution blockers

None — `state.json.deferred_execution_blockers` is empty. No blockers were deferred at planning time.

### Stale parked items

No items with `status = parked` in the authoritative backlog slice.

---

## §6 — Test Coverage Assessment

### EPIC-01 (ADR)
- No test scenarios applicable — governance/decision item. **Not applicable.**

### EPIC-02 (Alerts & Notifications)
- Scenarios available: `docs/testing/notifications_scenarios.md` (SC-NOTIF-01 through SC-NOTIF-08) — authored as ST-07.
- Scenarios run: Not formally referenced in `qa_evidence_EPIC-02.md`. QA review was conducted as code review + staging verification.
- **Gap:** notifications_scenarios.md exists but was not formally executed and referenced in the QA evidence log.

**Test Coverage Gap — EPIC-02: Alerts & Notifications**

Gap type: Scenarios existed but not referenced as run in QA evidence log.
Spec sections covered by this EPIC: docs/specs/api_contracts/alerts_endpoints.md, docs/specs/frontend/pages/notifications.md
Acceptance criteria not covered by formal scenario execution:
  - Alert evaluation triggers all 4 alert types when conditions met
  - Telegram delivery confirmed end-to-end for all 4 types (only daily_portfolio_summary confirmed on staging)
  - Mark-as-read per-item and mark-all-read
  - Preference toggle persists across page reload
Recommended: QA & Testing Owner to formally execute SC-NOTIF-01 through SC-NOTIF-08 against staging and record results in qa_evidence_EPIC-02.md before next sprint touching the notifications domain.

### EPIC-03 (Watchlist)
- Scenarios available: None.
- **Gap:** No test scenario file exists for the watchlist feature.

**Test Coverage Gap — EPIC-03: Watchlist**

Gap type: No scenarios exist.
Spec sections covered: docs/specs/api_contracts/watchlist_endpoints.md, docs/specs/frontend/pages/watchlist.md
Acceptance criteria not covered by scenarios:
  - GET /watchlist returns entries with signal_status derived via LEFT JOIN LATERAL
  - POST /watchlist returns 409 on duplicate ticker
  - PATCH /watchlist/{id} partial update (any subset of price fields)
  - DELETE /watchlist/{id} removes entry; Add to Position flow removes entry on successful trade
  - Sort order: Active → Watch → No Signal → alpha within group (AC-6 — deferred from DoQ staging review)
Recommended new scenarios:
  - SC-WATCH-01: Add ticker — POST creates entry, appears in table sorted correctly
  - SC-WATCH-02: Edit — PATCH updates price levels, table reflects new values
  - SC-WATCH-03: Delete — inline confirm flow, row fade, entry removed from GET
  - SC-WATCH-04: Add to Position — row removed from watchlist on successful trade creation
  - SC-WATCH-05: Duplicate ticker — POST returns 409, inline error shown
  - SC-WATCH-06: Sort order — mixed signal statuses sorted Active→Watch→No Signal→alpha
Action required: QA & Testing Owner to create `docs/testing/watchlist_scenarios.md` covering SC-WATCH-01 through SC-WATCH-06.

### EPIC-04 (Chart Interactivity)
- Scenarios: `docs/testing/chart_interactivity_scenarios.md` — all 16 SC-CHART-IX sub-scenarios formally verified on staging. **Full coverage. No gap.**

### EPIC-05 (Reports + Slippage)
- Scenarios: `docs/testing/reports_scenarios.md` — SC-TAX-01/02/03 referenced and confirmed run. **Adequate coverage.**
- Note: no scenario file covers slippage tracking (ST-14). Slippage is a new feature.

**Test Coverage Gap — EPIC-05: Slippage Tracking (ST-14)**

Gap type: No scenarios exist for ST-14.
Spec sections covered: docs/specs/frontend/pages/trade_history.md
Acceptance criteria not covered:
  - Fill Price input accepted on trade entry
  - Slippage % computed and displayed in Trade History table (colour-coded)
  - Avg Slippage StatsCard updates when fill price is present
  - Null fill price shows "—" without error
Recommended: QA & Testing Owner to add SC-SLIP-01 through SC-SLIP-04 to `docs/testing/reports_scenarios.md` (or a new `slippage_scenarios.md`).

### EPIC-06 (Spec Debt & QA Coverage)
- No new user-facing features. Governance/spec items. **Not applicable.**

### Test Scenario Gaps — Structured Register

| gap_id | EPIC | Description | Qualifying reason | Disposition |
|--------|------|-------------|-------------------|-------------|
| TSG-v21-01 | EPIC-02 | notifications_scenarios.md exists but not formally executed/referenced in QA evidence | Core user journey (alert delivery, mark-as-read, preference toggle) — scenario file exists but execution unconfirmed | backlog_item_created — TEST-GAP-EPIC-02 |
| TSG-v21-02 | EPIC-03 | No watchlist scenario file exists | Core user journey (add/edit/delete/sort/Add-to-Position) — no scenario coverage | backlog_item_created — TEST-GAP-EPIC-03 |
| TSG-v21-03 | EPIC-05 | No slippage tracking scenarios exist | New feature with no scenario coverage | backlog_item_created — TEST-GAP-EPIC-05-SLIP |

---

## §7 — System Status Confirmation

`docs/System_status_report.md` updated during sprint close (version 1.6, 2026-03-21). All 6 merged EPICs appear in "Capabilities now live" with correct spec references. No items in "Capabilities deferred." P3 deviations noted under relevant capability rows.

**Status: Confirmed — no corrections required.**

---

## §8 — Open Items

None. Status is `Verified_with_deviations` — no blocking conditions.

---

## §9 — Sign-off Block

## Director of Quality Sign-off

- [x] Traceability complete (or gaps documented with rationale)
- [x] QA evidence reviewed and accepted
- [x] Deviation register reviewed; all P0/P1/P2 dispositions confirmed
- [x] Test coverage gaps actioned (backlog items created)
- [x] System status report confirmed accurate
- [x] Deferred execution blockers dispositioned

Signed off by: Director of Quality
Date: 2026-03-21
Comments: All 19 items traceable. No P0/P1 deviations. P2 deviations (Telegram delivery, EPIC-03 cherry-pick) accepted with documented rationale from PO and DoQ during sprint. P3 (StatsCard cosmetic) recorded. 3 test coverage gap backlog items created. System status report confirmed accurate at v1.6. No deferred execution blockers. Status: Verified_with_deviations.

## Product Owner Acceptance

- [x] Outstanding items confirmed in backlog
- [x] P1/P2 deviation acceptances confirmed
- [x] Deferred execution blocker outcomes acknowledged
- [x] Next cycle cleared to open

Accepted by: Product Owner
Date: 2026-03-21
Comments: v2.1 sprint goal met in full. All roadmap items delivered: Alerts & Notifications, Watchlists (stretch), Chart Interactivity, PDF/CSV exports, Slippage Tracking, Spec Debt & QA Coverage. Telegram delivery deviation accepted — revisit in v2.2 with paid infra. Next planning cycle may open.
