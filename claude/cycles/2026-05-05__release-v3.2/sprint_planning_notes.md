**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-06
**Cycle:** 2026-05-05__release-v3.2

---

# Sprint Planning Notes — 2026-05-05__release-v3.2

---

## Backlog Slice Source

Original — `claude/cycles/2026-05-05__release-v3.2/stage4_backlog_slice.md`

No amendment file; `amended_backlog_slice_path` is empty in state.json.

---

## Carry-Forward Items Reviewed

Source: `claude/cycles/2026-04-29__release-v3.1/lessons_learnt_closure.md ## Carry-Forward`

3 carry-forward items from v3.1:

| # | Item | Disposition in v3.2 |
|---|------|---------------------|
| 1 | sprint_planning_prompt.md has no branch verification step | Actioned as ST-07 (EPIC-03) — in scope Sprint 1 |
| 2 | execution_prompt.md §3.1.A test_scenarios backfill advisory missing (recurrence v3.0+v3.1) | Actioned as ST-09 (EPIC-03) — in scope Sprint 1 |
| 3 | Playwright waitFor pattern adoption deferred from v3.0 (CF-03) — networkidle pattern remains | Actioned as ST-10 (EPIC-03) — in scope Sprint 1 |

All 3 carry-forward items actioned as sprint stories. Carry-forward: 0 items remaining.

---

## Pre-Sprint Required Decisions

Source: `cycle_summary.md ## Pre-sprint Planning Required Decisions`

| Decision | Resolution | Evidence |
|----------|-----------|---------|
| [RISK-01] BLG-FE-22 Screener morning routine UX spec — must be complete and navigation model adopted into ST-04 AC before sprint planning seals | ✅ RESOLVED — design gate delivered `docs/design/2026-05-05__release-v3.2/screener-to-research-navigation/ux_spec.md` v1.0; `screener_results.md` updated to v1.1; `watchlist.md` updated to v0.2; Product Owner approved 2026-05-05 | design_gate.md (2026-05-05); design_gate_status=Passed in state.json |

All required decisions resolved. Sprint seal not blocked by required decisions.

---

## Deferred Items

No items deferred. All 17 ST items included in sprint scope.

The capacity WARN (~15 days vs ~11 available) is mitigated by 2-sprint phasing and the low actual effort of EPIC-03 governance patches (30–60 min each) and EPIC-04 documentation tasks. Product Owner acceptance of over-allocation is recorded in sprint_backlog.md sign-off block.

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | No deferrals | — |

---

## Dependency Map

| Item | Depends On | Type | Resolution |
|------|-----------|------|------------|
| ST-02 | ST-01 | Internal (EPIC-01) | ST-01 must complete before ST-02 starts |
| ST-03 | ST-01 | Internal (EPIC-01) | ST-01 must complete; ST-02 and ST-03 can run in parallel |
| ST-04 | ST-01 | Internal (EPIC-01) | ST-01 must complete; ST-02, ST-03, ST-04 can run in parallel post ST-01 |
| ST-05 | EPIC-01 merged | Cross-EPIC | EPIC-01 PR must merge to main before ST-05 begins |
| ST-06 | ST-05 | Internal (EPIC-02) | ST-05 must complete before ST-06 starts |
| ST-14 | ST-13 | Internal (EPIC-04) | ST-13 must complete before ST-14 (design system references component inventory) |
| ST-08 | None | — | Can combine with ST-09/ST-10 in a single commit (execution_prompt.md stories) |
| ST-09 | None | — | Can combine with ST-08/ST-10 in a single commit |
| ST-10 | None | — | Can combine with ST-08/ST-09 in a single commit |

No circular dependencies detected.

**External dependencies:**
- GET /research/{ticker} — backend shipped v3.1 ✅
- GET /portfolio/prospective-heat — backend shipped v2.0 ✅
- GET /trade-plans (or filter by ticker) — backend shipped v3.1 ✅
- PUT /trade-plans/{id} — backend shipped v3.1 ✅

No external blockers.

---

## Execution Sequence

### Sprint 1

**Phase A — EPIC-03 (Governance & Process Hardening):** Start first; lightweight autonomous patches clear outstanding governance debt. ST-07 through ST-10 can be delivered in 1–2 commits. ST-11 and ST-12 (test registration) follow independently.

1. ST-07 — sprint_planning_prompt.md STEP 0 branch check (autonomous)
2. ST-08, ST-09, ST-10 — execution_prompt.md patches (autonomous; combine in single commit per CLAUDE.md governance non-negotiables — all 3 story IDs in commit message)
3. ST-11 — Trade Plan test scenario registration (delegated_qa)
4. ST-12 — Earnings Calendar + UK screener test registration (delegated_qa; parallel with ST-11)

**Phase B — EPIC-01 (Pre-Trade Research View):** Start in parallel with EPIC-03 Phase A. EPIC-01 is the primary Sprint 1 user-value deliverable.

5. ST-01 — Research view page component (delegated_frontend; first — ST-02/03/04 depend on this)
6. ST-02 — Trade plan context panel (delegated_frontend; parallel with ST-03/04 after ST-01 complete)
7. ST-03 — Prospective heat integration (delegated_frontend; parallel with ST-02/04 after ST-01 complete)
8. ST-04 — Navigation integration (delegated_frontend; parallel with ST-02/03 after ST-01 complete)

### Sprint 2 (after EPIC-01 merged to main)

