Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-17 (created)
Cycle: 2026-11-11__release-v9.17

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v9.17 — Site Structure & Usability, Phase 3
Run: 2026-11-11__release-v9.17
Reviewed by: PMO Lead
Date filed: 2026-11-17
Prior cycle checked: 2026-11-06__release-v9.16

**Prior-cycle closure items checked (`2026-11-06__release-v9.16` `lessons_learnt_closure.md`):**
- Outstanding deferred patch 1, `BLG-GOV-419` (`LL-v9.16-Release-03`): **Applied** in v9.17 ST-18 (`release_planning_prompt.md` v2.75). AC 2 is a post-merge remainder; the item stays open as its tracker.
- Outstanding deferred patch 2 (`LL-v9.16-Release-02`, stale feature-gate scope): **Done** at the v9.16 STEP 12 groom.
- Carry-Forward 1 (seat the five accepted P2s at v9.17): all five seated (ST-11 to ST-15). `BLG-BE-211`, `BLG-FE-278`, `BLG-FE-281` and `BLG-FE-282` are now closed; `BLG-OPS-217` has its causes fixed and stays open for its post-fix weekly report. **Closed.**
- Carry-Forward 2 (`ESC-CLOSE-20261111-01`): ruled option (a); §1.4c step 1b seated Phase 3's P3s with no override. **Closed.**
- Carry-Forward 3 (link the governance overhead audit and the ST-45 sunset review at the next `run roadmap`): the Product Owner named v9.17 without a rebalance, so no `run roadmap` has run since 2026-11-03. **Carried** (Carry-Forward 3 below).
- Carry-Forward 4 (`BLG-FE-254` TL-09/TL-10 waits on `BLG-BE-205`): both seated and shipped (ST-09, ST-10); `BLG-FE-254` bannered at this run's STEP 3. **Closed.**

---

## What worked well

- **Banner pass on the first attempt.** Each slice `**Source:**` mapped to its `### BLG-` heading. 17 items were bannered in one scripted write (plus `BLG-BE-211`, already bannered at its post-merge backfill). `check_backlog_item_integrity.py` passed after each write.
- **No split-achievability judgement calls.** Every partial outcome was seal-marked post-merge with a named tracker (`BLG-OPS-217`, `BLG-GOV-419`), so STEP 3.1 case (i) applied without interpretation. The two `Pass_with_deviation` remainders already had follow-up items filed this cycle (`BLG-BE-215`, `BLG-SPEC-238`).
- **No STEP 5 routing.** Both `DEV-*` records had complete Known Deviations entries at verification.
- **Same-cycle application.** Six friction items with unambiguous fixes, plus this closure's own finding, were applied in this run across two prompts. The governance-drift check found all 29 tracked files in sync, and `OPERATIONAL_GUIDE.md` self-consistent at 4.261.

---

## Friction Log

### Friction Item 1

**Classification:**
- Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced

**Recurrence:** No

**What happened:**
At STEP 7, `scripts/check_specs_index_freshness.py` reported two live spec files that `docs/specs/Specs_Index.md` does not reference: `docs/specs/frontend/pages/journal.md` (created by ST-05) and `docs/specs/frontend/pages/performance.md` (created by ST-06). No step in Sprint Execution, Delivery Verification or Post-Ship Closure runs the freshness script, so new canonical page specs went unregistered through all three phases. The run found them only because it chose to run the script.

**Where in the routine:**
STEP 7.2 — Add new gaps

**Root cause:**
process gap

**Blast radius analysis:**
- What would have propagated: the Specs Index, the map of canonical product truth, would omit the two specs that replaced Reports and Performance Analytics
- When it would have surfaced: the next manual freshness run, or a reader failing to find the spec
- Recovery cost if uncaught: low (single file fix)

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 7.2
  - Change: run `check_specs_index_freshness.py`; record each ADDITIONS entry in the cycle's Test Coverage Gaps section and add a closure record §6 action for the Head of Specs Team to register it.
  - Version: 2.47 → 2.48
  - Confirmed by: Head of Specs Team (agent-mediated, §5.3)
  - Prompt change log entry: Yes — appended to claude/system/prompt_change_log.md

