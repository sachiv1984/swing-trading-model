**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-17

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: v1.10 — Operations & Quality Foundation (completion event 2026-03-16)
Run: 2026-03-17__item-v1.10
Reviewed by: PMO Lead
Date filed: 2026-03-17
Prior cycle checked: 2026-03-15__item-5.3

---

## What worked well

- **Prior cycle actions fully resolved:** All 3 outstanding actions from 2026-03-15__item-5.3 (LL-01, LL-02, LL-02-patch) were resolved before this cycle ran. STEP -1.5 required zero carry-forwards.
- **Idea classification efficiency:** With 29 Parked-cycle-2 ideas and clear capacity constraints for v2.0, the classification logic was straightforward. The Park/Reject rationale criteria were clear and distinguishable.
- **Challenger process worked:** The Challenger produced a substantive counter-argument (Type A) for Candidate 2 (Positions Table Data Dictionary), and the PO rebuttal demonstrated genuine consideration of the overlap concern. STEP 8.6 guardrail passed naturally via the one park at STEP 5.
- **Horizon structure:** The Now/Next/Later labelling is a clean improvement to the roadmap — maps directly from the existing §3/§4/§5 structure without content changes.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type D — Cognitive Fatigue: A detail was missed due to prompt length, context overload, or accumulated complexity

**Recurrence:** No (not in 2026-03-15__item-5.3)

**What happened:**
The 29 Parked-cycle-2 ideas all become Parked-cycle-3 after this cycle's re-park decisions. While this is correct governance behaviour (stale = 3+ cycles, threshold triggers next cycle), the sheer volume of stale dispositions due next cycle (19 ideas + whatever is advanced/rejected from cycle-3 stale check) represents a significant Product Owner governance burden at the next roadmap run. This friction is latent — it will materialise at the next cycle, not this one.

**Where in the routine:** STEP 4.1 — Classification; STEP 4.5 — Parked Idea Expiry Rule

**Root cause:** Document staleness — the idea pool has not been refreshed (no new intake window) for 3 cycles, while existing ideas have been re-parked. The volume compounds. Additionally, the current per-file submission model (BLG-GOV-02) makes bulk classification laborious.

**Blast radius analysis:**
- What would have propagated: At the next roadmap run, 19 mandatory stale dispositions will require written PO rationale for each. This is 19 individual rationale entries to write — a significant burden that could delay or fragment the STEP 4 classification process.
- When it would have surfaced: Next roadmap rebalance cycle (next run)
- Recovery cost if uncaught: Medium — if stale dispositions are skipped, the cycle halts per §4.5 rules. If they are handled minimally (insufficient rationale), they represent a governance record gap.

**Process patch:**

→ Deferred patch (cannot apply this run):
- File: `claude/system/idea_intake_prompt.md`
- Section: STEP 3 (or new guidance section before STEP 1)
- Change required: Add a "stale warning horizon" note: when the remaining open ideas in the submissions folder are ≥15 and all at Parked-cycle-2 (one cycle from stale threshold), the Facilitator should note this in the cycle summary and recommend opening a new intake window (via `run ideas`) before the next roadmap run, to replace stale ideas with fresh submissions and reduce the stale disposition burden.
- Owner: Head of Specs Team
- Target date: Before next roadmap rebalance run (within current v2.0 planning window)

---

### Friction Item 2

**Classification:** Type B — Semantic Mismatch: The same concept was named or interpreted differently across documents or roles

**Recurrence:** No (not in 2026-03-15__item-5.3)

**What happened:**
During the Positions Table Data Dictionary (IDEA-data-model-owner-20260304-01) debate, the Challenger raised a valid concern about overlap with BLG-NEW-13 (Spec Coverage Inventory). The distinction between "spec coverage audit" (BLG-NEW-13) and "data dictionary" (BLG-DATA-01) is not documented — it was only resolved through the STEP 5 PO rebuttal. Without an explicit scope boundary in the backlog, future contributors might treat these as duplicates.

**Where in the routine:** STEP 5.2 — Product Owner Response

**Root cause:** Template omission — BLG-DATA-01 and BLG-NEW-13 backlog entries don't cross-reference each other or explicitly describe their scope boundary.

**Blast radius analysis:**
- What would have propagated: Future backlog grooming might incorrectly close or merge BLG-DATA-01 as a duplicate of BLG-NEW-13. Or a developer might begin work on one assuming it covers the other's scope.
- When it would have surfaced: Release planning or sprint planning for v2.0
- Recovery cost if uncaught: Low — single edit to add a "scope distinction" note to BLG-DATA-01 in the backlog

**Process patch:**

→ Immediate patch applied this run:
- File: `claude/backlog/backlog.md` (BLG-DATA-01 entry)
- Section: BLG-DATA-01 item description
- Change: "Scope constraint: Positions table only. Complements BLG-NEW-13 (Spec Coverage Inventory) — distinct scope: this is field-level semantics documentation, not coverage mapping." (added inline in the BLG-DATA-01 entry created this run)
- Version: N/A — backlog is not versioned (Class 4 planning document, no version increment required)
- Confirmed by: Head of Specs Team (lifecycle compliance — Class 4 description update; no version bump required for Class 4)
- Prompt change log entry: Not applicable — this is a backlog content update, not a prompt change

---

## Prior Cycle Deferred Lessons Status

All deferred patches from 2026-03-15__item-5.3 were confirmed applied before this cycle:
- LL-02-patch (roadmap_prompt.md STEP 8.5.B): Applied in v2.7 (post-ship closure 2026-03-16). Confirmed by Head of Specs Team.

No OVERDUE items. No escalations from prior cycle.

---

## Deferred Patches (for next governance session)

| Patch | Description | Prompt file | Section | Owner | Target |
|-------|------------|-------------|---------|-------|--------|
| LL-01-patch | Add stale warning horizon note — when ≥15 ideas are all at Parked-cycle-2, Facilitator should recommend opening new intake window before next run | `claude/system/idea_intake_prompt.md` | New guidance in STEP 3 or before STEP 1 | Head of Specs Team | Before next roadmap rebalance run |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-03-17__item-v1.10",
  "phase": "Roadmap",
  "filed_utc": "2026-03-17T00:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
