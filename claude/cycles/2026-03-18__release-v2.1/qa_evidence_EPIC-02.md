**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Signed Off — complete
**Version:** 1.0
**Last Updated:** 2026-03-20

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

## EPIC-level Consolidation

| ST Item | Sprint | Spec Reference | What was built | Result | Deviations |
|---------|--------|---------------|----------------|--------|------------|
| ST-02 | Sprint 2 | alerts_endpoints.md v0.1, data_model.md v1.9, openapi.yaml | Alerts & Notifications full domain spec: 10 endpoints, 3 DB tables, openapi coverage | Pass | DEV-EPIC02-01 (P3, process — cross-EPIC changelog entry; non-functional) |

---

## QA Sign-off Block

**Verified by Director of Quality review (2026-03-20):**
- [x] `alerts_endpoints.md` created with all 10 endpoint definitions, field tables, error codes
- [x] 4 alert types defined per roadmap description
- [x] 3 data model tables (alert_rules, notifications, notification_preferences) with DDL, field tables, constraints
- [x] Notification preference model: per-type email_enabled; GET/PATCH endpoints; seeding behaviour
- [x] `openapi.yaml` updated in same commit: 7 paths + schemas
- [x] `Specs_Index.md` registration confirmed
- [x] Head of Specs Team sign-off in file header
- [x] Architecture mode (FastAPI BackgroundTasks per ADR-003) reflected in spec
- [x] Router ordering constraint documented (mark-all-read before /{id})
- [x] No unresolved P0 or P1 deviations

- Signed off by: Director of Quality
- Date: 2026-03-20
- Comments: ST-02 spec is complete and sign-off-ready. All 7 ACs pass. The alerts domain spec is coherent with ADR-003, covers all 4 alert types from the roadmap, includes a comprehensive data model, and has full openapi.yaml coverage. One P3 process deviation (cross-EPIC changelog entry) noted — non-functional, non-blocking.

---

## Product Owner Acceptance

Accepted by: Product Owner
Date: 2026-03-20
Comments: ST-02 Alerts & Notifications spec is accepted. The domain spec covers all four alert types from the product roadmap, the notification preference model is clean and per-user-per-type, and the delivery architecture correctly follows ADR-003 (FastAPI BackgroundTasks — no new infrastructure). The three-table data model (alert_rules, notifications, notification_preferences) is well-structured and ready for backend implementation. Head of Specs Team sign-off is in place. This spec unblocks ST-03, ST-04, ST-05, ST-06, and ST-07. PR #116 is accepted.
