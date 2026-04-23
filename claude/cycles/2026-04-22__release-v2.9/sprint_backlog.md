# Sprint Backlog — 2026-04-22__release-v2.9

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-04-23
**Cycle:** 2026-04-22__release-v2.9
**Release:** v2.9
**Sprint Goal:** Deliver the complete Arc 1 specification and governance foundation in Sprint 1 (screener specs, §13 review, CI mock harness, and governance debt patches), then implement DS-03 sector enrichment, DS-05 Alpaca data integration, DS-06 news panel, and AI governance debt items in Sprint 2 — completing all prerequisites for the v3.0 screener engine.
**Backlog Slice Source:** original stage4_backlog_slice.md

---

## Sprint Scope

---

### Sprint 1

---

#### EPIC-03 — Arc 1 Governance & QA Foundation *(Sprint 1 lead-off — §13 gate)*

**Maps to:** S2-08, S2-09, S2-10
**Owner:** Strategy Rules & System Intent Owner + Director of Quality
**Estimated effort:** ~4.5 days (1× S, 2× M)
**Risk IDs:** RISK-04
**Execution sequence:** 1 (§13 review first; unblocks ST-07 in Sprint 2)

##### ST-08 — §13 review record for DS-06 (BLG-GOV-16)

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None
**Notes:** Hard gate for ST-07 (DS-06). Must be complete and signed off before Sprint 2 begins ST-07.

---

##### ST-09 — External API mock harness for CI (BLG-QA-08)

**Owner:** Director of Quality + QA & Testing Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None (independent of specs)
**Notes:** RISK-04 — scope to request/response mocking only; no auth flow required.

---

##### ST-10 — Screener test data library (BLG-QA-09)

**Owner:** QA & Testing Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** ST-09 (harness format should be confirmed before authoring test data library to ensure compatibility)
**Notes:** Author after ST-09 harness format is defined.

---

#### EPIC-01 — Arc 1 Specification Foundation *(Sprint 1)*

**Maps to:** S2-04, S2-05, S2-06, S2-07
**Owner:** Head of Specs Team + Frontend Specifications & UX Documentation Owner
**Estimated effort:** ~4 days (3× S, 1× M)
**Risk IDs:** RISK-01
**Execution sequence:** 2 (specs before implementation EPICs)

##### ST-01 — Screener results schema spec (BLG-SPEC-21)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None
**Notes:** Creates `docs/specs/screener_results_schema.md`. Adds entry to `docs/specs/Specs_Index.md`.

---

##### ST-02 — Alpaca API integration contract (BLG-SPEC-22)

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** None (leads ST-06 and ST-07 in Sprint 2)
**Notes:** RISK-01 gate item. Creates `docs/specs/api_contracts/alpaca_integration_contract.md`. OpenAPI entries required in same commit (CLAUDE.md §1). ST-06 (Sprint 2) may not start until this is done.

---

##### ST-03 — Screener internal API contract (BLG-SPEC-23)

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** None
**Notes:** Creates `docs/specs/api_contracts/screener_api_contract.md`. OpenAPI entries required in same commit (CLAUDE.md §1). Endpoints must be at `##` level per CLAUDE.md §1.

---

##### ST-04 — Screener results page UX spec (BLG-FE-17)

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** None (informational dependency on ST-01 and ST-03 for field names, but not a blocking gate)
**Notes:** Creates UX spec document; does not implement any UI. DS-02 implementation deferred to v3.0.

---

#### EPIC-04 — Governance Debt & Quick Wins *(Sprint 1 items: ST-11, ST-12, ST-13)*

**Maps to:** S2-11, S2-12, S2-13 (Sprint 1) + S2-14, S2-15 (Sprint 2)
**Owner:** Head of Specs Team + Backend Engineering Patterns Owner
**Sprint 1 estimated effort:** ~1.5 days (3× S)
**Risk IDs:** None
**Execution sequence:** 3 (governance patches can run parallel to specs; ST-12 must follow ST-11)

##### ST-11 — execution_prompt.md §3.2 governance patches (BLG-GOV-14)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** None
**Notes:** Applies CF-1 and CF-2 from v2.8 closure. CLAUDE.md §6 checklist mandatory: version bump (v3.8→v3.9), OPERATIONAL_GUIDE.md §14 updated, phase header updated, prompt_change_log.md entry appended. Head of Specs Team sign-off.

