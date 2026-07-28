**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-28
**Cycle:** 2026-07-28__release-v7.10
**Release:** v7.10
**Sprint Goal:** Materially reduce the platform's production risk surface — closing silent backend error-masking, hardening security posture (secrets scanning, rate-limit and exception hygiene), strengthening QA/CI infrastructure, correcting API contract debt, and clearing a first tranche of frontend technical debt — by delivering all 23 in-scope v7.10 hardening items within the confirmed capacity band.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

# Sprint Backlog — 2026-07-28__release-v7.10

## Sprint Scope

**Merge order:** EPIC-04 → EPIC-01 → EPIC-02 → EPIC-03 → EPIC-05 → EPIC-06 (see `sprint_planning_notes.md ## Execution Sequence`). `execution_state.json` owner: **EPIC-04**. No shared source files across EPICs beyond `execution_state.json` (see `sprint_planning_notes.md ## Multi-EPIC Execution Notes`).

---

### EPIC-04 — API Contract & Spec Debt Cleanup

**Maps to:** S2-13, S2-14, S2-15, S2-16
**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 2.75 days
**Risk IDs:** None
**Execution sequence:** 1

#### ST-13 — `position_endpoints.md` envelope claim doesn't match live `GET /positions` behaviour

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

#### ST-14 — `GET /positions` undocumented lifecycle fields

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

#### ST-15 — `trade_endpoints.md` JSON example omits documented fields

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

#### ST-16 — OpenAPI contract linter in CI for heading-level drift

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

### EPIC-01 — Backend Reliability & Error-Handling Hardening

**Maps to:** S2-01, S2-02, S2-03, S2-04
**Owner:** Backend Engineering Patterns Owner; Head of Backend Engineering
**Estimated effort:** 5.5 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-01 — Fix errors masked as HTTP 200 in portfolio_risk.py

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

#### ST-02 — Extend Alpaca backoff audit (BLG-BE-57) to Yahoo Finance, Gemini, and Claude call sites

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

#### ST-03 — Idempotency key pattern for state-mutating POST endpoints

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** None
**Notes:** RISK-02 — scope explicitly limited to an additive, opt-in dedup check (client-supplied key only); no change to existing request-handling behaviour when the key is absent.
**Staging-only ACs:** None

#### ST-04 — Deprecated table read-path audit

**Owner:** Head of Backend Engineering
**Estimated effort:** 1.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

---

### EPIC-02 — Security Hardening

**Maps to:** S2-05, S2-06, S2-07, S2-08
**Owner:** Cybersecurity & Trust Lead; Head of Engineering
**Estimated effort:** 5.5 days
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-05 — Secrets-scanning pre-commit/CI gate (gitleaks/trufflehog)

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

#### ST-06 — AI rate-limit bypass test

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** None
**Notes:** Any confirmed bypass must be filed as a P1/P0 security item per the story's own AC.
**Staging-only ACs:** None

#### ST-07 — Rate-limit audit on public-facing endpoints ahead of any future auth changes

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 2.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** None
**Notes:** Audit only; no implementation required unless a P0/P1 gap is found.
**Staging-only ACs:** None

#### ST-08 — Raw exception text returned in API error responses

**Owner:** Head of Engineering
**Estimated effort:** 1.5
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None
**Notes:** RISK-03 — touches ~44 call sites in `backend/main.py`; AC explicitly excludes safe 4xx messages from scope; QA to spot-check a 4xx sample.
**Staging-only ACs:** None

---

### EPIC-03 — QA & Test Infrastructure Hardening

**Maps to:** S2-09, S2-10, S2-11, S2-12
**Owner:** QA Lead; QA & Testing Owner; API Contracts & Documentation Owner
**Estimated effort:** 6.5 days
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-09 — Serve production build for Playwright E2E webServer instead of CRA dev server

**Owner:** QA Lead
**Estimated effort:** 1.5
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None
**Notes:** RISK-04 — land on a feature branch first; confirm the full 677-test suite passes against the production-served build in CI before merging; keep `npm start` as the local dev fallback.
**Staging-only ACs:** None

#### ST-10 — Red Flag Journal auth regression test

