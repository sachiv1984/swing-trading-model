Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-06 (created)
Cycle: 2026-11-03__release-v9.15

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v9.15 — Site Structure & Usability, Phase 1
Run: 2026-11-03__release-v9.15
Reviewed by: PMO Lead
Date filed: 2026-11-06
Prior cycle checked: 2026-10-29__release-v9.14

**Prior-cycle closure items checked (`2026-10-29__release-v9.14` `lessons_learnt_closure.md`):**
- Outstanding deferred patch 1, `BLG-GOV-404` (gate scan, roadmap feature IDs): **Applied** in v9.15 ST-37 (EPIC-07).
- Outstanding deferred patch 2, `BLG-QA-240` (`merge_gate` check, uninitialised EPICs): **Applied** in v9.15 ST-38 (EPIC-07). It worked live for EPIC-07 and EPIC-05.
- Outstanding deferred patch 3 (observation: rebalance before `plan release v9.15`): **Done**. `run roadmap` ran as `2026-11-03__scheduled`.
- Carry-Forward 1 (rebalance and link `governance_overhead_audit_2026-11-02.md`): the rebalance ran, but the audit was not linked as an input (no reference under `claude/cycles/2026-11-03__scheduled/` or `claude/roadmap/`). **Carried** (Carry-Forward 3 below).
- Carry-Forward 2 (weigh `BLG-FE-239`/`240`/`243`): all three were seated (ST-15, ST-16, ST-04). **Closed.**
- Carry-Forward 3 (`ESC-CLOSE-20261103-02`): resolved 2026-11-03, and `BLG-GOV-404` was seated. **Closed.**
- Carry-Forward 4 (post-merge remainders): `BLG-GOV-400` met (Release Planning Friction Item 4; banner at `groom backlog`). `BLG-OPS-201` (after 2026-12-01) and `BLG-GOV-399` (production read) are still open. **Partly carried** (Carry-Forward 2 below).

---

## What worked well

- STEP 3 banner pass by mechanical mapping: each ST's `**Source:**` in `stage4_backlog_slice.md` was matched to its `### BLG-` heading, and the banner carried the PR and commit from `execution_state.json`. All 41 shipped items were found in `backlog.md` on the first pass, and `check_backlog_item_integrity.py` passed after each write.
- A STEP 8 immediate patch applied in the same run. `post_ship_closure.md` v2.45 STEP 3.1 (planning-deferred item already met or superseded gets a banner) was applied live to `BLG-FE-240` (ST-16, superseded by ST-12). That also resolved TSG-v9.14-03, which would otherwise have stayed Open for another cycle.
- The STEP 5 `strategy_rules.md` owner route (`ESC-CLOSE-20261029-02` option (b)) gave a clear path for `BLG-FE-271`'s conditional divergence. The escalation carries proposed text, so no ruling was needed on whether this routine may write the file.
- All six phase friction items with an unambiguous fix were applied same-cycle (the v2.32 same-cycle application pattern). Four prompts were bumped under one CLAUDE.md §6 checklist pass, and the governance-drift check was clean afterwards (28 tracked files, OPERATIONAL_GUIDE.md self-consistent at 4.253).

---

## Friction Log

### Friction Item 1

**Classification:**
- Type B — Semantic Mismatch: The same concept was named or interpreted differently across documents or roles

**Recurrence:** No

**What happened:**
At STEP 3.1, ST-24 (`BLG-AI-23`, neither AC met) and ST-29 (`BLG-OPS-48`, AC 1 and AC 2 not met) both had a partial outcome. Every unmet AC had already been moved to dedicated follow-up items filed this cycle: `BLG-AI-27`, and `BLG-OPS-214`/`BLG-OPS-213`/`BLG-SPEC-223`. The split-achievability carve-out was written for remainders tracked only by an escalation (`BLG-GOV-264`, `BLG-GOV-178`). It does not say what to do here, so both source items were left open under its literal wording. Each unmet AC is now tracked by two open items. Pass_with_deviation stories whose remainders also moved to follow-up items (ST-20 → `BLG-BE-203`, ST-42 → `BLG-QA-250`) were bannered, as in the v9.14 precedent (ST-01 → `BLG-OPS-204`). The difference between those two groups is degree, not kind.

**Where in the routine:**
STEP 3.1 — split-achievability carve-out (LL-v8.9-P-Closure-01)

