**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-08
**Window:** IW-20261008-01

# Idea Intake Summary — IW-20261008-01

## Window Status: Closed

Opened: 2026-10-08T08:47:00Z
Closed: 2026-10-08T09:05:00Z

Invoked inline as STEP -1.6 of `run roadmap --reason "scheduled"` (`2026-10-08__scheduled`). The register held 0 open ideas, below the 20 threshold. Mode: `standard`.

**Reduced-roster disclosure:** this window opened for 4 of the 22 eligible roles: Product Owner, Head of UX & Design, Head of Engineering, and Frontend Specifications & UX Documentation Owner. The user, acting as Product Owner, chose this in-session on 2026-10-08. Their reason: the active backlog (~215 items) already far exceeds one release's capacity, and the rebalance was needed only to open v9.11. Precedents: `IW-20260928-01`, `IW-20260930-01`. **Roster rule (§2.1 step 2a):** a build-and-ship pull-forward is mandatory, because the latest `product_value_ratio_history.md` row is in the Alert tier and `2026-10-06__scheduled` recorded a §7.1 sustained-failure pull-forward. The window therefore had to include at least one user-facing role. All 4 participating roles are user-facing. The other 18 roles stay eligible at the next full-roster window. `BLG-GOV-364` (whether reduced rosters should be permitted at all) remains open.

**Stale-idea horizon check (STEP -0.5):** 0 rows at `Parked-cycle-2`, so no advisory.

**Parked queue pre-check (§2.0):** no `Parked-cycle-<n>` rows exist, so there was no overlap case.

**Surface chosen:** the Risk Dashboard (`src/pages/RiskDashboard.js` and `src/components/risk/*`). It has 0 mentions in the active backlog, and `IW-20261006-01` did not review it (that window read Settings, Trade Entry, Positions and the exit dialog). Each submission was read against `docs/specs/frontend/pages/risk_dashboard.md`, `backend/services/portfolio_service.py` (`GET /portfolio`) and `strategy_rules.md`.

**Backlog scope overlap check (§2.0 step 5):** grepped `backlog.md`/`backlog_archive.md` for `holding_days`, `PositionRiskTable`, `stop dist`, `Grace Period Positions`, `not enforced`, `1.38`, `entity fallback`, `Risk Dashboard`. Adjacent but distinct: `BLG-BE-149` (Risk page `display_status` uses the GBP P&L sign; a different field), `BLG-BE-147` (Positions-page grace alert counts `days_in_state`; a different page and field), and archived `BLG-RD-03` (sort order, shipped). **0 restatements.**

**Codebase overlap check (§2.0 step 6):** confirmed in code: `portfolio_service.py` reads `pos.get('holding_days', 0)` from the stored row (refreshed only by `GET /positions/analyze`), while `position_service.py` and `main.py` compute `calculate_holding_days(entry_date)` live. Also confirmed: the ×1.38 stored-price heuristic at `portfolio_service.py:122`; `PositionRiskTable.js` formatting `entry_price` with `currencyForMarket(market)` although the API returns GBP; and `current_stop` converted at the stored entry FX against `current_price` at live FX. **0 already-implemented topics.**

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|-----------------|--------------------|-------|
| Product Owner | 2 | 0 | 2 |
| Head of UX & Design | 2 | 0 | 2 |
| Head of Engineering | 2 | 0 | 2 |
| Frontend Specifications & UX Documentation Owner | 2 | 0 | 2 |
| **Total** | **8** | **0** | **8** |

## Agents Without Minimum Submissions

None. All 4 participating roles met the 2-idea minimum. The 18 roles not opened were left out by a disclosed scoping choice; this is not a §2.3 shortfall.

## Ideas Available for Roadmap STEP 4

| Idea ID | Agent | Title | Recommendation | Status |
|---------|-------|-------|----------------|--------|
| IDEA-product-owner-20261008-01 | Product Owner | Risk page shows a live stop and red stop-distance for grace positions, though §5/§6.3 say the stop is not enforced in grace | Now | Submitted |
| IDEA-product-owner-20261008-02 | Product Owner | Link each Risk Dashboard grace-panel row to that position on the Positions page | Soon | Submitted |
| IDEA-head-of-ux-20261008-01 | Head of UX & Design | Position Risk table prints US entry prices with a $ sign on GBP-converted values | Now | Submitted |
| IDEA-head-of-ux-20261008-02 | Head of UX & Design | Align Grace Period panel heading, count badge and entry-date format with `risk_dashboard.md` §5.2 | Soon | Submitted |
| IDEA-head-of-engineering-20261008-01 | Head of Engineering | `GET /portfolio` reads stored `holding_days`; compute it live from `entry_date` | Now | Submitted |
| IDEA-head-of-engineering-20261008-02 | Head of Engineering | `GET /portfolio` fabricates a US price via a hard-coded ×1.38 FX guess when the live fetch fails | Now | Submitted |
| IDEA-frontend-specs-20261008-01 | Frontend Specifications & UX Documentation Owner | Stop Dist % mixes live-FX price with entry-FX stop for US positions | Now | Submitted |
| IDEA-frontend-specs-20261008-02 | Frontend Specifications & UX Documentation Owner | Reconcile `risk_dashboard.md` §5.1/§6 data sources with shipped `GET /portfolio` fields | Soon | Submitted |

