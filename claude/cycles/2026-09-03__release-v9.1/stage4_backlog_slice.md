Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-03
Cycle: 2026-09-03__release-v9.1
Release: v9.1

# Backlog Slice — v9.1

<!-- release-plan-marker: RP:v9.1:2026-09-03__release-v9.1 -->

41 stories across 5 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope widened to the top of the confirmed ~24–28 day/sprint capacity band per explicit user "use full capacity" instruction (2026-09-03). No ungated build-and-ship U-item was available this cycle (all 15 P1 items are Arc 5/SI-02/SI-05/PO-02 gate-conditional; the sole ungated P2 feature candidate, `BLG-FEAT-92`, was reconciled this session as a `BLG-FEAT-30` sub-scope and excluded — see `run_manifest.md`). Scope instead consolidates frontend accessibility fixes, backend reliability/tech-debt cleanup, QA/test coverage, and governance/spec process debt — including resolution of all 3 outstanding passed-target items named in `backlog_health_20260903.md`.

---

## EPIC-01 — Frontend Accessibility & UI Consolidation

**Maps to:** S2-01
**Owner:** Frontend Specifications & UX Documentation Owner; Director of Quality

### ST-01 — Fix DashboardHome "AI Advisory" badge colour-contrast violation
**Source:** BLG-FE-165
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- axe-core no longer reports a `color-contrast` violation for this badge
- `KNOWN_VIOLATIONS["DashboardHome"]`'s `color-contrast` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

### ST-02 — Add accessible names to TradePlan select elements
**Source:** BLG-FE-166
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- axe-core no longer reports a `select-name` violation on TradePlan
- `KNOWN_VIOLATIONS["TradePlan"]`'s `select-name` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

### ST-03 — Add discernible text to Settings page combobox buttons
**Source:** BLG-FE-167
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- axe-core no longer reports a `button-name` violation on Settings
- `KNOWN_VIOLATIONS["Settings"]`'s `button-name` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

### ST-04 — Add labels to Settings page form inputs
**Source:** BLG-FE-168
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- axe-core no longer reports a `label` violation on Settings
- `KNOWN_VIOLATIONS["Settings"]`'s `label` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

### ST-05 — Fix Settings page subtitle colour-contrast violation
**Source:** BLG-FE-169
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- axe-core no longer reports a `color-contrast` violation for the Settings subtitle
- `KNOWN_VIOLATIONS["Settings"]`'s `color-contrast` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

### ST-06 — Consolidate PositionSizingWidget.js / WhatIfSizingPreview.js debounced-fetch boilerplate
**Source:** BLG-TECH-14
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `PositionSizingWidget.js` and `WhatIfSizingPreview.js` share the debounce/fetch/session-storage logic via one hook
- Existing Playwright coverage for both components (`position-sizing-concentration.spec.js`, `what-if-sizing-preview.spec.js`, `smoke-critical-paths.spec.js`) passes unchanged
- Frontend Specifications & UX Documentation Owner sign-off

### ST-07 — Add keyboard-navigation requirements section for table-based page specs
**Source:** BLG-SPEC-99
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- Section added to at least Positions, Trades, and Red Flag Journal specs

---

## EPIC-02 — Backend Reliability & Technical Debt

**Maps to:** S2-02
**Owner:** Backend Engineering Patterns Owner; Head of Engineering

### ST-08 — Fix npm dependency tree production-build regression after routine npm update
**Source:** BLG-TECH-18
**Priority:** P2
**Effort:** M (~1-2 days)
**Acceptance Criteria:**
- `npm update`'s full candidate list from `quarterly_dependency_upgrade_cadence_policy.md` §3.1 applied and `CI=false npm run build` succeeds
- Root cause of the `eslint-config-react-app` resolution failure documented (not just worked around)
- Full Playwright E2E suite re-verified passing against the updated dependency tree

### ST-09 — Log sector-concentration adjustment's fail-open exception handler
**Source:** BLG-TECH-16
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Exception is logged (level appropriate to a fail-open path, e.g. warning) with enough context to diagnose (ticker/sector where available)
- No change to the fail-open return behaviour itself
- Existing tests still pass

### ST-10 — Consolidate 4 independent sector-lookup implementations
**Source:** BLG-TECH-13
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Exactly one sector-lookup implementation exists in the codebase; the other three call sites delegate to it
- All 4 existing test suites (`test_pre_entry_validation.py`, `test_compliance_recheck.py`, `test_portfolio_risk_sector.py`, `test_sizing_concentration.py`) pass unchanged in behaviour (same assertions, potentially updated patch targets)
- Backend Engineering Patterns Owner sign-off

### ST-11 — Move raw SQL execution out of analytics.py/digest.py routers into the database layer
**Source:** BLG-BE-110
**Priority:** P3
**Effort:** L (~3-5 days)
**Acceptance Criteria:**
- Zero `cursor.execute()`/`conn.execute()` calls remain in `backend/routers/analytics.py` and `backend/routers/digest.py`
- All existing tests for these routers' endpoints continue to pass unchanged
- No new raw SQL introduced in the service layer either — `database.py` remains the sole SQL layer per the established pattern