---

### Friction Item 2

**Classification:**
- Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** No

**What happened:**
At STEP 2, line 4 of `claude/roadmap/current_roadmap.md` held a chained date history with no `**Last Updated:**` label. The label was lost at a 2026-11-11 edit (Release Planning STEP 5 or the PO naming edit before it). A reader or script looking for the field would not find it. This run restored the label in the same write.

**Where in the routine:**
STEP 2 — Roadmap Update

**Root cause:**
document staleness

**Blast radius analysis:**
- What would have propagated: header-field checks would skip the roadmap's last-update date
- When it would have surfaced: the next `run audit` header check, or never
- Recovery cost if uncaught: low (single file fix)

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/roadmap/current_roadmap.md`
  - Section: header, line 4
  - Change: restored the `**Last Updated:**` label (data fix; no prompt change, as the rule in CLAUDE.md §2 and `shared_standards.md` §16.14 already covers it).
  - Version: n/a (Class 4 header only)
  - Confirmed by: Head of Specs Team (agent-mediated, §5.3)
  - Prompt change log entry: No — not a prompt change

---

## Lessons learnt consolidated action summary (STEP 8)

Records reviewed: Release Planning `lessons_learnt.md` (3 friction items); `lessons_learnt_cycle.md` Phase 3 (5 friction items, 4 Carry-Forward rows) and Phase 4 (1 friction item); the v9.16 closure's deferred patches and Carry-Forward; this closure's own findings (2).

| Item | Source | Disposition | Action |
|------|--------|-------------|--------|
| `LL-v9.17-Release-01` — a phase row marked shipped while a remainder is open, waited-on item named only in prose | Release Planning FI-1 | immediate | `post_ship_closure.md` v2.47→v2.48 STEP 2 item 5a |
| `LL-v9.17-Release-02` — a split-achievability remainder has no effort rule | Release Planning FI-2 | immediate | `post_ship_closure.md` v2.48 STEP 3.1 case (i) remainder estimate note |
| `LL-v9.17-Release-03` — a carry-forward asking for `run roadmap` first has no enforcement point | Release Planning FI-3 (observation) | deferred | No prompt change (the PO may name a release directly). Carried as Carry-Forward 3 and closure record §6 |
| `LL-v9.17-P3-01` — locator collisions from hidden/moved text still reached CI | Phase 3 FI-1 | immediate (a) + deferred (b) | (a) `execution_prompt.md` v3.94→v3.95 §3.1.A step 13. (b) scripted check: `BLG-QA-268` (via `/backlog-add`), v9.18 |
| `LL-v9.17-P3-02` — spec premises the code contradicted found only at pre-commit review | Phase 3 FI-2 | deferred | `BLG-GOV-422` (P2, existing), v9.18 per the PO's 2026-11-12 direction, with the 2026-11-13 scope extensions |
| `LL-v9.17-P3-03` — visual baseline workflow cannot push to EPIC branches | Phase 3 FI-3 | deferred | `BLG-OPS-220` (P3, existing), v9.18 Release Planning |
| `LL-v9.17-P3-04` — process-note timestamps written as estimates | Phase 3 FI-4 | immediate | `execution_prompt.md` v3.95 §9.2 |
| `LL-v9.17-P3-05` — story status not moved to `merged` at one EPIC's merge | Phase 3 FI-5 | immediate | `execution_prompt.md` v3.95 STEP 4 step 2 (the optional consistency-script check is not applied) |
| `LL-v9.17-P4-01` — SSR spec cells did not match `spec_references` | Phase 4 FI-1 | immediate | `execution_prompt.md` v3.95 STEP 5.3A |
| `LL-v9.17-Closure-01` — new spec files go unregistered in the Specs Index | Closure FI-1 | immediate | `post_ship_closure.md` v2.48 STEP 7.2 |
| `LL-v9.17-Closure-02` — roadmap `**Last Updated:**` label missing | Closure FI-2 | immediate | Data fix in `current_roadmap.md` |

Totals: **8 immediate** (6 phase items, of which `LL-v9.17-P3-01` is split, plus 2 closure findings), **4 deferred** (`LL-v9.17-Release-03`, `LL-v9.17-P3-01` (b), `LL-v9.17-P3-02`, `LL-v9.17-P3-03`), **0 escalated**.

---

## Recurrence Escalations

None. The v9.16 closure's one deferred prompt patch (`BLG-GOV-419`) shipped this cycle as ST-18. Phase 3 FI-1 is the first scope gap against `LL-v9.16-P3-01`, as the Phase 3 record notes; part (a) closes the prose gap and `BLG-QA-268` makes it mechanical. No deferred patch has been carried 2+ cycles without a `prompt_change_log.md` entry.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | §3.1.A step 13; §9.2; STEP 4 step 2; STEP 5.3A | LL-v9.17-P3-01 (a), -P3-04, -P3-05, -P4-01 | 3.94 → 3.95 | Yes |
| `claude/system/post_ship_closure.md` | STEP 2 item 5a; STEP 3.1 case (i); STEP 7.2 | LL-v9.17-Release-01, -Release-02, -Closure-01 | 2.47 → 2.48 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | Header, §8/§10 source lines, §14 | Versions synced to the two prompts above | 4.260 → 4.261 | Yes |
| `scripts/prompt_size_baseline.json` | execution and post-ship entries | Baselines raised to the new sizes (reason in the change log rows) | — | Yes (in the prompt rows) |

---

## New files created this run

- None besides this record, `closure_record.md` and `closure_state.json`. No escalation was raised, so there is no `closure_escalations.md`.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| New script + `.claude/skills/commit-check` + `claude/system/execution_prompt.md` §3.1.A step 13 | — | Scripted locator-collision check for added/removed visible text (`LL-v9.17-P3-01` (b)) | Head of Specs Team; QA & Testing Owner | v9.18 — `BLG-QA-268` |
| `claude/system/design_gate_prompt.md` | STEP 2.2 | Data-source, writer, competing-value and failure-state checks (`LL-v9.17-P3-02`) | Head of Specs Team | v9.18 — `BLG-GOV-422` |
| `.github/workflows/update-visual-snapshots.yml` | job permissions, push step | Let regenerated baselines land on `exec/**` (`LL-v9.17-P3-03`) | Infrastructure & Operations Owner | v9.18 — `BLG-OPS-220` |

---

## Escalations

None.

---

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The Product Owner directed seating `BLG-GOV-422` and `BLG-QA-262` (P2) and `BLG-QA-260` (P3, stale Provisional-Target v9.17) next release, and extending `BLG-GOV-422`'s scope (writer, competing-value, failure-state and time-boundary checks; see v9.17 `execution_state.json` process_notes, `a207af77`) | Seat all three in the v9.18 slice, record a dated PO override for `BLG-QA-260`, and apply the `BLG-GOV-422` scope extension | Release Planning |
| 2 | `BLG-FE-294` (P2) is open, accepted by the PO and DoQ at the EPIC-06 merge gate; its Provisional-Target is `TBD` | Seat it ahead of P3 work, or record a dated PO reason for leaving it out | Release Planning |
| 3 | `docs/governance/governance_overhead_audit_2026-11-02.md` and the ST-45 sunset review (`BLG-GOV-408`) are still unlinked; no rebalance since 2026-11-03; `completed_cycle_count` is now 94 (even) and `next_release` is unscoped | Run `run roadmap --reason "scheduled"` before `plan release`, and link both as inputs | Roadmap |
| 4 | Site Structure & Usability Phase 3 shipped. `BLG-UX-08`'s gate (every item in `BLG-FE-244`–`266` and `BLG-SPEC-214`–`216` ✅ COMPLETE or closed) is **met** as of this run's STEP 3: none of those items remains open in `backlog.md` | Seat `BLG-UX-08` (the programme close-out re-review, Provisional-Target v9.18) and clear its gate in place under §1.3a; the user asked to be reminded when this point was reached | Release Planning |
