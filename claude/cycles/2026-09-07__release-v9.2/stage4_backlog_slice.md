Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-07
Cycle: 2026-09-07__release-v9.2
Release: v9.2

# Backlog Slice — v9.2

<!-- release-plan-marker: RP:v9.2:2026-09-07__release-v9.2 -->

56 stories across 5 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope set to the top of the confirmed ~24–28 day/sprint capacity band per explicit user "use full capacity" instruction (2026-09-07). `BLG-FEAT-44`'s gate cleared this cycle (Arc5ComplianceSection live 3+ months post-v4.1 ship) and is the sole ungated build-adjacent item available — all other P1 items remain Arc 5/SI-02/SI-05/PO-02 gate-conditional, and `BLG-FEAT-92` remains excluded as a reconciled `BLG-FEAT-30` sub-scope per the standing v9.1 Product Owner decision (see `run_manifest.md`). Scope otherwise consolidates frontend accessibility/spec compliance, QA/CI reliability debt, governance process debt, and spec/tech/ops debt.

---

## EPIC-01 — Arc 5 Compliance Score Low-Volume Advisory

**Maps to:** S2-01
**Owner:** Metrics Definitions & Analytics Owner; Head of UX & Design

### ST-01 — Arc 5 compliance score utility advisory at low trade volume
**Source:** BLG-FEAT-44
**Priority:** P1
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Assessment document produced (advisory or advisory-not-needed conclusion)
- If advisory warranted: UI advisory added to Arc5ComplianceSection for sub-20-trade states
- Gate condition verified before sprint planning


## EPIC-02 — Frontend Accessibility & Spec Compliance

**Maps to:** S2-02
**Owner:** Frontend Specifications & UX Documentation Owner; Director of Quality

### ST-02 — Settings page heading-order axe-core finding (moderate, non-blocking)
**Source:** BLG-FE-170
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- axe-core no longer reports a `heading-order` violation for the Settings page
- No visual/layout regression (heading level correction should be semantic-only, e.g. `h2`/`h3` tag change with equivalent styling preserved via className, not a visible redesign)

### ST-03 — aria-label duplicates visible label text instead of using aria-labelledby (TradePlan.js, Settings.js)
**Source:** BLG-FE-171
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- All 5 affected controls (TradePlan: Market, Status, Setup Type; Settings: Default Currency, Theme) use `aria-labelledby` instead of a hardcoded `aria-label` string
- `tests/e2e/accessibility-axe-scan.spec.js` continues to pass with no new violations

### ST-04 — Arc5ComplianceSection "Top Rule Breach" card diverges from canonical spec (text format + null display)
**Source:** BLG-FE-172
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Spec and implementation agree on Card 3's text format and null display
- `tests/e2e/arc5-compliance-section.spec.js` (SC-ARC5-07/SC-ARC5-08) updated to match the resolved behaviour if the implementation changes

### ST-05 — Motion-vs-contrast trade-off (entrance fade-in animations) has no design_system.md guideline
**Source:** BLG-SPEC-134
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `design_system.md` either gains an explicit guideline addressing text-element entrance-animation contrast, or records an explicit decision that no guideline is needed and why
- Head of UX & Design sign-off


## EPIC-03 — QA & CI Reliability Debt

**Maps to:** S2-03
**Owner:** QA Testing Owner; Director of Quality

### ST-06 — playwright.yml CI trigger path filter excludes package.json/package-lock.json — dependency-bump PRs never run the E2E suite in CI
**Source:** BLG-OPS-149
**Priority:** P2
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A PR that only modifies `package.json`/`package-lock.json` triggers the Playwright E2E Acceptance Tests job
- No change to which paths trigger the job for existing frontend-file changes (additive only)
- Infrastructure & Operations Owner sign-off

### ST-07 — accessibility-axe-scan.spec.js's runAxeScan() uses a fixed sleep instead of a condition-based wait
**Source:** BLG-QA-157
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `runAxeScan()` no longer relies on a fixed-duration sleep to avoid animation-timing false positives
- All 4 existing page scans (`DashboardHome`, `Positions`, `TradePlan`, `Settings`) continue to pass with the new wait mechanism
- QA & Testing Owner sign-off

