# Post-Ship Closure

**Owner:** PMO Lead
**Type:** PMO Process Template
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-21

---

## Purpose

Run this process when the Product Owner confirms ship sign-off for a feature. Its job is to ensure all planning and operational documents are updated to reflect the closed state of the feature before the next feature enters pre-alignment.

A feature is not fully delivered until its documentation is closed. Stale planning documents, unclosed backlog items, and missing changelog entries are process debt that compounds across releases.

---

## When to Run

- Triggered by the PMO Lead when the Product Owner confirms ship sign-off
- Must be complete before the next feature's readiness audit begins
- Applies to every shipped feature, including tech backlog items that ship alongside a primary feature

---

## Inputs Required

Before running the closure sweep, collect:

- The ship sign-off confirmation (date, who signed off)
- The roadmap item ID and feature name
- The scope document location
- The decisions record location
- Any tech backlog items that shipped alongside this feature

---

## Closure Checklist

### 1. Changelog

- [ ] Has a changelog entry been written for this release version?
- [ ] Does the entry cover: all backend changes, all frontend changes, all canonical spec versions updated, and sign-off detail?
- [ ] If any tech backlog items shipped alongside the feature: are they recorded as distinct sub-sections within the same version entry?
- [ ] Is `Last Updated` on `docs/product/changelog.md` set to today's date?

**Failure condition:** Missing changelog entry. The changelog is the permanent delivery record — a ship without an entry is not recorded.

---

### 2. Roadmap

- [ ] Is the feature's roadmap entry updated to **✅ Complete** with the ship date and sign-off reference?
- [ ] Has the "Current Version" header in the roadmap been updated to reflect the shipped version?
- [ ] Has the "Next planned release" header been updated to the next version?
- [ ] If the shipped version contained quality gate items (e.g. tech backlog P0s): are those marked complete within their roadmap section?
- [ ] Is the release summary table at the bottom of the roadmap current?
- [ ] Is `Last Updated` on `docs/product/roadmap.md` set to today's date?

**Failure condition:** Roadmap still shows feature as Planned or In Progress after ship. Stale roadmap status erodes trust in the document.

---

### 3. Backlog

- [ ] Are all shipped backlog items (tech and feature) marked **✅ COMPLETE** with closure date and evidence?
- [ ] Do items that are now assigned to the next release have their target release noted?
- [ ] Is `Last Updated` on `docs/product/backlog.md` set to today's date?

**Failure condition:** Shipped item still shown as open in backlog.

---

### 4. Scope Document

- [ ] Has the scope document status been updated from **Active** to **Superseded**?
- [ ] Does the supersession note reference the changelog entry for the shipped version and the verification report?
- [ ] Is `Last Updated` on the scope document set to today's date?

Location: `docs/product/scope/scope--{id}-{slug}.md`

**Failure condition:** Scope document still Active after ship. Per lifecycle guide §4: scope documents must be updated to Superseded when the feature ships.

---

### 5. Decisions Record

- [ ] Has the decisions record status been updated from **Active** to **Superseded**?
- [ ] Does the supersession note reference the changelog entry for the shipped version?
- [ ] Is `Last Updated` on the decisions record set to today's date?

Location: `docs/product/decisions/{id}-{slug}.md`

**Failure condition:** Decisions record still Active after ship.

---

### 6. Supporting Operational Documents

For each operational document that references metrics, validation, or system behaviour affected by this feature:

- [ ] Are metric counts, expected values, and example outputs current?
- [ ] Are any "planned" or "backlog" notes in operational docs updated to reflect what actually shipped?
- [ ] Does `docs/operations/validation_system.md` reflect the current validated metric list and counts?

**Common documents to check:**
- `docs/operations/validation_system.md` — metric list, counts, severity assignments, example summaries
- Any status report that may reference the affected feature

---

### 7. Specs Index — Open Items Review

- [ ] Review `docs/specs/Specs_Index.md` Section 6 (Pending Spec Work) and Section 7 (Open Compliance Issues)
- [ ] Have any items been resolved by this ship? If so, mark them resolved with date.
- [ ] Have any new gaps been identified during this delivery that should be added?
- [ ] Is `Last Updated` on the Specs Index set to today's date if changes were made?

---

### 8. Lessons Learnt

- [ ] Has the lessons learnt review been run per `processes/lessons_learnt.md`?
- [ ] Has the lessons learnt record been filed at `docs/product/lessons_learnt/{id}-{slug}-lessons.md`?
- [ ] Have all process improvement actions been actioned (templates updated, versions bumped)?

**Failure condition:** Lessons learnt skipped. Per the lessons learnt template: process debt compounds if this step is skipped.

---

## Outputs

When all checklist items are complete, communicate to the Product Owner and Head of Specs Team:

- Feature `{name}` post-ship closure complete as of `{date}`
- All planning documents updated to Superseded
- Changelog entry confirmed
- Lessons learnt filed at `{path}`
- Any outstanding actions: `{list or "none"}`

---

## Escalation

If a document owner has not made their required update and it is blocking closure:

- PMO Lead notifies the owner directly with the specific item and deadline
- If unresolved within 24 hours: escalate to Product Owner
- PMO Lead does not make content changes to documents outside their ownership — they coordinate and escalate

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-02-21 | Initial version. Created as a result of lessons learnt for 3.2 Position Sizing Calculator — post-ship document sweep had no template and was reconstructed by audit. |