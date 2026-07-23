# Sprint Backlog — 2026-07-21__release-v7.7

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-23
**Cycle:** 2026-07-21__release-v7.7
**Release:** v7.7
**Sprint Goal:** Ship the four design-gated Strategy Intelligence & Notification UX items and clear seven ready capacity-fill items to fully utilise this sprint's confirmed capacity. See `sprint_goal.md`.
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-06 → EPIC-07 → EPIC-09 → EPIC-10 → EPIC-05 → EPIC-08 → EPIC-11 (rationale: `sprint_planning_notes.md ## Execution Sequence`)
- **`execution_state.json` owner:** EPIC-01
- **Shared files across EPICs:** `docs/reference/openapi.yaml` / `docs/specs/api_contracts/*` (EPIC-01 adds `compliance_rate` to the strategy comparison contract; EPIC-02 adds `since_days`/`read` params to the Notification Feed endpoint — EPIC-02 must rebase onto `main` after EPIC-01 merges); `design_system.md` (EPIC-04 sole owner — Standing Alert component transcription); nightly backtest job surface (EPIC-09 idempotency audit, then EPIC-10 monitoring/alerting — hard dependency, not just shared-file). Full detail: `sprint_planning_notes.md ## Shared File Ownership Advisory`.

---

## Sprint Scope

### EPIC-01 — SI-04 Strategy Version Comparison

**Maps to:** S2-01
**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 6.5 days
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 1

#### ST-01 — Build SI-04 strategy-version performance comparison view

**Owner:** Head of Engineering
**Estimated effort:** 6.5 days
**Delegation class:** autonomous — new comparison view built against a locked frontend spec (`docs/specs/frontend/pages/strategy_benchmark.md` v0.4) and design artefact (`docs/design/2026-07-21__release-v7.7/si04-strategy-version-comparison/ux_spec.md`), Design Gate cleared (`BLG-GOV-72` fast-path (c)). The `compliance_rate` sourcing sub-decision is a scoped question within implementation, not a blocker to starting work — tracked as an outstanding action (mirrors the `2026-07-20__release-v7.6` EPIC-07 precedent).

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** User can select two `strategy_rules.md` versions and see a side-by-side performance comparison for trades executed under each, surfaced as a new dedicated comparison view (per `ux_spec.md §2` — the "dedicated comparison view" alternative, avoiding a pull-in of out-of-scope `BLG-FE-59`). Comparison includes win rate, average R, and compliance rate per version. No trade-volume gate applies (PO decision, `decisions--2026-07-21__release-v7.7.md`). MVP slice is bounded to these three metrics only — no stretch scope (RISK-01 mitigation).
- **Quality:** Playwright coverage confirms (a) the version-selector UI functions and produces a side-by-side render, (b) all three required metrics display correctly for both selected versions using mocked/fixture data conforming to `strategy_version_comparison_contract.md`.
- **Security:** N/A — read-only display of already-authorised trade history data; no new write surface.
- **Verification:** Head of Engineering confirms backend metric calculation correctness; Director of Quality sign-off with Playwright evidence in `qa_evidence_EPIC-01.md`. Strategy Rules & System Intent Owner must confirm the `compliance_rate` sourcing formula (journal-completion-rate vs. Arc 5 composite score) before the contract's 0.1.0→0.2.0 update lands — outstanding action, not a seal blocker.

**Dependencies:** None

**Notes:** Largest single item (RISK-01) — sequenced first among design-gated items per `stage4_backlog_slice.md`'s own sequencing note. `execution_state.json` owner for this sprint. API contract gap (`compliance_rate` field missing from `strategy_version_comparison_contract.md` v0.1.0) must be resolved in the same commit as the contract update, per CLAUDE.md §2.

**Staging-only ACs:** None — both observable ACs (selector UI, metric rendering) are Playwright-coverable with mocked/fixture data once contract v0.2.0 lands.

---

### EPIC-02 — Consolidate notification/digest surfaces

**Maps to:** S2-02
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-02 — Remove nav duplication and unify digest/notification concepts

