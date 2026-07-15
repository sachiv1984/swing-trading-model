**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-15
**Cycle:** 2026-07-15__release-v7.2
**Release:** v7.2

<!-- release-plan-marker: RP:v7.2:2026-07-15__release-v7.2 -->

# Stage 4 Backlog Slice — v7.2 Dashboard & Trade-Plan UX Hardening

## EPIC-01 — Mobile Responsiveness Baseline

**Maps to:** S2-01
**Owner:** Head of UX & Design

Assessment-only item recommended to run first — findings may affect scope/approach for EPIC-02 and EPIC-03.

### ST-01 — Mobile responsiveness baseline assessment

**Backlog ref:** `BLG-FE-55`
**Owner:** Head of UX & Design
**Effort:** M (~1–2 days)
**Delegation class:** autonomous (no observable UI change — produces an assessment report)
**Spec references:** `src/pages/Dashboard.js`, `src/pages/Positions.js`, `src/pages/Screener.js`, trade plan form, Red Flag Journal

**Acceptance Criteria:**
- AC-01: Mobile responsiveness assessment report produced.
- AC-02: Views assessed cover at minimum: positions, screener, trade plan form, Red Flag Journal.
- AC-03: Gate condition (Arc 5 completeness) verified and explicitly noted as not yet met before commencing — this is a Product Owner priority override, not a gate resolution (see `run_manifest.md`/backlog note).

**Staging-only ACs:** None — output is a written report, no code/UI change to verify visually.

---

## EPIC-02 — Trade-Plan-to-Execution Linkage

**Maps to:** S2-02, S2-03
**Owner:** Head of Specs Team; Head of UX & Design; Base44 Frontend Prompt Owner
**Sequencing constraint:** ST-02 (readiness pass) must complete before ST-03 (implementation) enters sprint planning.

### ST-02 — BLG-FE-109 pre-implementation readiness pass

**Backlog ref:** `BLG-SPEC-89`
**Owner:** Head of Specs Team
**Effort:** M (~2–3 days)
**Delegation class:** autonomous
**Spec references:** `docs/specs/api_contracts/*`, `data_model.md`, §13 human-in-the-loop boundary doc, `src/pages/TradeEntry.js`, `backend/routers/test.py`, SI-02 metric definition

**Acceptance Criteria:**
- AC-01: `trade_plan_id` auto-link consistency confirmed for the new path.
- AC-02: `docs/specs/api_contracts/` entry pre-staged for the new linkage behaviour.
- AC-03: Field documented in `data_model.md`.
- AC-04: `TradeEntry.js` pre-fill API surface confirmed/scoped.
- AC-05: Authorization boundaries confirmed to hold for the new action.
- AC-06: Action confirmed not to cross the §13 automated-execution boundary.
- AC-07: `TradeEntry.js` validation flagged as a specific regression-risk AC for ST-03.
- AC-08: SI-02 trade-count metric definition reviewed.
- AC-09: `test.py` entry requirement confirmed for when the backend route lands.
- AC-10: All 9 scope points addressed (documentation, confirmed-no-gap, or filed follow-up) before ST-03 sprint planning; ST-03's own AC updated to reference this readiness pass.

**Staging-only ACs:** None — documentation/confirmation pass, no UI to verify visually.

---

### ST-03 — Trade-plan-to-execution linkage UX ("Start Trade from Plan")

**Backlog ref:** `BLG-FE-109`
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Effort:** M (~1–2 days)
**Delegation class:** delegated_frontend
**Spec references:** `src/pages/TradePlan.js`, `src/pages/TradePlans.js`, `src/pages/TradeEntry.js`; readiness pass ST-02 (`BLG-SPEC-89`)
**Depends on:** ST-02 must be complete before this item enters sprint planning.

**Acceptance Criteria:**
- AC-01: A "Start Trade from Plan" action is visible and functional on both `TradePlan.js` (detail view) and `TradePlans.js` (list view).
- AC-02: Trades created via this action have `trade_plan_id` populated with no additional user action.
- AC-03: Manually-entered trades (no plan origin) are unaffected and can still optionally select a plan to link.
- AC-04: No regression to existing `TradeEntry.js` validation or submission behaviour.

**Staging-only ACs:** AC-01 (visible/functional action, element presence/interaction) requires Playwright coverage or recorded human staging sign-off per CLAUDE.md's observable-AC rule — code review alone is not sufficient.

---

## EPIC-03 — Dashboard UX Hardening

**Maps to:** S2-04, S2-05, S2-06
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design; Base44 Frontend Prompt Owner
**Sequencing constraint:** ST-04 (spec/instrumentation pass) must complete before ST-05/ST-06 enter sprint planning.

### ST-04 — BLG-FE-110/111 pre-implementation spec & instrumentation pass

**Backlog ref:** `BLG-SPEC-90`
**Owner:** Frontend Specs & UX Documentation Owner
**Effort:** S–M (~1–2 days)
**Delegation class:** autonomous
**Spec references:** `design_system.md`, Base44 prompt template library, `src/pages/DashboardHome.js`

