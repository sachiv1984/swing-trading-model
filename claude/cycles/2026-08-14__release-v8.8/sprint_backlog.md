**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-14
**Cycle:** 2026-08-14__release-v8.8
**Release:** v8.8
**Sprint Goal:** Close the two live P1 data-integrity gaps (stale screener refresh, stuck RISK OFF badge) and ship the full v8.8 debt-closure slice — 29 stories across 7 EPICs (backend hardening, frontend UX/dead-code cleanup, QA, security, spec, and governance debt) — within the confirmed ~24–28 day capacity band.
**Backlog Slice Source:** Original — `claude/cycles/2026-08-14__release-v8.8/stage4_backlog_slice.md`

# Sprint Backlog — 2026-08-14__release-v8.8

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06 → EPIC-07 (per `sprint_planning_notes.md ## Execution Sequence`)
- **`execution_state.json` owner:** EPIC-01
- **Shared files:** `docs/ops/api_performance_baseline.md` (EPIC-01 canonical, EPIC-02's ST-11 rebases after) and the backend market-regime code path feeding `risk_off_exit`/`check_market_regime()` (EPIC-01 canonical, EPIC-02's ST-07 rebases after) — full detail in `sprint_planning_notes.md ## Multi-EPIC Execution Notes`.

---

## Sprint Scope

### EPIC-01 — Live Data-Integrity & Scheduled Job Coverage

**Maps to:** S2-01
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 2.75 days
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Add scheduled overnight screener refresh workflow

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None
**Notes:** Live P1 data-integrity fix — screener results 24 days stale.
**Staging-only ACs:** None

---

#### ST-02 — Add scheduled nightly risk-off-alerts workflow (regime badge permanently stuck)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** None
**Notes:** Live P1 data-integrity fix — RISK OFF badge structurally stuck. Design Pre-Approved (`positions.md` v2.7 §Alerts Column, locked reference). Shares backend market-regime code path with EPIC-02 ST-07 — see Merge Order.
**Staging-only ACs:** None

---

#### ST-03 — Investigate nightly backtest import failure (Strategy Benchmark "data as of" line never populates)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** None
**Notes:** RISK-01 — root cause unconfirmed pending live GitHub Actions/Render log review; sequence first within this EPIC per release plan mitigation.
**Staging-only ACs:** Root-cause confirmation and fix verification depend on live GitHub Actions/Render log review — not reproducible in CI alone.

---

#### ST-04 — Add remaining pre-v4.6 endpoint (GET /v1beta1/news) to api_performance_baseline.md

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** None
**Notes:** Shares `docs/ops/api_performance_baseline.md` with EPIC-02 ST-11 — this EPIC owns the canonical version, see Merge Order.
**Staging-only ACs:** Live-measured p50/p95 latency entries required, consistent with existing measurement methodology — not CI-reproducible.

---

#### ST-05 — Add GET /trade-plans/tags to api_performance_baseline.md

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** None
**Notes:** Shares `docs/ops/api_performance_baseline.md` with EPIC-02 ST-11 — this EPIC owns the canonical version, see Merge Order.
**Staging-only ACs:** Live-measured p50/p95/max latency entries required — not CI-reproducible.

---

#### ST-06 — Live timing measurement for GET /analytics/strategy-version-comparison in api_performance_baseline.md

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** None
**Notes:** Row already exists (§34, added v8.4), scope narrowed to running the live measurement only. Shares `docs/ops/api_performance_baseline.md` — this EPIC owns the canonical version, see Merge Order.
**Staging-only ACs:** Requires ≥5 live staging samples to replace estimated values — not CI-reproducible.

---

### EPIC-02 — Backend Engineering Hardening

**Maps to:** S2-02
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 7.25 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-07 — Consolidate two divergent check_market_regime() implementations

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** None (must rebase onto `main` after EPIC-01 merges — see Merge Order)
**Notes:** Found while investigating EPIC-01 ST-02 (`BLG-OPS-145`). Shares backend market-regime code path with EPIC-01 ST-02.
**Staging-only ACs:** None

---

#### ST-08 — Position lifecycle state-transition history table

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

