**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Signed Off — complete
**Version:** 2.0
**Last Updated:** 2026-03-21

---

# QA Evidence — EPIC-02: Alerts & Notifications

**Cycle:** 2026-03-18__release-v2.1
**EPIC:** EPIC-02
**Branch:** exec/2026-03-18__release-v2.1/EPIC-02
**PR:** #116

---

## ST-02 — Spec: Alerts Endpoint + Notification Preference Model

**Classification:** delegated_decision (spec authoring)
**Delegation record:** DEL-20260319-02
**Commit:** 2b93a36
**Spec references:**
- `docs/specs/api_contracts/alerts_endpoints.md` v0.1
- `docs/specs/data_model.md` v1.9
- `docs/reference/openapi.yaml`
- `docs/specs/Specs_Index.md`
- `docs/adr/ADR-003-notification-delivery-architecture.md`

### What was built

**Spec (commit 2b93a36):**
- `docs/specs/api_contracts/alerts_endpoints.md` v0.1 — new file, 10 endpoints:
  - Alert rules CRUD: `GET /alerts/rules`, `POST /alerts/rules`, `PATCH /alerts/rules/{rule_id}`, `DELETE /alerts/rules/{rule_id}`
  - Alert evaluation: `POST /alerts/evaluate`
  - Notification feed: `GET /notifications`, `PATCH /notifications/{id}`, `POST /notifications/mark-all-read`
  - Notification preferences: `GET /notifications/preferences`, `PATCH /notifications/preferences`
- `docs/specs/data_model.md` v1.9 — 3 new tables: `alert_rules`, `notifications` (with delivery tracking fields per ADR-003), `notification_preferences`
- `docs/reference/openapi.yaml` — 7 new paths covering all endpoints; schemas for AlertRule, Notification, NotificationPreference
- `docs/specs/Specs_Index.md` — `alerts_endpoints.md` registered
- `docs/specs/api_contracts/api_changelog.md` — v2.1.0 entry + v2.1.1 entry (ST-13 EPIC-05 entry pre-populated as convenience — cross-EPIC content, see Deviations below)
- `docs/specs/api_contracts/README.md` — alerts_endpoints.md listed

### Acceptance criteria verification

| AC | Status | Evidence method | Notes |
|----|--------|-----------------|-------|
| `alerts_endpoints.md` created with full endpoint definitions | Pass | Code review commit 2b93a36 | 10 endpoints fully defined with request/response schemas, field tables, error codes |
| Alert rule types defined per roadmap description | Pass | Code review | 4 types: stop_loss_approach, grace_period_warning, market_regime_change, daily_portfolio_summary — all per backlog spec |
| Database schema specified in `data_model.md` | Pass | Code review | 3 tables with DDL, field definitions, constraints, indexes — data_model.md v1.9 |
| Notification preference model defined | Pass | Code review | GET/PATCH /notifications/preferences; per-type email_enabled flags; seeds defaults on first use |
| `openapi.yaml` updated in same commit | Pass | git log 2b93a36 | All 7 alert/notification paths + schemas in same commit |
| Registered in `Specs_Index.md` | Pass | Code review | Line 105 of Specs_Index.md: alerts_endpoints.md, Class 1 Canonical, v0.1 |
| Head of Specs Team sign-off | Pass | alerts_endpoints.md header | "Signed off by: Head of Specs Team, Sign-off date: 2026-03-20" |
| Architecture mode per ADR-003 reflected | Pass | Code review | "FastAPI BackgroundTasks (ADR-003, Option C)" in spec Overview §Architecture mode; no Redis/Celery required |

**DoQ evidence method:**
ST-02 is a spec-only story. All AC verification is by code/document review. No implementation to run; no staging verification required. The spec content and sign-off are the deliverables.