### ST-08 — Arc5ComplianceSection Playwright tests SC-ARC5-06/SC-ARC5-07 use unscoped text selectors
**Source:** BLG-QA-158
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `SC-ARC5-06` and `SC-ARC5-07` assertions are scoped to the `Arc5ComplianceSection` container (or an equivalent explicit justification is recorded for why scoping isn't needed there)
- Full `arc5-compliance-section.spec.js` file continues to pass (8/8)

### ST-09 — governance_sync.yml's over-closing prevention (unknown→skip) unverified in real CI
**Source:** BLG-QA-159
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A regression test (real CI exercise, or an extended local simulation script) specifically covers the `unknown` status fallback's skip behaviour
- Test confirms no auto-close occurs for a story with no `execution_state.json` entry at push time that later resolves to a `blocked_*` status

### ST-10 — governance_sync.yml never recovers a story-issue close when the state-sync commit lands separately from the tagged work commit
**Source:** BLG-QA-160
**Priority:** P2
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A story whose work-commit and state-sync-commit are pushed as two separate events is auto-closed on the second push, without requiring the state-sync commit to carry a bracketed `[ST-xx]` tag
- Regression test covers this split-commit scenario and passes
- Existing BLG-GOV-314/BLG-QA-159 behaviour (under-closing/over-closing fixes) unaffected

### ST-11 — check_specs_index_freshness.py has zero automated test coverage
**Source:** BLG-QA-161
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A regression test exists and passes, covering both the addition and removal detection paths and at least one exclusion-rule case
- Test explicitly confirms a legitimate non-`docs/specs/` cross-reference (e.g. `strategy_rules.md`) is not flagged as a removal (false-positive guard)

### ST-12 — Regression suite runtime budget & trend report (last 90 days)
**Source:** BLG-QA-147
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Trend report produced; QA & Testing Owner sign-off.

### ST-13 — DEV-* deviation recurrence pattern report
**Source:** BLG-QA-141
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Report produced for the current deviation set; Director of Quality sign-off.

### ST-14 — pip-audit trend log across sprint-planning runs
**Source:** BLG-QA-103
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Log convention documented and applied from the next sprint planning onward.

### ST-15 — DoQ sign-off template alignment check (FI-P3-02 wording-only exception)
**Source:** BLG-QA-109
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Comparison performed; template confirmed current or corrected.

### ST-16 — Staging sign-off backlog tracker (FI-P3-02 wording-only AC exceptions)
**Source:** BLG-QA-132
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Tracker created and backfilled where findable; QA Lead sign-off.


## EPIC-04 — Governance Process Debt

**Maps to:** S2-04
**Owner:** Head of Specs Team; PMO Lead

### ST-17 — Quarterly model/prompt-drift compliance attestation log
**Source:** BLG-GOV-242
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Attestation log document created; first entry filed.

### ST-18 — Deprecation header convention for retiring API endpoints
**Source:** BLG-GOV-244
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Convention documented; referenced from `shared_standards.md` or an equivalent canonical location.

### ST-19 — Formal expiry review for §13-adjacent initiatives open more than 2 cycles
**Source:** BLG-GOV-245
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Check specified; would have fired correctly against at least one historical example if run retroactively (or confirmed no qualifying example exists).

### ST-20 — stage4_backlog_slice.md post-gate-correction addendum mechanism
**Source:** BLG-GOV-287
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `design_gate_prompt.md` patched with the addendum mechanism
- Head of Specs Team sign-off

### ST-21 — AI response caching evaluation for morning briefing
**Source:** BLG-GOV-149
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Evaluation document produced covering cache key design, staleness risk, and cost-benefit analysis
- Recommendation: cache / no-cache with rationale
- Backend Engineering Owner and FinOps sign-off

### ST-22 — Gemini AI usage audit-trail retention policy
**Source:** BLG-GOV-203
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Retention policy documented; archival mechanism specified; AI Compliance Officer sign-off.

### ST-23 — Standardise `api_changelog.md` entry template
**Source:** BLG-GOV-205
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Template documented; existing entries conform or a migration note is filed.

### ST-24 — Frame Skill-Silo Alert as workload-composition, not just product-mix
**Source:** BLG-GOV-209
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `roadmap_prompt.md` STEP 7.1 patched (versioned per `CLAUDE.md` §6); Director of HR sign-off.

### ST-25 — Governance-cycle wall-clock cost logging
**Source:** BLG-GOV-210
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Logging convention documented; applied from the next cycle onward.

### ST-26 — Product Value Ratio historical trend row in `velocity_metrics.md`
**Source:** BLG-GOV-215
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Row added retroactively for the last 3 readings; convention documented for future cycles.

### ST-27 — Surface meta-review countdown in every `run_manifest.md`
**Source:** BLG-GOV-217
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `roadmap_prompt.md` STEP 1.1 patched (versioned per `CLAUDE.md` §6) to include the field.

### ST-28 — Data-retention policy for closed-trade and journal records
**Source:** BLG-GOV-252
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Policy documented; no implementation required until data volume warrants action.

### ST-29 — Onboarding checklist for new governance agent roles
**Source:** BLG-GOV-253
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Checklist added to `claude/charter/` or `claude/system/`; Head of Specs Team sign-off.

### ST-30 — Periodic §13 boundary review cadence tied to SI-02's gate history
**Source:** BLG-GOV-255
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Review cadence documented; Strategy Rules & System Intent Owner sign-off.

### ST-31 — Lightweight due-date index for outstanding deferred-patch reminders across cycles
**Source:** BLG-GOV-261
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Index file created and documented; PMO Lead sign-off.

### ST-32 — Agent onboarding runbook for adding a new governance role
**Source:** BLG-GOV-271
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Runbook created; Director of HR sign-off.

### ST-33 — Recurring spec-debt backlog review cadence
**Source:** BLG-GOV-272
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Cadence defined and documented in `backlog_management_prompt.md`; Head of Specs Team confirmation.

### ST-34 — Searchable index of STEP 11.4 meta-review findings across cycles
**Source:** BLG-GOV-275
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Index created and backfilled from existing `meta_review.md` files; Head of Specs Team sign-off.

### ST-35 — Document exact skill-category taxonomy used for Skill-Silo classification
**Source:** BLG-GOV-277
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Taxonomy documented; Metrics Definitions & Analytics Canonical Owner sign-off.

### ST-36 — AI feature cost-vs-value retrospective (6-month actuals vs original estimates)
**Source:** BLG-GOV-299
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Retrospective document filed; FinOps & Resource Architect sign-off.

### ST-37 — Formal alert threshold for the cross-role workload-concentration check
**Source:** BLG-GOV-300
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Assessment filed; threshold confirmed or revised in `roadmap_prompt.md` §7.2; Director of HR sign-off.

### ST-38 — Formalise condensed-tier trigger thresholds beyond the "no new FTE required" test
**Source:** BLG-GOV-247
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Review completed; either a specific prompt change proposed, or an explicit decision recorded that the existing language is fine as-is.

### ST-39 — Formalise a data-volume threshold trigger for the §12.2 "elements that may change" review
**Source:** BLG-GOV-262
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Threshold documented in §12.2; Strategy Rules & System Intent Owner sign-off.

### ST-40 — Formalise Product Value Ratio rolling-window boundary-trade handling in metrics_definitions.md
**Source:** BLG-GOV-276
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Rule documented; Metrics Definitions & Analytics Canonical Owner sign-off.

### ST-41 — strategy_rules.md version cross-reference consistency check in dependent docs
**Source:** BLG-GOV-282
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Check added; first run's findings triaged; Strategy Rules & System Intent Owner sign-off.

### ST-42 — Strategy rules change-justification template
**Source:** BLG-GOV-306
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Template added; applied to the next `strategy_rules.md` version bump; Strategy Rules & System Intent Owner sign-off.


## EPIC-05 — Spec, Tech & Ops Debt

**Maps to:** S2-05
**Owner:** Head of Specs Team; Infrastructure & Operations Owner

### ST-43 — Deprecated/superseded endpoint sunset tracker
**Source:** BLG-SPEC-119
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Tracker added; API Contracts & Documentation Owner sign-off.

### ST-44 — Contract example-payload freshness check against live response shape
**Source:** BLG-SPEC-120
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Check added/scheduled; API Contracts & Documentation Owner sign-off.

### ST-45 — Base44 prompt-version provenance tag on generated components
**Source:** BLG-SPEC-121
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Convention documented in `base44_prompt_template_library.md`; Base44 Frontend Prompt Owner sign-off.

### ST-46 — Base44 regeneration diff checklist — design-token compliance pass
**Source:** BLG-SPEC-122
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Checklist added; Base44 Frontend Prompt Owner sign-off.

### ST-47 — Component prop-naming convention consistency audit
**Source:** BLG-SPEC-123
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Audit complete; convention documented in `design_system.md`; Frontend Specifications & UX Documentation Owner sign-off.

### ST-48 — Gate-metric naming consistency across roadmap, SI-05 digest, and Reports page
**Source:** BLG-SPEC-128
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Naming standardised; Metrics Definitions & Analytics Canonical Owner sign-off.

### ST-49 — Populate Specs_Index.md with the 78 spec files its own freshness check found unregistered
**Source:** BLG-SPEC-135
**Priority:** P3
**Effort:** M (~2-3d)
**Acceptance Criteria:**
- `scripts/check_specs_index_freshness.py` reports 0 unexplained additions after this work
- Head of Specs Team sign-off

### ST-50 — Scope a future migration off Create React App (react-scripts v5)
**Source:** BLG-TECH-11
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Migration scoping document produced (target toolchain recommendation, effort estimate, risk areas identified); Head of Engineering sign-off.

### ST-51 — Unexplained package-lock.json "dev": true churn from the react-router-dom bump
**Source:** BLG-TECH-12
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Root cause confirmed and documented as benign, or a real issue found and fixed.

### ST-52 — Remove unused namesquatted/erroneous npm packages from package.json
**Source:** BLG-TECH-19
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `package.json` no longer lists `x`, `textarea`, or `sqlalchemy` as dependencies
- `package-lock.json` has no residual entries for any of the three
- `CI=false npm run build` succeeds unchanged

### ST-53 — AI cost-threshold alert value review
**Source:** BLG-OPS-106
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Review documented; threshold confirmed or adjusted with rationale.

### ST-54 — AI endpoint (daily-briefing/chat) cost & latency drift monitoring
**Source:** BLG-OPS-112
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Anomaly check scoped and added; confirmed to fire on a simulated cost/latency spike.

### ST-55 — Staging environment data-reset cadence review
**Source:** BLG-OPS-141
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Cadence defined and documented; Infrastructure & Operations Owner sign-off.

### ST-56 — AI feature cost-trend tracking has not kept pace with feature shipping
**Source:** BLG-OPS-150
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Cost-trend document reflects all 6 current AI-invoking endpoints
- Real query data obtained for at least the current quarter
- FinOps & Resource Architect sign-off

---