#### ST-09 — Link price_alerts to the trade they trigger (real alert-to-trade provenance)

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M (Product Owner-confirmed scope, 2026-08-14 — see below)
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None
**Notes:** RISK-02 — effort estimate was advisory/not fully scoped at release planning. **Product Owner confirmed at sprint planning (2026-08-14): full linkage scope proceeds (schema + backend + frontend)** — not trimmed to backend-only. Coordinate the frontend wiring half with the Frontend Specifications & UX Documentation Owner during execution. Reporting treatment (new `trade_origin` value vs. separate field) must be decided and documented as part of this story per its own AC.
**Staging-only ACs:** None

---

#### ST-10 — Populate si05_digest_log.telegram_message_id on successful send

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** XS
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

#### ST-11 — Add duration logging around POST /digest/si05/send's Telegram send call

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** XS
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** None (must rebase onto `main` after EPIC-01 merges — see Merge Order)
**Notes:** Updates `docs/ops/api_performance_baseline.md` §36 — shares this file with EPIC-01 (ST-04/05/06).
**Staging-only ACs:** Verification requires the next real invocation (scheduled cron run or manual `workflow_dispatch`) — not CI-reproducible.

---

#### ST-12 — Pre-Trade Research View query-latency budget review

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** S
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** None
**Notes:** Requires Head of Engineering sign-off.
**Staging-only ACs:** None

---

### EPIC-03 — Frontend UX & Dead-Code Cleanup

**Maps to:** S2-03
**Owner:** Frontend Specifications & UX Documentation Owner; Product Owner
**Estimated effort:** 3.00 days
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-13 — "What's New" panel surfaces user-facing benefit statements, not raw engineering copy

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** M
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None
**Notes:** Design Required — decision record: `docs/design/2026-08-14__release-v8.8/whats-new-user-benefit-copy/decision_record.md`. Frontend spec: `dashboard.md` v3.3 (§6A). Authoring-convention documentation update (RISK-03) is part of this story's own AC.
**Staging-only ACs:** None — Playwright-coverable / code-review-verifiable.

---

#### ST-14 — Research page trade plan status badge: fix raw snake_case for 3 of 6 statuses

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** XS
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None
**Notes:** Design Required — decision record: `docs/design/2026-08-14__release-v8.8/research-status-badge-single-source/decision_record.md`. Frontend spec: `research_view.md` v1.3 (§4.7).
**Staging-only ACs:** None — observable rendering AC, requires Playwright coverage or recorded staging run per CLAUDE.md §2 (not CI-only code review).

---

#### ST-15 — Ticker Universe page filtering by search, sector, and industry

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** S
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None (ST-17 depends on this completing first)
**Notes:** Design Required — new interaction flow, decision record: `docs/design/2026-08-14__release-v8.8/ticker-universe-search-sector-industry-filters/decision_record.md`. Frontend spec: `ticker_universe.md` v1.2 (§10). 200ms debounce is a named design decision (motion/timing-sensitive clause, `design_gate_prompt.md` §6). Introduces new user-facing filter controls — `execution_state.json` `epics.EPIC-03.test_scenarios = "pending — QA & Testing Owner to author before next sprint on this domain"` to be set at execution initialisation (LL-v2.0-P4-2).
**Staging-only ACs:** None — Playwright-coverable (filter interaction, debounce timing, reset behaviour).

---

#### ST-16 — Resolve PositionEntryModal.js dead-code/unreachable-mount-point status

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** XS
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`
**Dependencies:** None
**Notes:** Design gate already resolved the keep-or-kill decision to **removal** (Option B) — decision record: `docs/design/2026-08-14__release-v8.8/position-entry-modal-dead-code-removal/decision_record.md`. Implementation is deletion of `PositionEntryModal.js` and its stale `Layout.js` comment reference only — no new UX to build, hence autonomous despite EPIC-03's Design Required classification.
**Staging-only ACs:** None

---

#### ST-17 — Add Playwright coverage for Card and secondary-variant components when a live call site exists

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** XS
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`
**Dependencies:** ST-15 (must complete first — its "Clear filters" control is the first live call site for the `secondary` Badge variant)
**Notes:** `Card` component's own call-site gap (`BLG-FE-160`) remains open by design-gate decision — only the `secondary` Badge half is actionable this sprint.
**Staging-only ACs:** None — the AC is itself Playwright test authorship.

