**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-09-07
**Cycle:** 2026-09-07__release-v9.2
**Release:** v9.2
**Sprint Goal:** Ship the Arc 5 low-volume compliance-score advisory and clear a full-capacity slate of 55 accessibility, QA/CI reliability, governance-process, and spec/tech/ops debt items across all 5 EPICs — exhausting the confirmed ~24–28 day capacity band at 27.55 days, with 0 P1/P2 debt items carried past this sprint on capacity grounds.
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

# Sprint Backlog — 2026-09-07__release-v9.2

**Merge order (5 EPICs in scope):** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05. **`execution_state.json` owner: EPIC-01.** Shared files across EPICs: `docs/specs/frontend/components/arc5_compliance_section.md` (EPIC-01/EPIC-02), `docs/specs/frontend/design_system.md` (EPIC-02/EPIC-05), `tests/e2e/arc5-compliance-section.spec.js` (EPIC-02/EPIC-03) — see `sprint_planning_notes.md` Multi-EPIC Execution Notes for full ownership/sequencing advisory.

---

## Sprint Scope

### EPIC-01 — Arc 5 Compliance Score Low-Volume Advisory

**Maps to:** S2-01
**Owner:** Metrics Definitions & Analytics Owner; Head of UX & Design
**Estimated effort:** 0.50d
**Risk IDs:** RISK-01 (Resolved), RISK-06 (Resolved)
**Execution sequence:** 1

#### ST-01 — Arc 5 compliance score utility advisory at low trade volume

**Owner:** Metrics Definitions & Analytics Owner; Head of UX & Design
**Estimated effort:** 0.50d
**Delegation class:** autonomous — locked design artefact (`docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/decision_record.md`, `StandingAlert` Info-tone reuse) and locked frontend spec reference (`arc5_compliance_section.md` v1.1.0); no new design decision required at execution.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (shared-file sequencing advisory only — see Multi-EPIC Execution Notes)

**Notes:** Gate condition formally confirmed by Metrics Definitions & Analytics Owner this session (see `sprint_planning_notes.md`). If the assessment concludes advisory-not-needed, the UI-addition AC and its spec bump are void — record that outcome explicitly rather than silently skipping.

**Staging-only ACs:** None — advisory UI addition (if warranted) is Playwright-testable per CLAUDE.md frontend-visible-changes rule; if Playwright coverage proves infeasible, staging sign-off + a filed backlog item are required before the PR opens (RISK-02-equivalent risk, not itself in RISK-02's EPIC-02 scope).

---

### EPIC-02 — Frontend Accessibility & Spec Compliance

**Maps to:** S2-02
**Owner:** Frontend Specifications & UX Documentation Owner; Director of Quality
**Estimated effort:** 0.95d
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-02 — Settings page heading-order axe-core finding (moderate, non-blocking)

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15d
**Delegation class:** autonomous — semantic heading-tag correction, no UX change (BLG-GOV-72 fast-path (a))

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Design Pre-Approved at design gate — no visual/layout regression permitted (equivalent styling preserved via className).

**Staging-only ACs:** None — `axe-core` scan runs in CI (`tests/e2e/accessibility-axe-scan.spec.js`).

#### ST-03 — aria-label duplicates visible label text instead of using aria-labelledby (TradePlan.js, Settings.js)

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15d
**Delegation class:** autonomous — accessible-name mechanism swap, no visible/behavioural change (BLG-GOV-72 fast-path (a))

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Design Pre-Approved at design gate. 5 controls affected across 2 files — TradePlan.js (Market, Status, Setup Type), Settings.js (Default Currency, Theme).

**Staging-only ACs:** None — `tests/e2e/accessibility-axe-scan.spec.js` regression coverage runs in CI.

#### ST-04 — Arc5ComplianceSection "Top Rule Breach" card diverges from canonical spec (text format + null display)

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design (design direction confirmed)
**Estimated effort:** 0.15d
**Delegation class:** autonomous — spec correction to match already-shipped, tested, sibling-consistent implementation; no code/UI change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** Blocks ST-08 (EPIC-03) — sequence this story first; see `sprint_planning_notes.md` Dependency Map.

**Notes:** Design Pre-Approved — resolves a documented Known Deviation in `arc5_compliance_section.md` v1.1.0 (v9.2 target release) by correcting the spec, not the implementation. Bumps `arc5_compliance_section.md`; see Multi-EPIC Execution Notes for EPIC-01/EPIC-02 shared-file sequencing.

**Staging-only ACs:** None — spec-only change; `tests/e2e/arc5-compliance-section.spec.js` (SC-ARC5-07/SC-ARC5-08) update, if needed, is CI-verifiable.

#### ST-05 — Motion-vs-contrast trade-off (entrance fade-in animations) has no design_system.md guideline

**Owner:** Head of UX & Design
**Estimated effort:** 0.50d
**Delegation class:** autonomous — documentation-only deliverable (guideline prose or explicit no-guideline-needed decision); locked design artefact produced at gate (`docs/design/2026-09-07__release-v9.2/motion-contrast-guideline-standard/decision_record.md`)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** Blocks ST-47 (EPIC-05) — sequence this story before ST-47; see `sprint_planning_notes.md` Dependency Map.

**Notes:** Design Required per the motion/timing-sensitive-interaction special rule (§6, BLG-FE-131) — classification standard-setting, not a shipped-animation-parameter change. Bumps `design_system.md`; see Multi-EPIC Execution Notes.

**Staging-only ACs:** None — documentation deliverable, no runtime behaviour to verify.

---

### EPIC-03 — QA & CI Reliability Debt

**Maps to:** S2-03
**Owner:** QA Testing Owner; Director of Quality
**Estimated effort:** 4.45d
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-06 — playwright.yml CI trigger path filter excludes package.json/package-lock.json

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15d
**Delegation class:** autonomous — additive CI trigger-path fix

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Additive only — must not change which paths trigger the job for existing frontend-file changes.

**Staging-only ACs:** None — verifiable by a real CI run against the modified `playwright.yml` (RISK-03-adjacent evidence standard: CI run URL/log excerpt required at DoQ, not "staging" per se).

#### ST-07 — accessibility-axe-scan.spec.js's runAxeScan() uses a fixed sleep instead of a condition-based wait

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — test-infrastructure timing fix, no UI change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** All 4 existing page scans (DashboardHome, Positions, TradePlan, Settings) must continue passing unchanged.

**Staging-only ACs:** None — CI-verifiable.

#### ST-08 — Arc5ComplianceSection Playwright tests SC-ARC5-06/SC-ARC5-07 use unscoped text selectors

**Owner:** QA Testing Owner
**Estimated effort:** 0.15d
**Delegation class:** autonomous — test-selector scoping fix, no product change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** ST-04 (EPIC-02) must complete first — both touch `SC-ARC5-07` in the same spec file. See `sprint_planning_notes.md` Dependency Map.

**Notes:** Full `arc5-compliance-section.spec.js` file must continue passing (8/8) after rebase onto ST-04's changes.

**Staging-only ACs:** None — CI-verifiable.

#### ST-09 — governance_sync.yml's over-closing prevention (unknown→skip) unverified in real CI

**Owner:** QA Testing Owner; Director of Quality
**Estimated effort:** 0.50d
**Delegation class:** autonomous — regression test authorship; live CI exercise or extended local simulation

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** Blocks ST-10 — sequence this story first. See `sprint_planning_notes.md` Dependency Map.

**Notes:** RISK-03 — code review alone cannot confirm this fix; DoQ sign-off requires actual CI run evidence (run URL/log excerpt).

**Staging-only ACs:** None per the strict staging definition, but flagged: DoQ sign-off requires a real CI run's evidence, not code review alone — same evidentiary bar as `[staging-only evidence]` in substance. If a live CI exercise cannot be obtained pre-merge, file a backlog item before the PR opens per CLAUDE.md's observable-behaviour rule analogue.

#### ST-10 — governance_sync.yml never recovers a story-issue close when the state-sync commit lands separately from the tagged work commit

**Owner:** QA Testing Owner; Director of Quality
**Estimated effort:** 0.50d
**Delegation class:** autonomous — regression test authorship for the split-commit scenario

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** ST-09 must complete first (Internal — see Dependency Map).

**Notes:** RISK-03 — same live-CI-evidence requirement as ST-09. AC explicitly requires confirming ST-09/BLG-QA-159 behaviour is unaffected.

**Staging-only ACs:** None per the strict definition; same real-CI-run evidentiary flag as ST-09.

#### ST-11 — check_specs_index_freshness.py has zero automated test coverage

**Owner:** QA Testing Owner
**Estimated effort:** 0.15d
**Delegation class:** autonomous — unit test authorship for an existing script

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Must cover addition + removal detection paths and at least one exclusion-rule false-positive guard (e.g. `strategy_rules.md`).

**Staging-only ACs:** None — CI-verifiable unit test.

#### ST-12 — Regression suite runtime budget & trend report (last 90 days)

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — reporting artefact

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

#### ST-13 — DEV-* deviation recurrence pattern report

**Owner:** Director of Quality
**Estimated effort:** 0.50d
**Delegation class:** autonomous — reporting artefact against the current deviation set

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

#### ST-14 — pip-audit trend log across sprint-planning runs

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — logging convention + application from next sprint planning onward

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** If the convention requires editing `sprint_planning_prompt.md` STEP -1's pip-audit advisory check text, apply the full CLAUDE.md §6 governance file edit checklist and sequence after EPIC-04's serial governance-prompt block (see Multi-EPIC Execution Notes).

**Staging-only ACs:** None.

#### ST-15 — DoQ sign-off template alignment check (FI-P3-02 wording-only exception)

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — comparison + confirm/correct

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

#### ST-16 — Staging sign-off backlog tracker (FI-P3-02 wording-only AC exceptions)

**Owner:** QA Lead
**Estimated effort:** 0.50d
**Delegation class:** autonomous — tracker creation + backfill

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

### EPIC-04 — Governance Process Debt

**Maps to:** S2-04
**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 13.00d
**Risk IDs:** RISK-04
**Execution sequence:** 4

**Mandatory serial execution (RISK-04):** ST-17 through ST-42 execute one at a time, in listed order, on the EPIC-04 branch — no parallel sub-branches. Each item applies the full CLAUDE.md §6 Governance File Edit Checklist (version bump, OPERATIONAL_GUIDE.md §14 sync, phase-section header sync, prompt_change_log.md entry) before the next begins.

All 26 items below: **Delegation class: autonomous** (documentation/prompt-patch/policy artefacts, no UX change). **Staging-only ACs: None** (no runtime UI behaviour). **Dependencies: None** beyond the mandatory serial-execution ordering stated above.

#### ST-17 — Quarterly model/prompt-drift compliance attestation log

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`
**Notes:** None.

#### ST-18 — Deprecation header convention for retiring API endpoints

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`
**Notes:** Reference from `shared_standards.md` or an equivalent canonical location.

#### ST-19 — Formal expiry review for §13-adjacent initiatives open more than 2 cycles

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`
**Notes:** §13 pre-check confirmed not applicable (process cadence review, no AI-provider call).

#### ST-20 — stage4_backlog_slice.md post-gate-correction addendum mechanism

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`
**Notes:** Patches `design_gate_prompt.md` — full CLAUDE.md §6 checklist applies to that file specifically.

#### ST-21 — AI response caching evaluation for morning briefing

**Owner:** Backend Engineering Owner; FinOps & Resource Architect
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`
**Notes:** §13 pre-check confirmed not applicable (evaluates an already-shipped AI feature).

#### ST-22 — Gemini AI usage audit-trail retention policy

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`
**Notes:** §13 pre-check confirmed not applicable.

#### ST-23 — Standardise api_changelog.md entry template

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`
**Notes:** None.

#### ST-24 — Frame Skill-Silo Alert as workload-composition, not just product-mix

**Owner:** Director of HR
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`
**Notes:** Patches `roadmap_prompt.md` STEP 7.1 — versioned per CLAUDE.md §6.

#### ST-25 — Governance-cycle wall-clock cost logging

**Owner:** PMO Lead
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`
**Notes:** None.

#### ST-26 — Product Value Ratio historical trend row in velocity_metrics.md

**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`
**Notes:** Row added retroactively for the last 3 readings.

#### ST-27 — Surface meta-review countdown in every run_manifest.md

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`
**Notes:** Patches `roadmap_prompt.md` STEP 1.1.

#### ST-28 — Data-retention policy for closed-trade and journal records

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`
**Notes:** No implementation required until data volume warrants action.

#### ST-29 — Onboarding checklist for new governance agent roles

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`
**Notes:** None.

#### ST-30 — Periodic §13 boundary review cadence tied to SI-02's gate history

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`
**Notes:** None.

#### ST-31 — Lightweight due-date index for outstanding deferred-patch reminders across cycles

**Owner:** PMO Lead
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`
**Notes:** None.

#### ST-32 — Agent onboarding runbook for adding a new governance role

**Owner:** Director of HR
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`
**Notes:** None.

#### ST-33 — Recurring spec-debt backlog review cadence

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`
**Notes:** Cadence defined in `backlog_management_prompt.md` — full CLAUDE.md §6 checklist applies.

#### ST-34 — Searchable index of STEP 11.4 meta-review findings across cycles

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`
**Notes:** Backfilled from existing `meta_review.md` files.

#### ST-35 — Document exact skill-category taxonomy used for Skill-Silo classification

**Owner:** Metrics Definitions & Analytics Canonical Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`
**Notes:** None.

#### ST-36 — AI feature cost-vs-value retrospective (6-month actuals vs original estimates)

**Owner:** FinOps & Resource Architect
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`
**Notes:** §13 pre-check confirmed not applicable.

#### ST-37 — Formal alert threshold for the cross-role workload-concentration check

**Owner:** Director of HR
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`
**Notes:** Patches `roadmap_prompt.md` §7.2.

#### ST-38 — Formalise condensed-tier trigger thresholds beyond the "no new FTE required" test

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`
**Notes:** May resolve as "no change needed, existing language is fine" — that outcome satisfies the AC.

#### ST-39 — Formalise a data-volume threshold trigger for the §12.2 "elements that may change" review

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`
**Notes:** Threshold documented in §12.2.

#### ST-40 — Formalise Product Value Ratio rolling-window boundary-trade handling in metrics_definitions.md

**Owner:** Metrics Definitions & Analytics Canonical Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-40`
**Notes:** None.

#### ST-41 — strategy_rules.md version cross-reference consistency check in dependent docs

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-41`
**Notes:** First run's findings triaged.

#### ST-42 — Strategy rules change-justification template

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-42`
**Notes:** Applied to the next `strategy_rules.md` version bump.

---

### EPIC-05 — Spec, Tech & Ops Debt

**Maps to:** S2-05
**Owner:** Head of Specs Team; Infrastructure & Operations Owner
**Estimated effort:** 8.65d
**Risk IDs:** RISK-05
**Execution sequence:** 5

**Single review pass (RISK-05):** Head of Specs Team runs one consolidated review across all 14 items below before DoQ sign-off, to catch cross-item drift (several touch overlapping API-contract/spec-index concerns).

All 14 items below: **Delegation class: autonomous.** **Staging-only ACs: None** (documentation/tracker/audit/dependency-cleanup artefacts, no staging-only runtime behaviour), except ST-52 where CI build verification is explicitly CI-checkable, not staging.

#### ST-43 — Deprecated/superseded endpoint sunset tracker

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-43`
**Dependencies:** None
**Notes:** None.

#### ST-44 — Contract example-payload freshness check against live response shape

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-44`
**Dependencies:** None
**Notes:** None.

#### ST-45 — Base44 prompt-version provenance tag on generated components

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-45`
**Dependencies:** None
**Notes:** Documented in `base44_prompt_template_library.md`.

#### ST-46 — Base44 regeneration diff checklist — design-token compliance pass

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-46`
**Dependencies:** None
**Notes:** Uses existing `design_system.md` tokens as reference — adds no new token/pattern.

#### ST-47 — Component prop-naming convention consistency audit

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-47`
**Dependencies:** ST-05 (EPIC-02) must complete first — both write to `docs/specs/frontend/design_system.md`. See `sprint_planning_notes.md` Dependency Map.
**Notes:** Rebase onto `main` after EPIC-02 merges before finalising the convention documentation.

#### ST-48 — Gate-metric naming consistency across roadmap, SI-05 digest, and Reports page

**Owner:** Metrics Definitions & Analytics Canonical Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-48`
**Dependencies:** None
**Notes:** No behavioural/UI change expected — naming/terminology standardisation only.

#### ST-49 — Populate Specs_Index.md with the 78 spec files its own freshness check found unregistered

**Owner:** Head of Specs Team
**Estimated effort:** 2.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-49`
**Dependencies:** None
**Notes:** Largest item in scope (M effort). AC requires `scripts/check_specs_index_freshness.py` to report 0 unexplained additions after this work — verify via script run.

#### ST-50 — Scope a future migration off Create React App (react-scripts v5)

**Owner:** Head of Engineering
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-50`
**Dependencies:** None
**Notes:** Scoping document only — no migration implementation this cycle.

#### ST-51 — Unexplained package-lock.json "dev": true churn from the react-router-dom bump

**Owner:** Head of Engineering
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-51`
**Dependencies:** None
**Notes:** Root cause confirmed benign, or a real issue found and fixed — either outcome satisfies the AC.

#### ST-52 — Remove unused namesquatted/erroneous npm packages from package.json

**Owner:** Head of Engineering
**Estimated effort:** 0.15d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-52`
**Dependencies:** None
**Notes:** `CI=false npm run build` must succeed unchanged after removing `x`, `textarea`, `sqlalchemy`.

#### ST-53 — AI cost-threshold alert value review

**Owner:** FinOps & Resource Architect
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-53`
**Dependencies:** None
**Notes:** §13 pre-check confirmed not applicable.

#### ST-54 — AI endpoint (daily-briefing/chat) cost & latency drift monitoring

**Owner:** FinOps & Resource Architect
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-54`
**Dependencies:** None
**Notes:** §13 pre-check confirmed not applicable. AC requires confirming the check fires on a simulated cost/latency spike.

#### ST-55 — Staging environment data-reset cadence review

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-55`
**Dependencies:** None
**Notes:** None.

#### ST-56 — AI feature cost-trend tracking has not kept pace with feature shipping

**Owner:** FinOps & Resource Architect
**Estimated effort:** 0.50d
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-56`
**Dependencies:** None
**Notes:** §13 pre-check confirmed not applicable. Must reflect all 6 current AI-invoking endpoints with real current-quarter query data.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days |
| Total estimated effort (in-scope) | 27.55 days |
| Utilisation | 98.4% of band ceiling (28d); within band |
| Over-allocation | No — within confirmed capacity; buffer-floor advisory (§1.5) acknowledged by Product Owner, see `sprint_capacity.md` |

## Items Deferred This Sprint

None. All 56 items from the authoritative backlog slice are in scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| None — the sole Pre-sprint Planning Required Decision (RISK-06/`BLG-FEAT-44` gate sign-off) was resolved this session. | — | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — Product Owner, 2026-09-07.
**Scope confirmed:** Confirmed — all 56 items (5 EPICs) selected per `sprint_capacity.md` and `sprint_planning_notes.md`; 0 items deferred. Product Owner, 2026-09-07.
**Capacity confirmed:** Confirmed — 27.55d vs ~24–28d band, no over-allocation; buffer-floor-exceeded advisory (98.4%) explicitly acknowledged (proceed at full scope). Product Owner, 2026-09-07.
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`.
**Signed off by:** Product Owner
**Date:** 2026-09-07
