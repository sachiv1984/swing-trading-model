**Owner:** Base44 Frontend Prompt Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-07 (created — v9.1 ST-36, BLG-GOV-267)

---

# Base44 Generation Failure-Mode Log

## Purpose

BLG-GOV-267: Base44-generated components occasionally need manual correction, but no log tracked which failure modes recur — prompt-template improvements have been made ad hoc rather than targeting the most frequent gaps. This log tracks recurring correction patterns so future prompt-template revisions can target the actual highest-frequency issues, not anecdote.

## Method

Backfilled from real historical records (backlog items, audit findings, sprint-close deviations) rather than fabricated examples — each entry below cites its evidence source.

## Log

| # | Failure mode | Occurrences (evidence) | Root-cause category |
|---|--------------|--------------------------|------------------------|
| 1 | **Missing `dark:` variant on a text/UI class** — a class string ships with only a light-theme value, no corresponding dark-theme pair | `src/pages/Reports.js:660`, `src/components/dashboard/home/WhatsNewCard.js:56,61` (2 instances, found in the `2026-08-08__release-v8.5` ST-09 secondary-text-token audit, `st09_secondary_text_token_audit_findings.md`) | Generation-time omission — the dark-mode pairing convention (`text-slate-600 dark:text-slate-400`, established v6.7) wasn't consistently applied to newly-generated sibling elements in an otherwise-compliant file |
| 2 | **Wrong/stale shade used instead of the canonical contrast-passing token** — an element uses a superficially-similar but contrast-failing shade (e.g. `text-slate-500` at 4.34:1, below the 4.5:1 WCAG AA bar) instead of the canonical `text-slate-600` | `src/pages/Positions.js:591`, `src/components/positions/PositionCard.js:127`, `src/components/watchlist/WatchlistRow.js:27`, `src/Layout.js` search-affordance button + badge (4 instances, same `v8.5` ST-09 audit) | Generation-time drift from the canonical token — likely copied from an older, pre-v6.7-remediation component rather than the current canonical pattern |
| 3 | **Missing accessible name on a `<select>`/`SelectTrigger`/combobox control** — a visually-adjacent `Label` element exists but is not programmatically associated (`aria-label`, `id`/`htmlFor`), failing axe-core's `select-name`/`button-name` rules | `TradePlan.js` Market/Status/Setup Type selects, `Settings.js` Default Currency/Theme `SelectTrigger`s, all 12 Settings form `Label`+`Input` pairs (found and fixed this same cycle, v9.1 EPIC-01 ST-02/ST-03/ST-04, `2026-09-03__release-v9.1`) | Generation-time omission — visual adjacency (label sits next to the control) was treated as sufficient; the generated markup never wired the programmatic association even though the visual design implied one |
| 4 | **Colour-contrast finding that is actually a scan-timing race against an entrance animation, not a real contrast defect** — a `framer-motion` fade-in (opacity 0→1) on page load causes an accessibility scanner to occasionally sample transiently-reduced-opacity text mid-animation, reporting a false contrast failure even though the resting-state colour token is already correct | `PageHeader.js` subtitle on the Settings page (found and fixed this same cycle, v9.1 EPIC-01 ST-05, `2026-09-03__release-v9.1`) — confirmed via 5 consecutive clean local runs post-fix, previously reproduced intermittently ~1-in-3 runs | Not a generation defect in the traditional sense (the colour token was already correct) — a test/measurement-timing gap that looks identical to a real contrast defect until investigated; flagged here since it consumed real correction effort and could recur on any other page using the same entrance-animation pattern |

## Review Cadence

Reviewed at each quarterly AI feature usage review (`docs/governance/ai_feature_usage_quarterly_review_*.md`) or whenever a new manual-correction pattern is found during sprint execution — append a new row rather than creating a new document. A pattern appearing 3+ times across independent stories is the trigger to prioritise a Base44 prompt-template fix targeting it specifically (modes #1/#2 above, both from the same single-cycle audit, are the closest current candidates — worth a combined prompt-template review of the dark-mode/contrast-token instruction block).

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Base44 Frontend Prompt Owner role — §5.3)
- Date: 2026-09-07
- Comments: Log created with 4 real, evidence-cited entries — the 2 explicitly named recurring modes (dark-mode class pairs, contrast) both backfilled from a real audit document, not invented examples. 2 additional genuine recurring patterns found from this same cycle's own EPIC-01 work, included since they meet the same evidentiary bar. Satisfies BLG-GOV-267's AC (log created; known recurring modes backfilled; Base44 Frontend Prompt Owner sign-off).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-07 | Initial creation — v9.1 ST-36, BLG-GOV-267. |
