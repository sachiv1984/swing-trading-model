**Owner:** Head of UX & Design
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-05
**Cycle:** 2026-05-05__release-v3.2
**Approved by:** Product Owner — 2026-05-05
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Pre-Trade Entry Checklist (EPIC-02: ST-05, ST-06)

## Purpose

This document defines the layout, interaction model, and design decisions for the Pre-Trade Entry Checklist component embedded in the Trade Plan form/flow. It is the authoritative design source for the checklist section of `docs/specs/frontend/pages/trade_plan.md`.

---

## Component Overview

The entry checklist is a lightweight advisory component embedded in the Trade Plan creation and edit forms. It surfaces four pre-trade hygiene checks. Checklist state is persisted as part of the Trade Plan record. The checklist is advisory — items are not required to be checked before saving.

---

## Checklist Items

| Item ID | Label | Pre-population trigger | Source field |
|---------|-------|----------------------|-------------|
| CHK-01 | Strategy signal confirmed | Automatic — always unchecked | Manual only |
| CHK-02 | Position size within heat limits | Not pre-populated | Manual only |
| CHK-03 | Stop level defined | Auto-check if `stop_level` is non-null in the trade plan | `stop_level` |
| CHK-04 | Pre-trade research reviewed | Auto-check if `risk_reward_notes` is non-null (any text present) | `risk_reward_notes` |

**Pre-population is advisory:** pre-populated items may be unchecked by the user. Existing user-set state is never overwritten on re-open.

---

## Component Layout (within Trade Plan form)

```
┌──────────────────────────────────────────┐
│  PRE-TRADE CHECKLIST                     │
│                                          │
│  [✓] Strategy signal confirmed           │
│  [ ] Position size within heat limits    │
│  [✓] Stop level defined                  │
│  [✓] Pre-trade research reviewed         │
│                                          │
│  Review research →                       │
│  (links to /research/{ticker})           │
└──────────────────────────────────────────┘
```

- Rendered as a grouped section within the Trade Plan form, below the core plan fields (ticker, stop level, notes)
- Section heading: "Pre-Trade Checklist"
- Each item: checkbox + label, single line
- All items visible regardless of check state

---

## "Review Research" Link (ST-06)

- Label: "Review research →" (arrow indicates navigation)
- Placement: below checklist items, right-aligned or below last item
- Target: `/research/{ticker}` where ticker is the Trade Plan's ticker
- Visible in both creation and edit modes
- Not visible if the trade plan has no ticker yet (creation form before ticker is entered)

---

## Read-Only State (Trade Plan Detail View)

When the trade plan is in detail/view mode (not editing):

- Checklist items shown as read-only indicators (checked/unchecked icons, not interactive checkboxes)
- "Review research" link remains active
- Section heading unchanged: "Pre-Trade Checklist"

---

## Persistence

- Checklist state (array of `{item_id, checked: bool}`) stored as part of the Trade Plan record
- Submitted with Trade Plan create/update via `POST /trade-plans` / `PUT /trade-plans/{id}`
- Backend schema: `checklist` field as array (see execution stories for schema definition)

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Checklist is advisory, not gating | Prevents friction when users have valid reasons to leave items unchecked; plan can be saved at any state |
| Pre-population is one-way (auto-check only) | Reduces manual overhead; user retains ability to uncheck if they disagree |
| 4-item minimum | Covers the core pre-trade discipline without being overwhelming; extensible in future |
| "Review research" link persistent | Always-accessible navigation to research view from within the checklist context |
| Checklist stored on trade plan record | Allows QA/reflection review of discipline adherence per plan in future |

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-05 | Initial design gate artefact for v3.2 EPIC-02 (ST-05, ST-06). Approved by Product Owner 2026-05-05. |
