**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-22
**Cycle:** 2026-06-19__release-v6.0
**Story:** ST-07 (EPIC-04)
**BLG-ID:** BLG-FE-41
**Input:** docs/design/2026-06-19__release-v6.0/rfj-design-review/brief.md (ST-06)

---

# Red Flag Journal — Visual Design Review

## Summary

The Red Flag Journal is functionally sound for its purpose as a personal accountability tool. The current list layout is appropriate for sole-trader usage at low event volumes. **No full redesign is recommended.** Two refinements are identified — one filed as a backlog item, one trivial enough to not require a sprint story.

---

## Review Findings

### 1. Filters UX — Verdict: Refine

**Finding:** The filter set (event type, ticker, date-from) is appropriate for the use case. The three filters cover the primary lookup scenarios: "what type of breach?", "which position?", and "in what period?".

The ticker filter's "Apply" button pattern (rather than live filtering) is correct — it avoids excessive API calls during typing and is a familiar interaction for traders used to form-submit patterns.

**Minor gap identified:** The "date-from" filter supports only a start date, not a date range. For a growing journal this will become limiting — a user who wants to review "last month's" events has no way to set an upper bound. At current volume this is acceptable, but it warrants a backlog item.

**Recommendation:** Accept current filters. File a backlog item for date-range filter (date-from + date-to) to be addressed when event volume makes it necessary.

**Verdict: Refine** (backlog only — no sprint story required now)

---

### 2. Severity Visual Hierarchy — Verdict: Accept

**Finding:** The absence of an explicit severity field is a deliberate product constraint, not a design gap. All 4 event types represent strategy governance breaches — by definition, the trader is the severity arbiter at the moment of override. Introducing a severity hierarchy in the UI without a severity data field would be cosmetically misleading.

The current equal-weight rendering of all event types is correct given the data model. The visual differentiation that matters is *type*, not severity — the trader already knows what each event type means in context.

**For future consideration:** If a severity field is added to the `red_flag_events` data model, the design should adopt a prominence hierarchy (e.g., HIGH events pinned or rendered with a stronger visual treatment). This is a future data model decision, not a current design problem.

**Verdict: Accept**

---

### 3. Event Type Colour Coding — Verdict: Refine

**Finding:** The current four-colour scheme — amber-400, orange-400, red-400, rose-400 — uses exclusively warm-spectrum hues. The distinctions are semantically arbitrary (no colour communicates more severity than another) and practically difficult to distinguish, particularly:
- orange-400 vs rose-400 are perceptually similar in the `light-daltonized` theme
- All four colours occupy the same "danger" semantic register without differentiation

The icons (AlertTriangle, CheckSquare, SkipForward, TrendingDown) are doing the real accessibility work here — they vary in shape and are the primary scannable signal. The colour is supplementary.

**Recommendation:** Retain the current icon approach as the primary differentiator. Revise the colour palette to use more semantically distinct hues that are also accessible under the daltonized theme. Suggested mapping:

| Event type | Current colour | Proposed colour | Rationale |
|-----------|----------------|-----------------|-----------|
| pre_entry_override | amber-400 | amber-400 | Retain — pre-trade, caution register ✓ |
| checklist_skipped | orange-400 | sky-400 | Move to blue register — administrative miss, not a risk event |
| stop_prompt_dismissed | red-400 | red-400 | Retain — post-entry risk event, red appropriate |
| drawdown_prompt_dismissed | rose-400 | red-500 | Deepen to red-500 to distinguish from stop_prompt and signal greater concern |

This makes `checklist_skipped` visually distinct from the three risk events, and differentiates the two stop/drawdown events by depth of red.

**This change is low-risk and small.** File as a backlog item (P3, cosmetic). Does not require a sprint story or UX spec — it is a 3-line CSS change.

**Verdict: Refine** (backlog item filed — see below)

---

### 4. Timeline vs List Layout — Verdict: Accept

**Finding:** The paginated reverse-chronological list is the correct layout for this use case. The arguments for a timeline layout — surfacing temporal patterns, grouping by date — do not apply meaningfully to the sole-trader context where:

1. Event frequency is low (the journal should be sparse by design — frequent entries signal a systemic strategy adherence problem, not a UI problem)
2. The primary use case is lookup ("did I dismiss a stop on AAPL recently?") not pattern analysis ("when do I tend to breach most?")
3. The "From date" filter already satisfies the temporal scoping need for most lookups

A timeline view would add complexity for negligible gain at current volumes. If event frequency significantly increases (e.g., > 50 events/month sustained), a date-grouped list view (not a visual timeline) could be considered. This is a future concern.

**Verdict: Accept**

---

## Backlog Items Filed (AC-03)

Two refinement items are being filed. Neither constitutes a redesign — no UX spec is required.

### BLG-FE-66 — RFJ date-range filter (date-to field)

- **Type:** UX Refinement
- **Priority:** P3
- **Effort:** XS
- **Description:** Add a "To date" input to the Red Flag Journal filter panel, converting the current date-from-only filter to a date range. Requires backend `until` parameter support on `GET /portfolio/red-flag-journal`.
- **Trigger:** When event volume makes date-from-only filtering insufficient for monthly/weekly review workflows.
- **Status:** Filed — not scheduled.

### BLG-FE-67 — RFJ event type colour palette refinement

- **Type:** Cosmetic / Accessibility
- **Priority:** P3
- **Effort:** XS
- **Description:** Update `checklist_skipped` colour from `orange-400` to `sky-400` and `drawdown_prompt_dismissed` from `rose-400` to `red-500` in `EVENT_TYPE_CONFIG` in `RedFlagJournal.js`. Improves semantic distinction and daltonized-theme legibility.
- **Status:** Filed — not scheduled.

---

## Overall Recommendation

**Accept the current Red Flag Journal design.** The list layout, filter model, and event type differentiation are appropriate for the sole-trader use case. Two minor refinements have been identified and filed as low-priority backlog items — neither warrants immediate sprint work. No redesign is required.

---

## Head of UX & Design Sign-Off (AC-02)

- Reviewed by: Head of UX & Design
- Date: 2026-06-22
- Recommendation: Accept current design; two P3 refinement items filed (BLG-FE-66, BLG-FE-67)
- No redesign: UX spec not required (AC-03 — N/A, no redesign triggered)
- Notes: Review conducted against all 4 brief areas (ST-06). Findings align with sole-trader product context. Icons remain the primary accessibility signal; colour palette refinement is cosmetic and low-risk.
