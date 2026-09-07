**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-07__release-v9.2
**Story:** ST-01 (EPIC-01, BLG-FEAT-44)

# Decision Record — Arc5ComplianceSection Low-Trade-Volume Advisory

## 1. Problem

`Arc5ComplianceSection` computes compliance statistics (Red Flag Events/Week, Override Rate, Top Rule Breach, Trade Plan Adherence) from whatever closed-trade history exists, with no floor on sample size. At low trade counts these percentages are statistically noisy (e.g. a single override on 2 closed trades reads as a 50% Override Rate) but the component renders them with the same visual confidence as a mature 100-trade sample. ST-01's own AC #1 tasks the story with producing an assessment (during sprint execution) of whether this warrants a UI advisory. Because that assessment's conclusion is not yet known at gate time, this record fixes the **design** in advance — conditional on the assessment landing on "advisory warranted" — so the story is not blocked waiting on a second design-gate pass mid-sprint. If the assessment instead concludes "not needed," this design is simply unused; no re-gating required either way (§6 default-to-Design-Required precedent for conditional-outcome items, `2026-08-21__release-v9.0` ST-03/ST-07/ST-10).

## 2. Decision

**If** the assessment concludes an advisory is warranted, render a static, non-dismissible notice below the four-card stat grid when the underlying trade count backing the compliance statistics is below the assessment's chosen threshold (AC references "sub-20-trade states" as the anchor case).

### Visual treatment

Reuse the existing `StandingAlert` **Info** tone token verbatim (`design_system.md` §Standing Alert) rather than introduce a new colour/tone pair:

| Element | Spec |
|---------|------|
| Container | `bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-950 dark:border-blue-800 dark:text-blue-200` |
| Icon | `Info` (lucide-react) |
| Placement | Full-width row beneath the 4-card grid, inside `Arc5ComplianceSection`'s own container — not a page-level `StandingAlertStack` entry (this is section-scoped context, not an app-wide condition) |
| Dismissal | None — static while the underlying condition holds; re-evaluated on each data fetch, same lifecycle as the stat cards themselves. Distinct from `StandingAlert`'s manual-dismiss pattern, which does not fit a condition that is a fact about the current data (not an event to acknowledge). |
| Copy | One sentence, present tense, states the reliability caveat and the sample size it's based on (e.g. `"Based on N closed trades — treat these figures as indicative until more trade history accumulates."`) — exact threshold/wording finalised by the assessment, not fixed here |

### Why not the `gated`/`empty` `DataState` branches

Neither fits: the section has real, renderable data (not absent, not locked) — the concern is statistical confidence in the data that's already showing, which is a supplementary annotation alongside the cards, not a state that replaces them.

## 3. §13 Compliance

Purely a display-confidence caveat on already-computed, already-approved compliance statistics (no new computation, no new recommendation). Consistent with the component's existing "display-only, no automated recommendation" classification (`arc5_compliance_section.md` §13 line). Does not introduce or extend any AI-provider call — §13 boundary pre-check (STEP 1) does not apply.

## 4. Frontend Spec Impact

`docs/specs/frontend/components/arc5_compliance_section.md` gains a new "Low-Trade-Volume Advisory" subsection (conditional — only if the assessment confirms it ships) documenting the trigger threshold, copy pattern, and Info-tone reuse, authored during sprint execution alongside the assessment's conclusion, per `CLAUDE.md` §6 versioning checklist.

## 5. Approval

Head of UX & Design: confirmed, 2026-09-07.
Product Owner: confirmed, 2026-09-07.
