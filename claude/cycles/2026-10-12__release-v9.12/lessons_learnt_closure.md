Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-15

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Restore AI journal summaries for UUID trade IDs (`BLG-BE-162`, P1, the v9.11 verification acceptance condition). Make signal sizing, stops and position status correct across Signals, Positions and Risk. Let Trade Entry show the stop, risk and size before save (`BLG-BE-146`). Ship v9.12's accessibility, security, operations, spec and governance hygiene items. 48 stories across 6 EPICs.
Run: 2026-10-12__release-v9.12
Reviewed by: PMO Lead
Date filed: 2026-10-15
Prior cycle checked: 2026-10-08__release-v9.11 (`lessons_learnt_closure.md`)

---

## What worked well

- **Tracing.** All 48 shipped stories traced to their `BLG-*` source items in one scripted pass (STEP 3), using each slice entry's `**Source:**` field. Every COMPLETE banner carries the EPIC PR and the story commit SHA from `execution_state.json`, and `scripts/check_backlog_item_integrity.py` passed after the edit. The split-achievability carve-out was checked: ST-28's `numpy` hold (`BLG-TECH-24`) and ST-34's unrecoverable names (`BLG-QA-223`) have their own items, ST-06 closed with no remainder, and no open escalation references a source item. So all 48 were correctly marked COMPLETE.
- **Changelog `User Impact` parsed as intended.** The v9.12 entry was read back through `get_latest_changelog_entry()`: it returns the 4 user-facing EPIC rows and excludes EPIC-05/06.
- **The STEP 7.3 sweep found real resolutions.** 10 Open TSG entries were checked and 3 resolved (TSG-v9.9-03, TSG-v9.9-04, TSG-v9.11-01), because this cycle shipped their backlog items (ST-45, ST-47, ST-01). The previous two closures checked 4 and 7 entries and resolved none.
- **v9.11 carry-forward items closed in-cycle.** `BLG-BE-162` was seated at P1 and shipped as ST-01 (Carry-Forward #2). `BLG-GOV-385` shipped as ST-39, so CLAUDE.md §8 step 2c now runs the backlog item integrity check (Carry-Forward #3). Two of the v9.11 deferred patches shipped as stories (ST-39, ST-40).
- **Same-cycle application pattern held.** All five prompt patches with unambiguous fix text (3 Phase 3/4, 2 Release Planning) were applied at this closure, plus the carried v9.11 closure action #8(b). `OPERATIONAL_GUIDE.md` §14 and the phase source-prompt headers were re-checked afterwards: 34 version references, 0 mismatches.

---

## Friction Log

### Friction Item 1

**Classification:**
- Type B — Semantic Mismatch: The same concept was named or interpreted differently across documents or roles

**Recurrence:** Yes — the deferred patch was first filed at `2026-10-06__release-v9.10` (Release Planning Friction Item 1) and carried at `2026-10-08__release-v9.11`

**What happened:**
The v9.11 closure carried the deferred patch "treat `Gate criteria: None`/`N/A` as ungated in `scan_backlog_gate_conditions.py`" with `BLG-GOV-373` as its vehicle. Reading `BLG-GOV-373` directly at this closure showed that its scope is only an allow-list for two known date-lapse false positives. It does not mention `None` or `N/A` gate values. The patch has had no item covering it for 2 cycles, and the script is unchanged.

**Where in the routine:**
STEP 8.5 — `lessons_learnt_prompt.md` §3.7 row-completeness reconciliation

**Root cause:**
process gap. "Folded into `<ID>`" was recorded without confirming that the item's scope covers the patch, which §3.7 requires.

**Blast radius analysis:**
- What would have propagated: the patch would keep being carried under a vehicle that will never deliver it. Each Release Planning run keeps reading `None`/`N/A` gates by hand.
- When it would have surfaced: when `BLG-GOV-373` shipped without the change, or never.
- Recovery cost if uncaught: low (single file fix)

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `scripts/scan_backlog_gate_conditions.py`
  - Section: Gate parsing
  - Change required: Treat a literal `Gate criteria: None`/`N/A` as ungated. The vehicle needs a decision (a dedicated backlog item, or widening `BLG-GOV-373`). Scripts are outside this routine's write scope.
  - Owner: Head of Specs Team / Head of Engineering
  - Target: `ESC-CLOSE-20261015-01` (SLA 2026-10-18)

---

## Recurrence Escalations

| Issue | Prior cycle(s) | Escalated to | ESC-ID |
|-------|----------------|--------------|--------|
| `scan_backlog_gate_conditions.py` `None`/`N/A` gate handling: carried 3 cycles, and its named vehicle `BLG-GOV-373` does not cover it (Friction Item 1) | `2026-10-06__release-v9.10`, `2026-10-08__release-v9.11` | Head of Specs Team | `ESC-CLOSE-20261015-01` |

**Recurrence Notes (§3.7 row-completeness reconciliation of the v9.11 Outstanding deferred patches table):** each row was re-checked by patch ID against `prompt_change_log.md` as of this run, and by reading the named target file directly.
1. **`scan_backlog_gate_conditions.py`, treat `Gate criteria: None`/`N/A` as ungated.** Not applied; the "folded into `BLG-GOV-373`" disposition does not hold (Friction Item 1). **Escalated**, `ESC-CLOSE-20261015-01`.
2. **"Gating item shipped — verify" list.** **Applied:** ST-40 (`122bfac3`, `BLG-GOV-386`), `release_planning_prompt.md` v2.61→v2.62 and the script's new output.
3. **Backlog lock before §1.3a edits.** Not applied. A design choice between two options is still required. **Carried, 2nd cycle** (table below). Target unchanged at 2026-10-20.
4. **§1.3a bound 5 for gates removed outside Release Planning.** **Applied this run:** `release_planning_prompt.md` v2.62→v2.63.
5. **CLAUDE.md §8 step 2c.** **Applied:** ST-39 (`3481be3b`, `BLG-GOV-385`).
6. **`/reports` case in `categorizeEndpoint()`.** **Folded into `BLG-FE-217`** (P3, filed 2026-10-12). Its scope is this exact change, plus a Playwright grouping assertion. Still open.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | §3.1.A step 4d (new) | Before `done`, list every workflow run for the story's SHA. `ci-tests.yml` must conclude `success` when the commit touches `backend/**` or `requirements*.txt` (LL-v9.12-P3-01, Phase 3 friction item 1) | v3.86 → v3.87 | Yes |
| `claude/system/execution_prompt.md` | §3.2.B step 7 (new); STEP 4 note | Run `gh pr view --json state` before any later commit to an EPIC branch, including merge-gate records. If `MERGED`, commit on `main` (LL-v9.12-P3-02, Phase 3 friction item 2) | v3.86 → v3.87 (same bump) | Yes |
| `claude/system/execution_prompt.md` | §5.3 Deviations filed this sprint | `Pass_with_deviation` rows show the deviation's severity and the tracking item's own backlog priority as separate columns (LL-v9.12-P4-01, Phase 4 friction item) | v3.86 → v3.87 (same bump) | Yes |
| `claude/system/release_planning_prompt.md` | STEP 4 calibration check | Applies to the whole ready pool before §1.4c selection (LL-v9.12-Release-03, Release Planning Friction Item 3) | v2.62 → v2.63 | Yes |
| `claude/system/release_planning_prompt.md` | §1.3a bound 5 | Also covers gates removed by a Product Owner decision outside Release Planning (v9.11 closure action #8(b)) | v2.62 → v2.63 (same bump) | Yes |
| `claude/system/post_ship_closure.md` | STEP 8 | A deferred action that needs a prompt change is applied now or tracked by a backlog item with a sprint target, never a "before `plan release`" deadline (LL-v9.12-Release-01, Release Planning Friction Item 1) | v2.40 → v2.41 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | Source-prompt headers; §14 | Versions synced for the three prompt bumps above; Change Log row added | v4.238 → v4.239 | Yes |

Size budget (`shared_standards.md` §11): `execution_prompt.md` and `post_ship_closure.md` were already over 68,500 bytes, and their split items are open (`BLG-GOV-379`, `BLG-GOV-381`), so no new item was filed. Each addition is kept to the minimum process text.

---

## New files created this run

- `claude/cycles/2026-10-12__release-v9.12/closure_escalations.md` (`ESC-CLOSE-20261015-01`)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `scripts/scan_backlog_gate_conditions.py` | Gate parsing | Treat a literal `Gate criteria: None`/`N/A` as ungated (v9.10 Release Planning Friction Item 1; Friction Item 1 above). 3rd cycle, escalated | Head of Specs Team / Head of Engineering | `ESC-CLOSE-20261015-01`, SLA 2026-10-18 |
| `claude/system/release_planning_prompt.md` | §1.3a / STEP 3.9 | Acquire `claude/backlog/.lock` before the first §1.3a in-place gate edit, or move those edits after STEP 3.9. A design choice between the two options is required (v9.11 Release Planning Friction Item 2). 2nd cycle. Under post_ship_closure.md v2.41, file it via `/backlog-add` with a sprint target if the choice is not made by its target | Head of Specs Team | 2026-10-20 |
| `src/pages/SystemStatus.js` | `categorizeEndpoint()` | Add a `/reports` case plus a Playwright grouping assertion (v9.11 closure Friction Item 2) | Head of Engineering | `BLG-FE-217` (P3), next sprint that seats it |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| `scan_backlog_gate_conditions.py` `None`/`N/A` gate handling has had no covering vehicle for 3 cycles (`ESC-CLOSE-20261015-01`) | Recurrence | Head of Specs Team | §3.7: a deferred patch carried two or more cycles unapplied is a recurrence escalation, and its named vehicle does not cover it. |

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `next_release` still reads `v9.12`, the release just shipped, and roadmap §1 "Next planned release" is `[TBD]`. | Run `run roadmap --reason scheduled` (or make a scoping decision) before `plan release v9.13`. | Roadmap |
| 2 | About 22 items tagged `Provisional-Target: v9.12` were not seated (v9.12 Release Planning Friction Item 2). | When filing a follow-up item, set `Provisional-Target: TBD` unless the roadmap commits the release to it. Treat a stale same-release tag as carrying no selection weight (`ESC-CLOSE-20260923-01`). | All |
| 3 | Verification sign-off was agent-mediated on user direction for the 5th consecutive cycle (v9.8–v9.12), and is marked "Pending human confirmation". | Confirm or amend the v9.12 DoQ and PO sign-offs before `plan release v9.13`, as was done for v8.0–v9.11 on 2026-10-12. | Release Planning |