---

## EPIC-03 — QA & Test Coverage

**Maps to:** S2-03
**Owner:** Director of Quality; QA & Testing Owner

### ST-12 — Add Playwright coverage for Arc5ComplianceSection's events_per_week value formatting
**Source:** BLG-QA-154
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- New Playwright scenario asserts the rendered `events_per_week` text matches the expected `fmtCount` output for a known mock value
- Test passes against current implementation

### ST-13 — Add Playwright coverage for Arc5ComplianceSection's top_rule_breach text formatting
**Source:** BLG-QA-155
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- New Playwright scenario asserts the rendered `top_rule_breach` text matches the expected `fmtText` output (underscores replaced with spaces) for a known mock value
- Test passes against current implementation

### ST-14 — Add Playwright coverage for Arc5ComplianceSection's null-value handling
**Source:** BLG-QA-156
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- New Playwright scenario asserts `"—"` renders for at least one `null` field covering each of `fmtRate`/`fmtCount`/`fmtText`
- Test passes against current implementation

### ST-15 — Build a quality trend index aggregating DEV-* records over time
**Source:** BLG-QA-130
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- Index created and backfilled from available cycle history
- Director of Quality sign-off

### ST-16 — Definition-of-Done compliance spot-check across the last 5 cycles
**Source:** BLG-QA-142
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Spot-check complete
- findings documented
- Director of Quality sign-off

### ST-17 — Spot-check Tier 1/Tier 2 DoQ severity-labelling consistency
**Source:** BLG-QA-108
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Spot-check completed and documented
- any labelling drift found is either corrected going forward or explicitly justified

### ST-18 — Define regression suite runtime budget & reporting
**Source:** BLG-QA-134
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Budget defined
- reporting added
- QA & Testing Owner sign-off

---

## EPIC-04 — Governance Process Debt & Overdue Dispositions

**Maps to:** S2-04
**Owner:** Head of Specs Team; PMO Lead; Strategy Rules & System Intent Owner

### ST-19 — Fix governance_sync.yml auto-close gap for split work/completion commits
**Source:** BLG-GOV-314
**Priority:** P2
**Effort:** S (~0.5-1d)
**Acceptance Criteria:**
- A story completed via the commit→push→get-SHA→separate-governance-commit pattern has its GitHub issue auto-closed by `governance_sync.yml` without manual intervention
- A story that ends up `blocked_backend`/`blocked_decision` (rather than `done`) after its work commit is pushed does NOT have its issue auto-closed, even if no `execution_state.json` entry exists yet at the moment the work commit's own push triggers the workflow
- Existing anti-premature-closure protection (`BLG-GOV-285` — a delegation-record-only commit must not close the issue) remains intact

### ST-20 — Document convention for "Signed off by: PENDING" placeholders in Class 3 docs
**Source:** BLG-GOV-310
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- Convention documented (in `shared_standards.md` or equivalent canonical location)
- Head of Specs Team sign-off

### ST-21 — Add ST-06 §13 CONDITIONAL clearance to strategy_rules.md §13.5 roster
**Source:** BLG-GOV-311
**Priority:** P3
**Effort:** XS (~15min)
**Acceptance Criteria:**
- `strategy_rules.md` §13.5's roster table includes a ST-06/BLG-FEAT-90 row pointing at the CONDITIONAL review document
- Edit committed under Strategy Rules & System Intent Owner authority, in a session/prompt whose write scope explicitly covers `claude/strategy/`
- If `strategy_rules.md`'s version is bumped: CLAUDE.md §6 governance file edit checklist steps 1–4 completed in the same commit

### ST-22 — Fix recurrence-check false positive — require reading the named target file directly
**Source:** BLG-GOV-312
**Priority:** P3
**Effort:** S (~0.5 day)
**Acceptance Criteria:**
- `lessons_learnt_prompt.md §3.7` gains an explicit "read the named target file directly" step
- Standard CLAUDE.md §6 governance file edit checklist applied (version bump, `OPERATIONAL_GUIDE.md` §14, `prompt_change_log.md` entry)
- Head of Specs Team sign-off

### ST-23 — AI feature usage quarterly review (BLG-GOV-63 mandate)
**Source:** BLG-GOV-74
**Priority:** P2
**Effort:** S (~0.5 day)
**Acceptance Criteria:**
- Quarterly audit log review completed; findings documented
- Anomalies (if any) filed as BLG items
- Next review date recorded (2026-11-29)

### ST-24 — Correct trade_plan.md §5.1 stale "Risk/Reward Notes" field reference
**Source:** BLG-SPEC-131
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- §5.1's field table accurately reflects the live form
- any other section referencing `risk_reward_notes` reconciled or explicitly confirmed still accurate
- Head of Specs Team sign-off

