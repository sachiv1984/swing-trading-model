**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-21
**Cycle:** 2026-08-21__release-v9.0
**Release:** v9.0
**Sprint Goal:** Close out the correctness and data-integrity follow-through surfaced directly by v8.9's own PR-review process — fixing the live nightly-backtest rebalance-date bug and the open-position breakeven-floor stop invariant gap — while hardening operational resilience (deploy-path and staging safeguards) and expanding QA and cost/capacity hygiene coverage across the full v9.0 backlog slice.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

# Sprint Backlog — 2026-08-21__release-v9.0

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 (matches execution sequence — see `sprint_planning_notes.md`).

**`execution_state.json` owner:** EPIC-01. All later-merging EPIC branches must check for its existence before creating their own version and append their section rather than overwrite.

**Shared files across EPICs:** None identified beyond `execution_state.json` (owner-EPIC rule above governs). `data_model.md` may be touched by EPIC-02 alone if ST-07's decision surfaces a schema change — no other EPIC expected to touch it this cycle; re-apply CLAUDE.md §8 if that changes.

## Sprint Scope

### EPIC-01 — AI Post-Trade Debrief & Backtest Correctness Follow-Through

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; AI Compliance & Governance Officer
**Estimated effort:** 4.00d
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Fix nightly backtest rebalance-date computation to exclude the current in-progress month

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.75d (S, ~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (must complete before ST-05)

**Notes:** Live production data-correctness bug (found 2026-08-21 investigating INTC/WDC trade behaviour) — leads capacity allocation per `release_plan.md`. RISK-01.

**Staging-only ACs:** None

---

#### ST-02 — Configure root/app logging so logger.info() calls actually reach Render's captured logs

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.50d (S, ~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** AC2 ("A real post-deploy production invocation confirms at least the `si05_digest_service.py` duration line is now captured in Render logs")

---

#### ST-03 — Decide "linked journal entries" data source for the AI Post-Trade Debrief

**Owner:** Product Owner (decision); Backend Engineering Patterns Owner (implementation, if any)
**Estimated effort:** 0.50d (S, ~0.5d, once decided)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** §13 pre-check covered by existing v8.9 ST-06 review (`docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`). Design Pre-Approved (PO-confirmed downgrade, see `design_gate.md`).

**Staging-only ACs:** None

---

#### ST-04 — Fix debrief-generation prompt's unverifiable cross-trade pattern language

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.75d (S, ~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** §13 pre-check covered by existing v8.9 ST-06 review (Condition 9 numeric cross-check).

**Staging-only ACs:** None

---

#### ST-05 — Consolidate backtest_rule_service.py's ported algorithm functions with production_strategy.py

**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 1.50d (M, ~1-2d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-01 (must complete first — same rebalance-date computation surface)

**Notes:** RISK-01 — verify against a fixed historical run before replacing either call site.

**Staging-only ACs:** None

---

### EPIC-02 — Live Risk-Management & Trade-Plan Data-Integrity Closure

**Maps to:** S2-02
**Owner:** Backend Engineering Patterns Owner; Product Owner; Frontend Specifications & UX Documentation Owner; Director of Quality
**Estimated effort:** 3.75d
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-06 — Audit and backfill open positions against the breakeven-floor stop invariant

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.75d (S, ~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None (sequence first within EPIC-02 per RISK-02 mitigation)

**Notes:** Closes the deferred v8.9 ST-01 AC from `BLG-BE-102`. Apply only via the existing, regression-tested `calculate_trailing_stop()` floor logic through the existing nightly recompute path — no bespoke one-off script. RISK-02 (High).

**Staging-only ACs:** AC1 ("Live-DB query confirms the count of open profitable positions with `current_stop < entry_price`, before and after correction")

---

#### ST-07 — Decide and apply treatment for trade_plans.setup_type="Other" conflating user-chosen-Other with never-classified

**Owner:** Product Owner
**Estimated effort:** 0.50d (S, ~0.5d)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Direct continuation of v8.9 ST-13's identical decision item — same downgrade rationale (`design_gate.md`).

**Staging-only ACs:** None

---

#### ST-08 — Add a lock around ensure_trade_plans_table()'s memoization flag

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.50d (S, ~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

---

#### ST-09 — Add down-migration rollback verification tests for the 5 most recent schema migrations

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 1.00d (S, ~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

---

#### ST-10 — Close the What-If Sizing Preview FX-rate reproducibility gap for US-market plans

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50d (S, ~0.5d)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Design Pre-Approved (PO-confirmed downgrade). Implementation outcome not yet chosen: (a) FX override field reusing the existing `PositionSizingWidget` pattern verbatim, or (b) a spec-wording-only fix with no UI change. If (a) is chosen: any frontend-visible change requires Playwright coverage or human staging sign-off per CLAUDE.md §2 — confirm before merge.

**Staging-only ACs:** None (both possible outcomes are CI-verifiable — (a) via Playwright, (b) via spec review)

---

#### ST-11 — Add Playwright coverage for UK-market position on current_trailing_stop_native

**Owner:** Director of Quality
**Estimated effort:** 0.50d (S, ~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

---

### EPIC-03 — Operational Resilience & Deploy-Path Safeguards

**Maps to:** S2-03
**Owner:** Infrastructure & Operations Owner; Director of Quality
**Estimated effort:** 5.90d
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-12 — Production database backup/restore drill

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.25d (S, ~0.5-2 days)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Requires deliberate execution against a live non-production infrastructure target — human-reviewable operational action.

**Staging-only ACs:** AC2 ("One full restore drill performed against a non-production target confirming the procedure works")

---

#### ST-13 — Automated staging smoke test on deploy/merge

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 2.00d (M, ~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** RISK-03 — confirm the check fails correctly on a deliberately-broken dry run before enabling as a blocking gate.

**Staging-only ACs:** AC5 ("Confirmed to fail correctly on a deliberately-broken staging deploy (dry run)")

---

#### ST-14 — Staging environment drift detector

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 2.00d (M, ~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** RISK-03. Covers both confirmed incident shapes (`BLG-OPS-82` missing-deploy; this item's own dashboard-only build-path-filter gate-clearing incident — see [[render_build_filters_gotcha]] memory).

**Staging-only ACs:** None (both incident-shape checks are automatable/CI-testable per the item's own AC)

---

#### ST-15 — Confirm production PUBLIC_URL is actually set in the Render dashboard

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15d (XS, <1h)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Requires confirming a live value in the Render dashboard — no code-level source of truth.

**Staging-only ACs:** AC1 ("Production `PUBLIC_URL` dashboard value confirmed one way or the other, documented in this item's resolution")

---

#### ST-16 — Add CI safeguard to catch future PUBLIC_URL/asset-path regressions on GitHub Pages deploy

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50d (S, ~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Traces to the 2026-08-21 GitHub Pages white-page incident and its `BLG-OPS-146` (v8.9 ST-16) remainder.

**Staging-only ACs:** None (deliberate local test is CI-reproducible)

---

### EPIC-04 — QA Coverage & Process Hardening

**Maps to:** S2-04
**Owner:** Director of Quality; QA Lead; QA & Testing Owner; Financial Reporting & Records Owner
**Estimated effort:** 8.25d
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-17 — Arc 5 QA protocol

**Owner:** QA Lead; Product Owner
**Estimated effort:** 2.00d (M, ~2 days)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Full Arc 5 flow protocol document + Playwright core-path coverage; explicit QA Lead + Product Owner sign-off required.

**Staging-only ACs:** None

---

#### ST-18 — Visual regression baseline snapshots (contrast-sensitive + chart-heavy components)

**Owner:** Director of Quality
**Estimated effort:** 2.00d (M, ~2 days)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Visual baseline capture requires human visual-correctness confirmation per CLAUDE.md's frontend visual-evidence rule.

**Staging-only ACs:** None (baseline capture itself is CI-executable; human confirmation is a code-review-equivalent step, not a live-system dependency)

---

#### ST-19 — R-multiple calculation regression test

**Owner:** QA & Testing Owner
**Estimated effort:** 1.25d (S, ~0.5-2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Locks v6.8 R-multiple FX spec's behaviour against known trade fixtures.

**Staging-only ACs:** None

---

#### ST-20 — Playwright coverage gap audit for Arc5ComplianceSection

**Owner:** QA Lead
**Estimated effort:** 1.00d (S, bare label — default applied)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** Gaps found must be filed as backlog items (per this item's own AC and CLAUDE.md §2).

**Staging-only ACs:** None

---

#### ST-21 — Standalone axe-core accessibility CI scan

**Owner:** QA & Testing Owner
**Estimated effort:** 1.00d (S, ~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

---

#### ST-22 — Publish backend test coverage report to PR comments

**Owner:** QA & Testing Owner
**Estimated effort:** 1.00d (S, ~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

---

### EPIC-05 — Backend Architecture & Cost/Capacity Hygiene

**Maps to:** S2-05
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; FinOps & Resource Architect
**Estimated effort:** 5.25d
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-23 — Backend service-layer boundary review

**Owner:** Head of Engineering
**Estimated effort:** 1.25d (S, ~0.5-2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

---

#### ST-24 — Database connection pool tuning review

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 1.25d (S, ~0.5-2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** RISK-05 — measure before adjusting, configuration-only change.

**Staging-only ACs:** AC1 ("Current concurrent connection usage measured and compared against the configured pool size")

---

#### ST-25 — Render hosting tier review

**Owner:** FinOps & Resource Architect
**Estimated effort:** 1.25d (S, ~0.5-2 days)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** Requires comparing live Render billing/usage data (external system) against confirmed limits — FinOps judgment call.

**Staging-only ACs:** AC1 ("Current Render service tier cost/limits compared against actual measured usage since v6.8")

---

#### ST-26 — Render hosting cost trend dashboard

**Owner:** FinOps & Resource Architect
**Estimated effort:** 1.00d (S, ~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** Sourced from existing, already-collected monthly review data.

**Staging-only ACs:** None

---

#### ST-27 — Quarterly dependency minor-version upgrade cadence policy

**Owner:** Head of Engineering
**Estimated effort:** 0.50d (S, ~0.5 day per quarter)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** Policy document requires Head of Engineering / FinOps stakeholder agreement before adoption.

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 working-day-equivalent units |
| Total estimated effort (in-scope) | 27.15d (27 items) |
| Utilisation | ~97-113% of band (near top, matches explicit PO "use full capacity" instruction) |
| Over-allocation | No (within confirmed band; upper-bound utilisation exceeds the 95% advisory buffer floor — see Minimum Capacity Buffer Floor Advisory in `sprint_capacity.md`, PO-acknowledged) |

## Items Deferred This Sprint

None. All 27 items in the authoritative backlog slice enter the sprint — total effort (27.15d) fits within the confirmed 24-28d capacity band.

## Deferred Execution Blockers Accepted

*(omitted — `deferred_execution_blockers` is empty in `state.json`)*

## Outstanding Actions at Planning Seal

None. No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders. No blocker-flagged outstanding actions.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed, 2026-08-21 — see `sprint_goal.md`
**Scope confirmed:** Confirmed, 2026-08-21 — all 27 items, 5 EPICs, full backlog slice
**Capacity confirmed:** Confirmed, 2026-08-21 — 27.15d within 24-28d band; buffer-floor advisory acknowledged, no trim (continuation of the release-planning "use full capacity" decision)
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-08-21
