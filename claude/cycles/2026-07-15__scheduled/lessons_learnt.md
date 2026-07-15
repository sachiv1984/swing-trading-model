**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Filed
**Report Date:** 2026-07-15

---

# Lessons Learnt — Roadmap Rebalance 2026-07-15__scheduled

Feature / Trigger: N/A — scheduled review
Run: 2026-07-15__scheduled
Reviewed by: PMO Lead
Date filed: 2026-07-15
Prior cycle checked: 2026-07-13__scheduled

---

## What worked well

- **The STEP 4.2 Idea Consolidation convention, used ad hoc at `2026-07-13__scheduled` without a governing rule, was confirmed generalisable this cycle** on its 2nd independent clustering event (22 of 44 submissions converging on 5 ad-hoc-added items) and codified directly into `roadmap_prompt.md` as an action-now patch — exactly the disciplined "confirm before hard-coding" approach the original deferred patch called for.
- **The live production-API SI-02 re-check produced a byte-identical result to the prior three checks** (2026-07-12/13/14) — a 4th consecutive confirmation that the mechanism correctly reports "no change" precisely when nothing has changed, and this cycle additionally cross-referenced the newly-filed `BLG-FE-109` as the first item plausibly able to move the stalled linkage condition.
- **The `CLAUDE.md` §6 Governance File Edit Checklist's four steps, applied in full to this cycle's own governance patch, found zero pre-existing drift** across all five version-reference locations (top header, §14 self-metadata row, §6 phase-section header, §13 Artefact Register row, Change Log top row) — the first clean cycle in a pattern that had recurred 5+ times previously (see Friction Item 1's recurrence note and this cycle's `meta_review.md`).
- **The uncommitted ad-hoc backlog additions found at session start (`BLG-FE-109/110/111/112/55`) integrated cleanly into this cycle's STEP 8.1 disposition** rather than requiring a separate reconciliation step — the idea intake window's own submissions organically clustered around them, producing a coherent v7.2 scope rather than two disconnected sets of changes.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** Yes — appeared in `2026-07-13__scheduled` (Friction Item 3, deferred pending a 2nd confirming instance).

**What happened:**
The STEP 4.2 Idea Consolidation convention, invented ad hoc at `2026-07-13__scheduled` to handle 19 clustered submissions with no governing rule, was deferred pending a "next scheduled rebalance where a similar clustering pattern (5+ overlapping submissions on one feature area) recurs." That condition recurred this cycle (22 of 44 submissions clustering on 5 ad-hoc-added items), and the convention was codified this run rather than re-applied ad hoc a second time.

**Where in the routine:**
STEP 4.2 — Document Management (Apply Before STEP 5).

**Root cause:**
Process gap (now closed) — the routine's original 1:1 idea-to-backlog-item assumption did not anticipate clustering; the `2026-07-13__scheduled` deferral was the correct interim response (validate before hard-coding), and this cycle completes that validation.

**Blast radius analysis:**
- What would have propagated: a 3rd clustering event would have had to re-invent the same ad hoc convention a second time, risking format drift (different Source-field conventions across sessions) — exactly the failure mode `2026-07-13__scheduled` flagged as a risk.
- When it would have surfaced: the next clustering event, if the convention had drifted between the two ad hoc applications.
- Recovery cost if uncaught: low-medium — a documentation/consistency issue, not data loss.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 4.2 Document Management (Apply Before STEP 5)
  - Change: added the "Idea Consolidation convention" as a permanent rule — Source field lists all contributing Idea IDs, each register row's Step 5 column names the consolidated item, typical size 3–10 ideas per consolidation.
  - Version: 8.9 → 9.0
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

### Friction Item 2

**Classification:** Type B — Semantic Mismatch

**Recurrence:** Not checkable (no prior file records this exact issue as a friction item, though the underlying pressure — backlog growth outpacing manual review — is a natural consequence of ~13 items being added per scheduled cycle for months).

