**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-17
**Cycle:** 2026-06-17__release-v5.8

---

# Sprint Planning Notes — v5.8

---

## Preflight Summary

| Gate | Result | Notes |
|------|--------|-------|
| Branch check | PASS | Current branch: `main` |
| Status check | PASS | `.claude_current_state.json` status = `Published` |
| Release plan sealed | PASS | `state.json` status = Published; `publish_eligible = true`; `open_escalations = []`; `deferred_execution_blockers = []` |
| Design gate | PASS (bypass) | `design_gate_status = not_required`; bypass authority: "Head of UX & Design + Product Owner" (IMP-30 compliant); bypass reason present |
| Backlog slice | PASS | 2 EPICs, 7 ST items; using `stage4_backlog_slice.md` (no amendment) |
| Role agents | PASS | All 5 required roles present |
| Write test | PASS | Created and deleted `.write_test` |
| lessons_learnt_prompt.md | PASS | Exists |
| pip-audit | CLEAN | No CVEs found |
| Prompt change log gaps | CLEAN | `post_ship_closure.md` v2.13 matches log (last entry: v2.12→v2.13, 2026-06-03); `roadmap_management_prompt.md` v1.4 matches log (last entry: v1.3→v1.4, 2026-05-09) — no gaps. Note: v5.7 sprint planning advisories OA-SP-01/02 were confirmed false positives (root cause: `tail` vs `head` usage, resolved in sprint_planning_prompt.md v3.10). |
| Before-sprint backlog items | NONE | No items with `Provisional-Target: Before v5.8 sprint planning` found |
| Amendment slice | N/A | `amended_backlog_slice_path` empty; using `stage4_backlog_slice.md` |

---

## Carry-Forward Items Reviewed

Carry-forward items reviewed: 2 items from cycle `2026-06-16__release-v5.7`.

| # | Item | Status at Sprint Planning |
|---|------|--------------------------|
| 1 | BLG-FE-64 firm inclusion at v5.8 (gate 2026-06-21 time-certain) | Actioned — included as firm ST-01 in release plan and sprint backlog |
| 2 | FRONTEND_URL production env var must be set before next SI-05 digest delivery | Actioned — included as firm ST-03 (P1 OA); sprint backlog firm story |

Both carry-forward items are resolved by their inclusion in the sprint backlog. No further action required.

---

## Load Summary (STEP 0)

- EPICs loaded: 2 (EPIC-01, EPIC-02)
- ST items loaded: 7 (4 firm Sprint 1, 3 conditional Sprint 2)
- Confirmed capacity: ~12–14 working days / sprint (solo developer)
- Backlog slice source: `stage4_backlog_slice.md` (original — no amendment)
- Deferred execution blockers: none
- Capacity check outcome: PASS
- Sprint goal proposed from cycle_summary.md themes (no explicit candidate in cycle_summary.md `## Carry-Forward Advisory`; goal derived from release context)

---

## Dependency Map

### Sprint 1 — EPIC-01

| Story | Depends on | Type |
|-------|------------|------|
| ST-01 | None | Independent |
| ST-02 | ST-01 | ST-01 pre-brief scopes the ST-02 review; ST-02 begins only after ST-01 brief is signed off |
| ST-03 | None | Independent (ops action on Render) |
| ST-04 | None | Independent (governance assessment) |

No circular dependencies. No external infrastructure blockers.

**Within-sprint date gates:**
- ST-01 and ST-02: gate 2026-06-21 (SI-03 live ≥30 days from 2026-05-22). Gate is time-certain — clears 4 days after sprint start. Sprint should begin ST-03 and ST-04 immediately; ST-01/ST-02 begin on or after 2026-06-21.
- ST-03: no date gate — execute immediately
- ST-04: no date gate — execute immediately (gate was pre-cleared: 0 open audit items)

### Sprint 2 — EPIC-02 (Conditional)

- All 3 stories (ST-05, ST-06, ST-07) are gated on 2026-07-04 (BLG-GOV-113 complete + ≥4 weeks SI-05 production operation)
- Gate check required at Sprint 2 opening: if BLG-GOV-113 not complete by 2026-07-04, return all 3 stories to backlog and close Sprint 2 as gate-deferred
- ST-05 and ST-06 are related (cadence review → actionability metrics; both benefit from same effectiveness review data) but have no strict dependency
- ST-07 is independent of ST-05/ST-06

---

## Execution Sequencing

### Sprint 1 Recommended Order

