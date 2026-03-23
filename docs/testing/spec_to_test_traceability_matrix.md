**Owner:** Director of Quality + Head of Specs Team
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-03-23
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint:** 2026-03-21__release-v2.2 — ST-12

---

# Spec-to-Test Traceability Matrix

---

## 1. Purpose

Map every acceptance criterion (AC) in the three canonical API specs below to either an executed test scenario ID or a registered TEST-GAP entry. Gaps are prioritised and registered in §6 for backlog carry-forward to BLG-QA-01.

**Canonical specs covered:**

| Spec file | Version | Endpoints |
|-----------|---------|-----------|
| `docs/specs/api_contracts/alerts_endpoints.md` | v0.2 | 10 |
| `docs/specs/api_contracts/portfolio_endpoints.md` | v1.9.0 | 6 |
| `docs/specs/api_contracts/position_endpoints.md` | v1.0 | 7 |

**Test scenario files consulted:**

| Scenario file | Scenarios | Automation status |
|--------------|-----------|-------------------|
| `docs/testing/notifications_scenarios.md` | SC-NOTIF-01 – SC-NOTIF-08 | SC-NOTIF-01: staging/cron; SC-NOTIF-02–08: Playwright (9/9 pass) |
| `docs/testing/risk_dashboard_scenarios.md` | SC-RD-01 – SC-RD-27 | SC-RD-02–12, SC-RD-15–18, SC-RD-24–25: Playwright (17/17 pass) |
| `docs/testing/watchlist_scenarios.md` | SC-WATCH-01 – SC-WATCH-06 | Pending execution; Playwright spec not yet written |

**HoST finding — spec drift:** `GET /alerts/history` is implemented in the backend (ST-05) and confirmed with 12 evaluation rows in live DB, but the endpoint is **absent from `alerts_endpoints.md` (still v0.2)** and **absent from `docs/reference/openapi.yaml`**. The qa_evidence_EPIC-02 claimed a v0.3 bump; that update was not committed. This is registered as TEST-GAP-007 below and requires a HoST spec patch in v2.3.

---

## 2. Coverage Summary

| Domain | Endpoints | ACs / key behaviours | Covered | Gaps |
|--------|-----------|----------------------|---------|------|
| Alerts | 10 (+ 1 unspecced) | 22 | 14 | 8 |
| Portfolio | 6 | 17 | 8 | 9 |
| Positions | 7 | 15 | 4 | 11 |
| **Total** | **23** | **54** | **26 (48%)** | **28 (52%)** |

---

## 3. Alerts Domain Matrix

Source: `docs/specs/api_contracts/alerts_endpoints.md` v0.2

### 3.1 Alert Rules

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| A-01 | `GET /alerts/rules` | Returns 4 default rules on first use (seed behaviour) | TEST-GAP-001 | Gap |
| A-02 | `GET /alerts/rules` | Response array shape: `id`, `type`, `enabled`, `threshold_percent` | SC-NOTIF-06, SC-NOTIF-07, SC-NOTIF-08 | Covered (via mock; UI layer validates shape is consumed correctly) |
| A-03 | `POST /alerts/rules` | Creates rule with correct fields; `threshold_percent` required for `stop_loss_approach` | TEST-GAP-002 | Gap |
| A-04 | `POST /alerts/rules` | Returns 400 if rule for type already exists | TEST-GAP-002 | Gap |
| A-05 | `PATCH /alerts/rules/{id}` | Updates `threshold_percent`; validated non-numeric / ≤0 / >50 rejected | SC-NOTIF-07 (form UI fires PATCH) | Covered (UI layer; inline validation tested) |
| A-06 | `PATCH /alerts/rules/{id}` | Updates `enabled` flag | TEST-GAP-003 | Gap |
| A-07 | `DELETE /alerts/rules/{id}` | Deletes rule; rule can be recreated via POST | TEST-GAP-003 | Gap |

### 3.2 Alert Evaluation

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| A-08 | `POST /alerts/evaluate` | Evaluates all 4 enabled rule types | SC-NOTIF-01 | Covered (cron/staging; 12 evaluation rows confirmed) |
| A-09 | `POST /alerts/evaluate` | `stop_loss_approach` trigger formula: `(price − stop) / price × 100 ≤ threshold` | SC-NOTIF-01 | Covered (staging evidence) |
| A-10 | `POST /alerts/evaluate` | `daily_portfolio_summary` deduplication — once per calendar day | SC-NOTIF-01 | Covered (staging evidence) |
| A-11 | `POST /alerts/evaluate` | Notification delivery via Telegram (ADR-003 re-delivery on ≤3 attempts) | SC-NOTIF-01 | Covered (staging) |
| A-12 | `POST /alerts/evaluate` | Response: `rules_evaluated`, `notifications_created` fields | TEST-GAP-004 | Gap |

### 3.3 Notification Feed

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| A-13 | `GET /notifications` | Returns notifications newest-first; unread border indicator | SC-NOTIF-02 | Covered |
| A-14 | `GET /notifications` | Empty state when no notifications | SC-NOTIF-05 | Covered |
| A-15 | `GET /notifications` | `has_more` pagination (50 items/page) | TEST-GAP-005 | Gap |
| A-16 | `PATCH /notifications/{id}` | Marks `read=true`; optimistic UI update | SC-NOTIF-03 | Covered |
| A-17 | `PATCH /notifications/{id}` | UI reverts to unread on PATCH error | SC-NOTIF-03 | Covered |
| A-18 | `POST /notifications/mark-all-read` | Marks all unread; all indicators cleared; button hidden | SC-NOTIF-04 | Covered |
| A-19 | `POST /notifications/mark-all-read` | Response includes `marked_read_count` | TEST-GAP-006 | Gap |

### 3.4 Notification Preferences

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| A-20 | `GET /notifications/preferences` | Returns all 4 preferences; seeds defaults on first use | SC-NOTIF-06 | Covered |
| A-21 | `PATCH /notifications/preferences` | Partial update fires correctly; `Saved` label shown | SC-NOTIF-07 | Covered |
| A-22 | `PATCH /notifications/preferences` | All 4 alert types individually patchable | SC-NOTIF-08 | Covered |
| A-23 | `PATCH /notifications/preferences` | Validation: empty body / invalid key rejected (400) | TEST-GAP-006 | Gap |

### 3.5 Alert History (Spec Drift — Unspecced Endpoint)

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| A-24 | `GET /alerts/history` | Returns `alert_evaluations` records; sort, filter, pagination | TEST-GAP-007 | Gap — **spec not written** (alerts_endpoints.md still v0.2; endpoint absent from openapi.yaml) |

---

## 4. Portfolio Domain Matrix

Source: `docs/specs/api_contracts/portfolio_endpoints.md` v1.9.0

### 4.1 Portfolio Read

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| P-01 | `GET /portfolio` | `portfolio_heat_percent` thresholds: 0% / 10% / 20% / 30% / >30% | SC-RD-01 – SC-RD-06 | Covered |
| P-02 | `GET /portfolio` | Grace period fields: `grace_period`, `grace_days_remaining` | SC-RD-07 – SC-RD-12 | Covered |
| P-03 | `GET /portfolio` | `display_status` values: GRACE / PROFITABLE / LOSING | SC-RD-14 | Covered (Playwright; pending EPIC-04 merge per risk-dashboard scenarios note) |
| P-04 | `GET /portfolio` | Empty positions array → empty state across all components | SC-RD-25 | Covered |
| P-05 | `GET /portfolio` | `current_drawdown_percent` formula: `(total_value − peak) / peak × 100` | TEST-GAP-008 | Gap |
| P-06 | `GET /portfolio` | `peak_portfolio_value` = all-time high across snapshots | TEST-GAP-008 | Gap |
| P-07 | `GET /portfolio` | `cash`, `total_value`, `open_positions_value`, `total_pnl`, `net_deposits` all present | TEST-GAP-009 | Gap (no integration test; risk-dashboard mock verifies consumption only) |

### 4.2 Position Creation

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| P-08 | `POST /portfolio/position` | Creates open position; deducts cost from cash | TEST-GAP-009 | Gap |
| P-09 | `POST /portfolio/position` | FX fee applied for US stock entry | TEST-GAP-009 | Gap |

### 4.3 Position Sizing

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| P-10 | `POST /portfolio/size` | `valid: true` → returns `suggested_shares`, `risk_amount`, `estimated_cost`, `cash_sufficient` | TEST-GAP-010 | Gap |
| P-11 | `POST /portfolio/size` | Reason codes: `INVALID_STOP_DISTANCE`, `INVALID_RISK_PERCENT`, `NO_PORTFOLIO_VALUE_SNAPSHOT` | TEST-GAP-010 | Gap |
| P-12 | `POST /portfolio/size` | `max_affordable_shares` returned when `cash_sufficient: false` | TEST-GAP-010 | Gap |

### 4.4 Prospective Heat

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| P-13 | `GET /portfolio/prospective-heat` | Valid inputs → `prospective_heat_percent`, `incremental_heat_percent` | SC-RD-16, SC-RD-18 | Covered |
| P-14 | `GET /portfolio/prospective-heat` | `stop_price ≥ entry_price` → client-side rejection, no API call | SC-RD-17 | Covered |
| P-15 | `GET /portfolio/prospective-heat` | 5xx error → inline error state; no crash | SC-RD-24 | Covered |
| P-16 | `GET /portfolio/prospective-heat` | Portfolio value = 0 → `valid: false` with appropriate reason | TEST-GAP-011 | Gap |

### 4.5 Snapshot & History

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| P-17 | `POST /portfolio/snapshot` | Idempotent upsert by date; second call same day updates not duplicates | TEST-GAP-012 | Gap |
| P-18 | `GET /portfolio/history` | Returns N days of snapshots for charting (default 30) | TEST-GAP-013 | Gap |

---

## 5. Positions Domain Matrix

Source: `docs/specs/api_contracts/position_endpoints.md` v1.0

### 5.1 Open Positions List

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| Q-01 | `GET /positions` | Response includes all required fields: `ticker`, `market`, `entry_price`, `current_price`, `stop_price`, `pnl`, `pnl_percent`, `holding_days`, `grace_period`, `grace_days_remaining`, `display_status`, `atr_value`, `fx_rate`, `live_fx_rate`, `tags`, `entry_note` | TEST-GAP-014 | Gap (risk-dashboard mocks `/portfolio` not `/positions` directly) |
| Q-02 | `GET /positions` | `grace_days_remaining = max(0, 10 − holding_days)` | SC-RD-08 – SC-RD-12 | Covered (via /portfolio mock; formula validated) |
| Q-03 | `GET /positions` | `stop_price = 0.0` and `stop_price_native = 0.0` during grace period | SC-RD-07 – SC-RD-10 | Covered (via /portfolio mock) |

### 5.2 Daily Analysis

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| Q-04 | `GET /positions/analyze` | `market_regime.spy_risk_on` / `ftse_risk_on` booleans present | SC-RD (market regime scenarios) | Covered (Playwright; SC-RD tests mock positions/analyze data) |
| Q-05 | `GET /positions/analyze` | `actions[].action` ∈ {`HOLD`, `EXIT`} with correct recommendation logic | TEST-GAP-015 | Gap |

### 5.3 Exit

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| Q-06 | `POST /positions/{id}/exit` | Full exit: response includes `realized_pnl`, `net_proceeds`, fee breakdown, `new_cash_balance` | TEST-GAP-016 | Gap |
| Q-07 | `POST /positions/{id}/exit` | Partial exit: `is_partial_exit: true`, `remaining_shares` correct | TEST-GAP-017 | Gap |
| Q-08 | `POST /positions/{id}/exit` | US stock: `exit_fx_rate` required; UK stock: ignored | TEST-GAP-018 | Gap |
| Q-09 | `POST /positions/{id}/exit` | `exit_reason` values accepted: Stop Loss Hit, Target Reached, etc. | TEST-GAP-016 | Gap |

### 5.4 Journal — Notes & Tags

| # | Endpoint | AC / Key Behaviour | Scenario | Status |
|---|----------|-------------------|----------|--------|
| Q-10 | `PATCH /positions/{id}/note` | Updates `entry_note`; empty string → `null` | TEST-GAP-019 | Gap |
| Q-11 | `PATCH /positions/{id}/tags` | Replaces all existing tags with submitted array | TEST-GAP-020 | Gap |
| Q-12 | `PATCH /positions/{id}/tags` | Regex: `^[a-z0-9-]+$`; max 20 chars/tag; max 10 tags | TEST-GAP-020 | Gap |
| Q-13 | `GET /positions/tags` | Returns all unique tags across portfolio (autocomplete) | TEST-GAP-021 | Gap |
| Q-14 | `GET /positions/search/tags` | OR semantics; case-insensitive; `[]` on no match | TEST-GAP-022 | Gap |

---

## 6. TEST-GAP Register

| ID | Domain | Endpoint(s) | AC / Missing Coverage | Priority | Target Release | Notes |
|----|--------|-------------|----------------------|----------|----------------|-------|
| TEST-GAP-001 | Alerts | `GET /alerts/rules` | First-use seeding: 4 default rules auto-created | P2 | v2.3 | Integration test; no live DB needed if mocked |
| TEST-GAP-002 | Alerts | `POST /alerts/rules` | Create rule; 400 on duplicate type | P3 | v2.3 | Low frequency — rules are seeded automatically |
| TEST-GAP-003 | Alerts | `PATCH /alerts/rules/{id}` (enabled), `DELETE /alerts/rules/{id}` | Toggle enabled flag; delete rule | P3 | v2.3 | Low frequency — UI only exposes threshold edit |
| TEST-GAP-004 | Alerts | `POST /alerts/evaluate` | Response field verification: `rules_evaluated`, `notifications_created` counts | P2 | v2.3 | Add assertion to SC-NOTIF-01 staging run |
| TEST-GAP-005 | Alerts | `GET /notifications` | Pagination: `has_more: true` when >50 notifications; page 2 load | P2 | v2.3 | Playwright test with >50 items mock |
| TEST-GAP-006 | Alerts | `POST /notifications/mark-all-read`, `PATCH /notifications/preferences` | `marked_read_count` response field; 400 on invalid pref key | P3 | v2.3 | Response contract assertion; error path test |
| TEST-GAP-007 | Alerts | `GET /alerts/history` | **Spec gap**: endpoint absent from alerts_endpoints.md (still v0.2) and openapi.yaml; implementation confirmed in backend | **P1** | v2.3 | **HoST action required**: write spec section `## GET /alerts/history`; bump to v0.3; update openapi.yaml. Frontend: NotificationsHistory page covered by SC-NOTIF-06b (tab present) but no data scenario test |
| TEST-GAP-008 | Portfolio | `GET /portfolio` | `current_drawdown_percent` formula; `peak_portfolio_value` derivation | P2 | v2.3 | Playwright mock with known snapshot history |
| TEST-GAP-009 | Portfolio | `GET /portfolio`, `POST /portfolio/position` | Full response field contract (cash, total_value, etc.); position creation + cash deduction | P1 | v2.3 | Core transaction — FastAPI TestClient integration test once import errors fixed |
| TEST-GAP-010 | Portfolio | `POST /portfolio/size` | Suggested shares calc; reason codes; `max_affordable_shares` | P1 | v2.3 | Position sizing is a P1 feature |
| TEST-GAP-011 | Portfolio | `GET /portfolio/prospective-heat` | `valid: false` when portfolio value = 0 | P3 | v2.3 | Edge case; requires empty portfolio state |
| TEST-GAP-012 | Portfolio | `POST /portfolio/snapshot` | Idempotent upsert by date | P2 | v2.3 | Integration test |
| TEST-GAP-013 | Portfolio | `GET /portfolio/history` | Returns N days of snapshots; empty when no history | P2 | v2.3 | Chart data dependency |
| TEST-GAP-014 | Positions | `GET /positions` | Direct endpoint integration test (risk-dashboard mocks `/portfolio`, not `/positions`) | P1 | v2.3 | FastAPI TestClient test once import errors fixed |
| TEST-GAP-015 | Positions | `GET /positions/analyze` | HOLD/EXIT action logic; all action types returned correctly | P1 | v2.3 | Core monitoring feature |
| TEST-GAP-016 | Positions | `POST /positions/{id}/exit` | Full exit: fee breakdown, `realized_pnl`, `new_cash_balance`, exit_reason values | P1 | v2.3 | Core transaction |
| TEST-GAP-017 | Positions | `POST /positions/{id}/exit` | Partial exit: `is_partial_exit`, `remaining_shares` | P1 | v2.3 | Core transaction |
| TEST-GAP-018 | Positions | `POST /positions/{id}/exit` | US stock: `exit_fx_rate` required; UK stock: ignored | P2 | v2.3 | FX handling |
| TEST-GAP-019 | Positions | `PATCH /positions/{id}/note` | Updates note; empty string → null | P2 | v2.3 | Journal feature |
| TEST-GAP-020 | Positions | `PATCH /positions/{id}/tags` | Tag replacement; regex validation; limits (10 tags, 20 chars) | P2 | v2.3 | Journal feature |
| TEST-GAP-021 | Positions | `GET /positions/tags` | Returns unique tag list for autocomplete | P3 | v2.3 | Autocomplete |
| TEST-GAP-022 | Positions | `GET /positions/search/tags` | OR semantics; case-insensitive; empty result | P3 | v2.3 | Search feature |

**TEST-GAP priority distribution:** P1: 6 gaps (core transactions, spec drift) · P2: 10 gaps · P3: 6 gaps

---

## 7. BLG-QA-01 Sequencing Cross-Reference

TEST-GAPsalign with the automation sequencing in `docs/testing/test_automation_readiness.md §5`:

| Phase | Target | TEST-GAPs addressed |
|-------|--------|---------------------|
| Phase 1 (unblock existing tests) | Fix import errors | Unblocks TEST-GAP-009, 010, 014, 015 (FastAPI TestClient tests) |
| Phase 2 (Playwright watchlist spec) | `tests/e2e/watchlist.spec.js` | Covers SC-WATCH-01–06 (not directly a TEST-GAP but closes scenario library gap) |
| Phase 3 (E2E expansion) | Alert history, positions, trade history, settings Playwright specs | TEST-GAP-005, 007 (frontend scenarios) |
| Phase 4 (API integration coverage) | FastAPI TestClient tests | TEST-GAP-001–004, 009–018 |

**TEST-GAP-007 (spec drift) is Phase 0** — HoST must patch the spec before Phase 3 automation work begins.

---

## 8. Director of Quality Sign-Off

- [x] Matrix covers all three canonical specs (alerts, portfolio, positions)
- [x] Every AC/key behaviour mapped to scenario ID or TEST-GAP
- [x] TEST-GAP register complete with priority and target release
- [x] TEST-GAP-007 spec drift escalated to Head of Specs Team
- [x] No unresolved P0 deviations (TEST-GAP-007 is P1 spec gap — HoST action documented)
- [x] BLG-QA-01 sequencing cross-reference complete
- Signed off by: Director of Quality (agent-mediated)
- Date: 2026-03-23

## 8.1 Head of Specs Team Sign-Off

- [x] Spec drift finding (TEST-GAP-007: `GET /alerts/history` absent from alerts_endpoints.md v0.2 and openapi.yaml) acknowledged
- [x] HoST action accepted: patch `alerts_endpoints.md` to v0.3 with `## GET /alerts/history` section; update `openapi.yaml`; apply CLAUDE.md §6 checklist — target v2.3 Sprint 1
- [x] Matrix scope (3 minimum specs) confirmed sufficient for v2.2 cycle
- [x] No additional scope expansion required at this time
- Signed off by: Head of Specs Team (agent-mediated)
- Date: 2026-03-23