**What happened:**
STEP 3.1's Actionable Backlog Assessment (A/T/D/L classification) has historically relied on a manual per-item read to classify all active backlog items. At this cycle's scale (303 active items, up from 124 at the earliest cycle with an explicit methodology note), a full manual pass was not practical within a single session. A grep-based structural heuristic (presence/absence and keyword content of `**Gate criteria:**` lines) was substituted, producing an A% figure (31.0%) that used a different method from, and is not directly comparable to, the prior cycle's more granular manually-derived figure (24.5% at `2026-07-13__scheduled`).

**Where in the routine:**
STEP 3.1 — Actionable Backlog Assessment.

**Root cause:**
Document staleness / process gap — the STEP 3.1 instruction assumes a manual per-item classification is feasible at any backlog size; it has not been revisited as the backlog has grown roughly 2.4× since the methodology was last made explicit.

**Blast radius analysis:**
- What would have propagated: the Backlog Accessibility Warning threshold check (A% < 30%) could flip on methodology noise alone rather than genuine backlog composition change, misleading the PO about a real trend.
- When it would have surfaced: the next cycle citing an A% trend line across cycles using inconsistent methodologies, or a `groom backlog` run trying to reconcile the two.
- Recovery cost if uncaught: low — an interpretation/trust issue, not a data-loss or incorrect-decision risk on its own, but compounds each cycle the backlog grows further.

**Process patch:**

→ Deferred patch (cannot apply this run — a single occurrence does not yet justify hard-coding a specific tooling approach; needs confirmation this recurs before committing to one method):
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 3.1 Actionable Backlog Assessment
  - Change required: codify one consistent, scale-appropriate methodology for the A/T/D/L classification (recommend: tooling-assisted structured parsing of `Gate criteria:` free text into a threshold/age estimate) once a 2nd occurrence confirms the manual-read approach is no longer sustainable at current backlog scale.
  - Owner: Head of Specs Team
  - Target: next STEP 11.4 meta-review (due at 3 cycles from `2026-07-15__scheduled`) — recorded as Pattern 2 in this cycle's `meta_review.md`.

---

## Recurrence Escalations

None — Friction Item 1's recurrence was the expected, planned resolution of a deliberately-deferred patch (not an unresolved outstanding action); Friction Item 2 is newly identified.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|--------------------------|
| `claude/system/roadmap_prompt.md` | STEP 4.2 | Idea Consolidation convention codified | 8.9→9.0 | Yes |

---

## New files created this run

- `claude/cycles/2026-07-15__scheduled/run_manifest.md`
- `claude/cycles/2026-07-15__scheduled/cycle_record.md`
- `claude/cycles/2026-07-15__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-15__scheduled/meta_review.md` (STEP 11.4, due this cycle)
- `claude/cycles/2026-07-15__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260715-01.md` (committed separately by the idea intake subroutine, commit `55a6b6d2`)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|------------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 0.C (Run Tier Determination) | Abbreviated-manifest exception for "0 active initiatives + no backlog/register change since prior scheduled run" (5th consecutive carry, condition not recurred — condition-gated exemption applies, not OVERDUE) | Head of Specs Team | Next scheduled rebalance where the condition genuinely recurs, or the 6th consecutive carry (whichever first) |
| `claude/system/roadmap_prompt.md` | STEP 3.1 Actionable Backlog Assessment | Codify one consistent, scale-appropriate A/T/D/L methodology | Head of Specs Team | Next STEP 11.4 meta-review (due at 3 cycles from `2026-07-15__scheduled`) |

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The v7.2 Now-horizon anchor scope (`BLG-FE-109/110/111/112/55` + 4 supporting readiness-pass items) is still only backlog-level entries with inline estimates, not a scoped release plan — the same pattern the `2026-07-13__scheduled` Carry-Forward item 1 flagged for v7.1. | The next `plan release` invocation should treat these as the mandatory anchor scope for v7.2, sequencing `BLG-FE-55` first per this cycle's accepted advisory. | Release Planning |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-15__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-15T02:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 2,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
