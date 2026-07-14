**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-14
**Cycle:** 2026-07-14__release-v7.1
**Release:** v7.1

<!-- release-plan-marker: RP:v7.1:2026-07-14__release-v7.1 -->

# Stage 4 Backlog Slice — v7.1 Nightly Backtest Data Integrity

## EPIC-01 — Nightly Backtest Data Integrity

**Maps to:** S2-01, S2-02
**Owner:** Backend Engineering Patterns Owner

Two P1 correctness bugs in the nightly backtest job (`import_backtest.py` / `production_strategy.py`) feeding the user-visible Strategy Benchmark page's backtest-vs-actual comparison. Surfaced via STEP 8.0 Production Correctness Fast-Track, 2026-07-13.

### ST-01 — Gate nightly backtest ticker eligibility on ticker_universe.created_at

**Backlog ref:** `BLG-BE-59`
**Owner:** Backend Engineering Patterns Owner
**Effort:** M (~1-2 days)
**Delegation class:** autonomous
**Spec references:** `backend/services/production_strategy.py` (`_load_tickers()`, `compute_signals()` lines 199-204), `backend/services/ticker_universe_service.py:100`

**Problem:** `_load_tickers()` pulls whatever is currently `active=TRUE` in `ticker_universe`, and `compute_signals()` ranks momentum across all of those tickers on every historical date back to 2018 in one DataFrame-wide computation — there is no concept of "this ticker wasn't tracked yet as of this date." Adding a ticker today retroactively injects its momentum score into the ranking competition for the entire 2018-present window, changing which trades were selected, when they exited, and (via the compounding fully-invested cash simulation) the dollar size of every subsequent trade, even trades that closed months or years ago. `ticker_universe.created_at` already exists and is unused for this purpose.

**Acceptance Criteria:**
- AC-01: Each ticker's eligibility in the momentum/trend signal computation is gated on its own `created_at` date — `signals` is masked to `False` for a ticker before its `created_at`.
- AC-02: Adding a new ticker to `ticker_universe` only affects selections from today forward; closed historical trades are unaffected by a subsequent ticker addition (verified via a before/after backtest re-run comparison on a fixed historical window).
- AC-03: No change to trades/exits on the portion of the historical window preceding any newly-added ticker's `created_at`.

**Staging-only ACs:** None — all ACs verifiable via backtest re-run comparison in CI/local test.

---

### ST-02 — Fix nightly backtest total_pnl_gbp non-reproducibility

**Backlog ref:** `BLG-BE-60`
**Owner:** Backend Engineering Patterns Owner
**Effort:** L (~3-5 days)
**Delegation class:** autonomous
**Spec references:** `import_backtest.py`, `production_strategy.py` (fully-invested compounding cash simulation), GH Actions nightly backtest job logs 2026-07-09–2026-07-13

**Problem:** `trades_imported`/`open_positions_imported` stayed flat at 587/5 (zero exits) across 5 consecutive nightly runs, yet `total_pnl_gbp` swung by tens of thousands of GBP night to night. Diffing trade rows between consecutive runs showed every trade shifted PnL(£) by an identical ratio (×1.02701) while PnL% and dates stayed byte-identical — consistent with a single global rescaling of the compounding cash trajectory, most likely from `yfinance`'s `auto_adjust=True` retroactively revising a historical adjusted close on the nightly full re-download-and-re-simulate. Because position sizing is fully-invested and compounding, any tiny historical price revision rescales every subsequent trade's dollar PnL. `import_backtest.py` already prints a "Total P&L drift check" but nothing monitors or alerts on it.

**Acceptance Criteria:**
- AC-01: A fix vehicle is selected and implemented from the candidate set — (a) persist/cache historical price data and only extend forward rather than re-downloading/re-simulating the full 8-year window nightly, (b) make the trade ledger append-only (write only newly-closed trades instead of deleting/reinserting all rows every run), or (c) at minimum, wire the existing drift-check output into an actual alert/threshold so an unexpected swing is flagged rather than silently logged. Fix vehicle choice recorded in sprint planning notes (RISK-01).
- AC-02: Two consecutive nightly runs with zero new exits produce byte-identical (or documented-tolerance) `total_pnl_gbp` — verified via a controlled re-run comparison.
- AC-03: If option (c) is the selected/interim vehicle, the drift-check threshold and alert destination are documented and testable (e.g. CI assertion or a monitored log pattern).

**Staging-only ACs:** [If option (a) or (b) is selected and requires a live nightly GH Actions run to confirm reproducibility over consecutive real nights] "AC-02 (night-to-night reproducibility under production nightly schedule)" — flag for human staging sign-off if not fully reproducible in a local/CI simulated re-run. Confirm at execution time based on fix vehicle chosen.

---

## EPIC-02 — Table View Badge Spec Compliance

**Maps to:** S2-03
**Owner:** Head of Engineering / Head of UX & Design
**Sequencing constraint:** After Design Gate passes (RISK-03) — `design_gate_required = true`.

### ST-03 — Table View RISK OFF badge colour/label spec compliance

**Backlog ref:** `BLG-FE-107`
**Owner:** Head of Engineering
**Effort:** S (~0.5 day)
**Delegation class:** autonomous (post-design-gate)
**Spec references:** `docs/specs/frontend/pages/positions.md` §Alerts Column, `src/pages/Positions.js` (`AlertsCell`), `tests/e2e/epic01-v62-stops-alerts.spec.js` (`SC-RO-02`), v7.0 combined-badge differentiation decision record, deviation `DEV-EPIC01-ST05-01`

**Problem:** `positions.md` §Alerts Column specifies the RISK OFF badge as Label "RISK OFF", Background `#1E40AF` (blue-800). The shipped Table View implementation instead renders `bg-amber-900/60 text-amber-300`, label "Risk-Off", plus a `ShieldAlert` icon not in spec — pre-existing since v6.2, encoded as expected by passing test `SC-RO-02`. The v7.0 Grid View RISK OFF badge (ST-02) correctly uses the spec's blue `#1E40AF`, so Table View and Grid View are now visually inconsistent for the same badge, undermining the v7.0 combined-badge differentiation decision record's "hue separation" rationale for Table View specifically (both RISK OFF and GAP RISK currently render in the amber family there).

**Acceptance Criteria:**
- AC-01: Design gate resolves the treatment — either (a) bring Table View into spec compliance (`#1E40AF`, "RISK OFF" label) and update `SC-RO-02`'s amber assertion, or (b) formally accept amber as canonical Table View treatment and update `positions.md` + the combined-badge decision record to match.
- AC-02: Table View and Grid View RISK OFF badges use a single, consistent, spec-documented colour/label per the design gate's resolution.
- AC-03: `SC-RO-02` and the v7.0 Grid View parity tests (`SC-GVP-02`) remain internally consistent with whichever treatment is chosen.
- AC-04: Combined-badge differentiation decision record's hue-separation rationale is verified true for both views after the change.

**Staging-only ACs:** None — AC-02/AC-03 are colour/label rendering claims requiring Playwright coverage (existing `SC-RO-02`/`SC-GVP-02` updated in place); no new staging-only evidence needed beyond existing CI coverage.

---

## EPIC-03 — v7.0 Post-Ship Hardening

**Maps to:** S2-04, S2-05, S2-06, S2-07
**Owner:** Backend Engineering Patterns Owner / QA & Testing Owner / Data Model & Domain Schema Owner / API Contracts & Documentation Owner

Four capacity-filling hardening passes closing gaps identified in v7.0 shipped features (position review-cadence nudge, realized/unrealized P&L split, tax-year P&L CSV export). All items carry `Provisional-Target: v7.1`.

### ST-04 — Position review-cadence nudge: backend/data-integrity hardening pass

**Backlog ref:** `BLG-BE-61`
**Owner:** Backend Engineering Patterns Owner
**Effort:** M
**Delegation class:** autonomous
**Spec references:** `docs/specs/strategy_rules.md §9`, `docs/specs/frontend/pages/positions.md`, `PATCH /positions/{id}/mark-reviewed`

**Acceptance Criteria:**
- AC-01: IDOR regression check confirming `PATCH /positions/{id}/mark-reviewed` enforces the same portfolio-ownership check as other position-mutating endpoints — documented with pass/fail result.
- AC-02: NULL/backfill semantics for `last_reviewed_at` on pre-existing (pre-v7.0) positions defined and verified against production data.
- AC-03: Explicit written confirmation in `strategy_rules.md §9` or `positions.md` that the review-cadence concept is a metadata annotation, not a 5th position lifecycle state (state machine remains GRACE → LOSING → PROFITABLE → EXIT ZONE, 4 states unchanged).

