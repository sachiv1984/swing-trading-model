**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-26
**Cycle:** 2026-06-26__release-v6.3
**Story:** ST-12 (BLG-FE-80)
**Approved by:** Product Owner — 2026-06-26

---

# UX Spec — Morning Briefing Progressive Disclosure

## Context

The AI Daily Briefing Card (`AiDailyBriefing.js`) currently displays two content sections — Summary and Actions — always fully expanded. A user who has already reviewed the briefing must scroll past the full card to reach AI Chat on every page load. This spec adds expand/collapse toggles to reduce visual noise for repeat daily use.

---

## Sections Subject to Collapse

The card has two collapsible content sections:

| Section Key | Section Label | Content |
|------------|--------------|---------|
| `summary` | **Market Context** | `response.summary` paragraph |
| `actions` | **Suggested Actions** | `response.actions[]` ordered list |

**Not collapsible (always visible):**
- Card header (title, timestamp, Regenerate button)
- Advisory label ("AI Advisory" + "All actions require your confirmation") — §13 requirement; must remain visible at all times regardless of section collapse state

---

## Section Header Design

Each collapsible section gets a section header row:

```
┌─────────────────────────────────────────────┐
│  Market Context                          ▼  │  ← expanded state
├─────────────────────────────────────────────┤
│  [summary paragraph content]                │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Market Context                          ▶  │  ← collapsed state
└─────────────────────────────────────────────┘
```

| Element | Spec |
|---------|------|
| Section label | Left-aligned, `text-sm font-semibold text-slate-300` |
| Toggle icon | Chevron: `ChevronDown` (expanded) / `ChevronRight` (collapsed) — Lucide; right-aligned; `text-slate-400` |
| Header row background | Subtle separator: `border-t border-slate-700/50` above each section header (except first) |
| Hover state | Header row: `hover:bg-slate-700/20` cursor-pointer |
| Click target | Full width of section header row |

---

## Collapse Behaviour

| State | Content Visibility | Animation |
|-------|-------------------|-----------|
| Expanded | Section content fully visible | — |
| Collapsed | Section content hidden (display:none equivalent) | No animation required — instant toggle is acceptable; smooth transition preferred if low-effort |
| Transitioning | — | If animated: 150ms ease-out height transition |

**Independent toggles:** Each section collapses and expands independently. Collapsing Market Context does not affect Suggested Actions.

---

## localStorage Persistence

**Key:** `ai-briefing-collapse-state-v1` — versioned to handle future schema changes without stale data conflict.

**Value (JSON):**
```json
{
  "summary": false,
  "actions": false
}
```

`false` = expanded (default); `true` = collapsed.

**Behaviour:**
- On mount: read key from localStorage; apply stored state
- On toggle: update localStorage synchronously
- If key absent or parse error: default to all expanded; do not throw
- No server-side persistence — client preference only

---

## Default State

All sections expanded. This ensures new users and users who have cleared localStorage see the full briefing without any hidden content.

---

## States Integration

The existing card states (No briefing yet, Loading, Normal, Empty actions, Error) are unaffected in behaviour. Additions:

| Existing State | Collapse Behaviour |
|---------------|-------------------|
| Loading | Section headers shown with skeleton body; toggle disabled during loading (no localStorage read until data loads) |
| No briefing yet | No section headers shown — placeholder message fills card body as before |
| Error | No section headers shown — error message fills card body as before |
| Normal | Section headers shown; localStorage state applied |

---

## Advisory Label Position

The Advisory label ("AI Advisory" amber badge + "All actions require your confirmation") is placed **below the card header, above the first section header**. It is always visible. It does not collapse.

```
┌──────────────────────────────────────────┐
│  Today's Briefing    HH:MM  [Regenerate] │  ← always visible
│  ⚠ AI Advisory  All actions require...   │  ← always visible (§13)
├──────────────────────────────────────────┤
│  Market Context                       ▼  │  ← collapsible
│  [summary content]                       │
├──────────────────────────────────────────┤
│  Suggested Actions                    ▼  │  ← collapsible
│  [actions list]                          │
└──────────────────────────────────────────┘
```

---

## Playwright Coverage Requirement (AC-05)

The following scenario must be covered by a Playwright test:

1. Expand all sections (default state)
2. Collapse the Market Context section
3. Reload the page
4. Assert: Market Context section remains collapsed
5. Assert: Suggested Actions section remains expanded

Test ID to use: `SC-BRIEF-01` (new test ID in the briefing test suite).

---

## Constraints

- Advisory label position and styling must not change — §13 compliance
- The Regenerate button behaviour is unchanged
- Section collapse state is a purely client-side preference — no API changes required
- If the card is in a loading or error state, section headers must not render (no partial UI)
- This change affects `AiDailyBriefing.js` only; `dashboard.md` frontend spec must be updated (§5) to reflect the new section headers and localStorage behaviour
