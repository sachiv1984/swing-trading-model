**Owner:** Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Active
**Last Updated:** 2026-05-15
**Cycle:** 2026-05-15__release-v3.5

---

# QA Evidence — EPIC-03: Spec & QA Debt

**EPIC:** EPIC-03 — Spec & QA Debt
**Cycle:** 2026-05-15__release-v3.5
**Sprint goal:** Complete Arc 3's Alpaca paper trading integration (§13 gate permitting) and establish Arc 4 foundations with the Plan vs Reality analysis service, while clearing all v3.4 spec, QA, and governance debt.
**Branch:** `exec/2026-05-15__release-v3.5/EPIC-03`

---

## Story Evidence

### ST-07 — BLG-SPEC-29: Correct grace-period-alert ux_spec.md sessionStorage

**Spec reference:** `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md`
**Commit:** `736ce8f1`
**What was built:** `ux_spec.md` v1.0→v1.1: §5 corrected to reference `sessionStorage` (not `localStorage`) for dismiss persistence; added note "Dismiss resets on tab close; alert reappears in a new browser session."; DEV-v3.4-01 marked ✅ RESOLVED v3.5.

**Acceptance criteria:**
- [x] AC-1: `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md` §5 updated to reference `sessionStorage`
- [x] AC-2: §5 note added re tab-close reset
- [x] AC-3: No implementation change required — confirmed; spec-only change
- [x] AC-4: BLG-SPEC-29 marked ✅ COMPLETE v3.5 in backlog

**Result:** Pass
**Deviations:** None

Note: AC-1 in `stage4_backlog_slice.md` references `docs/ux_specs/grace-period-alert/ux_spec.md`. Actual canonical file is at `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md` per design gate record and sprint_backlog.md notes. Intent check: spec intent and implementation match — no deviation filed per LL-v3.4-P3-03.

---

### ST-08 — BLG-SPEC-30: Correct stop-management-workflow ux_spec.md HTTP verb

**Spec reference:** `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md`
**Commit:** `736ce8f1`
**What was built:** `ux_spec.md` v1.0→v1.1: §4.4 corrected to reference `PATCH /positions/{id}` (not `PUT /positions/{id}`); DEV-v3.4-01 marked ✅ RESOLVED v3.5.

**Acceptance criteria:**
- [x] AC-1: `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md` §4.4 updated to reference `PATCH /positions/{id}`
- [x] AC-2: No implementation change required — confirmed; spec-only change
- [x] AC-3: BLG-SPEC-30 marked ✅ COMPLETE v3.5 in backlog

**Result:** Pass
**Deviations:** None

Note: Same path note applies as ST-07 — AC-1 in slice references `docs/ux_specs/stop-management-workflow/...`; actual path used per design gate record. Intent match confirmed per LL-v3.4-P3-03.

---

### ST-09 — BLG-SPEC-31: React Query v5 onSuccess Codebase Scan

**Spec reference:** None — scan + fix task
**Commits:** `736ce8f1` (fix), `39c25cc8` (Playwright test SC-TP-08)
**What was built:**
- Full scan of `src/` for `onSuccess` in `useQuery` calls. One active issue found: `TradePlan.js` line 125 had `onSuccess` inside `useQuery` — silently dropped by React Query v5, causing edit-mode form pre-population to fail.
- Fixed by removing `onSuccess` from `useQuery` config and adding `useEffect` watching `existingPlan` data.
- All other `onSuccess` usages (Signals.js, TradePlans.js, TradeEntry.js, Positions.js, CashManagementModal.js, Settings.js, SystemStatus.js) confirmed in `useMutation` calls — unaffected.
- SC-TP-08 Playwright test added to `tests/e2e/trade-plan.spec.js`: verifies form pre-population in edit mode (`?edit={id}`). 9/9 tests pass.

**Acceptance criteria:**
- [x] AC-1: All `useQuery` calls in `src/` scanned for `onSuccess` usage
- [x] AC-2: `TradePlan.js` identified as affected — `onSuccess` in `useQuery` silently dropped
- [x] AC-3: Fix applied: `useEffect` with `existingPlan` dependency; behaviour equivalent
- [x] AC-4: Closure note filed in BLG-SPEC-31 backlog entry
- [x] AC-5: E2E test coverage added: SC-TP-08 in `tests/e2e/trade-plan.spec.js`; 9/9 pass
- [x] AC-6: BLG-SPEC-31 marked ✅ COMPLETE v3.5 in backlog