## Parked Ideas Carried Forward (Not Resubmitted)

None.

## Idea Details

Full template fields are recorded here rather than in per-idea files, because the window is small (the `IW-20260928-01`/`IW-20260930-01` convention).

### IDEA-product-owner-20261008-01 — Grace positions shown with an enforced-looking stop on the Risk page

- **Problem Statement:** `PositionRiskTable.js` shows `current_stop` and a red/amber "Stop Dist %" for every row, GRACE rows included. `GET /portfolio` returns the stored `current_stop` for grace positions. The Positions page (`GET /positions`) returns `stop_price = 0` during grace. The two pages therefore disagree, and the Risk page implies a live exit level that the system will not act on.
- **Strategic Alignment:** §5 ("The stop is not enforced during the grace period") and §6.3. The surface states the opposite of the rule.
- **Proposed Solution:** for GRACE rows, show "Not enforced (grace)" in the Stop Price and Stop Dist % cells and exclude them from the at-risk colouring.
- **Expected Value:** removes 1 cross-page contradiction about the rule that governs a position's first 10 days. Every grace position currently shows a misleading stop.
- **Effort Estimate:** Small (~0.5 day). Frontend only; Playwright AC required.
- **Reversibility:** Fully reversible (display only).
- **What Would You Stop?** No view — leave to debate.
- **Recommendation:** Now. It is a user-visible strategy contradiction.
- **Build-and-ship:** yes.

### IDEA-product-owner-20261008-02 — Link grace-panel rows to the Positions page

- **Problem Statement:** the Grace Period panel lists tickers but has no route to the position, where notes, exit and stop detail live. The user has to find it again on Positions.
- **Strategic Alignment:** §6.3: the grace window is when the user should review without acting reactively. Getting quickly to the position's thesis and notes supports that.
- **Proposed Solution:** make each grace row a link to the Positions page, filtered or scrolled to that position.
- **Expected Value:** reaching a grace position's detail from the Risk page drops from about 3 actions to 1.
- **Effort Estimate:** Small (~0.5 day).
- **Reversibility:** Fully reversible.
- **What Would You Stop?** No view — leave to debate.
- **Recommendation:** Soon. Useful, not a correctness issue.
- **Build-and-ship:** yes (second candidate).

### IDEA-head-of-ux-20261008-01 — Wrong currency symbol on US entry prices in Position Risk

- **Problem Statement:** `portfolio_service.py` converts US `entry_price` to GBP (`entry_price / stored_fx_rate`). `PositionRiskTable.js` then formats it with `currencyForMarket(market)`, which prints "$" for US. `risk_dashboard.md` §6.2 specifies GBP for every price column. A US entry price shows as, for example, "$78.74" when the real entry was $100.00 (£78.74).
- **Strategic Alignment:** §2: decisions rest on accurate data. A wrong currency symbol on an entry price misstates the position's basis.
- **Proposed Solution:** format the Entry Price cell as GBP, matching Current and Stop and the spec.
- **Expected Value:** every US row's entry price becomes correctly labelled. It is currently wrong on 100% of US rows.
- **Effort Estimate:** Small (~0.25 day) plus a Playwright check.
- **Reversibility:** Fully reversible.
- **What Would You Stop?** No view — leave to debate.
- **Recommendation:** Now.
- **Build-and-ship:** yes.

### IDEA-head-of-ux-20261008-02 — Grace panel text and format drift from spec

- **Problem Statement:** `risk_dashboard.md` §5.2 specifies the heading "Grace Period Positions", a badge reading "N positions in grace period", and entry dates as DD MMM YYYY. `GracePeriodPanel.js` renders "Grace Period", "N positions" and `dd MMM yy`.
- **Strategic Alignment:** §2 consistency. A small spec-conformance gap on a user-facing panel.
- **Proposed Solution:** align the three strings and the format with §5.2, or amend the spec if the shipped text is preferred.
- **Expected Value:** clears 3 spec/UI mismatches on one panel.
- **Effort Estimate:** Small (~0.25 day). Wording-only ACs may use code review (FI-P3-02).
- **Reversibility:** Fully reversible.
- **What Would You Stop?** No view — leave to debate.
- **Recommendation:** Soon.
- **Build-and-ship:** yes (small).

### IDEA-head-of-engineering-20261008-01 — Live `holding_days` on `GET /portfolio`

