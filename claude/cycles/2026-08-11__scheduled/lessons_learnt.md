# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled rebalance, invoked by the user (`run roadmap --scheduled`, confirmed as `--reason "scheduled"` via clarifying question per the Invocation Rule hard gate)
Run: 2026-08-11__scheduled
Reviewed by: PMO Lead
Date filed: 2026-08-11
Prior cycle checked: 2026-07-28__scheduled

---

## What worked well

- **The gate-verification re-scan (LP-05) caught its own first-pass error before any candidate was named.** An automated `awk`-based gate-detection script (built ad hoc this session, not a pre-existing tool) had a blank-line-boundary bug that caused several P3 `Product Feature / Analytics` items (`BLG-FEAT-26/30/31/32/34/35`) to be misclassified as ungated — their `**Gate criteria:**` field appears after a blank line the script's record boundary treated as terminal. Direct inspection of each candidate before naming it (the same discipline LP-05 already mandates for P1/P2 candidates) caught this before it propagated into a bad candidate naming, and in fact turned up a genuine positive: `BLG-FEAT-32`'s gate is fully cleared and had simply never been promoted. This is a stronger confirmation of LP-05's value than any prior cycle — the check didn't just prevent naming a still-gated item, it surfaced a wrongly-gated one.
- **The combined Product Value Alert + Skill-Silo mandatory-pull-forward response worked as a single coherent Product Owner decision rather than two separate, potentially conflicting ones.** Both triggers this cycle trace to the same root cause (0/11 linked trade plans), which let the response name one structural fix (`BLG-BE-91`, P1) addressing both, rather than two disconnected pull-forward actions.
- **The idea consolidation convention (v9.0) correctly identified 3 genuine overlaps this window** (`BLG-BE-91`, `BLG-SPEC-124`, `BLG-GOV-303`), each explicitly cross-referencing a companion submission in its own text — the clearest signal for genuine overlap this convention has seen yet, not merely adjacent topics.
- **STEP -1.5's "second consecutive cycle" carry-forward rule correctly avoided a false OVERDUE classification.** The Six-Arc-model deferred patch's original target (`2026-07-31__scheduled`) never materialised as an actual cycle (no scheduled rebalance ran between `2026-07-28` and this cycle), and the rule correctly recognised this as the *first* re-check, not a second missed one — preventing an unwarranted escalation to Head of Specs Team for a patch that has genuinely only been reviewed once.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Execution Error (session-scoped tooling, not a governance-prompt defect)

**Recurrence:** First occurrence — no prior cycle has used an automated gate-detection script of this shape (prior cycles' STEP 3.1/STEP 7.1 candidate scans were described as manual/structural-heuristic reads, not a purpose-built script).

**What happened:** An ad hoc `awk` script built this session to classify backlog items as gated/ungated used blank-line boundaries to delimit a record, but several items' `**Gate criteria:**` field appears *after* a blank line separating it from the `**Provisional-Target:**` field — outside the script's record window. This caused a first-pass false "ungated" classification for 6 P3 `Product Feature / Analytics` items.

**Where in the routine:** STEP 7.1 — Skill-Silo Alert candidate search (mandatory this cycle, given the 3rd-consecutive-worsening trigger).

**Root cause:** Backlog entries are not formatted with a single unbroken block per item — several use a blank line between the metadata block (Priority/Type/Owner/Source/Effort/Provisional-Target) and the `**Gate criteria:**` line, which sits closer to the `**Problem**` section. A record-boundary heuristic keyed on "first blank line after the metadata header" does not account for this.

**Blast radius analysis:**
- What would have propagated: naming an already-gated item as an ungated pull-forward candidate — exactly the class of error `shared_standards.md` LP-05 exists to prevent, and exactly the class of error `2026-07-03__scheduled` made with `BLG-FEAT-52` before LP-05 existed.
- When it would have surfaced: likely at the next `plan release` invocation, when Release Planning's own gate-verification step re-checked the named candidate and found it still gated — the same catch-downstream pattern documented for the `BLG-FE-128` incident at `2026-07-27__release-v7.9`.
- Recovery cost if uncaught: low-to-moderate — caught within this same session before any candidate was named in a written artefact, so no downstream correction was needed. The near-miss is the finding, not an actual propagated error.

**Process patch:**

→ Action-now (applied this session, not deferred): this run's own gate-verification pass used direct inspection (reading each candidate's full entry) rather than trusting the script's output, per LP-05's existing requirement — so the immediate risk was already closed by following the existing rule correctly. No `roadmap_prompt.md` logic change is needed; the existing LP-05 mandatory-direct-inspection requirement is sufficient and worked as designed. Recorded here as a friction item because the *near-miss* is instructive, not because the governing rule needs to change.

- File: N/A — no prompt file requires a change.
- Confirmed by: Head of Specs Team (reviewed this cycle's STEP 7.1 methodology note in `run_manifest.md`/`cycle_record.md`).
- Prompt change log entry: N/A this cycle (no prompt file changed).

---

## Recurrence Escalations

None — Friction Item 1 is a first occurrence, and its own mitigation (direct inspection per existing LP-05) already worked without requiring a new rule.

---

## Process improvements actioned this run

None — no `roadmap_prompt.md` or other governance prompt changes applied this cycle.

---

## New files created this run

- `claude/cycles/2026-08-11__scheduled/run_manifest.md`
- `claude/cycles/2026-08-11__scheduled/cycle_record.md`
- `claude/cycles/2026-08-11__scheduled/cycle_summary.md`
- `claude/cycles/2026-08-11__scheduled/lessons_learnt.md` (this file)

---

## Outstanding deferred patches

1 — Six-Arc roadmap model vs backlog-driven delivery divergence (carried from `2026-07-28__scheduled`, this cycle's 1st re-check — not OVERDUE). Owner: Head of Specs Team. New target: next `STEP 11.4` meta-review (due after this cycle's count reaches 2 of 3) or the next scheduled rebalance if it independently picks it up first.

---

## Escalations

None new this cycle. (2 cross-routine escalations found via the STEP -1.7 due-date scan — `BLG-GOV-292`, `DEV-EPIC02-ST03-01` — were both already resolved prior to this session; see `run_manifest.md`.)

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The Six-Arc roadmap model and the backlog-driven release model remain unreconciled (Friction Item 1 from `2026-07-28__scheduled`) — this cycle's 1st re-check found neither trigger condition had fired, so it was carried forward without escalation. | The next `STEP 11.4` meta-review (due once `rebalance_cycles_since_meta_review` reaches 3) or the next scheduled rebalance should pick this up if Head of Specs Team has not yet assessed it by then. | Roadmap Rebalance / Head of Specs Team |
| 2 | STEP 7.2 (Cross-Role Workload Balance Check) was deliberately not recomputed this cycle (advisory-only, deferred to avoid a redundant `sprint_backlog.md` read across 3 consecutive cycles with no material composition change expected). | The next roadmap rebalance that does recompute STEP 7.1 in full should also recompute STEP 7.2, so this advisory does not go more than 2 cycles without a fresh reading. | Roadmap Rebalance |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-11__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-08-11T00:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
