# Sprint Backlog — 2026-07-12__release-v7.0

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-13
**Cycle:** 2026-07-12__release-v7.0
**Release:** v7.0
**Sprint Goal:** Close the Grid View/Table View position-risk badge and trailing-stop parity gap, resolve the v6.9-carried spec-reconciliation and data-correctness debt, and ship three new reporting and position-review features (tax-year P&L CSV export, realized/unrealized P&L split, and position review-cadence nudge) — fully utilising this cycle's ~12–14 day capacity per the Product Owner's scope-maximisation directive.
**Backlog Slice Source:** Original — `claude/cycles/2026-07-12__release-v7.0/stage4_backlog_slice.md`

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 (matches `release_plan.md`/`stage4_backlog_slice.md` listing order; EPIC-01 is the canonical owner of the most heavily shared files and must land first).
- **`execution_state.json` owner:** EPIC-01 (first in execution order).
- **Shared files across EPICs:**
  - `docs/specs/frontend/pages/positions.md` — edited by EPIC-01 (ST-01 authors the Grid View badge subsection, v2.0→v2.1; ST-05 bumps to v2.2 per the combined-badge design decision record) **and** by EPIC-03 (ST-15 also bumps to v2.2 per its own design gate artefact, `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md`). EPIC-01 owns the canonical version. **EPIC-03 must rebase onto `main` after EPIC-01 merges** and reconcile its own `positions.md` edit onto EPIC-01's already-merged v2.2 (renumbering to v2.3 as needed) before finalising ST-15.
  - `PositionCard.js` (Grid View position card component) — edited by EPIC-01 (ST-02, ST-03, ST-05) and likely by EPIC-03 (ST-15, review-cadence display). EPIC-01 owns the canonical version; EPIC-03 must rebase onto `main` after EPIC-01 merges before finalising its own edit to this file.
  - `Positions.js` (Table View) — edited by EPIC-02 (ST-09 breach badge conformance) and possibly EPIC-03 (ST-15, if the review-cadence nudge also renders in Table View). EPIC-02 owns the canonical version (merges before EPIC-03); EPIC-03 must rebase onto `main` after EPIC-02 merges if it also touches this file.
  - `Reports.js` — edited by EPIC-03 only (ST-13, ST-14 both touch the P&L views); no cross-EPIC conflict, but sequence ST-13 before ST-14 within the EPIC-03 branch to avoid rebasing churn (per `release_plan.md §Execution Plan`).

---

## Sprint Scope

### EPIC-01 — Positions Grid View Parity

**Maps to:** S2-01
**Owner:** Head of Engineering
**Estimated effort:** ~2.35 days
**Risk IDs:** RISK-01, RISK-04
**Execution sequence:** 1

#### ST-01 — `positions.md` Grid View badge placement subsection (BLG-SPEC-80)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (lands first per RISK-01 sequencing so ST-02 can cite the spec directly)

**Notes:** Spec-authoring only, no code. Design gate: Design Pre-Approved (spec debt, documents existing approved badge visuals). Lands first or alongside ST-02 per `release_plan.md §Execution Plan`.

**Staging-only ACs:** None — spec-only, no runtime behaviour to verify.

---

#### ST-02 — Positions Grid View missing RISK OFF badge (BLG-FE-102)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** S (~0.25–0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 (spec subsection should land first/alongside so this implementation can cite it directly)

**Notes:** Design gate: Design Pre-Approved — visual treatment (`#1E40AF`, "RISK OFF") fully specified in `positions.md` §Alerts Column; this is a parity implementation of an existing, already-shipped Table View pattern into `PositionCard.js` (BLG-GOV-72 fast-path (c) — locked spec, existing pattern reused). No new UX decision.

**Staging-only ACs:** None — badge rendering driven by `risk_off_exit` position-data flag, fully mockable via Playwright API fixtures.

---

#### ST-03 — Positions Grid View missing trailing-stop value and breach indicator (BLG-FE-97)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-02 (per RISK-01 sequencing — same file, avoid rework)

**Notes:** Design gate: Design Pre-Approved — `positions.md` v2.1 already documents Grid View trailing-stop placement. Parity implementation of existing Table View breach-icon logic.

**Staging-only ACs:** None — trailing-stop value and breach state are position-data driven, mockable via Playwright fixtures.

---

#### ST-04 — Positions Grid View badge parity Playwright coverage (BLG-QA-95)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** ST-02, ST-03 (both badge/indicator stories must ship before parity coverage can be authored)

