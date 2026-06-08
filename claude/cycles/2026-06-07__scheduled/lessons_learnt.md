**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-07
**Cycle:** 2026-06-07__scheduled

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled run
Run: 2026-06-07__scheduled
Reviewed by: PMO Lead
Date filed: 2026-06-07
Prior cycle checked: 2026-06-03__scheduled (claude/cycles/2026-06-03__scheduled/lessons_learnt.md — found)

---

## What Worked Well

- **Inline idea intake executed cleanly.** IW-20260607-01 opened and closed in a single session. All 22 agents (Facilitator excluded per charter) submitted minimum 2 ideas. No STEP 2.0 parked queue overlap to resolve (register was empty).
- **v5.2 Now horizon established efficiently.** STEP 8.1 fired (empty Now + no v5.2 section), PO chose Option (a), and the v5.2 section was added with OA-01/02 pre-conditions in a single write. The recurring STEP 8.1 advisory from prior cycles (fired as Option b in 2026-06-03__scheduled) is now resolved for this cycle.
- **SI-05 operational hardening cluster identified proactively.** 9 of 25 new items are SI-05 Phase 1 follow-up (delivered v5.1 just 3 days ago). The idea intake mechanism surfaced these before they became urgent incidents, which is the intended behaviour for early-stage operational gaps.
- **Prior cycle OA-01/02 now backlog items.** BLG-GOV-93 (OA-01/02 enforcement) converts the open actions into a sprint story, addressing the F-01 OVERDUE patch recurrence pattern from 2026-06-03__scheduled.

---

## Friction Log

| # | Type | Description | Blast radius | Patch |
|---|------|-------------|-------------|-------|
| F-01 | Type D (duplicate submission) | IDEA-head-of-specs-20260607-01 ("BLG-SPEC-47 resolution plan") was advanced through STEP 4 and consumed a STEP 5 debate slot before being identified as a complete duplicate of BLG-SPEC-47 already in the active backlog. The ideas intake STEP 2.0 checks for overlap with parked ideas from the same agent, but does not check the active backlog for existing items covering the same scope. | Single STEP 5 debate slot wasted. No downstream impact. | Deferred: consider adding a "check active backlog for idea scope overlap" advisory step to idea_intake_prompt.md STEP 2.0 (after the parked queue pre-check). Would surface obvious duplicates before the advance decision. Not action-now — the cost is low (one wasted debate slot per cycle maximum); the fix requires specifying what constitutes "scope overlap" clearly enough to prevent false positives. |

---

## Deferred Patches

| # | File | Section | Change | Owner | Target |
|---|------|---------|--------|-------|--------|
| 1 | claude/system/idea_intake_prompt.md | §2.0 Parked Queue Pre-Check | After the parked queue pre-check, add an advisory step: "Before generating new submissions, briefly scan active `backlog.md` items for any scope overlap with planned submissions. If clear overlap exists: note in submission that it may duplicate an existing item; roadmap engine STEP 4 will assess." Advisory only — not a hard gate; does not change the advance/park/reject decision. | Head of Specs Team | v5.2+ prompt review |

---

## Outstanding Actions

None. No escalations.

---

## Process Observations (Not Friction)

| # | Observation | Owner | Action |
|---|-------------|-------|--------|
| LL-01 | 9 of 25 new items are SI-05 operational hardening. This is the highest post-feature-ship backlog cluster observed in recent cycles (typical post-ship additions are 1-3 operational items). It reflects the fact that SI-05 introduced several new operational surfaces (Telegram token, scheduled service, new endpoint) that generate their own governance and security follow-up work. This is expected and healthy behaviour; it would be worth flagging at v5.2 sprint planning to ensure the SI-05 cluster items are prioritised appropriately. | PMO Lead | Flag at v5.2 sprint planning. |
| LL-02 | BLG-SPEC-48 (POST /digest/si05/send API contract gap check) is P1 because it addresses a potential CLAUDE.md §2 compliance violation. If the contract was NOT filed at v5.1 sprint time, this is spec debt. It should be resolved in v5.2 as a first-priority item — before any other SI-05 stories enter sprint planning. The endpoint test suite update (CLAUDE.md §2 last bullet) should also be verified at the same time. | Head of Engineering | Verify BLG-SPEC-48 scope before v5.2 sprint planning; if contract missing, treat as P0 in v5.2. |
| LL-03 | Meta-review NOT due this cycle (1 cycle since last meta-review at 2026-06-02__scheduled). Next meta-review due after 2 more cycles. | PMO Lead | Schedule meta-review at the 3rd rebalance from now. |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-06-07__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-06-07T11:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
