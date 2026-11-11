Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-11 (created)
Cycle: 2026-11-06__release-v9.16

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v9.16 — Site Structure & Usability, Phase 2
Run: 2026-11-06__release-v9.16
Reviewed by: PMO Lead
Date filed: 2026-11-11
Prior cycle checked: 2026-11-03__release-v9.15

**Prior-cycle closure items checked (`2026-11-03__release-v9.15` `lessons_learnt_closure.md`):**
- Outstanding deferred patch 1, `BLG-GOV-413` (split-achievability case (ii)): **Applied** in v9.16 ST-28 (`post_ship_closure.md` v2.46). It was used live in this run's STEP 3.1 on `BLG-AI-23` and `BLG-OPS-48`, which meets `BLG-GOV-414`.
- Outstanding deferred patch 2 (legacy `BLG-GOV-192`, `197`–`201` with no ACs): `BLG-GOV-198` shipped as ST-30. `BLG-GOV-197` and `199` are no longer active. `BLG-GOV-192`, `200` and `201` remain. **Partly carried** (closure record §6).
- Outstanding deferred patch 3 (`BLG-GOV-400` banner): **Done** at the v9.15 STEP 12.
- Carry-Forward 1 (seat `BLG-OPS-214`/`BLG-OPS-213` at v9.16): both seated (ST-11, ST-12) and shipped. **Closed.**
- Carry-Forward 2 (open post-merge remainders): `BLG-AI-27` shipped (ST-19) and `BLG-OPS-197` shipped (ST-13). `BLG-OPS-211`, `BLG-GOV-408`, `BLG-OPS-201` and `BLG-GOV-399` are still open. **Partly carried.**
- Carry-Forward 3 (link the governance overhead audit and the ST-45 sunset review at the next `run roadmap`): no `run roadmap` has run since. **Carried** (Carry-Forward 3 below).
- Carry-Forward 4 (programme-phase hold): `ESC-CLOSE-20261106-02` was ruled, and §1.4c step 0 held Phase 3 at v9.16 with no override. **Closed.** Its counterpart for the current phase is `ESC-CLOSE-20261111-01` below.

---

## What worked well

- **STEP 3.1 case (ii) on first use.** `BLG-AI-23` (remainder `BLG-AI-27`, shipped as ST-19) and `BLG-OPS-48` (remainders `BLG-OPS-214` and `BLG-OPS-213`, both shipped; `BLG-SPEC-223` open) were bannered by the v2.46 rule. This closes the two "Ambiguous — Confirm" items left by the v9.15 groom.
- **Mechanical banner pass.** Each slice `**Source:**` was mapped to its `### BLG-` heading, with the PR and commit taken from `execution_state.json`. All 30 source items were found on the first pass, and `check_backlog_item_integrity.py` passed after every write.
- **Same-cycle application.** All 7 phase friction items with an unambiguous fix, plus this closure's own finding, were applied in this run (the v2.32 pattern). Four prompts were bumped in one CLAUDE.md §6 checklist pass. The governance-drift check found all 27 tracked files in sync, and `OPERATIONAL_GUIDE.md` self-consistent at 4.258 once the §14 self-row was updated.
- **STEP 5 routed entry.** Delivery Verification routed `BLG-FE-282`'s Known Deviations question to STEP 5, and the entry was added in the same run (`trade_plan.md` v1.24, `DEV-v9.16-ST27-01`).

---

## Friction Log

### Friction Item 1

**Classification:**
- Type C — Missing Gate or Check: A required check did not exist at the point where it was needed

**Recurrence:** No

**What happened:**
The ninth deviation consolidation review (STEP 5.1) found that `metrics_definitions.md` Appendix E Item 4 still read `Open — Known Deviation`. Its tracking item, `BLG-FE-240`, was bannered ✅ COMPLETE at the v9.15 closure under the STEP 3.1 planning-deferred rule (superseded by v9.15 ST-12, which removed the legacy Dashboard) and archived the same day. A story that fixes a deviation updates its spec in the same commit, but a closure banner touches only `backlog.md`, so nothing updated the spec entry.