**Notes:** Design gate: Design Not Applicable — test-only, no UI change. Provides the Grid View half of the `SC-RO-*` Table View coverage already in CI.

**Staging-only ACs:** None — this story is itself the Playwright coverage deliverable.

---

#### ST-05 — GAP RISK / RISK OFF combined-badge visual differentiation review (BLG-FE-104)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-02, ST-03 (both badges must be rendered together for the review; runs last in EPIC-01 per `release_plan.md`)

**Notes:** Design gate: Design Required — review already completed and confirmed at the design gate, artefact `docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md` (positions.md bumped to v2.2). No open design decision remains; execution implements whatever the decision record specifies (confirmed-distinguishable, or the named fix).

**Staging-only ACs:** None — combined-badge render state is mockable (both flags true) in Playwright.

---

### EPIC-02 — v6.9 Carryover Fixes & Reconciliation

**Maps to:** S2-02
**Owner:** Head of Engineering
**Estimated effort:** ~2.15 days
**Risk IDs:** RISK-02, RISK-04
**Execution sequence:** 2

#### ST-06 — Reports.js Tax Year P&L tab spec reconciliation (BLG-SPEC-71)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Design gate: Design Pre-Approved — spec-debt correction only, no code/UI change. RISK-02: apply `document_lifecycle_guide.md` versioning conventions carefully to avoid repeating the spec/shipped-feature changelog-wording ambiguity that caused this drift; mark corrected sections "Design Only — Implementation Pending" per the item's own suggested convention.

**Staging-only ACs:** None — spec-only.

---

#### ST-07 — Instrument trailing-stop recommendation capture for `trailing_stop_action_rate` metric (BLG-BE-50)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Design gate: Design Not Applicable — backend logging table, no user-visible effect. AC's "Capture window (24-hour proposal) confirmed by Product Owner" is resolved at planning: Product Owner (delegated authority) confirms the 24-hour default proposed in the backlog item as the capture window — see Outstanding Actions below (non-blocking to seal, consistent with `2026-07-10__release-v6.9` §13 sign-off precedent).

**Staging-only ACs:** None — backend table/query logic, unit/integration-testable.

---

#### ST-08 — Dashboard/StrategyBenchmark page-title light-theme contrast gap (BLG-FE-95)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Design gate: Design Required — canonical light-theme heading token decision already resolved and locked at the design gate (`docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md`; `dashboard.md` v2.8, `strategy_benchmark.md` v0.3). No open design decision remains; CSS-token-only change. Confirmed still unimplemented in code as of planning (`DashboardHome.js:36`, `StrategyBenchmark.js` still bare `text-white`). `BLG-FE-106` (PageHeader component consolidation) is an explicitly out-of-scope follow-up filed at the design gate — do not bundle into this story.

**Staging-only ACs:** None — contrast/colour is a Playwright-checkable computed-style assertion in both themes.

---

#### ST-09 — Positions Table View breach badge does not match approved spec colour/label (BLG-FE-96)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Design gate: Design Pre-Approved — `positions.md` already specifies `#EA580C` / "⚠ BREACH"; pure conformance fix (`Positions.js`), no design decision.

**Staging-only ACs:** None — badge colour/label is a Playwright-checkable computed-style/text assertion.

---

#### ST-10 — Gate Progress Indicator copy divergence (BLG-SPEC-73)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Design gate: Design Pre-Approved — wording-only AC, FI-P3-02 exception applies (per CLAUDE.md — code review of static JSX/text may substitute for staging sign-off; no visual/colour/layout claim).

**Staging-only ACs:** None — FI-P3-02 code-review exception applies; no Playwright/staging evidence required for this wording-only AC.

---

#### ST-11 — Add endpoint and date-range filters to `GET /ai/claude-audit-log` (BLG-BE-51)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Design gate: Design Not Applicable — backend-only, no UI change. No new endpoint (parameter addition to existing route), but per CLAUDE.md contract-currency practice, `docs/specs/api_contracts/ai_endpoints.md` and `docs/reference/openapi.yaml` must both be updated in the same commit as the parameter change.

**Staging-only ACs:** None — query-parameter filtering is unit/integration-testable.

---

#### ST-12 — Sector Concentration: join `ticker_universe` for sector data (BLG-BE-38)

**Status at sprint open: ready**

