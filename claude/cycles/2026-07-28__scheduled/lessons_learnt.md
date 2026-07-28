# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled rebalance, invoked immediately after a user capacity question ("should I increase my sprint capacity?")
Run: 2026-07-28__scheduled
Reviewed by: PMO Lead
Date filed: 2026-07-28
Prior cycle checked: 2026-07-27__scheduled

---

## What worked well

- **The Carry-Forward mechanism (STEP 0, §16.8) worked exactly as designed to close a genuine cross-engine gap.** `2026-07-27__release-v7.9`'s own post-ship closure flagged (Carry-Forward Item 2) that the next roadmap rebalance should attempt a genuine live SI-02 re-check rather than citing the stale 2026-07-17 field. This cycle found that a genuine live re-check had *already* happened — during that same release's own sprint execution (EPIC-08/ST-08) — but Sprint Execution has no write path to `current_roadmap.md`, so the result sat unrecorded for exactly one cycle (the expected lag) until this rebalance picked it up via the Carry-Forward read. No value changed (still 20 total / 0 linked), but the citation is now correctly dated.
- **The mandatory backlog-overlap check (idea_intake_prompt.md v2.8, added last cycle in response to a 52% duplicate rate) continued to perform as intended at a second window** — 20 of 44 initially-planned topics were caught and reframed *before* submission, confirming the check materially reduces downstream STEP 4 rejection cost rather than just adding process overhead. `BLG-GOV-278` (filed this cycle) will formally assess this after a few more windows.
- **Idea consolidation (v9.0 convention) correctly identified a genuine 2-idea overlap** (`IDEA-challenger-20260728-02` / `IDEA-pmo-lead-20260728-02`, both proposing a tracker for the same recurring direct-write-bypass pattern) and filed one item rather than two, even though the convention's stated typical range is 3–10 ideas — the rule's actual test (genuine scope overlap) was met regardless of count.
- **LP-05 candidate-gate verification correctly prevented a bad Skill-Silo pull-forward naming.** Both obvious P1 U-shaped candidates (`BLG-FEAT-73`, `BLG-FEAT-74`) were checked against their own backlog entries before being considered — both are still gate-blocked (confirmed via the same-day SI-02 re-check and a VH-effort/§13-pending status respectively) — so neither was named, and the search correctly fell through to the actual next-best candidate.

---

## Friction Log

### Friction Item 1

**Classification:** Type D — Recurring/Structural (not a single-cycle defect)

**Recurrence:** No prior cycle has named this specific pattern explicitly, though the underlying condition has been building for many consecutive cycles.

**What happened:** STEP 2.3's Horizon Review has produced an identical "no movement" finding for a long, unbroken run of scheduled rebalances. Checking `current_roadmap.md`: Arc 1 (Stock Discovery & Screening) and Arc 2 (Pre-Trade Research & Planning) are both marked "✅ Fully Complete." Arc 3 (In-Trade Risk Management) is fully shipped. Every release from roughly v6.x through v7.9 has been explicitly noted in the roadmap's own history as "backlog-driven" (e.g. v7.9: "no formal `## v7.9` roadmap section created... scoped via STEP -1.2 Option (b) equivalence... backlog-driven, 15 ungated/ready items"). The Six-Arc structure (§2a–§2c) that Horizon Review is built to walk (Now → Next → Later, arc by arc) no longer describes how releases actually get scoped — it describes a sequencing model that stopped being the operative planning mechanism several releases ago, while remaining the document Horizon Review formally checks every cycle.

**Where in the routine:** STEP 2.3 — Horizon Review (Every Run).

**Root cause:** The roadmap's Six-Arc model (§2a–§2c) and the backlog-driven release model that has actually been in use since roughly v6.x have diverged without either being formally reconciled or retired. Horizon Review still runs correctly and still finds "nothing to promote" correctly — it is not producing a wrong answer — but the check itself has become a low-information no-op relative to how the product actually gets built now.

**Blast radius analysis:**
- What would have propagated: continued "no movement" Horizon Review findings indefinitely, with the roadmap's Next/Later sections drifting further from relevance to actual release scoping, while all real prioritisation signal lives in `backlog.md`'s Priority fields instead.
- When it would have surfaced: likely only at a future `run audit` or STEP 11.4 meta-review, if someone specifically asked "does the roadmap still reflect how we plan releases?"
- Recovery cost if uncaught: low in the short term (no incorrect decision results — Horizon Review's "nothing to promote" answer is currently accurate), but the roadmap document's value as a planning artefact continues to erode the longer the divergence goes unaddressed.

**Process patch:**

→ Deferred (not action-now — this requires a substantive Head of Specs Team / Product Owner assessment of whether to refresh, restructure, or formally retire the Six-Arc model in favour of the backlog-driven model, not a quick prompt-text edit):
- File: `claude/roadmap/current_roadmap.md` (content, not `roadmap_prompt.md` logic)
- Section: §2a–§2c (Six Arcs) and §4–§5 (Next/Later horizons)
- Change: Assess whether the Six-Arc framing should be refreshed against actual v6.x–v7.9 delivery, reframed as a completed/historical model, or retired in favour of the backlog-driven planning approach that has been the de facto mechanism for many releases.
- Owner: Head of Specs Team
- Target date: `2026-07-31__scheduled` or the next STEP 11.4 meta-review, whichever comes first (meta-review is not yet due — 1 cycle since `2026-07-24__scheduled` reset, needs 3)
- Confirmed by: Not yet — deferred for explicit Head of Specs Team assessment, not applied this session.
- Prompt change log entry: N/A this cycle (no prompt file changed).

---

## Recurrence Escalations

None — Friction Item 1 is newly identified this cycle (structural/gradual, not a discrete recurring failure with a prior explicit flag).

---

## Process improvements actioned this run

None — no `roadmap_prompt.md` or other governance prompt changes applied this cycle (Friction Item 1's patch is deferred to content assessment, not a prompt-logic change).

---

## New files created this run

- `claude/cycles/2026-07-28__scheduled/run_manifest.md`
- `claude/cycles/2026-07-28__scheduled/cycle_record.md`
- `claude/cycles/2026-07-28__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-28__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260728-01.md` (committed separately, commit `cbf1042f`)

---

## Outstanding deferred patches

1 — see Friction Item 1 above (Head of Specs Team, target `2026-07-31__scheduled` or next due meta-review).

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-OPS-111` (endpoint coverage drift tracking item) still covers only 21 of 25 currently-missing endpoints — not reconciled this cycle (out of this engine's scope; carried from `2026-07-27__release-v7.9` closure). | Whichever engine next actions `BLG-OPS-111` should reconcile against the current gap before treating it as complete. | Post-Ship Closure |
| 2 | The Six-Arc roadmap model and the backlog-driven release model have diverged (Friction Item 1) — not resolved this cycle, deferred for explicit assessment. | The next roadmap rebalance or STEP 11.4 meta-review (whichever comes first) should pick this up if Head of Specs Team has not yet assessed it. | Roadmap Rebalance |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-28__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-28T22:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