1. **ST-03** (FRONTEND_URL) — XS ops action; execute first to restore production deep links before next SI-05 digest delivery
2. **ST-04** (Governance complexity assessment) — M effort; independent; execute in parallel with ST-03; can proceed immediately
3. **ST-01** (RFJ design review pre-brief) — XS; execute on or after 2026-06-21 (gate); brief defines ST-02 scope
4. **ST-02** (RFJ visual design review) — M; begins after ST-01 brief is signed off

### Sprint 2 (if gate clears at 2026-07-04)

Execute ST-05, ST-06, ST-07 in any order — all are independent and gate-homogeneous.

---

## Scope Classification

| ST | Delegation Class | Justification |
|----|-----------------|---------------|
| ST-01 | `delegated_decision` | Head of UX & Design sign-off required on brief scope (AC-03); documentation deliverable |
| ST-02 | `delegated_decision` | Head of UX & Design sign-off required on design recommendation (AC-04); design review output |
| ST-03 | `delegated_backend` | Infrastructure & Operations Owner must perform Render dashboard action (AC-01, AC-03); env var change requires human Render access |
| ST-04 | `delegated_decision` | Multi-authority sign-off: Director of HR, PMO Lead, Head of Specs Team (AC-05); governance assessment |
| ST-05 | `delegated_decision` | Product Owner sign-off required (AC-04); conditional |
| ST-06 | `delegated_decision` | Metrics Definitions & Analytics Owner sign-off required (AC-02, AC-05); conditional |
| ST-07 | `delegated_backend` | Infrastructure & Operations Owner sign-off required (AC-04); conditional |

Note: ST-01/ST-02/ST-04 classified `delegated_decision` as these items require a specific human authority sign-off and the deliverable is a governance/design artefact that cannot be autonomously produced by the engine. ST-03 classified `delegated_backend` as Render dashboard access is a human-only action.

---

## Multi-EPIC Execution Notes

Sprint has 2 EPICs across 2 sprints (sequential, not parallel). EPIC-01 is the sole Sprint 1 EPIC and owns `execution_state.json`. EPIC-02 (Sprint 2, conditional) must check for `execution_state.json` existence before initialising and append its section rather than overwrite.

**Merge order:**
- Sprint 1: EPIC-01 (single PR)
- Sprint 2: EPIC-02 (single PR; conditional on 2026-07-04 gate)

No shared source files between EPIC-01 and EPIC-02 — EPICs are non-overlapping (UX/Ops/Gov vs SI-05 effectiveness).

---

## Staging-Only ACs

| ST | AC | Designation | Implication |
|----|----|-------------|-------------|
| ST-03 | AC-04 | `[staging-only evidence]` | "Deep links confirmed working in next SI-05 digest delivery post-deploy" — requires production SI-05 digest to fire post-FRONTEND_URL env var set. CI cannot verify. Evidence must come from Infrastructure & Operations Owner observing next scheduled digest delivery. |

Backlog obligation: If staging sign-off is deferred to post-merge (ST-03 AC-04), a backlog item must be filed before the PR opens (per CLAUDE.md §2). Execution Engine to file backlog item at ST-03 execution time if AC-04 sign-off cannot be obtained before PR opens.

---

## Deferred Items

| ST | Reason | Status in backlog |
|----|--------|------------------|
| ST-05 | Gate 2026-07-04 not yet met; conditional EPIC-02 deferred at planning | Remains in backlog; `status: deferred_at_planning` in execution_state.json |
| ST-06 | Gate 2026-07-04 not yet met; conditional EPIC-02 deferred at planning | Remains in backlog; `status: deferred_at_planning` in execution_state.json |
| ST-07 | Gate 2026-07-04 not yet met; conditional EPIC-02 deferred at planning | Remains in backlog; `status: deferred_at_planning` in execution_state.json |

---

## Risk Register Review

| RISK-ID | Status at Sprint Planning |
|---------|--------------------------|
| RISK-01 | Mitigation valid: ST-01 pre-brief explicitly caps ST-02 scope; Head of UX & Design owns scope boundary. No escalation. |
| RISK-02 | Acknowledged: EPIC-02 conditional — 2026-07-04 gate must be confirmed at Sprint 2 opening. If not confirmed, return all 3 stories to backlog. No materialisation observed. |

---

## Outstanding Actions

None. All `[AC REQUIRED]`, `[ESTIMATE REQUIRED]`, and pre-sprint advisory items resolved. No `Blocker? Yes` OAs.
