**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-22
**Cycle:** 2026-06-19__release-v6.0
**Story:** ST-06 (EPIC-04)
**BLG-ID:** BLG-FE-64

---

# Red Flag Journal — Design Review Pre-Brief

## Purpose

This brief scopes the design review of the Red Flag Journal (`/src/pages/RedFlagJournal.js`), which has been in production since approximately 2026-05-22 (≥30 days as of 2026-06-22, satisfying AC-01). The review (ST-07) will assess whether the current implementation is fit for ongoing use or requires refinement.

## Context

The Red Flag Journal records strategy deviations — moments where the trader proceeded past a governance gate without compliance. It is a personal accountability tool, not a reporting system. The audience is a single sole trader who both creates and reviews entries. Usage frequency is expected to be low (events occur when strategy rules are bypassed, which should be infrequent by design).

Current implementation serves 4 event types: Pre-Entry Override, Checklist Skipped, Stop Prompt Dismissed, Drawdown Prompt Dismissed.

---

## Review Scope

The ST-07 review must address the following four areas:

### 1. Filters UX

**What to assess:**
- Does the current filter set (event type, ticker, date-from) serve real lookup needs?
- Is the filter interaction model (type dropdown, ticker input + Apply button, date picker) intuitive?
- Does "Clear filters" provide sufficient visibility when filters are active?
- Does the filter panel scale if event volume increases over time?

**Current state:** Three filters in a horizontal flex row. Ticker requires an explicit "Apply" button (not live). No active-filter indicator beyond the appearance of "Clear filters" text.

**Question to answer:** Are the current filters sufficient, or is any filter missing (e.g., date-range instead of date-from-only)?

---

### 2. Severity Visual Hierarchy

**What to assess:**
- The current implementation has no explicit severity field — events are differentiated by type only.
- Should severity (e.g., HIGH / MEDIUM / LOW) be visually communicated separately from event type?
- If severity is not a data field today, can severity be inferred from event type (e.g., stop/drawdown dismissals as higher severity than checklist skips)?
- Does the current layout give appropriate visual weight to more serious deviation types?

**Current state:** All 4 event types render identically in size, layout, and visual weight. Colour is the only differentiator. No severity indicator exists.

**Question to answer:** Is visual hierarchy between event types needed, or is event type alone sufficient for this sole-trader context?

---

### 3. Event Type Colour Coding

**What to assess:**
- Current colours: amber-400 (pre_entry_override), orange-400 (checklist_skipped), red-400 (stop_prompt_dismissed), rose-400 (drawdown_prompt_dismissed).
- All four colours are warm-spectrum — distinctions are subtle, particularly between orange and rose.
- The user's interface theme is `light-daltonized` (colour accessibility mode) — review must consider colour-blind legibility.
- Do the current colours communicate meaningful semantic distinctions, or are they arbitrary?

**Current state:** Four warm-spectrum colours. No shape or pattern variation to complement colour (icon shape varies, which does help accessibility).

**Question to answer:** Are the current colours semantically meaningful and accessible, or should a more differentiated palette be adopted?

---

### 4. Timeline vs List Layout

**What to assess:**
- Current layout: paginated reverse-chronological list, 20 items per page.
- A timeline layout would group events by date or week, surfacing temporal patterns.
- For a sole trader with low deviation frequency, does a timeline add meaningful value?
- Could a simple date-grouped list (not a full visual timeline) be a lower-cost improvement?

**Current state:** Flat list with relative timestamps. No date grouping. Pagination at 20 per page.

**Question to answer:** Does the current list layout serve the review use case, or would date-grouping / timeline significantly improve pattern recognition?

---

## Evaluation Criteria for ST-07

The review in ST-07 should produce a recommendation against each area using this framework:

| Decision | Meaning |
|----------|---------|
| **Accept** | Current implementation is fit for purpose — no change needed |
| **Refine** | Minor improvement recommended — can be a backlog item, no immediate sprint work |
| **Redesign** | Significant change recommended — UX spec + implementation backlog item required (AC-03) |

A full redesign recommendation requires a UX spec document and a filed backlog item before the story can close.

---

## Expected ST-07 Deliverable

A design recommendation document covering each of the 4 review areas with an Accept / Refine / Redesign verdict and rationale. If any area is rated Redesign, a corresponding UX spec must be produced and a backlog item filed.

---

## Head of UX & Design Sign-Off (AC-03)

- Reviewed by: Head of UX & Design
- Date: 2026-06-22
- Brief scope confirmed: covers all 4 required areas (filters UX, severity visual hierarchy, colour coding, timeline vs list)
- Notes: Brief serves as direct input to ST-07 visual design review. Evaluation criteria framework defined above governs ST-07 deliverable format.
