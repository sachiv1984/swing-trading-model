**Owner:** Financial Reporting & Records Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-07-30
**Cycle:** 2026-07-30__release-v8.0
**Story:** ST-02 (EPIC-01)
**Backlog source:** BLG-SPEC-79

---

# FX Handling Review — post-DS-05 US Market Source Change

## Scope

`strategy_rules.md` §4.1.5 (Currency and FX handling, canonical) predates DS-05's switch to Alpaca Markets as the primary OHLCV/ATR data source for US tickers (v2.9, EPIC-02). Confirm whether that data-source change introduced, or could introduce, a silent position-sizing miscalculation for GBP-denominated accounts trading US tickers — i.e. whether the FX conversion path used in sizing/position-entry ever became coupled to the OHLCV data source that DS-05 changed.

## What DS-05 actually changed

DS-05 changed the routing for **price/ATR data only**:
- `backend/utils/pricing.py::get_current_price()` — US tickers try Alpaca Data API v2 first, Yahoo Finance fallback.
- `backend/utils/pricing.py::calculate_atr()` — same Alpaca-first / Yahoo-fallback routing for ATR.

Neither function has any role in currency conversion. Both return prices in the instrument's **native currency** (USD for US tickers) regardless of which upstream source served the request — the routing choice is invisible to every downstream caller.

## FX rate path — independent of DS-05

`backend/utils/pricing.py::get_live_fx_rate()` fetches the GBP/USD rate directly from Yahoo Finance (5-minute cache, falls back to a hardcoded default on failure). This function was not touched by DS-05 and has no dependency on `get_current_price()`/`calculate_atr()` or on which OHLCV provider served a given ticker's price/ATR. It is called independently, on its own path, wherever an FX conversion is needed:

- `backend/services/sizing_service.py::size_position()` (line ~127) — the Position Sizing Calculator (§4.1.7). `entry_price` and `stop_price` are caller-supplied form inputs, not fetched from Alpaca or Yahoo internally; `fx_rate_used` is computed from `get_live_fx_rate()` (or a user override) and is already returned in the response (`"fx_rate_used": round(fx_rate_used, 4)`), satisfying §4.1.5's auditability requirement as written.
- `backend/services/position_service.py::add_position()` (line ~766) — actual position entry. `entry_price` is the broker fill price passed by the caller; `fx_rate_to_use` again comes from `get_live_fx_rate()` (or a user-provided override), independently of whichever OHLCV source was used earlier in the workflow to display live prices/ATR to the user.

In both call sites, the value ultimately converted (entry/stop price) is a user- or broker-supplied number, not a value read back from Alpaca or Yahoo's OHLCV bars — so there is no path by which an Alpaca-vs-Yahoo pricing difference (e.g. split-adjustment convention, timestamp/close-price definition) could silently propagate into the FX-converted GBP figures. The FX rate itself is single-sourced (Yahoo Finance GBP/USD) regardless of which provider served the OHLCV/ATR data for that ticker.

## Determination

**No silent position-sizing miscalculation risk found.** DS-05's OHLCV/ATR routing change and the FX conversion path are, and always were, fully decoupled — they do not share a data source, and the values FX-converted originate from user/broker input, not from the OHLCV pipeline. `strategy_rules.md` §4.1.5 is confirmed accurate as currently written; **no amendment filed.**

No P1/P2 backlog item filed — the audit found the two paths already independent by construction; no code change was required.

## Sign-Off

**Signed off by:** Financial Reporting & Records Owner (agent-mediated, §5.3)
**Date:** 2026-07-30
**Determination:** Review complete — no gap found; `strategy_rules.md` §4.1.5 confirmed accurate, no amendment required.
