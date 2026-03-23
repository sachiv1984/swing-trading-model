**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-23
**Cycle:** 2026-03-21__release-v2.2

---

# Delegation Log — 2026-03-21__release-v2.2

*Append-only. Do not edit previous entries.*

---

## DEL-20260322-01 — ST-01: API Key Authentication for Render Deployment (Spec Phase)

**Date:** 2026-03-22
**Assigned To:** Head of Specs Team
**Classification:** delegated_decision (reclassified from delegated_backend)
**GitHub Issue:** #118
**Branch:** exec/2026-03-21__release-v2.2/EPIC-01
**Status:** Resolved — 2026-03-23

**Resolution:** conventions.md §1 authored (v1.1) and approved by Head of Specs Team (agent-mediated sign-off). ST-01 reclassified to delegated_backend and reassigned to Head of Engineering via DEL-20260323-01.

**Reason for delegation:**
conventions.md §1 explicitly states authentication is "out of scope" — no lockable spec exists for X-API-Key auth. Per execution_prompt §5 rule, a delegated_backend item with no lockable spec must be reclassified to delegated_decision and surfaced to Head of Specs Team.

**Decision required:**
Author a canonical spec section for X-API-Key authentication. Options:
1. Update `docs/specs/api_contracts/conventions.md` §1 to document the X-API-Key scheme, 401 envelope, and exemption list (e.g. GET /health, redirect endpoints).
2. Create a new `docs/specs/api_contracts/security_endpoints.md` or `auth_conventions.md`.

Once spec is locked and marked Canonical, re-classify ST-01 to `delegated_backend` and delegate implementation to Head of Engineering.

**Unblock criteria:**
- Canonical spec section for X-API-Key authentication authored and status set to Canonical
- spec_references field populated in execution_state.json for ST-01
- Head of Engineering assigned implementation

**Commit format when complete:** `[EPIC-01][ST-01] <description>`
**SLA:** 24 hours (lifecycle decision)

---

## DEL-20260323-01 — ST-01: API Key Authentication for Render Deployment (Implementation)

**Date:** 2026-03-23
**Assigned To:** Head of Engineering
**Classification:** delegated_backend
**GitHub Issue:** #118
**Branch:** exec/2026-03-21__release-v2.2/EPIC-01
**Status:** Pending
**Supersedes:** DEL-20260322-01 (spec phase — resolved)

**Locked spec:** `docs/specs/api_contracts/conventions.md §1` (v1.1, Canonical)

**What is needed:**

Implement X-API-Key authentication per `conventions.md §1`. The spec is now locked.

**Backend tasks:**
1. Add FastAPI middleware (or dependency injection) that reads `API_KEY` from environment and validates the `X-API-Key` request header on all incoming requests.
2. Return HTTP 401 with `{"status": "error", "message": "Unauthorized"}` on missing or invalid key — per conventions.md §1.3 and §13.
3. Exempt `GET /health` — no auth check required for that path.
4. All existing tests must pass (AC-4).

**Frontend tasks:**
5. Read `REACT_APP_API_KEY` from environment and include as `X-API-Key` header on all API calls via the shared API wrapper (not per-component — per conventions.md §1.2).

**OpenAPI tasks (same commit as implementation):**
6. Add `security: []` path-level override on `GET /health` in `docs/reference/openapi.yaml` to mark it exempt.
7. Remove `description: "API key for authentication (future use)"` from the `ApiKey` securityScheme — replace with `"API key required for all non-exempt endpoints. Passed as X-API-Key header."`.

**DoQ requirements (AC-6):**
- (a) 401 path tested (unit or integration test)
- (b) Frontend env-var wiring confirmed via code review
- (c) No endpoint left unprotected (code review or automated check)

**Commit format:** `[EPIC-01][ST-01] Add X-API-Key authentication middleware and frontend env-var wiring`
**Unblock criteria:** All 7 tasks complete; AC-1 through AC-6 verified; DoQ sign-off obtained.

---

## DEL-20260322-02 — ST-03: Alert Scheduling Design

**Date:** 2026-03-22
**Assigned To:** Product Owner
**Classification:** delegated_decision
**GitHub Issue:** #120
**Branch:** exec/2026-03-21__release-v2.2/EPIC-02
**Status:** Resolved — 2026-03-23

