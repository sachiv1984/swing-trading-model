**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-09-16
**Cycle:** 2026-09-15__release-v9.5
**Release:** v9.5
**Sprint Goal:** Clear the full v9.5 debt-reduction scope — 43 items across 6 EPICs — at the top of confirmed sprint capacity, resolving the cycle's two genuine ungated P1 items first. See `sprint_goal.md`.
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

## Sprint Scope

**Merge order:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06 (rationale: `sprint_planning_notes.md ## Execution Sequence` — `BLG-BE-117`/ST-01 is CI-blocking for every open/future PR and lands first). **`execution_state.json` owner:** EPIC-01. **Shared files:** none across EPICs this cycle. Within-EPIC only: `workforce_capacity.md` (EPIC-05 — ST-37 lands before ST-38); `design_system.md` (EPIC-06 — ST-41 lands before ST-42).

---

### EPIC-01 — Backend & Platform Engineering Debt

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Head of Engineering
**Estimated effort:** 6.00 days
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — CI-blocking test_changelog_service.py failure on every PR

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** S (~0.5–1d, pending root cause)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None — sequence first within EPIC-01 and ideally first across the whole cycle (CI-blocking for every open/future PR)

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-02 — Backend logging output does not conform to structured_logging_standards.md's mandatory JSON Lines format

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M (~2–3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** AC offers two genuine alternative fix vehicles (conform code to spec, or formally revise the spec) — the executing engine decides based on what existing log-based monitoring already depends on, and documents the rationale for whichever path is taken.

**Staging-only ACs:** None.

---

#### ST-03 — Validate limit/offset are non-negative on screener endpoints

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-04 — Consolidate duplicated ATR trailing-stop recalculation logic

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** RISK-01 — diff all 3 existing implementations line-by-line before writing the shared version; preserve whichever behaviour existing passing tests actually exercise; file any unclear divergence as its own item rather than guess.

**Staging-only ACs:** None.

---

### EPIC-02 — Operations & Security Debt

**Maps to:** S2-02
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 6.30 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-05 — nightly-stop-update and rebalance-exit appear to have no live scheduled trigger

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (investigation/confirmation) — remediation effort TBD pending confirmation
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** RISK-02 — scope capped to investigation + documentation-correction this cycle; if a live gap is confirmed and remediation exceeds this story's small-effort estimate, stop and file the wiring fix as a new backlog item rather than absorb open-ended scope. Classified `delegated_decision` because `BLG-OPS-159`/ST-12 (this same EPIC) documents a confirmed prior gotcha that Render dashboard-only settings are invisible to repo search — the "Render dashboard checked" AC plausibly requires a live dashboard login, not something derivable from `render.yaml` alone.

**Staging-only ACs:** AC-02 (live confirmation that `GET /health/scheduler` shows a recent `last_run` for all three job names) is `[staging-only evidence]` if a live gap is confirmed and endpoints are wired this cycle — CI cannot exercise a live scheduler trigger.

---

#### ST-06 — AI audit log cost-monitoring follow-ons: storage projection, per-feature trend, silent-purge-failure visibility

**Owner:** FinOps & Resource Architect
**Estimated effort:** M (~2 days, 3 small sub-items)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** FinOps & Resource Architect sign-off required at close.

**Staging-only ACs:** None.

---

#### ST-07 — New api_call_log table has no retention/purge policy

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-08 — get_api_session_report() anomaly baseline is self-inclusive

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-09 — Add 1 new endpoint to api_performance_baseline.md re-run

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1h, plus a live measurement re-run)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Live measurement re-run is against the app's own `GET /positions/{id}` endpoint (in-repo test tooling), not an external dashboard — no external-access blocker.

**Staging-only ACs:** None.

---

#### ST-10 — Recurring quarterly hosting-cost trend review

**Owner:** FinOps & Resource Architect
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** AC requires the first cadence-driven review to actually be completed with results recorded, not merely documented as a future cadence.

**Staging-only ACs:** None.

---

#### ST-11 — Synthetic uptime monitor for /health independent of hosting dashboard

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** If confirming a real monitor firing on a deliberate test failure requires an external monitoring service with no in-repo simulation path, treat that specific sub-check as staging-only evidence at execution rather than fabricating a firing event.

**Staging-only ACs:** Potentially AC "Monitor configured and confirmed firing on a deliberate test failure" if no in-repo simulation is possible — confirm at execution.

---

#### ST-12 — Document the dashboard-only deploy path-filter gotcha in the ops runbook

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** This is the item that documents the gotcha cross-referenced in ST-05's Notes above.

**Staging-only ACs:** None.

---

#### ST-13 — claude_audit_log has no latency column; no real-data source for AI endpoint latency anomaly checks

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-14 — Provision read-only staging DATABASE_URL for sprint-execution sessions

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Requires actual credential provisioning in the hosting/secrets environment — cannot be self-provisioned by the execution engine.

**Staging-only ACs:** AC "A sprint-execution session can successfully run a real read-only query against staging data end-to-end" is `[staging-only evidence]`, sequenced after the credential exists.

---

### EPIC-03 — QA & Test Coverage Debt

**Maps to:** S2-03
**Owner:** QA & Testing Owner; Director of Quality
**Estimated effort:** 3.20 days
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-15 — Arc 4 E2E test strategy pre-design (PO-02/03/04)

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (soft consistency link to ST-23's Arc 4 contract stubs — same Arc 4 pre-authoring wave, no hard ordering)

**Notes:** Reviewed by Director of Quality before close.

**Staging-only ACs:** None.

---

#### ST-16 — Extract governance_sync.yml's embedded bash logic into a shared, sourced script

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-17 — Add unit test coverage for check_contract_example_freshness.py

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-18 — Playwright coverage matrix file-inventory count is stale (39 vs actual ~100+ spec files)

**Owner:** QA & Testing Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** RISK-03 — re-count against the current `tests/e2e/` directory contents before applying the fix; the filed 39-file count may already be further stale.

**Staging-only ACs:** None.

---

#### ST-19 — ST-09 cross-browser evaluation cites stale pre-sharding CI baseline

**Owner:** QA & Testing Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-20 — ST-05 SignalCard spec consolidation lacks before/after runtime evidence

**Owner:** QA & Testing Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-21 — qa_evidence_EPIC-03.md test-count claim inaccurate (30 vs. actual 28)

**Owner:** QA & Testing Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** RISK-03 — re-count against the actual current `tests/test_cost_monitoring.py` contents before applying the fix.

**Staging-only ACs:** None.

---

### EPIC-04 — Spec & Documentation Debt

**Maps to:** S2-04
**Owner:** Head of Specs Team; API Contracts & Documentation Owner; Data Model & Domain Schema Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 7.34 days
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-22 — data_model.md positions table (DS-17 addition) not confirmed against live deployed schema

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** XS (confirmation only, once DB access is available)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** RISK-04 — `DATABASE_URL` re-confirmed unset in this execution environment, consistent with every prior cycle's own risk register since v9.2. Prepare the confirmation query regardless; disclose explicitly rather than fabricate a schema confirmation if still unavailable, following the `ESC-EXEC-20260910-01` honest-disclosure precedent.

**Staging-only ACs:** AC "Live schema confirmed to match spec" is `[staging-only evidence]` — requires DB access unavailable in this environment.

---

#### ST-23 — Arc 4 API contract pre-authoring (PO-02/03/04)

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** ST-24 (soft — sequence ST-24's data-model pre-definition before or alongside this story so the contract stubs have a model to reference; see `sprint_planning_notes.md ## Dependency Map`)

**Notes:** `BLG-SPEC-35` §13 pre-assessment remains open/P1 and is the governing review — this item routes new boundary questions to it rather than bypassing it (per `design_gate.md` ST-23 rationale).

**Staging-only ACs:** None — stub-only, no implementation.

---

#### ST-24 — Data model v3 pre-definition for Arc 4 journal intelligence

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** Sequence before or alongside ST-23 (shared cross-reference — see `sprint_planning_notes.md ## Dependency Map`)

**Notes:** Reviewed by Head of Specs Team and Infrastructure & Operations Owner before close.

**Staging-only ACs:** None — pre-definition document only, no migration SQL.

---

#### ST-25 — position_endpoints.md example JSON: current_trailing_stop_native doesn't reconcile with current_trailing_stop × live_fx_rate

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** XS (~15min)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-26 — Triage contract example-payload freshness check findings

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** All 40 baseline findings need a recorded disposition — not merely the highest-priority subset.

**Staging-only ACs:** None.

---

#### ST-27 — Make check_orphaned_specs.py path-aware to resolve duplicate-basename blind spots

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** Existing 10 unit tests in `tests/test_check_orphaned_specs.py` must still pass; add new tests for the path-aware resolution and ambiguity-flagging fallback.

**Staging-only ACs:** None.

---

#### ST-28 — Spec debt dashboard sort key mishandles same-day-filed items

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-29 — Canonical position/trade lifecycle state diagram

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** M
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None

**Notes:** All 3 source files must cross-reference the new diagram.

**Staging-only ACs:** None.

---

#### ST-30 — Consolidate divergent empty-state copy patterns

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** None

**Notes:** AC is confirm-and-document only — no shipped UI copy change is required unless a genuine remaining gap is confirmed against the v9.1 ST-29 prior consolidation. If a copy change is made during execution, it would need its own design-gate pass at that time (not covered by this cycle's gate).

**Staging-only ACs:** None as scoped (confirm-and-document); would require a fresh design-gate + Playwright/staging check if scope expands to an actual copy change.

---

### EPIC-05 — Governance Process Debt

**Maps to:** S2-05
**Owner:** Head of Specs Team; PMO Lead; FinOps & Resource Architect; Director of HR; Director of Quality
**Estimated effort:** 3.95 days
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-31 — Require resolving commits to update the canonical spec's own Known Deviation fields when closing a deviation

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None

**Notes:** Follow the Governance File Edit Checklist (CLAUDE.md §6) in full for whichever governance file this rule lands in.

**Staging-only ACs:** None.

---

#### ST-32 — Wire the wall-clock cost logging convention (§22) into an engine's STEP list

**Owner:** PMO Lead
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-33 — Codify whether opportunistic in-file fixes found mid-story need their own backlog entry

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`

**Dependencies:** None

**Notes:** Product Owner sign-off (agent-mediated, per `shared_standards.md §16.13`).

**Staging-only ACs:** None.

---

#### ST-34 — record-visual-qa skill's documented output format has drifted ~5 months from actual staging sign-off practice

**Owner:** Director of Quality
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None

**Notes:** Reconcile against a real sample of recent `qa_evidence_EPIC-*.md` entries, not an assumed format.

**Staging-only ACs:** None.

---

#### ST-35 — File a Product Owner decision record for ST-20's trade-tagging "no closed taxonomy" call

**Owner:** Product Owner
**Estimated effort:** XS (<1h)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None

**Notes:** Genuine open product decision requiring an actual Product Owner ruling, not a documentation-only task.

**Staging-only ACs:** None.

---

#### ST-36 — Lightweight role-retirement process for inactive agent charters

**Owner:** Director of HR
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`

**Dependencies:** None

**Notes:** Must be applied at least once to confirm it runs end to end — 0 qualifying roles is a valid outcome.

**Staging-only ACs:** None.

---

#### ST-37 — Cross-role pairing rotation note in workforce_capacity.md

**Owner:** Director of HR
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`

**Dependencies:** Sequence before ST-38 (both edit `workforce_capacity.md` — RISK-05)

**Notes:** Cross-reference from `roadmap_prompt.md` §7.1's pull-forward step.

**Staging-only ACs:** None.

---

#### ST-38 — Cost-per-cycle wall-clock rollup in workforce_capacity.md

**Owner:** FinOps & Resource Architect
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`

**Dependencies:** Sequence after ST-37 (both edit `workforce_capacity.md` — RISK-05)

**Notes:** Populate with available historical figures; document refresh cadence.

**Staging-only ACs:** None.

---

#### ST-39 — Formalise the STEP 8.0.5 / STEP 8.2 candidate-verification pattern as one subroutine

**Owner:** Head of Specs Team
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`

**Dependencies:** None

**Notes:** Governance File Edit Checklist (CLAUDE.md §6) applies in full — version bump + `prompt_change_log.md` entry required in the same commit.

**Staging-only ACs:** None.

---

### EPIC-06 — Frontend & UX Debt

**Maps to:** S2-06
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Estimated effort:** 1.20 days
**Risk IDs:** RISK-06 (resolved — design gate Passed)
**Execution sequence:** 6

#### ST-40 — Fix trade plan link display to use formatted text instead of snake_case

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-40`

**Dependencies:** None

**Notes:** Design Pre-Approved (`design_gate.md`) — apply the existing `trade_plan.md` §9 Status Badge Scheme / `STATUS_LABELS` convention at the missed `TradeEntry.js` call site; no new visual/interaction decision needed.

**Staging-only ACs:** None — wording-only text-formatting change (no new layout/colour/interaction claim); code review of the static JSX substitutes for staging sign-off per CLAUDE.md §2 (FI-P3-02 exception).

---

#### ST-41 — Bring the 4 known motion-timing non-compliant components under the 500ms ceiling

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-41`

**Dependencies:** Sequence before ST-42 (both edit `design_system.md` — different sections, but not parallel commits)

**Notes:** Design Required, reusing the already-approved `2026-09-14__release-v9.4` remediation plan (`design_gate.md`) — implementation only, no new design decision.

**Staging-only ACs:** Timing-behaviour change — requires existing Playwright coverage for these 4 components to still pass, or a human staging run recorded in the DoQ sign-off block if no such coverage exists. Confirm coverage status at execution before treating this as code-review-only.

---

#### ST-42 — Bring 9 non-conforming toast call sites into line with the Toast Notification Timing standard

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-42`

**Dependencies:** Sequence after ST-41 (both edit `design_system.md`)

**Notes:** Design Required, reusing the already-approved `2026-09-14__release-v9.4` Toast Notification Timing standard and 9-site inventory (`design_gate.md`) — implementation only.

**Staging-only ACs:** Timing-behaviour change — requires existing Playwright coverage for these 9 call sites to still pass, or a human staging run recorded in the DoQ sign-off block if no such coverage exists. Confirm coverage status at execution before treating this as code-review-only.

---

#### ST-43 — Arc 5 low-trade-volume advisory: surface the 20-trade threshold and remaining-trades count, reconsider placement above the stat grid

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-43`

**Dependencies:** None

**Notes:** Design Required, new decision record produced this gate (`arc5_compliance_section.md` v1.3.0 → v1.4.0) — `design_gate.md` confirmed the existing `tests/e2e/arc5-compliance-section.spec.js` assertions (`SC-ARC5-09`/`SC-ARC5-10a/b/c`) are not broken by the copy/placement change.

**Staging-only ACs:** Confirm at execution whether the new threshold/remaining-count copy needs a *new* Playwright assertion beyond the existing suite (which only confirms the change doesn't break existing assertions, not that the new copy itself is covered). If new Playwright coverage cannot be added, file a backlog item before the PR opens per CLAUDE.md §2 — do not defer to "code review only" without a filed item.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalents |
| Total estimated effort (in-scope) | 27.99 days |
| Utilisation | 99.96% of the 28-day ceiling |
| Over-allocation | No — within band, buffer floor (95%) exceeded and acknowledged (see `sprint_capacity.md §1.5`) |

## Items Deferred This Sprint

None — all 43 items in the authoritative backlog slice enter this sprint.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Buffer-floor-exceeded acknowledgement (99.96%) | Product Owner | No |
| Confirm ST-05's Render-dashboard AC requires live access (no repo-derivable substitute) | Infrastructure & Operations Owner | No |
| Confirm ST-41/ST-42 Playwright coverage status before treating as code-review-only | Director of Quality | No |
| Confirm whether ST-43's new copy needs a new Playwright assertion; file backlog item before PR if deferred to staging | Base44 Frontend Prompt Owner | No |
| File backlog item reconciling `sprint_planning_prompt.md` STEP -1 Hard Gates 1–2 status-vocabulary wording | Head of Specs Team | No |

No outstanding action is marked `Blocker? Yes`.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (agent-mediated, 2026-09-16 — see `sprint_goal.md`)
**Scope confirmed:** Confirmed — full 43-item / 6-EPIC scope per Release Planning and Design Gate, no items deferred at Sprint Planning
**Capacity confirmed:** Confirmed — 27.99d within the ~24–28d band, buffer-floor overage (99.96%) acknowledged as the direct consequence of the standing "use full capacity" instruction
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner (agent-mediated, per `shared_standards.md §16.13` method)
**Date:** 2026-09-16

---

## Change Log

| Date | Change |
|------|--------|
| 2026-09-16 | Initial publication and seal — 43 items / 6 EPICs, 27.99d, for 2026-09-15__release-v9.5. |
