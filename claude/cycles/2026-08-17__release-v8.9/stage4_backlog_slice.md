Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-17
Cycle: 2026-08-17__release-v8.9
Release: v8.9

# Backlog Slice — v8.9

<!-- release-plan-marker: RP:v8.9:2026-08-17__release-v8.9 -->

22 stories across 6 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Led by 2 live P0 risk-management-correctness fixes; scope widened to the confirmed ~24–28 day/sprint capacity band per Product Owner decision (2026-08-17).

---

## EPIC-01 — Live Risk-Management Correctness

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner

### ST-01 — Fix nightly trailing-stop ratchet to apply breakeven floor for profitable positions
**Source:** BLG-BE-102
**Priority:** P0 (Critical)
**Effort:** M
**Acceptance Criteria:**
- Only one trailing-stop calculation path is used in production (nightly job and any on-demand recompute)
- No open profitable position has `current_stop` below its own `entry_price`
- Regression test added and passing, covering the breakeven-floor case
- Backend Engineering Patterns Owner sign-off

### ST-02 — Fix currency basis of current_trailing_stop/stop_price for US-market positions
**Source:** BLG-BE-103
**Priority:** P0 (Critical)
**Effort:** S
**Depends on:** ST-01 (same position data path)
**Acceptance Criteria:**
- `initial_stop`, `current_trailing_stop`, and `stop_price` are all in the same currency basis (native) for a given position, or are unambiguously suffixed and the frontend consumes the correct one
- A US-market profitable position test case shows a single consistent stop value across Init and live-stop tiles
- Backend Engineering Patterns Owner and Frontend Specifications & UX Documentation Owner sign-off

### ST-03 — Add trailing_stop_action_rate spec entry with validation tolerances
**Source:** BLG-SPEC-85
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Entry added to `metrics_definitions.md`
- Tolerances stated numerically, not qualitatively

---

## EPIC-02 — Trade Sizing & Post-Trade Intelligence

**Maps to:** S2-02
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner

### ST-04 — Correlation/sector-concentration-aware position sizing
**Source:** BLG-BE-104
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- A new position's sizing calculation reflects existing open-position sector concentration, not just the candidate ticker's own volatility
- Sizing output includes a visible reason when reduced or flagged for concentration
- Regression test confirms two same-sector (correlated) positions produce a smaller second size than two uncorrelated ones would
- Backend Engineering Patterns Owner sign-off

### ST-05 — Pre-commit "what-if" sizing/risk simulator on the trade-plan form
**Source:** BLG-FEAT-91
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- User can adjust stop distance/entry price on the trade-plan form and see position size, R at risk, and portfolio heat impact update live, before saving
- Preview value matches what is actually saved when the plan is submitted with the same inputs
- No DB write occurs from interacting with the preview alone

