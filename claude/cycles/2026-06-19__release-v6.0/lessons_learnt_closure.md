Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-06-22
Cycle: 2026-06-19__release-v6.0

---

# Lessons Learnt — Post-Ship Closure — v6.0

Feature / Trigger: Signal Correctness, User Intelligence & SI-05 Effectiveness
Run: 2026-06-19__release-v6.0
Reviewed by: PMO Lead
Date filed: 2026-06-22
Prior cycle checked: 2026-06-17__release-v5.9

---

## What worked well

1. **Both v5.9 carry-forwards fully resolved** — BLG-FE-64 gate cleared (2026-06-21) and activated as ST-06/07 (EPIC-04 Cluster A); BLG-OPS-70 deep link AC-04 confirmed via ST-05. Both items that had been open at prior closure landed in v6.0 scope as intended.

2. **Velocity 1.00 — second consecutive clean sprint** — All 11 stories shipped, 2 P3 process deviations accepted under PO authority, zero stories returned. Verification status Verified_with_deviations is compliant; no P0/P1/P2 deviations.

3. **Stale Specs_Index entry caught and corrected at STEP 7** — TSG-v50-01 (BLG-FE-61) had been listed as "Open" in §27.1 since v5.0 despite being resolved in v5.1. Closure STEP 7 review detected and corrected this; §28 (TSG-v60-01 / BLG-QA-61) added cleanly.

4. **All planning documents found and superseded without friction** — scope document and decisions record both superseded cleanly with correct lifecycle headers; changelog entry and roadmap updates complete; 11 backlog completion markers applied correctly.

---

## Friction Log

### Friction Item 1

**Classification:**
- Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced

**Recurrence:** No

**What happened:**
STEP 6 endpoint coverage drift check found that `PATCH /trades/{trade_id}/costs` (added in v6.0 ST-03 as part of BLG-FEAT-20 net-of-costs) is present in `docs/reference/openapi.yaml` but absent from `docs/operations/api_performance_baseline.md`. BLG-OPS-73 filed as an advisory. The endpoint was added to the OpenAPI spec correctly (per CLAUDE.md non-negotiable) but the performance baseline update was not required or prompted anywhere in the delivery process.

**Where in the routine:**
STEP 6 — Endpoint coverage drift advisory check

**Root cause:**
Process gap — no CLAUDE.md non-negotiable or execution_prompt.md step requires updating `api_performance_baseline.md` when a new endpoint is added to `openapi.yaml`.

**Blast radius analysis:**
- What would have propagated: performance baseline remains incomplete, masking latency monitoring gap for the new endpoint
- When it would have surfaced: next time BLG-OPS-type backlog item references baseline coverage (or at next closure STEP 6 check)
- Recovery cost if uncaught: low (single file fix — add one row to api_performance_baseline.md) but accumulates if multiple endpoints are added across cycles

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `docs/CLAUDE.md` or `claude/system/execution_prompt.md`
  - Section: CLAUDE.md non-negotiables §2 (API endpoint rules) or execution_prompt.md STEP 3 API contract block
  - Change required: Add advisory: "When adding a new endpoint to `docs/reference/openapi.yaml`, also add a corresponding row to `docs/operations/api_performance_baseline.md` in the same commit."
  - Owner: Head of Specs Team
  - Target: v6.1 (before sprint planning seals)

---

### Friction Item 2

**Classification:**
- Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** Not checkable (v5.9 closure had no Specs_Index TSG reconciliation friction)

**What happened:**
STEP 7 Specs_Index review found §27.1 TSG-v50-01 (BLG-FE-61) still listed as "Open" when BLG-FE-61 had been resolved and marked COMPLETE in `backlog.md` during v5.1. The entry had remained stale for three cycles. The fix was applied during this closure STEP 7 (corrected to RESOLVED). The gap: when a TSG backlog item is marked COMPLETE in `backlog.md`, there is no companion step requiring the corresponding Specs_Index §27.x entry to be updated.

**Where in the routine:**
STEP 7 — Specs Index review

**Root cause:**
Process gap — `backlog.md` completion marking and `Specs_Index.md` TSG status are maintained independently with no enforced synchronisation trigger.

**Blast radius analysis:**
- What would have propagated: Specs_Index continues to misrepresent open technical gaps; downstream consumers (roadmap engine STEP 0 gap-check) may over-count open risks
- When it would have surfaced: next Specs_Index review at a future post-ship closure
- Recovery cost if uncaught: low (single entry update per stale row) but accumulates if multiple TSG entries are not reconciled across cycles

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 7 — Specs Index review
  - Change required: Add an explicit sub-step: "For each TSG entry in §27 marked as 'Open', cross-check against `backlog.md` — if the corresponding BLG item is marked COMPLETE, update the Specs_Index §27.x entry to RESOLVED."
  - Owner: PMO Lead
  - Target: v6.1 post-ship closure (next run of this routine)

