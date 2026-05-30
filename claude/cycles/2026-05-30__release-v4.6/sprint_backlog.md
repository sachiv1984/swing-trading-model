**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.6
**Release:** v4.6
**Sprint Goal:** Implement SI-02 Behavioural Drift Detection end-to-end — DS-07 migration, 4-metric drift service, and GET /analytics/behavioural-drift endpoint in Sprint 1; BehaviouralDriftPanel frontend and Arc 5 enablers in Sprint 2 — alongside governance debt clearance and v4.5 OA resolution, completing SI-02 as the fourth of five planned Arc 5 signals.
**Backlog Slice Source:** original — `claude/cycles/2026-05-30__release-v4.6/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-05-30__release-v4.6

---

## Sprint Scope

### Merge Order and Execution Notes

**Sprint 1 merge order: EPIC-04 → EPIC-01**
**Sprint 2 merge order: EPIC-03 → EPIC-02 (EPIC-02 conditional — amendment required if data density gate met)**

**execution_state.json owner: EPIC-04** (first EPIC in Sprint 1 execution order). All other EPICs check for file existence before creating; append their section rather than overwriting.

**Shared files:**
- `docs/reference/openapi.yaml`: EPIC-01 (ST-04) adds new endpoint; EPIC-03 (ST-09) adds severity filter. EPIC-03 must rebase onto main after EPIC-01 merges before finalising openapi.yaml changes.
- `docs/specs/api_contracts/`: EPIC-01 creates new API contract doc; EPIC-03 updates existing. Rebase sequence applies.

**Deferred at planning (conditional gates):**
- EPIC-02 (ST-06/07/08): gated on ST-16 data density audit confirming ≥20 closed trades with linked trade_plans. If gate met, invoke `amend cycle` before Sprint 2 planning seals.
- EPIC-03 ST-13: gated on SI-01 + SI-03 live ≥30 days (clears 2026-06-21). If gate met, invoke `amend cycle` before Sprint 2 planning seals with ST-13.

---

## Sprint 1

---

### EPIC-04 — Governance, Spec Debt & OA Resolution

**Maps to:** S2-04
**Owner:** Head of Specs Team; PMO Lead; Product Owner; Strategy Rules & System Intent Owner; QA Lead
**Estimated effort:** ~1.5–2 days
**Risk IDs:** RISK-05
**Execution sequence:** 1 (first in Sprint 1; execution_state.json owner)
**Branch:** `exec/2026-05-30__release-v4.6/EPIC-04`

---

#### ST-14 — OA-01: System_status_report.md v4.4 stale status correction

**Owner:** PMO Lead
**Estimated effort:** XS (~15 min)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Single document update; no cascading changes. Commit format: `[EPIC-04][ST-14] fix: System_status_report.md v4.4 section status to Verified-2026-05-29`.

**Staging-only ACs:** None

---

#### ST-15 — BLG-GOV-32 + BLG-GOV-43: release_planning_prompt.md gate scan + data density checkpoint

**Owner:** Head of Specs Team; PMO Lead; Product Owner
**Estimated effort:** S (~2–3 hrs including §6 checklist)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (independent governance patch)

**Notes:** Two backlog items (BLG-GOV-32 + BLG-GOV-43) grouped into one story to avoid duplicate §6 checklist overhead. Full §6 checklist mandatory: (1) bump release_planning_prompt.md version, (2) update OPERATIONAL_GUIDE.md §14, (3) update §6B source prompt header in OPERATIONAL_GUIDE.md, (4) append prompt_change_log.md entry. Commit separately from ST-22 (roadmap_prompt.md).

**Staging-only ACs:** None

---

#### ST-16 — BLG-GOV-33: closed trade count audit (PT-04 + SI-02 data density gate)

**Owner:** Product Owner; Challenger
**Estimated effort:** XS (~30 min)
**Delegation class:** delegated_decision (Product Owner)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None (can run at any point in Sprint 1; must complete before Sprint 2 EPIC-02 gate decision)

**Notes:** Product Owner runs production database queries. Result governs EPIC-02 Sprint 2 gate. If ≥20 trades with linked trade_plans: EPIC-02 proceeds via amendment cycle. If < 20: EPIC-02 deferred; release closes with Sprint 1 + EPIC-03 only. Result must be documented in QA evidence before Sprint 2 planning opens.

**Staging-only ACs:** AC-01 (production database query — `SELECT COUNT(*) FROM trade_history WHERE pnl IS NOT NULL`); AC-02 (production database query — join query for SI-02 gate count)

---

#### ST-17 — BLG-GOV-34: Arc 4 data density risk trajectory assessment

**Owner:** Product Owner; Challenger
**Estimated effort:** S (~2–3 hrs)
**Delegation class:** delegated_decision (Product Owner)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Produces `docs/product/decisions/arc4_data_density_trajectory_v4.6.md`. No code changes; document production only.

**Staging-only ACs:** None

---

#### ST-18 — BLG-GOV-45: Arc 6 Monte Carlo §13 pre-assessment

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** S (~2–3 hrs)
**Delegation class:** delegated_decision (Strategy Rules & System Intent Owner)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Produces `docs/product/decisions/arc6_ps03_section13_preassessment.md`. PASS or CONDITIONAL determination documented. No code changes.

**Staging-only ACs:** None

---

#### ST-19 — BLG-GOV-52: trade plan schema field count gate check

**Owner:** Data Model & Domain Schema Owner; Product Owner
**Estimated effort:** S (~1–2 hrs)
**Delegation class:** delegated_decision (Data Model & Domain Schema Owner)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** ST-01 (DS-07 migration adds 5 columns to trade_plans — ST-19 should run after ST-01 is committed so the schema audit reflects the post-migration state). Run after EPIC-01 ST-01 commits, or note pre-migration state and post-migration fields separately.

**Notes:** Produces `docs/specs/data_model/trade_plan_schema_audit_v4.6.md`. Should be done after ST-01 DS-07 migration commits so the full post-v4.6 schema is audited. If EPIC-01 branch has not merged when EPIC-04 executes ST-19, audit against current schema and note the 5 upcoming DS-07 columns as pending.

**Staging-only ACs:** None

---

#### ST-20 — BLG-GOV-41: sprint close automation failure investigation

**Owner:** PMO Lead; Infrastructure & Operations Owner
**Estimated effort:** S (~1–2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** Review GitHub Actions run logs for cycle 2026-05-22__release-v4.0. Root cause documented; resolution or retirement committed. Produces `docs/ops/sprint_close_reminder_investigation_v4.6.md`.

**Staging-only ACs:** None

---

#### ST-21 — BLG-SPEC-32: external API integration spec template

**Owner:** Head of Specs Team; API Contracts Documentation Owner
**Estimated effort:** S (~2–3 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Gate cleared (≥2 external API integrations: Alpaca, Yahoo Finance, Anthropic = 3). Produces `docs/specs/api_contracts/_external_api_template.md`. Sealed artefacts not modified retroactively — conformance gaps noted as advisory.

**Staging-only ACs:** None

---

#### ST-22 — OA-02: roadmap_prompt.md advisory — set next_release after DL decision

**Owner:** Head of Specs Team
**Estimated effort:** XS (~1 hr including §6 checklist)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None (independent of ST-15; commit separately)

**Notes:** Advisory text patch only — no hard gate added. Full §6 checklist mandatory: (1) bump roadmap_prompt.md version, (2) update OPERATIONAL_GUIDE.md §14, (3) update §6 source prompt header in OPERATIONAL_GUIDE.md, (4) append prompt_change_log.md entry. Resolves v4.5 carry-forward item 1.

**Staging-only ACs:** None

---

### EPIC-01 — SI-02 Behavioural Drift Detection: Backend

**Maps to:** S2-01
**Owner:** Head of Backend Engineering; Data Model & Domain Schema Owner
**Estimated effort:** ~1.5–2 days
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 2 (second in Sprint 1; after EPIC-04 in merge order)
**Branch:** `exec/2026-05-30__release-v4.6/EPIC-01`

---

#### ST-01 — DS-07 data migration: add SI-02 columns to trade_plans

**Owner:** Data Model & Domain Schema Owner; Head of Backend Engineering
**Estimated effort:** M (~3–4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (first story in EPIC-01)

**Notes:** RISK-01 — two separate migration files required: (a) ALTER TABLE in transaction (5 nullable columns + P1 index inside transaction or via separate CONCURRENTLY file per §6 note); (b) P2 CONCURRENTLY indexes outside transaction. Verify migration runner handles CONCURRENTLY outside transaction before committing. Both files must be reversible. Reference: `docs/specs/data_model/si02_data_schema.md §4–§6`.

**Staging-only ACs:** AC-05 ([staging-only evidence] — migration applied cleanly on staging; `\d trade_plans` confirms schema; all 3 indexes created)

---

#### ST-02 — POST /trade-plans: capture 5 new SI-02 fields at plan creation

**Owner:** Head of Backend Engineering
**Estimated effort:** M (~3–4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 (5 nullable columns must exist in trade_plans before handler update)

**Notes:** All capture is additive and backward-compatible. Existing plan creation flows with missing fields must succeed without error. Reference: `docs/specs/data_model/si02_data_schema.md §7`.

**Staging-only ACs:** None (AC-06/07 are unit tests verifiable in CI; AC-08 is QA sign-off)

---

#### ST-03 — SI-02 behavioural drift detection service (4 metrics)

**Owner:** Head of Backend Engineering
**Estimated effort:** H (~1–1.5 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-01 (trade_plans columns required for sizing_adherence and consecutive_loss_sizing metrics)

**Notes:** §13 PASS confirmed (9 binding conditions; `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md`). Output is display-only; no automated recommendations; no ML inference; all formulas deterministic. 90-day rolling window; minimum 10 closed trades. Reference: `docs/specs/metrics/si02_drift_score.md §2–§4`.

**Staging-only ACs:** None (all 4 metrics verifiable via unit tests in CI; AC-10 is QA sign-off)

---

#### ST-04 — GET /analytics/behavioural-drift endpoint, openapi.yaml, API contract

**Owner:** Head of Backend Engineering; API Contracts Documentation Owner
**Estimated effort:** M (~3–4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** ST-03 (drift service must exist before endpoint wraps it)

**Notes:** CLAUDE.md §2 same-commit rule: `GET /analytics/behavioural-drift` must be added to `docs/reference/openapi.yaml` AND `docs/specs/api_contracts/` (new file, `## GET /analytics/behavioural-drift` at `##` level) in the same commit as the endpoint. Endpoint must also be registered in `backend/routers/test.py` (hardcoded count updated) and `SC-SS-01b` in `tests/e2e/system-status.spec.js` updated to match new total (CLAUDE.md §2 rule). Returns 200 with `status: "insufficient_data"` when < 10 trades.

