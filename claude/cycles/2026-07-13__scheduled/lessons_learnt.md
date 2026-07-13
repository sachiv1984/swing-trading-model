**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Filed
**Report Date:** 2026-07-13

---

# Lessons Learnt — Roadmap Rebalance 2026-07-13__scheduled

Feature / Trigger: N/A — scheduled review
Run: 2026-07-13__scheduled
Reviewed by: PMO Lead
Date filed: 2026-07-13
Prior cycle checked: 2026-07-12__scheduled

---

## What worked well

- **STEP 8.0's Production Correctness Fast-Track fired for the first time in this engine's run history**, and did exactly what it was designed to do: two fresh P1 nightly-backtest data-integrity bugs, confirmed feeding the user-visible Strategy Benchmark page, were promoted directly into a new v7.1 Now-horizon section ahead of any governance/debt competition for the slot — resolving the "empty Now horizon" pattern that had persisted through 2 prior scheduled cycles' Option (b) deferrals, without requiring a separate debate.
- **The idea-consolidation approach for overlapping submissions** (19 of 44 ideas, converging on 3 newly-shipped v7.0 features, consolidated into 4 backlog items rather than 19 near-duplicates) kept the backlog additions proportionate to genuine scope rather than mechanically 1:1 with submission count, while preserving full provenance via each item's Source field.
- **SI-02's live re-check produced a byte-identical result to the prior cycle** (all three conditions unchanged) — confirmed the re-check mechanism correctly reports "no change" rather than manufacturing false movement, which matters for trusting the mechanism precisely when nothing *has* changed.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** Related to, but not identical to, `2026-07-12__scheduled` Friction Item 2 (which addressed the "outside write scope" excuse for OVERDUE patches). This item addresses a different gap in the same STEP -1.5 rule: no provision existed for *condition-gated* (as opposed to *date-gated*) deferred patches, which the OVERDUE mechanism's cycle-count language does not cleanly fit. Marking **No** — distinct root cause, same rule section.

**What happened:**
The STEP 0.C abbreviated-manifest exception deferred patch reached its 4th consecutive carry this cycle (originated `2026-07-08__scheduled`; carried at `2026-07-10__scheduled`, `2026-07-12__scheduled`, now `2026-07-13__scheduled`). By STEP -1.5's literal text ("second consecutive cycle carrying this patch → classify OVERDUE"), this should arguably have triggered an OVERDUE halt at its very first carry. It never did, across any of the three prior cycles — each instead recorded `overdue_patches: 0` and treated the carry as legitimate because the trigger condition genuinely had not recurred. This session had to re-derive that same judgment call from scratch, reading the raw rule text and reconciling it against observed precedent, because the exemption had never been written down.

**Where in the routine:**
STEP -1.5 — Prior Cycle Outstanding Actions (Prompt patch confirmation sub-section).