---

### EPIC-04 — Quality & Test-Coverage Debt

**Maps to:** S2-04
**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 3.00 days
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-18 — Field-population completeness audit for Arc 6 prerequisite fields

**Owner:** QA & Testing Owner
**Estimated effort:** S
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

#### ST-19 — Consolidated backend service-layer test-coverage report

**Owner:** QA & Testing Owner
**Estimated effort:** S
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

#### ST-20 — Test-environment parity check — local vs CI vs staging config drift

**Owner:** QA Lead
**Estimated effort:** S
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

#### ST-21 — backend/routers/test.py completeness re-audit

**Owner:** QA & Testing Owner
**Estimated effort:** S
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

### EPIC-05 — Security Hardening

**Maps to:** S2-05
**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 2.50 days
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-22 — Add system/user role separation to Claude thesis-generation prompts

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** S
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`
**Dependencies:** None
**Notes:** §13 boundary pre-check considered at design gate — no covering review required (non-functional hardening of an already-cleared call site, no new capability/content path/provider call).
**Staging-only ACs:** None

---

#### ST-23 — Dependency license compliance scan

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** S
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`
**Dependencies:** None
**Notes:** Requires Cybersecurity & Trust Lead sign-off.
**Staging-only ACs:** None

---

#### ST-24 — Review baseline npm audit HIGH/CRITICAL findings (react-scripts toolchain)

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** S
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`
**Dependencies:** None
**Notes:** 16 baseline advisory IDs each need a fix-or-accept-risk decision.
**Staging-only ACs:** None

---

#### ST-25 — Add Telegram Bot Token to api_key_rotation_policy.md scope

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** XS
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

### EPIC-06 — API & Spec Debt Closure

**Maps to:** S2-06
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Estimated effort:** 1.00 days
**Risk IDs:** RISK-06
**Execution sequence:** 6

#### ST-26 — Backfill api_changelog.md entries for v7.9–v8.4 endpoint additions

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** S
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`
**Dependencies:** None
**Notes:** Selected per Backlog Age Advisory — stale since v7.8.0.
**Staging-only ACs:** None

---

#### ST-27 — Correct trade_plan.md §5.1's stale "Risk/Reward Notes" field anchor

**Owner:** Head of Specs Team
**Estimated effort:** XS
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

### EPIC-07 — Governance Correctness Fixes

**Maps to:** S2-07
**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 1.00 days
**Risk IDs:** RISK-07
**Execution sequence:** 7

#### ST-28 — Correct CLAUDE.md §8's commit message template to match the enforced commit-format hook

**Owner:** Head of Specs Team
**Estimated effort:** XS
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

#### ST-29 — Assign an owning engine for .claude_current_state.json's prior_cycle field

**Owner:** Head of Specs Team
**Estimated effort:** XS
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`
**Dependencies:** None
**Notes:** RISK-07 — sequenced last; must not conflict with this cycle's own STEP 9 authoritative write to `.claude_current_state.json`. Governance prompt edit — CLAUDE.md §6 Governance File Edit Checklist applies (version bump, OPERATIONAL_GUIDE §14, prompt_change_log.md entry) if `release_planning_prompt.md` is the file amended to name the owner.
**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalent units |
| Total estimated effort (in-scope) | 20.50 days |
| Utilisation | ~73–85% (of band) |
| Over-allocation | No |

## Items Deferred This Sprint

None.

## Deferred Execution Blockers Accepted

*(omitted — `deferred_execution_blockers` was empty in the release plan)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Install `pip-audit` in the execution environment | PMO Lead / Head of Engineering | No |
| File a `BLG-OPS-*` story for the carried-forward `check_api_performance_baseline_drift.py` false-negative fix | PMO Lead | No |
| Coordinate ST-09's frontend wiring half with Frontend Specs & UX Documentation Owner during execution | Backend Engineering Patterns Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed 2026-08-14 (see `sprint_goal.md`)
**Scope confirmed:** Confirmed 2026-08-14 — 29 stories / 7 EPICs, including full-linkage scope for ST-09
**Capacity confirmed:** Confirmed 2026-08-14 — 20.50 days vs ~24–28 day band, no over-allocation
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-08-14
