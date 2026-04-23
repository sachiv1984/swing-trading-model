Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-04-23
Cycle: 2026-04-22__release-v2.9

---

# Sprint Planning Notes — 2026-04-22__release-v2.9

## Backlog Slice Source

Original — `claude/cycles/2026-04-22__release-v2.9/stage4_backlog_slice.md`

No `amended_backlog_slice_path` set. Stage 4 slice is authoritative.

## Carry-Forward Items Reviewed

2 items from cycle `2026-04-17__release-v2.8` (lessons_learnt_closure.md):

| # | Carry-Forward Item | Resolution in v2.9 |
|---|-------------------|--------------------|
| 1 | Frontend reclassification (delegated_frontend→autonomous) requires Director of Quality counter-sign when frontend changes are present | Addressed by ST-11 (BLG-GOV-14) §3.2.A patch |
| 2 | Domain-gated EPICs need DoQ EPIC-level consolidation block in qa_evidence in addition to domain authority sign-off | Addressed by ST-11 (BLG-GOV-14) §3.2 patch |

## Preflight Results

| Check | Result | Notes |
|-------|--------|-------|
| -1.1 Global state | PASS | status=Published, no amended slice |
| -1.2 Release plan sealed | PASS | status=Published, publish_eligible=true, no open escalations |
| -1.3 Design gate bypass | NOTE | design_gate_status=not_started; bypass confirmed: Head of UX & Design + Product Owner (no frontend UI deliveries in v2.9; DS-02 deferred; ST-04 is doc authoring; ST-13 is one-line utility fix). Fields written to .claude_current_state.json |
| -1.4 Backlog slice present | PASS | 4 EPICs, 15 ST items |
| -1.5 Required files | PASS | stage4_5_capacity_check.md absent — schema v2 cycle; capacity embedded in release_plan.md § Capacity Check (compliant) |
| -1.6 Authority roles | PASS | All 5 required roles present in claude/agents/ |
| -1.7 lessons_learnt_prompt | PASS | Present |
| -1.8 Write permission | PASS | .write_test created and removed |
| -1.9 pip-audit | CLEAN | 0 vulnerabilities across all 55 dependencies |
| -1.10 Pre-sprint decisions | NOTE | RISK-01 is a Sprint 2 kickoff sequencing gate, not a planning seal gate — recorded below |
| -1.11 Prompt change log hygiene | PASS | No gaps detected. OA-v29-01 was false advisory — sprint_planning_prompt.md log entries confirmed complete (v2.3→v2.4 on 2026-03-24, v2.4→v2.5 on 2026-04-05). execution_prompt.md v3.6→v3.7 and v3.7→v3.8 entries confirmed present. |

## Pre-Sprint Vulnerability Scan

**Result: CLEAN** — pip-audit found 0 known vulnerabilities in `backend/requirements.txt` (55 packages scanned: fastapi, sqlalchemy, anthropic, httpx, pydantic, uvicorn, psycopg2-binary, requests, and all transitive dependencies). Pre-sprint scan: clean as of 2026-04-23.

## Deferred Items

No stories deferred from the backlog slice. All 15 ST items are within capacity and proceeding into the sprint backlog.

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| — | — | — | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-06 (DS-05) | ST-02 (BLG-SPEC-22) | Internal — spec before implementation | Sequential: ST-02 Sprint 1, ST-06 Sprint 2 |
| ST-07 (DS-06) | ST-08 (BLG-GOV-16) | Internal — §13 gate before implementation | Sequential: ST-08 Sprint 1, ST-07 Sprint 2 |
| ST-07 (DS-06) | ST-02 (BLG-SPEC-22) | Internal — API contract before implementation | Sequential: ST-02 Sprint 1, ST-07 Sprint 2 |
| ST-12 (BLG-GOV-15) | ST-11 (BLG-GOV-14) | Internal — version bump must be in sequence | ST-11 first (same sprint); ST-12 bumps from ST-11 base |
| ST-10 (BLG-QA-09) | ST-09 (BLG-QA-08) | Design dependency — harness format drives library format | Same sprint; ST-09 should be authored before ST-10 |

