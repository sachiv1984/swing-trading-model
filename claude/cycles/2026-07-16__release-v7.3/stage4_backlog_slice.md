**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-16
**Cycle:** 2026-07-16__release-v7.3
**Release:** v7.3

<!-- release-plan-marker: RP:v7.3:2026-07-16__release-v7.3 -->

# Stage 4 Backlog Slice — v7.3 Dashboard/Trade-Plan/Navigation UX Continuation

## EPIC-01 — Dashboard & Trade-Plan UX Implementation (carried from v7.2)

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner

All 3 items already passed the design gate under `2026-07-15__release-v7.2` and their own readiness/spec passes (`BLG-SPEC-89`, `BLG-SPEC-90`) already shipped that same cycle. Carried forward unbuilt — ready for immediate sprint planning.

### ST-01 — Trade-plan-to-execution linkage UX ("Start Trade from Plan")

**Backlog ref:** `BLG-FE-109`
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Effort:** M (~1–2 days)
**Delegation class:** delegated_frontend
**Spec references:** `src/pages/TradePlan.js`, `src/pages/TradePlans.js`, `src/pages/TradeEntry.js`; readiness pass `BLG-SPEC-89` (shipped v7.2)

**Acceptance Criteria:**
- AC-01: A "Start Trade from Plan" action is visible and functional on both `TradePlan.js` (detail view) and `TradePlans.js` (list view).
- AC-02: Trades created via this action have `trade_plan_id` populated with no additional user action.
- AC-03: Manually-entered trades (no plan origin) are unaffected and can still optionally select a plan to link.
- AC-04: No regression to existing `TradeEntry.js` validation or submission behaviour.

**Staging-only ACs:** AC-01 (visible/functional action, element presence/interaction) requires Playwright coverage or recorded human staging sign-off per CLAUDE.md's observable-AC rule — code review alone is not sufficient.

---

### ST-02 — Dashboard empty/first-run state coverage

**Backlog ref:** `BLG-FE-110`
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Effort:** S–M (~0.5–1 day)
**Delegation class:** delegated_frontend
**Spec references:** `src/pages/DashboardHome.js` (`OpenPositionsCard`, `PortfolioHeatCard`, `GracePeriodCard`, `SignalStatusCard`, `RecentActivityCard`, `MorningBriefing`, `AiDailyBriefing`), shared `DataState` component, `src/pages/Watchlist.js` (reference pattern)

**Acceptance Criteria:**
- AC-01: Every card on `DashboardHome.js` renders a clear, on-brand empty state (not a blank card or raw zero/null value) when its underlying data is empty.
- AC-02: Empty states use the shared `DataState` component consistent with `Watchlist.js`.
- AC-03: Loading and error states for each card are unaffected by this change.

**Staging-only ACs:** AC-01/AC-02 (empty-state rendering, colour/iconography) require Playwright coverage or recorded human staging sign-off per CLAUDE.md's observable-AC rule.

---

### ST-03 — Dashboard briefing visual hierarchy

**Backlog ref:** `BLG-FE-111`
**Owner:** Head of UX & Design
**Effort:** S (~0.5 day)
**Delegation class:** delegated_frontend
**Spec references:** `src/pages/DashboardHome.js` (`MorningBriefing`, `AiDailyBriefing`)

**Acceptance Criteria:**
- AC-01: `MorningBriefing` and `AiDailyBriefing` are visually distinguishable from the status-card grid on page load, without scrolling past other cards first.
- AC-02: No change to underlying card data, queries, or the existing `dashboard-retry-root` retry behaviour.
- AC-03: Layout change verified in both light and dark themes.

**Staging-only ACs:** AC-01/AC-03 (visual distinction, dual-theme layout) require Playwright coverage or recorded human staging sign-off per CLAUDE.md's observable-AC rule.

---

## EPIC-02 — Command Palette Readiness Pass

**Maps to:** S2-04
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design

Spec-only item. `BLG-FE-115` itself is not in this release's scope — see Deferred Items.

### ST-04 — Command Palette (BLG-FE-115) pre-implementation spec, prompt template & discoverability/adoption pass

**Backlog ref:** `BLG-SPEC-91`
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Effort:** M (~2–3 days)
**Delegation class:** autonomous
**Spec references:** `src/components/ui/command.js`, `docs/specs/api_contracts/*`, `design_system.md` (`DataState` no-results state), Base44 prompt template library

**Acceptance Criteria:**
- AC-01: Formal spec authored covering searchable entity index scope and keyboard interaction contract.
- AC-02: Base44 prompt template for the Cmd/Ctrl-K pattern added to the prompt template library.
- AC-03: Discoverability/onboarding plan documented (desktop power-user pattern with no in-app precedent).
- AC-04: Adoption metric defined (invocations/session, search-to-navigation success rate).
- AC-05: API contract stub pre-staged.
- AC-06: `design_system.md` v1.1 `DataState` empty-state pattern reuse confirmed for the palette's no-results state.

**Staging-only ACs:** None — documentation/spec pass, no UI to verify visually.

---

## EPIC-03 — Custom Price Alerts Readiness Pass

**Maps to:** S2-05
**Owner:** Data Model & Domain Schema Owner; Backend Engineering Patterns Owner