**Owner:** Head of Engineering
**Estimated effort:** XS (~2h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Design gate: Design Pre-Approved — bug fix to an existing rendering path (`backend/routers/portfolio_risk.py`); data now populates an already-specified UI state, no UI/spec change. AC-04 explicitly prohibits adding a yfinance live-call to the hot path — join must use existing `ticker_universe` table data only.

**Staging-only ACs:** None — join/query correctness is unit/integration-testable.

---

### EPIC-03 — User-Facing Feature Enhancements

**Maps to:** S2-03
**Owner:** Financial Reporting & Records Owner
**Estimated effort:** ~5.0 days
**Risk IDs:** RISK-03, RISK-04
**Execution sequence:** 3

#### ST-13 — Tax-year P&L CSV export (BLG-FEAT-69)

**Status at sprint open: ready**

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None (sequence before ST-14 within EPIC-03 branch to avoid `Reports.js` rebase churn — no hard blocker)

**Notes:** Design gate: Design Required — fresh decision needed because the existing v2.1 "URL-parameter only, no button" spec note was stale/never implemented and inconsistent with the shipped PDF export button. Resolved and locked at design gate: `docs/design/2026-07-12__release-v7.0/tax-year-csv-export/ux_spec.md`, `reports.md` v0.7. No open design decision remains.

**Staging-only ACs:** None — CSV export/download and figure-matching are Playwright-testable via `page.waitForEvent('download')` and mocked report-data fixtures.

---

#### ST-14 — Realized vs. unrealized gain distinction in monthly P&L (BLG-FEAT-70)

**Status at sprint open: ready**

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** ST-13 (same-file sequencing to avoid `Reports.js` rebase churn — no hard blocker, same EPIC/branch)

**Notes:** Design gate: Design Required — new data column, layout change. Resolved and locked at design gate: `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`, `reports.md` v0.7. No open design decision remains. AC's regression check (figures sum to existing combined total) should be covered by an explicit test case.

**Staging-only ACs:** None — realized/unrealized split rendering and the sum-regression check are Playwright/unit-testable with mocked P&L fixtures.

---

#### ST-15 — Position review cadence nudge (BLG-FEAT-68)

**Status at sprint open: ready**

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (independent of ST-13/ST-14 — touches position-review UI, not `Reports.js`)

**Notes:** Design gate: Design Required — new UI (days-since-review display, flag state, Mark Reviewed action). Resolved and locked at design gate: `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md`, `positions.md` v2.2. No open design decision remains. **Shared-file conflict:** also bumps `positions.md` to v2.2 independently of EPIC-01's ST-05 bump — see Merge Order section above; must rebase onto `main` after EPIC-01 (and EPIC-02, if it also touches `PositionCard.js`/`Positions.js`) merge. AC-04 (no double-flagging with Grace Period/Drawdown prompts) requires explicit precedence-order test coverage.

**Staging-only ACs:** None — days-since-review, threshold flagging, and Mark Reviewed reset are all mockable via Playwright with fixed/mocked dates and API responses.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 days |
| Total estimated effort (in-scope) | ~9.5 days |
| Utilisation | ~68–79% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 15 ST items from the authoritative backlog slice are `include`. See `release_plan.md §Scope → Items explicitly deferred` for items considered and not selected at release planning (`BLG-FEAT-66`, `BLG-FEAT-67`, and all SI-02/SI-04/PO-02/Arc-gated items) — out of this routine's scope to revisit.

## Deferred Execution Blockers Accepted

*(omitted — `state.json deferred_execution_blockers` is empty for this cycle)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Confirm 24-hour capture-window default for ST-07's `trailing_stop_recommendation_log` (AC: "Capture window ... confirmed by Product Owner") | Product Owner (delegated authority — confirmed at planning: 24-hour default accepted as proposed) | No |
| Rebase `positions.md`/`PositionCard.js` edits in EPIC-03 (ST-15) onto `main` after EPIC-01 merges (shared-file conflict, see Merge Order) | Head of Engineering / Financial Reporting & Records Owner | No — execution-time sequencing note, not a planning-seal blocker |

No outstanding action is marked `Blocker? Yes`.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-13
**Scope confirmed:** Confirmed — 2026-07-13 (15 ST items, 3 EPICs, all Firm, within capacity — ~9.5 of ~12–14 days)
**Capacity confirmed:** Confirmed — 2026-07-13 (~9.5 days estimated against ~12–14 days available, no over-allocation, capacity check outcome `pass`)
**Deferred execution blockers accepted (if any):** N/A — none present (`state.json deferred_execution_blockers` empty)
**Signed off by:** Product Owner (delegated authority, consistent with the release plan's own delegated scope-maximisation decision and `2026-07-10__release-v6.9` sign-off precedent)
**Date:** 2026-07-13
