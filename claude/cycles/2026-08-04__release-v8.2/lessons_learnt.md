Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-04
Cycle: 2026-08-04__release-v8.2

# Lessons Learnt — Release Planning — v8.2

## What worked well

- The user-facing scan this cycle found 5 ready items instead of the single item found at each of the last two cycles — reading each candidate's full Problem/Scope text (not just its priority label) surfaced genuinely shippable UX-polish and accessibility items (`BLG-FE-67`, `BLG-FE-105`, `BLG-FE-138`) that a priority-only scan (all P3) would likely have skipped in favour of higher-labelled but gate-blocked items.
- `BLG-SEC-27`, `BLG-OPS-128`, and `BLG-GOV-285` were filed during `v8.1` execution with `Provisional-Target: v8.2` already set, correctly anticipating this cycle — a good signal that forward-targeting newly-discovered items at filing time (rather than leaving them `TBD`) reduces re-derivation work at the next Release Planning session.
- The STEP 1.4a.1 Sunset Criteria (added at `v8.1` via `BLG-GOV-280`) made this cycle's `BLG-FEAT-73`/`BLG-FEAT-74` disposition mechanical rather than an ad hoc judgment call: the check is explicitly "3 of 4, not yet mandatory" rather than requiring fresh reasoning about when enough is enough.

## Friction Log

### Friction Item 1

**Classification:** Type C — Self-caught verification error (scan-methodology gap, not a prompt defect)

**Recurrence:** 3rd consecutive Release Planning cycle with a related self-caught ungated-candidate scan miss (`v8.0`: gate-field-name variant on `BLG-BE-24`/`BLG-OPS-48`; `v8.1`: scan line-window bounds on the same two items; `v8.2`, this cycle: `BLG-OPS-48` again — a 3rd, distinct failure mode). Per `v8.1`'s own lessons learnt Recurrence Escalation 1, which stated explicitly "if a second instance ... is found, file a `BLG-GOV-*` item" and separately flagged that this file's own Carry-Forward Item 1 treats a 3rd instance as a threshold ("If a 3rd instance occurs, this should be treated as a mandatory action-now patch, not a further carry-forward") — **this is that 3rd instance.**

**What happened:** The initial P1/P2 ungated-candidate scan (a scripted full-block regex check for `**Gate criteria:**`/`**Gate:**`/`**Gate date:**` as standalone bolded field labels) again missed `BLG-OPS-48`'s real gate condition, because it is expressed as free text inside the `**Provisional-Target:**` field value ("Gate date: 2026-11-01") rather than as its own bolded field. The item was briefly included in a draft `backlog.md` edit (its `Provisional-Target` field was overwritten to `v8.2`) before being caught on a subsequent verification pass that specifically re-read each selected item's full block for stray gate language. The erroneous `backlog.md` edit was reverted to the item's original two-line `Provisional-Target` text before the release plan was finalised; `BLG-OPS-48` was removed from scope entirely (25 items, not 26).

**Where in the routine:** STEP 2 scope extraction (candidate identification) and the STEP 4 backlog-write step — caught between draft and commit, before `backlog_txn.json` was marked `committed`.

**Root cause:** Same structural gap named at `v8.0` and `v8.1` — `release_planning_prompt.md` still does not define or require a canonical, mechanically-reliable scan procedure for identifying gated vs. ungated candidates. `BLG-OPS-48` specifically has a known pre-existing data-quality defect (a duplicate `**Provisional-Target:**` field, one of which duplicates the gate condition as free text) that has now caused two different scan misses across two different cycles (`v8.0`'s field-name-variant search, `v8.2`'s field-name-only search) — the item itself is a repeat offender, not just the scan methodology.