Spec-only item. `BLG-FE-116` itself is not in this release's scope — see Deferred Items. Highest-priority readiness gate in this release (RISK-03 — §13 pre-check).

### ST-05 — Custom Price Alerts (BLG-FE-116) pre-implementation readiness pass

**Backlog ref:** `BLG-SPEC-92`
**Owner:** Data Model & Domain Schema Owner; Backend Engineering Patterns Owner
**Effort:** L (~3–4 days)
**Delegation class:** autonomous
**Spec references:** existing nightly-job/scheduler infrastructure, `GET /health/scheduler`, `docs/specs/api_contracts/*`, §13 human-in-the-loop boundary doc, `design_system.md` (`DataState` no-alerts state)

**Acceptance Criteria:**
- AC-01: Data schema pre-designed (ticker/condition/threshold/active flag) and documented.
- AC-02: Background alert-evaluation service pattern designed, confirmed to extend (not duplicate) existing scheduler infrastructure, with health-check surfacing on `GET /health/scheduler`.
- AC-03: Auth/rate-limit review completed for the new evaluation path.
- AC-04: Cost-impact pre-assessment completed (Render compute trend).
- AC-05: §13 pre-check completed and recorded PASS or a named follow-up, confirming the feature remains user-defined-threshold-plus-passive-notification, not automated execution.
- AC-06: Trigger-accuracy/false-positive metric defined.
- AC-07: Mock-payload strategy for Playwright tests documented.
- AC-08: API contract stub pre-staged.
- AC-09: `DataState` empty-state reuse confirmed for "no alerts configured."

**Staging-only ACs:** None — documentation/design pass, no UI to verify visually.

---

## EPIC-04 — Bulk Actions Readiness Pass

**Maps to:** S2-06
**Owner:** Backend Engineering Patterns Owner; Director of Quality

Spec-only item. `BLG-FE-117` itself is not in this release's scope — see Deferred Items.

### ST-06 — Bulk Actions (BLG-FE-117) pre-implementation readiness pass

**Backlog ref:** `BLG-SPEC-93`
**Owner:** Backend Engineering Patterns Owner; Director of Quality
**Effort:** M (~2 days)
**Delegation class:** autonomous
**Spec references:** existing `backend/routers/` batch-mutation conventions, Base44 prompt template library, §13 human-in-the-loop boundary doc, `tests/e2e/*` conventions

**Acceptance Criteria:**
- AC-01: Single-call batch-mutation endpoint pattern designed (tag/archive/remove), consistent with existing backend conventions.
- AC-02: Base44 prompt template for the multi-select + bulk-action-toolbar pattern added.
- AC-03: §13 pre-check completed and recorded PASS, confirming bulk operations remain human-initiated batch actions on existing rows, not automated decision-making.
- AC-04: Playwright coverage plan drafted (scenario list, not yet implemented).
- AC-05: `DataState`/design-system consistency confirmed for the toolbar's empty/zero-selected state.

**Staging-only ACs:** None — documentation/design pass, no UI to verify visually.

---

## EPIC-05 — Saved Filters & Calendar View Readiness Pass

**Maps to:** S2-07
**Owner:** Data Model & Domain Schema Owner; Frontend Specs & UX Documentation Owner

Spec-only item. `BLG-FE-118` itself is not in this release's scope — see Deferred Items.

### ST-07 — Saved Filters & Calendar View (BLG-FE-118) pre-implementation spec pass

**Backlog ref:** `BLG-SPEC-94`
**Owner:** Data Model & Domain Schema Owner; Frontend Specs & UX Documentation Owner
**Effort:** M (~2–3 days)
**Delegation class:** autonomous
**Spec references:** `src/components/ui/calendar.js`, `BLG-FE-40` versioned-localStorage-envelope pattern, `docs/specs/api_contracts/*`, `design_system.md` (`DataState` no-events state)

**Acceptance Criteria:**
- AC-01: Schema decision recorded with rationale — JSON-column-on-settings vs. dedicated table for saved filter presets — made during this pass, not deferred to execution kickoff.
- AC-02: Formal spec authored for the calendar view (date sourcing, navigation model).
- AC-03: Feasibility assessed for feeding the realized/unrealized P&L split into the calendar view for date-anchored P&L context.
- AC-04: QA acceptance-criteria template drafted, reusing the `BLG-FE-40` localStorage-envelope pattern for cross-reload filter persistence.
- AC-05: API contract stub pre-staged.
- AC-06: `DataState` empty-state reuse confirmed for the calendar's no-events state.

**Staging-only ACs:** None — documentation/spec pass, no UI to verify visually.

---

## Deferred Items

| Item | Reason |
|------|--------|
| `BLG-FE-115` — Global command palette | Blocked on `BLG-SPEC-91` (ST-04) completing first |
| `BLG-FE-116` — Custom price alerts | Blocked on `BLG-SPEC-92` (ST-05) completing first |
| `BLG-FE-117` — Bulk actions | Blocked on `BLG-SPEC-93` (ST-06) completing first |
| `BLG-FE-118` — Saved filters / calendar view | Blocked on `BLG-SPEC-94` (ST-07) completing first |

These four items were named alongside this release's scope as part of the same PO anchor-scope decision (`2026-07-16__scheduled`, DL-067), but each depends on its own not-yet-complete readiness pass and cannot enter sprint planning until that pass ships. Candidates for `v7.4`.
