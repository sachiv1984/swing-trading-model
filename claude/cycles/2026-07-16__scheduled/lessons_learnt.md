**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Filed
**Report Date:** 2026-07-16

---

# Lessons Learnt — Roadmap Rebalance 2026-07-16__scheduled

Feature / Trigger: N/A — scheduled review
Run: 2026-07-16__scheduled
Reviewed by: PMO Lead
Date filed: 2026-07-16
Prior cycle checked: 2026-07-15__scheduled

---

## What worked well

- **The live production-API SI-02 re-check produced its 5th consecutive byte-identical result** — continued confirmation that the mechanism correctly distinguishes "confirmed still true" from "not re-checked," at negligible cost (2 free-tier API calls).
- **This cycle's own idea intake surfaced a genuine, unprompted 2nd data point for both outstanding STEP -1.5 deferred patches** — the Challenger and Head of Specs Team submissions independently proposed resolving the STEP 0.C exception now, and this cycle's STEP 3.1 assessment independently hit the "2nd occurrence" trigger the prior cycle's deferred patch named — both closed this run rather than carried further, without needing a dedicated meta-review cycle to surface them.
- **The Product Value Alert and Skill-Silo worsening, arriving in the same cycle, resolved cleanly against already-existing scope** — no new backlog item or scope compromise was needed to satisfy either mandate, because the Now horizon already carried 3 genuine U-items and this cycle's own idea intake surfaced 4 more, all before the alerts fired. This is a case where prior cycles' groundwork (naming `BLG-FE-109/110/111` at `2026-07-15__scheduled`) paid forward.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** Yes — carried across 6 consecutive cycles (`2026-07-08__scheduled` through `2026-07-15__scheduled`, plus this cycle).

**What happened:**
The STEP 0.C abbreviated-manifest exception (a proposed lightweight-manifest carve-out for "0 active initiatives + no backlog/register change since prior scheduled run") never once recurred in 6 tries — every single scheduled cycle in that window had a backlog and/or register change, because STEP -1.6 idea intake itself modifies the register on effectively every cycle it fires (which is nearly all of them, since the register is emptied by ideas-housekeeping at every post-ship close). The condition as stated describes a state that this system's cycle rhythm structurally cannot produce.

**Where in the routine:**
STEP -1.5 — Prior Cycle Outstanding Actions / STEP 0.C — Run Tier Determination.

**Root cause:**
The condition was designed around a hypothetical "quiet" scheduled cycle that assumed idea intake might sometimes not fire, or the register might sometimes already hold ≥20 open ideas carrying over untouched. In practice, idea intake fires on nearly every cycle (register is emptied at each post-ship close) and always appends new rows — so "no register change" is not a realistic gate condition for this system, only for a hypothetically different cadence.

**Blast radius analysis:**
- What would have propagated: a 7th, 8th, Nth silent carry, with no additional information gained each time — the condition was not converging toward recurrence, it was structurally prevented from recurring.
- When it would have surfaced: eventually as a meta-review pattern (Type A recurring ≥2 cycles), but this cycle's own STEP -1.5 disposition caught it first via the Stale Condition-Gated Defer advisory (6-carry threshold) introduced at `2026-07-13__scheduled`.
- Recovery cost if uncaught: low (no incorrect decision resulted from carrying it), but a continuing drag on run-manifest verbosity and a live example of a deferred-patch mechanism not being self-correcting.

**Process patch:**

→ Immediate action this run: **retire the proposed STEP 0.C abbreviated-manifest exception.** It was never implemented as prompt text (tracked only via the lessons-learnt carry-forward chain), so no `roadmap_prompt.md` version bump or revert is needed — retirement is simply "stop carrying this in future `run_manifest.md`/`lessons_learnt.md` files." Rationale: 6 consecutive non-recurrences is sufficient evidence the condition does not describe an achievable state for this system's actual cycle rhythm (idea intake empties and refills the register on nearly every scheduled cycle by design). If a future cycle genuinely has 0 active initiatives, an empty idea intake, and no backlog change, the existing Standard/Lightweight tier logic already handles it — no separate exception is needed.
- Confirmed by: Head of Specs Team.
- Prompt change log entry: Not required (no prompt text was ever written for this proposal — nothing to record a version bump against).

