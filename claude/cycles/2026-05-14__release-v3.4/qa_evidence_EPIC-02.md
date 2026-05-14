**Owner:** Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Active
**Cycle:** 2026-05-14__release-v3.4
**EPIC:** EPIC-02 — Arc 3 Risk Prompts: Drawdown Review & Concentration Limits
**Branch:** exec/2026-05-14__release-v3.4/EPIC-02

---

# QA Evidence — EPIC-02

---

## ST-04 — Drawdown-Triggered Review Prompt backend (IT-04)

**Delegation class:** autonomous (backend)
**Commit:** 25a316a0
**GitHub issue:** 374

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | `GET /portfolio/drawdown-status` returns current_drawdown_pct, threshold_pct, threshold_breached | Code review — `portfolio_risk.py` GET /portfolio/drawdown-status endpoint | Pass |
| AC-02 | Drawdown % = (30d_peak − current_value) / 30d_peak × 100; peak = MAX(total_value) last 30 days | Code review — `_get_30d_peak()` uses `get_portfolio_snapshots(portfolio_id, days=30)`; formula in `get_drawdown_status()` | Pass |
| AC-03 | Threshold configurable via settings (default 10%, range 5–50%) | Code review — `_get_settings_value("drawdown_threshold_pct", 10.0)` | Pass |
| AC-04 | When breached: also returns lifecycle state counts, portfolio heat %, regime status | Code review — `threshold_breached` guard block returns `positions_by_state`, `portfolio_heat_pct`, `regime_status` | Pass |
| AC-05 | Endpoint registered in `backend/routers/test.py`; SystemStatus.js fallback updated | Code review — test.py entry added (count 53→55); SystemStatus.js fallback '49'→'55' | Pass |
| AC-06 | Endpoint added to `docs/reference/openapi.yaml` in same commit | Code review — openapi.yaml `/portfolio/drawdown-status` path added in commit 25a316a0 | Pass |

**Deviations:** None

---

## ST-05 — Drawdown-Triggered Review Prompt frontend (IT-04)

**Delegation class:** autonomous (frontend, engine delivery)
**Commit:** a704ddbf
**GitHub issue:** 375

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | Review prompt visible when `GET /portfolio/drawdown-status` returns `threshold_breached: true` | Playwright SC-DD-02 — "Portfolio Drawdown Review" visible | Pass |
| AC-02 | Prompt displays: current drawdown %, breach threshold %, positions by state, portfolio heat %, regime | Playwright SC-DD-03 — 12.4%, 6.3%, "Bearish" visible; SC-DD-04 — state chips visible | Pass |
| AC-03 | §13 compliance: prompt is display-only — no automated position changes | Code review — `role="alert"`, no mutations; Dismiss only | Pass |
| AC-04 | Dismissal persists until next page load (session-scoped in-memory state) | Playwright SC-DD-05 — click dismiss, prompt not visible; code review — `useState(false)` for dismissed | Pass |
| AC-05 | No prompt when `threshold_breached: false` | Playwright SC-DD-01 — no prompt rendered | Pass |
| AC-06 | Playwright E2E test coverage recorded before PR merge | tests/e2e/epic02-v34-risk-prompts.spec.js — 5 DD scenarios, all pass | Pass |

**Deviations:**
- DEV-01: Dismissal uses React `useState` (session-scoped in-memory). Spec says "not localStorage — server-side acknowledgement or session-scoped". In-memory state satisfies session-scoped per UX spec §6 rationale (server-side ack would require additional endpoint scope).

---

## ST-06 — Position Concentration Limits backend + frontend (IT-05)

**Delegation class:** autonomous (backend + frontend, engine delivery)
**Commits:** 25a316a0 (backend), a704ddbf (frontend)
**GitHub issue:** 376

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | Backend: `GET /portfolio/concentration-status` returns per-position heat %, sector concentration %, breaching items | Code review — `concentration_status()` endpoint in `portfolio_risk.py` | Pass |
| AC-02 | Single-position threshold default 15%, configurable; sector threshold default 30%, configurable | Code review — `_get_settings_value("concentration_position_threshold_pct", 15.0)` and `concentration_sector_threshold_pct` | Pass |
| AC-03 | Frontend: warning on positions page when any threshold breached; lists breaching positions/sectors | Playwright SC-CC-02, SC-CC-03, SC-CC-04 — warning card renders with NVDA, 22.1%, Technology, 41.2% | Pass |
| AC-04 | DS-03 sector data used where available; graceful degradation when absent | Code review — `sector = pos.get("sector")` guard; sector_risk dict only populated when sector is not None | Pass |
| AC-05 | Thresholds configurable via settings | Code review — settings lookup with defaults; validated range in settings table (not frontend validation) | Pass |
| AC-06 | Playwright E2E test coverage before PR merge | tests/e2e/epic02-v34-risk-prompts.spec.js — 5 CC scenarios, all pass | Pass |
| AC-07 | New endpoints registered in `backend/routers/test.py` and `openapi.yaml` | Code review — both endpoints in test.py and openapi.yaml (commit 25a316a0) | Pass |

**Deviations:** None

---

## Consolidation

| Story | Playwright | Code Review | Status |
|-------|-----------|-------------|--------|
| ST-04 | N/A (backend) | portfolio_risk.py router, openapi.yaml, test.py, SystemStatus.js | Pass |
| ST-05 | 5/5 scenarios pass | DrawdownReviewPrompt component, useState dismiss | Pass |
| ST-06 | 5/5 scenarios pass | ConcentrationLimitsWarning component, concentration_status() endpoint | Pass |

**DoQ Sign-off:** Director of Quality — 2026-05-14
**Test run date:** 2026-05-14 — all 10 Playwright scenarios pass
