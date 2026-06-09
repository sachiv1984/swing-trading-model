**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-08__release-v5.3 (ST-22, BLG-FE-67)
**Gate:** BLG-FE-64 clears 2026-06-21 — scope definition should complete before or at that date

---

# BLG-FE-64 — Visual Design Review: Scope Definition

## 1. Purpose

This document defines the precise scope of BLG-FE-64 (visual design review). It is a one-page scope document usable as the story AC at sprint planning when BLG-FE-64 is activated.

## 2. Scope: What BLG-FE-64 Covers

BLG-FE-64 is a **visual design review** — it covers:

| Element | In Scope | Specifics |
|---------|----------|-----------|
| Typography | ✅ | Heading hierarchy (h1/h2/h3 consistency), body text size and line spacing, font weight usage across pages |
| Colour palette | ✅ | Consistency of accent colours (green/red for P&L), neutral greys, contrast ratios for accessibility |
| Spacing system | ✅ | Card padding, table row height, gap between sections — consistency across all major pages |
| Component consistency | ✅ | Button styles (primary/secondary/ghost), badge colours, tag styles across pages |
| Which pages | ✅ | All pages currently in the sidebar nav: Dashboard, Portfolio, Trades, Analytics, Signals, Screener, Research, Red Flag Journal, Weekly Digest, System Status |
| Acceptance criteria form | ✅ | "Visual design feels cohesive and professional across all pages" — specific checklist per element above |

## 3. Scope: What BLG-FE-64 Does NOT Cover (Distinction from BLG-FE-66)

BLG-FE-66 (Red Flag Journal UX review, completed ST-21 v5.3) covered **interaction design** — how users interact with features (filter UX, pagination, empty states, user flows). BLG-FE-64 covers **visual design** only.

| Aspect | BLG-FE-64 (Visual) | BLG-FE-66 (Interaction) |
|--------|--------------------|-------------------------|
| Colour consistency | ✅ BLG-FE-64 | — |
| Typography hierarchy | ✅ BLG-FE-64 | — |
| Filter UX flow | — | ✅ BLG-FE-66 |
| Empty state messaging | — | ✅ BLG-FE-66 |
| Table readability (column content) | — | ✅ BLG-FE-66 |
| Table visual appearance (row height, borders) | ✅ BLG-FE-64 | — |

## 4. Acceptance Criteria (for Sprint Planning)

When BLG-FE-64 is activated as a sprint story, the following constitute "done":

1. Visual design review conducted across all 10 sidebar pages
2. Typography consistency checklist completed (heading hierarchy, body text, font weights)
3. Colour palette audit completed (accent colours, contrast ratios, P&L colour coding)
4. Spacing audit completed (card padding, table row height, section gaps)
5. Component consistency audit completed (buttons, badges, tags)
6. Findings documented: top-3 visual inconsistencies with screenshots/descriptions
7. Follow-up backlog items filed for any significant visual issues found (BLG-FE-68+)
8. One-page pre-brief report produced for Product Owner review

## 5. Effort Estimate

**S (~0.5 day)** — primarily a structured visual review with document output; no code changes.

## 6. Dependencies

- Gate date: 2026-06-21 (BLG-FE-64 activation gate)
- No technical dependencies; purely visual/design review

## 7. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Frontend Specs & UX Documentation Owner | Approved (agent-mediated) | 2026-06-09 |
| Head of UX & Design | Approved (agent-mediated) | 2026-06-09 |