---

### Friction Item 2

**Classification:** Type B — Semantic Mismatch

**Recurrence:** Yes — 2nd consecutive cycle using the grep-based structural heuristic for STEP 3.1 (first at `2026-07-15__scheduled`, deferred pending this confirming occurrence).

**What happened:**
`2026-07-15__scheduled`'s lessons learnt explicitly named "a 2nd occurrence" as the trigger to codify a scale-appropriate STEP 3.1 methodology rather than re-defer. This cycle (319 active items) is that 2nd occurrence — the manual per-item read remains impractical at this scale, and the same grep-based heuristic was used again.

**Where in the routine:**
STEP 3.1 — Actionable Backlog Assessment.

**Root cause:**
Document staleness — the original STEP 3.1 instruction assumed manual classification is always feasible; it had not been updated to name an explicit scale threshold or an alternative structured method.

**Blast radius analysis:**
- What would have propagated: a 3rd, 4th ad hoc re-application of an undocumented heuristic, risking silent drift in exactly which keywords/patterns are used to split T/D/L, making cross-cycle A% figures progressively less comparable without anyone deciding that was acceptable.
- When it would have surfaced: the next cross-cycle trend analysis (e.g. a future meta-review) attempting to compare A% figures across the manual-era and heuristic-era cycles.
- Recovery cost if uncaught: low-medium — an interpretation/trust issue in a diagnostic metric, not a decision-correctness issue on its own.

**Process patch:**

→ Immediate patch applied this run:
- File: `claude/system/roadmap_prompt.md`
- Section: STEP 3.1 Actionable Backlog Assessment
- Change: added a "Scale-appropriate methodology" subsection — manual read below ~150 active items; above that, a codified structural heuristic (gate-criteria-field presence for A/gated; keyword-pattern scan of gate-criteria text for T/D/L). Requires recording which method was used in `run_manifest.md`.
- Version: 9.0 → 9.1
- Confirmed by: Head of Specs Team
- Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

## Recurrence Escalations

None — both friction items above were expected, planned resolutions of deliberately-deferred patches at their own named trigger points (6-carry threshold; 2nd occurrence), not unresolved outstanding actions requiring escalation.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|--------------------------|
| `claude/system/roadmap_prompt.md` | STEP 3.1 | Scale-appropriate A/T/D/L methodology codified | 9.0→9.1 | Yes |
| *(no file — proposal only)* | STEP 0.C / STEP -1.5 | Abbreviated-manifest exception retired (6 non-recurrences) | N/A | Not required |

---

## New files created this run

- `claude/cycles/2026-07-16__scheduled/run_manifest.md`
- `claude/cycles/2026-07-16__scheduled/cycle_record.md`
- `claude/cycles/2026-07-16__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-16__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260716-01.md` (committed separately by the idea intake subroutine, commit `38593511`)

---

## Outstanding deferred patches

None. Both patches carried into this cycle from `2026-07-15__scheduled` were resolved this run (one retired, one codified).

---

## Escalations

One non-blocking advisory raised and resolved within this same cycle (STEP 0.C Stale Condition-Gated Defer — see Friction Item 1). One pre-existing open escalation not owned by this engine remains: Head of Specs Team day-range effort mandate formalisation, deadline 2026-07-17 (from `2026-07-15__release-v7.2` `lessons_learnt_closure.md` Carry-Forward #2) — not yet due, no action required from this engine.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The Product Value Alert (0.28) and Skill-Silo worsening (66.7%) both fired this cycle but were fully satisfiable from already-existing Now-horizon/backlog scope (`BLG-FE-109/110/111/115/116/117/118`) with no fresh action needed. The next `plan release` invocation should treat these 7 items as the mandatory anchor scope — sequencing per the Head of UX & Design's `2026-07-15__scheduled` advisory (`BLG-FE-55` first, still applicable by extension) plus the 4 new pre-implementation readiness passes (`BLG-SPEC-91-94`) as fast precursors. | Release Planning | Release Planning |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-16__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-16T09:30:00Z",
  "friction_item_count": 2,
  "action_now_count": 2,
  "deferred_count": 0,
  "escalation_count": 1,
  "overdue_patches": 0,
  "status": "Complete"
}
```
