Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-24

---

**EPIC:** EPIC-01 — Strategy Parity: Core Engine Alignment
**Cycle:** 2026-06-24__release-v6.2
**Sprint goal:** Sprint 1: Ship the production strategy parity cluster — nightly trailing stop computation with breach badge, month-end rebalance exit signals, inverse-volatility position sizing for signal entries, and risk-off exit alerts.
**Test scenarios used:** Derived from spec + AC (tests/e2e/ Playwright specs to be added by Head of Engineering alongside implementation)

---

## Story Evidence

### ST-01 — Nightly trailing stop computation — backend service

**Delegation class:** delegated_backend
**Assigned to:** Head of Engineering
**Delegation record:** DEL-20260624-01
**GitHub issue:** #839
**Spec reference:** docs/specs/api_contracts/position_endpoints.md#GET /positions
**Branch:** exec/2026-06-24__release-v6.2/EPIC-01

| AC | Description | Result |
|----|-------------|--------|
| AC-01 | Nightly job computes trailing stop using profit-lock logic: profit → `price − 2×ATR`, else `entry − 5×ATR` | Pending — awaiting HoE commit |
| AC-02 | Ratchet enforced: `max(CurrentStop, NewStop)` — stop only moves up | Pending — awaiting HoE commit |
| AC-03 | Updated stop stored per position; retrievable via GET /positions as `current_trailing_stop` | Pending — awaiting HoE commit |
| AC-04 | Logic matches `production_strategy.py`: `INITIAL_ATR_MULT=5`, `PROFIT_ATR_MULT=2`, `ATR_PERIOD=14` | Pending — awaiting HoE commit |
| AC-05 | `initial_stop` field unchanged — `current_trailing_stop` is additive | Pending — awaiting HoE commit |

**Notes:** Unit tests must cover profit-lock branch, ratchet invariant, and reference-input validation. Regression: GET /positions response schema unchanged.

---

### ST-02 — Trailing stop display and breach badge — frontend

**Delegation class:** delegated_frontend
**Assigned to:** Head of Engineering
**Delegation record:** DEL-20260624-02
**GitHub issue:** #840
**Spec reference:** docs/specs/frontend/pages/positions.md
**Branch:** exec/2026-06-24__release-v6.2/EPIC-01
**Dependency:** ST-01 must be done first

| AC | Description | Result |
|----|-------------|--------|
| AC-01 | Each open position displays `current_trailing_stop` alongside `initial_stop` | Pending — awaiting HoE commit |
| AC-02 | Breach badge/alert shown when `current_price ≤ current_trailing_stop` | Pending — awaiting HoE commit |
| AC-03 | Breach badge visually distinct from other status indicators (colour/icon) | Pending — **staging-only: requires human staging sign-off** |
| AC-04 | No breach badge when position is within stop bounds | Pending — awaiting HoE commit |

**Notes:** Design spec: `docs/design/2026-06-24__release-v6.2/trailing-stop-display/ux_spec.md`. Layout advisory: if >~15 columns cause scroll, Initial Stop + Trail Stop may be combined into a two-line cell (implementation-level decision, no spec amendment). Playwright must cover AC-01, AC-02, AC-04. AC-03 requires human staging sign-off with date recorded here before PR opens.

---

### ST-03 — Month-end rebalance exit signal generation

**Delegation class:** delegated_backend
**Assigned to:** Head of Engineering
**Delegation record:** DEL-20260624-03
**GitHub issue:** #841
**Spec reference:** docs/specs/api_contracts/signal_endpoints.md#GET /signals
**Branch:** exec/2026-06-24__release-v6.2/EPIC-01

| AC | Description | Result |
|----|-------------|--------|
| AC-01 | On last trading day of each calendar month, computes open positions NOT in top-5 momentum list | Pending — awaiting HoE commit |
| AC-02 | Signal record `status = exit_rebalance` generated for each such position | Pending — awaiting HoE commit |
| AC-03 | Month-end detection uses last trading day logic (weekend/holiday aware) | Pending — awaiting HoE commit |
| AC-04 | No duplicate `exit_rebalance` if position also crossing a stop | Pending — awaiting HoE commit |
| AC-05 | `exit_rebalance` in GET /signals; distinct label/styling from stop exits | Pending — **AC-05 styling: staging-only staging sign-off required** |

**Notes:** Design spec: `docs/design/2026-06-24__release-v6.2/rebalance-exit-signal-style/ux_spec.md`. Pre-check: confirm `stop_exit` is live before applying red badge styling — if not live, defer badge variant. Playwright must cover `exit_rebalance` label presence (AC-05 label part). Styling confirmation is staging-only.

---

### ST-04 — Inverse-volatility position sizing for signal-driven entries

