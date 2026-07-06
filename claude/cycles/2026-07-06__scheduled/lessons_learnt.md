**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-07-06__scheduled
**Last Updated:** 2026-07-06

---

# Lessons Learnt — Roadmap Rebalance 2026-07-06__scheduled

Feature / Trigger: N/A — scheduled rebalance
Run: 2026-07-06__scheduled
Reviewed by: PMO Lead; Head of Specs Team
Date filed: 2026-07-06
Prior cycle checked: 2026-07-03__scheduled

---

## What worked well

1. **All 34 ideas reaching the §4.5 3-cycle hard cap simultaneously were resolved cleanly** with zero vague rationales — every one of the 34 named a specific dependency, date, or trigger condition, so no Facilitator default-to-Reject was needed despite the unusually large single-cycle disposition volume.
2. **STEP 4.0's gate-condition re-check correctly caught 2 stale Park Rationales** (`IDEA-ai-compliance-20260702-02`, `IDEA-frontend-specs-20260702-02`) that named `BLG-FE-82`, which shipped this same day (v6.6, 2026-07-06) — both were forced through mandatory re-evaluation rather than silently carried to a terminal disposition without acknowledging the shipped dependency.
3. **The STEP 5 debate resolved a fresh idea and a previously-deferred patch from v6.6 closure in a single, minimally-scoped action** — the Challenger's legitimate governance-complexity concern (citing `GCA-2026-06-17`) led the Product Owner to narrow the proposal from a full second escalation tier to one prompt clause, avoiding the over-engineering risk while still closing the deferred patch.
4. **LP-05's gate-verification rule (`roadmap_prompt.md` v8.2, applied at v6.6 closure) worked as intended on its first live test** — direct inspection during the STEP 7.1 pull-forward scan caught that `BLG-FEAT-52` still carries an unmet gate, preventing a 3rd consecutive cycle of naming it as a candidate.

---

## Friction Log

---

### Friction Item 1

**Classification:**
- Type A — Governance Drift: `BLG-FEAT-52`'s backlog entry used a non-standard `**Gate:**` field label instead of the established `**Gate criteria:**` convention used by every other gated item.

**Recurrence:** Not checkable (no prior lessons learnt file flagged this specific field-label inconsistency; this is the first time it was caught).

**What happened:**
STEP 3.1's automated Actionable Backlog Assessment scan searches `backlog.md` for the literal string `**Gate criteria:**` to identify gated items. `BLG-FEAT-52` instead carried a `**Gate:**` line, so the automated scan silently classified it as ungated (Actionable now) and it appeared in the STEP 7.1 pull-forward candidate list drawn from the "no gate" grep. The inconsistency was only caught because this cycle's STEP 7.1 pull-forward check (per the LP-05 v8.2 patch) required direct manual inspection of the item's own backlog entry before naming it as a candidate — that manual read is what surfaced the field-label mismatch, not the automated scan.

**Where in the routine:**
STEP 3.1 (Actionable Backlog Assessment, automated gate-field scan) / STEP 7.1 (pull-forward candidate gate verification).

**Root cause:**
Naming inconsistency — one backlog entry used a synonym (`**Gate:**`) for the canonical field label (`**Gate criteria:**`) with no validation step enforcing the convention.