No circular dependencies detected.

## Execution Sequence

### Sprint 1

1. **EPIC-03 — ST-08** (BLG-GOV-16): §13 review for DS-06 — unblocks ST-07 in Sprint 2
2. **EPIC-01 — ST-01** (BLG-SPEC-21): Screener results schema spec
3. **EPIC-01 — ST-02** (BLG-SPEC-22): Alpaca API integration contract — unblocks ST-06/ST-07 in Sprint 2
4. **EPIC-01 — ST-03** (BLG-SPEC-23): Screener internal API contract
5. **EPIC-01 — ST-04** (BLG-FE-17): Screener results page UX spec
6. **EPIC-03 — ST-09** (BLG-QA-08): External API mock harness for CI
7. **EPIC-03 — ST-10** (BLG-QA-09): Screener test data library (after ST-09 harness format confirmed)
8. **EPIC-04 — ST-11** (BLG-GOV-14): execution_prompt.md §3.2 governance patches
9. **EPIC-04 — ST-12** (BLG-GOV-15): execution_prompt.md STEP 5.1.B advisory (after ST-11 bump)
10. **EPIC-04 — ST-13** (BLG-FE-15): SystemStatus.js /ai prefix fix

### Sprint 2

*(Requires Sprint 1 complete for EPIC-01/EPIC-03 prerequisites)*

1. **EPIC-02 — ST-05** (DS-03): Sector & Industry Classification
2. **EPIC-02 — ST-06** (DS-05): Alpaca US Market Data Integration (requires ST-02 ✅)
3. **EPIC-02 — ST-07** (DS-06): Alpaca News Panel (requires ST-08 ✅ and ST-02 ✅)
4. **EPIC-04 — ST-14** (BLG-AI-01): AI Journal summary audit log
5. **EPIC-04 — ST-15** (TEST-GAP-EPIC-04): AI Journal test scenario coverage

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 ST-02, EPIC-02 ST-06 | Valid — ST-02 (Sprint 1) gates ST-06 (Sprint 2); execution sequence enforces this |
| RISK-02 | EPIC-03 ST-08, EPIC-02 ST-07 | Valid — ST-08 (Sprint 1) gates ST-07 (Sprint 2); execution sequence enforces this |
| RISK-03 | EPIC-02 ST-06 | Valid — BLG-SPEC-22 pins API version; ST-06 ACs reference contract |
| RISK-04 | EPIC-03 ST-09 | Valid — scope limited to request/response mocking; auth flow deferred to v3.0 |

## Pre-Sprint Required Decision — RISK-01 (Sprint 2 Gate)

**Decision:** Confirm ST-02 (BLG-SPEC-22 Alpaca API contract) is complete and signed off before Sprint 2 execution of ST-06 (DS-05) begins.

This is a Sprint 2 **kickoff gate**, not a sprint planning seal gate. The sprint plan is sealed with this gate captured as an execution dependency. The Execution Engine must verify ST-02 is `done` in execution_state.json before commencing ST-06.

**Unblock criteria:** ST-02 execution_state.json status = `done` with DoQ sign-off dated.

## Governance Hygiene Notes

- **OA-v29-01 (false advisory):** sprint_planning_prompt.md change log IS complete — v2.3→v2.4 entry dated 2026-03-24, v2.4→v2.5 entry dated 2026-04-05. No gap exists. Advisory from release planning run_manifest.md was a false positive from top-first scan. No action required.
- **Design gate bypass:** Head of UX & Design + Product Owner have confirmed design gate is not applicable for v2.9 sprint (no frontend UI implementations; DS-02 deferred; ST-04 is document authoring; ST-13 is a utility function patch). Both authority fields written to `.claude_current_state.json`.

## Outstanding Actions

| Action | Owner | Blocker? |
|--------|-------|---------|
| Verify ST-02 complete before Sprint 2 ST-06 kickoff (RISK-01) | Head of Specs Team + Backend Engineering Owner | Yes (Sprint 2 kickoff only — not sprint seal) |
| OA-v29-02: Retire BLG-GOV-08 at next `groom backlog` run | Product Owner | No |