**Owner:** Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 days
**Delegation class:** autonomous — modification of existing, fully-specified UI against 3 locked frontend specs from Design Gate (`navigation.md` v1.4, `notifications.md` v0.5, `weekly_digest.md` v0.2), per `BLG-GOV-72` fast-path (c). The real `Layout.js` `NAV_GROUPS` bug (Alerts/Notifications both routing to `page: "notifications"`) was independently confirmed during the Design Gate audit, giving execution a concrete, unambiguous starting point.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** No two nav entries route to the same page without a visual indicator they're the same (fixes the confirmed `Layout.js` `NAV_GROUPS` "Alerts"/"Notifications" duplication); Weekly Digest is discoverable from the same nav grouping/tab bar as Alerts/Notifications; Weekly Digest's alert-count values link to the corresponding filtered notification history view; "Daily Portfolio Summary" (notification preference) and "Weekly Digest" (page) concepts unified or clearly differentiated. Notification Feed endpoint (`GET /notifications`) gets 2 new optional query params (`since_days`, `read`) to support the deep-links, same-commit OpenAPI/contract update per CLAUDE.md §2.
- **Quality:** Playwright coverage confirms (a) Alerts and Notifications nav entries no longer silently duplicate, (b) Weekly Digest appears in the same nav grouping as Alerts/Notifications, (c) clicking an alert-count value on Weekly Digest navigates to the correctly-filtered notification history view.
- **Security:** N/A — navigation/UX restructuring and additive read-only query params; no new data exposure.
- **Verification:** Director of Quality sign-off with Playwright evidence in `qa_evidence_EPIC-02.md`; Frontend Specs & UX Documentation Owner confirms alignment with the 3 locked specs.

**Dependencies:** None (sequencing choice — see Notes)

**Notes:** Sequenced after EPIC-01 so its own `openapi.yaml`/contract touch rebases cleanly onto EPIC-01's, per Shared File Ownership Advisory.

**Staging-only ACs:** None — all three observable ACs are Playwright-coverable.

---

### EPIC-03 — Confirm AiDailyBriefing light-theme rendering

**Maps to:** S2-03
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** 0.75 days
**Risk IDs:** RISK-02
**Execution sequence:** 3

#### ST-03 — Staging check and fix AiDailyBriefing light-theme contrast

**Owner:** Head of UX & Design
**Estimated effort:** 0.75 days
**Delegation class:** autonomous — verification pass against an already-established light/dark token convention (Design Pre-Approved, downgraded from default Design Required at Design Gate; `dashboard.md` §5 v3.1 locked spec unchanged). The staging check itself is the AC; handled via the Staging-only ACs field, not a distinct delegation class — mirrors the `2026-07-20__release-v7.6` EPIC-03 production-reconciliation-run precedent.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Staging check performed against `AiDailyBriefing.js`/`Section` light-theme rendering; if fail, explicit light-mode class pairs added (e.g. `bg-white dark:bg-slate-900`) and verified in both themes; if pass, item closed with staging evidence, no code change needed.
- **Quality:** `[staging-only evidence]` Staging check performed and result (pass/fail) recorded with evidence (screenshot or equivalent) for whichever outcome occurs.
- **Security:** N/A — CSS/rendering only, no data exposure change.
- **Verification:** Head of UX & Design confirms staging check evidence; Director of Quality sign-off recorded in `qa_evidence_EPIC-03.md` with staging date.

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** AC-01 (staging check performed and result recorded — CI cannot execute a live-rendering visual check; must be executed directly against staging, with a fix-and-reverify pass if the result is fail).

---

### EPIC-04 — Shared toast/notification primitive for alert-style UI

**Maps to:** S2-04
**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 2.0 days
**Risk IDs:** RISK-02, RISK-03
**Execution sequence:** 4

#### ST-04 — Build shared "standing alert" component distinct from transient toast

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 2.0 days
**Delegation class:** autonomous — new shared component built against a locked design artefact (`docs/design/2026-07-21__release-v7.7/standing-alert-component/ux_spec.md`), Design Gate cleared, per `BLG-GOV-72` fast-path (c). `design_system.md` transcription is a known execution-time step (v7.5 command-palette precedent, confirmed applicable in `design_gate.md` Notes).

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Component built and documented in `design_system.md` (target v1.2→v1.3); at least one integration point identified for `BLG-FE-116`'s future implementation, per locked `ux_spec.md`.
- **Quality:** Playwright coverage confirms the component renders correctly and is visually/behaviourally distinct from existing transient toast notifications (persistence/dismissal behaviour, not auto-dismiss).
- **Security:** N/A — new UI primitive, no data exposure.
- **Verification:** Base44 Frontend Prompt Owner confirms `design_system.md` transcription; Director of Quality sign-off with Playwright evidence in `qa_evidence_EPIC-04.md`.

**Dependencies:** None

