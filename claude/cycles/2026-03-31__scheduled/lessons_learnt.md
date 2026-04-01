**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-31

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: Scheduled run — N/A (no completion event; post-v2.3 ship scheduled rebalance)
Run: 2026-03-31__scheduled
Reviewed by: PMO Lead
Date filed: 2026-03-31
Prior cycle checked: 2026-03-24__scheduled

---

## What Worked Well

- **Standard-tier run completed in one session:** Unlike the prior Extended-tier run (2026-03-24__scheduled), this Standard-tier run (4 advancing ideas, ~15 output files) completed fully in a single session without context exhaustion. Context budget estimates for Standard-tier are accurate.
- **OVERDUE patch resolved via B7 escalation:** The deferred STEP 8.5 Extended-tier advisory patch (carried twice) was resolved via the B7 auto-escalation path in STEP 11. The escalation mechanism functioned correctly — the run did not proceed past STEP -1.5 without a resolution commitment.
- **Carry-forward from prior cycle consumed:** The 1 carry-forward item from 2026-03-24__scheduled (Extended-tier session context advisory) was directly addressed by the OVERDUE patch. Carry-forward loop closed cleanly.
- **ID anomaly detected and corrected:** The BLG-FEAT-12 duplicate ID (from backlog-add skill session item) was caught during STEP 3 backlog health review and corrected in STEP 9. The run_manifest.md and cycle_record.md both document the correction with clear traceability.
- **4 gate-cleared ideas advanced cleanly:** All 4 advancing ideas had clear gate conditions satisfied by v2.3 shipping. The park rationale update pattern ("revisit post-v2.3") from the prior cycle worked exactly as intended — v2.3 shipping was the trigger, and the ideas were immediately eligible to advance.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type B — Process Gap: backlog-add skill ID assignment error (reuse of archived ID)

**Recurrence:** No (not in prior cycles)

**What happened:**
The backlog-add skill (a pre-existing session skill, not the roadmap engine) assigned BLG-FEAT-12 to a new item ("Add gated feature rollout capability") without checking the archive for prior holders of that ID. BLG-FEAT-12 was previously used for "Alert history table" (shipped v2.2, archived). The skill's Step 1 instructions say "search both active items AND the Closed Items table — archived items still consume their ID" but the check apparently did not include the archive. The error was detected at roadmap rebalance STEP 3 backlog health review.

**Where in the routine:** Pre-run (session backlog-add skill); detected at STEP 3

**Root cause:** The backlog-add skill's ID scan in Step 1 did not include the backlog_archive.md. The instruction exists but the implementation missed the archive search.

**Blast radius analysis:**
- What would have propagated: The duplicate ID would persist in the backlog indefinitely until a future groom or manual review caught it. Decision log references to "BLG-FEAT-12" would become ambiguous between the archived item and the new item.
- When it would have surfaced: At the next backlog groom run or when someone searched for "BLG-FEAT-12" in the decision log and found two different items.
- Recovery cost if uncaught: Low-medium — renaming requires updating backlog.md + a note in the release plan. No functional impact.

**Process patch:**

→ Lessons learnt (skills):
- File: `.claude/skills/backlog-add/SKILL.md`
- Section: Step 1 — Scan existing IDs
- Change required: Add explicit instruction: "The archive scan must include `claude/backlog/backlog_archive.md`. Search for `### BLG-{NAMESPACE}-` in both `backlog.md` AND `backlog_archive.md`. The highest number across both files is the current maximum."
- Owner: Head of Specs Team
- Target: Apply as action-now (this run)

→ This will be applied in STEP 11 as a secondary action-now (skills file update, not a governance prompt file — outside the formal prompt patch log scope, but appropriate as a skills maintenance action).

---

## Recurrence Escalations

None.

---

## Process Improvements Actioned This Run

1. **OVERDUE patch applied:** roadmap_prompt.md STEP 8.5 Extended-tier session advisory — v4.5→v4.6. Head of Specs Team sign-off. Formally resolves the B7-triggered OVERDUE item from two consecutive prior cycles.

---

## New Files Created This Run

| File | Rationale |
|------|-----------|
| `claude/cycles/2026-03-31__scheduled/run_manifest.md` | Standard cycle artefact — roadmap run manifest |
| `claude/cycles/2026-03-31__scheduled/cycle_record.md` | Standard cycle artefact — STEP 2–8 working content |
| `claude/cycles/2026-03-31__scheduled/cycle_summary.md` | Standard cycle artefact — STEP 10 summary |
| `claude/cycles/2026-03-31__scheduled/lessons_learnt.md` | This file — STEP 11 |

---

## Outstanding Deferred Patches

None. Prior OVERDUE patch resolved in this run.

---

## Escalations

None.

---

## Carry-Forward

Items: 0

No carry-forward items this cycle. Prior cycle carry-forward item consumed by OVERDUE patch resolution.

