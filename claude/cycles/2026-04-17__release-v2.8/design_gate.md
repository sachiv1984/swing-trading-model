**Owner:** Head of UX & Design
**Class:** Governance Record (Class 3)
**Status:** Passed
**Version:** 1.0
**Cycle:** 2026-04-17__release-v2.8
**Completed:** 2026-04-17
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Design Gate Record — 2026-04-17__release-v2.8

## Gate Status: PASSED

No stories blocked. Sprint Planning pre-condition: **MET**.

---

## Classification Table

| Story | Title | EPIC | Classification | Design Artefact | Canonical Spec Updated |
|-------|-------|------|---------------|-----------------|----------------------|
| ST-01 | Market Correlation View | EPIC-01 | Design Required | `docs/design/2026-04-17__release-v2.8/market-correlation/ux_spec.md` | `docs/specs/frontend/pages/analytics.md` v1.7 |
| ST-02 | Market Correlation Endpoint Scenarios | EPIC-02 | Design Not Applicable | — | — |
| ST-03 | Supplementary Indicator Scenarios | EPIC-02 | Design Not Applicable | — | — |
| ST-04 | DoQ Date Field Reminder Patch | EPIC-03 | Design Not Applicable | — | — |
| ST-05 | Sprint Close Terminology Clarification | EPIC-03 | Design Not Applicable | — | — |
| ST-06 | Backlog Archive Deduplication | EPIC-03 | Design Not Applicable | — | — |
| ST-07 | AI Journal Summary Backend | EPIC-04 | Design Not Applicable | — | — |
| ST-08 | AI Journal Summary Frontend | EPIC-04 | Design Required | `docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md` | `docs/specs/frontend/pages/trade_history.md` v1.7 |

---

## Classification Rationale

### Design Required

**ST-01 — Market Correlation View:**
New frontend section (§18) on the Analytics page. Requires placement decision, component layout, severity colour scheme, null handling, and state specifications. Design artefact produced and PO-approved.

**ST-08 — AI Journal Summary Frontend:**
New collapsible section on the Trade History page. Requires UX placement, collapsed-by-default behaviour, disclaimer labelling (SRB-v1.7 conditional compliance), state machine, and button semantics. Design artefact produced and PO-approved.

### Design Not Applicable

- **ST-02, ST-03:** Backend test scenario stories (no frontend surface). No UX decisions required.
- **ST-04:** Internal governance doc patch — no UI surface.
- **ST-05:** Governance terminology clarification — no UI surface.
- **ST-06:** Backlog tooling maintenance — no UI surface.
- **ST-07:** Backend API story — no frontend component. API contract spec is governed separately under `docs/specs/api_contracts/`.

---

## Design Artefacts Produced

### ST-01 — Market Correlation View
- **File:** `docs/design/2026-04-17__release-v2.8/market-correlation/ux_spec.md`
- **PO Approval:** 2026-04-17
- **Key decisions:** Analytics page §18 placement (after §17 Discipline & Compliance). Portfolio summary card + per-position table. Severity: high=Rose-500 / moderate=Amber-500 / low=Emerald-500 / null=Slate-500. Sort severity descending. Null rows to bottom. Data source: backend only.

### ST-08 — AI Journal Summary Frontend
- **File:** `docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md`
- **PO Approval:** 2026-04-17
- **Key decisions:** Trade History page only (not Analytics). Collapsed by default. Disclaimer mandatory and non-dismissible. No auto-generation on page load. SRB-v1.7 conditional compliance. Strategy Rules sign-off required before merge (remains as AC in ST-08).

---

## Canonical Spec Updates

### analytics.md — v1.6 → v1.7
- **File:** `docs/specs/frontend/pages/analytics.md`
- **Changes:** Purpose & User Goals updated; API Dependency updated (`GET /analytics/market-correlation`); Component Rendering Order extended to 18 items; §18 Market Correlation section added (portfolio summary card, per-position table, severity scheme, null handling, states, hard rules). Design Source header added. Changelog entry added.

### trade_history.md — v1.6 → v1.7
- **File:** `docs/specs/frontend/pages/trade_history.md`
- **Changes:** AI Journal Summary section added above Trade History Table (below Filters). Covers: collapsed-by-default behaviour, disclaimer label spec, Generate/Refresh button, POST endpoint context, 4 states, all SRB-v1.7 hard rules, Strategy Rules sign-off AC note. Design Source header added. Changelog entry added.

---

## Blocked Items

**None.** All classified stories are either cleared by artefact or classified Design Not Applicable.

---

## Outstanding Pre-Sprint Actions

The following items are NOT design gate blockers but must be resolved before the corresponding story is merged:

| Item | Story | Action Required | Owner |
|------|-------|----------------|-------|
| Strategy Rules sign-off | ST-08 | Strategy Rules owner must sign off on AI Journal Summary implementation before merge. This is an AC in ST-08 — not a gate blocker but a merge pre-condition. | Strategy Rules Owner |

---

## Frontend Spec Versions Locked

| Spec File | Version Locked |
|-----------|---------------|
| `docs/specs/frontend/pages/analytics.md` | v1.7 |
| `docs/specs/frontend/pages/trade_history.md` | v1.7 |

---

## Sprint Planning Pre-Condition

**MET.** Design gate PASSED. Sprint Planning may proceed for cycle `2026-04-17__release-v2.8`.