**Notes:** Sole owner of `design_system.md` this sprint (see Shared File Ownership Advisory). Enabler for `BLG-FE-116` (out of this release's scope, RISK-03) — no mitigation required this cycle; build to spec regardless of the consuming feature's own scheduling.

**Staging-only ACs:** None — component rendering/behaviour is Playwright-coverable.

---

### EPIC-05 — Investigate UX nudge to accelerate SI-02 trade-count gate

**Maps to:** S2-05
**Owner:** Product Owner
**Estimated effort:** 2.0 days
**Risk IDs:** None
**Execution sequence:** 9

#### ST-05 — Review nudge feasibility for SI-02 gate acceleration

**Owner:** Product Owner
**Estimated effort:** 2.0 days
**Delegation class:** autonomous — investigation and recommendation-drafting is engine-executable analytical work; Design Not Applicable confirmed at Design Gate (investigation output only, no shipped UI) — no HoST design session required (`LL-v2.2-SP-01` N/A).

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Review completed assessing whether a lightweight in-app nudge would meaningfully accelerate SI-02 gate clearance, given `BLG-FE-109` has been in production a full sprint cycle (shipped v7.3, 2026-07-16); review references the SI-02 gate's live re-check history (9 consecutive byte-identical NOT MET readings since 2026-07-12, per `run_manifest.md`).
- **Quality:** Recommendation recorded — either a nudge feature proposed with scope sketch, or an explicit "no action — time-gated only" conclusion, with supporting rationale.
- **Security:** N/A — investigation/documentation output, no shipped UI or data surface.
- **Verification:** Product Owner reviews and confirms the recommendation.

**Dependencies:** None

**Notes:** No Design Gate dependency (investigation output, no shipped UI).

**Staging-only ACs:** None — no UI surface.

---

### EPIC-06 — CI curl response validation (daily-snapshot.yml)

**Maps to:** S2-06
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.25 days
**Risk IDs:** None
**Execution sequence:** 5

#### ST-06 — Add response validation to daily-snapshot.yml curl calls

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.25 days
**Delegation class:** autonomous — CI/CD workflow change, fully specified, no UX, no human decision required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** `--fail` (or explicit status/body validation) added to all three curl invocations (Run Position Analysis, Create Portfolio Snapshot, Generate Signals) in `daily-snapshot.yml`.
- **Quality:** A broken write path now surfaces as a failed CI run rather than a false-green status, confirmed via a simulated failure (e.g. temporarily pointing at an invalid endpoint); other workflows posting to business endpoints audited for the same gap, confirming `backtest.yml`'s existing Python status-code validation is sufficient.
- **Security:** N/A — CI workflow hardening only.
- **Verification:** Infrastructure & Operations Owner confirms simulated-failure test and audit completeness; Director of Quality sign-off.

**Dependencies:** None

**Notes:** P1 — a 3-releases-overdue CI correctness gap (per `cycle_summary.md`).

**Staging-only ACs:** None — CI-verifiable.

---

### EPIC-07 — PT-04 §13 compliance review (retroactive)

**Maps to:** S2-07
**Owner:** Head of Specs Team
**Estimated effort:** 0.5 days
**Risk IDs:** None
**Execution sequence:** 6

#### ST-07 — Run retroactive §13 compliance review against shipped PT-04

**Owner:** Head of Specs Team
**Estimated effort:** 0.5 days
**Delegation class:** autonomous — governance/documentation review against existing shipped code, no UI change, no external stakeholder input required beyond the named sign-off (mirrors the `2026-07-20__release-v7.6` EPIC-08 "named sign-off, still autonomous" precedent). Design Not Applicable confirmed at Design Gate — no HoST design session required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** §13 checklist run against PT-04's shipped implementation (Setup Quality Score scoring algorithm + API endpoint).
- **Quality:** PASS/FAIL determination documented, with any binding conditions recorded.
- **Security:** N/A — governance/documentation review of already-shipped code; any binding-condition code change is out of this item's own scope and would be filed as a follow-up.
- **Verification:** Sign-off recorded by Head of Specs Team (named explicitly in backlog AC).

**Dependencies:** None

**Notes:** P1 — overdue §13 review, explicitly flagged for pickup at this cycle (per `cycle_summary.md`).

**Staging-only ACs:** None — review of existing shipped code and its own documentation, no live-environment dependency.

---

### EPIC-08 — numpy-scalar regression coverage for create_rebalance_exit_signal

**Maps to:** S2-08
**Owner:** QA & Testing Owner
**Estimated effort:** 0.5 days
**Risk IDs:** None
**Execution sequence:** 10

#### ST-08 — Add automated regression test for numpy-scalar handling

**Owner:** QA & Testing Owner
**Estimated effort:** 0.5 days
**Delegation class:** autonomous — backend/test-only regression coverage, fully specified, no UX, no decision required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Automated test added confirming `create_rebalance_exit_signal` (`backend/database.py`) safely handles numpy scalar inputs via `decimal_to_float()` upstream.
- **Quality:** Test guards against recurrence of the PR #971 defect class (numpy≥2.0 scalar `repr()` reaching a raw psycopg2 INSERT); runs in CI on every PR touching `backend/database.py`.
- **Security:** N/A — test-only change, no production code path altered beyond the guarded function's existing behaviour.
- **Verification:** QA & Testing Owner confirms test coverage and CI trigger path; Director of Quality sign-off.

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — CI-run pytest, fully automatable.

---

### EPIC-09 — Nightly backtest job idempotency check

**Maps to:** S2-09
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 1.0 day
**Risk IDs:** None
**Execution sequence:** 7

#### ST-09 — Verify nightly backtest job is safe against double-run/retry

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 1.0 day
**Delegation class:** autonomous — backend audit/test; filing a follow-up backlog item for any gap found is engine-executable (via `/backlog-add`), no human decision required mid-task.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Idempotency confirmed by test or code review — a retry or manual re-trigger must not produce duplicate or divergent results.
- **Quality:** Any gap found filed as a P1/P2 correctness item per its severity (via `/backlog-add`), with the specific failure mode documented.
- **Security:** N/A — backend audit/test; a found gap could itself be a data-integrity risk, tracked via the filed item's own severity.
- **Verification:** Backend Engineering Patterns Owner confirms audit/test completeness; Director of Quality sign-off.

**Dependencies:** None (must complete before EPIC-10 — see Notes)

**Notes:** Sequenced before EPIC-10 (monitoring/alerting should observe the idempotency-audited version of the job, not a pre-audit baseline). Sole owner of the nightly backtest job surface alongside EPIC-10 — see Shared File Ownership Advisory.

**Staging-only ACs:** None — audit/test against existing job code and history, no live-environment dependency beyond reading existing state.

---

### EPIC-10 — Nightly backtest job monitoring/alerting

**Maps to:** S2-10
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** 1.5 days
**Risk IDs:** None
**Execution sequence:** 8

#### ST-10 — Add monitoring/alerting for nightly backtest failures or anomalies

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.5 days
**Delegation class:** autonomous — monitoring/alerting implementation and simulated-failure test; no UX, no human decision required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Monitoring/alerting mechanism added for nightly backtest job failures or output anomalies.
- **Quality:** Confirmed to fire on a simulated failure/anomaly.
- **Security:** N/A — observability addition, no new data exposure.
- **Verification:** Infrastructure & Operations Owner confirms the simulated-failure trigger test; Head of Engineering sign-off.

**Dependencies:** ST-09 (must complete first — see Dependency Map)

**Notes:** Consumes EPIC-09's audit findings.

**Staging-only ACs:** None — simulated-failure trigger is engine/CI-executable.

---

### EPIC-11 — Automate endpoint-count drift check (CLAUDE.md §2)

**Maps to:** S2-11
**Owner:** QA & Testing Owner
**Estimated effort:** 2.0 days
**Risk IDs:** None
**Execution sequence:** 11

#### ST-11 — Add CI lint step for router-decorator vs. SystemStatus.js fallback count

**Owner:** QA & Testing Owner
**Estimated effort:** 2.0 days
**Delegation class:** autonomous — CI lint tooling; fully specified, no UX, no decision required.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Structured AC (Technical / Quality / Security / Verification):**
- **Technical:** Lint step added to `quality_gate.yml` counting `@router` decorators across `backend/routers/` vs. the hardcoded fallback constant in `SystemStatus.js`.
- **Quality:** Fails on a synthetic mismatch test case; passes on current repository state.
- **Security:** N/A — CI tooling only.
- **Verification:** QA & Testing Owner confirms both the synthetic-failure and current-state-pass cases; Director of Quality sign-off.

**Dependencies:** None

**Notes:** Sequenced last as a housekeeping capstone. If EPIC-01 or EPIC-02 end up adding a new backend endpoint this sprint, that EPIC's own commit — not this one — must update `SystemStatus.js`'s fallback count and `SC-SS-01b` (per CLAUDE.md §2; see Shared File Ownership Advisory).

**Staging-only ACs:** None — CI-verifiable.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days |
| Total estimated effort (in-scope) | ~19.5 days midpoint |
| Utilisation | ~70–81% |
| Over-allocation | No |

## Items Deferred This Sprint

None.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|----------|
| Confirm `compliance_rate` sourcing formula for `strategy_version_comparison_contract.md` before/during EPIC-01 execution | Strategy Rules & System Intent Owner | No |
| Confirm at EPIC-01/EPIC-02 execution kickoff whether either item requires a genuinely new backend endpoint; apply same-commit CLAUDE.md §2 requirements if so | Head of Engineering | No |
| Backfill `prompt_change_log.md` entries for `sprint_planning_prompt.md`, `shared_standards.md`, `release_planning_prompt.md` | Head of Specs Team | No |
| Update `sprint_planning_prompt.md` STEP -1 Hard Gate 1 prose to enumerate `Design_Gate_Passed` explicitly, matching `shared_standards.md §10.1` | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed — all 11 EPICs / 11 ST items
**Capacity confirmed:** Confirmed — ~19.5 days midpoint of ~24–28 days capacity, no over-allocation
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-07-23
