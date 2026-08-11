Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-11
Cycle: 2026-08-11__release-v8.6
Release: v8.6

# Backlog Slice — v8.6

<!-- release-plan-marker: RP:v8.6:2026-08-11__release-v8.6 -->

26 stories across 6 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution).

---

## EPIC-01 — User-Facing Product Features

**Maps to:** S2-01
**Owner:** Product Owner

### ST-01 — Trade plan completion rate tracking
**Source:** BLG-FEAT-32
**Priority:** P2 (escalated from P3, 2026-08-11 rebalance)
**Effort:** S
**Acceptance Criteria:**
- Trade plan completion rate (`plans_created`, `plans_completed`, `plans_abandoned`, `completion_rate`) computable and displayable
- Optional: segmented by setup quality score tier

### ST-02 — AI-assisted setup thesis digest at order placement
**Source:** BLG-FEAT-56
**Priority:** P1
**Effort:** M
**Note:** Gate condition (AI adoption window + established usage patterns) confirmed met by Product Owner disposition, 2026-08-11 — see `decisions--2026-08-11__release-v8.6.md`.
**Acceptance Criteria:**
- Digest (setup thesis + key risk factors) renders at the order-placement step using the existing Claude thesis generation service (v4.0 infrastructure)

---

## EPIC-02 — Trade-Plan Data Integrity Foundation

**Maps to:** S2-02
**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner

### ST-03 — Enforce trade-plan linkage at position entry + DB-level safeguard against orphaned trade_plans rows
**Source:** BLG-BE-91
**Priority:** P1 (escalated 2026-08-11 rebalance — named structural response to the Skill-Silo mandatory pull-forward finding)
**Effort:** M
**Acceptance Criteria:**
- Entry-flow linkage confirmed enforced (staging-verified) — a trade plan is linked at position creation as the default path
- DB-level safeguard (constraint, trigger, or scheduled integrity check) implemented and tested to flag/prevent new orphaned `trade_plans` rows going forward
- Data Model, Domain & Schema Owner + Product Owner sign-off

---

## EPIC-03 — Frontend Design Consistency & Correctness Carryover

**Maps to:** S2-03
**Owner:** Frontend Specifications & UX Documentation Owner

### ST-04 — Register remaining unregistered shadcn design tokens in tailwind.config.js
**Source:** BLG-FE-147
**Priority:** P2
**Effort:** M
**Sequencing note:** Should land before/alongside ST-05 — coverage needs the tokens registered first.
**Acceptance Criteria:**
- `bg-card`, `text-card-foreground`, `bg-popover`, `text-primary`, `bg-secondary`, `bg-accent`, `bg-destructive`, `border-border`, `bg-input`, `ring-ring` (and any other affected token-derived classes found in scope) compile to a non-empty CSS rule, verified via a real `tailwindcss` build
- No visual regression at any confirmed-affected call site — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

### ST-05 — Playwright coverage for the remaining -muted/muted-foreground call sites left untested by v8.5/ST-06
**Source:** BLG-FE-148
**Priority:** P2
**Effort:** S
**Acceptance Criteria:**
- Each of `Select`, `Tabs`, `Sheet`, `Toast`, `Toggle` has at least one Playwright test asserting the real post-fix computed colour at a confirmed-affected call site
- `DialogDescription`'s actual exposure (or non-exposure) of the default `text-muted-foreground` styling is confirmed and documented, with a test added if any live call site exposes it

### ST-06 — Fix 6 drift instances against the v6.7 canonical secondary-text token
**Source:** BLG-FE-149
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- All 6 instances (`Positions.js`, `PositionCard.js`, `WatchlistRow.js`, `Layout.js` search-affordance/⌘K badge, `Reports.js`, `WhatsNewCard.js`) use exactly `text-slate-600 dark:text-slate-400` (or the equivalent `isDark` ternary form)
- No visual regression — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

### ST-07 — Design decision: should modals/dialogs support light theme?
**Source:** BLG-FE-150
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- A decision record is produced either confirming dark-only modals as intentional (documented in `design_system.md`) or directing a follow-up implementation item to make modals theme-aware

### ST-08 — Switch Layout.js's dark-class document.documentElement sync to useLayoutEffect
**Source:** BLG-FE-153
**Priority:** P4
**Effort:** XS
**Acceptance Criteria:**
- Either the hook is switched to `useLayoutEffect`, or a code comment explains why the current `useEffect` timing is intentionally acceptable

### ST-09 — Correct st15_nav_bar_redesign_exploration.md's nav group/page counts against live NAV_GROUPS
**Source:** BLG-FE-154
**Priority:** P2
**Effort:** S
**Acceptance Criteria:**
- `st15_nav_bar_redesign_exploration.md`'s group/page counts match the live `NAV_GROUPS` array in `src/Layout.js` exactly
- `navigation.md`'s staleness is either fixed or explicitly flagged with a follow-up item

### ST-10 — Migrate CohortAnalysis.js from client-side computation to GET /analytics/cohort
**Source:** BLG-FE-155
**Priority:** P2
**Effort:** S
**Acceptance Criteria:**
- `CohortAnalysis.js` sources cohort groupings, win rates, avg R-multiple, and net P&L from `GET /analytics/cohort` rather than client-side `buildCohorts()`
- No client-side R-multiple computation remains in this component, per `analytics.md` §15's canonical rule
- No visual regression — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

---

## EPIC-04 — Backend & Financial Correctness

**Maps to:** S2-04
**Owner:** Financial Reporting & Records Owner; Cybersecurity & Trust Lead

### ST-11 — get_regime_distribution's NULL-exclusion documented behaviour is dead code
**Source:** BLG-BE-88
**Priority:** P2
**Effort:** S
**Acceptance Criteria:**
- `get_regime_distribution()`'s documented NULL-handling behaviour matches what the code actually does, verified against a real fetch-failure scenario (either persist NULL on fetch failure, or correct the docs to state the real `risk_off`-default behaviour)

### ST-12 — Multi-currency cost-basis rounding consistency check
**Source:** BLG-BE-92
**Priority:** P2
**Effort:** M
**Acceptance Criteria:**
- Cost-basis rounding audited across UK (.L) and US market positions; any inconsistency found is fixed
- Financial Reporting & Records Owner sign-off

### ST-13 — Closed-trade export completeness check against tax-year boundary edge cases
**Source:** BLG-BE-93
**Priority:** P2
**Effort:** S
**Acceptance Criteria:**
- Boundary-case test added and passing for trades closing exactly on a tax-year boundary date (no silent omission or double-count)
- Financial Reporting & Records Owner sign-off

### ST-14 — check_dependency_vuln_rescan.py silently treats a failed audit tool as "zero findings"
**Source:** BLG-SEC-29
**Priority:** P2
**Effort:** S
**Acceptance Criteria:**
- A simulated tool failure (missing lockfile, non-JSON output, or nonzero exit) is surfaced as a distinguishable failure/inconclusive state in `dependency-vuln-rescan.yml`, not silently reported as "0 findings"

---

## EPIC-05 — QA Test-Coverage Debt Closure

**Maps to:** S2-05
**Owner:** Director of Quality

### ST-15 — Add endpoint-level regression test for GET /analytics/tag-performance's ensure_trade_plans_table call
**Source:** BLG-QA-136
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- A test calls the actual `GET /analytics/tag-performance` router endpoint and asserts `ensure_trade_plans_table()` is invoked before the query

### ST-16 — Add Playwright coverage for setNarrativeField AI-draft-badge clearing on the 3 non-setup_thesis fields
**Source:** BLG-QA-137
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Playwright coverage exists and passes for all 4 narrative fields' (`setup_thesis`, `entry_rationale`, `confirmation_criteria`, `early_exit_conditions`) AI-draft-badge-clearing behaviour

### ST-17 — Add unit tests for scripts/check_dependency_vuln_rescan.py
**Source:** BLG-QA-138
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- `tests/` has a test file covering the script's core parsing/dedup logic with at least 3 scenarios: baseline-hit, new-finding, malformed/error-shaped input

### ST-18 — Document one-directional limitation of test_alerts_service.py's sys.modules restore fixture
**Source:** BLG-QA-139
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- The fixture's code comment or docstring explicitly states the one-directional scope of the protection it provides

---

## EPIC-06 — Operations & Governance Debt Closure

**Maps to:** S2-06
**Owner:** Head of Specs Team

### ST-19 — Align api-key-cross-environment-check.yml's alert-step grep with the skip-guard's ::error:: prefix
**Source:** BLG-OPS-136
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- The missing-secrets skip-guard path's Telegram alert includes the specific error detail, verified once fixed

### ST-20 — Document CVE-2026-4539 ignore rationale in dependency-vuln-rescan.yml
**Source:** BLG-OPS-137
**Priority:** P4
**Effort:** XS
**Acceptance Criteria:**
- `dependency-vuln-rescan.yml`'s `CVE-2026-4539` ignore has an inline rationale comment or cross-reference to `vulnerability-scan.yml`'s

### ST-21 — Confirm dependency-vuln-rescan.yml runs successfully post-merge
**Source:** BLG-OPS-138
**Priority:** P2
**Effort:** XS
**Acceptance Criteria:**
- A confirmed-successful `dependency-vuln-rescan.yml` run exists post-merge, closing v8.5/ST-04's originally-deferred AC

### ST-22 — File retroactive DEV record for the dark-mode/Radix-portal Layout.js fix
**Source:** BLG-GOV-294
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- A `DEV-*` record exists for the `src/Layout.js` dark-mode/Radix-portal fix, matching the format used for `DEV-REPORTS-ST01-02`

### ST-23 — shared_standards_changelog.md missing v3.27 entry
**Source:** BLG-GOV-295
**Priority:** P3
**Effort:** XS
**Acceptance Criteria:**
- `shared_standards_changelog.md`'s top row matches `shared_standards.md`'s current version (v3.27, §20 addition)

### ST-24 — execution_state.json's deviations_filed field is used as "check performed" not literally "filed"
**Source:** BLG-GOV-296
**Priority:** P2
**Effort:** M
**Acceptance Criteria:**
- `execution_state_schema.json` and `shared_standards.md` document the field's actual, current meaning without contradiction
- No qa_evidence log can simultaneously say "deviations filed: None" while every story's `deviations_filed` reads `true`, going forward
- Head of Specs Team sign-off

### ST-25 — Annotate BLG-FE-146/BLG-FE-139 with 2026-08-10 trigger-condition re-check
**Source:** BLG-GOV-297
**Priority:** P4
**Effort:** XS
**Acceptance Criteria:**
- Both items carry the 2026-08-10 re-check confirmation inline in `backlog.md`

### ST-26 — Correct BLG-GOV-288's Acceptance Criteria text (says STEP 0, actual fix is STEP 7)
**Source:** BLG-GOV-298
**Priority:** P4
**Effort:** XS
**Acceptance Criteria:**
- `BLG-GOV-288`'s AC text matches the actual, correct implementation site (STEP 7)
