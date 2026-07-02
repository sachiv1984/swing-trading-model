**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-07-02__scheduled
**Last Updated:** 2026-07-02

---

# Lessons Learnt — Roadmap Rebalance 2026-07-02__scheduled

Feature / Trigger: N/A — scheduled rebalance
Run: 2026-07-02__scheduled
Reviewed by: PMO Lead; Head of Specs Team
Date filed: 2026-07-02
Prior cycle checked: 2026-07-01__scheduled

---

## What worked well

1. **The STEP 11.2 deferred patch resolved cleanly on its own named target.** Filed at `2026-07-01__scheduled` with Target = "next `run roadmap` scheduled cycle" (a cycle-based target, not a bare release version), it was unambiguously due this cycle and was applied action-now without any STEP -1.5 ambiguity — demonstrating that the very fix the patch itself codifies (cycle_id/date targets over release-version targets) works as intended.

2. **All three FI-P3-01/FI-P3-02/FI-P4-01 recurrence escalations closed cleanly.** Verified via `claude/cycles/2026-07-02__release-v6.4/qa_evidence_EPIC-02.md` (AC-02/AC-03/AC-05 all Pass) and `lessons_learnt_closure.md` (LP-01 validated pattern). No further carry-forward needed.

3. **The idea intake window processed a large volume (63 ideas: 44 new + 19 terminal) without any Facilitator queue-count discrepancy** — STEP 4.4's mandatory row-count check passed on the first pass.

4. **STEP 8.0 correctly found zero fast-track items** rather than forcing a strained match — the only P1 item present (`BLG-SPEC-35`) was correctly re-confirmed as pre-work, not a correctness bug, consistent with the prior cycle's finding.

---

## Friction Log

---

### Friction Item 1

**Classification:**
- Type D — Cognitive Fatigue: A detail was missed due to an incomplete verification step, not a missing rule

**Recurrence:** No — first identified this cycle, though the underlying rule (STEP 4.0) has existed since v5.0.

**What happened:**
This cycle's STEP 4.0 gate-condition re-check found that `BLG-GOV-131` (referenced by `IDEA-challenger-20260626-02`'s Park Rationale) had in fact shipped in v6.1 (2026-06-23) — but the prior cycle (`2026-07-01__scheduled`) had recorded it as "still active/unshipped" in its own STEP 4.0 table. The prior cycle's check appears to have grepped only `backlog.md` (the active backlog), found no match (correctly, since the item had already archived), and stopped there rather than confirming absence via `backlog_archive.md` before concluding "not shipped."

**Where in the routine:**
STEP 4.0 — Gate-Condition Re-Check, at the originating cycle (`2026-07-01__scheduled`); caught this cycle by a more thorough version of the same check.

**Root cause:**
Process gap — STEP 4.0's instruction said "check whether the referenced item has shipped (in `backlog.md` as COMPLETE...)" without an explicit instruction to check `backlog_archive.md` when the item is absent from `backlog.md` altogether. Absence from the active backlog is ambiguous — it could mean "not yet added" or "already shipped and archived" — and the prior wording didn't disambiguate.

**Blast radius analysis:**
- What would have propagated: the idea would have continued to silently re-park indefinitely (it was already at its 3-cycle terminal point this cycle) with a rationale that no longer reflected the real backlog state, potentially masking that its underlying need (a governance-overhead enforcement mechanism) was already substantially addressed by the live STEP 7.1 Skill-Silo Alert.
- When it would have surfaced: possibly never on its own — would require a manual audit of parked-idea rationales against the archive to notice.
- Recovery cost if uncaught: low-medium — the idea itself was not high-stakes, but the pattern (silent staleness in gate-condition checks) could recur with a higher-stakes idea.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 4.0 (Gate-Condition Re-Check)
  - Change: explicit two-step check added — grep `backlog.md`; if the referenced item is absent, grep `backlog_archive.md` before concluding "not shipped."
  - Version: 7.9 → 8.0
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes (bundled with Friction Items 2 and 3 below, same commit)

---

### Friction Item 2

**Classification:**
- Type C — Dependency Stall: A gate mechanism's correction assumption was implicit and unvalidated

**Recurrence:** No — first identified this cycle (the underlying mechanism, STEP 7.1, has fired for several consecutive cycles, but this is the first time its single-item correction assumption was explicitly checked against outcome data).

**What happened:**
The `2026-07-01__scheduled` cycle's `lessons_learnt_closure.md` carry-forward item #4 asked this cycle to confirm whether bundling `BLG-FEAT-54` (a single U-story pull-forward) had brought the Skill-Silo rolling-3-cycle average back under the 40% ceiling. It had not — the average rose from 53.2% to 64.8%, because the two other cycles in the new 3-cycle window (v6.3, v6.4) were both unusually debt/governance-heavy (86.7% and 76.9% respectively). STEP 7.1's pull-forward mechanism implicitly assumed a single U-item per cycle is sufficient correction; this cycle's data shows that assumption does not hold when surrounding cycles are heavily governance-weighted.

**Where in the routine:**
STEP 7.1 — Skill-Silo Alert (mandatory pull-forward scan)

**Root cause:**
Template omission — the pull-forward mechanism's wording did not distinguish between "present a candidate" (which it does correctly) and "the ceiling will actually correct" (which it doesn't guarantee and previously wasn't flagged as uncertain).