**Where in the routine:**
STEP 3.1 — planning-deferred banner and split-achievability case (ii)

**Root cause:**
process gap

**Blast radius analysis:**
- What would have propagated: an open deviation in a canonical spec with no active tracking item. Later readers would treat a removed defect as live.
- When it would have surfaced: only at a consolidation review (every 3rd closure), as here
- Recovery cost if uncaught: low (single file fix by the spec owner)

**Process patch:**

→ Applied this run:
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 3.1
  - Change: a banner applied without a fixing story checks `docs/` and `claude/strategy/` for an open Known Deviations entry naming the item, and records a §6 action for that spec's owner.
  - Version: 2.46 → 2.47

---

## Lessons learnt consolidated action summary (STEP 8)

Records reviewed: Release Planning `lessons_learnt.md` (3 friction items); `lessons_learnt_cycle.md` Phase 3 (6 friction items, 4 Carry-Forward rows) and Phase 4 (1 friction item); the v9.15 closure's deferred patches and Carry-Forward; this closure's own finding (1).

| Item | Source | Disposition | Action |
|------|--------|-------------|--------|
| `LL-v9.16-Release-01` — §1.4c step 0 holds later phases but does not seat the current phase's P3/P4 items | Release Planning FI-1 | decision_required | `ESC-CLOSE-20261111-01`, Head of Specs Team with the Product Owner, SLA 2026-11-14T16:55:20Z |
| `LL-v9.16-Release-02` — long-cleared feature gates surface oldest items with stale scope | Release Planning FI-2 (observation) | deferred | Check the remaining feature-ID gates for stale scope at `groom backlog` (STEP 12 of this run) |
| `LL-v9.16-Release-03` — `Provisional-Target` contradicts a cleared gate | Release Planning FI-3 | deferred | `BLG-GOV-419` (via `/backlog-add`), v9.17. Deferred because it widens a bound set by the `ESC-CLOSE-20261007-01` ruling. The one live case, `BLG-OPS-48`, was bannered at STEP 3 |
| `LL-v9.16-P3-01` — new always-visible text breaks unscoped locators | Phase 3 FI-1 | immediate | `execution_prompt.md` v3.93→v3.94 §3.1.A step 13 |
| `LL-v9.16-P3-02` — state commit swept in staged deletions | Phase 3 FI-2 | immediate | `execution_prompt.md` v3.94 §3.1.A step 4a |
| `LL-v9.16-P3-03` — duplicate scenario ID caught only in CI | Phase 3 FI-3 | immediate | `execution_prompt.md` v3.94 §3.1.A step 2b |
| `LL-v9.16-P3-04` — gate dated from the wrong deploy | Phase 3 FI-4 | immediate | `release_planning_prompt.md` v2.72→v2.73 §1.4b step 5 |
| `LL-v9.16-P3-05` — P2 found defects reached close with no acceptance rationale | Phase 3 FI-5 | immediate | `execution_prompt.md` v3.94 STEP 4 Merge Gate Confirmations |
| `LL-v9.16-P3-06` — post-merge trackers met in-cycle have no banner path | Phase 3 FI-6 | immediate | `execution_prompt.md` v3.94 §7 and STEP 5.3. This cycle's four were bannered at STEP 3 |
| `LL-v9.16-P4-01` — post-merge AC met before verification has no named disposition | Phase 4 FI-1 | immediate | `delivery_verification_prompt.md` v3.17→v3.18 STEP 2.1 |
| `LL-v9.16-Closure-01` — banner without a fixing story leaves its Known Deviations entry open | Closure FI-1 | immediate | `post_ship_closure.md` v2.46→v2.47 STEP 3.1 |

