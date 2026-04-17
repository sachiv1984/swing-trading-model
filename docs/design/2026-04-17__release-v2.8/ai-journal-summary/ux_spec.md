**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-17
**Cycle:** 2026-04-17__release-v2.8
**Story:** ST-08 (EPIC-04)
**Approved by:** Product Owner — 2026-04-17

---

# UX Spec — AI Journal Summary Frontend (ST-08)

## Purpose

A read-only AI-generated summary of the user's trade journal entries — surfaced as a UX convenience view only. Raw journal entries remain the source of truth and are always visible. This feature is CONDITIONALLY COMPLIANT under SRB-v1.7 (2026-03-02).

---

## Page Placement

**Page:** Trade History (`/history`)

**Placement:** A new collapsible section titled **"AI Journal Summary"** positioned above the Trade History table (below the filter bar). This placement gives users context before reviewing individual trades without disrupting the primary trade table workflow.

---

## Component Anatomy

### Section Header
- Title: "AI Journal Summary"
- Subtitle/description: "AI-generated themes across your journal entries."
- Expand/collapse toggle (chevron): collapsed by default on page load; state persists in session (not localStorage).

### When collapsed (default)
- Header row only visible. No API call made until the user expands.

### When expanded
- **Disclaimer label** (always visible, above summary text):
  > *"AI-generated summary — for reference only. Not a trading recommendation."*
  > Displayed in a muted amber/info banner style to distinguish it clearly from content. Cannot be dismissed. Always visible whenever the summary is shown.

- **Generate / Refresh button:**
  - Label: "Generate Summary" (first time); "Refresh Summary" (if summary already loaded)
  - Clicking calls `POST /ai/journal-summary` with current filter context (date range and trade IDs from visible trades)
  - Disabled while loading
  - Placement: in the section header row (right side), inline with the title

- **Summary text panel:**
  - Renders the `summary` text from the API response
  - Card/panel with distinct background (e.g. slate-800 or subtle differentiation from raw entries) to visually separate AI content from journalled content
  - Font: regular body size; not displayed in journal-entry styling
  - Max-height with scroll if content is long

### States

| State | Behaviour |
|-------|-----------|
| Not yet generated | Placeholder: "Click 'Generate Summary' to get an AI overview of your journal entries." |
| Loading | Spinner inside the summary panel; button disabled |
| Loaded | Summary text rendered with disclaimer above |
| Error / Unavailable | "Summary unavailable. Please try again later." — muted, no error icon or technical message exposed to user |

---

## Scope Constraints (SRB-v1.7)

- AI summary output is **display-only**. It must NOT be used as input to any signal, scoring, compliance, or recommendation calculation — anywhere in the frontend.
- The disclaimer label is **mandatory** and must appear **whenever the summary is shown**, without requiring user interaction. It cannot be collapsed, hidden, or made optional.
- Raw journal entries remain fully visible and accessible on this page. The AI summary supplements; it does not replace.

---

## Hard Rules

- The section is **collapsed by default** — the AI feature is opt-in per session; users must actively expand and click Generate.
- No auto-generation on page load.
- Filter context: the summary covers the same trade scope as the currently visible filtered trade list (if date filter is active, summary reflects that filtered set). Pass trade IDs or date range to `POST /ai/journal-summary`.
- Strategy Rules owner sign-off on implementation is **required before merge** (AC in ST-08).

---

## Product Owner Approval

Approved: Product Owner — 2026-04-17
Collapsed-by-default approach confirmed (avoids implicit AI content on page load). Disclaimer placement and styling confirmed. Analytics page is NOT the target (Trade History only).
