**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-24

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: Scheduled run — N/A (no completion event; post-v2.2 ship scheduled rebalance)
Run: 2026-03-24__scheduled
Reviewed by: PMO Lead
Date filed: 2026-03-24
Prior cycle checked: 2026-03-21__item-3.5

---

## What Worked Well

- **Prior cycle patches effective:** Friction Item 1 from 2026-03-21__item-3.5 (STEP 5 debate omission) was resolved by roadmap_prompt.md v4.3 STEP 4.4 queue + STEP 5 preflight. This cycle's STEP 5 queue was fully populated (8 items) and all 8 received debate entries before STEP 5 was marked complete. Zero debate omissions.
- **Initiative register patch effective:** Friction Item 2 from 2026-03-21__item-3.5 (initiative_register.md Active table stale) was resolved by roadmap_management_prompt.md v1.3. The register was current at run start ("No active initiatives as of 2026-03-21") — no correction required in STEP 9.
- **STEP 8.6 guardrail satisfied naturally:** With 8 items advancing, Challenger issued a Type A counter-argument on BLG-QA-05 (§3 human-in-loop risk from Playwright automation). The rebuttal was substantive and advance was confirmed with an explicit scope constraint. The guardrail is working as intended.
- **Meta-review clean:** 3rd rebalance cycle trigger met. Meta-review conducted and filed. No new prompt patches required — all previously identified patterns are resolved or previously addressed. First meta-review with a "no new patches" outcome, indicating the governance process is reaching maturity.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type D — Cognitive Fatigue: STEP 9 canonical writes required a new session (context exhaustion mid-run)

**Recurrence:** No (not in 2026-03-21__item-3.5)

**What happened:**
The roadmap rebalance run (STEP 2–8 including 40 idea classifications, 8 debates, scoring matrix, and workforce economics) consumed sufficient context that STEP 9 canonical writes could not be completed in the same session. A new session was required to execute the STEP 9 write plan. The run_manifest.md and cycle_record.md were created in the first session; the 13 remaining canonical writes (scored_initiatives.md, ideas_register.md, backlog.md, etc.) were executed in the second session by reading the cycle_record.md STEP 8.5.B write plan.

**Where in the routine:** STEP 9 — Canonical Write (session boundary mid-execution)

**Root cause:** Context window pressure — scheduled Extended-tier runs are the heaviest single routine in the system. A scheduled run processes: 40 idea classifications (STEP 4), 8 debates (STEP 5), full scoring matrix (STEP 6), workforce economics (STEP 7), final decisions (STEP 8), write plan verification (STEP 8.5), guardrail check (STEP 8.6), plus all 13 output file writes (STEP 9) and cycle outputs (STEPS 10, 11, 12). The Extended tier adds a horizon review that is absent from item-triggered runs.

**Blast radius analysis:**
- What would have propagated: Session boundary during STEP 9 is low-risk if the write plan (STEP 8.5.B) is complete and recorded in cycle_record.md — the new session can resume from the plan. No decision-making restarts; only mechanical writes remain at that point.
- When it would have surfaced: Immediately — the new session started with explicit context from cycle_record.md STEP 8.5.B. No artefact was lost or incorrect.
- Recovery cost if uncaught: Low — the write plan in cycle_record.md is the recovery artefact. As long as STEP 8.5 completes before the session ends, STEP 9 can restart cleanly.

**Process patch:**

→ Deferred patch:
- File: `claude/system/roadmap_prompt.md`
- Section: STEP 8.5 (Stateless Write Safety Gate) — add a note after the write plan table
- Change required: Add advisory: "For Extended-tier scheduled runs (40+ ideas), STEP 9 write volume (~13 files) may require a new session. Before closing session: confirm STEP 8.5.B write plan is complete and recorded in cycle_record.md. The write plan is the resumption artefact — a new session can execute STEP 9 by reading cycle_record.md §8.5.B directly."
- Owner: Head of Specs Team
- Target: Next roadmap_prompt.md version update (next governance sprint or pre-v2.3 release planning cycle)

---

## Recurrence Escalations

None.

---

## Process Improvements Actioned This Run

None applied this run.

---

## New Files Created This Run

| File | Rationale |
|------|-----------|
| `claude/cycles/2026-03-24__scheduled/run_manifest.md` | Standard cycle artefact — roadmap run manifest |
| `claude/cycles/2026-03-24__scheduled/cycle_record.md` | Standard cycle artefact — STEP 2–8 working content |
| `claude/cycles/2026-03-24__scheduled/cycle_summary.md` | Standard cycle artefact — STEP 10 summary |
| `claude/cycles/2026-03-24__scheduled/lessons_learnt.md` | This file — STEP 11 |
| `claude/cycles/2026-03-24__scheduled/meta_review.md` | STEP 11.4 — meta-review due (3rd cycle) |

---

## Outstanding Deferred Patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 8.5 (Stateless Write Safety Gate) | Add Extended-tier session advisory: before closing session, confirm STEP 8.5.B write plan is complete in cycle_record.md — the write plan is the resumption artefact for STEP 9 | Head of Specs Team | Next roadmap_prompt.md version update (next governance sprint or pre-v2.3 release planning) |

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Extended-tier scheduled runs (40+ ideas) exhaust session context before STEP 9 canonical writes complete. The STEP 8.5.B write plan in cycle_record.md is the reliable resumption artefact — session restarts from the plan without loss. | Before closing the session after STEP 8.5 completes: confirm the write plan is complete and recorded. Treat STEP 8.5.B as a hard checkpoint before ending any Extended-tier session. | Roadmap |