**Acceptance Criteria:**
- AC-01: `DataState` empty-state pattern formalised in `design_system.md` and the Base44 prompt template library.
- AC-02: Primary vs secondary dashboard card treatment defined in frontend_specs.
- AC-03: Basic view/interaction instrumentation added to `DashboardHome.js` cards.
- AC-04: Base44 prompt drafts and Playwright coverage for both ST-05 and ST-06 explicitly call out dual-theme (light/dark) verification.
- AC-05: `design_system.md`/frontend_specs updates merged before ST-05/ST-06 sprint planning; both items' AC cross-reference this pass.

**Staging-only ACs:** None — documentation/spec pass, no UI to verify visually.

---

### ST-05 — Dashboard empty/first-run state coverage

**Backlog ref:** `BLG-FE-110`
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Effort:** S–M (~0.5–1 day)
**Delegation class:** delegated_frontend
**Spec references:** `src/pages/DashboardHome.js` (`OpenPositionsCard`, `PortfolioHeatCard`, `GracePeriodCard`, `SignalStatusCard`, `RecentActivityCard`, `MorningBriefing`, `AiDailyBriefing`), shared `DataState` component, `src/pages/Watchlist.js` (reference pattern)
**Depends on:** ST-04 must be complete before this item enters sprint planning.

**Acceptance Criteria:**
- AC-01: Every card on `DashboardHome.js` renders a clear, on-brand empty state (not a blank card or raw zero/null value) when its underlying data is empty.
- AC-02: Empty states use the shared `DataState` component consistent with `Watchlist.js`.
- AC-03: Loading and error states for each card are unaffected by this change.

**Staging-only ACs:** AC-01/AC-02 (empty-state rendering, colour/iconography) require Playwright coverage or recorded human staging sign-off per CLAUDE.md's observable-AC rule.

---

### ST-06 — Dashboard briefing visual hierarchy

**Backlog ref:** `BLG-FE-111`
**Owner:** Head of UX & Design
**Effort:** S (~0.5 day)
**Delegation class:** delegated_frontend
**Spec references:** `src/pages/DashboardHome.js` (`MorningBriefing`, `AiDailyBriefing`)
**Depends on:** ST-04 must be complete before this item enters sprint planning.

**Acceptance Criteria:**
- AC-01: `MorningBriefing` and `AiDailyBriefing` are visually distinguishable from the status-card grid on page load, without scrolling past other cards first.
- AC-02: No change to underlying card data, queries, or the existing `dashboard-retry-root` retry behaviour.
- AC-03: Layout change verified in both light and dark themes.

**Staging-only ACs:** AC-01/AC-03 (visual distinction, dual-theme layout) require Playwright coverage or recorded human staging sign-off per CLAUDE.md's observable-AC rule.

---

## EPIC-04 — Notification Surface Consolidation Review

**Maps to:** S2-07
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner

Audit-only item — no implementation this release.

### ST-07 — Notification/digest surface consolidation review

**Backlog ref:** `BLG-FE-112`
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Effort:** M (~1–2 days, audit only)
**Delegation class:** autonomous (no observable UI change — produces a findings report)
**Spec references:** `src/pages/Notifications.js`, `src/pages/NotificationsHistory.js`, `src/pages/NotificationPreferences.js`, `src/pages/WeeklyDigest.js`

**Acceptance Criteria:**
- AC-01: Current navigation entry points, usage patterns, and content overlap across all four surfaces audited.
- AC-02: Findings report produced identifying redundancy, gaps, and a recommendation on whether/how to consolidate.
- AC-03: Implementation of any consolidation explicitly out of scope for this item — filed as a follow-up backlog item if the audit recommends it.

**Staging-only ACs:** None — output is a written report, no code/UI change to verify visually.

---

## EPIC-05 — Combined Design Review & Shared QA Suite Planning

**Maps to:** S2-08
**Owner:** Head of UX & Design; Director of Quality

Cross-cutting process item covering EPIC-02, EPIC-03, and EPIC-04. Should be scheduled ahead of sprint planning per its own AC.

### ST-08 — Combined design review + shared Playwright suite plan

**Backlog ref:** `BLG-QA-111`
**Owner:** Head of UX & Design; Director of Quality
**Effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Spec references:** `tests/e2e/*` (Playwright suite conventions), CLAUDE.md frontend Playwright coverage requirement

**Acceptance Criteria:**
- AC-01: One combined design review session scoped covering ST-03, ST-05, ST-06, ST-07.
- AC-02: One shared Playwright spec file scoped (rather than four separate ones), consistent with CLAUDE.md's frontend Playwright coverage requirement.
- AC-03: Combined design review scheduled ahead of sprint planning for v7.2.
- AC-04: Shared Playwright spec file named in each of ST-03/ST-05/ST-06's sprint-backlog entry.

**Staging-only ACs:** None — process/planning item, no UI to verify visually.

---

## Deferred Items

None. All 8 v7.2 Now-horizon roadmap candidates are in scope this cycle.
