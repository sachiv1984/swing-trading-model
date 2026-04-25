**Owner:** Head of UX & Design
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Date:** 2026-04-25
**Cycle:** 2026-04-25__release-v3.0
**Story:** ST-11 (BLG-FE-19)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Decision Record — Keyboard Shortcuts (ST-11)

## Scope

Global keyboard shortcuts for common trading actions. Applies to the screener results page (new in v3.0) and any existing pages where the shortcut action is available.

---

## Shortcut Definitions

| Key | Action | Applicable Pages |
|-----|--------|-----------------|
| `n` | Open new position form/modal | Positions, Trade History |
| `w` | Add-to-watchlist trigger | Watchlist, Screener Results |
| `r` | Refresh / reload page data | All pages with a primary data endpoint |

**Suppression rule:** Shortcuts must not fire when keyboard focus is inside a `<input>`, `<textarea>`, or `<select>` element. Implementation must check `document.activeElement.tagName` before acting.

---

## Shortcut Reference UI

**Form chosen:** Sidebar footer hint (persistent, low-profile).

**Rationale:** Sidebar footer is visible on all applicable pages without requiring a separate overlay component or layout change. Least intrusive among the AC-approved options (tooltip, help overlay, footer hint).

**Location:** Bottom of the left sidebar navigation panel, below all nav group items.

**Content:** Three rows, each showing `[key]` chip + action label. Show only shortcuts applicable to the current page (dynamically filtered). If no shortcuts apply to the current page, the hint section is hidden.

**Visual treatment:**
- Section label: "Shortcuts" in uppercase small-caps, secondary muted colour (consistent with nav group headers)
- Each row: monospace key label rendered as a small chip/badge (light background, rounded, border) + action label in secondary typography
- No interactive state required (purely informational)

**Responsive:** On mobile sidebar (collapsed/hamburger), the hint is hidden — shortcuts remain active but the reference is not shown (acceptable for v3.0; tooltip on help icon may be added in a future cycle).

---

## Product Owner Approval

Approved by: Product Owner
Date: 2026-04-25
Notes: Display-only, sidebar footer placement approved. Suppression rule in text inputs confirmed. Applicable-page filtering approved.

---

## Frontend Spec Target

`docs/specs/frontend/pages/navigation.md` — add §Keyboard Shortcuts section.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-25 | Initial version. Design gate 2026-04-25__release-v3.0. Head of UX & Design. Product Owner approved. |
