**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-05
**Cycle:** 2026-08-05__release-v8.3
**Release:** v8.3
**Sprint Goal:** Restore and harden the SI-05 weekly digest pipeline (fix plus delivery-failure alerting) while clearing a curated slate of backend resilience, frontend design-system, QA/spec, and governance-process debt — leaving no ungated P1 operational gap open and no item below its stated acceptance bar.
**Backlog Slice Source:** original `stage4_backlog_slice.md` (ST-11 AC/effort superseded by the corrected `backlog.md#BLG-FE-103` text — see `sprint_planning_notes.md §Stale Backlog Slice Text (ST-11)`)

# Sprint Backlog — 2026-08-05__release-v8.3

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06 (thematic/priority order — EPIC-01 leads per the two P1 operational items; EPIC-04 sequenced after EPIC-03 for the shared `design_system.md` reason below; see `sprint_planning_notes.md §Execution Sequence` for full rationale). All 6 EPICs are classified fully `autonomous` — no delegation-tier grouping constraint applies.

**`execution_state` owner:** EPIC-01 owns `execution_state/_cycle_meta.json` (cycle-level fields, first EPIC to open). Each EPIC branch owns and writes only its own `execution_state/EPIC-xx.json` per the current per-EPIC mechanism (`shared_standards.md §12.1`) — there is no shared file for EPIC branches to conflict on.

**Shared files across EPICs:** `docs/specs/frontend/design_system.md` (EPIC-03/ST-12+ST-13 and EPIC-04/ST-21 — EPIC-03 owns the combined `1.6→1.7` version bump per `design_gate.md`; EPIC-04 must rebase onto `main` after EPIC-03 merges before finalising its ST-21 edit). Full ownership table: `sprint_planning_notes.md §Multi-EPIC Execution Notes`.

---

## Sprint Scope

### EPIC-01 — Operational Reliability & Security

**Maps to:** S2-01
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** 4.25 days (S+S+S+S)
**Risk IDs:** —
**Execution sequence:** 1

#### ST-01 — Investigate and fix the SI-05 weekly Telegram digest delivery pipeline

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.25 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (backend/infra fix, no UI change). If root-cause diagnosis requires a dashboard-only setting not visible via repo search (e.g. a Render deploy/cron configuration, per the precedent that produced `BLG-OPS-128`), escalate rather than guessing — see prior-cycle finding on dashboard-only config invisibility.

**Staging-only ACs:** "SI-05 digest delivery confirmed working again (at least one successful send observed post-fix)" — `[staging-only evidence]`, a live Telegram send is not CI-reproducible. If deferred to post-merge staging, a backlog item must be filed before the PR opens per CLAUDE.md §2.

**Status at sprint open: ready**

---

#### ST-02 — Add delivery-failure alerting for the SI-05 weekly digest

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.00 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 (must complete first — alerting design should follow root-cause understanding, per `stage4_backlog_slice.md`)

**Notes:** Design Gate: Design Not Applicable (alerting infra, no UI change).

**Staging-only ACs:** None — "confirmed firing correctly on a deliberately-stale test" is achievable via a simulated stale-state test harness (same pattern as `BLG-OPS-128`), not a live-production-only check.

**Status at sprint open: ready**

---

#### ST-03 — Recurring check confirming staging/production API keys remain distinct

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.00 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (security/infra automated check, no UI change).

**Staging-only ACs:** None — "confirmed firing correctly on a deliberately-cross-wired test" is simulatable in CI without live cross-environment credentials.

**Status at sprint open: ready**

---

#### ST-04 — Gemini API key rotation runbook

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.00 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (documentation only). Per FI-P3-02, a documentation-only story with no visual/UI claim needs neither Playwright coverage nor staging sign-off.

**Staging-only ACs:** None — documentation deliverable, verifiable by code/doc review.

**Status at sprint open: ready**

---

### EPIC-02 — Backend Engineering Hardening

**Maps to:** S2-02
**Owner:** Infrastructure & Operations Owner; Head of Engineering; Data Model & Domain Schema Owner; Backend Engineering Patterns Owner
**Estimated effort:** 4.50 days (S+S+S+M+S+S)
**Risk IDs:** RISK-01
**Execution sequence:** 2

#### ST-05 — Database index audit for Arc 4 cross-table queries

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 0.50 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (backend audit document, no UI change).

**Staging-only ACs:** None — audit document, verifiable by review; any missing indexes found are filed as separate follow-up items, not evidenced live in this story.