**Staging-only ACs:** None — verifiable via code review + production data query.

---

### ST-05 — Position review-cadence nudge: frontend/QA polish pass

**Backlog ref:** `BLG-QA-106`
**Owner:** QA & Testing Owner
**Effort:** M
**Delegation class:** autonomous (UX consistency sub-item routed through design gate, RISK-04)
**Spec references:** `docs/specs/frontend/pages/positions.md`, Arc 3 structured prompts (grace period alert, drawdown review), FI-P3-01 advisory

**Acceptance Criteria:**
- AC-01: Explicit `data-testid` confirmed present on the nudge component (per standing FI-P3-01 advisory).
- AC-02: Ordering/coexistence rule documented in `positions.md` for when the nudge fires alongside other structured position prompts (grace period alert, drawdown review, etc.).
- AC-03: UX consistency review against Arc 3 prompt visual precedents completed, sign-off recorded (via design gate, RISK-04).
- AC-04: Acceptance criteria for the nudge traced to a canonical `positions.md` section (not ad hoc).
- AC-05: ≥1 dedicated (not bundled-generic) Playwright scenario for the nudge, passing in CI.

**Staging-only ACs:** AC-03 (UX consistency review) — visual/design judgment call; requires design gate sign-off or human staging review, not code-review-only (per CLAUDE.md observable-AC rule).

---

### ST-06 — Realized/unrealized P&L split: spec & metrics hardening pass

**Backlog ref:** `BLG-SPEC-83`
**Owner:** Data Model & Domain Schema Owner
**Effort:** M
**Delegation class:** autonomous
**Spec references:** v7.0 EPIC-03 ST-14 (`BLG-FEAT-70`), `docs/reference/openapi.yaml`, `claude/system/metrics_definitions.md` (or equivalent canonical metrics doc)

**Acceptance Criteria:**
- AC-01: Stored-vs-computed-on-read ownership decision for realized/unrealized P&L values documented.
- AC-02: Exact currency/rounding rules stated for the Base44 frontend prompt.
- AC-03: Reconciliation rule confirming `realized + unrealized` ties back to the existing net P&L figure — defined and verified against at least one real portfolio's figures.
- AC-04: Visual treatment confirmed distinct from (or explicitly aligned with) the pre-existing P&L colour convention.
- AC-05: Formal `metrics_definitions.md` entry added.
- AC-06: `openapi.yaml` examples confirmed to reflect the realized/unrealized split (same-commit rule per CLAUDE.md).
- AC-07: ≥1 dedicated Playwright scenario for the split (companion to ST-05's nudge coverage), passing in CI.

**Staging-only ACs:** AC-04 (visual treatment) — colour/layout claim; Playwright coverage required or human staging sign-off if not covered by AC-07's scenario.

---

### ST-07 — Tax-year P&L CSV export: spec & test hardening pass

**Backlog ref:** `BLG-SPEC-84`
**Owner:** API Contracts & Documentation Owner
**Effort:** M
**Delegation class:** autonomous
**Spec references:** v7.0 EPIC-03 ST-13 (`BLG-FEAT-69`), `backend/backend_engineering_patterns.md`, `docs/reference/openapi.yaml`

**Acceptance Criteria:**
- AC-01: Response `Content-Type`/charset/filename convention documented.
- AC-02: `X-API-Key` auth enforcement parity with other financial endpoints confirmed.
- AC-03: Financial-record-vs-analytics-export classification made, with a versioning decision recorded.
- AC-04: Smoke-test/health-check harness coverage added confirming endpoint reachability.
- AC-05: A content-asserting test added (asserts actual CSV file contents, not just that a download was triggered).
- AC-06: Written test scenario document authored.
- AC-07: Canonical CSV/export response-body pattern entry added to `backend_engineering_patterns.md` for future export endpoints.

**Staging-only ACs:** None — all ACs verifiable via code review, CI test, and documentation review.

---

## Deferred Items

| Item | Reason |
|------|--------|
| `BLG-BE-62` | `Provisional-Target: TBD` — broader cross-job idempotency audit, not scoped to v7.1 |
| `BLG-SPEC-85` | `Provisional-Target: TBD`, P3 — deferred |