**Delegation class:** delegated_backend
**Assigned to:** Head of Engineering
**Delegation record:** DEL-20260624-04
**GitHub issue:** #842
**Spec reference:** docs/specs/api_contracts/signal_endpoints.md#POST /signals/generate
**Branch:** exec/2026-06-24__release-v6.2/EPIC-01

| AC | Description | Result |
|----|-------------|--------|
| AC-01 | Inv-vol weights computed: `weight_i = (1/ATR_i) / Σ(1/ATR_j)` | Pending — awaiting HoE commit |
| AC-02 | Each weight constrained to `[5%, 20%]` of available cash, re-normalised to sum to 100% | Pending — awaiting HoE commit |
| AC-03 | New signal allocations use inv-vol sizing (not fixed-risk £200 model) | Pending — awaiting HoE commit |
| AC-04 | Manual position sizing path unchanged (RISK-03 regression protection) | Pending — awaiting HoE commit |
| AC-05 | Sizing matches `production_strategy.py` backtest logic for known batch input | Pending — awaiting HoE commit |

**Notes:** RISK-03 — high regression risk. AC-04 is critical: manual sizing path must produce identical output before and after this change. Unit test with known batch case required for AC-05.

---

### ST-05 — Risk-off exit alerts for existing positions

**Delegation class:** delegated_backend
**Assigned to:** Head of Engineering
**Delegation record:** DEL-20260624-05
**GitHub issue:** #843
**Spec reference:** docs/specs/api_contracts/position_endpoints.md#GET /positions
**Branch:** exec/2026-06-24__release-v6.2/EPIC-01

| AC | Description | Result |
|----|-------------|--------|
| AC-01 | Nightly regime check: `SPY < MA200` → flag US positions; `FTSE < MA200` → flag UK positions with `risk_off_exit` | Pending — awaiting HoE commit |
| AC-02 | `risk_off_exit` alert visible per position, visually distinct from trailing stop breach and `exit_rebalance` | Pending — **styling: staging-only sign-off required** |
| AC-03 | Alerts clear when relevant index recovers above MA200 | Pending — awaiting HoE commit |
| AC-04 | US risk-off does NOT trigger UK alerts, and vice versa | Pending — awaiting HoE commit |

**Notes:** Design spec: `docs/design/2026-06-24__release-v6.2/risk-off-exit-alert/ux_spec.md`. Sprint 2 (ST-06 daily briefing) depends on `risk_off_exit` alerts being live — verify AC-01/03/04 before Sprint 1 close. Playwright covers AC-01/AC-03/AC-04. AC-02 styling is staging-only.

---

## Consolidation Block

**EPIC:** EPIC-01 — Strategy Parity: Core Engine Alignment
**Cycle:** 2026-06-24__release-v6.2
**Sprint goal:** Sprint 1: Ship the production strategy parity cluster

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | position_endpoints.md#GET /positions | Nightly trailing stop computation service | AC-01–05 | Pending DoQ | None |
| ST-02 | frontend/pages/positions.md | Trailing stop display + breach badge | AC-01–04 (AC-03 staging) | Pending DoQ | None |
| ST-03 | signal_endpoints.md#GET /signals | Month-end rebalance exit signal generation | AC-01–05 (AC-05 styling staging) | Pending DoQ | None |
| ST-04 | signal_endpoints.md#POST /signals/generate | Inverse-volatility position sizing | AC-01–05 | Pending DoQ | None |
| ST-05 | position_endpoints.md#GET /positions | Risk-off exit alerts | AC-01–04 (AC-02 styling staging) | Pending DoQ | None |

**QA test coverage:**
- Scenarios run: Playwright E2E (to be confirmed post-implementation) + unit tests (backend logic) + staging sign-off (AC-02/ST-02, AC-05 styling/ST-03, AC-02 styling/ST-05)
- Regression areas checked: GET /positions response schema, manual sizing path (RISK-03), GET /signals response
- Known deviations filed: None at sprint open

**Staging-only ACs requiring human sign-off before PR merge:**
- ST-02/AC-03: Breach badge visual distinctiveness
- ST-03/AC-05: `exit_rebalance` visual distinctiveness from stop exits
- ST-05/AC-02: `risk_off_exit` styling vs. other alerts

---

## Sign-Off Block

> **Date field requirement:** Date must be non-blank before the PR can be opened. Staging sign-off dates for AC-02/ST-02, AC-05 styling/ST-03, and AC-02/ST-05 must also be recorded here.

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked (RISK-03 manual sizing path confirmed unchanged)
- [ ] Staging-only ACs signed off: ST-02/AC-03 staging date: ___; ST-03/AC-05 staging date: ___; ST-05/AC-02 staging date: ___
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm URL-base variable is exposed on imported object
- Signed off by: Director of Quality
- Date: [AWAITING — must be non-blank before PR opens]
- Comments:
