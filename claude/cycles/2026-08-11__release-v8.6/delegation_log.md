Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-11

# Delegation Log — 2026-08-11__release-v8.6

---

## DEL-20260811-02

- **ST Item:** ST-12 — Multi-currency cost-basis rounding consistency check
- **EPIC:** EPIC-04
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #1343
- **Branch:** exec/2026-08-11__release-v8.6/EPIC-04
- **Delegated at:** 2026-08-11T22:00:00Z
- **What is needed:**
  1. **Audit scope:** Systematically audit cost-basis rounding across every UK (.L) and US market call site in `backend/services/position_service.py`: `add_position()` (entry), `exit_position()` (exit/partial-exit), and any P&L/export consumers that re-derive cost basis (`reports_service.py`'s tax-year report, reconciliation report). Compare against `docs/specs/data_model.md`'s `positions`/`trade_history` schema — `entry_price NUMERIC(10,4)` vs `total_cost NUMERIC(12,2)` (2 different precisions on the same row).
  2. **Concrete finding already identified (starting point, not exhaustive):** In `add_position()`, `total_cost_gbp` is computed unrounded in Python (`total_cost_native / fx_rate_to_use` for US; `total_cost_native` directly for UK) and passed to `create_position()` — but the DB column is `DECIMAL(12,2)`, so Postgres silently truncates/rounds to 2dp on INSERT regardless of what Python sent. This means: **UK positions' persisted `total_cost` is already exact to 2dp** (native currency is GBP, no division involved) — **but US positions' persisted `total_cost` carries FX-division rounding noise baked in at the DB layer**, a rounding source UK positions never experience. Then in `exit_position()`, a partial exit computes `cost_per_share = total_cost / total_shares` (reading the already-DB-rounded `total_cost` back) and `exit_total_cost = cost_per_share * exit_shares` — for a US position with fractional shares, this re-derives a per-share cost from a value that already lost precision at both the FX-division step AND the DB DECIMAL(12,2) truncation step, then divides again by share count. UK positions only ever go through one rounding step (the DB truncation); US positions go through at least three (native fee/cost math → FX division → DB truncation → per-share re-division on partial exit). Whether the cumulative effect is material (likely sub-penny per position, but could compound across many partial exits of large US positions) has not been quantified.
  3. **Fix or document:** either (a) fix any inconsistency found (e.g. by rounding `total_cost_gbp` to 2dp explicitly in Python before persisting, so the value stored matches what was computed rather than relying on implicit DB truncation, making the rounding point explicit and auditable — same approach for both markets), or (b) if the audit concludes the discrepancy is immaterial (sub-penny, no observable financial-reporting impact), document that finding and the quantified bound explicitly in a spec/decision record, per the AC's "any inconsistency found is fixed" framing (which implies "not found" is also a valid, documented outcome).
  4. Add/extend tests confirming UK and US positions produce cost-basis values consistent with the audit's conclusion (either bit-for-bit consistent, or documented-and-bounded).
- **Spec reference:** `docs/specs/data_model.md` (`positions`/`trade_history` schema, `total_cost`/`entry_price` column precisions — locked reference); no canonical spec yet defines the intended rounding-order/point discipline for multi-currency cost basis — document the chosen approach as an addition to `data_model.md` or a new decision record in the same commit, which then becomes the locked reference.
- **Unblock criteria:** Audit complete (systematic, not just the starting-point finding above); any inconsistency found is fixed (or documented as immaterial with a quantified bound); Financial Reporting & Records Owner sign-off recorded.
- **Commit format required:** `[EPIC-04][ST-12] <description>` pushed to `exec/2026-08-11__release-v8.6/EPIC-04`
- **Status:** Unblocked

**Resolution (2026-08-12, Sprint Execution Engine acting as Head of Engineering, per explicit user direction):**
1. **Audit complete, systematic** — traced every arithmetic step from raw entry/exit price to persisted `total_cost` across all 3 named call sites (`add_position()`, `exit_position()`, `reports_service.py`'s tax-year/reconciliation/monthly-P&L consumers), not just the starting-point finding. Full write-up: `docs/product/decisions/multi-currency-cost-basis-rounding-audit--2026-08-12.md`.
2. **Finding: the delegation's own starting-point hypothesis does not survive DB persistence.** `total_cost` is `NUMERIC(12,2)` on both `positions` and `trade_history` — Postgres rounds (not truncates) every write to 2dp regardless of how many unrounded Python steps preceded it, so the US-side extra FX-division step produces no extra *persisted* imprecision versus UK. The real rounding source is market-**symmetric**: partial-exit proportional cost allocation (`cost_per_share = total_cost / total_shares`), which is currency-agnostic. Quantified, tested bound: ≤£0.02 worst-case per partial-exit sequence tested, non-compounding (each write independently rounded, not accumulated).
3. **No code fix applied** — per unblock criterion (b), documented as immaterial with a quantified, test-verified bound. Consistent with the codebase's own existing ±£0.01 reconciliation-report tolerance precedent for the same class of float-aggregation noise.
4. Tests: `tests/test_multi_currency_cost_basis_rounding_audit.py` (5 tests, exercising the REAL `add_position()`/`exit_position()`/`calculate_realized_pnl()` with only the DB layer mocked). Full backend suite (1071 tests) confirmed green.
- **Sign-off:** Financial Reporting & Records Owner: agent-mediated review, 2026-08-12 — first pass NOT CONFIRMED (one blocking finding: the test file's docstring cited a nonexistent `docs/specs/data_model.md` "DS-13" entry instead of the actual decision-record file, and referenced a stale test name), remediated in-session (docstring corrected to cite the real file/test names, plus an added caveat that the Postgres round-vs-truncate claim is documented semantics rather than something this sandbox can live-verify against Postgres). Reviewer independently re-derived the rounding mechanism across a much wider parameter sweep and confirmed the audit's bound is conservative (real worst-case drift far smaller than the ≤£0.02 asserted), and confirmed the audit is genuinely systematic (it disproves rather than rubber-stamps the delegation's own starting hypothesis). Product Owner: acceptance still pending (this delegation record does not itself constitute Product Owner sign-off — see EPIC-04 PR for that gate).