**Deviations:**
- **DEV-EPIC02-01 (P3 — process):** Commit 2b93a36 includes a v2.1.1 api_changelog.md entry for ST-13 (EPIC-05). Per CLAUDE.md §2, ST-13 content belongs on the EPIC-05 branch. The entry is accurate and will be consistent when both PRs merge (EPIC-05 also carries the v2.1.1 entry post-fix commit 208ca49). Impact: cosmetic — merge will succeed without conflict. Not a functional deviation. Filed as P3 observation; no remediation required beyond noting.

---

## ST-03 — Backend: Alert Rules Engine

**Classification:** delegated_backend
**Commit:** c64d074
**Spec references:**
- `docs/specs/api_contracts/alerts_endpoints.md` v0.1
- `docs/adr/ADR-003-notification-delivery-architecture.md`

### What was built

- `backend/services/alerts_service.py` — alert evaluation engine (4 rule types), CRUD for alert rules, notification creation, Telegram delivery stub
- `backend/routers/alerts.py` — 10 endpoints wired per spec
- `main.py` — router registered; `ensure_alerts_tables()` called on startup
- 34 unit tests passing

### Acceptance criteria verification

| AC | Status | Evidence method | Notes |
|----|--------|-----------------|-------|
| Alert rules CRUD endpoints implemented (GET/POST/PATCH/DELETE) | Pass | Code review c64d074 | All 4 CRUD endpoints present in routers/alerts.py |
| Alert evaluation endpoint (`POST /alerts/evaluate`) implemented | Pass | Code review | Evaluates all 4 rule types; returns rules_evaluated, notifications_created counts |
| Notification feed endpoints (GET, PATCH, POST mark-all-read) implemented | Pass | Code review | 3 notification endpoints per spec |
| Notification preferences endpoints (GET, PATCH) implemented | Pass | Code review | Seeds defaults on first use per spec |
| Database tables bootstrapped on startup | Pass | Code review | `ensure_alerts_tables()` uses CREATE IF NOT EXISTS; called on startup and lazily in preferences |
| 34 unit tests passing | Pass | Head of Engineering sign-off 2026-03-20 | All unit tests green |
| Email delivery stubbed pending ST-04 | Pass | Code review | Stub in place; wired by ST-04 |

**DoQ evidence method:** Code review. Backend — no UI behaviour. Unit test count verified by Head of Engineering sign-off.

**Deviations:** None.

---

## ST-04 — Backend: Notification Delivery (Email → Telegram)

**Classification:** delegated_backend
**Commit:** fb87043
**Spec references:**
- `docs/specs/api_contracts/alerts_endpoints.md` v0.1
- `docs/adr/ADR-003-notification-delivery-architecture.md`

### What was built

- `_send_via_telegram()` in `alerts_service.py` — Telegram Bot API delivery via urllib (no extra dependencies)
- Environment variables: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
- Delivery confirmed in staging: Telegram message received for `daily_portfolio_summary` rule 2026-03-20
- Implementation path: Resend (a5e0911) → Gmail SMTP (c858bb0) → Brevo (a0d4d61) → Telegram (fb87043)

### Acceptance criteria verification

| AC | Status | Evidence method | Notes |
|----|--------|-----------------|-------|
| Notification delivered for triggered alert types | Conditional Pass | Staging — Telegram message received 2026-03-20 | `daily_portfolio_summary` confirmed. Remaining 3 types require open positions; delivery path is identical |
| Delivery fires via BackgroundTasks post-response (ADR-003) | Pass | Code review | Consistent with ADR-003 Option C |

**DoQ evidence method:** Staging verification — Telegram message received. Director of Quality sign-off 2026-03-20.

**Deviations:**
- **DEV-ST04-01 (P2):** Delivery channel changed from email to Telegram Bot API. Gmail SMTP (port 587) blocked on Render free tier (errno 101). Brevo requires paid domain verification. Telegram Bot API operates over HTTPS port 443 — Render-compatible and free. AC met in spirit: delivery confirmed for `daily_portfolio_summary`; remaining 3 types share identical delivery path. BLG-OPS-04 filed (scheduling gap). **ACCEPTED** — Director of Quality sign-off 2026-03-20.