---

##### ST-12 — execution_prompt.md STEP 5.1.B advisory (BLG-GOV-15)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** ST-11 (must follow ST-11; version bump base is ST-11's post-bump version)
**Notes:** CLAUDE.md §6 checklist mandatory. If same commit as ST-11, version bumps are cumulative (v3.8→v3.9→v3.10 or equivalent). Head of Specs Team sign-off.

---

##### ST-13 — SystemStatus.js /ai prefix fix (BLG-FE-15)

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None
**Notes:** Single case addition to `categorizeEndpoint()`. Verification by code review only (no UX behaviour change). DoQ verification method must be stated as "code review" in sign-off block.

---

### Sprint 2

*(Sprint 2 may not commence ST-06 or ST-07 until Sprint 1 ST-02 and ST-08 are confirmed done in execution_state.json — see RISK-01 Sprint 2 gate)*

---

#### EPIC-02 — Arc 1 Implementation Start *(Sprint 2)*

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** ~4 days (2× S, 1× M)
**Risk IDs:** RISK-01, RISK-02, RISK-03
**Execution sequence:** 4 (requires Sprint 1 EPIC-01/03 complete)

##### ST-05 — Sector & Industry Classification (DS-03)

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** None (independent of Alpaca contract)
**Notes:** Yahoo Finance enrichment only. UK and US tickers both in scope. Data model change requires migration script if schema change needed.

---

##### ST-06 — Alpaca US Market Data Integration (DS-05)

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** ST-02 (BLG-SPEC-22 — hard gate; must be `done` in execution_state.json before this story begins)
**Notes:** RISK-01 gate. US tickers only; UK tickers continue using Yahoo Finance. API version must be pinned per BLG-SPEC-22 contract. Fallback strategy per contract required.

---

##### ST-07 — Alpaca News Panel (DS-06)

**Owner:** Backend Engineering Patterns Owner + Frontend Specifications & UX Documentation Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** ST-08 (BLG-GOV-16 — hard gate); ST-02 (BLG-SPEC-22 — API contract)
**Notes:** RISK-02 gate. Display-only per BLG-GOV-16 sign-off conditions — no sentiment scoring, no automated advisory. Panel surfaces on watchlist in v2.9; screener results integration deferred until DS-02 ships in v3.0.

---

#### EPIC-04 — Governance Debt & Quick Wins *(Sprint 2 items: ST-14, ST-15)*

**Estimated effort:** ~1.5 days (2× S)
**Execution sequence:** 5

##### ST-14 — AI Journal summary audit log (BLG-AI-01)

**Owner:** AI Compliance & Governance Officer + Backend Engineering Patterns Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None
**Notes:** Persistent DB table (not application logs). Must integrate with existing `POST /api/ai/journal-summary` endpoint. Output hash, model version, trade_ids, timestamp all required. DoQ sign-off.

---

##### ST-15 — AI Journal test scenario coverage (TEST-GAP-EPIC-04)

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None (scenarios reference existing canonical specs)
**Notes:** Creates `docs/testing/ai_scenarios.md`. References `docs/specs/api_contracts/ai_endpoints.md` and `trade_history.md v1.7` as canonical specs. DoQ sign-off.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~14.25 days (velocity-based; v2.8=1.00, rolling avg=0.99) |
| Total estimated effort (in-scope) | ~14.25 days |
| Utilisation | ~100% |
| Over-allocation | No |

## Items Deferred This Sprint

None. All 15 items from stage4_backlog_slice.md are in scope.

## Deferred Execution Blockers Accepted

*(No deferred_execution_blockers in release plan state.json — section not applicable)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Verify ST-02 (BLG-SPEC-22) done before Sprint 2 ST-06/ST-07 kickoff (RISK-01 + RISK-02 gate) | Head of Specs Team + Backend Engineering Owner | Yes (Sprint 2 kickoff gate — not a seal gate) |
| OA-v29-02: Retire BLG-GOV-08 at next `groom backlog` | Product Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed — all 15 stories within capacity; sequencing enforced by execution order
**Capacity confirmed:** Confirmed — PASS (14.25 days; within v2.6/v2.3 demonstrated range)
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-04-23
