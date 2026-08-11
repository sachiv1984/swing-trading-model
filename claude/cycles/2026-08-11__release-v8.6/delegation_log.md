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
- **Status:** Pending