**Root cause:**
Template omission — the OVERDUE rule was written with only one shape of deferred patch in mind (a specific edit that should have been applied by now and wasn't), and never anticipated a patch whose "not yet applied" state is because its own trigger condition hasn't occurred, which is a legitimately different failure mode.

**Blast radius analysis:**
- What would have propagated: continued cycle-by-cycle re-litigation of the same judgment call, with a nonzero chance a future session reads the rule more literally and halts a cycle unnecessarily over a condition that simply hasn't recurred yet.
- When it would have surfaced: the next time a new hire / fresh session encounters this exact defer without the benefit of this conversation's accumulated precedent-reading.
- Recovery cost if uncaught: low — worst case is a spurious halt requiring a quick Head of Specs Team override, not data loss or an incorrect roadmap write.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP -1.5 Prior Cycle Outstanding Actions
  - Change: added a "condition-gated defer exemption" clause — a deferred patch whose Target names a recurrence condition (not a cycle_id/date) is exempt from the cycle-count OVERDUE mechanism; a new 6+-consecutive-carry "Stale Condition-Gated Defer" advisory applies instead.
  - Version: 8.7 → 8.8
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

### Friction Item 2

**Classification:** Type A — Governance Drift

**Recurrence:** Not checkable against prior friction logs directly (this is a *discovery*, not a repeat of a previously-logged friction item) — but it is the **5th recurrence of an already-named pattern**: `OPERATIONAL_GUIDE.md` §14's own Change Log explicitly documents 4 prior occurrences of this exact class (header drift ahead of/behind the §14 table), including a dedicated drift-prevention note added at v4.85. Marking **Yes — recurring pattern**, though not a repeat of a specific unresolved prior-cycle item.

**What happened:**
While applying this cycle's own `roadmap_prompt.md` version bump, `OPERATIONAL_GUIDE.md` §14's table was found to read `Version | 4.91` / `Last Updated | 2026-07-10` — despite the document's own top header already reading `4.92`/`2026-07-12`, and the Change Log's own top entry confirming a `4.91→4.92` bump had already happened at the `2026-07-12__scheduled` cycle. The §14 table's Version/Last Updated *value row* itself had simply never been edited during that prior bump, even though every other field it should have touched (Roadmap Engine Source, Artefact Register row) was correctly updated. This is despite the table carrying its own explicit drift-prevention instruction (added v4.85) specifically warning that this exact field had drifted 4 times before.

**Where in the routine:**
STEP 12 / Governance File Edit Checklist (CLAUDE.md §6) — specifically the "update OPERATIONAL_GUIDE.md §14 governance table" step.

**Root cause:**
Process gap — the existing drift-prevention note instructs reading the table's row "before bumping" the *top header*, but does not itself instruct verifying that the table's *own* Version/Last Updated row was actually edited in the same pass as the engine-specific rows (Roadmap Engine Source, Artefact Register) — it's possible to update every specific engine row correctly and still leave the table's own summary Version/Last Updated stale, exactly as happened here.

**Blast radius analysis:**
- What would have propagated: `OPERATIONAL_GUIDE.md` §14 continuing to report a stale document version, undermining confidence in the table as a source of truth for "when was this last touched" even when the per-engine rows below it are accurate.
- When it would have surfaced: the next `governance-drift` skill invocation, or the next STEP 11.4 meta-review, which would likely re-flag this as a 6th recurrence rather than catching it live.
- Recovery cost if uncaught: low (single-table field fix) but compounding — each uncaught recurrence erodes trust in the table's self-reported freshness.

**Process patch:**

→ Deferred patch (cannot apply this run — requires broader §14 process redesign, not a one-line text edit):
  - File: `claude/system/OPERATIONAL_GUIDE.md`
  - Section: §14 Playbook Governance, Change Log drift-prevention note
  - Change required: extend the existing drift-prevention note to explicitly require, as a distinct verification step, confirming the table's own `Version`/`Last Updated` value row (not just the per-engine rows) was actually edited in the same pass as any per-engine version bump — e.g. a one-line "before closing out this edit, re-read this table's Version/Last Updated row and confirm it matches the top document header" checklist item.
  - Owner: Head of Specs Team
  - Target: next scheduled rebalance or the next STEP 11.4 meta-review (due at cycle 3 from `2026-07-10__scheduled` reset), whichever comes first

---

### Friction Item 3

**Classification:** Type C — Dependency Stall

**Recurrence:** No — first occurrence of this specific gap.

**What happened:**
STEP 4.1/4.2 define exactly four idea dispositions (Advance, Park, Backlog (gate-conditional), Reject) with no formal option for consolidating multiple overlapping submissions into a single backlog item. This cycle's window summary itself flagged 19 of 44 submissions as converging on 3 newly-shipped features, explicitly asking STEP 4/5 to consolidate rather than debate independently — but the routine had no documented procedure for how to do so (how many ideas may be merged, what the resulting item's Source field should look like, whether register rows should cross-reference each other). This session invented a convention (list every contributing Idea ID in the new backlog item's Source field; leave each register row's Step 5 column pointing at the consolidated item) without a governing rule to follow.

**Where in the routine:**
STEP 4.1/4.2 — Per-Idea Classification and Document Management.

**Root cause:**
Process gap — the routine was designed assuming a roughly 1:1 idea-to-backlog-item mapping, which has held in most prior cycles but broke down this cycle specifically because the window's submissions clustered heavily around 3 shared features (itself a natural consequence of 22 role-perspectives independently reacting to the same freshly-shipped release).