---

## ST-05 — Frontend: Notification Preferences Page

**Classification:** delegated_frontend
**Delegation record:** DEL-20260320-01
**Commit:** 9c4813d
**Spec references:**
- `docs/specs/frontend/pages/notifications.md`
- `docs/specs/api_contracts/alerts_endpoints.md`

### What was built

- `NotificationPreferences.js` — GET/PATCH wiring, optimistic toggle, 150ms debounce, "Saved" fade, error revert, skeleton, error state
- `NotificationTabBar.js` — Feed/Preferences sub-nav
- `PreferenceRow.js` — animated "Saved" label
- `Layout.js` / `App.js` — Notifications nav item; dual routes (`/notifications`, `/notifications/preferences`)
- Post-commit fixes: Body annotation on PATCH; route ordering (preferences before wildcard); startup race (ensure_alerts_tables on @app.on_event('startup'))

### Acceptance criteria verification

| AC | Status | Evidence method | Notes |
|----|--------|-----------------|-------|
| Preferences page renders all 4 alert types with toggles | Pass | Staging — DoQ 2026-03-20 | All 4 rows visible with label, description, toggle |
| Toggle saves with optimistic update and "Saved" confirmation | Pass | Staging — DoQ 2026-03-20 | Toggle flips immediately; "Saved" label fades |
| Error reverts toggle to prior state | Pass | Code review | Revert logic present in error handler |
| Tab bar sub-navigation (Feed / Preferences) present | Pass | Staging — DoQ 2026-03-20 | Both tabs navigate correctly |
| Sidebar nav item highlights on both routes | Pass | Staging — DoQ 2026-03-20 | isActive correct on `/notifications` and `/notifications/preferences` |

**DoQ evidence method:** Staging verification — toggle saves, "Saved" confirmation visible, Feed tab no longer 404s. Director of Quality sign-off 2026-03-20.

**Deviations:** None.

---

## ST-06 — Frontend: In-App Notification Feed

**Classification:** delegated_frontend
**Delegation record:** DEL-20260320-02
**Commit:** 47efe4b
**Spec references:**
- `docs/specs/frontend/pages/notifications.md`

### What was built

- `Notifications.js` — feed page: GET/PATCH/POST wiring, optimistic mark-as-read per-item and mark-all, load-more pagination, skeleton, empty state, error state
- `NotificationRow.js` — type icons, relative timestamp, unread cyan border, mark-as-read button
- `App.js` — `/notifications` route; `Layout.js` — nav item links to feed, isActive on both sub-routes

### Acceptance criteria verification

| AC | Status | Evidence method | Notes |
|----|--------|-----------------|-------|
| Feed renders with unread indicators (cyan left border) | Pass | Staging — DoQ 2026-03-20 | Confirmed in staging |
| Alert type icon displayed per row | Pass | Staging — DoQ 2026-03-20 | Confirmed |
| Mark-as-read per-item (optimistic, persisted) | Pass | Staging — DoQ 2026-03-20 | Confirmed |
| Mark-all-as-read (optimistic, header button hidden) | Pass | Staging — DoQ 2026-03-20 | Confirmed |
| Empty state renders with Bell icon and correct strings | Pass | Staging (live) — DoQ 2026-03-20 | Confirmed in live environment |
| Sidebar nav item active on both routes | Pass | Staging — DoQ 2026-03-20 | Confirmed |

**DoQ evidence method:** Staging verification — feed shows, empty state in live, nav highlights on both tabs. Director of Quality sign-off 2026-03-20.

**Deviations:** None.

---

## ST-07 — QA: Notification Delivery Test Scenarios — Live Execution

**Classification:** delegated_qa
**Spec reference:** `docs/testing/notifications_scenarios.md`
**Execution date:** 2026-03-21
**Executed by:** Director of Quality (live run)

### Test execution results

