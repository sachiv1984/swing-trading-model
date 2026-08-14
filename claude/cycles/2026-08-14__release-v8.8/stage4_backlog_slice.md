Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-14
Cycle: 2026-08-14__release-v8.8
Release: v8.8

# Backlog Slice — v8.8

<!-- release-plan-marker: RP:v8.8:2026-08-14__release-v8.8 -->

29 stories across 7 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope widened beyond the 7 items explicitly `Provisional-Target: v8.8` per Product Owner decision (2026-08-14) to target closer to the confirmed ~24–28 day/sprint capacity band; led by 2 live P1 data-integrity gaps.

---

## EPIC-01 — Live Data-Integrity & Scheduled Job Coverage

**Maps to:** S2-01
**Owner:** Infrastructure & Operations Owner

### ST-01 — Add scheduled overnight screener refresh workflow
**Source:** BLG-OPS-144
**Priority:** P1 (High)
**Effort:** S
**Acceptance Criteria:**
- Screener results refresh automatically on a nightly schedule with no manual trigger required
- A missed/failed run is visible via `GET /health/scheduler`

### ST-02 — Add scheduled nightly risk-off-alerts workflow (regime badge permanently stuck)
**Source:** BLG-OPS-145
**Priority:** P1 (High)
**Effort:** S
**Acceptance Criteria:**
- `risk_off_exit` is refreshed nightly against live market regime data
- The `RISK OFF` badge on Positions correctly reflects current regime state
- The job's run status is visible via `GET /health/scheduler`

### ST-03 — Investigate nightly backtest import failure (Strategy Benchmark "data as of" line never populates)
**Source:** BLG-OPS-143
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- `backtest.yml` completes successfully on its next scheduled run and `backtest_trades.imported_at` reflects a current timestamp
- "Benchmark data as of ..." line renders on the Strategy Benchmark page with a recent date

### ST-04 — Add remaining pre-v4.6 endpoint (GET /v1beta1/news) to api_performance_baseline.md
**Source:** BLG-OPS-13
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- `GET /v1beta1/news` has p50 and p95 latency entries in the baseline document, consistent with existing measurement methodology
- Re-confirmed against the correct canonical path/shape post `BLG-SPEC-116`

### ST-05 — Add GET /trade-plans/tags to api_performance_baseline.md
**Source:** BLG-OPS-135
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- `GET /trade-plans/tags` has p50/p95/max latency entries in the baseline document, consistent with existing measurement methodology

### ST-06 — Live timing measurement for GET /analytics/strategy-version-comparison in api_performance_baseline.md
**Source:** BLG-OPS-51
**Priority:** P3 (Low)
**Effort:** S
**Note:** Row already exists in §34 (added v8.4) marked "Pending live timing run" with estimated values — scope narrowed to running the live measurement, not building the row from scratch (per 2026-08-13 backlog audit note).
**Acceptance Criteria:** `GET /analytics/strategy-version-comparison`'s baseline row updated with measured (not estimated) p50/p95 values from ≥5 staging samples

---

## EPIC-02 — Backend Engineering Hardening

**Maps to:** S2-02
**Owner:** Backend Engineering Patterns Owner

### ST-07 — Consolidate two divergent check_market_regime() implementations
**Source:** BLG-BE-97
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- Only one `check_market_regime()` implementation remains in the backend
- All call sites (position analysis, `/market/status`, pre-entry validation, signal generation) use it
- No behavioural regression in existing regime-dependent tests

### ST-08 — Position lifecycle state-transition history table
**Source:** BLG-BE-58
**Priority:** P3 (Low)
**Effort:** M
**Acceptance Criteria:**
- Append-only `position_state_history` table added with migration
- Transitions logged on each lifecycle state change
- No behavioural change to current lifecycle logic

### ST-09 — Link price_alerts to the trade they trigger (real alert-to-trade provenance)
**Source:** BLG-BE-84
**Priority:** P3 (Low)
**Effort:** M (estimate advisory only — not fully scoped; see RISK-02)
**Acceptance Criteria:**
- A trade plan created via the alert-notification-to-trade-plan path records which `price_alerts` row triggered it
- A trade plan created any other way leaves the field null
- Reporting treatment (new `trade_origin` value vs. separate field) decided and documented before implementation

### ST-10 — Populate si05_digest_log.telegram_message_id on successful send
**Source:** BLG-BE-85
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- A successful SI-05 digest send populates a real, non-null `telegram_message_id` in `si05_digest_log`
- Failure-path logging unchanged
- Existing retry/backoff behaviour unaffected

### ST-11 — Add duration logging around POST /digest/si05/send's Telegram send call
**Source:** BLG-BE-87
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- A successful or failed invocation's Render log line includes an elapsed-time value
- Verified against the next real invocation (scheduled cron run or manual `workflow_dispatch`)
- `docs/ops/api_performance_baseline.md` §36 updated with real log-derived timing

### ST-12 — Pre-Trade Research View query-latency budget review
**Source:** BLG-BE-94
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:** Review complete; any regression fixed or filed; Head of Engineering sign-off

---

## EPIC-03 — Frontend UX & Dead-Code Cleanup

**Maps to:** S2-03
**Owner:** Frontend Specifications & UX Documentation Owner; Product Owner

**Design Gate:** Required — all 5 items below carry observable UI acceptance criteria (see STEP 4.1).

