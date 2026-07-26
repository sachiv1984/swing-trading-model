**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-26
**Cycle:** 2026-07-24__release-v7.8
**Release:** v7.8
**Sprint Goal:** Ship all 12 v7.8 EPICs — the release/spend-visibility feature set and the engineering-hardening set — with every acceptance criterion met and QA sign-off recorded for each EPIC. (See `sprint_goal.md`.)
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

# Sprint Backlog — 2026-07-24__release-v7.8

## Merge Order

**EPIC merge sequence:** EPIC-04 → EPIC-03 → EPIC-09 → EPIC-07 → EPIC-08 → EPIC-12 → EPIC-10 → EPIC-02 → EPIC-01 → EPIC-05 → EPIC-06 → EPIC-11

**`execution_state.json` owner:** EPIC-04 (first in merge sequence). Every other EPIC branch must check for `execution_state.json` before creating its own — if present, append rather than overwrite.

**Shared files across EPICs** (full detail: `sprint_planning_notes.md ## Multi-EPIC Execution Notes`):

| Shared file | Owning EPIC | Must rebase after |
|---|---|---|
| `docs/specs/frontend/design_system.md` | EPIC-04 | EPIC-03 |
| `docs/reference/openapi.yaml` | EPIC-01 | EPIC-05, EPIC-06 |
| `docs/specs/api_contracts/*.md` | EPIC-01 | EPIC-05, EPIC-06 |
| `backend/routers/test.py` | EPIC-01 | EPIC-05, EPIC-06 |
| `src/pages/SystemStatus.js` | EPIC-01 | EPIC-05, EPIC-06 |
| `tests/e2e/system-status.spec.js` | EPIC-01 | EPIC-05, EPIC-06 |

---

## Sprint Scope

### EPIC-01 — In-app "what's new" panel for most recent release

**Maps to:** S2-01
**Owner:** Product Owner; Base44 Frontend Prompt Owner
**Estimated effort:** 2.0 days (M)
**Risk IDs:** RISK-01 (resolved — Design Gate Passed)
**Execution sequence:** 9

#### ST-01 — Build in-app "what's new" panel sourced from changelog.md

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous — new component against locked frontend spec (`docs/design/2026-07-24__release-v7.8/whats-new-panel/ux_spec.md`, `docs/specs/frontend/pages/dashboard.md` v3.2), per BLG-GOV-72 fast-path (c)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (first of the EPIC-01/05/06 shared-file cluster; owns `openapi.yaml`/`api_contracts`/`backend/routers/test.py`/`SystemStatus.js`/`system-status.spec.js` for this cluster)

**Notes:** Design Gate noted a backend dependency — new endpoint/aggregation not yet built to serve changelog data. Same-commit API contract entry (`docs/reference/openapi.yaml` + `docs/specs/api_contracts/*.md`) required per CLAUDE.md §2, and `backend/routers/test.py` + `SystemStatus.js` fallback count + `SC-SS-01b` must update in the same commit as the new route per CLAUDE.md §2.

**Staging-only ACs:** None — all 3 ACs (changelog parsing, auto-update on next release, empty/loading state) are verifiable via unit/integration test with fixture changelog content. Observable UI ACs require Playwright coverage or recorded staging sign-off before PR opens (CLAUDE.md §2) — confirm feasibility at kickoff (see `sprint_planning_notes.md`).

---

### EPIC-02 — Automated Telegram changelog digest after each release

**Maps to:** S2-02
**Owner:** Product Owner
**Estimated effort:** 1.0 days (S)
**Risk IDs:** None
**Execution sequence:** 8

#### ST-02 — Send Telegram digest of shipped items on post-ship closure

**Owner:** Product Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous — backend/infrastructure change reusing existing Telegram notification plumbing (shipped v2.4), no UI surface

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** No Design Gate dependency (Design Pre-Approved).

**Staging-only ACs:** None — Telegram API failure path is verifiable via a mocked/simulated failure in CI (unit test asserting Post-Ship Closure proceeds and the failure is logged, not fatal).

---

### EPIC-03 — Accessibility pass on v7.7 notification UX components

**Maps to:** S2-03
**Owner:** Head of UX & Design
**Estimated effort:** 1.0 days (S)
**Risk IDs:** RISK-01 (resolved — Design Gate Passed)
**Execution sequence:** 2

#### ST-03 — Contrast/focus-state accessibility pass on v7.7 notification UX

**Owner:** Head of UX & Design
**Estimated effort:** 1.0
**Delegation class:** autonomous — audit standard, scope, and findings-disposition rule (fix directly if trivial, else file follow-up) are fully locked in `docs/design/2026-07-24__release-v7.8/notification-accessibility-audit/decision_record.md`; only the audit-dependent findings themselves are determined at execution time, per that locked rule

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-04 (shared file: `docs/specs/frontend/design_system.md` — rebase after EPIC-04 merges)

**Notes:** Targets the v7.7 notification/digest surface consolidation (`BLG-FE-114`) and shared standing-alert component (`BLG-FE-120`).