**Status at sprint open: ready**

---

#### ST-06 — Alpaca API rate-limit backoff audit

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.50 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (backend audit document, no UI change).

**Staging-only ACs:** None — audit document; gaps found are filed as follow-up items.

**Status at sprint open: ready**

---

#### ST-07 — Canonical enum registry for position_state values shared frontend/backend

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 0.50 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable — shared-constant/reconciliation refactor; values and rendering unchanged, only the source of truth moves.

**Staging-only ACs:** None — registry existence and frontend/backend derivation are verifiable by code review/CI.

**Status at sprint open: ready**

---

#### ST-08 — Conform remaining routers to canonical error envelope + status codes

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.00 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None (sequencing note: sequenced last within EPIC-02 per RISK-01 — apply incrementally across multiple sequenced commits/PRs, not one large diff)

**Notes:** Design Gate: Design Not Applicable — AC explicitly excludes frontend error-handling behaviour change without a corresponding check. RISK-01: touches error-response paths across ~17 router files; incremental PRs required per its own scope note.

**Staging-only ACs:** None — response envelope/status-code shape is backend-integration-test-verifiable in CI.

**Status at sprint open: ready**

---

#### ST-09 — Retry/backoff for Yahoo Finance regime-check call sites

**Owner:** Head of Engineering
**Estimated effort:** 0.50 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (backend resilience only, no UI change).

**Staging-only ACs:** None — "regression test confirms retry attempts occur before fallback" is a mocked/CI-verifiable test.

**Status at sprint open: ready**

---

#### ST-10 — Idempotent retry for Alpaca paper-trading order sync

**Owner:** Head of Engineering
**Estimated effort:** 0.50 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (backend resilience only, no UI change).

**Staging-only ACs:** None — "test confirms a retried call ... does not create a duplicate order (mocked)" is explicitly a mocked, CI-verifiable test.

**Status at sprint open: ready**

---

### EPIC-03 — Frontend & Design-System Debt

**Maps to:** S2-03
**Owner:** Base44 Frontend Prompt Owner; Head of Engineering; Head of UX & Design
**Estimated effort:** 5.00 days (S+S+M+S+S) — recalculated; see `sprint_capacity.md` ST-11 effort correction note
**Risk IDs:** RISK-02
**Execution sequence:** 3

#### ST-11 — Migrate ComplianceRecheckModal.js onto the shared Dialog primitive

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 1.00 (S — corrected from M; see below)
**Delegation class:** autonomous

**Acceptance Criteria:** `stage4_backlog_slice.md#ST-11` is **stale** (pre-`ESC-20260805-01`-correction text — see `sprint_planning_notes.md §Stale Backlog Slice Text (ST-11)`). Use the corrected AC from `claude/backlog/backlog.md#BLG-FE-103` instead:
- `ComplianceRecheckModal.js` renders via the shared `Dialog`/`DialogContent` primitive (no bespoke overlay markup remaining)
- Focus trap + restoration and Escape-to-close match the existing shared-primitive convention (`TradePlan.js` Abandon modal precedent)
- No visual/behavioural regression (Playwright coverage confirms)

**Dependencies:** None

**Notes:** Design Gate: **Design Pre-Approved** (re-classified this run, `ESC-20260805-01` resolved — was Blocked). Applies an already-existing, already-documented pattern (`design_system.md` §Confirmation Modal, "existing Dialog primitive convention"); no new UX decision, no spec version bump required. Per CLAUDE.md's Any-Story-Introducing-Frontend-Visible-Changes rule: this is an observable AC (visual rendering + interaction), so Playwright coverage or a recorded staging run is required — code review alone is not sufficient evidence.

**Staging-only ACs:** None — observable UI change is Playwright-verifiable in CI per RISK-02's own stated mitigation ("Playwright coverage ... required per CLAUDE.md for each observable AC").

**Status at sprint open: ready**

---

#### ST-12 — Extract a shared modal-confirmation component

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 1.00 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None (forward reference, non-blocking: `BLG-FE-116`/`BLG-FE-117`, not in this sprint, are expected to reference this component's Base44 prompt templates in a future sprint)

**Notes:** Design Gate: **Design Required**, cleared — genuinely new interaction pattern (undo-window countdown), no prior artefact. Decision record: `docs/design/2026-08-05__release-v8.3/shared-confirmation-modal-undo-window/decision_record.md`. `design_system.md` bump to v1.7 — EPIC-03 owns this combined bump (see Merge Order).

**Staging-only ACs:** None — component existence/configurability is Playwright- and code-review-verifiable; no live-environment dependency in the stated AC.

**Status at sprint open: ready**

---

#### ST-13 — Unified loading-skeleton pattern for async-loading cards

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 2.00 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Design Gate: **Design Required**, cleared — genuinely new visual pattern (today's loading state is spinner-only) plus a new motion/timing parameter (Design-Required-triggering under §6 independent of layout, per `BLG-FE-131` precedent). Decision record: `docs/design/2026-08-05__release-v8.3/loading-skeleton-pattern/decision_record.md`. Not required to retrofit all existing cards in one pass — AC is documentation-of-pattern, not full rollout. `design_system.md` bump to v1.7 — EPIC-03 owns this combined bump (see Merge Order).

**Staging-only ACs:** None — AC as written is "pattern documented in `design_system.md`," a doc/code-review-verifiable deliverable, not a live-rendering claim.

**Status at sprint open: ready**

---

#### ST-14 — Standard Base44 prompt section for dark/light theme compliance

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 0.50 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Design Gate: **Design Pre-Approved** — codifies already-fully-specified `design_system.md` rules into a Base44 prompt template section; no new UX decision, template packaging only.

**Staging-only ACs:** None — documentation/template deliverable, code-review-verifiable (FI-P3-02 wording-only exception applies).

**Status at sprint open: ready**

---

#### ST-15 — AI disclaimer component extraction

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 0.50 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Design Gate: **Design Pre-Approved** — extraction only; both consumer instances' contrast fixes verified still shipped/unchanged (`dashboard.md` v3.2, `positions.md` v2.7). Explicit "no visual regression" AC.

**Staging-only ACs:** None — "existing disclaimer visibility assertions still pass" is explicitly a Playwright-in-CI check per RISK-02's mitigation.

**Status at sprint open: ready**

---

### EPIC-04 — QA & Spec Debt

**Maps to:** S2-04
**Owner:** Director of Quality; API Contracts & Documentation Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 4.50 days (S×6)
**Risk IDs:** —
**Execution sequence:** 4

#### ST-16 — Add baseline Playwright coverage for Watchlist.js

**Owner:** Director of Quality
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (test infrastructure only, no UI change).

**Staging-only ACs:** None — the story's own deliverable is a CI-run Playwright spec.

**Status at sprint open: ready**

---

#### ST-17 — OpenAPI drift gate false-negative sweep

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (QA process procedure, no UI change).

**Staging-only ACs:** None — sweep procedure and its first run are documentable/verifiable without a live environment.

**Status at sprint open: ready**

---

#### ST-18 — DoQ sign-off staleness pre-merge lint

**Owner:** Director of Quality
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (CI/CD lint check, no UI change).

**Staging-only ACs:** None — "fails on a synthetic Pending-row test case" is explicitly a CI-verifiable test.

**Status at sprint open: ready**

---

#### ST-19 — OpenAPI response-example drift spot-check

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (documentation audit, no UI change).

**Staging-only ACs:** None — spot-check performed against live responses is a one-time verification step documented as output, not an ongoing staging-only AC; any drift found is filed as follow-up.

**Status at sprint open: ready**

---

#### ST-20 — API endpoint deprecation-window policy

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (API documentation standards, no UI change).

**Staging-only ACs:** None — policy document, code/doc-review-verifiable.

**Status at sprint open: ready**

---

#### ST-21 — Canonical form validation error-message pattern spec

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None (sequencing note: sequenced last within EPIC-04, and EPIC-04 sequenced after EPIC-03 in the merge order, because this story shares `design_system.md` with EPIC-03/ST-12+ST-13 — see Merge Order)

**Notes:** Design Gate: **Design Required**, cleared — two shipped instances (`WatchlistModal.js`, `TradePlan.js`) verified to diverge on trigger timing, plus an unaddressed dark-only colour-token gap (same defect class as `BLG-FE-87/88/95`). Decision record: `docs/design/2026-08-05__release-v8.3/form-validation-error-message-pattern/decision_record.md`. **Must rebase onto `main` after EPIC-03 merges** before finalising this story's `design_system.md` edit — EPIC-03 owns the combined `1.6→1.7` version bump.

**Staging-only ACs:** None — pattern spec is a documentation deliverable, code/doc-review-verifiable.

**Status at sprint open: ready**

---

### EPIC-05 — Governance Process

**Maps to:** S2-05
**Owner:** Head of Specs Team; AI Compliance & Governance Officer; Strategy Rules & System Intent Owner; Director of HR
**Estimated effort:** 5.50 days (S+M+S+M+S)
**Risk IDs:** —
**Execution sequence:** 5

#### ST-22 — SC-02: Remove RESUME PRECHECK mutation detection block from release_planning_prompt.md

**Owner:** Head of Specs Team
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** ST-25 (sequenced after — this story's required `prompt_change_log.md` append per CLAUDE.md §6 should land in the corrected prepend/append format ST-25 establishes, not the defective mixed-ordering format)

**Notes:** Design Gate: Design Not Applicable (governance prompt amendment, no UI change). Governance File Edit Checklist (CLAUDE.md §6) applies in full: version bump, `OPERATIONAL_GUIDE.md` §14 update, phase-section header update, `prompt_change_log.md` append — all in the same commit.

**Staging-only ACs:** None — "dry-run validation pass confirming no functional regression" is a `plan release --dry-run`-class CI/local check, not staging-only.

**Status at sprint open: ready**

---

#### ST-23 — Formal §13 boundary re-attestation cadence

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 1.75 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (governance process cadence, no UI change).

**Staging-only ACs:** None — cadence proposal + first review date is a documentation deliverable.

**Status at sprint open: ready**

---

#### ST-24 — SI-02 trade-count gate threshold calibration review

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** 0.50 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (governance/metrics review, no UI change).

**Staging-only ACs:** None — review + written conclusion is a documentation deliverable; underlying trade-plan count data is queryable, not live-only.

**Status at sprint open: ready**

---

#### ST-25 — prompt_change_log.md mixed prepend/append ordering breaks gap detection

**Owner:** Head of Specs Team
**Estimated effort:** 1.75 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None (sequenced first within EPIC-05 — see ST-22's Dependencies field)

**Notes:** Design Gate: Design Not Applicable (governance file/process fix, no UI change). Two fix options named in the source item (full re-sort vs. scan-logic change) — this is an additive-scope choice with no materially different effort estimate between options, not a multi-vehicle risk requiring a phasing cross-reference (LP-14 check: not applicable).

**Staging-only ACs:** None — verifiable by re-running the STEP -1.7-class gap-detection check against the fixed file/logic.

**Status at sprint open: ready**

---

#### ST-26 — Cross-role workload balance check

**Owner:** Director of HR
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable (governance-engine report output surfaced at roadmap rebalance, not app UI, no UI change).

**Staging-only ACs:** None — check definition + its output at the next roadmap rebalance is documentation/process, not staging-only.

**Status at sprint open: ready**

---

### EPIC-06 — Product Retrospective

**Maps to:** S2-06
**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 0.50 days (S)
**Risk IDs:** —
**Execution sequence:** 6

#### ST-27 — Monthly P&L report format review — 3-month usage retrospective

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 0.50 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** Design Gate: Design Not Applicable — review/recommendations document only; any identified format change is filed as a separate future item subject to its own design gate. Date gate (`≥ 2026-08-05`) cleared exactly this cycle per `release_plan.md §Readiness` STEP 1.4b.

**Staging-only ACs:** None — review + recommendations document, code/doc-review-verifiable.

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days |
| Total estimated effort (in-scope) | ~24.25 days (recalculated post-ST-11-correction; see `sprint_capacity.md`) |
| Utilisation | ~87-101% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 27 items in the authoritative backlog slice entered the sprint.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| File a `BLG-GOV-*` item proposing a `stage4_backlog_slice.md` post-gate-correction addendum mechanism | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-08-05 (agent-mediated, delegated authority; see `sprint_goal.md`)
**Scope confirmed:** Confirmed — 27 items, 6 EPICs, all classified `include`; no items deferred — 2026-08-05
**Capacity confirmed:** Confirmed — ~24.25d against ~24-28d confirmed band, `pass` outcome at every point in the band; buffer-floor note at the bottom-of-band denominator acknowledged (see `sprint_capacity.md §Minimum Capacity Buffer Floor`) — 2026-08-05
**Deferred execution blockers accepted (if any):** N/A — `state.json.deferred_execution_blockers` empty
**Signed off by:** Product Owner (agent-mediated, delegated authority)
**Date:** 2026-08-05
