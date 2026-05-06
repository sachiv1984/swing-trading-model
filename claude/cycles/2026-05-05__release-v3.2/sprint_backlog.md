**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-06
**Cycle:** 2026-05-05__release-v3.2
**Release:** v3.2
**Sprint Goal:** Ship the Pre-Trade Research View (PT-02) and Prospective Heat integration (PT-03) in Sprint 1 and the Pre-Trade Entry Checklist (PT-05) in Sprint 2, completing Arc 2's primary user-value deliverables, while clearing four v3.1 governance deferred actions and five documentation/security backlog items.
**Backlog Slice Source:** original stage4_backlog_slice.md

---

# Sprint Backlog — 2026-05-05__release-v3.2

---

## Sprint Scope

---

### Sprint 1

---

#### EPIC-03 — Governance & Process Hardening

**Maps to:** S2-04, S2-05
**Owner:** Head of Specs Team
**Estimated effort:** ~2–3 days (XS×4 + S×2)
**Risk IDs:** RISK-03
**Execution sequence:** 1 (first in Sprint 1 — autonomous patches deploy before EPIC-01 frontend work)

##### ST-07 — sprint_planning_prompt.md STEP 0 main-branch verification

**Owner:** Head of Specs Team
**Estimated effort:** XS (~30 min)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** None
**Notes:** Source: OA-02 / D-01 (v3.1 lessons_learnt_closure.md). CLAUDE.md §6 checklist (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry) required in same commit. Commit message: `[EPIC-03][ST-07] <description>`.

---

##### ST-08 — execution_prompt.md STEP 5.1 deviations_filed enforcement

**Owner:** Head of Specs Team
**Estimated effort:** XS (~30 min)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None
**Notes:** Source: OA-03 / D-02 (v3.1 lessons_learnt_closure.md). May be combined with ST-09 and/or ST-10 in a single commit — all story IDs must appear in commit message per CLAUDE.md governance non-negotiables. CLAUDE.md §6 checklist required.

---

##### ST-09 — execution_prompt.md §3.1.A test_scenarios post-story advisory

**Owner:** Head of Specs Team
**Estimated effort:** XS (~30 min)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None
**Notes:** Source: OA-04 / D-03 (v3.1 lessons_learnt_closure.md — recurrence from v3.0 TSG-v30-01). May combine with ST-08 and/or ST-10 in same commit. CLAUDE.md §6 checklist required.

---

##### ST-10 — Playwright waitFor pattern — test authoring standard

**Owner:** Head of Specs Team / QA & Testing Owner
**Estimated effort:** XS (~30–60 min)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** None
**Notes:** Source: OA-05 / D-04 (v3.1 lessons_learnt_closure.md — carry-forward from v3.0 CF-03). Scan all existing Playwright test files for `networkidle` usage; replace with `waitFor` pattern. May combine with ST-08/ST-09 in same commit. CLAUDE.md §6 checklist required.

---

##### ST-11 — Trade Plan domain test scenario registration (TEST-GAP-EPIC-01)

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** None
**Notes:** Source: TEST-GAP-EPIC-01 (v3.1 delivery verification). Verify `tests/e2e/trade-plan.spec.js` exists; register SC-TP-01 to SC-TP-07 in execution_state.json test_scenarios. Can run in parallel with ST-12.

---

##### ST-12 — Earnings Calendar and UK screener test registration (TEST-GAP-EPIC-03)

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** None
**Notes:** Source: TEST-GAP-EPIC-03 (v3.1 delivery verification). Verify `tests/e2e/earnings-calendar.spec.js` and `tests/e2e/screener-uk-suffix.spec.js` exist; register all scenarios in execution_state.json. Can run in parallel with ST-11.

---

#### EPIC-01 — Pre-Trade Research View (PT-02 + PT-03)

**Maps to:** S2-01, S2-02
**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** ~5–8 days (M–M–S–S)
**Risk IDs:** RISK-01 (resolved at design gate)
**Execution sequence:** 2 (start in parallel with EPIC-03; primary Sprint 1 user-value deliverable)

**Design artefacts locked:**
- `docs/design/2026-05-05__release-v3.2/pre-trade-research-view/ux_spec.md` v1.0 (ST-01, ST-02, ST-03)
- `docs/design/2026-05-05__release-v3.2/screener-to-research-navigation/ux_spec.md` v1.0 (ST-04 / BLG-FE-22)
- `docs/specs/frontend/pages/pre_trade_research.md` v0.1 (ST-01, ST-02, ST-03)
- `docs/specs/frontend/pages/screener_results.md` v1.1 (ST-04)
- `docs/specs/frontend/pages/watchlist.md` v0.2 (ST-04)

**Test scenario gap flag (LL-v2.0-P4-2):** EPIC-01 introduces a new page (`/research/{ticker}`) and new user-facing controls across four stories. QA & Testing Owner must author `test_scenarios` for this EPIC before next sprint on this domain. Recommended file: `tests/e2e/pre-trade-research.spec.js`.

