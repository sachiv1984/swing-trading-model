# Phase Gate Document — {Feature Name}

**Owner:** PMO Lead
**Type:** PMO Process Template
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-20

---

## Purpose

This document is the single source of truth for the current status of a feature moving through pre-alignment and delivery. It is updated by the PMO Lead at every gate transition and shared with all stakeholders.

Its job is to ensure no one ever has to ask "what's happening?" or "what do I do next?" — the answer is always in this document, and it is always current.

One Phase Gate Document is created per feature at the start of Phase 0 and closed at shipping. It is filed at `docs/product/phase_gates/{id}-{slug}-phase-gate.md`.

---

## How to Use

**PMO Lead:** Update this document every time a gate passes, a blocker clears, or a status changes. Do not wait for someone to ask. If the document is more than 24 hours stale during an active phase, it is out of date.

**All other roles:** Check this document first before asking the PMO Lead for a status update. If something is missing or wrong, flag it to the PMO Lead immediately.

---

## Feature Summary

| Field | Value |
|-------|-------|
| Feature | {roadmap item id} — {feature name} |
| Roadmap entry | `docs/product/roadmap.md §{id}` |
| Target release | {version} |
| PMO Lead | PMO Lead |
| Date opened | {date} |
| Date shipped | {date or —} |

---

## Current Status

```
Current phase:    {Phase 0 / 1 / 2 / 3 / 4 / Implementation / Phase 5 / Shipped}
Gate passed:      {date or —}
Next gate:        {what the next gate is}
Who acts next:    {role}
What they do:     {one sentence}
Deadline:         {date or "as soon as possible"}
Blockers:         {None / description}
```

---

## Phase History

| Phase | Gate condition | Status | Date | Notes |
|-------|---------------|--------|------|-------|
| Phase 0 — Readiness Audit | Audit complete, Go/No-Go issued | ⬜ Not started | — | |
| Phase 1 — Pre-Alignment Meeting | All decisions closed, decisions record committed | ⬜ Not started | — | |
| Phase 2 — Parallel Spec Delivery | All spec actions complete and committed | ⬜ Not started | — | |
| Phase 3 — QA Review Gate | QA sign-off confirmed | ⬜ Not started | — | |
| Phase 4 — Scope Document | Scope document committed, implementation declared open | ⬜ Not started | — | |
| Implementation | Engineering builds against locked specs | ⬜ Not started | — | |
| Phase 5 — Verification | All criteria pass, Director of Quality final sign-off | ⬜ Not started | — | |
| Shipping Closure | Changelog, roadmap, supersession actions complete | ⬜ Not started | — | |

Status key: ⬜ Not started &nbsp;|&nbsp; 🟡 In progress &nbsp;|&nbsp; ✅ Complete &nbsp;|&nbsp; 🔴 Blocked

---

## Action Register

The PMO Lead maintains this table throughout the feature. Every open action has an owner and a status.

| # | Action | Owner | Status | Blocked on | Due |
|---|--------|-------|--------|------------|-----|
| | | | | | |

---

## Stakeholder Next Steps

This section is rewritten at every gate. It always describes what each relevant role needs to do right now. If a role is not listed, they have no current action.

**As of {date}:**

| Role | Action | By when |
|------|--------|---------|
| {Role} | {What they need to do} | {Date} |

---

## Open Blockers

| # | Blocker | Affects | Owner | Raised | Status |
|---|---------|---------|-------|--------|--------|
| | | | | | |

If there are no open blockers, state: **No open blockers.**

---

## Defect & Observation Register

Populated during Phase 5 (verification). The PMO Lead does not own this — the QA Lead maintains the verification report. This is a summary for stakeholder visibility.

| ID | Severity | Summary | Status |
|----|----------|---------|--------|
| | | | |

---

## Decisions Record Reference

Pre-alignment decisions: `docs/product/decisions/{id}-{slug}.md`

Key decisions summary (for stakeholder orientation — full rationale in decisions record):

| # | Decision | Confirmed by |
|---|----------|-------------|
| | | |

---

## Shipping Closure Checklist

Completed by PMO Lead once Director of Quality final sign-off is confirmed.

- [ ] Changelog entry added (`docs/product/changelog.md`)
- [ ] Roadmap updated — status → ✅ Complete, version bumped
- [ ] Scope document status → Superseded
- [ ] Decisions record status → Superseded
- [ ] Head of Engineering notified
- [ ] Lessons learnt review scheduled
- [ ] This phase gate document status → Shipped, date filed

---

## Template Usage Notes

**File location:** `docs/product/phase_gates/{roadmap-item-id}-{feature-slug}-phase-gate.md`

**When to create:** At the start of Phase 0 (readiness audit). Not after the meeting — before.

**When to close:** When shipping closure is complete and all checklist items above are ticked.

**Retention:** Filed permanently. Phase gate documents are not deleted or archived — they provide a complete per-feature delivery record.
