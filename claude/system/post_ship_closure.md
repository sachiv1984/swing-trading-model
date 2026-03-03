# Post-Ship Closure

**Owner:** PMO Lead  
**Type:** PMO Process Template  
**Status:** Canonical  
**Version:** 2.0  
**Last Updated:** 2026-03-03  
**Playbook Reference:** `claude/system/OPERATIONAL_GUIDE.md` v1.3  

---

## Purpose

Run this process after Phase 4 (Delivery Verification) completes with a `Verified` or `Verified_with_deviations` status. Its job is to ensure all planning, operational, and governance documents are updated to reflect the closed state of the release before the next cycle opens.

A release is not fully delivered until its documentation is closed. Stale planning documents, unclosed backlog items, missing changelog entries, and unfiled lessons learnt are process debt that compounds across releases.

---

## When to Run

- Triggered by the PMO Lead immediately after `.claude_current_state.json` status = `Verified` or `Verified_with_deviations`
- Must be complete before the next cycle's Phase 1 or Phase 1B is invoked
- Applies to every shipped release, including releases that contain tech backlog items alongside a primary feature
- The `next_cycle_unblocked = true` flag in `.claude_current_state.json` is a necessary but not sufficient condition — this closure process must also be complete before the next cycle opens

---

## Inputs Required

Before running the closure sweep, collect:

- `.claude_current_state.json` — confirm `status = Verified` or `Verified_with_deviations` and `next_cycle_unblocked = true`
- `claude/cycles/<cycle_id>/verification_report.md` — the definitive record of what passed, what deviated, and any accepted items
- `claude/cycles/<cycle_id>/sprint_close.md` — outcomes, returned items, deviations filed
- `claude/cycles/<cycle_id>/execution_state.json` — sealed item list with spec references and delegation outcomes
- `claude/cycles/<cycle_id>/lessons_learnt.md` — Release Planning lessons (Phase 1B)
- `claude/cycles/<cycle_id>/lessons_learnt_execution.md` — Sprint Execution lessons (Phase 3)
- `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` — one per merged EPIC
- `docs/System_status_report.md` — confirmed current by Phase 4
- The roadmap item ID, release version, and feature name
- Any tech backlog items that shipped alongside the primary feature

---

## Closure Checklist

### 1. Changelog

- [ ] Has a changelog entry been written for this release version?
- [ ] Does the entry cover: all EPICs merged this sprint (with EPIC IDs), all spec versions updated, all canonical spec deviations accepted (P1/P2 with rationale references), and the verification report reference?
- [ ] If any tech backlog items shipped alongside the feature: are they recorded as distinct sub-sections within the same version entry?
- [ ] Does the entry reference the `cycle_id` and the `verification_report.md` path?
- [ ] Is `Last Updated` on `docs/product/changelog.md` set to today's date?

**Failure condition:** Missing changelog entry. The changelog is the permanent delivery record — a ship without an entry is not recorded.

**What the entry must include:**

```
## v<X.Y> — <feature name> — <ship date>
Cycle: <cycle_id>
Verified: <Verified | Verified_with_deviations>
Verification report: claude/cycles/<cycle_id>/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-xx | <description> | <spec file#section> |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-ref | P1/P2/P3 | <one line> | PO / PO + DoQ |

### Tech backlog items shipped
- [ST-xx] <title> — <one line description>

Sign-off: Product Owner — <date>
QA sign-off: Director of Quality — <date>
```

---

### 2. Roadmap

- [ ] Is the feature's roadmap entry in `claude/roadmap/current_roadmap.md` updated to **✅ Complete** with the ship date and `cycle_id` reference?
- [ ] Has the "Current Version" header been updated to reflect the shipped version?
- [ ] Has the "Next planned release" header been updated to the next version?
- [ ] If the shipped release contained quality gate items (e.g. P0/P1 tech backlog items): are those marked complete within their roadmap section?
- [ ] Is the release summary table current?
- [ ] Is `Last Updated` on `claude/roadmap/current_roadmap.md` set to today's date?

