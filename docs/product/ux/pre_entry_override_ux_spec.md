**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Class:** Specification Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-10
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Backlog ref:** BLG-FE-56
**Cycle:** 2026-06-09__release-v5.4 (ST-02, EPIC-02)

---

# Pre-Entry Panel Override Acknowledgement UX Specification

## 1. Purpose

This specification separates the override acknowledgement flow for `warn` and `fail` check results in `PreEntryValidationPanel`. The current implementation uses a single checkbox for both severity levels. This document defines distinct flows so that strategy violations (`fail`) require a deliberate additional step, while advisory warnings (`warn`) preserve the existing checkbox flow.

**Predecessor:** `docs/product/ux/pre_entry_panel_ux_assessment.md` (BLG-FE-49, v4.7) identified the single-acknowledgement pattern as an improvement candidate.

**Implementation note:** This story produces a specification/design output. Frontend implementation (code changes to `PreEntryValidationPanel`) is a separate follow-on story requiring Product Owner approval.

---

## 2. Severity Classification

| Severity | Meaning | Examples |
|----------|---------|---------|
| `warn` | Advisory — strategy preference not met; trade may proceed with acknowledgement | Sector concentration, earnings proximity |
| `fail` | Strategy hard stop — fundamental rule violated; override is deliberate deviation from own strategy | Cash constraint exceeded, regime gate failed, position size limit exceeded |
| `pass` | No issue — check cleared | All passing checks |
| `skipped` | Check could not run — missing data | Insufficient price data for proximity check |

---

## 3. Current Behaviour

All warn and fail checks share a single override checkbox:

```
☐  I acknowledge the advisory warnings
```

Checking this box unlocks the "Save Trade Plan" button regardless of whether the outstanding checks are `warn`, `fail`, or mixed. No distinction in acknowledgement effort is required between a minor advisory and a hard-stop violation.

---

## 4. Specified Behaviour

### 4.1 Warn-Only State (no `fail` checks outstanding)

**Current behaviour preserved.** Single checkbox acknowledgement remains appropriate for advisory-only warnings.

```
┌─────────────────────────────────────────────────────────────┐
│ ⚡ PRE-ENTRY CHECKS         [Warn]         [↓ collapse]     │
├─────────────────────────────────────────────────────────────┤
│ ✓  Regime Gate                                              │
│ ⚠  Sector Concentration — 2 positions in Energy sector      │
│                                                             │
│ ☐  I acknowledge the advisory warnings                      │
│    [Save Trade Plan — disabled until checked]               │
└─────────────────────────────────────────────────────────────┘
```

**Checkbox label:** "I acknowledge the advisory warnings"
**Button unlock:** Save is enabled once checkbox is checked.
**No change to current implementation for this path.**

---

### 4.2 Fail State (one or more `fail` checks outstanding)

The fail-state acknowledgement requires an explicit additional step. The simple checkbox alone is not sufficient when a `fail`-severity check is outstanding.

#### 4.2.1 Panel State

```
┌─────────────────────────────────────────────────────────────┐
│ ⚡ PRE-ENTRY CHECKS         [Fail]         [↓ collapse]     │
├─────────────────────────────────────────────────────────────┤
│ ✓  Regime Gate                                              │
│ ✗  Cash Constraint — Insufficient buying power ($4,200      │
│    available; trade requires $6,500)                        │
│ ⚠  Sector Concentration — 2 positions in Energy sector      │
│                                                             │
│ [Override Strategy Violation — button, red/warning style]   │
└─────────────────────────────────────────────────────────────┘
```

**Mechanism:** A single confirmation button (not a checkbox) labelled "Override Strategy Violation". Clicking this button triggers the confirmation modal (§4.2.2).

**Rationale:** A button is a more deliberate action than checking a checkbox. It requires a separate click intent and triggers a modal rather than silently enabling Save.

#### 4.2.2 Confirmation Modal

When the user clicks "Override Strategy Violation", a modal appears:

```
┌──────────────────────────────────────────────┐
│  Override Strategy Violation                  │
│                                              │
│  You are about to proceed with a trade plan  │
│  that violates one or more strategy rules:   │
│                                              │
│  • Cash Constraint — Insufficient buying     │
│    power ($4,200 available; requires $6,500) │
│                                              │
│  (any additional fail checks listed here)    │
│                                              │
│  Type OVERRIDE to confirm you understand     │
│  this trade deviates from your strategy.     │
│                                              │
│  [________________]  ← text input            │
│                                              │
│  [Cancel]        [Confirm Override]          │
│                 (disabled until OVERRIDE typed)│
└──────────────────────────────────────────────┘
```

**Confirmation requirement:** User must type the word `OVERRIDE` (case-insensitive) in the text field to enable the "Confirm Override" button. This provides a friction-proportionate barrier to accidental strategy violation.

**On confirmation:**
- Modal closes
- Save Trade Plan button is enabled
- A visible "Override acknowledged" badge or note is displayed in the panel (red badge or inline note)

**On cancel:** Modal closes; Save remains disabled; panel unchanged.

#### 4.2.3 Post-Confirmation Panel State

After the user confirms the override, the panel reflects the acknowledged state:

```
┌─────────────────────────────────────────────────────────────┐
│ ⚡ PRE-ENTRY CHECKS         [Fail]         [↓ collapse]     │
├─────────────────────────────────────────────────────────────┤
│ ✓  Regime Gate                                              │
│ ✗  Cash Constraint — Insufficient buying power              │
│ ⚠  Sector Concentration — 2 positions in Energy sector      │
│                                                             │
│ ⚠ Strategy violation override acknowledged                  │
│    [Save Trade Plan — enabled]                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 4.3 Mixed State (both `warn` and `fail` checks outstanding)

When both `warn` and `fail` severity checks are outstanding simultaneously, the fail-state modal flow governs. The modal lists all outstanding `fail` checks. The warn-only checkbox is suppressed (folded into the modal acknowledgement).

After override confirmation, the panel shows the "override acknowledged" state; the previously visible warn checkbox is not shown separately.

---

## 5. Interaction Summary

| State | Mechanism | Friction level | Rationale |
|-------|-----------|---------------|-----------|
| Pass only | Save enabled immediately | None | No issue |
| Warn only | Single checkbox | Low | Advisory; user should note but can proceed |
| Fail (any) | Button → modal → type OVERRIDE | High (deliberate) | Strategy hard stop; must be conscious decision |
| Mixed | Fail flow governs | High | Fail severity dominates |

---

## 6. UX Principles Applied

1. **Proportionate friction:** Friction scales with consequence. Advisory warnings do not need the same barrier as hard stops.
2. **Intent legibility:** The modal surface forces the user to read what they are overriding — the fail check detail is displayed explicitly.
3. **Type-to-confirm:** Used in high-stakes UX contexts (e.g., Stripe, GitHub destructive operations). Prevents accidental click-through.
4. **State persistence:** The acknowledged state is visible in the panel after confirmation, confirming to the user that override is recorded.

---

## 7. Implementation Notes (for follow-on story)

- `PreEntryValidationPanel` in `src/pages/TradePlan.js` — existing `hasOverrides` / checkbox logic to be extended.
- The `fail` detection needs to distinguish `fail`-severity checks from `warn`-severity checks — the check result payload already includes a `status` field (`pass`/`warn`/`fail`/`skipped`).
- Modal component: can use existing `Dialog`/`Modal` pattern in the codebase or a lightweight inline modal.
- The type-to-confirm input should accept `OVERRIDE` case-insensitively but display the word in uppercase in the hint text.
- Override confirmation should be stored in component state only (not persisted) — the trade plan save captures the intent at the point of save.

---

## 8. Acceptance Criteria (Spec Verification)

- [x] AC-01: Spec differentiates warn (advisory checkbox) from fail (strategy violation — modal + type-to-confirm)
- [x] AC-02: Fail override requires additional deliberate step (button → modal → typed confirmation)
- [x] AC-03: Warn-only flow preserved unchanged
- [x] AC-04: Spec signed off by Head of UX & Design and Frontend Specs & UX Documentation Owner
- [x] AC-05: Output filed in docs/product/ux/

---

## 9. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Head of UX & Design | Approved (agent-mediated) | 2026-06-10 |
| Frontend Specs & UX Documentation Owner | Approved (agent-mediated) | 2026-06-10 |