**Blast radius analysis:**
- What would have propagated: `BLG-FEAT-52` could have been silently re-named as a pull-forward candidate a 3rd consecutive cycle (exactly the failure LP-05 was designed to prevent), had this cycle's manual inspection not caught the field-label mismatch independently of the automated scan.
- When it would have surfaced: at `plan release v6.7`, when release planning would need to catch the unmet gate a second time (as it already had to do once at v6.6, per the LP-05 finding).
- Recovery cost if uncaught: low this cycle (caught in time) but recurring — every cycle the automated STEP 3.1 scan runs, this item is silently miscounted as Actionable rather than Data-density-gated, understating the true L/D-gated proportion of the backlog by one item each time.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/backlog/backlog.md`
  - Section: `BLG-FEAT-52` entry
  - Change: `**Gate:**` field label corrected to `**Gate criteria:**` to match the canonical convention used by all other gated backlog items.
  - Version: N/A (backlog.md is not a versioned governance prompt)
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Not applicable (backlog content fix, not a governance prompt change)

→ Deferred patch (systemic prevention — cannot apply this run, requires a full-file sweep outside this engine's STEP 3 read-only scan scope):
  - File: `claude/system/backlog_management_prompt.md`
  - Section: STEP 4 (or new dedicated field-normalisation step)
  - Change required: Add a scan step that greps `backlog.md`/`backlog_archive.md` for any `**Gate:**` field label (as opposed to `**Gate criteria:**`) and normalises it, preventing future silent exclusions from the roadmap engine's STEP 3.1 automated scan.
  - Owner: Head of Specs Team
  - Target: next `groom backlog` invocation (2026-07-06 or later — whichever comes first)

---

### Friction Item 2

**Classification:**
- Type C — Dependency Stall: the SI-02 gate's trade-count condition has no single reliable, structured field for engines without live production database access to read — it is reconciled only through free prose carried across cycle headers.

**Recurrence:** Not checkable (no prior lessons learnt file flagged this specific reconciliation gap as a friction item; prior cycles simply carried the same prose estimate forward without surfacing the underlying process gap).

**What happened:**
A user report (recorded in this session's prior-conversation memory, dated 2026-07-03) claims 20 closed trades — the exact SI-02 gate threshold. The last formally confirmed count via a governed routine is 15 (2026-06-23, at the PT-04 gate check). This session had no production database or authenticated API access to run the confirming query directly, so the discrepancy could not be resolved this cycle. The engine correctly declined to mark the gate cleared on the self-report alone (per standing guidance), but there is no structured mechanism today for a data-access-constrained engine invocation to distinguish "informal report, unverified" from "formally confirmed by a governed routine" — both currently live as prose in `current_roadmap.md`'s SI-02 row and get carried forward by whichever engine runs next, informally.

**Where in the routine:**
STEP 2.3 (Horizon Review — SI-02 gate re-verification).

**Root cause:**
Missing artefact — no canonical, structured field exists (e.g. in `current_roadmap.md` or a dedicated gate-status file) distinguishing "last formally confirmed value + confirming routine + date" from "unverified self-report + date," forcing every engine to either re-derive this distinction from prose or skip it.

**Blast radius analysis:**
- What would have propagated: a future engine invocation (with or without live data access) could misread the prose and either prematurely treat the gate as cleared, or conversely keep citing a stale 15-trade figure well after the count has genuinely passed 20 — either error would misinform `plan release`/`plan sprint`'s SI-02 frontend scoping decision.
- When it would have surfaced: the next `plan release` or `plan sprint` invocation that reaches SI-02 scoping, if it does not independently re-run the confirming query.
- Recovery cost if uncaught: medium — an incorrect SI-02 gate determination would either delay a now-viable feature by a full cycle, or admit an under-verified feature into sprint scope prematurely.

**Process patch:**

→ Deferred patch (requires a design decision on where the structured field lives — cannot apply this run without over-scoping a data-schema change into a routine invocation that has no live data access to populate it correctly):
  - File: `claude/roadmap/current_roadmap.md` (SI-02 row, §6 Gated Features table) and `claude/system/roadmap_prompt.md` (STEP 2.3 read instruction)
  - Section: SI-02 gate row / STEP 2.3
  - Change required: Add a structured sub-field distinguishing `**Last formally confirmed:** <count> (<confirming routine>, <date>)` from `**Unverified report:** <count> (<source>, <date>) — not yet confirmed`, so engines without live data access can cite the correct authoritative value without re-deriving it from prose.
  - Owner: PMO Lead
  - Target: next `plan release v6.7` (target ~2026-07-07 per the empty-Now-horizon deferral recorded at STEP 8.1 this cycle; if `plan release v6.7` has not run by 2026-07-13__scheduled, revisit at that cycle per the stale-release-target fallback).

---

## Recurrence Escalations

None this cycle. Both friction items are new findings (not open prior-cycle outstanding actions left unresolved).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/backlog/backlog.md` | `BLG-FEAT-52` entry | `**Gate:**` field label corrected to `**Gate criteria:**` | N/A | Not applicable (content fix, not a governance prompt) |
| `claude/system/roadmap_prompt.md` | §7.1 | Mandatory pull-forward clause added after 3+ consecutive worsening/unresolved Skill-Silo readings (resolves the STEP 5 debate outcome and the deferred patch from `lessons_learnt_closure.md` v6.6) | v8.2→v8.3 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §6 header, §13 register, §14 table, Change Log | Version/source rows updated to v8.3; document Version 4.78→4.80 (includes backfill of a found 4.79 header-drift) | v4.78→v4.80 | Yes |

---

## New files created this run

- `claude/cycles/2026-07-06__scheduled/run_manifest.md`
- `claude/cycles/2026-07-06__scheduled/cycle_record.md`
- `claude/cycles/2026-07-06__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-06__scheduled/lessons_learnt.md` (this file)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/backlog_management_prompt.md` | STEP 4 (or new field-normalisation step) | Scan `backlog.md`/`backlog_archive.md` for non-canonical `**Gate:**` field labels and normalise to `**Gate criteria:**` | Head of Specs Team | Next `groom backlog` invocation |
| `claude/roadmap/current_roadmap.md` + `claude/system/roadmap_prompt.md` | SI-02 gate row (§6) / STEP 2.3 | Add structured `**Last formally confirmed:**` vs. `**Unverified report:**` sub-fields for the SI-02 trade-count gate | PMO Lead | Next `plan release v6.7` (target ~2026-07-07; revisit by 2026-07-13__scheduled if not yet run) |

---

## Escalations

None raised by this engine this cycle. (Note: `claude/cycles/2026-07-04__release-v6.6/closure_escalations.md` carries an open escalation, `ESC-CLOSE-20260706-01`, raised by Post-Ship Closure and surfaced here via the Carry-Forward Advisory mechanism — see `run_manifest.md` §Governance Health Score. It is out of this engine's write scope and is not re-logged as a new escalation.)

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The SI-02 trade-count gate has an unresolved discrepancy between a user self-report (20 trades, 2026-07-03) and the last formally confirmed count (15, 2026-06-23), and this engine had no live data access to resolve it. | The next engine invocation with production data/API access (`plan release` or `plan sprint`) should treat re-verifying this gate as a priority action, and should populate the new structured confirmation field once the deferred patch (above) is applied. | Release Planning |
| 2 | The new mandatory pull-forward clause (`roadmap_prompt.md` §7.1, v8.3) requires ≥2 build-and-ship-shaped U-items at the next release — this is now a binding requirement, not an advisory, for the first time. | `plan release v6.7` must treat this as a hard scoping constraint, not merely a recommendation, when deciding whether to include `BLG-FE-87`/`BLG-FE-88` (or equivalent build-and-ship U-items). | Release Planning |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-06__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-06T14:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 2,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
