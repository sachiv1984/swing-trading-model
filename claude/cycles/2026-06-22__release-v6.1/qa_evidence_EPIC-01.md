---
**Owner:** Head of Specs Team; PMO Lead
**Class:** QA Evidence Log (Class 3)
**Status:** Signed Off
**EPIC:** EPIC-01 — Governance Prompt Correctness
**Cycle:** 2026-06-22__release-v6.1
**Branch:** exec/2026-06-22__release-v6.1/EPIC-01
**Commits:** cb0bb33f (ST-01/ST-02), 322a884d (ST-03)
**Date:** 2026-06-23
---

# QA Evidence Log — EPIC-01 (Governance Prompt Correctness)

## Stories in Scope

| Story | Title | Status |
|-------|-------|--------|
| ST-01 | Release planning: Design Gate Required flag | Done |
| ST-02 | Sprint planning: Design Gate hard gate at preflight | Done |
| ST-03 | Governance overhead ceiling metric and accountability mechanism | Done |

---

## ST-01 — Release planning: Design Gate Required flag

**Classification:** Autonomous — prompt file edit; no observable UI ACs.

### Acceptance Criteria Verification

| AC | Description | Evidence | Status |
|----|-------------|----------|--------|
| AC-01 | STEP 4 scans backlog slice for UI-facing scope and classifies design_gate_required = true/false | New STEP 4.1 added to release_planning_prompt.md: scans story classifications (delegated_frontend, autonomous with observable UI ACs) and sets design_gate_required | ✅ Pass |
| AC-02 | design_gate_required = true → advisory "⚠ DESIGN GATE REQUIRED" in output | STEP 4.1 output block includes advisory with cycle_id and `run design-gate` instruction | ✅ Pass |
| AC-03 | design_gate_required = false → output "Design Gate: Not Required" | STEP 4.1 else-branch outputs "Design Gate: Not Required — proceed directly to plan sprint" | ✅ Pass |
| AC-04 | cycle/state.json and .claude_current_state.json updated with design_gate_required at STEP 4 | STEP 4.1 includes explicit update instruction for both files at classification completion | ✅ Pass |
| AC-05 | cycle_summary.md header includes design_gate_required status line | STEP 7 of release_planning_prompt.md updated to include design_gate_required in header | ✅ Pass |
| AC-06 | release_planning_prompt.md version bumped; §14 OPERATIONAL_GUIDE.md and prompt_change_log.md updated in same commit | Version bumped v2.37→v2.38; prompt_change_log.md appended; OPERATIONAL_GUIDE.md §14 table updated. All in commit cb0bb33f | ✅ Pass |

**Playwright coverage:** No tests required — prompt file edit, no observable UI behaviour.

---

## ST-02 — Sprint planning: Design Gate hard gate at preflight

**Classification:** Autonomous — prompt file edit; no observable UI ACs.

### Acceptance Criteria Verification

| AC | Description | Evidence | Status |
|----|-------------|----------|--------|
| AC-01 | STEP -1.3 checks design_gate_status when design_gate_required = true; non-Passed with empty bypass fields → halt fires | STEP -1 check 3 added: conditional on `design_gate_required = true`; fires halt when `design_gate_status ≠ Passed` and bypass fields empty | ✅ Pass |
| AC-02 | Bypass path: both bypass fields populated → proceeds with bypass acknowledgement in sprint notes | Bypass branch documented: appends "[BYPASS APPLIED]" note to sprint_planning_notes.md before proceeding | ✅ Pass |
| AC-03 | Pass path: design_gate_status = Passed → logs "Design gate: Passed" and proceeds normally | Pass branch outputs "Design gate: Passed — proceeding to preflight" | ✅ Pass |
| AC-04 | design_gate_required = false → gate check skipped; noted "Design gate: Not Required for this cycle" | Else-branch at check 3: outputs "Design gate: Not Required for this cycle — skipping check" | ✅ Pass |
| AC-05 | sprint_planning_prompt.md version bumped; §14 OPERATIONAL_GUIDE.md and prompt_change_log.md updated in same commit | Version bumped v3.10→v3.11; prompt_change_log.md and OPERATIONAL_GUIDE.md updated. All in commit cb0bb33f | ✅ Pass |

**Playwright coverage:** No tests required — prompt file edit, no observable UI behaviour.

---

## ST-03 — Governance overhead ceiling metric and accountability mechanism

**Classification:** Autonomous — proposal document; no observable UI ACs. No prompt files modified (implementation deferred to Head of Specs Team sign-off).

### Acceptance Criteria Verification

| AC | Description | Evidence | Status |
|----|-------------|----------|--------|
| AC-01 | Governance overhead ceiling metric defined: G+D+P% over rolling 5-cycle window, alert threshold ≥ 60% | §2 of proposal defines the metric formula. §3 documents alert threshold ≥ 60% with rationale | ✅ Pass |
| AC-02 | Proposal document at `docs/product/decisions/gov_overhead_ceiling_proposal_v6.1.md` | File created at the specified path in commit 322a884d | ✅ Pass |
| AC-03 | Draft amendment to roadmap_prompt.md STEP 2 included in proposal | §6 of proposal contains draft STEP 2.4 amendment text (Governance Overhead Percentage addition). Not yet applied — requires HoST sign-off per CLAUDE.md §6 | ✅ Pass |
| AC-04 | Proposal includes prior 5-cycle G+D+P% data to establish baseline | §4 contains 5-cycle table (v5.5–v5.9): G+D+P%=86.0%. v6.0 context row also included | ✅ Pass |

**Playwright coverage:** No tests required — documentation-only story; no observable UI behaviour.

---

## Consolidation Sign-Off

```
DoQ Sign-Off — EPIC-01 (Governance Prompt Correctness)
Cycle: 2026-06-22__release-v6.1
Date: 2026-06-23

ST-01: release_planning_prompt.md patched with STEP 4.1 (design_gate_required flag).
All 6 ACs verified by inspection of committed claude/system/release_planning_prompt.md.
Governance edit checklist complete (v2.37→v2.38, prompt_change_log.md, OPERATIONAL_GUIDE.md).

ST-02: sprint_planning_prompt.md patched with STEP -1.3 design gate check.
All 5 ACs verified by inspection of committed claude/system/sprint_planning_prompt.md.
Governance edit checklist complete (v3.10→v3.11, prompt_change_log.md, OPERATIONAL_GUIDE.md).

ST-03: Proposal document delivered at docs/product/decisions/gov_overhead_ceiling_proposal_v6.1.md.
All 4 ACs verified. G+D+P% metric defined (§2), ≥60% threshold (§3), 5-cycle baseline data (§4,
G+D+P%=86.0%), draft STEP 2.4 amendment (§6). No prompt files modified — implementation deferred
pending HoST + PMO Lead review per CLAUDE.md §6.

All 3 stories: governance/documentation changes. No observable UI ACs. No Playwright coverage
required. EPIC-01 stories complete — ready for PR.

Signed: [x] Sprint Execution Engine (autonomous class) — 2026-06-23
```
