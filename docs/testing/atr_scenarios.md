**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-04-06
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `backend/utils/pricing.py` — `calculate_atr()` v2.4 fix (ST-01, 2026-03-31__release-v2.4)
**Sprint:** 2026-04-05__release-v2.5 — ST-13 (closes TEST-GAP-EPIC-01-v24)

---

# Acceptance Test Scenarios — ATR Pence→GBP Conversion

---

## 1. Scope

These scenarios verify that ATR calculation for UK-listed tickers (`.L` suffix) correctly converts the Yahoo Finance raw value from pence to GBP (÷ 100). This was a correctness bug fixed in v2.4 EPIC-01 ST-01. Without the fix, UK stop-loss calculations were 100× too large, resulting in positions never being sized or immediately stopped out.

Spec reference: `backend/utils/pricing.py` — `calculate_atr()` function, `.L` suffix handling.

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| ATR calculation | `backend/utils/pricing.py` — `calculate_atr()` |
| .L ticker conversion | `backend/utils/pricing.py` line 315: `if ticker.endswith('.L'): atr = atr / 100` |
| Stop loss usage | `backend/services/sizing_service.py` — uses ATR for stop-loss distance |

---

## 3. Prerequisites

- Live or stubbed Yahoo Finance response for a .L ticker (e.g. `FRES.L`)
- Access to `calculate_atr()` either via unit test or via a staging endpoint that triggers ATR

---

## 4. Test Scenarios

### SC-ATR-01 — ATR converted from pence to GBP for .L tickers

**Category:** Correctness
**Priority:** P1

**Setup:**
- Ticker: any `.L` ticker (e.g. `FRES.L`)
- Yahoo Finance returns raw ATR values in pence (e.g. raw TR values summing to ~2,400 pence for the 14-day window)

**Test action:**
- Call `calculate_atr("FRES.L")` (or equivalent API path that internally calls this function)
- Capture the returned ATR value

**Expected result:**
- Returned ATR is in GBP (e.g. ~24.0, not ~2,400.0)
- The console log contains: `converted from pence`
- ATR value is consistent with typical UK stock price movements (1–5% of share price range)

**Failure conditions:**
- ATR returned is ~100× the expected value (pence not converted)
- Stop-loss suggested by the sizing service is unrealistically wide for the position size

**Regression:**
- This scenario confirms the v2.4 ST-01 fix holds. Any regression to `git log -1` behaviour prior to commit `9c8fa2d` would cause this to fail.

---

## 5. Known Deviations

None.
