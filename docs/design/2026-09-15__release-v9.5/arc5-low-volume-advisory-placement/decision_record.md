**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-15__release-v9.5
**Story:** ST-43 (EPIC-06, BLG-UX-05)

# Decision Record — Arc5ComplianceSection Low-Trade-Volume Advisory: Threshold Disclosure + Placement

## 1. Problem

The v9.2 low-trade-volume advisory (`docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/decision_record.md`) tells the user the compliance figures are indicative but never states the actual threshold (20 closed trades) or how many more trades are needed before the figures are considered fully reliable. It also renders below the four stat cards, so the user reads the (potentially low-confidence) numbers before the caveat that qualifies them. `BLG-UX-05`, filed from ST-26's (v9.4) usability review, asks Head of UX & Design to decide whether either gap is worth closing.

## 2. Decision

Both changes are worth making — they are low-cost (copy + a container reorder, no new component) and directly address a real usability finding (caveat read after the numbers it qualifies).

### 2.1 Copy — add threshold + remaining-trades count

Change the advisory body from:

> `"Based on {N} closed trade(s) — treat these figures as indicative until more trade history accumulates."`

to:

> `"Based on {N} closed trade(s) — treat these figures as indicative until more trade history accumulates. Reliability improves at 20+ closed trades ({20-N} more needed)."`

**Compatibility constraint (deliberate):** the AC requires existing Playwright coverage (`tests/e2e/arc5-compliance-section.spec.js`, `SC-ARC5-09`) to still pass without modification. That test asserts `toContainText('Based on 12 closed trades')` and `toContainText('indicative until more trade history accumulates')` as two independent substring checks. The new copy is constructed as a pure append after the original sentence, preserving both substrings verbatim — no wording inside the existing sentence changes. `{20-N}` is computed from the same `total_closed_trades` value already driving the component; no new prop or fetch.

### 2.2 Placement — move above the stat grid

Move the advisory banner from beneath the four-card grid to a full-width row above it (still inside `Arc5ComplianceSection`'s own container, not a page-level `StandingAlertStack` entry — that part of the v9.2 decision is unchanged). Rationale: the caveat should be read before the numbers it qualifies, not after. Confirmed no existing Playwright assertion depends on DOM order relative to the grid (`SC-ARC5-09`/`SC-ARC5-10a/b/c` all query the advisory by its own `data-testid`, independent of sibling order) — the reorder is safe against existing coverage.

### 2.3 Unchanged

Visual tone/token (`StandingAlert` Info tone), `data-testid="arc5-low-volume-advisory"`, the `< 20` threshold trigger condition, non-dismissible/static behaviour, and hidden-when-loading/error/null/absent handling — none of this is affected by the AC.

## 3. §13 Compliance

Same basis as the v9.2 decision this extends: purely a display-confidence caveat on already-computed, already-approved compliance statistics — no new computation, no recommendation. Does not introduce or extend any AI-provider call — §13 boundary pre-check (STEP 1) does not apply.

## 4. Frontend Spec Impact

`docs/specs/frontend/components/arc5_compliance_section.md` §Low-Trade-Volume Advisory updated this gate (v1.3.0 → v1.4.0): new copy string, placement moved above the stat grid, cross-reference to this decision record added alongside the existing v9.2 one.

## 5. Approval

Head of UX & Design: confirmed, 2026-09-15.
Product Owner: confirmed, 2026-09-15.