### ST-25 — Document PositionSizingWidget baseline in trade_plan.md
**Source:** BLG-SPEC-132
**Priority:** P3
**Effort:** S (~0.5-1d)
**Acceptance Criteria:**
- `trade_plan.md` has a dedicated `PositionSizingWidget` baseline subsection documenting fields, debounce behaviour, and the `POST /portfolio/size` contract
- Frontend Specifications & UX Documentation Owner sign-off

### ST-26 — Physically create the Displacement Debt Register and close ESC-EXEC-20260727-02
**Source:** BLG-GOV-264
**Priority:** P3
**Effort:** XS
**Note:** Half-achieved already — `roadmap_prompt.md` STEP 8's prompt-wiring action (v9.15→v9.16) is done; only the physical file creation remains, deferred to this story because `execution_prompt.md`'s write scope does not permit Sprint Execution to write `claude/roadmap/*`. Carried via `ESC-EXEC-20260818-02` (`claude/cycles/2026-08-17__release-v8.9/execution_escalations.md`), Open/non-blocking.
**Acceptance Criteria:**
- `claude/roadmap/displacement_debt_register.md` created with the seeded content (per `roadmap_prompt.md` STEP 8's create-if-absent spec)
- `ESC-EXEC-20260727-02` and `ESC-EXEC-20260818-02` both closed

### ST-27 — Scope governed-vs-ad-hoc backlog scope visibility tally
**Source:** BLG-GOV-238
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Tally mechanism scoped
- first data point recorded retroactively for v7.1/this cycle where determinable

### ST-28 — Give Specs_Index.md a proper Changelog table
**Source:** BLG-SPEC-117
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `docs/specs/Specs_Index.md` has a `## Changelog` table or companion changelog file
- `**Last Updated:**` header field is a single line, no `prior —` chaining
- Head of Specs Team sign-off

---

## EPIC-05 — Spec & Knowledge Debt / AI Governance Register

**Maps to:** S2-05
**Owner:** Head of Specs Team; AI Compliance & Governance Officer

### ST-29 — Consolidate duplicate empty-state pattern specs
**Source:** BLG-SPEC-98
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- Duplicate definitions removed from at least 3 page specs
- `design_system.md` remains the single source

### ST-30 — Build canonical AI feature touchpoint register with per-feature §13 classification
**Source:** BLG-GOV-266
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- Register created and covers all currently-shipped AI touchpoints
- AI Compliance & Governance Officer sign-off

### ST-31 — Spec-to-backlog traceability audit
**Source:** BLG-SPEC-125
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- Audit complete
- orphans resolved
- Head of Specs Team sign-off

### ST-32 — Quarterly retrospective: estimated vs. actual effort bands
**Source:** BLG-GOV-259
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Retrospective cadence documented
- FinOps & Resource Architect sign-off

### ST-33 — Automated Specs_Index.md freshness check against live spec files
**Source:** BLG-GOV-274
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Check added
- Head of Specs Team sign-off

### ST-34 — Add worked example of the ATR-based sizing edge case to strategy_rules.md
**Source:** BLG-SPEC-101
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Worked example added
- Strategy Rules & System Intent Owner sign-off
- no functional/behavioural change (documentation only)

### ST-35 — Formalise minimum-interval guideline between scheduled rebalances
**Source:** BLG-GOV-208
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Guideline documented in `claude/charter/team_charter.md` or `CLAUDE.md` §5
- Director of HR + Head of Specs Team sign-off

### ST-36 — Base44 generation failure-mode log
**Source:** BLG-GOV-267
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Log created
- at least the known recurring modes (dark-mode class pairs, contrast) backfilled
- Base44 Frontend Prompt Owner sign-off

### ST-37 — Canonical "win rate" vs "hit rate" definitions
**Source:** BLG-SPEC-100
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Canonical definitions added
- at least the highest-traffic specs (Performance Analytics, Reports) reconciled to use them consistently

### ST-38 — Formal definition for the "90-day trade window" cited in SI-02 gate readings
**Source:** BLG-SPEC-127
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Definition added
- Metrics Definitions & Analytics Canonical Owner sign-off

### ST-39 — Effort-band accuracy retrospective
**Source:** BLG-GOV-211
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- First retrospective produced
- process documented for repeat

### ST-40 — Extract PVR and Skill-Silo metrics from rebalance prose into structured state fields
**Source:** BLG-GOV-307
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `last_rebalance_pvr` and `last_skill_silo_rolling_avg` are present as top-level numeric fields in `.claude_current_state.json` after the next `run roadmap` invocation
- Both fields are documented in `claude/schemas/state_field_owners.json`
- `last_rebalance_outcome`'s existing prose summary is unchanged in content (fields are additive, not a replacement)
- Head of Specs Team sign-off

### ST-41 — Canonical glossary consolidation
**Source:** BLG-SPEC-126
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- Glossary created
- Head of Specs Team sign-off

---