| Scenario | Result | Notes |
|----------|--------|-------|
| SC-NOTIF-01 — Alert evaluation creates notification and delivers via Telegram | **Pass** | `POST /alerts/evaluate` returned 200; notification created; Telegram message received |
| SC-NOTIF-02 — Notification feed displays correctly; unread indicator present | **Pass** | Feed rendered correctly with unread indicator. Only `daily_portfolio_summary` type observed — lack of test data (no open positions) for the other 3 alert types. All 3 remaining types are covered by the identical delivery path verified in SC-NOTIF-01 |
| SC-NOTIF-03 — Mark single notification as read; optimistic update | **Pass** | Optimistic update confirmed; persisted after reload |
| SC-NOTIF-04 — Mark all as read; header button hidden | **Conditional Pass** | Lack of test data: only one notification existed in the system. "Mark all as read" button was visible before marking, absent after the single notification was read — button visibility behaviour confirmed correct. Bulk mark-all operation could not be exercised with multiple unread items. See DEV-EPIC02-02 |
| SC-NOTIF-05 — Empty state displayed when no notifications exist | **Pass** | Tested in live environment; empty state rendered correctly |
| SC-NOTIF-06 — Notification preferences page loads; all four alert types displayed | **Pass** | All 4 rows, tab bar, and nav item confirmed |
| SC-NOTIF-07 — Preference toggle persists; "Saved" confirmation shown | **Pass** | Tested in live; toggle persists, "Saved" label visible |
| SC-NOTIF-08 — All four alert types can be individually toggled | **Pass** | All 4 types toggled independently; each PATCH fires correctly |

### Deviations

- **DEV-EPIC02-02 (P3 — test data):** SC-NOTIF-04 could not be fully exercised. Only one notification existed during the test run; the bulk "mark all as read" operation requires ≥2 unread notifications. The button visibility behaviour (visible when unread items exist, hidden when none remain) was confirmed correct. The bulk POST endpoint is covered by unit tests (ST-03). Full scenario re-execution is recommended when positions data is seeded for EPIC-02 regression testing.
- **DEV-EPIC02-03 (P3 — data coverage):** SC-NOTIF-02 observed only the `daily_portfolio_summary` alert type due to absence of open positions. The remaining 3 types (`stop_loss_approach`, `grace_period_warning`, `market_regime_change`) require open positions within trigger thresholds. The frontend rendering path (icon, border, timestamp) is identical across types; all 3 are out of scope per `notifications_scenarios.md §4` for this reason.

---

## EPIC-level Consolidation

| ST Item | Sprint | Spec Reference | What was built | Result | Deviations |
|---------|--------|---------------|----------------|--------|------------|
| ST-02 | Sprint 2 | alerts_endpoints.md v0.1, data_model.md v1.9, openapi.yaml | Alerts & Notifications full domain spec: 10 endpoints, 3 DB tables, openapi coverage | Pass | DEV-EPIC02-01 (P3, process — cross-EPIC changelog entry; non-functional) |
| ST-03 | Sprint 2 | alerts_endpoints.md v0.1, ADR-003 | Backend alert rules engine: evaluation, CRUD, notification creation, 10 endpoints, 34 unit tests | Pass | None |
| ST-04 | Sprint 2 | alerts_endpoints.md v0.1, ADR-003 | Telegram notification delivery; env vars TELEGRAM_BOT_TOKEN/CHAT_ID; delivery confirmed staging | Conditional Pass | DEV-ST04-01 (P2 — email→Telegram; Render SMTP blocked; accepted) |
| ST-05 | Sprint 2 | notifications.md, alerts_endpoints.md | Notification preferences page: 4 types, toggles, "Saved" feedback, tab nav, dual routes | Pass | None |
| ST-06 | Sprint 2 | notifications.md | In-app notification feed: unread indicators, type icons, mark-as-read, mark-all, empty state | Pass | None |
| ST-07 | Sprint 2 | notifications_scenarios.md | 8 SC-NOTIF scenarios executed live 2026-03-21; 7 Pass, 1 Conditional Pass (SC-NOTIF-04 — test data gap) | Pass | DEV-EPIC02-02 (P3 — SC-NOTIF-04 test data), DEV-EPIC02-03 (P3 — SC-NOTIF-02 data coverage) |

