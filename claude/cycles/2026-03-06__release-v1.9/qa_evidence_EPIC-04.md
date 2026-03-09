# QA Evidence Log — EPIC-04 Risk Dashboard Fixes

**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active — ST-07 signed off; ST-08, ST-09, ST-10 pending delivery
**Last Updated:** 2026-03-09

---

**EPIC:** EPIC-04 — Risk Dashboard: Deviations & Fixes
**Cycle:** 2026-03-06__release-v1.9
**Sprint goal:** Fully resolve all Risk Dashboard deviations from v1.8.
**Branch:** exec/2026-03-06__release-v1.9/EPIC-04

---

## ST Item Evidence

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-07 | `risk_dashboard.md §6.2`; `portfolio_endpoints.md` | `backend/services/portfolio_service.py`: added GBP conversion block (lines 135–142) for `entry_price` and `current_stop` for US positions using `stored_fx_rate`. UK positions unchanged. 5 new golden output vectors (FX-01–FX-05). | entry_price in GBP for US positions; current_stop in GBP for US positions; UK positions unaffected; golden output CI passes; no regressions | **Pass** | See QA-OBS-ST07-01 (observation only — no block) |
| ST-08 | `risk_dashboard.md §3.4, §4.3, §5.5, §6.5, §7.6` | Pending delegated frontend delivery | All 5 components render independent error states; SC-RD-02 and SC-RD-03 pass | Pending | — |
| ST-09 | `risk_dashboard.md §5.2, §6.2, §6.4, §7.5` | Pending delegated frontend delivery | Sort ascending, Stop Price column, Days in Grace column, threshold label badge; SC-RD-04/05/07/08 pass | Pending | — |
| ST-10 | `risk_dashboard.md §3.2, §6.3` | Pending delegated frontend delivery | GRACE badge blue; GBP value at risk shown; SC-RD-05/06 pass | Pending | — |

---

## ST-07 Detailed Review — 2026-03-09

**Reviewer:** Director of Quality
**Commit reviewed:** `b31536f` — `[EPIC-04][ST-07] Convert entry_price and current_stop to GBP for US positions`
**Branch:** `exec/2026-03-06__release-v1.9/EPIC-04`

### Code Review

**File:** `backend/services/portfolio_service.py`

Reviewed change block (lines 135–142 on branch):

```python
# Convert entry_price and current_stop to GBP for display
# Spec: risk_dashboard.md §6.2 — all price columns in GBP
if market == 'US':
    entry_price_gbp = round(entry_price / stored_fx_rate, 2)
    current_stop_gbp = round(pos.get("current_stop", 0) / stored_fx_rate, 2)
else:
    entry_price_gbp = round(entry_price, 2)
    current_stop_gbp = round(pos.get("current_stop", 0), 2)
```

| Check | Finding | Result |
|-------|---------|--------|
| US `entry_price` → GBP | Divides by `stored_fx_rate` (`pos.get('fx_rate', 1.27)`) — same rate used for position risk calculation (line 158). Consistent. | ✓ |
| US `current_stop` → GBP | Same pattern — divides by `stored_fx_rate`. Correct. | ✓ |
| UK positions — no conversion | `else` branch returns native value as-is. UK prices already in GBP. | ✓ |
| P&L calculation unaffected | `pnl_native` (line 126) uses `entry_price` (native). `pnl_gbp` uses `live_fx_rate` (line 129). Conversion block runs after P&L — no side-effect. | ✓ |
| Position risk calculation unaffected | `risk_native` (line 166) uses `entry_price` (native). FX conversion in position risk block uses `stored_fx_rate`. Unchanged. | ✓ |
| Rounding | Both `entry_price_gbp` and `current_stop_gbp` are pre-rounded to 2dp before being placed in `positions_list`. Matches §6.2 "2 decimal places". | ✓ |
| `positions_list` lines 185, 191 | `"entry_price": entry_price_gbp` and `"current_stop": current_stop_gbp` — correctly reference the GBP-converted values. | ✓ |

### Spec Compliance Check

| Spec requirement | Implementation | Result |
|-----------------|----------------|--------|
| §6.2: Entry Price — "GBP, 2 decimal places" | `entry_price_gbp = round(entry_price / stored_fx_rate, 2)` for US | ✓ |
| §6.2: Stop Price — "GBP, 2 decimal places" | `current_stop_gbp = round(current_stop / stored_fx_rate, 2)` for US | ✓ |
| §11 DEV-ST03-11: US entry_price in USD — resolved | Entry price now GBP-converted for US positions | ✓ Resolved |
| §11 DEV-ST03-12: current_stop in USD — resolved | current_stop now GBP-converted for US positions | ✓ Resolved |

### Golden Output CI Review

| Check | Result |
|-------|--------|
| Golden Output Regression Gate | **Pass** — run 22845931436, 28s, success |
| New vectors FX-01 to FX-05 in `golden_outputs.json` | Present and correct (US at fx_rate 1.25 and 1.27; UK no-conversion) |
| All 23 tests pass (18 pre-existing + 5 new) | Confirmed — 0 regressions |
| Governance Sync failure | Pre-existing known issue (token lacks `issues:write`) — unrelated to ST-07 |

### Observation Filed

**QA-OBS-ST07-01** (non-blocking): `current_price` uses `live_fx_rate` (line 116) while `entry_price_gbp` and `current_stop_gbp` use `stored_fx_rate` (line 138). These two rates may differ, producing a minor basis discrepancy in the Stop Distance % when derived on the frontend as `(current_stop − current_price) / current_price × 100`. Spec §6.2 describes Stop Distance as "purely presentational display arithmetic on backend-provided values", and all three fields are in GBP — the discrepancy is second-order (typically < 1% of the percentage). This is a pre-existing design pattern (matching position risk, which also uses `stored_fx_rate`). No action required for ST-07 sign-off. Logged as a future refinement consideration.

### Acceptance Criteria Checklist

- [x] `entry_price` returned in GBP for US positions — verified in code and spec
- [x] `current_stop` returned in GBP for US positions — verified in code and spec
- [x] UK positions unaffected (no conversion applied) — verified
- [x] All P&L and position risk calculations continue to use native currency — verified (no regression)
- [x] Golden output CI passes — run 22845931436 (success)
- [x] 5 new spec-derived golden vectors (FX-01–FX-05) present and correctly exercised
- [x] No regressions on existing 18 golden output tests — confirmed
- [x] Commit `[EPIC-04][ST-07]` pushed to `exec/2026-03-06__release-v1.9/EPIC-04` — b31536f

**Result: PASS**

- Signed off by: Director of Quality
- Date: 2026-03-09
- Comments: DEV-ST03-11 and DEV-ST03-12 are resolved. Implementation is spec-compliant and internally consistent. QA-OBS-ST07-01 filed as a non-blocking observation. ST-07 is accepted.

---

## QA Test Coverage (EPIC-04 overall)

- Test scenarios in scope: `docs/testing/risk_dashboard_scenarios.md`
- ST-07 relevant scenarios: SC-RD-14 (US position entry price display), SC-RD-27 (stop price currency). These require live frontend testing — covered by ST-11 (canonical test library delivery).
- ST-07 backend gate: golden output regression (pure-math, CI-verified)
- ST-08, ST-09, ST-10: pending delivery — QA review will follow each commit