**Result:** Pass
**Deviations:** None

**Playwright evidence:**
```
Running 9 tests using 1 worker
9 passed (15.6s)
```
SC-TP-08: Edit mode pre-populates form fields from GET /trade-plans/{id} — PASS

---

### ST-10 — BLG-QA-19: Research View Regression Test Protocol

**Spec reference:** `docs/qa/acceptance_protocols/research_view_regression_protocol.md` (v0.1 draft)
**Commit:** `1315ecbe`
**Classification:** delegated_qa
**Delegation record:** DEL-20260515-01 in `claude/cycles/2026-05-15__release-v3.5/delegation_log.md`
**Status:** Complete — QA Lead sign-off received (2026-05-15)
**Commit (sign-off):** `a80144ad`

**What was built (engine contribution):**
- `docs/qa/acceptance_protocols/research_view_regression_protocol.md` v0.1 created: canonical regression suite (SC-RES-01–13), SC-RV-18/19 gap note with BLG-FE-33 reference, IT-series checklist (IT-04/05 covered)
- `docs/specs/api_contracts/research_endpoint.md` v1.0→v1.1: regression test anchor cross-reference added

**QA Lead corrections applied (commit a80144ad):**
- §4 IT-04/IT-05 references replaced with PT-03/PT-05 (correct feature IDs)
- BLG-FE-33 → BLG-FE-32 (correct backlog ID)
- SC-RES-01–13 confirmed canonical; SC-RV-18/19 gap confirmed; BLG-QA-19 COMPLETE

**Acceptance criteria:**
- [x] AC-1: `docs/qa/acceptance_protocols/research_view_regression_protocol.md` created (v0.1→v1.0)
- [x] AC-2: Protocol defines canonical regression suite for `/research/{ticker}` and research view
- [x] AC-3: Protocol covers PT-02 base fields, PT-03/PT-05 additions, null/degraded state handling (SC-RV-18/SC-RV-19 gap noted)
- [x] AC-4: Protocol explicitly references existing test IDs from `tests/e2e/`
- [x] AC-5: Protocol cross-referenced in `docs/specs/api_contracts/research_endpoint.md`
- [x] **AC-6: QA Lead sign-off recorded in document** — v0.1→v1.0, corrections applied (commit a80144ad)
- [x] **AC-7: BLG-QA-19 marked COMPLETE in backlog** — COMPLETE v3.5

**Result:** Pass
**Deviations:** None

---

## QA test coverage summary

| Story | Test method | Scenarios | Result |
|-------|-------------|-----------|--------|
| ST-07 | Code review — spec-only change | None applicable | Pass |
| ST-08 | Code review — spec-only change | None applicable | Pass |
| ST-09 | Playwright SC-TP-08 + code review | SC-TP-01–08 (9/9 pass) | Pass |
| ST-10 | QA Lead sign-off (human) | SC-RES-01–13 canonical; protocol v1.0 | Pass |

---

## DoQ Consolidation Sign-off

| Story | P | Deviation | Backlog item | Priority |
|-------|---|-----------|-------------|----------|
| ST-07 | Pass | None | BLG-SPEC-29 ✅ COMPLETE | — |
| ST-08 | Pass | None | BLG-SPEC-30 ✅ COMPLETE | — |
| ST-09 | Pass | None | BLG-SPEC-31 ✅ COMPLETE | — |
| ST-10 | Pass | None | BLG-QA-19 ✅ COMPLETE | — |

**Signed off by:** Director of Quality — 2026-05-15
**Test run date:** 2026-05-15 — QA Lead sign-off received; SC-TP-08 Playwright test 9/9 pass
**Comments:** ST-07/08 are spec-only corrections. ST-09 code fix verified by SC-TP-08. ST-10 QA Lead sign-off (human) received via DEL-20260515-01 Completed (commit a80144ad). All 4 stories Pass.