---

## QA Sign-off Block (v2.0 — updated 2026-03-21)

**Verified by Director of Quality (original sign-off 2026-03-20; updated 2026-03-21 with live SC-NOTIF execution results):**

ST-02:
- [x] `alerts_endpoints.md` created with all 10 endpoint definitions, field tables, error codes
- [x] 4 alert types defined per roadmap description
- [x] 3 data model tables with DDL, field tables, constraints
- [x] Notification preference model: per-type email_enabled; GET/PATCH endpoints; seeding behaviour
- [x] `openapi.yaml` updated in same commit: 7 paths + schemas
- [x] `Specs_Index.md` registration confirmed
- [x] Head of Specs Team sign-off in file header
- [x] Architecture mode (FastAPI BackgroundTasks per ADR-003) reflected in spec
- [x] Router ordering constraint documented (mark-all-read before /{id})
- [x] No unresolved P0 or P1 deviations

ST-03 through ST-06 (staging verification 2026-03-20):
- [x] Alert rules engine: 10 endpoints, 34 unit tests, startup bootstrapping — Head of Engineering sign-off
- [x] Telegram delivery: confirmed in staging (daily_portfolio_summary); DEV-ST04-01 (P2) accepted
- [x] Preferences page: 4 types, optimistic toggle, "Saved" label, tab nav — staging confirmed
- [x] Notification feed: unread indicators, type icons, mark-as-read, empty state — staging + live confirmed

ST-07 (SC-NOTIF live execution 2026-03-21):
- [x] SC-NOTIF-01: Pass — alert evaluation + Telegram delivery confirmed
- [x] SC-NOTIF-02: Pass — feed display and unread indicator confirmed (daily_portfolio_summary type; other 3 types data-limited, P3 deviation filed)
- [x] SC-NOTIF-03: Pass — per-item mark-as-read, optimistic update, persistence confirmed
- [x] SC-NOTIF-04: Conditional Pass — button visibility confirmed; bulk operation not testable with single notification (P3 deviation filed)
- [x] SC-NOTIF-05: Pass — empty state confirmed in live
- [x] SC-NOTIF-06: Pass — preferences page, all 4 types, tab nav, sidebar active state confirmed
- [x] SC-NOTIF-07: Pass — toggle persistence, "Saved" label confirmed in live
- [x] SC-NOTIF-08: Pass — all 4 types individually toggleable, correct PATCH keys confirmed
- [x] No unresolved P0 or P1 deviations across EPIC-02

- Signed off by: Director of Quality
- Date: 2026-03-21
- Comments: EPIC-02 QA evidence updated with live SC-NOTIF execution results (2026-03-21). All 6 stories verified. 7 of 8 scenarios Pass; SC-NOTIF-04 is Conditional Pass due to test data constraint (P3, non-blocking). Two P3 deviations filed (DEV-EPIC02-02, DEV-EPIC02-03) — both are data-coverage observations, not functional failures. No P0 or P1 deviations exist across EPIC-02. EPIC-02 is QA sign-off-ready for PR merge.

---

## Product Owner Acceptance

Accepted by: Product Owner
Date: 2026-03-20
Comments: ST-02 Alerts & Notifications spec is accepted. The domain spec covers all four alert types from the product roadmap, the notification preference model is clean and per-user-per-type, and the delivery architecture correctly follows ADR-003 (FastAPI BackgroundTasks — no new infrastructure). The three-table data model (alert_rules, notifications, notification_preferences) is well-structured and ready for backend implementation. Head of Specs Team sign-off is in place. This spec unblocks ST-03, ST-04, ST-05, ST-06, and ST-07. PR #116 is accepted.
