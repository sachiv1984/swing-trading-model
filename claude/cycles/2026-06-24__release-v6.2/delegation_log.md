Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-25

---

# Delegation Log — 2026-06-24__release-v6.2

This file is append-only. Do not edit previous entries.

---

## DEL-20260624-01

- **Story:** ST-01 — Nightly trailing stop computation — backend service (EPIC-01)
- **Delegation class:** delegated_backend
- **Assigned to:** Head of Engineering
- **Raised at:** 2026-06-24T15:00:00Z
- **GitHub issue:** #839
- **Branch:** exec/2026-06-24__release-v6.2/EPIC-01
- **Commit format required:** `[EPIC-01][ST-01] <description>`
- **Spec reference:** docs/specs/api_contracts/position_endpoints.md#GET /positions
- **Required layers:** service (nightly trailing stop computation logic), database (current_trailing_stop field storage)
- **Delegation context:**
  - Nightly job iterates all open positions, fetches current price + 14-day ATR, computes trailing stop using profit-lock logic
  - `INITIAL_ATR_MULT=5`, `PROFIT_ATR_MULT=2`, `ATR_PERIOD=14` — must match production_strategy.py exactly
  - Stop ratchet enforced: `UpdatedStop = max(CurrentStop, NewStop)`
  - New field `current_trailing_stop` added to `GET /positions` response; existing `initial_stop` unchanged
  - AC-04 (regression): manual position sizing path unchanged; only nightly computation affected
  - Unit tests: profit-lock branch, ratchet invariant, ATR-14 parameter validation; integration test: GET /positions schema
- **Unblock criteria:** Commit `[EPIC-01][ST-01]` pushed to exec/2026-06-24__release-v6.2/EPIC-01 with all 5 ACs implemented
- **Status:** Unblocked
- **commit_sha:** e49d5a8b1a5dd14247d28338ae19765c77cf33c3

---

## DEL-20260624-02

- **Story:** ST-02 — Trailing stop display and breach badge — frontend (EPIC-01)
- **Delegation class:** delegated_frontend
- **Assigned to:** Head of Engineering
- **Raised at:** 2026-06-24T15:00:00Z
- **GitHub issue:** #840
- **Branch:** exec/2026-06-24__release-v6.2/EPIC-01
- **Commit format required:** `[EPIC-01][ST-02] <description>`
- **Spec reference:** docs/specs/frontend/pages/positions.md (v1.8)
- **Design spec:** docs/design/2026-06-24__release-v6.2/trailing-stop-display/ux_spec.md
- **Dependency:** ST-01 must be done first (current_trailing_stop field required)
- **Delegation context — Base44 prompt draft:**
  1. **Context:** Portfolio positions table needs two new display elements: (a) `current_trailing_stop` column alongside `initial_stop`; (b) breach badge when `current_price ≤ current_trailing_stop`
  2. **Change required:** Display `current_trailing_stop` per-position in portfolio view; add breach badge when breach condition is true; badge must be visually distinct from other status indicators per UX spec (trailing-stop-display/ux_spec.md — orange #EA580C from v6.2 design gate)
  3. **API contract reference:** `GET /positions` response now includes `current_trailing_stop` field (added by ST-01)
  4. **Behaviour rules:** AC-01: trailing stop value visible; AC-02: badge present on breach; AC-03: badge visually distinct (staging sign-off); AC-04: no badge on non-breach; layout note: if >15 columns cause horizontal scroll, Initial Stop + Trail Stop may use two-line cell (implementation-level decision, no spec amendment needed)
  5. **Non-functional rules:** §13 compliant — display only, no signal/recommendation use
  6. **Expected outcome:** Playwright tests for AC-01, AC-02, AC-04; human staging sign-off for AC-03 (badge colour/icon distinctiveness)
- **Unblock criteria:** Commit `[EPIC-01][ST-02]` pushed; Playwright tests for AC-01/02/04 passing; AC-03 staging sign-off obtained
- **Status:** Unblocked
- **commit_sha:** e49d5a8b1a5dd14247d28338ae19765c77cf33c3

---

## DEL-20260624-03

- **Story:** ST-03 — Month-end rebalance exit signal generation (EPIC-01)
- **Delegation class:** delegated_backend
- **Assigned to:** Head of Engineering
- **Raised at:** 2026-06-24T15:00:00Z
- **GitHub issue:** #841
- **Branch:** exec/2026-06-24__release-v6.2/EPIC-01
- **Commit format required:** `[EPIC-01][ST-03] <description>`
- **Spec reference:** docs/specs/api_contracts/signal_endpoints.md#GET /signals
- **Design spec:** docs/design/2026-06-24__release-v6.2/rebalance-exit-signal-style/ux_spec.md
- **Delegation context:**
  - On last trading day of each calendar month: compute which open positions are NOT in current top-5 momentum signal list
  - Generate signal record with `status = exit_rebalance` for each such position
  - Last-trading-day detection must handle weekends and holidays
  - No duplicate `exit_rebalance` signal if position is also crossing a stop (deduplication required)
  - `exit_rebalance` signals returned by `GET /signals`; UI label "Rebalance Exit" teal #0891B2 per v6.2 design gate
  - Pre-check: confirm `stop_exit` is a live API value in GET /signals before applying red badge styling — if not live, defer that badge variant
- **Unblock criteria:** Commit `[EPIC-01][ST-03]` pushed with all 5 ACs implemented
- **Status:** Unblocked
- **commit_sha:** e49d5a8b1a5dd14247d28338ae19765c77cf33c3

---

## DEL-20260624-04

- **Story:** ST-04 — Inverse-volatility position sizing for signal-driven entries (EPIC-01)
- **Delegation class:** delegated_backend
- **Assigned to:** Head of Engineering
- **Raised at:** 2026-06-24T15:00:00Z
- **GitHub issue:** #842
- **Branch:** exec/2026-06-24__release-v6.2/EPIC-01
- **Commit format required:** `[EPIC-01][ST-04] <description>`
- **Spec reference:** docs/specs/api_contracts/signal_endpoints.md#POST /signals/generate
- **Delegation context:**
  - Replace fixed-risk £200 sizing model with inverse-volatility weighting for signal entries
  - Weight formula: `weight_i = (1/ATR_i) / Σ(1/ATR_j)` for each batch of new signals
  - Weights constrained to [5%, 20%] of available cash, then re-normalised to sum to 100%
  - Manual position sizing (non-signal entries) must remain UNCHANGED — this is the RISK-03 regression gate
  - Output must match production_strategy.py backtest logic for equivalent inputs
  - Unit tests: weight calculation, constraint+normalisation, manual path unchanged, reference calculation match; integration: new signal response includes inv-vol allocated shares
- **Unblock criteria:** Commit `[EPIC-01][ST-04]` pushed with all 5 ACs implemented; manual sizing regression test passing
- **Status:** Unblocked
- **commit_sha:** e49d5a8b1a5dd14247d28338ae19765c77cf33c3

---

## DEL-20260624-05

- **Story:** ST-05 — Risk-off exit alerts for existing positions (EPIC-01)
- **Delegation class:** delegated_backend
- **Assigned to:** Head of Engineering
- **Raised at:** 2026-06-24T15:00:00Z
- **GitHub issue:** #843
- **Branch:** exec/2026-06-24__release-v6.2/EPIC-01
- **Commit format required:** `[EPIC-01][ST-05] <description>`
- **Spec references:** docs/specs/api_contracts/position_endpoints.md#GET /positions
- **Design spec:** docs/design/2026-06-24__release-v6.2/risk-off-exit-alert/ux_spec.md
- **Delegation context:**
  - Nightly regime check: if `SPY < MA200` → flag all open US positions with `risk_off_exit` alert; if `FTSE < MA200` → flag all open UK positions
  - Alerts clear automatically when relevant index recovers above MA200
  - US and UK markets are isolated — US regime does NOT affect UK positions and vice versa
  - `risk_off_exit` alert visible per position in portfolio view; visually distinct from trailing stop breach and `exit_rebalance` signals per UX spec (deep blue #1E40AF per v6.2 design gate)
  - ST-06 (Sprint 2) depends on risk_off_exit alerts being live — verify AC-01/03/04 before Sprint 1 close
- **Unblock criteria:** Commit `[EPIC-01][ST-05]` pushed with all 4 ACs implemented
- **Status:** Unblocked
- **commit_sha:** e49d5a8b1a5dd14247d28338ae19765c77cf33c3

---

## DEL-20260624-06

- **Story:** ST-06 — AI daily briefing — backend endpoint (EPIC-02)
- **Delegation class:** delegated_backend
- **Assigned to:** Head of Engineering
- **Raised at:** 2026-06-24T15:00:00Z
- **GitHub issue:** #848
- **Branch:** exec/2026-06-24__release-v6.2/EPIC-02
- **Commit format required:** `[EPIC-02][ST-06] <description>`
- **Spec reference:** docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing (new endpoint — must be added in same commit)
- **Dependencies:** ST-01, ST-03, ST-05 must be verified and live before execution begins
- **Pre-condition gate:** §13 review PASS recorded 2026-06-24 in decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md + EPIC-01 complete
- **Delegation context:**
  - `POST /ai/daily-briefing` endpoint: assembles current portfolio state, top-5 signals, per-position trailing stops, regime status, rebalance date check; sends to claude-sonnet-4-6; returns `{ summary: string, actions: [{type, ticker, description}] }`
  - Response time < 10 seconds for < 10 open positions
  - Uses `claude-sonnet-4-6` model; token usage logged to `claude_audit_log` per established pattern
  - `advisory: true` required in response metadata
  - **Same-commit requirements (CLAUDE.md §2):** (a) `## POST /ai/daily-briefing` entry in `docs/specs/api_contracts/ai_endpoints.md`; (b) `POST /ai/daily-briefing` path in `docs/reference/openapi.yaml`; (c) route registered in `backend/routers/test.py`; (d) `src/pages/SystemStatus.js` fallback count updated; (e) SC-SS-01b in `tests/e2e/system-status.spec.js` updated to match new fallback count
- **Unblock criteria:** EPIC-01 complete + §13 PASS confirmed; commit `[EPIC-02][ST-06]` pushed with all 6 ACs and all same-commit requirements met
- **Status:** Unblocked
- **commit_sha:** 98ca767119318072be8644daef222ee818f4cc77

---

## DEL-20260624-07

- **Story:** ST-07 — AI Daily Briefing card — frontend (EPIC-02)
- **Delegation class:** delegated_frontend
- **Assigned to:** Head of Engineering
- **Raised at:** 2026-06-24T15:00:00Z
- **GitHub issue:** #849
- **Branch:** exec/2026-06-24__release-v6.2/EPIC-02
- **Commit format required:** `[EPIC-02][ST-07] <description>`
- **Spec reference:** docs/specs/frontend/pages/dashboard.md (v2.3)
- **Design spec:** docs/design/2026-06-24__release-v6.2/ai-daily-briefing-card/ux_spec.md
- **Dependency:** ST-06 must be done first
- **Delegation context — Base44 prompt draft:**
  1. **Context:** Dashboard page needs a "Today's Briefing" card displaying the AI daily briefing
  2. **Change required:** Full-width card below session-summary section; calls POST /ai/daily-briefing; displays summary paragraph, ordered action list with type chips (EXIT/ENTER/MONITOR/HOLD), generation timestamp, and Regenerate button
  3. **API contract reference:** docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing; response shape: `{ summary: string, actions: [{type, ticker, description}], advisory: true }`
  4. **Behaviour rules:** Card visible on Dashboard; action list with type chips; Regenerate button triggers new POST call; advisory label non-dismissible; verify `advisory: true` client-side before displaying
  5. **Non-functional rules:** §13 compliant — advisory-only display; AI advisory label "AI Advisory — all actions require your confirmation" must be present and non-dismissible
  6. **Expected outcome:** Playwright for AC-01/02/03/05; human staging sign-off for AC-04 (advisory label wording and styling)
- **Unblock criteria:** ST-06 done; commit `[EPIC-02][ST-07]` pushed with Playwright tests for AC-01/02/03/05; AC-04 staging sign-off
- **Status:** Unblocked
- **commit_sha:** bbcb38e395bdc3cff7e3a90a08e931dade7e10e3

---

## DEL-20260624-08

- **Story:** ST-08 — Conversational AI trade advisor — backend endpoint (EPIC-02)
- **Delegation class:** delegated_backend
- **Assigned to:** Head of Engineering
- **Raised at:** 2026-06-24T15:00:00Z
- **GitHub issue:** #850
- **Branch:** exec/2026-06-24__release-v6.2/EPIC-02
- **Commit format required:** `[EPIC-02][ST-08] <description>`
- **Spec reference:** docs/specs/api_contracts/ai_endpoints.md#POST /ai/chat (new endpoint — must be added in same commit)
- **Dependency:** ST-06 (shared context assembly pattern)
- **Delegation context:**
  - `POST /ai/chat` accepts `{ question: string, context?: { ticker?, position_id? } }`
  - Loads full portfolio + signal state and injects as system prompt context; grounded in live portfolio state
  - Response time < 15 seconds; stateless per request (no session memory)
  - Uses `claude-sonnet-4-6`; token usage logged
  - **Same-commit requirements (CLAUDE.md §2):** (a) `## POST /ai/chat` entry in `docs/specs/api_contracts/ai_endpoints.md`; (b) `POST /ai/chat` path in `docs/reference/openapi.yaml`; (c) route registered in `backend/routers/test.py`; (d) `src/pages/SystemStatus.js` fallback count updated; (e) SC-SS-01b in `tests/e2e/system-status.spec.js` updated to match new fallback count
- **Unblock criteria:** ST-06 done; commit `[EPIC-02][ST-08]` pushed with all 6 ACs and same-commit requirements met
- **Status:** Unblocked
- **commit_sha:** 98ca767119318072be8644daef222ee818f4cc77

---

## DEL-20260624-09

- **Story:** ST-09 — AI chat widget — frontend (EPIC-02)
- **Delegation class:** delegated_frontend
- **Assigned to:** Head of Engineering
- **Raised at:** 2026-06-24T15:00:00Z
- **GitHub issue:** #851
- **Branch:** exec/2026-06-24__release-v6.2/EPIC-02
- **Commit format required:** `[EPIC-02][ST-09] <description>`
- **Spec reference:** docs/specs/frontend/pages/positions.md (v1.8)
- **Design spec:** docs/design/2026-06-24__release-v6.2/ai-chat-widget/ux_spec.md
- **Dependency:** ST-08 must be done first
- **Delegation context — Base44 prompt draft:**
  1. **Context:** Positions page needs an AI chat widget for ad-hoc portfolio questions
  2. **Change required:** Floating chat widget on Positions page (canonical placement); user types question and submits; response displayed in widget; loading and error states required
  3. **API contract reference:** docs/specs/api_contracts/ai_endpoints.md#POST /ai/chat; request: `{ question: string, context?: { ticker?, position_id? } }`
  4. **Behaviour rules:** Widget visible on Positions page; submit/response flow; loading indicator during API call; error state if POST /ai/chat fails or times out; advisory label present and non-dismissible; no trade execution from widget
  5. **Non-functional rules:** §13 compliant — advisory-only; "AI Advisory — all actions require your confirmation" label present
  6. **Expected outcome:** Playwright for AC-01/02/04/05; human staging sign-off for AC-03 (advisory label wording and non-executability). Signals page placement is stretch goal only — do not treat as in-scope.
- **Unblock criteria:** ST-08 done; commit `[EPIC-02][ST-09]` pushed; Playwright for AC-01/02/04/05; AC-03 staging sign-off
- **Status:** Unblocked
- **commit_sha:** bbcb38e395bdc3cff7e3a90a08e931dade7e10e3