Totals: **8 immediate**, **2 deferred**, **1 escalated**.

---

## Recurrence Escalations

None. The v9.15 closure's one deferred prompt patch (`BLG-GOV-413`) shipped this cycle as ST-28. No deferred patch has been carried 2+ cycles without a `prompt_change_log.md` entry. Phase 3 FI-5 and FI-6 are first scope gaps against `LL-v9.15-P4-02` and `LL-v9.15-P3-01`, as the Phase 3 record notes.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | §3.1.A steps 13, 4a, 2b; STEP 4; §7; STEP 5.3 | LL-v9.16-P3-01, -02, -03, -05, -06 | 3.93 → 3.94 | Yes |
| `claude/system/release_planning_prompt.md` | §1.4b step 5 | Deploy-derived gate date cites the merged PR (LL-v9.16-P3-04) | 2.72 → 2.73 | Yes |
| `claude/system/delivery_verification_prompt.md` | STEP 2.1 | Gap met before verification registered `Resolved post-merge` (LL-v9.16-P4-01) | 3.17 → 3.18 | Yes |
| `claude/system/post_ship_closure.md` | STEP 3.1 | Story-less banner flags an open Known Deviations entry (LL-v9.16-Closure-01) | 2.46 → 2.47 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | Header, §6B/§7/§8/§10 source lines, §14 | Versions synced to the four prompts above | 4.257 → 4.258 | Yes |

---

## New files created this run

- `claude/cycles/2026-11-06__release-v9.16/closure_escalations.md`, holding `ESC-CLOSE-20261111-01` (current programme phase's P3/P4 tier in §1.4c).
- `docs/governance/deviation_consolidation_review_2026-11-11.md` (STEP 5.1, ninth run).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/release_planning_prompt.md` | §1.3a bound 2 | A gate clearance may set a gate-worded `Provisional-Target` to `TBD` (`LL-v9.16-Release-03`) | Head of Specs Team; PMO Lead | v9.17 sprint — `BLG-GOV-419` |
| — (observation) | `claude/backlog/backlog.md` feature-ID gates | Check the remaining feature-ID gates for stale scope (`LL-v9.16-Release-02`) | PMO Lead | This run, STEP 12 `groom backlog` |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| Should §1.4c seat the current programme phase's ready P3/P4 items as a tier after P1/P2 (`LL-v9.16-Release-01`)? `ESC-CLOSE-20261111-01` | Governance gap | Head of Specs Team, Product Owner | It changes the ready-pool ordering, which is a prioritisation policy |

---

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Five P2 found defects are open, each accepted by the PO and DoQ: `BLG-FE-282` (recommended first), `BLG-FE-281`, `BLG-OPS-217` (target still `TBD`), `BLG-BE-211` and `BLG-FE-278` | Seat them in the v9.17 slice ahead of P3 work, or record a dated PO reason for leaving one out | Release Planning |
| 2 | Until `ESC-CLOSE-20261111-01` is ruled, Phase 3's P3 items (`BLG-FE-257`–`263`, `265`, less the P2 `BLG-FE-260`) are not reached by §1.4c at v9.17 | Apply the ruling if given; otherwise seat them by recorded PO override, as at v9.16 | Release Planning |
| 3 | `docs/governance/governance_overhead_audit_2026-11-02.md` (v9.14 ST-53 AC 2) and the ST-45 sunset review (`BLG-GOV-408`) are still unlinked; `completed_cycle_count` is now 93 (odd), and `next_release` is unscoped | Run `run roadmap --reason "scheduled"` before `plan release`, and link both as inputs | Roadmap |
| 4 | `BLG-FE-254`'s Stops moved group (TL-09/TL-10) waits on `BLG-BE-205`, whose ACs cover the data but not the two Playwright ACs | Seat `BLG-BE-205` with the TL-09/TL-10 tests, or add them to its ACs, then banner `BLG-FE-254` | Release Planning |