**Failure condition:** Roadmap still shows feature as Planned or In Progress after ship. Stale roadmap status erodes trust in the document and will cause Phase 1 (Roadmap Rebalance) to misread the current state.

---

### 3. Backlog

- [ ] Are all shipped backlog items (tech and feature) marked **✅ COMPLETE** in `claude/backlog/backlog.md` with closure date and `cycle_id` reference?
- [ ] Are all items returned to backlog during this sprint (per `sprint_close.md`) confirmed present with context and `cycle_id` reference?
- [ ] Are all P2/P3 deviation backlog items (added by Phase 4) confirmed present?
- [ ] Are all test scenario gap backlog items (added by Phase 4) confirmed present?
- [ ] Do items assigned to the next release have their target release noted?
- [ ] Is `Last Updated` on `claude/backlog/backlog.md` set to today's date?

**Failure condition:** Shipped item still shown as open. Items added by Phase 4 engines missing from backlog.

---

### 4. Scope Document

- [ ] Has the scope document status been updated from **Active** to **Superseded**?
- [ ] Does the supersession note reference: the changelog entry, the `verification_report.md` path, and the `cycle_id`?
- [ ] Is `Last Updated` on the scope document set to today's date?

Location: `docs/product/scope/scope--{id}-{slug}.md`

**Failure condition:** Scope document still Active after ship. Per lifecycle guide §4: scope documents must be updated to Superseded when the feature ships.

---

### 5. Decisions Record

- [ ] Has the decisions record status been updated from **Active** to **Superseded**?
- [ ] Does the supersession note reference the changelog entry and `cycle_id`?
- [ ] Is `Last Updated` on the decisions record set to today's date?

Location: `docs/product/decisions/{id}-{slug}.md`

**Note:** Any Accepted Risk decision records (`AR-<release>-<cycle_id>-<esc_id>.md`) created during this cycle are Operational Records (Class 3) — they do not get Superseded; they are permanent. Confirm they are filed and linked from the changelog entry.

**Failure condition:** Decisions record still Active after ship.

---

### 6. Canonical Specs — Deviation Notes

- [ ] For each deviation filed this sprint (listed in `sprint_close.md`): confirm the deviation entry in the relevant canonical spec contains all required fields: description, canonical requirement, priority (P0–P3), target resolution release, owner, and backlog reference.
- [ ] Are P3 deviations noted in the changelog entry?
- [ ] Are accepted P1/P2 deviations referenced in both the changelog entry and the `verification_report.md` acceptance block?

**Failure condition:** Deviation note in spec missing required fields. This renders the spec non-compliant per §3 Known Deviation Standard.

---

### 7. Supporting Operational Documents

For each operational document that references metrics, validation, or system behaviour affected by this release:

- [ ] Are metric counts, expected values, and example outputs current?
- [ ] Are any "planned" or "backlog" notes in operational docs updated to reflect what actually shipped?
- [ ] Does `docs/System_status_report.md` reflect the final verified status for this cycle (confirmed by Phase 4 — if Phase 4 made corrections, verify those corrections are present)?

**Common documents to check:**
- `docs/System_status_report.md` — capabilities live, deviations, test scenarios referenced
- `docs/operations/validation_system.md` — metric list, counts, severity assignments, example summaries
- Any status report that references the affected feature

---

### 8. Specs Index — Open Items Review

- [ ] Review `docs/specs/Specs_Index.md` Section 6 (Pending Spec Work) and Section 7 (Open Compliance Issues)
- [ ] Have any items been resolved by this release? If so, mark them resolved with date and `cycle_id`.
- [ ] Have any new gaps been identified during this delivery (from `qa_evidence_EPIC-xx.md` or the `verification_report.md`) that should be added?
- [ ] Is `Last Updated` on the Specs Index set to today's date if changes were made?

