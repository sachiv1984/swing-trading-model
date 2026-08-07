Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Cycle: 2026-08-07__release-v8.4

# Lessons Learnt — Release Planning — v8.4

Feature / Trigger: Full-capacity, user-feature-prioritised backlog-driven release planning per explicit user instruction.
Run: 2026-08-07__release-v8.4
Reviewed by: Head of Specs Team

---

## What worked well

- The `2026-07-28__scheduled` rebalance's STEP 8.1 Option (b) equivalence continued to cleanly clear STEP -1.2 (5th consecutive release relying on the same decision, `v8.0`→`v8.4`) — no re-litigation needed of whether a backlog-driven release without a formal roadmap section is permitted.
- `BLG-GOV-286`'s own filing (a P1 item in this cycle's scope) primed this session to actively look for stale/mismatched gate-field data rather than trust a single scan pass — which directly led to catching the genuine `BLG-FEAT-78` gate-clear correction.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Tooling/Process Gap (ad hoc verification script produced a false result)

**Recurrence:** Yes — 4th distinct failure mode in the same "gate-detection procedure" problem class already tracked by `BLG-GOV-286` (v8.0: gate-field-name variant; v8.1: scan line-window bounds; v8.2: gate condition embedded in `Provisional-Target` free text).

**What happened:** This session's own ad hoc gate-verification script read a fixed-size line window (25-30 lines) starting from each backlog candidate's header to check for a `**Gate criteria:**`/`**Gate:**`/`**Gate date:**` field. For short entries (e.g. `BLG-QA-110`, whose own body is only 5 lines), the window extended past the entry's own `---` separator (or, in one case, past a missing separator) into a neighbouring item's content — producing a false-positive gate match against `BLG-QA-110` sourced from `BLG-FEAT-78`'s actual `Gate criteria` line 3 entries below. This was caught before being written into governance record content only because the full item text was read manually as a second check before trusting the automated scan result — not because the script itself detected the error.

**Where in the routine:** STEP 2 — Scope Extraction, ungated-candidate verification pass.

**Root cause:** Same class as `BLG-GOV-286`'s own three named failure modes — no scripted, field-boundary-aware gate-detection procedure exists yet. This session's specific manifestation (fixed-line-window read bleeding into a neighbouring entry, in both directions — false positive here, and separately a false negative earlier in the same session for `BLG-GOV-286`'s own gate-check, caused by a missing `---` separator before it) is a 4th distinct root cause worth folding into the same fix.

**Blast radius analysis:**
- What would have propagated: had the manual double-check not been performed, `BLG-QA-110` would have been wrongly excluded from scope on a fabricated gate condition, and the false "self-caught correction" narrative would have been written into `run_manifest.md`, `stage4_backlog_slice.md`, `release_plan.md`, and `decisions--2026-08-07__release-v8.4.md` — governance-record content asserting something untrue about a backlog item's history.
- When it would have surfaced: likely never, absent a future session specifically re-reading `BLG-QA-110`'s full entry and noticing no gate field is actually present.
- Recovery cost if uncaught: low-to-moderate (a few governance documents would carry a fabricated correction narrative; `BLG-QA-110` itself would have been unaffected since it was included in scope either way, just under the wrong justification).

**Process patch:**
→ Already in progress this cycle (not deferred): `BLG-GOV-286`'s acceptance criteria (`stage4_backlog_slice.md` ST-29, this cycle's own scope) have been extended to explicitly require the scripted procedure handle field-boundary detection (stop at the entry's own `---` separator or next `### ` header, never read past either) as a 4th named failure mode, alongside the 3 already tracked. No separate backlog item filed — folded into the existing P1 tracker to avoid creating a 2nd near-duplicate item in the same problem space (the exact pattern Friction Item 1 of the `v8.3` closure warned against).

---

## Recurrence Escalations

None filed this cycle — `BLG-GOV-286` already exists as the 3-cycle-recurring tracker for this problem class and is in this cycle's own scope (ST-29), so no new escalation is needed; this session's finding is folded into its acceptance criteria (see Process patch above) rather than escalated separately.

---

## Process improvements actioned this run

- `BLG-GOV-286` acceptance criteria extended in-place (within `stage4_backlog_slice.md`, this cycle's own write scope) to cover the 4th failure mode found this session. No prompt/template file was patched — the fix belongs in `release_planning_prompt.md` itself and will land when `ST-29` executes.
- `BLG-FEAT-78`'s stale `Gate criteria` field corrected in `backlog.md` (gate condition confirmed cleared, annotated with the clearing evidence and cycle reference).

---

## New files created this run

- `claude/cycles/2026-08-07__release-v8.4/run_manifest.md`
- `claude/cycles/2026-08-07__release-v8.4/state.json`
- `claude/cycles/2026-08-07__release-v8.4/release_plan.md`
- `claude/cycles/2026-08-07__release-v8.4/stage4_backlog_slice.md`
- `claude/cycles/2026-08-07__release-v8.4/stage4_issue_manifest.json`
- `claude/cycles/2026-08-07__release-v8.4/backlog_txn.json`
- `claude/cycles/2026-08-07__release-v8.4/roadmap_txn.json`
- `claude/cycles/2026-08-07__release-v8.4/cycle_summary.md`
- `claude/cycles/2026-08-07__release-v8.4/lessons_learnt.md` (this file)
- `docs/product/scope/scope--2026-08-07__release-v8.4.md`
- `docs/product/decisions/decisions--2026-08-07__release-v8.4.md`

---

## Outstanding deferred patches

None filed this cycle — see Process patch note above (folded into existing `BLG-GOV-286` scope rather than deferred).

---

## Escalations

None this cycle.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-GOV-286`'s scope (ST-29 this cycle) now needs to address 4 distinct gate-detection failure modes, not the original 3 it was filed against. | Sprint Execution should confirm the 4th failure mode (fixed-window body-bleed, both false-positive and false-negative directions) is genuinely covered by the scripted procedure's design, not just the 3 originally-named cases, before marking ST-29 complete. | Sprint Execution |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-07__release-v8.4",
  "phase": "Release",
  "filed_utc": "2026-08-07T00:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