### ST-13 — "What's New" panel surfaces user-facing benefit statements, not raw engineering copy
**Source:** BLG-FE-161
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- `WhatsNewCard` renders curated user-benefit copy, not raw EPIC implementation descriptions
- An EPIC with no user-facing change does not appear in the What's New feed
- Changelog authoring convention documented so future releases populate the new field correctly

### ST-14 — Research page trade plan status badge: fix raw snake_case for 3 of 6 statuses
**Source:** BLG-FE-162
**Priority:** P2 (Medium)
**Effort:** XS
**Acceptance Criteria:**
- All 6 trade plan statuses render a human-readable label on the Research page, none fall back to raw snake_case
- Single source of truth for status labels (no duplicate/divergent maps between TradePlan.js and Research.js)

### ST-15 — Ticker Universe page filtering by search, sector, and industry
**Source:** BLG-FE-163
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- User can filter the ticker table by typed search text, by sector, and by industry, independently or combined with the existing market/active filters
- Filters visibly narrow the table row count and clear/reset correctly

### ST-16 — Resolve PositionEntryModal.js dead-code/unreachable-mount-point status
**Source:** BLG-FE-159
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- `PositionEntryModal.js` is either reachable via a real user-navigable trigger with Playwright coverage of its light/dark theming, or removed from the codebase
- No orphaned/unreachable modal component remains without an explicit decision recorded

### ST-17 — Add Playwright coverage for Card and secondary-variant components when a live call site exists
**Source:** BLG-FE-160
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- Playwright test added covering `card`/`card-foreground` computed colour/background at the first live call site introduced for the Card component
- Playwright test added covering `secondary`/`secondary-foreground` computed colour/background at the first live call site introduced

---

## EPIC-04 — Quality & Test-Coverage Debt

**Maps to:** S2-04
**Owner:** Director of Quality; QA & Testing Owner

### ST-18 — Field-population completeness audit for Arc 6 prerequisite fields
**Source:** BLG-QA-140
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:** Audit complete; gaps fixed or filed; QA & Testing Owner sign-off

### ST-19 — Consolidated backend service-layer test-coverage report
**Source:** BLG-QA-143
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:** Report generated; gaps triaged; QA & Testing Owner sign-off

### ST-20 — Test-environment parity check — local vs CI vs staging config drift
**Source:** BLG-QA-145
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:** Audit complete; drift fixed or documented as intentional; QA Lead sign-off

### ST-21 — backend/routers/test.py completeness re-audit
**Source:** BLG-QA-146
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:** Re-audit complete against all `@router.*` decorators; any gap fixed; QA & Testing Owner sign-off

---

## EPIC-05 — Security Hardening

**Maps to:** S2-05
**Owner:** Cybersecurity & Trust Lead

### ST-22 — Add system/user role separation to Claude thesis-generation prompts
**Source:** BLG-SEC-33
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- `generate_full_plan()` and `generate_setup_thesis()` pass trusted instructions via the `system` parameter, not interleaved with untrusted user data
- `tests/test_gemini_prompt_injection_resistance.py`'s `test_no_system_role_separation_used` updated to assert the new hardened behaviour
- No regression to existing test coverage

### ST-23 — Dependency license compliance scan
**Source:** BLG-SEC-32
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:** Scan run across `backend/requirements.txt` and `package.json`; any incompatible license flagged and resolved; Cybersecurity & Trust Lead sign-off

### ST-24 — Review baseline npm audit HIGH/CRITICAL findings (react-scripts toolchain)
**Source:** BLG-SEC-18
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:** Each of the 16 baseline advisory IDs in `docs/security/dependency_vuln_baseline.json` has either been fixed (removed from baseline) or has a recorded accept-risk decision (owner, rationale, review-by date)

### ST-25 — Add Telegram Bot Token to api_key_rotation_policy.md scope
**Source:** BLG-SEC-28
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- `api_key_rotation_policy.md` Scope table and Rotation Schedule include the Telegram Bot Token
- Credential-Specific Notes subsection added, cross-referencing `docs/security/api_key_security_register.md` §7

---

## EPIC-06 — API & Spec Debt Closure

**Maps to:** S2-06
**Owner:** API Contracts & Documentation Owner; Head of Specs Team

### ST-26 — Backfill api_changelog.md entries for v7.9–v8.4 endpoint additions
**Source:** BLG-SPEC-118
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:** `api_changelog.md` contains an entry for every new endpoint shipped in `v7.9` through `v8.4`, in descending version order

### ST-27 — Correct trade_plan.md §5.1's stale "Risk/Reward Notes" field anchor
**Source:** BLG-SPEC-129
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:** §5.1 anchor corrected from "Risk/Reward Notes" to "Early Exit Conditions"; Head of Specs Team sign-off

---

## EPIC-07 — Governance Correctness Fixes

**Maps to:** S2-07
**Owner:** Head of Specs Team; PMO Lead

### ST-28 — Correct CLAUDE.md §8's commit message template to match the enforced commit-format hook
**Source:** BLG-GOV-291
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- `CLAUDE.md` §8's commit message template matches what the enforced pre-commit hook actually accepts
- Head of Specs Team sign-off

### ST-29 — Assign an owning engine for .claude_current_state.json's prior_cycle field
**Source:** BLG-GOV-293
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- `prior_cycle` is written unconditionally by exactly one engine's terminal step, documented as that field's authoritative owner
- Confirmed correct at the next cycle transition (reads the cycle that closed immediately prior, not an older one)
- Head of Specs Team sign-off