- **Problem Statement:** `GET /portfolio` takes `holding_days` from the stored `positions` row, which only `GET /positions/analyze` refreshes. `GET /positions` and `GET /positions/{id}` compute `calculate_holding_days(entry_date)` live. When the analyze path has not run that day, the Risk page's GRACE/LOSING/PROFITABLE status, "Held" column and grace countdown lag the Positions page by a day or more. On the day-10 boundary, a position can show GRACE on one page and post-grace on the other.
- **Strategic Alignment:** §6 (10 calendar days) and the role-charter rule that "UI, backend logic, and analytics interpret states consistently".
- **Proposed Solution:** compute `holding_days` live from `entry_date` in `portfolio_service.py`. Check the other stored readers (`alerts_service.py`, `compliance_service.py`) and either fix them in the same change or list them as follow-ups.
- **Expected Value:** the Risk and Positions pages agree on grace status every day, not only after an analyze run.
- **Effort Estimate:** Small (~1 day), including a unit test on the day-10 boundary.
- **Reversibility:** Fully reversible.
- **What Would You Stop?** No view — leave to debate.
- **Recommendation:** Now. It is correctness on the grace boundary.
- **Build-and-ship:** yes (user-visible status change).

### IDEA-head-of-engineering-20261008-02 — Remove the ×1.38 fabricated US price fallback

- **Problem Statement:** when the live price fetch fails, `portfolio_service.py:118-124` treats a stored US price below 500 as GBP and multiplies it by a hard-coded 1.38 to "estimate USD". That figure feeds the position's value, P&L, total portfolio value, drawdown and heat on the Dashboard and Risk pages, and nothing on screen marks it as estimated. v9.10 removed the same class of silent fallback for ATR (ST-02).
- **Strategic Alignment:** §2 (decisions on real data) and §11 (no hidden parameters). 1.38 is an undocumented FX constant.
- **Proposed Solution:** use the stored native price (or entry price) without the FX guess, return a `price_is_stale` flag, and show a stale marker on the affected rows.
- **Expected Value:** removes an error that can reach about 10% of a US position's value (1.38 against a live ~1.25–1.35) on every live-price outage, and makes the outage visible.
- **Effort Estimate:** Small–Medium (~1–1.5 days) across backend, contract (`portfolio_endpoints.md`, `openapi.yaml`) and frontend marker.
- **Reversibility:** Mostly reversible (additive response field).
- **What Would You Stop?** No view — leave to debate.
- **Recommendation:** Now.
- **Build-and-ship:** yes.

### IDEA-frontend-specs-20261008-01 — Stop Dist % for US positions uses two different FX rates

- **Problem Statement:** `GET /portfolio` converts `current_price` to GBP at the live FX rate and `current_stop` at the stored entry FX rate. `PositionRiskTable.js` computes `(current_price − current_stop) / current_price` from those two numbers. For US positions, the distance therefore includes FX drift since entry: at entry 1.27 and live 1.35, a true 8% distance shows as about 2%, or turns negative.
- **Strategic Alignment:** §7 (trailing stop) and §2. The "distance to stop" the user reads is not the distance at which the system will exit.
- **Proposed Solution:** compute stop distance in native currency (on the backend as `stop_distance_pct`, or on the frontend from native fields). Update `risk_dashboard.md` §6 to define it.
- **Expected Value:** for US positions, the error in Stop Dist % (currently equal to FX drift since entry) falls to 0, and the "most at risk first" sort uses true distance.
- **Effort Estimate:** Small (~1 day) including spec and contract update.
- **Reversibility:** Fully reversible.
- **What Would You Stop?** No view — leave to debate.
- **Recommendation:** Now.
- **Build-and-ship:** yes.

### IDEA-frontend-specs-20261008-02 — Reconcile `risk_dashboard.md` data-source wording with `GET /portfolio`

- **Problem Statement:** `risk_dashboard.md` §5.1 says the grace panel takes "positions where `status = "GRACE"`". The API returns `status: "open"` with a `grace_period` boolean and a `display_status` field, and the component filters on `grace_period`. The spec describes a field value that never occurs.
- **Strategic Alignment:** spec accuracy (Head of Specs canonical-truth rule). Not a strategy section; documentation debt.
- **Proposed Solution:** amend §5.1/§6.1 to name `grace_period` and `display_status`.
- **Expected Value:** 1 canonical spec section matches the shipped contract.
- **Effort Estimate:** Small (~0.25 day).
- **Reversibility:** Fully reversible.
- **What Would You Stop?** No view — leave to debate.
- **Recommendation:** Soon.
- **Build-and-ship:** no (documentation).

## Notes

Build-and-ship candidates (§2.1 step 2a): 7 — `IDEA-product-owner-20261008-01`, `-02` (Product Owner); `IDEA-head-of-ux-20261008-01`, `-02` (Head of UX & Design); `IDEA-head-of-engineering-20261008-01`, `-02` (Head of Engineering); `IDEA-frontend-specs-20261008-01` (Frontend Specifications & UX Documentation Owner). User-facing roles with none: None among the 4 participating roles. Base44 Frontend Prompt Owner was not opened (reduced roster).

No `[FIELD REQUIRED]` flags.
