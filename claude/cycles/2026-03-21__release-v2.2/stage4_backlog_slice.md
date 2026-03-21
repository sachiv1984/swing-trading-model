**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.2
**Cycle:** 2026-03-21__release-v2.2
**Last Updated:** 2026-03-21

---

# Backlog Slice — v2.2 Security, Alert Maturity & Quality

*Cycle: 2026-03-21__release-v2.2 | Planned: 2026-03-21 | Backlog source: claude/backlog/backlog.md*

---

## EPIC-01 — Security Hardening

**Maps to:** S2-01
**Owner:** Cybersecurity & Trust Lead + Backend Engineering Patterns Owner + Base44 Frontend Prompt Owner
**Description:** Implement API Key Authentication for the Render deployment and add Content Security Policy headers to the React frontend. These are the two highest-priority security baseline measures for the publicly accessible deployment.

### ST-01 — API Key Authentication for Render Deployment

**Epic:** EPIC-01
**Backlog item:** BLG-SEC-01
**Priority:** P1 (High)
**Effort:** M (~1 day)
**Owner:** Backend Engineering Patterns Owner + Base44 Frontend Prompt Owner

**Description:**
Add `X-API-Key` header requirement to all non-public API endpoints. Single hard-coded API key stored as an environment variable. Frontend includes key on all API calls.

**Acceptance Criteria:**
1. All API endpoints (except any explicitly public health or redirect endpoints) require a valid `X-API-Key` header.
2. Missing or invalid key returns HTTP 401 with standard error envelope per BLG-SPEC-G2.
3. Frontend reads API key from environment variable and includes it in all API calls via a shared API wrapper (not duplicated per component).
4. No regression to existing functionality — all existing tests pass.
5. `docs/specs/api_contracts/` updated to document the auth requirement; `openapi.yaml` updated with security scheme in same commit.
6. DoQ sign-off confirms: (a) test coverage of 401 path; (b) frontend env-var wiring confirmed via code review; (c) no endpoint left unprotected (code review or automated check).

**Sequencing:** Sprint 1. EPIC-01 highest priority; should be first story implemented.

---

### ST-02 — Content Security Policy Headers

**Epic:** EPIC-01
**Backlog item:** BLG-SEC-02
**Priority:** P3 (Low, but logical pairing with ST-01)
**Effort:** XS (<1 hour)
**Owner:** Cybersecurity & Trust Lead + Base44 Frontend Prompt Owner

**Description:**
Configure Content Security Policy (CSP) headers on the React frontend via meta tag or Render headers configuration. Restrict scripts to same-origin and used CDN sources.

**Acceptance Criteria:**
1. CSP header present on all frontend pages.
2. Browser console shows no CSP violations for normal application use (all current resources load correctly).
3. No regression to existing page functionality.
4. DoQ sign-off confirms: browser console clean under CSP (code review acceptable; local or staging run preferred).

**Sequencing:** Sprint 1. Bundle with ST-01 PR or immediately after.

---

## EPIC-02 — Alert System Maturity

**Maps to:** S2-02
**Owner:** Product Owner + Backend Engineering Patterns Owner + Data Model & Domain Schema Owner
**Description:** Complete the alert system introduced in v2.1 with: a scheduling decision and trigger mechanism design (Product Owner decision task), per-rule threshold customisation, and an alert history table for observability.

### ST-03 — Alert Scheduling: Define Trigger Mechanism and Rule Behaviour

**Epic:** EPIC-02
**Backlog item:** BLG-OPS-04
**Priority:** P1 (High)
**Effort:** S (~0.5–1 day — product design + spec output)
**Owner:** Product Owner (decision) + Backend Engineering Patterns Owner (spec authoring)

**Description:**
Product Owner answers the outstanding scheduling questions from BLG-OPS-04 and the decisions are documented in a spec update. Engineering authors the spec for the scheduler mechanism. This is a design + spec story, not an implementation story.

**Acceptance Criteria:**
1. Product Owner has answered and documented: (a) evaluation frequency (e.g. daily at market close, on-demand only, or external cron); (b) cooldown policy for stop_loss_approach and grace_period_warning; (c) source of truth for market_regime_change trigger; (d) preferred trigger mechanism (external cron, Render cron job, or other).
2. Decisions are recorded in `docs/product/decisions/` or as a spec update in `docs/specs/`.
3. `docs/specs/api_contracts/alerts_endpoints.md` updated to reflect any scheduling-related API additions (e.g. if a cron trigger endpoint is needed).
4. `openapi.yaml` updated in same commit if any new endpoint is defined.
5. This story gates ST-04 and ST-05 — no implementation begins until AC 1–4 are complete.

**Sequencing:** Sprint 1, design task. Must complete before ST-04 and ST-05 begin.

---

### ST-04 — Alert Threshold Customisation

**Epic:** EPIC-02
**Backlog item:** BLG-FEAT-10
**Priority:** P2 (Medium)
**Effort:** M (~2–3 days)
**Owner:** Backend Engineering Patterns Owner + Base44 Frontend Prompt Owner
**Depends on:** ST-03 (alert scheduling design complete; schema confirmed)

**Description:**
User-configurable numeric thresholds per alert rule type (e.g. stop_loss_approach: notify when within N% of stop). Store thresholds in the alert rule record. Frontend: threshold input fields on alert creation/edit UI.

**Acceptance Criteria:**
1. User can set a custom threshold when creating or editing an alert rule.
2. Alert evaluation uses the per-rule threshold value, not a hardcoded constant.
3. Default threshold (current hardcoded value) applies when no custom value is set (backward compatible).
4. Threshold is visible on the alert list view.
5. `docs/specs/api_contracts/alerts_endpoints.md` + `openapi.yaml` updated in same commit if request/response shape changes.
6. DoQ sign-off: threshold customisation verified (local run or staging); default behaviour regression confirmed.

**Sequencing:** Sprint 2. Gated on ST-03 complete.

---

### ST-05 — Alert History Table

**Epic:** EPIC-02
**Backlog item:** BLG-FEAT-12
**Priority:** P2 (Medium)
**Effort:** M (~2–3 days)
**Owner:** Data Model & Domain Schema Owner + Backend Engineering Patterns Owner + Base44 Frontend Prompt Owner
**Depends on:** ST-03 (scheduling design; confirms evaluation frequency and what to record)

**Description:**
New `alert_evaluations` table storing: evaluation timestamp, rule type, symbol, triggered (bool), values compared, notification_sent (bool). `GET /alerts/history` endpoint. Frontend alert history view (table/list, sortable).

**Acceptance Criteria:**
1. Every `POST /alerts/evaluate` call persists a record per rule evaluated (timestamp, rule type, symbol, triggered flag, notification_sent flag, values compared).
2. `GET /alerts/history` returns records with all above fields; supports last-N-days or last-N-records query parameter.
3. Frontend displays alert history; records sortable by date and filterable by rule type.
4. Schema migration includes down migration (reversible).
5. `docs/specs/api_contracts/alerts_endpoints.md` + `openapi.yaml` updated in same commit.
6. DoQ sign-off: history persists across evaluate calls (staging or local run); migration runs cleanly; down migration tested.

**Sequencing:** Sprint 2. Gated on ST-03 complete.

---

## EPIC-03 — Bug Fixes & Operational Quick Wins

**Maps to:** S2-03
**Owner:** Head of Engineering + Infrastructure & Operations Owner + Base44 Frontend Prompt Owner
**Description:** Three independent XS items: fix the latent CSV export function name bug, fix the Slippage StatsCard cosmetic regression, and add a health check endpoint. Bundle into a single PR.

### ST-06 — Fix CSV Export Function Name Import Bug

**Epic:** EPIC-03
**Backlog item:** BLG-BE-03
**Priority:** P2 (Medium)
**Effort:** XS (<15 min)
**Owner:** Head of Engineering