**Blast radius analysis:**
- What would have propagated: had this gone uncaught, `BLG-OPS-48` would have been committed to `stage4_backlog_slice.md`/`backlog.md` as firm scope 3+ months before its own stated gate condition clears, then surfaced as blocked/premature at Sprint Planning or Execution.
- Recovery cost if uncaught: low-medium — manual removal, capacity re-check (~0.5 day), ST renumbering, one stage later than ideal. Same class as the two prior instances.

**Process patch:** Not filed directly by this engine — new backlog items are outside Release Planning's write scope (`backlog.md` writes are release-slice-only per `release_planning_prompt.md` §7; `claude/system/*` is entirely out of scope for this engine). Per the mandatory-action-now threshold this instance crosses, the very next session with backlog write authority (`groom backlog`, `run roadmap`, or a direct user-directed session fix) **should treat filing the canonical gate-detection procedure item as action-now, not a further deferral** — two consecutive Release Planning cycles have now carried this forward without it being filed. Recommended item scope: (a) a canonical, scripted (not ad hoc) gate-detection procedure for `release_planning_prompt.md`'s scope-selection guidance, covering every observed gate-field variant including gate conditions embedded inside `Provisional-Target` text; (b) as a narrower, immediately-actionable companion, a direct data-quality fix to `BLG-OPS-48`'s own backlog entry — collapse its duplicate `**Provisional-Target:**` field into a single line with an explicit `**Gate criteria:**` field, so this specific item stops being a repeat scan-miss source regardless of whether (a) ships this cycle or not.

## Recurrence Escalations

**Recurrence Escalation 1 (elevated from `v8.1`'s Recurrence Escalation 1):** 3rd consecutive Release Planning cycle with a self-caught ungated-candidate scan miss. This crosses the mandatory-action-now threshold `v8.1`'s own lessons learnt named in advance. Flagged here with the strongest available language within this engine's write scope — the next session with backlog write authority should file the process-patch item (see Friction Item 1) as its first action, not as one item among many.

## Process improvements actioned this run

None (this engine's write scope does not extend to filing new backlog items or patching `release_planning_prompt.md`/`claude/system/*`).

## Outstanding deferred patches

| Patch | Target | Rationale |
|-------|--------|-----------|
| File `BLG-GOV-*`: canonical, scripted gate-detection procedure for Release Planning's scope-selection scan (full-block scan, canonical field-name list including gate conditions embedded in `Provisional-Target` text) | Next `groom backlog` or `run roadmap` session — **action-now**, per Recurrence Escalation 1 | 3rd consecutive cycle with a related self-caught miss |
| Fix `BLG-OPS-48`'s own backlog entry: collapse duplicate `**Provisional-Target:**` field, add explicit `**Gate criteria:**` field | Next session with `backlog.md` content-edit authority (not Release Planning) | This specific item has now caused 2 of the 3 recorded scan misses across 2 different cycles |

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The ungated-candidate scope-selection scan has now produced a self-caught miss at 3 consecutive Release Planning cycles (`v8.0`, `v8.1`, `v8.2`), crossing the mandatory-action-now threshold named at `v8.1`. | The next session with backlog write authority should file the canonical gate-detection procedure item as its first action. | Release Planning / groom backlog / run roadmap |
| 2 | `BLG-FEAT-73`/`BLG-FEAT-74` are now at 3 of 4 consecutive Option (a) perennial-return dispositions. | If `v8.3` also defers both under an unchanged rationale, the STEP 1.4a.1 mandatory sunset trigger fires and the next Release Planning session must force Option (b) or document a materially new gate-clearance path. | Release Planning |
| 3 | `.claude_current_state.json.prior_cycle` remains stale (now 4 releases behind), first flagged at `v8.1` and not corrected by that cycle's post-ship closure. | Post-Ship Closure should correct this field the next time it runs, and confirm going forward that its own STEP does write it. | Post-Ship Closure |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-04__release-v8.2",
  "phase": "Release",
  "filed_utc": "2026-08-04T08:50:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 2,
  "escalation_count": 1,
  "overdue_patches": 0,
  "status": "Complete"
}
```