**Staging-only ACs:** Contrast/focus-state visual fixes are observable UI changes — Playwright coverage or recorded staging sign-off required before PR opens (CLAUDE.md §2); confirm feasibility at kickoff. If any specific fix cannot be covered by Playwright, file the backlog item before the PR opens per CLAUDE.md §2 rather than leaving it as code-review-only.

---

### EPIC-04 — Dark-mode contrast audit across Base44-generated pages

**Maps to:** S2-04
**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 2.0 days (M)
**Risk IDs:** RISK-01 (resolved — Design Gate Passed)
**Execution sequence:** 1

#### ST-04 — Consolidated dark-mode contrast audit across shipped pages

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous — audit standard and consolidated-filing rule locked in `docs/design/2026-07-24__release-v7.8/base44-dark-mode-contrast-audit/decision_record.md` and `docs/specs/frontend/design_system.md` v1.4

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None (first to touch `design_system.md` this sprint — owns it for the cluster)

**Notes:** Findings filed as one consolidated batch, not per-page.

**Staging-only ACs:** Contrast fixes are observable UI changes — Playwright coverage or recorded staging sign-off required before PR opens (CLAUDE.md §2); confirm feasibility at kickoff.

---

### EPIC-05 — Monthly realized P&L CSV export

**Maps to:** S2-05
**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 1.0 days (S)
**Risk IDs:** RISK-01 (resolved — Design Gate Passed)
**Execution sequence:** 10

#### ST-05 — Add monthly CSV export option alongside existing tax-year export

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous — verbatim reuse of an existing export-control pattern (v7.6 `BLG-FEAT-79` tax-year export), locked spec (`docs/design/2026-07-24__release-v7.8/monthly-csv-export/ux_spec.md`, `docs/specs/frontend/pages/reports.md` v0.11)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-01 (shared files: `openapi.yaml`, `docs/specs/api_contracts/*.md`, `backend/routers/test.py`, `SystemStatus.js`, `system-status.spec.js` — rebase after EPIC-01 merges)

**Notes:** Design Gate noted a backend dependency — new endpoint/aggregation not yet built for monthly reconciliation. Same-commit API contract + endpoint test-suite + `SystemStatus.js`/`SC-SS-01b` update requirements per CLAUDE.md §2 apply, incrementing (not overwriting) whatever EPIC-01 left the fallback count/expected value at.

**Staging-only ACs:** None — reconciliation-against-tax-year-export AC is verifiable via unit/integration test with fixture trade data. Observable export-control UI requires Playwright coverage or recorded staging sign-off before PR opens (CLAUDE.md §2); confirm feasibility at kickoff.

---

### EPIC-06 — AI usage spend trend dashboard (Gemini/Claude, per release cycle)

**Maps to:** S2-06
**Owner:** FinOps & Resource Architect
**Estimated effort:** 2.0 days (M)
**Risk IDs:** RISK-01 (resolved — Design Gate Passed)
**Execution sequence:** 11

#### ST-06 — Add per-cycle AI spend trend chart to AI Usage & Costs view

**Owner:** FinOps & Resource Architect
**Estimated effort:** 2.0
**Delegation class:** autonomous — new chart in an existing settings card, locked spec (`docs/design/2026-07-24__release-v7.8/ai-spend-trend-chart/ux_spec.md`, `docs/specs/frontend/pages/settings.md` v1.6), existing chart styling conventions to follow

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** ST-05 (shared files: `openapi.yaml`, `docs/specs/api_contracts/*.md`, `backend/routers/test.py`, `SystemStatus.js`, `system-status.spec.js` — rebase after EPIC-05 merges)

**Notes:** Design Gate noted a backend dependency — new endpoint/aggregation not yet built to serve 6-cycle spend trend data from existing `gemini_audit_log`/Claude cost tracking (no new data collection). Same-commit contract/test-suite/`SystemStatus.js`/`SC-SS-01b` requirements apply, incrementing from whatever EPIC-05 left them at. Confirmed operational cost figure, not a strategy performance metric — no `strategy_rules.md §13` alignment step required (per `design_gate.md` Notes).

**Staging-only ACs:** None — chart data is sourced from existing logs, verifiable via fixture data in CI. Observable chart rendering requires Playwright coverage or recorded staging sign-off before PR opens (CLAUDE.md §2); confirm feasibility at kickoff.

---

### EPIC-07 — Scheduled rotation-and-audit cadence for third-party API keys

**Maps to:** S2-07
**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.0 days (S)
**Risk IDs:** None
**Execution sequence:** 4

#### ST-07 — Define rotation-and-audit schedule for all external API keys

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.0
**Delegation class:** autonomous — documentation/process only, extends existing `alpaca_key_rotation_policy.md` pattern

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** No Design Gate dependency (Design Not Applicable). May run before or after EPIC-08 for scheduling convenience only — not a hard constraint (both owned by Cybersecurity & Trust Lead).

**Staging-only ACs:** None — pure documentation artefact, verifiable by review.

---

### EPIC-08 — Rate-limiting review of public-facing endpoints

