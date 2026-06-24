**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.2
**Cycle:** 2026-06-24__release-v6.2
**Last Updated:** 2026-06-24

---

# Backlog Slice — v6.2 Production Strategy Parity & AI Intelligence

---

## EPIC-01 — Strategy Parity: Core Engine Alignment

**Maps to:** S2-01, S2-02, S2-03, S2-04
**Owner:** Head of Engineering
**Risk IDs:** RISK-03
**Sequencing:** Sprint 1 — prerequisite for EPIC-02

Close the gap between the live system and `production_strategy.py` backtest logic across four dimensions: trailing stop ratchet, month-end rebalance exit signals, inverse-volatility position sizing for signal entries, and risk-off exit alerts for open positions. These four items form a coherent parity cluster that makes the live system's daily behaviour consistent with the backtest.

---

### ST-01 — Nightly trailing stop computation — backend service

**EPIC:** EPIC-01
**Maps to:** S2-01 (BLG-FEAT-46)
**Owner:** Head of Engineering
**Effort:** M (~2 days)
**Delegation class:** delegated_backend
**Dependencies:** None

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | Nightly job iterates all open positions, fetches current price + 14-day ATR, and computes updated trailing stop using profit-lock logic: if position in profit use `current_price − 2×ATR`; else use `entry_price − 5×ATR` | Unit tests — profit-lock branch coverage |
| AC-02 | Stop ratchet is enforced: `UpdatedStop = max(CurrentStop, NewlyCalculatedStop)` — stop only ever moves up | Unit test — ratchet invariant |
| AC-03 | Updated stop stored per position in database and retrievable via `GET /positions` response (new field: `current_trailing_stop`) | Integration test |
| AC-04 | Logic matches `production_strategy.py` parameters: `INITIAL_ATR_MULT=5`, `PROFIT_ATR_MULT=2`, `ATR_PERIOD=14` | Unit test with known inputs validated against backtest |
| AC-05 | Existing `initial_stop` field is unchanged — `current_trailing_stop` is an additional computed field | Regression: GET /positions response schema unchanged |

---

### ST-02 — Trailing stop display and breach badge — frontend

**EPIC:** EPIC-01
**Maps to:** S2-01 (BLG-FEAT-46)
**Owner:** Head of Engineering
**Effort:** M (~1 day)
**Delegation class:** delegated_frontend
**Dependencies:** ST-01 (current_trailing_stop field must be available)

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | Each open position in the portfolio view displays `current_trailing_stop` alongside the original `initial_stop` | Playwright — trailing stop value visible on positions page |
| AC-02 | A visible breach badge/alert is shown when `current_price ≤ current_trailing_stop` | Playwright — badge visible for breach condition |
| AC-03 | Breach badge is visually distinct from other position status indicators (different colour/icon) | Human staging sign-off [staging-only evidence] |
| AC-04 | No breach badge shown when position is within stop bounds | Playwright — badge absent for non-breach condition |

---

### ST-03 — Month-end rebalance exit signal generation

**EPIC:** EPIC-01
**Maps to:** S2-02 (BLG-FEAT-47)
**Owner:** Head of Engineering
**Effort:** M (~1.5 days)
**Delegation class:** delegated_backend
**Dependencies:** None (independent of ST-01)

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | On the last trading day of each calendar month, system computes which open positions are NOT in the current top-5 momentum signal list | Unit test — month-end detection logic |
| AC-02 | A signal record with `status = exit_rebalance` is generated for each such position | Unit test — signal record creation |
| AC-03 | Month-end detection uses last trading day logic (not last calendar day) — weekend/holiday awareness | Unit test — weekend/holiday edge cases |
| AC-04 | No duplicate `exit_rebalance` signal if the position is also crossing a stop | Unit test — deduplication |
| AC-05 | `exit_rebalance` signals are returned by `GET /signals` and visually distinct from stop exits in the UI (distinct label/styling) | Playwright — `exit_rebalance` label visible; Human staging sign-off for styling [staging-only evidence] |

---

### ST-04 — Inverse-volatility position sizing for signal-driven entries

**EPIC:** EPIC-01
**Maps to:** S2-03 (BLG-FEAT-48)
**Owner:** Head of Engineering
**Effort:** M (~2 days)
**Delegation class:** delegated_backend
**Dependencies:** None

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | For each batch of new signals at a rebalance event, inv-vol weights are computed: `weight_i = (1/ATR_i) / Σ(1/ATR_j)` | Unit test — weight calculation correctness |
| AC-02 | Each weight is constrained to `[5%, 20%]` of available cash, then re-normalised to sum to 100% | Unit test — constraint + normalisation |
| AC-03 | New signal allocations use inv-vol sizing, not the fixed-risk £200 model | Integration test — new signal response includes inv-vol allocated shares |
| AC-04 | Manual position sizing (non-signal entries) continues to use the fixed-risk path unchanged | Regression: manual sizing output unchanged |
| AC-05 | Sizing output matches `production_strategy.py` backtest logic for equivalent inputs (test against known batch case) | Unit test — reference calculation match |

---

### ST-05 — Risk-off exit alerts for existing positions

**EPIC:** EPIC-01
**Maps to:** S2-04 (BLG-FEAT-49)
**Owner:** Head of Engineering
**Effort:** S (~0.5 day)
**Delegation class:** delegated_backend
**Dependencies:** None

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | Nightly regime check: if `SPY < MA200`, all open US positions are flagged with a `risk_off_exit` alert; if `FTSE < MA200`, all open UK positions flagged | Unit test — per-market flag logic |
| AC-02 | `risk_off_exit` alert is visible per position in the portfolio view, visually distinct from trailing stop breach and `exit_rebalance` signals | Playwright — alert visible; Human staging sign-off for styling [staging-only evidence] |
| AC-03 | Alerts clear automatically when the relevant index recovers above MA200 | Unit test — alert clearance logic |
| AC-04 | US risk-off event does NOT trigger alerts on UK positions, and vice versa | Unit test — market isolation |

---

## EPIC-02 — AI Intelligence Layer

**Maps to:** S2-05, S2-06
**Owner:** Head of Engineering
**Risk IDs:** RISK-01
**Sequencing:** Sprint 2 — after EPIC-01 complete; §13 review required before sprint planning seal

Layer AI decision support on top of the live strategy data. The daily briefing (S2-05) synthesises trailing stop alerts, rebalance exits, regime status, and new entries into a plain-English action plan. The trade advisor (S2-06) answers ad-hoc portfolio questions grounded in live state. Both are advisory-only, §13 compliant.

**Pre-condition gate:** Strategy Rules & System Intent Owner §13 review for BLG-FEAT-50 and BLG-FEAT-51 must be completed and recorded in decisions before sprint planning seal.

---

### ST-06 — AI daily briefing — backend endpoint

**EPIC:** EPIC-02
**Maps to:** S2-05 (BLG-FEAT-50)
**Owner:** Head of Engineering
**Effort:** M (~2 days)
**Delegation class:** delegated_backend
**Dependencies:** ST-01 (trailing stop data), ST-03 (rebalance exit signals), ST-05 (risk-off alerts)

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | `POST /ai/daily-briefing` endpoint exists and returns HTTP 200 with structured response | Integration test |
| AC-02 | Response assembles: current portfolio state, today's top-5 signals, per-position trailing stops, regime status, rebalance date check | Unit test — context assembly completeness |
| AC-03 | Response time < 10 seconds for typical portfolio (< 10 open positions) | Integration test — latency assertion |
| AC-04 | Response format: `{ summary: string, actions: [{type, ticker, description}] }` | Unit test — schema validation |
| AC-05 | Uses `claude-sonnet-4-6`; token usage logged to `claude_audit_log` per established pattern | Unit test — audit log entry created |
| AC-06 | Output labelled as AI advisory in response metadata (`advisory: true`); endpoint documented in relevant API contract | Contract compliance check |

---

### ST-07 — AI Daily Briefing card — frontend

**EPIC:** EPIC-02
**Maps to:** S2-05 (BLG-FEAT-50)
**Owner:** Head of Engineering
**Effort:** S (~0.5 day)
**Delegation class:** delegated_frontend
**Dependencies:** ST-06

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | "Today's Briefing" card visible on the Dashboard page | Playwright — card element present |
| AC-02 | Card displays AI briefing summary paragraph and ordered action list | Playwright — summary and action list visible |
| AC-03 | Card shows generation timestamp and "Regenerate" button | Playwright — timestamp and button visible |
| AC-04 | Card is clearly labelled as AI advisory (e.g. "AI Advisory — all actions require your confirmation") | Human staging sign-off [staging-only evidence] |
| AC-05 | Regenerate button triggers a new POST /ai/daily-briefing call and updates the card content | Playwright — button triggers update |

---

### ST-08 — Conversational AI trade advisor — backend endpoint

**EPIC:** EPIC-02
**Maps to:** S2-06 (BLG-FEAT-51)
**Owner:** Head of Engineering
**Effort:** M (~1 day)
**Delegation class:** delegated_backend
**Dependencies:** ST-06 (shared context assembly pattern)

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | `POST /ai/chat` endpoint accepts `{ question: string, context?: { ticker?, position_id? } }` | Integration test |
| AC-02 | Endpoint loads full portfolio + signal state and injects as system prompt context | Unit test — context injection confirmed |
| AC-03 | Responses are grounded in live portfolio state (not generic strategy descriptions) | Integration test — answer references live data |
| AC-04 | Response time < 15 seconds | Integration test — latency assertion |
| AC-05 | Conversation is stateless per request (no session memory across calls) | Unit test — no session state stored |
| AC-06 | Uses `claude-sonnet-4-6`; token usage logged; endpoint documented in API contract | Contract compliance + audit log |

---

### ST-09 — AI chat widget — frontend

**EPIC:** EPIC-02
**Maps to:** S2-06 (BLG-FEAT-51)
**Owner:** Head of Engineering
**Effort:** S (~0.5 day)
**Delegation class:** delegated_frontend
**Dependencies:** ST-08

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | AI chat widget visible on signals or portfolio page | Playwright — widget element present |
| AC-02 | User can type a question and submit; response displayed in widget | Playwright — submit and response flow |
| AC-03 | Widget clearly labelled as AI advisory; trade actions not executable from widget | Human staging sign-off [staging-only evidence] |
| AC-04 | Loading state shown during API call | Playwright — loading indicator visible |
| AC-05 | Error state shown if POST /ai/chat fails or times out | Playwright — error state visible |

---

## EPIC-03 — Governance & QA Debt

**Maps to:** S2-07, S2-08, S2-09, S2-10
**Owner:** Head of Specs Team (ST-10/11); Director of Quality (ST-13); Infrastructure & Operations Owner (ST-12)
**Risk IDs:** RISK-02 (release-level)
**Sequencing:** Sprint 1 — independent of EPIC-01/02

Four targeted debt items: two execution_prompt.md governance patches (BLG-GOV-135/136), one operations baseline update (BLG-OPS-75), and the structural Playwright registration fix (BLG-QA-62).

---

### ST-10 — execution_prompt autonomous class hard gate (BLG-GOV-135)

**EPIC:** EPIC-03
**Maps to:** S2-07 (BLG-GOV-135)
**Owner:** Head of Specs Team
**Effort:** XS (<1 hour)
**Delegation class:** autonomous
**Dependencies:** None

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | `execution_prompt.md §3.2.A` updated with explicit frontend-visible change detection rule: if any story creates/modifies `src/components/**` or `src/pages/**`, autonomous class path is unavailable | Document inspection |
| AC-02 | Rule unambiguously blocks autonomous class when any story has frontend-visible changes, regardless of Playwright coverage | Document inspection |
| AC-03 | `execution_prompt.md` version bumped; `OPERATIONAL_GUIDE.md §14` and `prompt_change_log.md` updated per CLAUDE.md §6 | Document inspection |
| AC-04 | `qa_evidence_template.md` criterion 3 advisory updated to reference the new rule | Document inspection |

---

### ST-11 — execution_prompt test_scenarios path validation (BLG-GOV-136)

**EPIC:** EPIC-03
**Maps to:** S2-08 (BLG-GOV-136)
**Owner:** Head of Specs Team
**Effort:** XS (<1 hour)
**Delegation class:** autonomous
**Dependencies:** None (may batch with ST-10)

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | `execution_prompt.md §3.2.A` (test_scenarios population) updated with advisory: test file paths must be under `tests/` or `tests/e2e/`; `docs/testing/` paths are QA evidence artefacts, not scenario files | Document inspection |
| AC-02 | `execution_prompt.md` version bumped; `OPERATIONAL_GUIDE.md §14` and `prompt_change_log.md` updated per CLAUDE.md §6 | Document inspection |

---

### ST-12 — api_performance_baseline.md — 2 new v6.1 endpoint measurements (BLG-OPS-75)

**EPIC:** EPIC-03
**Maps to:** S2-09 (BLG-OPS-75)
**Owner:** Infrastructure & Operations Owner
**Effort:** XS (<1 hour)
**Delegation class:** autonomous
**Dependencies:** None

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | `GET /portfolio/sector-weights` entry added to `docs/ops/api_performance_baseline.md` with p50, p95, and measurement date | Document inspection |
| AC-02 | `GET /trade-plans/setup-quality-score` entry added with p50, p95, and measurement date | Document inspection |
| AC-03 | Measurements sourced from Render internal logs or live endpoint test [staging-only evidence] | Human staging verification |

---

### ST-13 — Playwright spec auto-registration via glob pattern (BLG-QA-62)

**EPIC:** EPIC-03
**Maps to:** S2-10 (BLG-QA-62)
**Owner:** Director of Quality; Head of Frontend Engineering
**Effort:** S (<0.5 day)
**Delegation class:** delegated_qa
**Dependencies:** None

**Acceptance Criteria:**

| AC | Description | Verification |
|----|-------------|-------------|
| AC-01 | `playwright.yml` updated to use glob pattern (e.g. `tests/e2e/**/*.spec.js`) replacing the explicit spec file list | CI pass |
| AC-02 | All existing spec files continue to run in CI (no regression) | CI: all prior Playwright scenarios pass |
| AC-03 | A new spec file added to `tests/e2e/` is automatically included in CI without manual registration | Document inspection — no manual registration step required |
