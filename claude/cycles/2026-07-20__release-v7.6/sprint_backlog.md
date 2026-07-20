# Sprint Backlog — 2026-07-20__release-v7.6

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-20
**Cycle:** 2026-07-20__release-v7.6
**Release:** v7.6
**Sprint Goal:** Ship print/PDF export for WeeklyDigest and TradePlan (`BLG-FE-119`) and clear six ready backend/QA/documentation items to fully utilise this sprint's confirmed capacity. See `sprint_goal.md`.
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-04 → EPIC-02 → EPIC-03 → EPIC-05 → EPIC-06 → EPIC-07 → EPIC-08 (rationale: `sprint_planning_notes.md ## Execution Sequence`)
- **`execution_state.json` owner:** EPIC-01
- **Shared files across EPICs:** `backend/routers/*.py` (EPIC-04 canonical owner — audits/documents/lightly corrects response shapes across nearly all router files; later EPICs touching a router file must rebase onto `main` after EPIC-04 merges and conform to the documented envelope); `backend/services/signal_service.py` / `database.py` / `ai_service.py` (EPIC-08's new regression suite reads these — sequenced after EPIC-04 to avoid testing against a shape that changes underneath it). Full detail: `sprint_planning_notes.md ## Shared File Ownership Advisory`.

---

## Sprint Scope

### EPIC-01 — PDF / print-friendly export

**Maps to:** S2-01
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 days
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Add print/PDF export action to WeeklyDigest and TradePlan

**Owner:** Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 days
**Delegation class:** autonomous — new component against a locked frontend spec with confirmed Playwright feasibility (`BLG-GOV-72` fast-path (c)); Design Gate already resolved the placement decision (client-side `window.print()` + print stylesheet, per `design_gate.md`), locked specs exist (`docs/specs/frontend/pages/weekly_digest.md` v0.1, `trade_plan.md` v1.2). No further UX design decision required at execution.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** A "Print / Export PDF" action is added to both `WeeklyDigest.js` and `TradePlan.js`, implemented client-side via `window.print()` plus a dedicated print stylesheet that hides nav/sidebar chrome and formats page content for print/PDF output via the browser's native "Save as PDF" print destination.
- **Quality:** Playwright coverage confirms (a) the print/export action is present and clickable on both pages, (b) print-media emulation (`page.emulateMedia({ media: 'print' })`) shows the target content and confirms nav/sidebar elements are not rendered/visible in print mode.
- **Security:** N/A — no new data exposure; the action operates on already-rendered, already-authorised page content.
- **Verification:** Director of Quality confirms Playwright spec coverage for both Quality-AC scenarios; evidence recorded in `qa_evidence_EPIC-01.md`.

**Dependencies:** None

**Notes:** Anchor item. `execution_state.json` owner for this sprint.

**Staging-only ACs:** None — both observable ACs (action presence, print-mode chrome absence) are Playwright-coverable via media emulation; no staging-only evidence required.

---

### EPIC-02 — Regression suite baseline update

**Maps to:** S2-02
**Owner:** QA Lead
**Estimated effort:** 1.0 day
**Risk IDs:** RISK-02
**Execution sequence:** 3

#### ST-02 — Update regression suite baseline for BLG-FE-115-119 interaction surfaces

**Owner:** QA Lead
**Estimated effort:** 1.0 day
**Delegation class:** autonomous — documentation update, no UX change, no human decision required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Regression suite baseline document updated with new scenario entries covering `BLG-FE-115`–`BLG-FE-118` (already shipped v7.4/v7.5) interaction surfaces plus `BLG-FE-119`'s new print/export action (this cycle).
- **Quality:** Each new baseline entry cross-referenced against its corresponding Playwright spec file, including the new/updated spec covering ST-01's print action.
- **Security:** N/A — documentation-only change.
- **Verification:** Head of Specs Team confirms cross-references resolve to existing spec files; Director of Quality sign-off that the baseline is current.

**Dependencies:** ST-01 (must complete first — this item's AC requires cross-referencing ST-01's Playwright spec file, which does not exist until ST-01 is implemented)

**Notes:** Gate-triggered companion to EPIC-01 (gate fired: `BLG-FE-119` entered release scope).

**Staging-only ACs:** None — documentation cross-reference only.

---

### EPIC-03 — P&L export audit trail reconciliation

**Maps to:** S2-03
**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 2.0 days
**Risk IDs:** RISK-03
**Execution sequence:** 4

#### ST-03 — Reconcile realised P&L export against trade_plan closes

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 2.0 days
**Delegation class:** autonomous — backend reconciliation logic and a one-time production-data run; no UX change, no human decision beyond reviewing the run's own output.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Reconciliation logic specified and implemented comparing `trade_history` realised P&L rows against corresponding `trade_plans` closure data, flagging any mismatch.
- **Quality:** `[staging-only evidence]` Reconciliation run once against production data (read-only query); results recorded — either a clean pass, or specific mismatches filed as follow-up backlog items.
- **Security:** N/A — read-only reconciliation against existing authorised data; no new write surface.
- **Verification:** Financial Reporting & Records Owner confirms reconciliation logic and reviews results; Director of Quality sign-off on evidence recorded in `qa_evidence_EPIC-03.md`.

**Dependencies:** None

**Notes:** The production-data run is a one-time operator-executed audit deliverable, not a CI-reproducible test — flagged `[staging-only evidence]` per `stage4_backlog_slice.md §7`'s standard, not the CLAUDE.md frontend-testing gate (this item has no UI surface).

**Staging-only ACs:** AC-02 (reconciliation run against live production data — CI cannot reproduce; must be executed directly against production and results recorded in QA evidence).

---

### EPIC-04 — Backend error-response envelope standardisation

**Maps to:** S2-04
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.0 days
**Risk IDs:** RISK-04
**Execution sequence:** 2

#### ST-04 — Standardise error-response envelope across all routers

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.0 days
**Delegation class:** autonomous — audit and documentation of existing backend behaviour; no UX change, no human decision required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Audit of current error-response shapes across all `backend/routers/*.py` files completed; canonical error-response envelope (status/message/detail fields) documented in `backend_engineering_patterns.md`.
- **Quality:** Any non-conforming endpoints identified and filed as follow-up backlog items (not fixed in this item's scope unless trivial); audit confirmed to cover every router file.
- **Security:** N/A — audit/documentation of existing behaviour; any trivial fix applied must not alter a response shape relied on by existing frontend error handling without a corresponding frontend check.
- **Verification:** Backend Engineering Patterns Owner confirms audit completeness and canonical envelope documentation; Director of Quality sign-off.

**Dependencies:** None

**Notes:** Sequenced early (execution position 2) — this item's audit touches nearly every `backend/routers/*.py` file. Later EPICs modifying a router file (notably EPIC-07 if it adds an endpoint, and EPIC-08's regression suite reading `signal_service.py`) are sequenced after this EPIC merges. See `sprint_planning_notes.md ## Shared File Ownership Advisory`.

**Staging-only ACs:** None — audit and documentation, fully reviewable without live-environment dependency.

---

### EPIC-05 — OpenAPI-derived Playwright fixture library

**Maps to:** S2-05
**Owner:** QA & Testing Owner
**Estimated effort:** 2.0 days
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-05 — Build shared mock payload fixture library from openapi.yaml

**Owner:** QA & Testing Owner
**Estimated effort:** 2.0 days
**Delegation class:** autonomous — test tooling/infrastructure; no UX change, no human decision required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** A shared mock-payload fixture library built, deriving mock response shapes directly from `docs/reference/openapi.yaml`, covering at minimum the endpoints touched by `BLG-SPEC-95`'s scope.
- **Quality:** Fixture library documented as the preferred pattern for new Playwright tests; at least one existing or new Playwright spec updated to consume the shared fixtures as a working example.
- **Security:** N/A — test tooling only; no production code path affected.
- **Verification:** QA & Testing Owner confirms fixture shapes match `openapi.yaml` schemas (per `shared_standards.md §18` mock advisory — no flattening of nested objects); Director of Quality sign-off.

**Dependencies:** None

**Notes:** Useful precursor for EPIC-07's Quality AC (combined-total correctness against mocked fixture data) if sequenced first — however EPIC-07 is sequenced after EPIC-04 for the endpoint-conformance reason above; EPIC-07 may still consume EPIC-05's fixtures once both have merged, or use ad hoc mocks if EPIC-05 has not yet merged at EPIC-07's execution time.

**Staging-only ACs:** None — test tooling, fully CI-verifiable.

---

### EPIC-06 — Nightly batch-job idempotency audit

**Maps to:** S2-06
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.0 days
**Risk IDs:** RISK-06
**Execution sequence:** 6

#### ST-06 — Audit nightly batch jobs for idempotency risk

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.0 days
**Delegation class:** autonomous — backend audit of existing jobs; no UX change, no human decision required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** `daily-snapshot.yml`'s three jobs (position analysis, portfolio snapshot, signal generation) plus the nightly backtest import audited for idempotency — does re-running produce identical output given identical input state, or does it silently accumulate drift.
- **Quality:** Findings documented per job; any additional non-idempotency risks found filed as follow-up backlog items; audit explicitly cross-references `BLG-BE-59`/`BLG-BE-60` as the confirmed instance of this pattern.
- **Security:** N/A — audit/documentation only.
- **Verification:** Backend Engineering Patterns Owner confirms audit completeness; Director of Quality sign-off.

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — audit and documentation, no live-environment dependency beyond reading existing job history/config.

---

### EPIC-07 — Consolidated monthly AI cost view

**Maps to:** S2-07
**Owner:** FinOps & Resource Architect
**Estimated effort:** 2.0 days
**Risk IDs:** RISK-01
**Execution sequence:** 7

#### ST-07 — Add consolidated Gemini + Claude monthly cost summary

**Owner:** FinOps & Resource Architect
**Estimated effort:** 2.0 days
**Delegation class:** autonomous — new section against a locked frontend spec with confirmed Playwright feasibility (`BLG-GOV-72` fast-path (c)); Design Gate resolved the placement decision (Settings §6 "AI Usage & Costs", read-only, per `design_gate.md`), locked spec exists (`docs/specs/frontend/pages/settings.md` v1.4).

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** A consolidated monthly AI cost summary added to Settings §6 "AI Usage & Costs" (read-only) — showing Gemini and Claude costs plus a combined total for the current month. If no existing read endpoint exposes a combined figure, a new backend endpoint must be added, with the same-commit OpenAPI contract entry, `docs/specs/api_contracts/` `## METHOD /path` heading, and `backend/routers/test.py` registration per CLAUDE.md §2.
- **Quality:** Playwright coverage confirms (a) the new §6 section renders with both providers' costs and a combined total, (b) the displayed combined total equals the sum of the two per-provider source figures (verified against mocked/fixture API data).
- **Security:** N/A — read-only display of existing cost data already tracked server-side; no new data collection.
- **Verification:** FinOps & Resource Architect confirms combined-total correctness against the two source calculations; Director of Quality sign-off with Playwright evidence in `qa_evidence_EPIC-07.md`.

**Dependencies:** None (sequencing choice, not a hard dependency — see Notes)

**Notes:** Sequenced after EPIC-04 so that, if this item requires a new backend endpoint, it conforms to the freshly-merged error-envelope standard rather than needing a follow-up rebase. Confirm at execution kickoff whether `gemini_audit_log` / `POST /ai/check-daily-cost` already expose enough data for a client-side combine, or whether a new endpoint is required (outstanding action in `sprint_planning_notes.md`).

**Staging-only ACs:** None — both observable ACs (rendering, combined-total correctness) are Playwright-coverable with mocked/fixture API data.

---

### EPIC-08 — Ticker/market input sanitisation regression suite

**Maps to:** S2-08
**Owner:** Director of Quality; Backend Engineering Patterns Owner
**Estimated effort:** 1.5 days
**Risk IDs:** RISK-08
**Execution sequence:** 8

#### ST-08 — Add standing regression suite for ticker/market input sanitisation

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 1.5 days
**Delegation class:** autonomous — new pytest suite against existing, already-fixed code paths; no UX change, no human decision required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** A standing pytest regression suite added covering all 4 previously-vulnerable paths (`create_signal`, `create_rebalance_exit_signal`, `update_signal`, AI chat `context_opts.ticker`), consolidating `BLG-SEC-01`/`BLG-SEC-02` test cases (injection strings, trailing-newline bypass, invalid ticker/market values).
- **Quality:** Suite runs in CI on every PR touching `backend/services/signal_service.py`, `database.py`, or `ai_service.py` (CI workflow trigger path configured accordingly).
- **Security:** Confirms no regression of the `BLG-SEC-01`/`BLG-SEC-02` injection/validation fixes; the suite itself is a standing security regression control.
- **Verification:** Director of Quality sign-off required (named explicitly in the backlog AC); Backend Engineering Patterns Owner confirms CI trigger path configuration.

**Dependencies:** None (sequencing choice — see Notes)

**Notes:** Sequenced after EPIC-04 to avoid writing regression assertions against error-response shapes in `signal_service.py` / `database.py` / `ai_service.py` that change underneath it mid-sprint.

**Staging-only ACs:** None — CI-run pytest suite, fully automatable.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days |
| Total estimated effort (in-scope) | ~14.0 days midpoint |
| Utilisation | ~50–58% |
| Over-allocation | No |

## Items Deferred This Sprint

None.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|----------|
| Backfill `prompt_change_log.md` entries for `sprint_planning_prompt.md`, `shared_standards.md`, `release_planning_prompt.md` | Head of Specs Team | No |
| Confirm at EPIC-07 execution kickoff whether a new backend endpoint is required for the consolidated cost view | FinOps & Resource Architect; Head of Engineering | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed — all 8 EPICs / 8 ST items
**Capacity confirmed:** Confirmed — ~14.0 days midpoint of ~24–28 days capacity, no over-allocation
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-07-20