**Description:**
`backend/services/trade_service.py` (or `trade_csv_service.py`) imports `get_all_trade_history` but the actual function in `database.py` is `get_all_closed_trades_for_csv_export`. Fix the import.

**Acceptance Criteria:**
1. The incorrect import name is confirmed present before the fix (regression note in PR).
2. Import is corrected to `get_all_closed_trades_for_csv_export`.
3. `GET /trades/export/csv` returns a valid CSV without ImportError.
4. DoQ sign-off: endpoint exercised (integration test or manual call confirms no ImportError).

**Sequencing:** Sprint 1. Bundle with EPIC-03 quick wins PR.

---

### ST-07 — Fix Slippage StatsCard Gradient Key

**Epic:** EPIC-03
**Backlog item:** BLG-FE-01
**Priority:** P3 (Low)
**Effort:** XS (<30 min)
**Owner:** Base44 Frontend Prompt Owner

**Description:**
`TradeHistory.js` passes `color="cyan"` to the Avg Slippage StatsCard; the gradient map has no `"cyan"` key. Replace with a supported key (e.g. `"slate"` or `"violet"`).

**Acceptance Criteria:**
1. Avg Slippage StatsCard renders with a supported gradient key when slippage is null/zero.
2. No regression to the cell-level colour coding (emerald/rose) in `TradeHistoryTable.js`.
3. DoQ sign-off: code review sufficient (cosmetic fix; visual check preferred if local run available).

**Sequencing:** Sprint 1. Bundle with EPIC-03 quick wins PR.

---

### ST-08 — Health Check Endpoint

**Epic:** EPIC-03
**Backlog item:** BLG-OPS-06
**Priority:** P3 (Low)
**Effort:** XS (<1 hour)
**Owner:** Infrastructure & Operations Owner + Backend Engineering Patterns Owner

**Description:**
Add `GET /health` endpoint returning HTTP 200 with `{"status": "ok", "db": "connected"|"error", "last_market_status_check": "<ISO>", "last_alert_evaluation": "<ISO or null>"}`.

**Acceptance Criteria:**
1. `GET /health` returns HTTP 200 with the JSON schema above when system is healthy.
2. `db` field reflects actual DB connectivity (attempt a lightweight query).
3. `last_alert_evaluation` is null when no evaluation has been run.
4. `openapi.yaml` updated in same commit.
5. DoQ sign-off: endpoint returns 200 on staging or local run; openapi.yaml updated.

**Sequencing:** Sprint 1. Bundle with EPIC-03 quick wins PR.

---

## EPIC-04 — QA Coverage

**Maps to:** S2-04
**Owner:** Director of Quality + QA & Testing Owner
**Description:** Close QA scenario gaps flagged at v2.1 delivery verification (TSG-v21-01, TSG-v21-02), assess test automation readiness, and create a spec-to-test traceability matrix for key canonical specs.

### ST-09 — Execute Notification Scenarios on Staging

**Epic:** EPIC-04
**Backlog item:** TEST-GAP-EPIC-02
**Priority:** P2 (Medium)
**Effort:** S (~0.5 day)
**Owner:** QA & Testing Owner

**Description:**
Formally execute SC-NOTIF-01 through SC-NOTIF-08 from `docs/testing/notifications_scenarios.md` on staging. Record pass/fail results and reference in QA evidence. Three scenarios (stop_loss_approach, grace_period_warning, market_regime_change) require open positions to trigger.

**Acceptance Criteria:**
1. SC-NOTIF-01 through SC-NOTIF-08 executed on staging (or partial execution with documented blockers for data-dependent scenarios).
2. Results recorded in a QA evidence file or qa_evidence_EPIC-02.md update.
3. Any scenarios blocked by test data availability are documented with: scenario ID, blocker, and path to resolution.
4. Director of Quality sign-off on evidence record.

**Sequencing:** Sprint 2. No implementation dependency.

---

### ST-10 — Create Watchlist Test Scenarios

**Epic:** EPIC-04
**Backlog item:** TEST-GAP-EPIC-03
**Priority:** P2 (Medium)
**Effort:** S–M (~1 day)
**Owner:** QA & Testing Owner

