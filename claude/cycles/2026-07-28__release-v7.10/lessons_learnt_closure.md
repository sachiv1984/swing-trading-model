Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-30
Cycle: 2026-07-28__release-v7.10

# Lessons Learnt — Post-Ship Closure — v7.10

Feature / Trigger: Materially reduce the platform's production risk surface — closing silent backend error-masking, hardening security posture, strengthening QA/CI infrastructure, correcting API contract debt, and clearing a first tranche of frontend technical debt.
Run: 2026-07-28__release-v7.10
Reviewed by: PMO Lead
Date filed: 2026-07-30
Prior cycle checked: 2026-07-27__release-v7.9

---

## What worked well

- All three source records (`lessons_learnt.md`, `lessons_learnt_cycle.md` Phase 3 + Phase 4) were small, well-structured, and had every action item already pre-classified with a disposition — closure review confirmed each rather than performing first-pass triage from raw prose.
- Two lessons-learnt actions previously deferred by their originating phase (Delivery Verification could not touch `execution_prompt.md`; the phase's own Phase 3 action targeted "next groom backlog invocation") were both actionable at Post-Ship Closure, which has the correct write scope for both — closing them same-cycle rather than letting them sit as open deferred patches.
- The Endpoint Coverage Drift Check (STEP 6) correctly picked up and reconciled the exact carry-forward item flagged by v7.9's own closure lessons learnt (`BLG-OPS-111` list staleness) — the mechanism worked as designed across a cycle boundary.

---

## Friction Log

### Friction Item 1

**Classification:** Type D — Cognitive Fatigue (large tracking item accumulating drift, not caught by a single mechanical grep)

**Recurrence:** Yes — appeared in 2026-07-27__release-v7.9 (BLG-OPS-111 staleness, Carry-Forward item 1)

**What happened:** The STEP 6 Endpoint Coverage Drift Check found 20 normalised endpoint gaps this run, against `BLG-OPS-111`'s originally-filed list of 21. Composition, not just count, has drifted: 4 endpoints named in `BLG-OPS-111` are now covered in `api_performance_baseline.md` (resolved since filing), while 3 endpoints not on `BLG-OPS-111`'s list are newly missing (`PATCH /watchlist/{entry_id}`, `POST /alerts/rules`, `POST /settings` — all pre-existing endpoints, not introduced this cycle). Per routine, `BLG-OPS-111`'s body was not edited (outside write scope); the delta is recorded in the closure record and Advisory Summary instead.

**Where in the routine:** STEP 6 — Endpoint Coverage Drift Check (advisory)

**Root cause:** process gap — no mechanism re-derives `BLG-OPS-111`'s own endpoint list against the live gap at each cycle; it is a point-in-time snapshot from v7.2 that successive cycles can only append delta notes onto, not correct.

**Blast radius analysis:**
- What would have propagated: nothing incorrect this cycle — the delta is explicitly recorded, not silently absorbed.
- When it would have surfaced: the drift compounds every cycle it goes unreconciled; eventually the delta notes become harder to reconstruct than the tracking item itself.
- Recovery cost if uncaught: low today, rising over time (medium within a few more cycles if left unreconciled).

**Process patch:**
→ Deferred patch (cannot apply this run):
  - File: `claude/backlog/backlog.md`
  - Section: `BLG-OPS-111` entry body
  - Change required: Reconcile `BLG-OPS-111`'s own endpoint list against the current live gap (add `PATCH /watchlist/{entry_id}`, `POST /alerts/rules`, `POST /settings`; remove the 4 now-covered endpoints — `GET /portfolio/pre-entry-validation`, `GET /trade-plans/tags`, `POST /ai/check-daily-cost`, `POST /test/endpoints`) the next time this item is actioned or groomed. Post-Ship Closure's backlog write scope is mark-shipped-complete / add-missing-Phase-4-items only — it does not permit editing an existing open item's body.
  - Owner: Infrastructure & Operations Owner (item's named owner)
  - Target: Next time `BLG-OPS-111` is actioned, or next `groom backlog` review of long-lived P3 items — whichever comes first

---

## Recurrence Escalations

None. Friction Item 1 recurs the same underlying pattern as v7.9's Carry-Forward item 1, but v7.9's own outstanding-actions table was empty (the item was a Carry-Forward observation, not an open deferred patch) — so there is no unresolved prior-cycle action to escalate against. Continuing to track via Carry-Forward is the correct disposition, per the item's own advisory-only, non-blocking nature.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | STEP 7 — Seal Execution Record | New pre-seal check: verify `completed_items` is the full cross-EPIC union of `done`/`merged` story IDs before writing `sealed: true` (closes Phase 4 friction item — v7.10's own sealed record listed only EPIC-04's 4 stories instead of all 23). | v3.60→v3.61 | Yes |
| `claude/system/backlog_management_prompt.md` | STEP 1 — new §1.3 | New Governance Prompt Duplicate Cross-Check: grep `prompt_change_log.md` for a matching version-transition entry before confirming a `BLG-GOV-*` item still open; flag probable-duplicate candidates for owner review (closes Phase 3 friction item — 3 of 23 v7.10 stories reached sprint execution already resolved by prior-sprint fixes). | v1.12→v1.13 | Yes |

Both changes additionally required OPERATIONAL_GUIDE.md §14 governance-table updates (v4.121→v4.123, two sequential bumps) and their respective dedicated changelog files, per CLAUDE.md §6.

---

## New files created this run

None (this file itself is the standard STEP 8.5 output).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/backlog/backlog.md` | `BLG-OPS-111` entry body | Reconcile the item's endpoint list against the current live gap (3 additions, 4 removals — see Friction Item 1). | Infrastructure & Operations Owner | Next time `BLG-OPS-111` is actioned, or next `groom backlog` long-lived-P3 review |

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-OPS-111`'s endpoint list has now drifted for a second consecutive cycle (v7.9: understated by 4; v7.10: 4 resolved + 3 new, net count down but composition still misaligned) — recurring, low-cost drift that nonetheless compounds if left unreconciled across further cycles. | If a third consecutive cycle finds `BLG-OPS-111`'s list still misaligned against the live gap, this should be escalated from an advisory delta note to a mandatory reconciliation action at that cycle's Post-Ship Closure STEP 6, rather than continuing to accumulate delta notes indefinitely. | Post-Ship Closure |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-07-28__release-v7.10",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-07-30T13:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 2,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