**Owner:** QA & Testing Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** None
**Notes:** Sequenced before ST-11 so the endpoint coverage audit accounts for this newly-added test (see `sprint_planning_notes.md ## Dependency Map`).
**Staging-only ACs:** None

#### ST-11 — Endpoint test suite coverage audit against all backend/routers/ files

**Owner:** QA & Testing Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** ST-10 (must complete first)
**Notes:** None
**Staging-only ACs:** None

#### ST-12 — Consumer-driven contract check: frontend API calls vs documented contracts

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** ST-13, ST-14, ST-15 (EPIC-04 — must complete first, per merge order)
**Notes:** None
**Staging-only ACs:** None

---

### EPIC-05 — Frontend Technical Debt & Accessibility

**Maps to:** S2-17, S2-18, S2-19, S2-20
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design; Head of Engineering
**Estimated effort:** 3.4 days
**Risk IDs:** RISK-01
**Execution sequence:** 5

#### ST-17 — Rewrite calendar.js against the react-day-picker v9+ API

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`
**Dependencies:** None
**Notes:** RISK-01 — Design Gate cleared via existing implementation as approved visual reference (component has zero live consumers); visual output must be preserved 1:1 under the new library API.
**Staging-only ACs:** AC "renders correctly, spot-checked" (visual rendering spot-check) — Playwright coverage or recorded staging sign-off required per CLAUDE.md §2.

#### ST-18 — `SystemStatus.js` `categorizeEndpoint()` missing branches

**Owner:** Head of Engineering
**Estimated effort:** 0.25
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`
**Dependencies:** None
**Notes:** None
**Staging-only ACs:** None

#### ST-19 — Consolidate StrategyBenchmark.js page header onto shared PageHeader component

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`
**Dependencies:** None
**Notes:** RISK-01 — implements the target state already documented in `strategy_benchmark.md` §2 (v0.4); no new design decision.
**Staging-only ACs:** AC "no visual regression beyond the intended consolidation" (visual rendering match) — Playwright coverage or recorded staging sign-off required per CLAUDE.md §2.

#### ST-20 — Keyboard navigation & focus-order audit

**Owner:** Head of UX & Design
**Estimated effort:** 2.0
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`
**Dependencies:** None
**Notes:** Audit only; any gaps found filed as separate follow-up items (own design gate applies then).
**Staging-only ACs:** None

---

### EPIC-06 — Governance Process Hardening

**Maps to:** S2-21, S2-22, S2-23
**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 2.25 days
**Risk IDs:** None
**Execution sequence:** 6

#### ST-21 — design_gate_prompt.md does not sync .claude_current_state.json root pointer on gate pass

**Owner:** Head of Specs Team
**Estimated effort:** 0.75
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`
**Dependencies:** None
**Notes:** Versioned per CLAUDE.md §6 Governance File Edit Checklist (version bump, OPERATIONAL_GUIDE §14 sync, prompt_change_log.md entry, same commit).
**Staging-only ACs:** None

#### ST-22 — Recent-rebalance recency advisory at roadmap STEP -1

**Owner:** Head of Specs Team
**Estimated effort:** 0.75
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`
**Dependencies:** None
**Notes:** Versioned per CLAUDE.md §6.
**Staging-only ACs:** None

#### ST-23 — Same-day scheduled-rebalance cycle_id collision handling

**Owner:** Head of Specs Team
**Estimated effort:** 0.75
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`
**Dependencies:** None
**Notes:** Versioned per CLAUDE.md §6.
**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 working-day-equivalent units |
| Total estimated effort (in-scope) | ~26.15 days midpoint (release plan figure; EPIC subtotal sum = 25.9d, see `sprint_capacity.md`) |
| Utilisation | ~93-109% |
| Over-allocation | No — intentional full-capacity fill per explicit user instruction (RISK-05) |

## Items Deferred This Sprint

None — all 23 items from the authoritative backlog slice entered the sprint.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Confirm sprint goal | Product Owner | Yes |
| Confirm sprint backlog Product Owner Sign-Off block | Product Owner | Yes |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Yes — confirmed as written 2026-07-28
**Scope confirmed:** Yes — all 23 items across 6 EPICs
**Capacity confirmed:** Yes — ~26.15d/~24-28d band, ~93-109% utilisation, no over-allocation
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-07-28