**Root cause:**
process gap / naming inconsistency

**Blast radius analysis:**
- What would have propagated: the next Release Planning ready pool would hold `BLG-AI-23` beside `BLG-AI-27`, and `BLG-OPS-48` beside `BLG-OPS-214`. Either pair could be seated together, double-counting effort.
- When it would have surfaced: the next `plan release` or `groom backlog`
- Recovery cost if uncaught: low (single file fix)

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 3.1, split-achievability carve-out
  - Change required: distinguish a remainder tracked only by an escalation or by the source item (keep open) from one whose every unmet AC is moved to named follow-up backlog items filed this cycle (banner the source item and name the follow-ups).
  - Owner: Head of Specs Team; PMO Lead
  - Target: v9.16 sprint — `BLG-GOV-413`. This is deferred, not immediate, because which side the carve-out should default to is a design choice. `BLG-GOV-178` was kept open deliberately.

---

## Lessons learnt consolidated action summary (STEP 8)

Records reviewed: Release Planning `lessons_learnt.md` (4 friction items); `lessons_learnt_cycle.md` Phase 3 (2 friction items, 3 Carry-Forward rows) and Phase 4 (2 friction items); this closure's own finding (1).

| Item | Source | Disposition | Action |
|------|--------|-------------|--------|
| `LL-v9.15-Release-01` — §1.4c P2-first cuts across programme phasing | Release Planning FI-1 | decision_required | `ESC-CLOSE-20261106-02`, Head of Specs Team with the Product Owner, SLA 2026-11-09T16:18:41Z |
| `LL-v9.15-Release-02` — already-met planning deferral never bannered | Release Planning FI-2 (first recommendation) | immediate | `post_ship_closure.md` v2.44→v2.45 STEP 3.1; applied live to `BLG-FE-240` |
| `LL-v9.15-Release-02b` — 10 legacy `BLG-GOV-192`–`201` items with no ACs | Release Planning FI-2 (second recommendation) | deferred | Grooming, not a prompt change. PMO Lead at the next `groom backlog` that may write ACs, or the item owners. `BLG-GOV-193`–`196` shipped this cycle (ST-43/44/45, ST-28 for 194), so 6 remain: `BLG-GOV-192`, `197`–`201` |
| `LL-v9.15-Release-03` — calibration check reads Scope only | Release Planning FI-3 | immediate | `release_planning_prompt.md` v2.70→v2.71 STEP 4 |
| `LL-v9.15-Release-04` — `BLG-GOV-400` met with no close path | Release Planning FI-4 (observation) | deferred | STEP 12 of this routine (`groom backlog`) |
| `LL-v9.15-P3-01` — same-branch fixed items not bannered | Phase 3 FI-1 | immediate | `execution_prompt.md` v3.92→v3.93 §3.2.A and §7. This cycle's three items (`BLG-BE-204`, `BLG-FE-273`, `BLG-QA-251`) were bannered at STEP 3 |
| `LL-v9.15-P3-02` — in-flight return note timing | Phase 3 FI-2 | immediate | `execution_prompt.md` v3.93 STEP 5.2 |
| `LL-v9.15-P4-01` — verification STEP 1 does not name `deferred_at_planning` | Phase 4 FI-1 | immediate | `delivery_verification_prompt.md` v3.16→v3.17 STEP 1 |
| `LL-v9.15-P4-02` — P1/P2 found defect without PO + DoQ acceptance record | Phase 4 FI-2 | immediate | `execution_prompt.md` v3.93 STEP 5.1 |
| `LL-v9.15-Closure-01` — carve-out vs moved remainders | Closure FI-1 | deferred | `BLG-GOV-413`, v9.16 |

Totals: **6 immediate**, **3 deferred**, **1 escalated**.

---

## Recurrence Escalations

None. The prior closure's two deferred script patches shipped this cycle (ST-37, ST-38). No deferred patch has been carried 2+ cycles without a `prompt_change_log.md` entry.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | §3.2.A, §7 | Same-branch fix banner for items filed and fully fixed on the EPIC branch (LL-v9.15-P3-01) | 3.92 → 3.93 | Yes |
| `claude/system/execution_prompt.md` | STEP 5.2 | Write the return note at the in-flight transition (LL-v9.15-P3-02) | 3.93 (same bump) | Yes |
| `claude/system/execution_prompt.md` | STEP 5.1 | P1/P2 found-defect rows cite PO and DoQ acceptance with a rationale (LL-v9.15-P4-02) | 3.93 (same bump) | Yes |
| `claude/system/release_planning_prompt.md` | STEP 4 calibration check | Read Scope or Acceptance Criteria text (LL-v9.15-Release-03) | 2.70 → 2.71 | Yes |
| `claude/system/delivery_verification_prompt.md` | STEP 1 | Accept `deferred_at_planning`, with the same backlog check as `returned_to_backlog` (LL-v9.15-P4-01) | 3.16 → 3.17 | Yes |
| `claude/system/post_ship_closure.md` | STEP 3.1 | Banner a planning-deferred item that is already met or superseded (LL-v9.15-Release-02) | 2.44 → 2.45 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | Header, §6B, §8, §9, §10 source lines, §14 | Versions synced to the four prompts above | 4.252 → 4.253 | Yes |

---

## New files created this run

- `claude/cycles/2026-11-03__release-v9.15/closure_escalations.md`, holding `ESC-CLOSE-20261106-01` (`BLG-FE-271` §4.2.1 scope ruling and conditional Known Deviations text) and `ESC-CLOSE-20261106-02` (programme phasing vs §1.4c).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/post_ship_closure.md` | STEP 3.1 split-achievability carve-out | Distinguish escalation-only remainders (keep open) from remainders moved to follow-up items filed this cycle (banner) (`LL-v9.15-Closure-01`) | Head of Specs Team; PMO Lead | v9.16 sprint — `BLG-GOV-413` |
| — (grooming, no prompt change) | `claude/backlog/backlog.md` items `BLG-GOV-192`, `197`–`201` | Add ACs and an estimate, or kill (`LL-v9.15-Release-02b`) | PMO Lead; item owners | Before any of them is seated again; checked at the next `groom backlog` |
| — (observation) | `claude/backlog/backlog.md` `BLG-GOV-400` | Banner ✅ COMPLETE citing v9.15 `run_manifest.md` (`LL-v9.15-Release-04`) | PMO Lead | This run, STEP 12 `groom backlog` |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| Does `strategy_rules.md` §4.2.1 v1.23 apply to the plan-linked Trade Entry route (`BLG-FE-271`)? If so, add the proposed Known Deviations entry. `ESC-CLOSE-20261106-01` | Authority ambiguity | Strategy Rules & System Intent Owner | `strategy_rules.md` is sealed for this routine, and the entry depends on a scope ruling only the owner can make |
| How should a phased roadmap programme bind §1.4c selection (`LL-v9.15-Release-01`)? `ESC-CLOSE-20261106-02` | Governance gap | Head of Specs Team, Product Owner | There are two design options across two owners' prompts, and the choice changes how a DL-recorded programme binds Release Planning |

---

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-OPS-214` (P1, key rotation overdue since 2026-08-25) and `BLG-OPS-213` (P2, key copy in the public Pages build) were accepted post-merge and target v9.16 | Seat both in the v9.16 slice ahead of P2/P3 work, or record a dated PO reason for leaving either out | Release Planning |
| 2 | Open post-merge remainders: `BLG-OPS-211` (ST-31 on `main`), `BLG-GOV-408` (ST-45 AC 2), `BLG-AI-27` (ST-24, still `TBD`), `BLG-OPS-197` (ST-33, gate 2026-11-09), `BLG-OPS-201` (after 2026-12-01), `BLG-GOV-399` (production read). `BLG-SPEC-217` (ST-35 production) is recorded as done in ST-35's notes but has no banner | Check each at the next Release Planning; retarget `BLG-OPS-197`/`BLG-GOV-399` off the shipped v9.15; do not re-grade ST-24, ST-31, ST-35 or ST-45 | All |
| 3 | `docs/governance/governance_overhead_audit_2026-11-02.md` (v9.14 ST-53 AC 2) and the ST-45 sunset review (`BLG-GOV-408`) are both inputs the next `run roadmap` must link | Link both as inputs at the next `run roadmap` | Roadmap |
| 4 | Until `ESC-CLOSE-20261106-02` is ruled, §1.4c will again try to seat the programme's later-phase P2 items early (`BLG-FE-260` at v9.16) | Apply the ruling if given; otherwise hold programme items to their DL-088 phase by recorded PO override | Release Planning |