**Phase C — EPIC-02 (Pre-Trade Entry Checklist):** Hard dependency on EPIC-01 merge.

9. ST-05 — Entry checklist schema, component, Trade Plan form integration (delegated_frontend)
10. ST-06 — Checklist pre-population and research view link (delegated_frontend; after ST-05)

**Phase D — EPIC-04 (Documentation, Security & Backlog Clearance):** Independent of EPIC-02; can run in parallel.

11. ST-13 — React component inventory (autonomous)
12. ST-14 — Design system document (autonomous; after ST-13)
13. ST-15 — Alpaca credential audit and rotation policy (autonomous; parallel with ST-13/14)
14. ST-16 — External API dependency risk register (autonomous; parallel with ST-13/14/15)
15. ST-17 — Cycle artefact inventory (autonomous; parallel with ST-13/14/15/16)

---

## Risk Flags

| Risk ID | Associated Item | Description | Mitigation Status |
|---------|----------------|-------------|-------------------|
| RISK-01 | EPIC-01 (ST-04) | BLG-FE-22 UX spec not complete before sprint planning seal | ✅ Resolved — design gate delivered screener-to-research navigation UX spec; ST-04 AC already incorporates navigation model |
| RISK-02 | EPIC-02 | PT-05 depends on PT-02 merge | ✅ Valid — Sprint 2 sequencing enforces EPIC-01 merge before EPIC-02 begins; recorded as hard dependency in dependency map |
| RISK-03 | EPIC-03 | 4 governance prompt patches in same sprint — §6 checklist coordination overhead | ✅ Valid — mitigated by combining ST-08/ST-09/ST-10 in single commit (all 3 IDs in commit message per CLAUDE.md governance non-negotiables); each story confirms §6 checklist in QA evidence log |

---

## Pre-Sprint Vulnerability Scan

Result: **CLEAN** — pip-audit executed against `backend/requirements.txt` on 2026-05-06. No known vulnerabilities found across all 68 dependencies. No high/critical CVEs. Pre-sprint pip-audit: clean.

---

## Test Scenario Gap Flags (LL-v2.0-P4-2)

The following stories introduce new pages or new user-facing controls and are classified `delegated_frontend`. Per planning obligation, the EPIC's `test_scenarios` field in `execution_state.json` should be flagged as pending for QA & Testing Owner to author before next sprint on this domain.

| Story | Classification | Flag |
|-------|---------------|------|
| ST-01 | delegated_frontend — new page `/research/{ticker}` | test_scenarios pending — QA & Testing Owner to author before next sprint on this domain |
| ST-02 | delegated_frontend — new Trade Plan context panel (new controls in research view) | test_scenarios pending — QA & Testing Owner to author before next sprint on this domain |
| ST-03 | delegated_frontend — new prospective heat display widget | test_scenarios pending — QA & Testing Owner to author before next sprint on this domain |
| ST-04 | delegated_frontend — new Research links on screener and watchlist pages | test_scenarios pending — QA & Testing Owner to author before next sprint on this domain |
| ST-05 | delegated_frontend — new checklist component in Trade Plan form | test_scenarios pending — QA & Testing Owner to author before next sprint on this domain |
| ST-06 | delegated_frontend — new pre-population logic and research view link in checklist | test_scenarios pending — QA & Testing Owner to author before next sprint on this domain |

These flags are recorded at planning time. QA & Testing Owner should prepare test scenario files (e.g., `tests/e2e/pre-trade-research.spec.js`, `tests/e2e/entry-checklist.spec.js`) before sprint execution begins on EPIC-01 and EPIC-02 to allow Playwright coverage alongside or immediately after story delivery.

---

## Prompt Change Log Hygiene Advisory (-1.11)

The following gaps were detected between current prompt version headers and the last entries in `claude/system/prompt_change_log.md`:

| Prompt | Current Version | Last Logged Version | Gap |
|--------|----------------|--------------------|----|
| `execution_prompt.md` | v3.13 | v3.11 (2026-04-25) | 2 versions (v3.12, v3.13) not logged |
| `OPERATIONAL_GUIDE.md` | v3.66 | v3.64 (2026-04-25) | 2 versions (v3.65, v3.66) not logged |

Advisory only — does not block sprint planning. These entries should be prepended to `claude/system/prompt_change_log.md` (immediately after the header row) by the Head of Specs Team before sprint execution commits that touch these files.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? | Notes |
|--------|-------|----------------------|-------|
| OA-01 (from v3.1): v3.1 scope document creation (retroactive) | PMO Lead | No — not in Pre-sprint Planning Required Decisions | Open since v3.1 post-ship closure; PMO Lead to create or confirm not required for closed cycle |
| Product Owner capacity WARN acknowledgement | Product Owner | Yes — required before sprint seal | ⚠ Capacity check outcome = WARN; PO must explicitly accept over-allocation in sprint_backlog.md sign-off block |
| QA & Testing Owner: author Playwright test scenario files before EPIC-01/02 execution | QA & Testing Owner | No — advisory | Staging coverage: tests/e2e/pre-trade-research.spec.js, tests/e2e/entry-checklist.spec.js |
| prompt_change_log.md entries for execution_prompt.md v3.12/3.13 and OPERATIONAL_GUIDE.md v3.65/3.66 | Head of Specs Team | No — advisory | Log entries should be prepended per §6 checklist; tracked as prompt hygiene gap |