**Maps to:** S2-08
**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 2.0 days (M)
**Risk IDs:** RISK-04
**Execution sequence:** 5

#### ST-08 — Identify and remediate endpoints with no documented rate limit

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 2.0
**Delegation class:** autonomous — remediate-or-accept-risk rule is mechanical and bounded (RISK-04), no open-ended scope

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Extends `BLG-SEC-18`'s general audit, prioritising undocumented-limit endpoints. If findings exceed remaining capacity, accept-risk categorisation is the explicit fallback (RISK-04) — must be recorded, not silently skipped.

**Staging-only ACs:** None — rate-limit configuration and the endpoint list are verifiable via code/config review and CI tests.

---

### EPIC-09 — Shared retry/backoff decorator for external data calls

**Maps to:** S2-09
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.0 days (M)
**Risk IDs:** RISK-02
**Execution sequence:** 3

#### ST-09 — Extract shared retry/backoff decorator and migrate highest-traffic call site

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous — backend/infrastructure code with unit tests, no UI change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** RISK-02 bounds scope to proof-of-pattern on the single highest-traffic call site (Yahoo Finance or Alpaca, whichever is higher-traffic) — no full retrofit this cycle. Recommend running `pip-audit` (currently unavailable in `backend/.venv`) before touching these external call sites — see `sprint_planning_notes.md`.

**Staging-only ACs:** None — retry/backoff behaviour is verifiable via unit tests simulating failure/retry sequences.

---

### EPIC-10 — Flaky-test quarantine process for the Playwright suite

**Maps to:** S2-10
**Owner:** Director of Quality
**Estimated effort:** 2.0 days (M)
**Risk IDs:** None
**Execution sequence:** 7

#### ST-10 — Define and apply flaky-test quarantine mechanism

**Owner:** Director of Quality
**Estimated effort:** 2.0
**Delegation class:** autonomous — process/tooling definition (e.g. `test.fixme` + tracked follow-up), no external stakeholder input or novel UX decision required

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Apply to any currently-known flaky test in the Playwright suite at implementation time, if one exists.

**Staging-only ACs:** None — process definition and application are verifiable via review of the quarantine tag/mechanism and CI run.

---

### EPIC-11 — Contract tests for highest-traffic frontend/backend endpoints

**Maps to:** S2-11
**Owner:** Head of Engineering
**Estimated effort:** 2.0 days (M)
**Risk IDs:** RISK-03
**Execution sequence:** 12

#### ST-11 — Add pilot contract tests for 3 highest-traffic endpoints

**Owner:** Head of Engineering
**Estimated effort:** 2.0
**Delegation class:** delegated_decision — RISK-03: pilot endpoint selection (candidates: positions, trades, dashboard) has no telemetry-backed ranking on record and must be confirmed by Head of Engineering before implementation begins

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None (independent of the EPIC-01/05/06 shared-file cluster — different endpoints)

**Notes:** No HoST design session or equivalent artefact exists for the RISK-03 endpoint-selection decision (LL-v2.2-SP-01 advisory — see `sprint_planning_notes.md`). Confirm the 3 pilot endpoints at sprint kickoff before starting implementation.

**Staging-only ACs:** None — contract tests run and pass in CI by definition of the AC.

---

### EPIC-12 — Automated lint check for API contract `##` heading level

**Maps to:** S2-12
**Owner:** Head of Specs Team
**Estimated effort:** 1.0 days (S)
**Risk IDs:** None
**Execution sequence:** 6

#### ST-12 — Add CI lint step for API contract heading-level compliance

**Owner:** Head of Specs Team
**Estimated effort:** 1.0
**Delegation class:** autonomous — CI/CD tooling only, no UI change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Must catch the documented `###`-level silent-fail case from CLAUDE.md §2 (negative test with a deliberately-miscoded heading). Runs ahead of/alongside the existing OpenAPI Drift Detection gate.

**Staging-only ACs:** None — CI lint behaviour (including the negative test) is fully verifiable in CI.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 working-day-equivalent |
| Total estimated effort (in-scope) | ~19.0 days |
| Utilisation | ~68-79% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 12 EPICs / ST items are in scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Confirm 3 pilot endpoints for EPIC-11 (RISK-03) | Head of Engineering | No |
| Install and run `pip-audit` before EPIC-09 execution | Head of Engineering | No |
| Prompt change log gap: `sprint_planning_prompt.md` current v3.13, last logged v3.11→v3.12 | Head of Specs Team | No |
| File backlog item for `design_gate_prompt.md` STEP 5 root-pointer sync gap | Head of Specs Team | No |
| Confirm Playwright feasibility / arrange staging sign-off for EPIC-01/03/04/05/06 observable ACs at kickoff | Director of Quality | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-26 (see `sprint_goal.md`)
**Scope confirmed:** Confirmed — all 12 EPICs / ST items, no deferrals, no over-allocation
**Capacity confirmed:** Confirmed — ~19.0 days vs ~24-28 day ceiling, no WARN
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner
**Date:** 2026-07-26
