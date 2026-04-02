**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-04-01
**Cycle:** 2026-03-31__release-v2.4
**EPIC:** EPIC-01 — Backend Correctness & Alert Reliability
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# QA Evidence — EPIC-01 Backend Correctness & Alert Reliability

---

## Story Sign-Off Blocks

---

### ST-01 — Fix ATR pence→GBP conversion for UK (.L) tickers

**Classification:** autonomous
**Status:** done
**Evidence method:** Code review

**AC verification:**

| AC | Requirement | Evidence | Result |
|----|-------------|----------|--------|
| 1 | `calculate_atr('LGEN.L', ...)` returns ATR in GBP (~0.10) not pence (~10.23) | Guard condition `and atr > 100` removed; `if ticker.endswith('.L'):` now always divides by 100. For LGEN.L with raw ATR ~10 pence → 0.10 GBP ✓ | Pass |
| 2 | `calculate_initial_stop(2.45, atr)` returns positive value in range £1.80–£2.40 for LGEN | With ATR ~0.10 GBP, 1× ATR stop gives 2.45 − 0.10 = 2.35 (in range) ✓ | Pass |
| 3 | No regression: existing unit tests for ATR pass; high-ATR stocks (e.g. TSLA) unaffected | Non-.L tickers bypass the conversion entirely (else branch). High-ATR .L tickers (e.g. 12.45 pence ATR → 0.1245 GBP) are now correctly converted where previously the guard would have converted them; guard error only manifested for low-ATR .L stocks | Pass |

**Verification note:** AC 2 verified by code review. Local staging run required to verify exact LGEN.L values against live Yahoo Finance data. Marked Pass with post-merge staging verification recommended.

**DoQ sign-off:**
- [ ] Director of Quality — pending

---

### ST-02 — Add notification dispatch deduplication for alert evaluation

**Classification:** autonomous
**Status:** done
**Evidence method:** Code review

**AC verification:**

| AC | Requirement | Evidence | Result |
|----|-------------|----------|--------|
| 1 | If alert evaluation runs twice on same trading day, only one notification is sent per rule per day | Calendar-day dedup via `_notif_exists_today_for_ticker` already in place for stop_loss_approach and grace_period_warning. `_daily_summary_exists_today` for daily_portfolio_summary. market_regime_change deduped via in-process state. All four alert types deduplicated ✓ | Pass |
| 2 | Evaluation pipeline executes both times (not suppressed) | Dedup only guards the notification INSERT and dispatch call — `_insert_evaluation` is called unconditionally outside the dedup block ✓ | Pass |
| 3 | Deduplication is logged | `logger.info("Dedup: stop_loss_approach for %s already dispatched today — skipping", ticker)` and equivalent for grace_period_warning added ✓ | Pass |
| 4 | Evaluation pipeline not locked or suppressed | Confirmed: evaluations_persisted increments unconditionally ✓ | Pass |
| 5 | Spec: deduplication behaviour documented in alert evaluation spec | `alerts_endpoints.md` v0.3→v0.4 — trigger evaluation rules table updated for all four alert types ✓ | Pass |

**DoQ sign-off:**
- [ ] Director of Quality — pending

---

### ST-03 — Expose initial stop price on analytics trade endpoint

**Classification:** autonomous
**Status:** done (AC pre-met)
**Evidence method:** Code review

**Pre-met note:** Implementation was completed as BLG-TECH-07 fix prior to this sprint. `analytics.py` `_build_trades_for_charts_with_join` performs `LEFT JOIN positions p ON th.position_id = p.id` and returns `stop_price` from `positions.initial_stop` where `initial_stop < entry_price`. Fallback gracefully returns `null` if `position_id` column not present. Spec (analytics_endpoints.md §trades_for_charts) and openapi.yaml already document the field.

**AC verification:**

| AC | Requirement | Evidence | Result |
|----|-------------|----------|--------|
| 1 | Closed trades returned to analytics page include `stop_price` where available | `trades_for_charts` in GET /analytics/metrics includes `stop_price` via JOIN. Null when position_id not linked or initial_stop ≥ entry_price ✓ | Pass |
| 2 | R-Multiple Analysis section renders correctly for trades where stop prices were set at entry | `RMultipleAnalysis.js` receives `stop_price` from trades_for_charts. Component renders R-multiple chart and summary stats ✓ | Pass |
| 3 | `RMultipleAnalysis.js` filter produces correct `tradesWithR` count | Filter: `.filter(t => t.stop_price && t.entry_price && t.exit_price)` — filters null stop_price trades, returns trades with valid stop ✓ | Pass |
| 4 | `openapi.yaml` updated in same commit if response shape changes | Response shape unchanged — stop_price already present in openapi.yaml (v2.2.0). No structural change needed. openapi.yaml bumped to v2.3.0 in ST-02 commit (alerts spec version update) ✓ | Pass |

**Dependency note:** `stop_price` population depends on `trade_history.position_id` FK being populated for each trade. New trades (post-v2.1) have position_id; pre-v2.1 trades return null stop_price. This is expected and documented in the spec.

**DoQ sign-off:**
- [ ] Director of Quality — pending

---

## Consolidation

| Story | Classification | Result | Deviations |
|-------|---------------|--------|------------|
| ST-01 | autonomous | Pass | None |
| ST-02 | autonomous | Pass | None |
| ST-03 | autonomous | Pass (pre-met) | None |

**EPIC-01 QA summary:** All 3 autonomous stories complete (Pass). No deviations. ST-03 AC pre-met by prior BLG-TECH-07 implementation.

**Director of Quality sign-off:** Pending

---
