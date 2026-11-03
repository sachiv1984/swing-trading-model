Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-03
Cycle: 2026-10-29__release-v9.14

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v9.14 — Production Deploy Restore, Market-Data Resilience & Sizing Fix
Run: 2026-10-29__release-v9.14
Reviewed by: PMO Lead
Date filed: 2026-11-03
Prior cycle checked: 2026-10-16__release-v9.13 (`lessons_learnt_closure.md`)

---

## What worked well

- STEP 5's routed-entry path worked as designed for a non-`strategy_rules.md` spec. Delivery Verification routed two Known Deviations entries (`BLG-FE-239`, `BLG-FE-240`) to this step, and both were written into `metrics_definitions.md` Appendix E with all six fields, as a documentation-only v1.34.1. No escalation was needed, unlike v9.13's `strategy_rules.md` case.
- The STEP 3.1 split-achievability carve-out caught `BLG-GOV-178` (ST-23). It is a recurring quarterly item whose live-production bar is still open under the re-deferred `ESC-EXEC-20260910-01`, so marking it COMPLETE would have let STEP 12 archive it and drop that cross-reference. The other five seal-marked post-merge stories (ST-01, ST-39, ST-42, ST-43, ST-45) each have their own tracking item, so their source items were marked COMPLETE as `LL-v9.13-P3-03` intends.
- All three v9.13 deferred lessons-learnt patches (`BLG-QA-238`, `BLG-GOV-397`, `BLG-GOV-398`) shipped in v9.14 as ST-31, ST-44 and ST-45. That is the first full cycle of the `LL-v9.12-Release-01` rule (backlog item with a sprint target instead of a "before `plan release`" deadline), and it closed every row.
- The STEP 7.3 full-document sweep resolved 6 of 12 Open TSG entries in one pass, the most in one closure since the sweep was made mandatory. Most were EPIC-05 test-coverage stories that targeted earlier TSG rows directly.

---

## Friction Log

### Friction Item 1

**Classification:** Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced

**Recurrence:** Yes — appeared in 2026-10-16__release-v9.13 (Carry-Forward #1: run a rebalance before `plan release`)

**What happened:**
v9.13's closure carried forward "run `run roadmap --reason scheduled` … before `plan release v9.14`". DL-087 named v9.14 and Release Planning went ahead without a rebalance, so v9.14 was planned on DL-086's Skill-Silo and PVR readings (Release Planning Friction Item 3). `completed_cycle_count` is 90 (even), so this closure's STEP 0 advises a rebalance again, and the run will make it 91 at STEP 10. Unless the Product Owner runs one, v9.15 would be planned on readings three releases old. The `LL-v9.13-Release-02` observation (U share under P2-first ordering) also depended on that rebalance and is still unread.

**Where in the routine:**
STEP 0 — Rebalance Cadence Check (advisory); STEP 8 — Release Planning Friction Item 3

**Root cause:**
process gap

**Blast radius analysis:**
- What would have propagated: v9.15's scope selection, using Skill-Silo and PVR readings from `2026-10-16__scheduled`
- When it would have surfaced: next roadmap rebalance
- Recovery cost if uncaught: low (the readings inform weighting, not hard gates)

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: — (observation; the cadence advisory is non-blocking by design and the Product Owner may skip it, per STEP 0)
  - Section: `post_ship_closure.md` STEP 0 Rebalance Cadence Check
  - Change required: none; Carry-Forward #1 states the advisory as a Roadmap action before `plan release v9.15`
  - Owner: Product Owner
  - Target: before `plan release v9.15`

---

### Friction Item 2

**Classification:** Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** No

**What happened:**
Two post-merge tracking items carried to post-sprint, `BLG-OPS-201` (needs a full production month, so after 2026-12-01) and `BLG-GOV-399` (needs a production read), still carry `Provisional-Target: v9.14` now that v9.14 has shipped. `BLG-FE-243` is still `TBD`, although its P2 acceptance condition retargets it to v9.15. This routine's backlog scope (mark shipped complete; add missing Phase 4 items) does not allow editing either field.

**Where in the routine:**
STEP 3.3 — Confirm next-release items are tagged

**Root cause:**
document staleness

**Blast radius analysis:**
- What would have propagated: `roadmap_prompt.md` STEP -1.5's stale-release-target check and `groom backlog` STEP 3.5 Deferral Age Validation would read the two items as targeted at a shipped release
- When it would have surfaced: next `groom backlog` (STEP 12 of this run) or next rebalance
- Recovery cost if uncaught: low (single-field retarget)

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/backlog/backlog.md` (item fields, not a prompt)
  - Section: `BLG-OPS-201`, `BLG-GOV-399`, `BLG-FE-243` Provisional-Target
  - Change required: retarget `BLG-OPS-201` to v9.15 or later, `BLG-GOV-399` to v9.15 or TBD with a reason, and `BLG-FE-243` to v9.15 (acceptance condition)
  - Owner: PMO Lead; item owners
  - Target: STEP 12 `groom backlog` of this run, or the next Release Planning run

---

## Recurrence Escalations

None. Friction Item 1 recurs, but the prior outstanding action was an advisory that the Product Owner may skip (STEP 0), not an unapplied patch. Every row of v9.13's Outstanding deferred patches table is dispositioned:
- `LL-v9.13-P3-01` (`BLG-QA-238`): **Applied** — ST-31, `f1474aa4`.
- `LL-v9.13-P3-04` (`BLG-GOV-397`): **Applied** — ST-44, `d6a4892d`, `execution_prompt.md` v3.90.
- `LL-v9.13-Release-01` (`BLG-GOV-398`): **Applied** — ST-45, `a2168d7f`, `release_planning_prompt.md` v2.66.
- `LL-v9.13-Release-02` (observation): carried — no rebalance has run since; see Friction Item 1.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | §3.1.A step 2a | Run `CI=false npm run build` as its own command before any commit touching `src/**`/`package*.json`; never chain it with commit or push (`LL-v9.14-P3-03`) | 3.90 → 3.91 | Yes |
| `claude/system/execution_prompt.md` | STEP 4; STEP 5.1 | Every `qa_evidence_EPIC-xx.md` has a `## Merge Gate Confirmations` section naming the human QA sign-off, PO acceptance and merge, stating a bare merge plainly; STEP 5.1 checks it (`LL-v9.14-P3-02`) | 3.90 → 3.91 | Yes |
| `claude/system/execution_prompt.md` | STEP 5.1 | Slice-item record check: every `### ST-xx` in the authoritative slice has an `execution_state.json` entry, including `deferred_at_planning` (`LL-v9.14-P4-01`) | 3.90 → 3.91 | Yes |
| `claude/system/backlog_management_prompt.md` | STEP 0; STEP 1 | Load the latest Release Planning `run_manifest.md` archive-at-groom list and classify each listed item explicitly (`LL-v9.14-Release-04`) | 1.18 → 1.19 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | header; §8, §6M source lines; §14 | Version references for the two prompts above | 4.245 → 4.246 | Yes |
| `docs/specs/metrics_definitions.md` | Appendix E; Appendix D | Known Deviations entries for `BLG-FE-239` and `BLG-FE-240` (STEP 5, routed) | 1.34.0 → 1.34.1 | Not applicable (canonical spec, not a prompt) |

---

## New files created this run

- `claude/cycles/2026-10-29__release-v9.14/closure_escalations.md` — `ESC-CLOSE-20261103-01` and `-02`.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `scripts/scan_backlog_gate_conditions.py` | Gate-ID detection | Treat a shipped roadmap feature ID (PT-xx, SI-xx, PO-xx) as a met gate and list it as "gating item shipped" (`LL-v9.14-Release-02`) | Head of Specs Team; PMO Lead | v9.15 sprint — `BLG-GOV-404` |
| `scripts/check_execution_state_consistency.py`; `claude/system/execution_prompt.md` §9.2 | `merge_gate` check | When `merge_order` is present, expect `epics_pending` = `merge_order` minus merged EPICs (`LL-v9.14-P3-01`) | Head of Specs Team | v9.15 sprint — `BLG-QA-240` (`BLG-GOV-401` is a duplicate to fold at `groom backlog`) |
| — (observation, no prompt change) | `post_ship_closure.md` STEP 0 | Run the advised rebalance before `plan release v9.15` (Release Planning Friction Item 3; Friction Item 1 above) | Product Owner | Before `plan release v9.15` |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| Does a human merge with no separately recorded DoQ QA sign-off or PO acceptance satisfy the always-human merge-gate rows (PR #2137, #2139)? `ESC-CLOSE-20261103-01` | Authority ambiguity | Head of Specs Team, Product Owner | The v3.91 patch records the facts; whether they meet the gate is an authority ruling |
| Add a `release_planning_prompt.md` §1.4c tier for deferred lessons-learnt patch items (`LL-v9.14-Release-01`)? `ESC-CLOSE-20261103-02` | Authority ambiguity | Head of Specs Team, Product Owner | The tier would narrow the standing Product Owner ruling `ESC-CLOSE-20260923-01` (same-release targets carry no selection weight) |

---

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | No rebalance has run since `2026-10-16__scheduled`; STEP 0 advises one (count 90, even) and `next_release` reads `v9.14`, the release just shipped, with roadmap §1 "Next planned release" `[TBD]` | Run `run roadmap --reason scheduled` before `plan release v9.15`, and link `docs/governance/governance_overhead_audit_2026-11-02.md` as an input (ST-53 AC 2) | Roadmap |
| 2 | Three accepted P2 found defects (`BLG-FE-239`, `BLG-FE-240`, `BLG-FE-243`) carry an acceptance condition to stay P2 for v9.15; `BLG-FE-243` still reads `TBD` | Weigh all three for the v9.15 slice and record a reason if any is left out | Release Planning |
| 3 | `ESC-CLOSE-20261103-02` is open; until it is ruled on, `BLG-GOV-404` (P3, v9.15) has no selection tier ahead of the round-robin | Apply the ruling if given; otherwise seat it by Product Owner override, as at v9.14, or retarget with a reason | Release Planning |
| 4 | Three post-merge remainders stay open: `BLG-OPS-201` (after 2026-12-01), `BLG-GOV-399` (production read), `BLG-GOV-400` (next gate scan) | Check them at the next Release Planning and delivery verification; do not re-grade ST-23, ST-39 or ST-45 | All |