**Blast radius analysis:**
- What would have propagated: future cycles could keep presenting a single pull-forward candidate each time, satisfying the letter of STEP 7.1 without the ceiling ever actually correcting, since one U-item cannot outweigh two heavy governance cycles.
- When it would have surfaced: at a future meta-review, once the Alert had fired for several more consecutive cycles with no visible improvement.
- Recovery cost if uncaught: medium — release planning could continue treating the Alert as "handled" each cycle without addressing the structural imbalance.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 7.1 (Skill-Silo Alert)
  - Change: wording added clarifying that a single U-item pull-forward is not guaranteed to correct the ceiling across a heavy governance/debt window, with the v6.4 bundling outcome cited as the concrete example; PO advised to consider multiple U-items after 2+ consecutive Alert cycles.
  - Version: 7.9 → 8.0 (bundled with Friction Items 1 and 3)
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes

---

### Friction Item 3

**Classification:**
- Type B — Semantic Mismatch: The U/G/D/P story classification used by STEP 2.4 is not recorded anywhere at the time stories ship — it is reconstructed retrospectively from changelog prose each time the diagnostic runs.

**Recurrence:** Not checkable — this is the first cycle to explicitly note the reconstruction as a source of variance (no prior lessons_learnt.md flagged it), though the diagnostic itself has existed since v7.4.

**What happened:**
Computing this cycle's `user_value_ratio` required re-reading `docs/product/changelog.md` for the last 5 cycles and judgment-classifying each story as U/G/D/P from its prose description — v6.2's per-story split in particular required estimating a 9-story breakdown across two EPICs from a changelog that only explicitly enumerates 4 of those 9 stories by ID. A different reviewer re-running this diagnostic on the same 5 cycles could plausibly produce a materially different ratio.

**Where in the routine:**
STEP 2.4 — Product Value Ratio Diagnostic

**Root cause:**
Missing artefact — no canonical field records a story's U/G/D/P classification at the point it ships (post-ship closure does not currently tag this).

**Blast radius analysis:**
- What would have propagated: a future rebalance's Product Value Alert could fire or fail to fire based on reviewer judgment variance rather than a stable, auditable figure — undermining the diagnostic's credibility as a trigger for the Challenger's Product Velocity Concern exception.
- When it would have surfaced: the next time two different sessions computed the ratio for an overlapping cycle window and got different numbers.
- Recovery cost if uncaught: medium — could produce an inconsistent Alert/no-Alert flip-flop across cycles that isn't driven by real changes in product value delivery.

**Process patch:**

→ Deferred patch (a change to `post_ship_closure.md` is a larger, different-engine change than the three roadmap_prompt.md patches already bundled this run — deferring keeps this patch's own review scope clean):
  - File: `claude/system/post_ship_closure.md`
  - Section: the changelog-writing step (currently records "Tech backlog items shipped" per story with a one-line description)
  - Change required: tag each shipped story with its U/G/D/P classification inline (e.g., `[U]`, `[G]`, `[D]`, `[P]` prefix) at the point the changelog entry is written, so `roadmap_prompt.md` STEP 2.4 can read a stable classification instead of re-deriving it from prose each time.
  - Owner: Head of Specs Team
  - Target: `2026-07-05__scheduled` (or the next roadmap rebalance, whichever comes first — a concrete cycle_id per this cycle's own STEP 11.2 patch)

---

## Recurrence Escalations

None this cycle — all three recurrence escalations carried from `2026-07-01__scheduled` (FI-P3-01, FI-P3-02, FI-P4-01) confirmed Resolved (see "What worked well" #2).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/roadmap_prompt.md` | STEP 11.2 | Deferred-patch Target fields must name a cycle_id/date, not a bare release version (Friction Item 2 from `2026-07-01__scheduled`) | v7.9→v8.0 | Yes |
| `claude/system/roadmap_prompt.md` | STEP 4.0 | Two-step gate-condition check — `backlog.md` then `backlog_archive.md` before concluding "not shipped" (this cycle's Friction Item 1) | v7.9→v8.0 (same bump) | Yes |
| `claude/system/roadmap_prompt.md` | STEP 7.1 | Wording clarifying single-U-item pull-forward is not guaranteed to correct the ceiling (this cycle's Friction Item 2) | v7.9→v8.0 (same bump) | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §14 (Version field, Roadmap Engine Source, Change Log) | Version/source rows updated to v8.0; also corrected a stale §14-internal Version field (was 4.69 while doc header/Change Log had reached 4.71) | v4.71→v4.72 | Yes |

---

## New files created this run

- `claude/cycles/2026-07-02__scheduled/run_manifest.md`
- `claude/cycles/2026-07-02__scheduled/cycle_record.md`
- `claude/cycles/2026-07-02__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-02__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260702-01.md`

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/post_ship_closure.md` | Changelog-writing step | Tag each shipped story with U/G/D/P classification inline at ship time (Friction Item 3) | Head of Specs Team | `2026-07-05__scheduled` or next roadmap rebalance |

---

## Escalations

None this cycle.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Skill-Silo rolling-3-cycle average worsened to 64.8% despite a single U-item pull-forward at v6.4 | `plan release v6.5` should prioritise more than one user-facing item if the ceiling is to be meaningfully corrected, not repeat the single-item pattern | Release Planning |
| 2 | Backlog Accessibility Warning triggered for the first time (A=28% < 30% floor), driven partly by this cycle's 16 gate-conditional additions from the 3-cycle-cap idea disposition | `groom backlog` should review whether any newly-added gate-conditional items are, on reflection, better classified as long-horizon and candidates for consolidation | Backlog Management |

---

## STEP 11.4 — Meta-Review

**Trigger:** 2 cycles since last meta-review (`2026-06-26__scheduled`). Not due — threshold is 3.

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-02__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-02T22:00:00Z",
  "friction_item_count": 3,
  "action_now_count": 2,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