**Staging-only ACs:** None (AC-06/07 verifiable in CI; AC-08 is QA sign-off; openapi/contract verifiable by document inspection)

---

#### ST-05 — SI-02 unit test suite

**Owner:** QA Lead; Head of Backend Engineering
**Estimated effort:** M (~4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-03 + ST-04 (service and endpoint must exist before test suite is written)

**Notes:** ≥17 test cases total for SI-02 service. If new `database` imports added to `backend/services/position_service.py` or related services, update `_DB_STUB_FUNCTIONS` list in `tests/conftest.py` in the same commit (CLAUDE.md §2 rule). All tests must pass in CI.

**Staging-only ACs:** None (all 17+ test cases verifiable in CI; AC-08 is QA sign-off)

---

## Sprint 2

---

### EPIC-03 — Arc 5 Enablers & Gate-Cleared Items (Firm Scope)

**Maps to:** S2-03
**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner; Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** ~0.75–1 day (firm; +~1.5–2 days if ST-13 gate met)
**Risk IDs:** RISK-04
**Execution sequence:** 3 (first in Sprint 2; appends to EPIC-04-owned execution_state.json)
**Branch:** `exec/2026-05-30__release-v4.6/EPIC-03`

Note: ST-13 is deferred at planning (gate condition: 2026-06-21). Sprint 2 closes with ST-09–ST-12 if gate not met. See Items Deferred This Sprint section.

---

#### ST-09 — BLG-BE-16: red_flag_events severity field

**Owner:** Data Model & Domain Schema Owner; Head of Backend Engineering
**Estimated effort:** M (~3–4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None (gate cleared: SI-02 sprint planning imminent)

**Notes:** `openapi.yaml` must be updated for severity field and filter parameter in the same commit as the endpoint update (CLAUDE.md §2). Existing API contract updated (not a new `##` heading if endpoint already documented at `##` level). Backfill: existing red_flag_events updated with default severity. EPIC-03 must rebase onto main after EPIC-01 merges before finalising openapi.yaml changes to avoid conflict.

**Staging-only ACs:** AC-01 ([staging-only evidence] — severity column confirmed in staging DB); AC-02 ([staging-only evidence] — default severity assignment confirmed in staging); AC-03 ([staging-only evidence] — backfill of existing records confirmed on staging)

---

#### ST-10 — BLG-OPS-40: Arc 5 hosting cost projection assessment

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** S (~1–2 hrs)
**Delegation class:** delegated_decision (FinOps & Resource Architect)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None (gate cleared: SI-02 sprint planning initiated)

**Notes:** Produces `docs/ops/arc5_hosting_cost_projection.md`. Uses `api_performance_baseline.md v1.5` as reference. Recommendation must be stated (adequate / upgrade recommended with quantified rationale).

**Staging-only ACs:** None (document production; AC-05 is sign-off)

---

#### ST-11 — BLG-FE-42: Arc 5 nav cohesion review

**Owner:** Head of UX & Design
**Estimated effort:** M (~3–4 hrs)
**Delegation class:** delegated_decision (Head of UX & Design)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None (gate cleared: SI-02 sprint planning)

**Notes:** Review covers SI-01, SI-02, SI-03, SI-04, SI-05 projected nav inventory. If structural changes recommended: UX spec produced and backlog item filed. Document production only.

**Staging-only ACs:** None (document production; AC-05 is sign-off)

---

#### ST-12 — BLG-FE-47: Red Flag Journal design review scope document

**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** S (~1 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Produces `docs/specs/fe/rfj_design_review_scope.md`. Document must flag gate date for BLG-FE-41 (2026-06-21 — SI-03 live ≥30 days). Reviewed by PO and Head of UX & Design before filing. AC-02 scope boundary: if ST-09 severity field has shipped by Sprint 2, include severity colour coding in the presentation scope.

**Staging-only ACs:** None (document production; AC-05 is sign-off)

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity (both sprints) | ~48–56 days (doubled baseline) |
| Total estimated effort (firm in-scope) | ~3.75–5 days |
| Utilisation (firm) | ~7–10% |
| Over-allocation | No |
| Sprint 1 capacity | ~24–28 days; effort ~3–4 days (~12–15%) |
| Sprint 2 firm capacity | ~24–28 days; effort ~0.75–1 day (~3–4%) |
| Sprint 2 if all conditionals met | +~1.5–2 days (EPIC-02) + ~1.5–2 days (ST-13) → ~3.75–5 days total Sprint 2 (~14–18%) |

---

## Items Deferred This Sprint (Conditional — Deferred at Planning)

| Item | EPIC | Reason | Gate | Next Sprint Candidate? |
|------|------|--------|------|----------------------|
| ST-06 — BehaviouralDriftPanel component | EPIC-02 | Data density gate: ST-16 must confirm ≥20 closed trades with linked trade_plans | Product Owner confirms gate met after ST-16 result | Yes — Sprint 2 via amendment cycle if gate met |
| ST-07 — BehaviouralDriftPanel integration | EPIC-02 | Same gate as ST-06 | Same as ST-06 | Yes — Sprint 2 via amendment cycle if gate met |
| ST-08 — SI-02 Playwright test coverage | EPIC-02 | Same gate as ST-06 | Same as ST-06 | Yes — Sprint 2 via amendment cycle if gate met |
| ST-13 — BLG-GOV-67: SI-05 Phase 1 | EPIC-03 | Gate: SI-01 + SI-03 live ≥30 days; gate clears 2026-06-21 | Product Owner confirms gate met | Yes — Sprint 2 via amendment cycle if gate clears by seal |

**Deferred conditional effort (if all gates met):** EPIC-02 H+S+S ≈ 1–1.5 days; ST-13 M ≈ 1.5–2 days. Both additions remain within Sprint 2 capacity.

---

## Deferred Execution Blockers Accepted

*(Omitted — `deferred_execution_blockers` was empty in release plan state.json.)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Resolve prompt change log gaps (4 prompts — see sprint_planning_notes.md) | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — goal aligns with v4.6 release plan; SI-02 end-to-end delivery with data density gate governing EPIC-02 scope.
**Scope confirmed:** Confirmed — Sprint 1: EPIC-04 (9 stories) + EPIC-01 (5 stories); Sprint 2 firm: EPIC-03 ST-09–ST-12 (4 stories); EPIC-02 and ST-13 deferred at planning pending gate confirmation.
**Capacity confirmed:** Confirmed — double capacity; firm utilisation ~7–10%; well within bounds.
**Deferred execution blockers accepted:** N/A (none present)
**Signed off by:** Product Owner
**Date:** 2026-05-30