### ST-06 — Automated AI post-trade debrief
**Source:** BLG-FEAT-90
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- Every newly-closed trade has an AI-generated debrief available shortly after close (real-time generation, or on-demand if real-time isn't feasible)
- Debrief references plan-vs-reality data and any linked journal entries where present
- Generation is logged to `claude_audit_log` per existing AI governance policy
- AI Compliance & Governance Officer sign-off (per standing AI-generated-content governance requirement)

### ST-07 — In-app backtesting engine for strategy rule changes
**Source:** BLG-FEAT-89
**Priority:** P2 (Medium)
**Effort:** L
**Acceptance Criteria:**
- A candidate `strategy_rules.md` change can be run against historical data from inside the app, with no external script step
- Output includes win rate, R-multiple distribution, and drawdown compared against the current live rule set
- Each backtest run is persisted with enough detail to audit later (what was tested, when, by what rule diff)
- Strategy Rules & System Intent Owner sign-off

---

## EPIC-03 — Backend Reliability & Performance

**Maps to:** S2-03
**Owner:** Backend Engineering Patterns Owner; Head of Engineering

### ST-08 — Investigate GET /trade-plans/tags ~10s p50 latency
**Source:** BLG-BE-98
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- Root cause identified; fix applied or filed as a follow-up with root cause documented
- Re-measured p50 within the same order of magnitude as `GET /positions/tags`
- Backend Engineering Patterns Owner sign-off

### ST-09 — Verify ST-11 duration logging against a real post-merge invocation
**Source:** BLG-BE-99
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- A real invocation's Render log confirms the `"SI-05 digest sent... in %.2fs"` (or failure-path equivalent) line is present with a real elapsed-time value
- `docs/ops/api_performance_baseline.md` §36 updated with the real timing

### ST-10 — Wrap audit-trail writes in the same transaction as the primary state update
**Source:** BLG-BE-100
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- A documented, deliberate fix-or-accept decision exists for both audit-write call sites (`position_state_history`, `position_audit_log`)
- If fixed, a test demonstrates the audit row is not written when the primary write fails
- If accepted, the risk and rationale are recorded in `data_model.md`'s relevant DS entries

### ST-11 — Confirm trade_csv_service.py::build_trade_history_csv is dead code and remove, or document coexistence
**Source:** BLG-BE-101
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Dead-code status confirmed or refuted; if dead, removed; if kept, reason documented in a code comment
- Head of Engineering sign-off

---

## EPIC-04 — Test Coverage & QA Hardening

**Maps to:** S2-04
**Owner:** QA & Testing Owner; Director of Quality; Product Owner

### ST-12 — Add test coverage for screener_refresh/risk_off_alerts job-registration wiring
**Source:** BLG-QA-149
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- Tests added covering success + error paths for both `screener_refresh` and `risk_off_alerts`
- QA & Testing Owner sign-off

### ST-13 — Decide and apply treatment for trade_plans.setup_type with no default/required guarantee
**Source:** BLG-QA-150
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Decision recorded (required field vs. default value vs. accept-as-is with documented rationale)
- If a fix is chosen, implemented
- Product Owner sign-off

### ST-14 — Add direct unit tests for cash_service, compliance_service, news_service, validation_service
**Source:** BLG-QA-151
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- All 4 modules have at least one direct unit test exercising non-trivial logic (not just an HTTP-level smoke test)
- QA & Testing Owner sign-off

### ST-15 — Add Playwright coverage for WhatsNewCard's changelog User Impact rendering
**Source:** BLG-QA-152
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Playwright test added and passing in CI
- QA & Testing Owner sign-off

---

## EPIC-05 — Operations & Spec Currency

**Maps to:** S2-05
**Owner:** Infrastructure & Operations Owner; API Contracts & Documentation Owner; Head of Specs Team

### ST-16 — Local dev venv version-pin enforcement; confirm PUBLIC_URL parity on production
**Source:** BLG-OPS-146
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Local venv setup instructions updated so a fresh setup following them resolves to Python 3.11 (matching the existing pin)
- Production `PUBLIC_URL` status confirmed and documented
- Infrastructure & Operations Owner sign-off

### ST-17 — Archive window_summary_IW-*.md files older than 90 days
**Source:** BLG-OPS-113
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Archive folder created; files older than 90 days moved
- No content lost (move, not delete)

### ST-18 — Document screener_refresh and risk_off_alerts jobs in health_endpoints.md
**Source:** BLG-SPEC-130
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- All six live job names present in the spec's architecture note and response example
- API Contracts & Documentation Owner sign-off

---

## EPIC-06 — Governance Process Debt Closure

**Maps to:** S2-06
**Owner:** Head of Specs Team

### ST-19 — Fix post_ship_closure.md to actually write last_post_ship_cycle/last_post_ship_utc
**Source:** BLG-GOV-308
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- `post_ship_closure.md` STEP 10 unconditionally writes both fields every run
- Standard CLAUDE.md §6 governance file edit checklist applied (version bump, `OPERATIONAL_GUIDE.md` §14, `prompt_change_log.md` entry)
- Head of Specs Team sign-off

### ST-20 — Root-cause and correct execution_state.json timestamp drift from actual git commit dates
**Source:** BLG-GOV-309
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Root cause identified
- Fixed, or documented as intentional
- Head of Specs Team sign-off

### ST-21 — Physically place the Displacement Debt Register and wire it into roadmap_prompt.md STEP 8
**Source:** BLG-GOV-264
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- `claude/roadmap/displacement_debt_register.md` created with the seeded content
- `roadmap_prompt.md` STEP 8 updated to reference it (standard CLAUDE.md §6 checklist applied)
- `ESC-EXEC-20260727-02` closed

### ST-22 — Define a pruning rule for stale RA: roadmap-annotation markers older than 3 releases
**Source:** BLG-GOV-260
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Rule documented in `roadmap_management_prompt.md`
- Head of Specs Team sign-off