##### ST-01 — Pre-trade research view component — data display

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** M (~2–3 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None (GET /research/{ticker} backend shipped v3.1)
**Notes:** New page at `/research/{ticker}`. Foundation for ST-02, ST-03, ST-04 — must complete first. Spec: `docs/specs/frontend/pages/pre_trade_research.md` v0.1.

---

##### ST-02 — Trade plan context panel in research view

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** ST-01 (must complete first)
**Notes:** Parallel with ST-03 and ST-04 after ST-01 complete. Spec: `pre_trade_research.md` v0.1 §7.

---

##### ST-03 — Prospective heat at entry metric integration (PT-03)

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** ST-01 (must complete first)
**Notes:** Parallel with ST-02 and ST-04 after ST-01 complete. GET /portfolio/prospective-heat backend shipped v2.0. Spec: `pre_trade_research.md` v0.1 §6.

---

##### ST-04 — Navigation integration — screener and watchlist entry points to research view

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** ST-01 (must complete first)
**Notes:** Parallel with ST-02 and ST-03 after ST-01 complete. BLG-FE-22 navigation model adopted — UX spec delivered at design gate. Spec: `screener_results.md` v1.1 §11; `watchlist.md` v0.2 Research Navigation section.

---

### Sprint 2

---

#### EPIC-02 — Pre-Trade Entry Checklist (PT-05)

**Maps to:** S2-03
**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** ~2–3 days (M–M)
**Risk IDs:** RISK-02
**Execution sequence:** 3 (Sprint 2; hard dependency on EPIC-01 merged to main)

**Sequencing constraint:** EPIC-01 PR must be merged to main before ST-05 begins. EPIC-02 may not start until EPIC-01 is merged.

**Design artefacts locked:**
- `docs/design/2026-05-05__release-v3.2/pre-trade-entry-checklist/ux_spec.md` v1.0 (ST-05, ST-06)
- `docs/specs/frontend/pages/trade_plan.md` v0.2 §6 (ST-05, ST-06)

**Test scenario gap flag (LL-v2.0-P4-2):** EPIC-02 introduces a new checklist component in the Trade Plan form. QA & Testing Owner must author `test_scenarios` for this EPIC before next sprint on this domain. Recommended file: `tests/e2e/entry-checklist.spec.js`.

##### ST-05 — Entry checklist schema, component, and Trade Plan form integration

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** EPIC-01 merged (hard dependency)
**Notes:** Schema definition + frontend component + Trade Plan form embedding + persistence via PUT /trade-plans/{id}. Spec: `trade_plan.md` v0.2 §6.

---

##### ST-06 — Checklist pre-population from trade plan data and research view link

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** M (~1 day)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** ST-05 (must complete first)
**Notes:** Pre-population from existing trade plan data fields. "Review research" link → `/research/{ticker}`. Spec: `trade_plan.md` v0.2 §6.2, §6.3.

---

#### EPIC-04 — Documentation, Security & Backlog Clearance

**Maps to:** S2-06
**Owner:** PMO Lead + Cybersecurity & Trust Lead
**Estimated effort:** ~3–5 days (M–M–S–S–M)
**Risk IDs:** None
**Execution sequence:** 4 (Sprint 2; independent of EPIC-02; can run in parallel)

##### ST-13 — React component inventory (BLG-FE-16)

**Owner:** PMO Lead
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None
**Notes:** Source: BLG-FE-16. Output: `docs/frontend/component_inventory.md`. Designated living reference — must be updated whenever a component is added/removed/significantly changed during Arc 2 development. ST-14 depends on this.

---

##### ST-14 — Design system document (BLG-FE-21)

**Owner:** PMO Lead
**Estimated effort:** M (~1 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** ST-13 (must complete first)
**Notes:** Source: BLG-FE-21. Output: `docs/frontend/design_system.md`. Cross-references ST-13 component inventory. Designated living reference.

---

##### ST-15 — Alpaca credential audit and rotation policy (BLG-SEC-05)

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None
**Notes:** Source: BLG-SEC-05. Output: `docs/operations/credential_policy.md`. Designated living reference — updating it is a required step whenever a credential is added, rotated, or retired. Can run in parallel with ST-13/14.

---

##### ST-16 — External API dependency risk register (BLG-GOV-18)

**Owner:** PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`
**Dependencies:** None
**Notes:** Source: BLG-GOV-18. Output: `docs/operations/external_api_risk_register.md`. Covers Alpaca, Yahoo Finance, Anthropic. Designated living reference. Can run in parallel with ST-13/14/15.

---

##### ST-17 — Cycle artefact inventory and maintenance review (BLG-GOV-11)

**Owner:** PMO Lead
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`
**Dependencies:** None
**Notes:** Source: BLG-GOV-11 (3rd consecutive deferral — mandatory this cycle). Output: consolidated artefact inventory + OPERATIONAL_GUIDE update. Can run in parallel with ST-13/14/15/16.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~10–12 days |
| Total estimated effort (in-scope) | ~12–19 days (midpoint ~15 days) |
| Utilisation at midpoint | ~136% |
| Over-allocation | Yes — accepted by PO (see sign-off block) |

**Phasing:** Sprint 1 (EPIC-03 + EPIC-01, ~7–11 days est.); Sprint 2 (EPIC-02 + EPIC-04, ~5–8 days est.)

---

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| None | — | All 17 items included; capacity WARN accepted by Product Owner with phasing as mitigation |

---

## Deferred Execution Blockers Accepted

*(Section omitted — deferred_execution_blockers was empty in state.json)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Product Owner capacity WARN acknowledgement | Product Owner | Yes — required in sign-off block below |
| OA-01 (v3.1): v3.1 scope document creation (retroactive) | PMO Lead | No — not in Pre-sprint Planning Required Decisions; prior cycle OA |
| QA & Testing Owner: author Playwright test scenario files for EPIC-01/02 before execution | QA & Testing Owner | No — advisory; see sprint_planning_notes.md test scenario gap flags |
| prompt_change_log.md entries: execution_prompt.md v3.12/v3.13, OPERATIONAL_GUIDE.md v3.65/v3.66 | Head of Specs Team | No — advisory; governance hygiene |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed (all 17 items):** Confirmed
**Capacity WARN acknowledged (over-allocation accepted with phasing as mitigation):** Accepted
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-05-06