---

## Consolidated Action Summary

**Records reviewed:**
- `claude/cycles/2026-06-19__release-v6.0/lessons_learnt.md` (Release Planning — 6 carry-forward items: LL-P1-01 through LL-P1-04, LL-P2-01, LL-P2-02)
- `claude/cycles/2026-06-19__release-v6.0/lessons_learnt_cycle.md` (Phase 3 — 4 items; Phase 4 — 3 items)

### Immediate actions applied: 0

None — no friction items from the three lessons_learnt records met the criteria for immediate patch during this closure run.

### Deferred to next cycle: 8

| # | Action | Owner | Target |
|---|--------|-------|--------|
| 1 | LL-P1-04: PT-04 (BLG-FEAT-25) closed trade count gate — 13 at v6.0 planning, projected ~2026-07-02. Check at v6.1 sprint planning; if ≥20 trades, PT-04 + SI-02 frontend eligible for conditional scope. | PMO Lead | v6.1 sprint planning |
| 2 | LL-P2-01: Correct Skill-Silo ceiling text in `claude/roadmap/current_roadmap.md` v6.0 Now section (60% → 40%) at roadmap management pass. | Roadmap Management Engine (STEP 11) | v6.1 (STEP 11 this closure) |
| 3 | LL-P2-02: Apply roadmap_prompt.md STEP 8.2 deferred patch (active-backlog verification advisory). | Roadmap Management Engine (STEP 11) | v6.1 (STEP 11 this closure) |
| 4 | Phase 3 — Playwright CI gap (BLG-QA-60): add morning-briefing.spec.js and screener-quality.spec.js to playwright.yml CI workflow; update spec inventory comment (24→25 registered spec files). Execution engine should verify playwright.yml registration in same commit as spec file for any EPIC introducing new Playwright tests. | Director of Quality; Head of Engineering | v6.1 |
| 5 | Phase 3 — Stash-at-branch-switch pattern (recurrence v5.3/v5.4/v5.5/v6.0): patch execution_prompt.md STEP 3.2.B or STEP 4 to commit all working-tree changes before STEP 4 halt output (backlog.md/qa_evidence changes left uncommitted at EPIC PR merge). | Head of Specs Team | v6.1 |
| 6 | Phase 3 — PO gate override pre-authorization: consider adding pre-authorization language to sprint_backlog.md conditional cluster sections so in-sprint gate overrides can be recorded at planning seal rather than requiring a separate escalation session during execution. | Product Owner; PMO Lead | v6.1 post-ship review |
| 7 | Phase 4 — SSR STEP 5.3A recurrence (ESCALATION): execution_prompt.md STEP 5.3A — add mandatory write+verify sub-step: "Confirm the v<cycle_id> section now exists in docs/System_status_report.md before proceeding." The existing LL-v5.9-P4-01 staging instruction (v3.45) is necessary but not sufficient — it cannot stage a write that did not happen. Escalated to Head of Specs Team. | Head of Specs Team | v6.1 |
| 8 | Phase 4 — Test scenario gap advisory: delivery_verification_prompt.md STEP -1.3 or STEP 2 — add advisory: "For stories replacing a core algorithm or model, cross-check that test_scenarios listed in execution_state.json were either run or explicitly declared superseded by new tests." | Head of Specs Team; Director of Quality | v6.1 |

### Monitor (no action required): 2

| # | Item |
|---|------|
| 1 | Phase 3 — Multi-cluster conditional EPIC design (Cluster A: 2026-06-21; Cluster B: 2026-07-04) worked well. PO gate overrides were efficient once raised; autonomous classification for decision stories eliminated delegation overhead. Continue pattern. |
| 2 | Phase 4 — Pre-established DoQ sign-offs at EPIC level eliminated re-coordination friction at verification time. Multi-authority sign-off chain for EPIC-04 delegated class well-documented. Continue pattern. |

### Escalated for decision: 0

Note: Item 7 (SSR STEP 5.3A) carries an escalation flag to Head of Specs Team but is classified as "deferred" not "decision_required" — the patch is known (write+verify sub-step); authority is clear. It is recorded as an escalation in the Escalations section below.

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| SSR STEP 5.3A (write not executed during sprint close) | v5.9 Phase 4 (LL-v5.9-P4-01 → patch applied v3.44→v3.45) | Immediate action applied at v5.9 closure: `git add` instruction added to STEP 5.3A. Patch applied but did not prevent v6.0 recurrence (root cause: write step was skipped, not staging step). | Head of Specs Team |

---

## Process improvements actioned this run

None applied this run.

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| — | — | No immediate patches applied | — | Not applicable |

---

## New files created this run

None from process improvements. (Closure artefacts `closure_record.md`, `lessons_learnt_closure.md` are routine outputs, not process improvement files.)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `docs/CLAUDE.md` or `claude/system/execution_prompt.md` | CLAUDE.md §2 API non-negotiables or execution_prompt.md STEP 3 API contract block | Add advisory: when adding endpoint to openapi.yaml, also update api_performance_baseline.md in same commit | Head of Specs Team | v6.1 |
| `claude/system/post_ship_closure.md` | STEP 7 — Specs Index review | Add sub-step: cross-check §27 Open TSG entries against backlog.md; update to RESOLVED where BLG item is COMPLETE | PMO Lead | v6.1 post-ship closure |
| `claude/system/execution_prompt.md` | STEP 5.3A | Add mandatory write+verify confirmation sub-step after SSR write (ESCALATION — Head of Specs Team) | Head of Specs Team | v6.1 |
| `claude/system/execution_prompt.md` | STEP 3.2.B or STEP 4 | Commit all uncommitted working-tree changes before STEP 4 halt output (stash-at-branch-switch prevention) | Head of Specs Team | v6.1 |
| `claude/system/delivery_verification_prompt.md` | STEP -1.3 or STEP 2 | Add advisory for core algorithm replacement stories: cross-check test_scenarios listed in execution_state.json | Head of Specs Team; Director of Quality | v6.1 |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| SSR STEP 5.3A — v3.45 write+verify gap | Recurrence | Head of Specs Team | Third cycle (v5.9, v6.0 confirmed recurrence) with applied v3.45 patch insufficient; prompt requires two-step change (write + mandatory existence confirmation) to prevent silent skip. |

---

## Recurrence Check

Prior cycle closure: `claude/cycles/2026-06-17__release-v5.9/lessons_learnt_closure.md`

**v5.9 carry-forwards (2 items) — status at v6.0 closure:**
- CL-v59-CF-1: BLG-FE-64 gate (2026-06-21) — **RESOLVED**. Gate cleared; BLG-FE-64 and BLG-FE-41 both executed as ST-06/ST-07 in EPIC-04 Cluster A.
- CL-v59-CF-2: BLG-OPS-70 deep link AC-04 — **RESOLVED**. Confirmed via ST-05 delivery verification.

**v5.9 deferred items (2 items) — status at v6.0 closure:**
- LL-RP-v59-02 (perennial-return advisory protocol): addressed structurally in v6.0 via existing STEP 1.4a and 1.4b rules; BLG-FE-64 was the trigger item and has now been resolved. No new escalation cycle expected.
- LL-RP-v59-03 (PT-04 gate projection ~2026-07-02): gate check performed at v6.0 sprint planning — 13 trades, gate not met. Carried forward as LL-P1-04 (see deferred item #1 above).

**No recurrence from the closure phase itself** — v5.9 closure friction (CL-v59-03 SSR immediate action) resolved by LL-v5.9-P4-01 patch; however the SSR pattern recurred at the execution level (not the closure level). The closure routine itself ran cleanly both cycles.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | PT-04 (BLG-FEAT-25) closed trade count was 13 at v6.0 sprint planning (~1.5/week), projecting gate clear ~2026-07-02. BLG-FE-52/53 (SI-02 frontend) gate is the same. | Re-check closed trade count at v6.1 sprint planning — if ≥20, PT-04 and SI-02 frontend are eligible for conditional scope. Include both as conditional items in v6.1 scope document with explicit gate date. | Release Planning |
| 2 | SSR STEP 5.3A write+verify escalation is pending Head of Specs Team response and prompt patch. The v3.45 patch (LL-v5.9-P4-01) does not prevent a skip of the write step itself. | v6.1 sprint planning should confirm execution_prompt.md STEP 5.3A write+verify patch has been applied (prompt_change_log entry expected) before accepting EPIC-xx execution. If patch not yet applied, flag at sprint planning as pre-execution blocker. | Sprint Planning |
| 3 | BLG-QA-60 (Playwright CI registration gap — morning-briefing.spec.js and screener-quality.spec.js not in playwright.yml) filed and deferred to v6.1. Both spec files exist but are not being run in CI. | Confirm BLG-QA-60 is included in v6.1 firm scope at release planning. Do not defer further — the gap means CI cannot catch Playwright regressions for 2 out of N spec files. | Release Planning |
