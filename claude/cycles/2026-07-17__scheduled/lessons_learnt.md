# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled rebalance
Run: 2026-07-17__scheduled
Reviewed by: PMO Lead
Date filed: 2026-07-17
Prior cycle checked: 2026-07-16__scheduled

**Input files note:** `lessons_learnt_prompt.md` §3.1 lists `stage1_validation.md` through `stage5_rebalance.md` as Roadmap Rebalance inputs — these are stale references to a pre-consolidation file layout. This engine, consistent with every prior scheduled cycle, actually produces `run_manifest.md`, `cycle_record.md`, and `cycle_summary.md`; those three were read in place of the listed stage files (as every prior cycle's lessons_learnt.md has done, without ever flagging the mismatch as friction — not re-flagged here either, since it is long-standing, harmless, and outside this cycle's scope to fix).

---

## What worked well

- **STEP -1.5 prior-cycle outstanding actions check ran cleanly** — 0 deferred patches carried from `2026-07-16__scheduled` (both of that cycle's friction items were resolved same-run), keeping this cycle's preflight fast.
- **The Carry-Forward mechanism (`shared_standards.md` §16.8) worked exactly as designed** — `BLG-GOV-240`, filed as Carry-Forward #1 in `2026-07-16__release-v7.3`'s closure record with an explicit "action at next roadmap STEP 11 invocation" instruction, was found, actioned, and closed at precisely that point.
- **Live SI-02 production API re-check continues to be fast and reliable** — 6th consecutive successful live confirmation, no tooling friction.
- **The idea-consolidation convention (v9.0) correctly identified and bundled a genuine 9-idea cluster** (`BLG-SPEC-95`) sharing the same 4 target BLG-IDs, avoiding 9 near-duplicate backlog entries.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** No — not flagged in `2026-07-16__scheduled` lessons learnt (first identified this cycle), though the underlying drift itself had accumulated silently across 3+ prior cycles.

**What happened:**
While applying the CLAUDE.md §6 Governance File Edit Checklist's step 1 pre-check (read the file's own Change Log table's top row before bumping), `claude/system/changelogs/roadmap_prompt_changelog.md`'s top row read v8.8 while `roadmap_prompt.md`'s actual header read v9.1 — three versions (8.9, 9.0, 9.1) were missing from the standalone per-file changelog despite being correctly recorded in `claude/system/prompt_change_log.md` and `OPERATIONAL_GUIDE.md` §14 at the time each was applied. The same check applied to `claude/system/changelogs/shared_standards_changelog.md` found an even larger gap (top row 3.11 vs. actual 3.16, 5 versions missing) when this cycle's own Friction Item 1 patch required touching that file too.

**Where in the routine:**
STEP 11.2 (Prompt Change Classification) / CLAUDE.md §6 Governance File Edit Checklist step 1.

**Root cause:**
Process gap — no rule anywhere named the standalone per-file changelog as a required companion write alongside `prompt_change_log.md`. Every prior cycle's STEP 11 correctly updated `prompt_change_log.md` and `OPERATIONAL_GUIDE.md` §14 (both of which have explicit rules requiring them), but the per-file changelog file — despite its own header stating "the prompt itself contains only the current version — full history is here" — had no rule enforcing it, so it silently fell behind.

**Blast radius analysis:**
- What would have propagated: any future session trusting the per-file changelog as "full history" (per its own stated purpose) would have missed 3+ versions of change rationale, and the CLAUDE.md §6 step-1 pre-check itself would keep passing a stale document as if it were current unless the check specifically compared against the header (which it does — this is how the gap was caught).
- When it would have surfaced: the next `governance-drift` skill invocation, or the next session relying on this file specifically (rather than `prompt_change_log.md`) for roadmap_prompt.md history.
- Recovery cost if uncaught: low — a single reference-document staleness issue, not a decision-correctness issue (the canonical `prompt_change_log.md` stayed correct throughout).

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/shared_standards.md`
  - Section: §11 Prompt Version Control (IMP-10)
  - Change: added a "Companion per-file changelog rule" requiring each Class 6 prompt's standalone changelog file to be updated in the same commit as any version bump, alongside `prompt_change_log.md`.
  - Version: 3.16 → 3.17
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

(Companion action, same run: `changelogs/roadmap_prompt_changelog.md` backfilled with the 3 missing rows (8.9, 9.0, 9.1) plus this cycle's own 9.1→9.2 row; `changelogs/shared_standards_changelog.md` given its own new 3.17 top row. See Outstanding Deferred Patches below for the remaining `shared_standards_changelog.md` 3.12–3.16 backfill, deferred as disproportionate to reconstruct in this same session.)

---

### Friction Item 2

**Classification:** Type C — Dependency Stall

**Recurrence:** Not checkable — this is a structural gap in escalation surfacing, not a repeated instance of the same event.

**What happened:**
A pre-existing, cross-routine escalation (day-range effort mandate disposition, originally filed by Release Planning at `2026-07-14__release-v7.1`, deadline 2026-07-17 — due exactly this cycle) was found and resolved only because this session happened to inspect memory notes and grep historical closure records for it. No STEP in `roadmap_prompt.md` — including STEP -1.5 (Prior Cycle Outstanding Actions) and STEP -1.7 (Governance Health Score) — systematically scans other routines' recent `lessons_learnt_closure.md`/`lessons_learnt.md` files for escalations with a due date landing on or before the current cycle's date. STEP -1.5 only scans the roadmap engine's *own* prior cycle chain (`last_rebalance_cycle`).

**Where in the routine:**
STEP -1.5 / STEP -1.7 (Governance Health Score — Outstanding Action Count component).

**Root cause:** Process gap — escalations filed by one routine (Release Planning) with a deadline landing during a different routine's (Roadmap) invocation window have no defined cross-routine surfacing mechanism; they rely on ad hoc discovery.

**Blast radius analysis:**
- What would have propagated: the escalation could have silently missed its 72-hour-style deadline with no engine flagging the breach, relying entirely on a human or an unusually thorough session noticing it.
- When it would have surfaced: never automatically — only via manual review of closure records, exactly as happened this cycle.
- Recovery cost if uncaught: low-medium — a governance-process-hygiene gap (a due-date escalation quietly expiring unactioned), not a product-correctness issue.

**Process patch:**

→ Deferred patch (cannot apply this run — requires deciding which files/date-range to scan and how to avoid false positives across 5 engines' closure records, out of scope for a same-session fix):
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP -1.7 Governance Health Score — Outstanding Action Count component
  - Change required: Extend the Outstanding Action Count scan to include a due-date-aware pass over the last 3 completed cycles' `lessons_learnt_closure.md` / `lessons_learnt.md` files (any routine), surfacing any escalation whose stated deadline falls on or before the current cycle's date, whether or not it names the Roadmap engine as owner.
  - Owner: Head of Specs Team
  - Target: next roadmap STEP 11 invocation (2026-07-18__scheduled or the next scheduled cycle, whichever comes first)

---

## Recurrence Escalations

None.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|--------------------------|
| `claude/system/roadmap_prompt.md` | STEP 8.1 | Empty Now Horizon Gate condition 1 extended to fire on a non-empty-but-unversioned Now horizon, closing BLG-GOV-240 | 9.1 → 9.2 | Yes |
| `claude/system/shared_standards.md` | §11 | Companion per-file changelog rule added | 3.16 → 3.17 | Yes |

---

## New files created this run

- `claude/cycles/2026-07-17__scheduled/run_manifest.md`
- `claude/cycles/2026-07-17__scheduled/cycle_record.md`
- `claude/cycles/2026-07-17__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-17__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260717-01.md` (committed separately by the idea intake subroutine, commit `ccfb63e9`)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP -1.7 Governance Health Score | Extend Outstanding Action Count to a due-date-aware scan of the last 3 cycles' closure/lessons-learnt files across all routines (Friction Item 2) | Head of Specs Team | 2026-07-18__scheduled or next scheduled cycle |
| `claude/system/changelogs/shared_standards_changelog.md` | Full file | Backfill missing rows 3.12–3.16 (found this cycle to be absent despite the underlying version bumps being correctly recorded in `prompt_change_log.md`/`OPERATIONAL_GUIDE.md` §14) | Head of Specs Team | Next roadmap STEP 11 invocation |

---

## Escalations

None.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The v7.4 Now-horizon scope (`BLG-FE-115/116/117/118` + `BLG-SPEC-95`) is now formally version-labelled and PO-committed as the anchor scope, per DL-070. | The next `plan release v7.4` invocation should treat these 5 items as the mandatory anchor scope, sequencing `BLG-SPEC-95` first (or in parallel) per the `BLG-SPEC-91-94`/`BLG-SPEC-89/90` precedent. | Release Planning |
| 2 | STEP 7.1 Skill-Silo rolling-3-cycle average worsened for a 2nd consecutive reading (66.7%→80.9%), one reading short of the v8.3 mandatory-≥2-U-items trigger. | If the next reading (v7.2/v7.3/v7.4 window) does not improve, the mandatory clause will fire automatically at the following scheduled rebalance — the engine should not treat this as a surprise if it happens, since it is expected given the 2-reading trend already visible now. | Roadmap |
| 3 | STEP 11.4 meta-review is due at the next scheduled rebalance (cycle 3 since the `2026-07-15__scheduled` reset). | The next scheduled rebalance must run the meta-review — aggregate friction items by Type across `2026-07-16__scheduled` and `2026-07-17__scheduled`, including this cycle's 2 Type A/C items and the deferred `shared_standards_changelog.md` backfill. | Roadmap |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-17__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-17T10:30:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 2,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
