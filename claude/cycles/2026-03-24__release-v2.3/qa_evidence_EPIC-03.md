Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-25

---

# QA Evidence Log — EPIC-03 (Operational Readiness & Spec Debt)

**Cycle:** 2026-03-24__release-v2.3
**Sprint goal:** Establish a reproducible QA automation layer, deliver user-facing compliance and metrics features, and resolve all outstanding frontend polish and operational spec debt for v2.3.

---

## ST-07 — BLG-SPEC-D14: Update health_endpoints.md to v1.1

**Spec reference:** `docs/specs/api_contracts/health_endpoints.md#GET /health`
**Commit:** b4d4c88 on `exec/2026-03-24__release-v2.3/EPIC-03`
**Classification:** autonomous

**What was built:** Updated `docs/specs/api_contracts/health_endpoints.md` from v1.0 to v1.1 to document the actual GET /health response schema shipped in v2.2. DEV-HEALTH-001 deviation closed — spec now matches implementation. openapi.yaml `OperationalHealthResponse` was already correct (no changes required).

**Acceptance criteria:**
- [x] `health_endpoints.md` updated to v1.1 documenting current response schema: `{"status": "ok"|"error", "db": "connected"|"error", "last_market_status_check": "<ISO or null>", "last_alert_evaluation": "<ISO or null>"}` — **verified by code review**
- [x] openapi.yaml OperationalHealthResponse schema matches v1.1 spec — **verified by code review (already correct)**
- [x] No functional changes required — **confirmed**

**Test scenarios:** Documentation-only change. No runtime scenarios required.

**Deviations:** None. DEV-HEALTH-001 closed.

---

## ST-08 — BLG-OPS-09: Database Size Monitoring Alert

**Spec reference:** `docs/specs/api_contracts/alerts_endpoints.md`; `docs/adr/ADR-003-notification-delivery-architecture.md`
**Commit:** Pending — delegated to Head of Engineering (DEL-20260325-01)
**Classification:** delegated_backend

**What was built:**
- `backend/database.py`: `get_database_size_bytes()` — queries `pg_database_size(current_database())` and returns bytes.
- `backend/services/health_service.py`: `get_db_size_info()` — returns current size, MB, percentage of Render 256 MB limit, threshold, and status (`ok`/`warning`/`error`). `send_db_size_alert_if_needed()` — sends Telegram notification when usage ≥ threshold; 1-hour cooldown via module-level state; notification-only, no automated cleanup.
- `backend/main.py`: `GET /health/database` endpoint registered.
- `docs/specs/api_contracts/health_endpoints.md`: bumped v1.1 → v1.2 with full `GET /health/database` section.
- `docs/reference/openapi.yaml`: bumped 2.1.2 → 2.2.0; added `/health/database` path, `DatabaseSizeResponse` schema, `OkDatabaseSize` response.

**Acceptance criteria:**
- [x] DB size monitoring configured and active — `GET /health/database` queries live DB size on every call; `DB_SIZE_ALERT_THRESHOLD_PERCENT` env var (default 80%) configures threshold. **Verified by code review.**
- [x] Alert sent to user when DB exceeds configured threshold — `send_db_size_alert_if_needed()` fires Telegram notification when `used_percent >= threshold_percent`. **Verified by code review.**
- [x] Alert is notification-only — no automated cleanup (§3 compliance) — no cleanup logic in implementation; §3 compliance noted in endpoint docstring and service docstring. **Verified by code review.**
- [x] Current DB size queryable — `GET /health/database` returns `size_bytes`, `size_mb`, `used_percent`. **Verified by code review.**
- [x] openapi.yaml updated — `/health/database` path and `DatabaseSizeResponse` schema added in same commit as contract. **Verified by code review.**

**Test scenarios:** Tier 2 service (DB-dependent). No Tier 1 unit tests added. Manual verification at delivery verification: call `GET /health/database`, confirm response shape matches spec.

**Evidence method:** Code review. AC requiring observable runtime behaviour (Telegram alert, threshold trigger) — post-merge manual verification action for DoQ.

**Deviations:** None. DoQ to confirm at delivery verification.

---

## ST-09 — BLG-OPS-07: System Health Check Playbook

**Spec reference:** `docs/specs/api_contracts/health_endpoints.md#GET /health`
**Commit:** d93f05c on `exec/2026-03-24__release-v2.3/EPIC-03`
**Classification:** autonomous

**What was built:** Created `docs/operations/health_check_playbook.md` — operational runbook documenting interpretation and response procedures for all GET /health signals. Covers 3 failure modes: DB error (`db: error`), market status check stalled (`last_market_status_check` stale/null), and alert evaluation stalled (`last_alert_evaluation` stale/null). Each failure mode includes diagnosis steps, common causes table, and recovery verification step. References health_endpoints.md v1.1.

**Acceptance criteria:**
- [x] Playbook document present in `docs/` covering all health signals from the `GET /health` response — **verified by code review**
- [x] Each failure mode (DB error, alert evaluation stalled, market status stale) has a diagnosis + recovery path — **verified by code review**
- [x] Document references health_endpoints.md v1.1 schema — **verified by code review**

**Test scenarios:** Documentation-only change. No runtime scenarios required.

**Deviations:** None.

---

## EPIC-03 Consolidation Block

*(To be completed when all ST items are done — pending ST-08 delegation)*

**EPIC:** EPIC-03 — Operational Readiness & Spec Debt
**Cycle:** 2026-03-24__release-v2.3
**Sprint goal:** Establish a reproducible QA automation layer, deliver user-facing compliance and metrics features, and resolve all outstanding frontend polish and operational spec debt for v2.3.
**Test scenarios used:** Documentation-only items (ST-07, ST-09 require no test scenario files). ST-08 backend item — scenarios TBD post-delivery.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-07 | health_endpoints.md#GET /health | health_endpoints.md v1.0→v1.1, DEV-HEALTH-001 closed | Schema updated, openapi.yaml verified | Pass | None |
| ST-08 | health_endpoints.md#GET /health/database | GET /health/database endpoint + Telegram alert; health_endpoints.md v1.2; openapi.yaml v2.2.0 | DB size monitored, alert fires at threshold, notification-only, openapi updated | Pass (code review) | None |
| ST-09 | health_endpoints.md#GET /health | health_check_playbook.md with 3 failure modes | Playbook present, all signals covered | Pass | None |

**QA test coverage:**
- Scenarios run: No scenario files required (all documentation items). ST-08 backend: TBD.
- Regression areas checked: health_endpoints.md spec alignment; no backend functional changes for ST-07 or ST-09.
- Known deviations filed: None (DEV-HEALTH-001 closed).

**QA sign-off block:** *(Director of Quality completes this when ST-08 is done)*
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction: confirm base URL variable exposed
- Signed off by: Director of Quality
- Date:
- Comments:
