**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-24
**Cycle:** 2026-03-21__release-v2.2

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v2.2 Security, Alert Maturity & Quality — post-ship closure
Run: 2026-03-21__release-v2.2
Reviewed by: PMO Lead
Date filed: 2026-03-24
Prior cycle closure file checked: `claude/cycles/2026-03-18__release-v2.1/lessons_learnt_closure.md` — not found. Recurrence check not possible.

---

## What Worked Well

- **All 8 deferred lessons items were well-specified:** Each deferred patch from Release Planning, Phase 3, and Phase 4 had a named owner (Head of Specs Team) and a concrete file/section target. No ambiguous "we should improve X" entries to escalate.
- **Verification report §4 deviation register was comprehensive:** P2 acceptance records for DEV-HEALTH-001 and DEV-EPIC02-ST05-02 included rationale, confirmed backlog items, and dual sign-off (PO + DoQ) — STEP 5 deviation compliance check required only two minor backlog reference corrections.
- **Changelog entry quality:** The v2.2 changelog entry produced at STEP 1 contained all required fields: EPIC table with spec references, accepted deviations, backlog items shipped, and dual sign-off dates. No corrections required at STEP 5.
- **Specs Index §9 gaps were fully resolved:** TSG-v21-01 and TSG-v21-02 (both deferred from v2.1 verification) were closed by v2.2 delivery (ST-09, ST-10). Zero v2.1 gaps remain open except TSG-v21-03 (slippage scenarios — not in v2.2 scope).

---

## Friction Log

---

### Friction Item 1

**Classification:** Type C — Dependency Stall: Canonical spec deviation notes filed before backlog item IDs are known

**Recurrence:** Not checkable (no prior closure file)

**What happened:**
At STEP 5 deviation compliance check, two spec deviation entries had stale or incorrect backlog references. `notifications.md` DEV-EPIC02-ST04-01 referenced "to be filed as BLG-FE item at next roadmap rebalance" — but BLG-FE-04 had been created during delivery verification. `health_endpoints.md` DEV-HEALTH-001 referenced BLG-OPS-06 (the delivered health endpoint) rather than BLG-SPEC-D14 (the spec update backlog item filed by the verification engine). Both corrections were applied at STEP 5.

**Where in the routine:** STEP 5 — Canonical Spec Deviation Compliance Check

**Root cause:** Process gap — the execution engine files deviation notes in canonical specs (Phase 3) before the verification engine creates backlog items for those deviations (Phase 4). There is no synchronisation step between the two; the deviation note is written with a placeholder or a pre-existing item ID that may later be superseded.

**Blast radius analysis:**
- What would have propagated: Spec deviation notes with wrong backlog references would remain stale until the next spec review cycle; traceability from deviation → backlog item would be broken for BLG-SPEC-D14 and BLG-FE-04.
- When it would have surfaced: Next `run audit` or next sprint touching those spec files.
- Recovery cost if uncaught: Low — single field update per deviation entry; no functional impact.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/delivery_verification_prompt.md`
  - Section: STEP 3 (Deviation Register / Backlog item creation)
  - Change required: When the delivery verification engine creates a new backlog item for a deviation (e.g. BLG-FE-04, BLG-SPEC-D14), it should also update the `Backlog reference` field in the corresponding canonical spec deviation entry in the same session — preventing the stale-reference pattern that requires a closure fix.
  - Owner: Head of Specs Team
  - Target: 2026-03-21__release-v2.3 Sprint 1

---

## Recurrence Escalations

None.

---

## Process improvements actioned this run

None applied this run. All patches deferred.

---

## New files created this run

None.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/delivery_verification_prompt.md` | STEP 3 (Deviation Register) | When creating a backlog item for a deviation, also update the `Backlog reference` field in the canonical spec deviation entry in the same session | Head of Specs Team | 2026-03-21__release-v2.3 Sprint 1 |
| `claude/system/backlog_management_prompt.md` | Health Check step | Add ID uniqueness scan: flag active items with IDs matching closed items table (LL-RP-v22-01) | Head of Specs Team | Before next `groom backlog` run |
| `claude/system/execution_prompt.md` | STEP 3.1.A (post-merge confirmation) | Add substep: "update delegation log entry status to Unblocked" — prevents bulk rework at sprint close | Head of Specs Team | 2026-03-21__release-v2.3 |
| `claude/system/execution_prompt.md` | STEP 4 merge gate completion block | Add advisory: "When merge_gate.all_merged=true, STEP 5 Sprint Close must be invoked before delivery verification can proceed" | Head of Specs Team | 2026-03-21__release-v2.3 |
| `claude/system/execution_prompt.md` | §9 invariants | Reinforce: "Backend commits tightly coupled to a delegated_frontend story must land on the same EPIC branch unless explicitly authorised as direct-to-main by PMO Lead" (DEV-EPIC02-ST05-02) | Head of Specs Team | 2026-03-21__release-v2.3 |
| `claude/system/sprint_planning_prompt.md` | Sprint scope gate or advisory | Add note: "blocked_decision items with no HoST design authored should have a design session scheduled before sprint start to reduce mid-sprint overhead" | Head of Specs Team | 2026-03-21__release-v2.3 |
| `claude/system/execution_prompt.md` | §9.1 schema note | For delegated_qa documentation artefacts and autonomous infrastructure items with no prior spec, `spec_references` may be left empty with a note field value of "no prior spec applicable" | Head of Specs Team | 2026-03-21__release-v2.3 |
| `claude/system/execution_prompt.md` | STEP 3.1.A (QA evidence authoring) | When a test gap is identified in a delegated_qa item and the corresponding implementation story is not yet done, QA evidence should note "pending ST-xx completion" rather than flagging as a P1 gap | Head of Specs Team | 2026-03-21__release-v2.3 |

---

## Escalations

None.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Sprint planning scheduled `blocked_decision` items (ST-13/14/15) without a prior HoST design session, requiring full design sessions mid-sprint and adding session overhead | Sprint planning should surface an advisory when blocked_decision items are scheduled with no design artefact present: "HoST design session should precede sprint start for delegated_decision items" | Sprint Planning |
| 2 | The execution engine's delegation log was not updated in-flight (10 entries remained "Pending" until bulk update at sprint close) | Sprint planning or execution prompt should remind: delegation log entries must be updated to Unblocked/Cancelled at the point of merge confirmation, not batched at sprint close | Sprint Planning |
| 3 | `backlog_management_prompt.md` ID uniqueness scan was not in place (LL-RP-v22-01), allowing a duplicate BLG-BE-02 ID to go undetected until release planning advisory | The backlog grooming engine should run an ID uniqueness scan and flag any active item ID that already appears in the closed items table | Release Planning |