---

### 9. Lessons Learnt — Review and Apply

This release produces **two** lessons learnt records that must both be reviewed:

| Record | Location | Covers |
|--------|----------|--------|
| Release Planning lessons | `claude/cycles/<cycle_id>/lessons_learnt.md` | Phase 1B planning friction, escalation patterns, backlog quality |
| Sprint Execution lessons | `claude/cycles/<cycle_id>/lessons_learnt_execution.md` | Delegation patterns, GitHub integration, acceptance criteria gaps, gate friction |

For each record:

- [ ] Has each action item been reviewed by the PMO Lead?
- [ ] For actions that can be resolved by updating a template, prompt, or process document: has that update been made and the version bumped?
- [ ] For actions requiring a role decision (e.g. classification change, authority boundary question): has it been surfaced to the relevant owner with a deadline?
- [ ] Is there a consolidated action log noting which items were applied immediately, which are deferred to next cycle, and which require escalation?
- [ ] Have any process improvements applied during this closure been noted so they are visible before the next cycle opens?

**Failure condition:** Lessons learnt filed but not reviewed. Per the lessons learnt template: process debt compounds if this step is skipped. Filing without reviewing is equivalent to skipping.

---

## Outputs

When all checklist items are complete, the PMO Lead communicates to the Product Owner and Head of Specs Team:

```
Post-ship closure complete — <cycle_id> — <date>

Release: v<X.Y> — <feature name>
Verification status: <Verified | Verified_with_deviations>

Documents updated:
  ✅ Changelog — docs/product/changelog.md
  ✅ Roadmap — claude/roadmap/current_roadmap.md
  ✅ Backlog — claude/backlog/backlog.md
  ✅ Scope document — <path> → Superseded
  ✅ Decisions record — <path> → Superseded
  ✅ Canonical spec deviations — confirmed compliant
  ✅ System status report — confirmed current
  ✅ Specs Index — reviewed

Lessons learnt applied:
  Immediate actions applied: <N> (<list or "none">)
  Deferred to next cycle: <N> (<list or "none">)
  Escalated for decision: <N> (<list or "none">)

Outstanding actions carried forward: <list or "none">

Next cycle may now open.
```

---

## Escalation

If a document owner has not made their required update and it is blocking closure:

- PMO Lead notifies the owner directly with the specific item and a 24-hour deadline
- If unresolved within 24 hours: escalate to Product Owner
- PMO Lead does not make content changes to documents outside their ownership — they coordinate and escalate
- The next cycle does not open until closure is confirmed, regardless of delivery pressure

---

## Relationship to Playbook Phases

```
Phase 3 (Sprint Execution & Close)
  └─► Phase 4 (Delivery Verification)
        └─► .claude_current_state.json → Verified
              └─► Post-Ship Closure  ◄── YOU ARE HERE
                    └─► Phase 1 (Roadmap Rebalance, optional)
                          └─► Phase 1B (Release Planning — next cycle)
```

Phase 4 sets `next_cycle_unblocked = true` but does not perform document closure. This process is the bridge between a verified sprint and a clean next cycle.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.0 | 2026-03-03 | Full rewrite to align with Sprint Planning Operational Playbook v1.3. Added cycle artefact inputs (verification_report.md, sprint_close.md, execution_state.json, lessons_learnt_execution.md). Split lessons learnt into two records (Phase 1B and Phase 3). Added changelog entry template. Updated all document paths to match playbook conventions (claude/roadmap/, claude/backlog/). Added canonical spec deviation check. Added explicit sequencing diagram. Added Accepted Risk decision record note. Removed trigger dependency on generic ship sign-off — now triggers on Phase 4 Verified state. |
| 1.0 | 2026-02-21 | Initial version. Created as a result of lessons learnt for 3.2 Position Sizing Calculator — post-ship document sweep had no template and was reconstructed by audit. |