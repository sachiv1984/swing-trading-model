**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-04-06
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `backend/routers/analytics.py` — `stop_price` JOIN via `positions.initial_stop` (ST-03, 2026-03-31__release-v2.4 — pre-met)
**Sprint:** 2026-04-05__release-v2.5 — ST-13 (closes TEST-GAP-EPIC-01-v24)

---

# Acceptance Test Scenarios — Stop Price on Analytics Endpoint

---

## 1. Scope

These scenarios verify that the analytics endpoint returns `stop_price` for closed trades where `positions.initial_stop` is populated and `initial_stop < entry_price`. This was verified as pre-met in v2.4 EPIC-01 ST-03 but had no regression scenario authored. This file provides that coverage.

Spec reference: `backend/routers/analytics.py` — `_fetch_trades_for_charts_with_stop()` function; LEFT JOIN on `trade_history.position_id` to `positions.initial_stop`.

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| stop_price derivation | `backend/routers/analytics.py` — `_fetch_trades_for_charts_with_stop()` |
| SQL logic | Lines 64–68 / 89–93: `CASE WHEN p.initial_stop IS NOT NULL AND p.initial_stop < th.entry_price THEN p.initial_stop END AS stop_price` |
| Fallback behaviour | Line 128–133: if JOIN fails (no `position_id` column), returns `stop_price: null` for all trades gracefully |

---

## 3. Prerequisites

- Staging database with at least one closed trade linked to a position via `trade_history.position_id`
- The associated position has `positions.initial_stop` populated (non-null) and `initial_stop < entry_price`
- Migration `migration_add_position_id.sql` applied (required for the JOIN to function)

---

## 4. Test Scenarios

### SC-STOP-01 — stop_price present on analytics response for trades with known initial_stop

**Category:** Correctness
**Priority:** P1

**Setup:**
- Trade in `trade_history` linked to a position via `position_id`
- `positions.initial_stop` = `<some value less than entry_price>` (e.g. entry = 100.00, initial_stop = 92.00)

**Test action:**
- Call `GET /analytics/cohort?period=month` (or equivalent endpoint that returns trades for charts)
- Locate the trade in the response

**Expected result:**
- The trade object contains `"stop_price": 92.0` (matching `initial_stop`)
- `stop_price` is a float, not null
- R-multiple calculations for that trade use the correct stop (not null)

**Failure conditions:**
- `stop_price` is `null` for a trade with a known `initial_stop`
- `stop_price` is present but incorrect (e.g. does not match `initial_stop`)
- Response 500 error (JOIN failure not handled gracefully)

**Fallback regression check:**
- If `position_id` column is absent (migration not applied): `stop_price` must be `null` for all trades and the endpoint must return 200 (no crash). Log should contain the migration advisory message.

---

## 5. Known Deviations

None.
