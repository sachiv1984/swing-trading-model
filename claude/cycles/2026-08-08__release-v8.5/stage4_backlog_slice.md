Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-08
Cycle: 2026-08-08__release-v8.5
Release: v8.5

# Backlog Slice — v8.5

<!-- release-plan-marker: RP:v8.5:2026-08-08__release-v8.5 -->

25 stories across 6 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution).

---

## EPIC-01 — Production Correctness Fixes

**Maps to:** S2-01
**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner

### ST-01 — Fix GET /analytics/tag-performance 500 on staging (missing trade_tags column ensure)
**Source:** BLG-BE-86
**Priority:** P1
**Effort:** XS
**Acceptance Criteria:**
- `GET /analytics/tag-performance` returns 200 (or a real 400/404 for genuinely invalid input) on a database where `trade_tags` was never previously ensured
- No regression to existing `trade_plans.py` endpoints' own `ensure_trade_plans_table()` calls
- Root cause note added to `docs/ops/api_performance_baseline.md`'s entry for this endpoint confirmed resolved and updated

### ST-02 — Confirm api-key-cross-environment-check.yml is genuinely running, not silently skipping
**Source:** BLG-OPS-134
**Priority:** P1
**Effort:** XS
**Acceptance Criteria:**
- Confirmed (via a real run's log) that the cross-environment comparison is now executing, not skipping
- Decision recorded on whether the skip-guard's silent-pass behaviour should be hardened, and if so, implemented

---

## EPIC-02 — Security Hardening

**Maps to:** S2-02
**Owner:** Cybersecurity & Trust Lead; Metrics Definitions & Analytics Owner

### ST-03 — Security fix false-positive rate assessment (BLG-SEC-02)
**Source:** BLG-SEC-10
**Effort:** S
**Note:** Gate condition (30-day production observation window) confirmed cleared 2026-08-08 — 37 days in production since v6.4 (2026-07-02) with no incident on record.
**Acceptance Criteria:**
- Measurement conducted (false-positive rate of BLG-SEC-02 write-time validation), alongside BLG-QA-70's own equivalent finding

### ST-04 — Recurring dependency vulnerability re-scan cadence (consolidated)
**Source:** BLG-SEC-15
**Effort:** S
**Acceptance Criteria:**
- Scheduled job runs successfully at least once and reports results for both `pip-audit` and `npm audit`
- Combined cadence (sprint planning + scheduled interval) documented
- New HIGH/CRITICAL findings result in a filed backlog item

### ST-05 — API key rotation runbook
**Source:** BLG-SEC-16
**Effort:** S
**Acceptance Criteria:**
- Rotation runbook documented: steps, owner, verification checklist for rotating the registered `X-API-Key`

---

## EPIC-03 — Frontend Correctness Fixes

**Maps to:** S2-03
**Owner:** Frontend Specifications & UX Documentation Owner

### ST-06 — Register muted/muted-foreground (and other dead -muted classes) in tailwind.config.js
**Source:** BLG-FE-145
**Priority:** P2
**Effort:** S
**Sequencing note:** Should land before ST-09/ST-13 (EPIC-04 contrast/design-token audits) — those audits would otherwise be checking against a known-broken CSS baseline (see RISK-01).
**Acceptance Criteria:**
- `text-muted-foreground` (and any other `-muted` classes found in scope) compile to a non-empty CSS rule, verified via a real `tailwindcss` build
- No visual regression at any confirmed-affected call site — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

### ST-07 — Frontend wiring to populate trade_plans.thesis_model_version/thesis_prompt_version on save
**Source:** BLG-FE-143
**Effort:** XS
**Note:** `Provisional-Target: v8.5` already carried on this item — horizon-planned for this release.
**Acceptance Criteria:**
- A trade plan saved directly from AI-generated content (no manual edits to the narrative fields) has `thesis_model_version`/`thesis_prompt_version` populated in the database
- A manually-typed or user-edited plan leaves both fields null

### ST-08 — Reconcile Monthly P&L vs Tax Year table's exact-zero P&L colour convention
**Source:** BLG-FE-144
**Effort:** XS
**Acceptance Criteria:**
- Both tables render an exactly-zero realised P&L value with the same colour treatment
- `docs/specs/frontend/pages/reports.md` updated to state one convention for both tables, no remaining per-table caveat
- No visual regression to non-zero P&L colouring in either table — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

---

## EPIC-04 — Design System & Contrast Consistency Audit

**Maps to:** S2-04
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design

### ST-09 — Design token audit: v6.7 contrast fix consistency
**Source:** BLG-FE-91
**Effort:** S
**Acceptance Criteria:**
- Audit conducted; any drift found (hardcoded colour classes instead of the canonical secondary-text token) filed as a follow-up backlog item

### ST-10 — Empty-state illustration/microcopy consistency pass
**Source:** BLG-FE-92
**Effort:** M
**Acceptance Criteria:**
- Shared empty-state pattern documented
- Pattern applied to at least 3 pages

### ST-11 — Confirm theme-toggle persistence across sessions
**Source:** BLG-FE-93
**Effort:** S
**Acceptance Criteria:**
- Theme persistence behaviour verified across session boundaries (fresh session after a long gap; after a browser storage-clearing event)
- Any gap found fixed or filed as a follow-up

### ST-12 — Mobile responsive audit for PerformanceAnalytics page
**Source:** BLG-FE-94
**Effort:** M
**Acceptance Criteria:**
- Page audited at common mobile breakpoints
- Critical issues (overflow, truncation, unusable controls), if any, fixed or filed

### ST-13 — Dark/light theme contrast audit follow-up
**Source:** BLG-FE-100
**Effort:** S
**Acceptance Criteria:**
- Targeted follow-up contrast audit run, scoped to confirm no further secondary-text (or similar) contrast gaps remain beyond BLG-FE-87/88/89's known fixes

### ST-14 — Ad hoc component inventory: candidates for shared design-system extraction
**Source:** BLG-FE-133
**Effort:** M
**Acceptance Criteria:**
- Inventory of ad hoc/duplicated component patterns across the app produced, ranked by duplication count
- Head of UX & Design sign-off

---

## EPIC-05 — Frontend UX Review & Documentation

**Maps to:** S2-05
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner

### ST-15 — Nav bar redesign exploration
**Source:** BLG-FE-27
**Effort:** M
**Acceptance Criteria:**
- Design recommendation document produced (maintain current, or redesign to a named pattern)
- Rationale covers screen real-estate impact, mobile responsiveness, Arc 2+ page count
- If redesign recommended: UX spec produced and implementation backlog item filed

### ST-16 — User journey map: SI-05 Telegram digest to app action
**Source:** BLG-FE-65
**Effort:** S
**Acceptance Criteria:**
- User journey map document produced (entry points, navigation steps, friction findings)
- Any significant friction filed as a separate backlog item
- Head of UX & Design sign-off

### ST-17 — Reusable empty-state component spec for Base44 prompts
**Source:** BLG-FE-99
**Effort:** S
**Acceptance Criteria:**
- One reusable empty-state component spec defined for future Base44 prompts to reference instead of reinventing per page

### ST-18 — Reports page information hierarchy review
**Source:** BLG-FE-101
**Effort:** S
**Acceptance Criteria:**
- Head of UX & Design reviews the Reports page for visual clutter/hierarchy issues introduced by the SI-02 gate visibility indicator (BLG-FEAT-71, v6.8)
- Findings documented; any fix filed as a follow-up if not resolved in-story

### ST-19 — Rework ChartStyle to drop style-src 'unsafe-inline' dependency, if/when a consumer adopts ChartContainer
**Source:** BLG-FE-146
**Effort:** M
**Note:** `chart.js` has zero live consumers today — scope executes only if a consumer is adopted this cycle; otherwise this story closes as "confirmed still unused, no action needed" per its own conditional scope.
**Acceptance Criteria:**
- If a consumer is adopted: `ChartContainer` renders correct theme-appropriate colours with no `<style>`/`dangerouslySetInnerHTML` in `chart.js`, and CSP `style-src` no longer includes `'unsafe-inline'`
- No visual regression to any chart using `ChartContainer` — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

### ST-20 — Playwright/staging visual verification of calendar.js when a real consumer is added
**Source:** BLG-FE-139
**Effort:** XS
**Note:** Deferred-trigger item — `ui/calendar.js` has zero live consumers today; closes when a consumer ships with its own Playwright coverage or staging sign-off.
**Acceptance Criteria:**
- When a consumer of `ui/calendar.js` ships, its story's PR includes Playwright coverage or a recorded staging sign-off for the calendar's rendering; this item closed at that time referencing that story/PR

---

## EPIC-06 — Analytics & Governance Process Fixes

**Maps to:** S2-06
**Owner:** Metrics Definitions & Analytics Owner; Head of Specs Team; QA & Testing Owner

### ST-21 — Regime distribution metric over screener history
**Source:** BLG-FEAT-29
**Effort:** S
**Note:** Gate condition (screener live ≥ 60 days) confirmed cleared 2026-08-08 — screener shipped v3.0 (2026-04-27), 103 days ago.
**Acceptance Criteria:**
- Aggregate view (rolling 30d/60d/all) of regime distribution over screener history computable and displayable

### ST-22 — Product Value Ratio historical trend chart
**Source:** BLG-FEAT-72
**Effort:** S
**Acceptance Criteria:**
- Small chart/table visualising the STEP 2.4 U/G/D/P ratio across cycles, sourced from a structured record rather than re-derived decision-log prose each rebalance

### ST-23 — Release Planning does not reset root sprint_sealed to false on new-cycle publish
**Source:** BLG-GOV-288
**Priority:** P2
**Effort:** XS
**Governance-file note:** Patches `release_planning_prompt.md` STEP 0 — apply the standard Governance File Edit Checklist (CLAUDE.md §6: version bump, OPERATIONAL_GUIDE.md §14 sync, prompt_change_log.md entry) in the same commit.
**Acceptance Criteria:**
- `release_planning_prompt.md` STEP 0 patched to reset `sprint_sealed: false` on new-cycle publish
- Head of Specs Team sign-off

### ST-24 — CLAUDE.md §8 sibling-vs-sibling union clause for execution_state.json array fields
**Source:** BLG-GOV-289
**Priority:** P2
**Effort:** XS
**Governance-file note:** Patches `CLAUDE.md` §8 — apply the standard Governance File Edit Checklist per CLAUDE.md §6.
**Acceptance Criteria:**
- `CLAUDE.md` §8 explicitly covers the sibling-vs-sibling `blocked_items`/`delegated_items` union case (neither side is `main`)
- Head of Specs Team sign-off

### ST-25 — Fix unrestored sys.modules stubbing in test_alerts_service.py (cross-file test pollution)
**Source:** BLG-QA-105
**Priority:** P2
**Effort:** S
**Acceptance Criteria:**
- `test_alerts_service.py`'s `sys.modules` stubbing given proper scoping/teardown (e.g. a pytest fixture restoring prior entries after that file's tests complete), matching the guarded pattern already used in `test_trade_service.py`
- Full suite run confirms no cross-file pollution of `utils.formatting`/`utils.pricing`/`utils.calculations`/`config` for tests collected after this file

---

*(ST-01–ST-25, no gaps, no out-of-sequence additions this cycle.)*