**Description:**
Create `docs/testing/watchlist_scenarios.md` covering: SC-WATCH-01 (add), SC-WATCH-02 (edit), SC-WATCH-03 (delete), SC-WATCH-04 (Add to Position removes from watchlist), SC-WATCH-05 (duplicate 409 conflict), SC-WATCH-06 (sort order with mixed signal statuses). SC-WATCH-06 also satisfies deferred AC-6 from ST-10 (v2.1) DoQ sign-off.

**Acceptance Criteria:**
1. `docs/testing/watchlist_scenarios.md` created with SC-WATCH-01 through SC-WATCH-06.
2. Each scenario includes: preconditions, steps, expected result.
3. SC-WATCH-06 explicitly references the deferred AC-6 from ST-10 (v2.1) DoQ sign-off as the source requirement.
4. Director of Quality sign-off.

**Sequencing:** Sprint 2. No implementation dependency.

---

### ST-11 — Test Automation Readiness Assessment

**Epic:** EPIC-04
**Backlog item:** BLG-QA-02
**Priority:** P2 (Medium)
**Effort:** XS–S (~0.5–1 day)
**Owner:** QA & Testing Owner + Director of Quality
**Sequencing:** Should complete before ST-12 (traceability matrix) to confirm scope.

**Description:**
Review current test infrastructure (pytest integration tests, golden output tests, any existing Playwright setup). Map to BLG-QA-01 (Playwright E2E, deferred to v2.3) and existing TEST-GAP items. Produce a short readiness report recommending: what to automate first, with what tooling, in what sequence.

**Acceptance Criteria:**
1. Readiness assessment document produced in `docs/testing/` or as a cycle artefact.
2. Current automation coverage quantified (e.g. % endpoints with integration tests).
3. Recommended sequencing for BLG-QA-01 and other automation investments confirmed.
4. Director of Quality sign-off on the document.

**Sequencing:** Sprint 2, before ST-12.

---

### ST-12 — Spec-to-Test Traceability Matrix

**Epic:** EPIC-04
**Backlog item:** BLG-SPEC-T01
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Owner:** Director of Quality + Head of Specs Team
**Depends on:** ST-17 (Spec Coverage Inventory — ✅ shipped v2.1); ST-11 (readiness assessment confirms scope)

**Description:**
Create a spec-to-test traceability mapping: for each covered canonical spec, map each AC to the scenario ID(s) that cover it, or flag as "No scenario — gap." Start with high-value specs: alert rules, portfolio, positions, trade history.

**Acceptance Criteria:**
1. Traceability matrix exists for at least 3 canonical specs (alert rules, portfolio, positions recommended as minimum set).
2. Each AC in covered specs maps to ≥1 scenario ID, or is explicitly flagged as "No scenario — gap."
3. Gap entries are added to TEST-GAP tracking in the backlog or a dedicated gaps log.
4. Director of Quality + Head of Specs Team sign-off.

**Sequencing:** Sprint 2–3. After ST-11 (readiness assessment).

---

## EPIC-05 — Governance Process Enhancements

**Maps to:** S2-05
**Owner:** Head of Specs Team
**Description:** Apply three governance process improvements that address documented friction in prior cycles: provisional target signal from roadmap to backlog (BLG-GOV-04), effort sizing handoff from roadmap engine to release planning (BLG-GOV-05), and structured lessons learnt carry-forward block (BLG-GOV-06). All three require CLAUDE.md §6 governance edit checklist compliance.

### ST-13 — Roadmap Engine: Provisional-Target Field at Backlog Promotion

**Epic:** EPIC-05
**Backlog item:** BLG-GOV-04
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Owner:** Head of Specs Team

**Description:**
`roadmap_prompt.md` STEP 9 write instructions: when writing a promoted item to `backlog.md`, include a `**Provisional-Target:**` field derived from the item's horizon placement (Now → next planned release, Next → +1 release, Later → unscheduled). Document the field format in `shared_standards.md`. Release planning STEP 1 reads `Provisional-Target` as a candidate prioritisation input.

