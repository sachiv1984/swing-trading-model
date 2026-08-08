Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Cycle: 2026-08-08__release-v8.5

# Lessons Learnt — Release Planning — v8.5

Feature / Trigger: Full-capacity, user-feature-prioritised backlog-driven release planning per explicit user instruction.
Run: 2026-08-08__release-v8.5
Reviewed by: Head of Specs Team

---

## What worked well

- The `2026-07-28__scheduled` rebalance's STEP 8.1 Option (b) equivalence continued to cleanly clear STEP -1.2 (6th consecutive release relying on the same decision, `v8.0`→`v8.5`).
- A scripted candidate-ranking pass (Priority/Type/Effort/Provisional-Target field extraction across all 269 backlog items, cross-referenced against `scan_backlog_gate_conditions.py`'s output) made the full-capacity, user-feature-first selection tractable and auditable at this backlog size, rather than relying on ad hoc reading.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Tooling/Process Gap (scripted gate-detection scan missed a genuine gate condition)

**Recurrence:** Yes — 5th distinct failure mode in the same "gate-detection procedure" problem class tracked by `BLG-GOV-286` (v8.0: gate-field-name variant; v8.1: scan line-window bounds; v8.2: gate condition embedded in `Provisional-Target` free text; v8.4: missing `---` separator between adjacent entries).

**What happened:** `scripts/scan_backlog_gate_conditions.py`'s `EMBEDDED_GATE_SIGNAL_RE` data-quality-warning pattern only matches gate-like language inside **parentheses** within a `Provisional-Target` field. `BLG-FEAT-73`'s `Provisional-Target` carries unmet-gate language (`[gate status unverified/unmet]`) inside **square brackets** — neither a formal `Gate criteria`/`Gate`/`Gate date` field nor the parenthesis-only warning regex catches it, so the script's output alone would have treated `BLG-FEAT-73` as ready/ungated. Caught by a manual full-text read of the item (consistent with this repo's standing practice of never trusting a single scan pass) before it was included in scope.

**Where in the routine:** STEP 1.3a — Gate-Detection Procedure / STEP 2 — Scope Extraction candidate verification.

**Root cause:** Same class as `BLG-GOV-286`'s four previously-named failure modes — the script's coverage of gate-language-embedded-in-free-text is pattern-specific (parentheses only) rather than exhaustive.

**Blast radius analysis:**
- What would have propagated: had the manual check not caught it, `BLG-FEAT-73` (a P1-labelled, effort-M item) would have been wrongly available for the ready pool this cycle, potentially entering scope despite its BLG-GOV-107 gate conditions remaining unmet.
- When it would have surfaced: likely at sprint execution, when the item's own acceptance criteria ("Feature does not enter sprint planning until all 3 BLG-GOV-107 gate conditions are independently reconfirmed met") would have forced a stop — but only after scope had already been committed and communicated.
- Recovery cost if uncaught: moderate (a scope revision mid-sprint-planning, plus a documented process deviation).

**Process patch:**
→ Filed as a follow-up backlog item, not resolved in-cycle (found too late in an already capacity-full session to size/sequence): `BLG-GOV-292` — extend `EMBEDDED_GATE_SIGNAL_RE` to also match bracket-delimited gate language (`\[.*(gate|gated|unmet|...)*\]`), alongside the existing parenthesis pattern.

---

## Recurrence Escalations

None filed this cycle as a *new* escalation — this is the 5th occurrence of the same problem class already tracked under `BLG-GOV-286`'s lineage (which shipped its fix in `v8.4`, ST-29, covering 4 named failure modes). Given a 5th distinct failure mode has now surfaced in the cycle immediately after that fix shipped, **this is flagged as a Carry-Forward item for the next post-ship closure to assess whether a Recurrence Escalation is now warranted** (the fix's own acceptance criteria were satisfied for the 4 modes named at the time, but the class of failure — "free-text gate language the script's own AC didn't anticipate" — continues to recur one mode at a time). See Carry-Forward below.

---

## Process improvements actioned this run

- `BLG-GOV-292` filed (see Process patch above) — not actioned in-cycle, capacity already committed.

---

## New files created this run

- `claude/cycles/2026-08-08__release-v8.5/run_manifest.md`
- `claude/cycles/2026-08-08__release-v8.5/state.json`
- `claude/cycles/2026-08-08__release-v8.5/release_plan.md`
- `claude/cycles/2026-08-08__release-v8.5/stage4_backlog_slice.md`
- `claude/cycles/2026-08-08__release-v8.5/stage4_issue_manifest.json`
- `claude/cycles/2026-08-08__release-v8.5/backlog_txn.json`
- `claude/cycles/2026-08-08__release-v8.5/roadmap_txn.json`
- `claude/cycles/2026-08-08__release-v8.5/cycle_summary.md`
- `claude/cycles/2026-08-08__release-v8.5/lessons_learnt.md` (this file)
- `docs/product/scope/scope--2026-08-08__release-v8.5.md`
- `docs/product/decisions/decisions--2026-08-08__release-v8.5.md`

---

## Outstanding deferred patches

None — see Process patch note above (filed as a standalone backlog item rather than deferred as a prompt patch).

---

## Escalations

None this cycle.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-GOV-286`'s scripted fix (shipped `v8.4`, ST-29) covered 4 named gate-detection failure modes; a 5th distinct mode (bracket-delimited embedded gate language) surfaced in the very next cycle. | Post-Ship Closure for `v8.5` (or the next `groom backlog`) should assess whether this pattern — new failure modes continuing to surface one at a time after each fix — now warrants a Recurrence Escalation per `lessons_learnt_prompt.md §6.4`, rather than another one-off follow-up item (`BLG-GOV-292`). | Post-Ship Closure |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-08__release-v8.5",
  "phase": "Release",
  "filed_utc": "2026-08-08T18:04:30Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