**Blast radius analysis:**
- What would have propagated: a future cycle facing the same clustering pattern might either (a) mechanically file 15+ near-duplicate single-source items, inflating backlog noise, or (b) consolidate inconsistently (different Source-field conventions, inconsistent register cross-referencing) across different sessions, making the register harder to audit.
- When it would have surfaced: the next `groom backlog` run, if it tried to reconcile Source-field conventions across cycles and found this cycle's ad hoc format inconsistent with a future session's different ad hoc format.
- Recovery cost if uncaught: low-medium — a documentation/consistency issue, not a data-loss or incorrect-decision risk.

**Process patch:**

→ Deferred patch (cannot apply this run — the consolidation convention used this cycle should be validated against at least one more clustering event before being codified as a permanent rule):
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 4.2 Document Management (Apply Before STEP 5)
  - Change required: add a documented "Idea Consolidation" convention — when N submissions from the current window converge on the same feature/problem area (as flagged by the window summary's own overlap notes), the Facilitator may file one consolidated backlog item rather than N separate ones, provided the item's Source field lists every contributing Idea ID and each register row's Step 5 column names the consolidated item explicitly.
  - Owner: Head of Specs Team
  - Target: next scheduled rebalance where a similar clustering pattern (5+ overlapping submissions on one feature area) recurs, to confirm the convention generalises before hard-coding it

---

## Recurrence Escalations

None — Friction Item 1 is a newly-observed gap (not a repeat of a specific unresolved prior-cycle outstanding action); Friction Item 2, while the 5th instance of a *named pattern*, was fixed live this cycle rather than left unresolved, so it is not an open recurrence requiring escalation; Friction Item 3 is newly-identified.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|--------------------------|
| `claude/system/roadmap_prompt.md` | STEP -1.5 | Condition-gated defer exemption clause | 8.7→8.8 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §6/§13/§14 + Change Log | Version-reference sync for the above patch; also corrected the pre-existing §14 table Version/Last Updated drift found this cycle (5th recurrence of the named pattern) | 4.92→4.93 | Yes |

---

## New files created this run

- `claude/cycles/2026-07-13__scheduled/run_manifest.md`
- `claude/cycles/2026-07-13__scheduled/cycle_record.md`
- `claude/cycles/2026-07-13__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-13__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260713-01.md` (committed separately by the idea intake subroutine)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|------------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 0.C (Run Tier Determination) | Abbreviated-manifest exception for "0 active initiatives + no backlog/register change since prior scheduled run" (carried from `2026-07-08__scheduled`; 4th consecutive carry, condition not recurred — now explicitly exempted from the cycle-count OVERDUE mechanism per Friction Item 1's patch, subject to the new 6+-carry Stale Condition-Gated Defer advisory) | Head of Specs Team | Next scheduled rebalance where the condition genuinely recurs, or the 6th consecutive carry (whichever first) |
| `claude/system/OPERATIONAL_GUIDE.md` | §14 Change Log drift-prevention note | Extend the note to require verifying the table's own Version/Last Updated row was actually edited alongside any per-engine version bump, not just the per-engine rows | Head of Specs Team | Next scheduled rebalance or next STEP 11.4 meta-review (due at cycle 3 from `2026-07-10__scheduled` reset) |
| `claude/system/roadmap_prompt.md` | STEP 4.2 | Document an "Idea Consolidation" convention for clustered overlapping submissions | Head of Specs Team | Next scheduled rebalance where a 5+-submission clustering pattern recurs |

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The Production Correctness Fast-Track fired for the first time this cycle and directly resolved the empty-Now-horizon pattern — the two mandatory items (`BLG-BE-59`, `BLG-BE-60`) are still only backlog-level entries with inline estimates, not a scoped release plan. | The next `plan release` invocation should treat these two items as the mandatory anchor scope for v7.1, consistent with how the last 3 cycles' pull-forward candidates became de facto release scope. | Release Planning |
| 2 | 19 of this cycle's 44 idea submissions converged on 3 features that shipped in the immediately-prior release (v7.0) — a "post-ship hardening pass" pattern this specific window made visible for the first time at this scale. | If this pattern recurs at future post-ship-adjacent scheduled cycles, `plan release` should consider scoping a small "hardening" epic for the immediately-prior release's newest features rather than scattering the follow-ups as isolated backlog items across multiple future releases. | Release Planning |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-13__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-13T21:30:00Z",
  "friction_item_count": 3,
  "action_now_count": 1,
  "deferred_count": 3,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