**Acceptance Criteria:**
1. `roadmap_prompt.md` STEP 9 includes `Provisional-Target` field requirement on new backlog items.
2. `shared_standards.md` documents the `Provisional-Target` field format and horizon-to-release mapping.
3. `release_planning_prompt.md` STEP 1 reads `Provisional-Target` as a candidate prioritisation input.
4. All four steps of CLAUDE.md §6 governance edit checklist applied to all modified files: (a) version bumped; (b) OPERATIONAL_GUIDE §14 updated; (c) phase section source prompt header updated; (d) `prompt_change_log.md` entry added in same commit.
5. Head of Specs Team sign-off (is also the owner — self-authoring is permitted; DoQ sign-off of checklist compliance required).

**Sequencing:** Sprint 3.

---

### ST-14 — Release Planning: Load scored_initiatives.md for Effort Band Handoff

**Epic:** EPIC-05
**Backlog item:** BLG-GOV-05
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Owner:** Head of Specs Team

**Description:**
Add `claude/roadmap/scored_initiatives.md` to release planning STEP 0 load list. Release planning STEP 4 capacity check references effort bands from this file rather than re-deriving sizing. Document the handoff contract in `shared_standards.md`.

**Acceptance Criteria:**
1. `release_planning_prompt.md` STEP 0 includes `scored_initiatives.md` in its load list.
2. STEP 4 capacity check references effort bands from `scored_initiatives.md` where available; falls back to STEP 4 estimate if absent.
3. `shared_standards.md` documents the handoff contract between the roadmap engine and release planning engine.
4. All four steps of CLAUDE.md §6 governance edit checklist applied (version bumps, OPERATIONAL_GUIDE §14, source prompt headers, prompt_change_log.md).
5. Head of Specs Team sign-off.

**Sequencing:** Sprint 3. Logically paired with ST-13.

---

### ST-15 — Structured Lessons Learnt Carry-Forward Block

**Epic:** EPIC-05
**Backlog item:** BLG-GOV-06
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Owner:** Head of Specs Team

**Description:**
Standardise a `## Carry-Forward` section in `lessons_learnt_closure.md` (3–5 items max: observation, implication, which engine should act). All three engines (roadmap, release planning, sprint planning) read this section at STEP 0 and surface it to the operator. Post-ship closure engine writes the Carry-Forward section.

**Acceptance Criteria:**
1. `lessons_learnt_closure.md` schema includes `## Carry-Forward` section, documented in `shared_standards.md`.
2. `roadmap_prompt.md`, `release_planning_prompt.md`, `sprint_planning_prompt.md` STEP 0 each include a Carry-Forward read-and-acknowledge step.
3. `post_ship_closure.md` writes the Carry-Forward section as a mandatory STEP output.
4. All four steps of CLAUDE.md §6 governance edit checklist applied for all modified files.
5. Head of Specs Team sign-off.

**Sequencing:** Sprint 3. Logically paired with ST-13 and ST-14.

---

<!-- release-plan-marker: RP:v2.2:2026-03-21__release-v2.2 -->

---

## Summary

| EPIC | Stories | Sprint | Theme |
|------|---------|--------|-------|
| EPIC-01 | ST-01, ST-02 | Sprint 1 | Security Hardening |
| EPIC-02 | ST-03 (S1), ST-04, ST-05 (S2) | Sprint 1–2 | Alert System Maturity |
| EPIC-03 | ST-06, ST-07, ST-08 | Sprint 1 | Bug Fixes & Quick Wins |
| EPIC-04 | ST-09–ST-12 | Sprint 2–3 | QA Coverage |
| EPIC-05 | ST-13–ST-15 | Sprint 3 | Governance Process |
| **Total** | **15 stories** | **3 sprints** | Capacity: WARN (~16 days estimated) |

**Phasing recommendation:** See release_plan.md §Capacity Check §Phasing Recommendation.