**Resolution:** Product Owner made all four decisions (A–D). Challenger review completed: 4 must-answer challenges resolved, 3 worth-noting items acknowledged and recorded. Decision document authored at `docs/product/decisions/decisions--2026-03-21__release-v2.2.md §ST-03 Execution Decisions`. ST-04 and ST-05 are now unblocked.

**Decision required:**
Product Owner must document the following alert scheduling decisions:
(a) Evaluation frequency — e.g. daily at market close, on-demand only, or external cron
(b) Cooldown policy — for stop_loss_approach and grace_period_warning alert types
(c) Source of truth for market_regime_change trigger
(d) Preferred trigger mechanism — external cron, Render cron job, or other

Decisions must be recorded in `docs/product/decisions/` or as a spec update in `docs/specs/` (alerts_endpoints.md or new scheduling decisions doc).

**Unblock criteria:** AC 1–4 of ST-03 all complete. ST-04 and ST-05 may not begin until this item is unblocked.
**SLA:** 72 hours (strategy decision)

---

## DEL-20260322-03 — ST-09: Execute Notification Scenarios on Staging

**Date:** 2026-03-22
**Assigned To:** QA & Testing Owner
**Classification:** delegated_qa
**GitHub Issue:** #126
**Branch:** exec/2026-03-21__release-v2.2/EPIC-04
**Status:** Pending

**What is needed:**
Execute SC-NOTIF-01 through SC-NOTIF-08 from `docs/testing/notifications_scenarios.md` on staging. Record pass/fail results in `claude/cycles/2026-03-21__release-v2.2/qa_evidence_EPIC-04.md`.

3 of 8 scenarios (stop_loss_approach, grace_period_warning, market_regime_change) require open positions to trigger — partial execution acceptable, blocked scenarios must be documented with: scenario ID, blocker, path to resolution.

**Commit format:** `[EPIC-04][ST-09] Execute notification test scenarios — staging results`
**Unblock criteria:** All 8 scenarios attempted; results recorded; Director of Quality sign-off on evidence record.

---

## DEL-20260322-04 — ST-10: Create Watchlist Test Scenarios

**Date:** 2026-03-22
**Assigned To:** QA & Testing Owner
**Classification:** delegated_qa
**GitHub Issue:** #127
**Branch:** exec/2026-03-21__release-v2.2/EPIC-04
**Status:** Pending

**What is needed:**
Create `docs/testing/watchlist_scenarios.md` covering SC-WATCH-01 through SC-WATCH-06. Each scenario must include: preconditions, steps, expected result.

SC-WATCH-06 must explicitly reference the deferred AC-6 from ST-10 (v2.1) DoQ sign-off as the source requirement.

**Commit format:** `[EPIC-04][ST-10] Create watchlist test scenarios SC-WATCH-01 through SC-WATCH-06`
**Unblock criteria:** File created; all 6 scenarios have full structure; SC-WATCH-06 cross-references v2.1 deferred AC; Director of Quality sign-off.

---

## DEL-20260322-05 — ST-11: Test Automation Readiness Assessment

**Date:** 2026-03-22
**Assigned To:** QA & Testing Owner
**Classification:** delegated_qa
**GitHub Issue:** #128
**Branch:** exec/2026-03-21__release-v2.2/EPIC-04
**Status:** Pending

**What is needed:**
Produce a readiness assessment document in `docs/testing/` covering:
- Current automation coverage quantified (% endpoints with integration tests)
- Map to BLG-QA-01 (Playwright E2E, deferred to v2.3)
- Recommended sequencing for BLG-QA-01 and other automation investments

**Commit format:** `[EPIC-04][ST-11] Add test automation readiness assessment`
**Unblock criteria:** Document produced; coverage quantified; sequencing confirmed; Director of Quality sign-off. Should complete before ST-12.

---

## DEL-20260322-06 — ST-12: Spec-to-Test Traceability Matrix

**Date:** 2026-03-22
**Assigned To:** Director of Quality (with Head of Specs Team co-sign)
**Classification:** delegated_qa
**GitHub Issue:** #129
**Branch:** exec/2026-03-21__release-v2.2/EPIC-04
**Status:** Pending

