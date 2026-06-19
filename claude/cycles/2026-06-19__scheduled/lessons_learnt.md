# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: Scheduled rebalance — `--reason "scheduled"` — v6.0 Now horizon
Run: 2026-06-19__scheduled
Reviewed by: PMO Lead
Date filed: 2026-06-19
Prior cycle checked: 2026-06-17__scheduled

---

## What worked well

- **STEP -1.5 OVERDUE deferred patch resolution:** The gate fired correctly when LL-P5-03 (stale release target check) was identified as carrying its second consecutive cycle. Head of Specs Team authorisation was obtained promptly, the action-now patch was applied to `roadmap_prompt.md` v7.4→v7.5, all four §6 checklist steps were completed, and the run continued without ambiguity. The gate worked as designed.
- **Inline idea intake (STEP -1.6):** With 0 open ideas in the register, the inline idea intake triggered cleanly. All 8 eligible agents submitted; Facilitator exclusion was documented correctly per charter. 16 submissions were classified to terminal outcome within a single STEP 4 pass, with no boundary disputes or §13 concerns that required escalation.
- **Product Value Ratio Diagnostic (STEP 2.4):** The alert fired correctly at ratio 0.093, producing the mandatory pull-forward obligation and Challenger Product Velocity Concern at STEP 5. The structured debate resolved to a clear, documented outcome (BLG-FE-76 advanced; FEAT-46/47/20 satisfy pull-forward obligation). PO written response was captured per the STEP 2.4 rules.
- **BLG-GOV-113 status catch:** The archived status of BLG-GOV-113 (shipped v5.3) was identified before STEP 9 writes were finalised, preventing a stale item from appearing in the v6.0 Now section. The correction (4-item cluster, not 5) was applied consistently across all artefacts before commit.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced

**Recurrence:** No

**What happened:**
During STEP 8.2 composition of the v6.0 Now conditional scope (gate 2026-07-04), BLG-GOV-113 was included as an active backlog item alongside BLG-GOV-112/115/130 and BLG-OPS-59. BLG-GOV-113 (SI-05 Phase 1 effectiveness review protocol) had in fact been shipped in v5.3 (ST-23, EPIC-03) and archived. It was referenced in the run_manifest (written in the prior session before context compaction) as an active item, causing it to be carried forward incorrectly into the STEP 8 scope composition. The error was caught during STEP 9 write verification (backlog check returned no active BLG-GOV-113 entry).

**Where in the routine:**
STEP 8.2 — v6.0 Now Horizon Composition; propagated to run_manifest.md, cycle_record.md, cycle_summary.md, current_roadmap.md §8 release summary row, and DL-048 before correction.

**Root cause:**
Document staleness — the run_manifest was authored from memory of prior-cycle sprint history text (which referenced BLG-GOV-113 as a gate dependency) without verifying the item's current active/archived status in `backlog.md` and `backlog_archive.md`.

**Blast radius analysis:**
- What would have propagated: `current_roadmap.md` v6.0 Now section would have listed a shipped item as pending; `cycle_summary.md` DL-048 entry would have cited wrong scope count (12 vs 11); release planning `plan release v6.0` would have encountered a "missing item" at backlog lookup
- When it would have surfaced: At `plan release v6.0` when the backlog slice was built and BLG-GOV-113 could not be found
- Recovery cost if uncaught: Low (single correction at release planning) but would produce noise and a process deviation record

**Process patch:**

→ Deferred patch:
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 8.2 (v6.0 Now Horizon Composition)
  - Change required: Add a verification step before including any item in conditional scope — "For each proposed conditional scope item, verify the item exists in `backlog.md` (not only in `backlog_archive.md` or sprint history prose). If not found in active backlog, check archive; if archived/shipped, exclude from scope and note the status."
  - Owner: Head of Specs Team
  - Target: Next scheduled rebalance (2026-06-19__scheduled + 1 cycle, i.e., next `run roadmap --reason "scheduled"` or `--item-id`)

---

## Recurrence Escalations

None.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/roadmap_prompt.md` | STEP -1.5 "Prompt patch confirmation" | Added third bullet: stale release target check — if deferred patch targets a named release already shipped, classify OVERDUE immediately without waiting for second-consecutive-cycle rule | v7.4→v7.5 | Yes — appended 2026-06-19 |

---

## New files created this run

| File | Rationale |
|------|-----------|
| `claude/cycles/2026-06-19__scheduled/run_manifest.md` | Standard STEP 1.1 artefact |
| `claude/cycles/2026-06-19__scheduled/cycle_record.md` | Standard STEPS 2–8 record |
| `claude/cycles/2026-06-19__scheduled/cycle_summary.md` | Standard STEP 10 artefact |
| `claude/cycles/2026-06-19__scheduled/lessons_learnt.md` | This file — STEP 11 |
| `claude/ideas/window_summary_IW-20260619-01.md` | Idea window summary (STEP -1.6) |

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 8.2 (Now horizon composition) | Add active-backlog verification step before including conditional scope items: check `backlog.md` directly; exclude archived/shipped items | Head of Specs Team | Next `run roadmap` (next scheduled rebalance) |

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | BLG-FE-64 and BLG-FE-41 gates clear 2026-06-21 (2 days from rebalance date). Both are in v6.0 firm-adjacent conditional scope. | Release planning must verify gate clearance before sealing sprint 1 scope; both items are eligible on/after 2026-06-21 | Release Planning |
| 2 | BLG-GOV-131 (governance overhead ceiling metric, P2) was promoted and targets v6.1. The roadmap_prompt.md STEP 8.2 backlog-verification deferred patch targets the next rebalance run. | At next rebalance: (a) confirm BLG-GOV-131 proposal is in flight; (b) apply STEP 8.2 deferred patch per outstanding actions table above | Roadmap |