**What is needed:**
Create a spec-to-test traceability matrix for at least 3 canonical specs (alert rules, portfolio, positions recommended). For each AC in covered specs: map to ≥1 scenario ID, or flag as "No scenario — gap." Gap entries must be added to TEST-GAP tracking.

Gated on ST-11 completion. Target: Sprint 3.

**Commit format:** `[EPIC-04][ST-12] Add spec-to-test traceability matrix`
**Unblock criteria:** Matrix covers ≥3 specs; each AC mapped or flagged; gaps in TEST-GAP tracking; Director of Quality + Head of Specs Team sign-off.

---

## DEL-20260322-07 — ST-13: Roadmap Engine Provisional-Target Field

**Date:** 2026-03-22
**Assigned To:** Head of Specs Team
**Classification:** delegated_decision
**GitHub Issue:** #130
**Branch:** exec/2026-03-21__release-v2.2/EPIC-05
**Status:** Pending

**What is needed:**
Modify the following files per AC 1–3:
1. `claude/system/roadmap_prompt.md` STEP 9 — add Provisional-Target field requirement on new backlog items
2. `claude/system/shared_standards.md` — document Provisional-Target field format and horizon-to-release mapping
3. `claude/system/release_planning_prompt.md` STEP 1 — read Provisional-Target as a candidate prioritisation input

**Mandatory for each modified file (CLAUDE.md §6):**
(a) Version bumped; (b) OPERATIONAL_GUIDE §14 updated; (c) phase section source prompt header updated; (d) `prompt_change_log.md` entry added — all in same commit.

**Commit format:** `[EPIC-05][ST-13] Add Provisional-Target field to roadmap → backlog promotion`
**Unblock criteria:** All 3 files updated; §6 checklist applied to each; external DoQ review of checklist compliance.
**SLA:** 72 hours (governance content decision)

---

## DEL-20260322-08 — ST-14: Release Planning Load scored_initiatives.md

**Date:** 2026-03-22
**Assigned To:** Head of Specs Team
**Classification:** delegated_decision
**GitHub Issue:** #131
**Branch:** exec/2026-03-21__release-v2.2/EPIC-05
**Status:** Pending

**What is needed:**
Modify per AC 1–3:
1. `claude/system/release_planning_prompt.md` STEP 0 — add scored_initiatives.md to load list
2. `claude/system/release_planning_prompt.md` STEP 4 — reference effort bands from scored_initiatives.md; fall back to STEP 4 estimate if absent
3. `claude/system/shared_standards.md` — document the handoff contract between roadmap engine and release planning engine

CLAUDE.md §6 checklist required for all modified files.

**Commit format:** `[EPIC-05][ST-14] Load scored_initiatives.md in release planning for effort band handoff`
**Unblock criteria:** All changes per AC 1–3; §6 checklist applied; Head of Specs Team sign-off.
**SLA:** 72 hours (governance content decision)

---

## DEL-20260322-09 — ST-15: Structured Lessons Learnt Carry-Forward Block

**Date:** 2026-03-22
**Assigned To:** Head of Specs Team
**Classification:** delegated_decision
**GitHub Issue:** #132
**Branch:** exec/2026-03-21__release-v2.2/EPIC-05
**Status:** Pending

**What is needed:**
Modify per AC 1–3:
1. `claude/system/shared_standards.md` — document Carry-Forward section schema (3–5 items: observation, implication, which engine should act)
2. `claude/system/roadmap_prompt.md`, `release_planning_prompt.md`, `sprint_planning_prompt.md` STEP 0 — add carry-forward read-and-acknowledge step
3. `claude/system/post_ship_closure.md` — add Carry-Forward section write as mandatory STEP output

CLAUDE.md §6 checklist required for ALL modified files (largest change set in EPIC-05).

**Commit format:** `[EPIC-05][ST-15] Add structured lessons learnt carry-forward block to all engines`
**Unblock criteria:** All changes per AC 1–3; §6 checklist applied to each modified file; Head of Specs Team sign-off.
**SLA:** 72 hours (governance content decision)
