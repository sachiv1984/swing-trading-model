Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27
Cycle: 2026-07-27__release-v7.9
Release: v7.9

# Stage 4 Backlog Slice — v7.9

15 items, 15 EPICs. Backlog-driven scope (see `release_plan.md` Readiness/Scope for rationale).

---

### EPIC-01 — BLG-FEAT-66 — Watchlist staleness and decay review

**Maps to:** S2-01 | **Owner:** Head of UX & Design; Product Owner | **Priority:** P1 | **Effort:** S (~1 day)

**Problem:** DS-07 (Watchlist Promotion Flow, shipped v3.0) provides a one-click path from screener result to watchlist, but there is no corresponding exit path other than promotion to a trade plan. Tickers can accumulate indefinitely with no forcing function to review or remove them.

**Scope:**
- Track days-on-watchlist per entry (`added_at` timestamp already captured at add time)
- Frontend: staleness indicator (e.g. "45 days, no action") on watchlist entries past a configurable threshold (default 30 days)
- Explicit user action required: Keep (resets the clock) or Remove — no automatic removal

**Acceptance Criteria:**
- AC-01: Watchlist entries display days-since-added
- AC-02: Entries past the staleness threshold are visually flagged
- AC-03: User can explicitly "Keep" (resets staleness clock with a new timestamp) or "Remove" a stale entry
- AC-04: No automatic removal — user decision required in all cases

**Design Gate:** Required — AC-02 (visual flag), AC-03 (interaction) are observable UI.

---

### EPIC-02 — BLG-FEAT-67 — Historical sector/regime exposure trend

**Maps to:** S2-02 | **Owner:** Metrics Definitions & Analytics Owner; Head of UX & Design | **Priority:** P1 | **Effort:** M (~2 days)

**Problem:** `SectorHeatMap` (shipped v6.2) and regime status displays show only the current point-in-time snapshot. There is no way to see whether concentration or regime exposure has been drifting over recent months.

**Scope:**
- Backend: aggregate existing `portfolio_history` + sector/regime data into a rolling time series (weekly or monthly buckets)
- Frontend: trend chart (sector concentration % over time, regime status over time) added alongside the existing `SectorHeatMap` on the Positions or Reports page
- No new inputs — purely a historical view of data already captured

**Acceptance Criteria:**
- AC-01: Sector concentration trend chart renders using existing `portfolio_history` + sector data, no new data collection required
- AC-02: Regime status trend shown over the same time window
- AC-03: Chart handles insufficient-history state gracefully (e.g. fewer than 8 weeks of data)

**Design Gate:** Required — AC-01/AC-02 are chart rendering (visual), AC-03 is an observable UI state.

---

### EPIC-03 — BLG-SPEC-105 — Formalise trade_plan-to-position FK linkage schema

**Maps to:** S2-03 | **Owner:** Data Model & Domain Schema Owner | **Priority:** P2 | **Effort:** M (~2-3 days)

**Problem:** SI-02's gate condition (1) depends entirely on `trade_history.position_id` linking to `trade_plans`, but the linkage itself (relationship, not versioning) is documented only implicitly across `BLG-BE-46`/`BLG-FE-109`'s fix descriptions.

**Scope:** Document the canonical trade_plan↔position linkage schema (cardinality, nullability, backfill posture) in `data_model.md`.

**Acceptance Criteria:**
- AC-01: Schema section added to `data_model.md`
- AC-02: Data Model & Domain Schema Owner sign-off
- AC-03: Cross-referenced from the SI-02 gate note in `current_roadmap.md`

**Design Gate:** Not required — documentation-only, no UI.

---

### EPIC-04 — BLG-FEAT-85 — Monthly P&L CSV export: tax-lot cost-basis reconciliation

**Maps to:** S2-04 | **Owner:** Financial Reporting & Records Owner | **Priority:** P2 | **Effort:** M (~2-3 days)

**Problem:** The v7.8 Monthly P&L CSV export (`BLG-FEAT-81`) reports realized P&L but does not reconcile against a stated tax-lot cost-basis method (FIFO/specific-lot), leaving the export's basis assumption implicit.

**Scope:** Add an explicit cost-basis method disclosure/reconciliation column to the export.

**Acceptance Criteria:**
- AC-01: Export documents its cost-basis method
- AC-02: Reconciles against a manually-verified sample
- AC-03: Financial Reporting & Records Owner sign-off

**Design Gate:** Not required — CSV export column, no in-app UI rendering.

---

### EPIC-05 — BLG-FEAT-87 — "Why is my stop moving" explainer tooltip on the trailing-stop UI

**Maps to:** S2-05 | **Owner:** Head of Engineering; Head of UX & Design | **Priority:** P2 | **Effort:** S (~1-2 days)

**Problem:** The trailing-stop framework (`strategy_rules.md` §7) has non-obvious profit-aware logic (§7.2) and a hard stop-movement constraint (§7.3) that are not explained anywhere in the trade UI.

**Scope:** Add a short explainer tooltip on the position/trade view surfacing the current trailing-stop rule in plain language.

**Acceptance Criteria:**
- AC-01: Tooltip added to the position/trade view
- AC-02: Text reviewed against §7 for accuracy
- AC-03: Product Owner sign-off

**Design Gate:** Required — AC-01 is observable UI (visible rendering/interaction).

---

### EPIC-06 — BLG-BE-73 — Audit trail for manual position overrides

**Maps to:** S2-06 | **Owner:** Financial Reporting & Records Owner | **Priority:** P2 | **Effort:** M (~2-3 days)

**Problem:** Manual position overrides currently leave no audit trail distinguishing a manual edit from a normal lifecycle transition — distinct from `BLG-SEC-14`'s AI-journal-generation audit trail, which covers a different write path.

**Scope:** Add an audit-log entry (who, when, before/after values) whenever a position record is manually edited outside the normal trade lifecycle.

**Acceptance Criteria:**
- AC-01: Audit entries recorded for manual overrides
- AC-02: Financial Reporting & Records Owner sign-off

**Design Gate:** Not required — backend audit logging, no UI.

---

### EPIC-07 — BLG-BE-74 — Nightly backtest data-integrity smoke test as a standing CI gate

**Maps to:** S2-07 | **Owner:** Head of Engineering | **Priority:** P2 | **Effort:** M (~2-3 days)

**Problem:** Nightly-backtest data-integrity issues have been caught by one-off audits three times (`BLG-BE-59`/`60` fast-tracked v7.1, `BLG-BE-63` idempotency audit v7.7) rather than by a standing automated check.

**Scope:** Add a permanent smoke test to the nightly backtest CI job checking the same class of data-integrity invariant found in the prior three incidents.

**Acceptance Criteria:**
- AC-01: Smoke test added to CI
- AC-02: Passes on current data
- AC-03: Head of Engineering sign-off

**Design Gate:** Not required — CI/backend only.

**Notes:** RISK-02 — a newly-surfaced data-integrity defect during this build should be filed as its own backlog item, not treated as blocking this story's own AC.

---

### EPIC-08 — BLG-OPS-121 — Provision a staging credential so SI-02 live gate re-checks don't depend on ad hoc session environment

**Maps to:** S2-08 | **Owner:** Infrastructure & Operations Owner | **Priority:** P2 | **Effort:** S (~1-2 days)

**Problem:** Every recent scheduled roadmap rebalance has found production API credentials absent, meaning the SI-02 gate's "live re-check" instruction has not actually been exercisable this month.

**Scope:** Provision a read-only staging (or scoped production read) credential accessible to governed-routine sessions specifically for gate re-checks.

**Acceptance Criteria:**
- AC-01: Credential provisioned and documented
- AC-02: Next scheduled roadmap rebalance can perform a genuine live SI-02 re-check
- AC-03: Infrastructure & Operations Owner sign-off

**Design Gate:** Not required — infra/credential provisioning, no UI.

---

### EPIC-09 — BLG-QA-124 — Shared cross-EPIC smoke-test tagging for parallel-branch merges

**Maps to:** S2-09 | **Owner:** QA Lead | **Priority:** P2 | **Effort:** M (~2-3 days)

**Problem:** `shared_standards.md` §12 governs merge sequencing and conflict resolution for parallel EPIC branches, but there is no shared smoke-test tag ensuring each merged branch gets at least one common regression pass before the next EPIC's PR opens.

**Scope:** Define a smoke-test tag/suite that runs once per EPIC-branch merge as part of the §12 Rule 3 GOVERNANCE-commit step.

**Acceptance Criteria:**
- AC-01: Tag/suite defined
- AC-02: Documented in `shared_standards.md` §12
- AC-03: QA Lead sign-off

**Design Gate:** Not required — CI/process tooling, no UI.

---

### EPIC-10 — BLG-QA-125 — Pre-commit hook automating the `backend/routers/test.py` registration check

**Maps to:** S2-10 | **Owner:** QA & Testing Owner | **Priority:** P2 | **Effort:** S (~1-2 days)

**Problem:** `CLAUDE.md` §2 requires every new backend route to be registered in `backend/routers/test.py` in the same commit, enforced today only by manual discipline and CI failure after the fact.

**Scope:** Add a pre-commit hook that greps new `@router.*` decorators against `test.py` entries and blocks the commit if one is missing.

**Acceptance Criteria:**
- AC-01: Hook added to `.pre-commit-config` (or equivalent)
- AC-02: Tested against a deliberately-missing case
- AC-03: QA & Testing Owner sign-off

**Design Gate:** Not required — tooling only, no UI.

---

### EPIC-11 — BLG-FE-130 — WCAG contrast checklist addendum for chart colour palettes

**Maps to:** S2-11 | **Owner:** Frontend Specifications & UX Documentation Owner | **Priority:** P2 | **Effort:** S

**Problem:** `design_system.md` v1.4 added a WCAG contrast standard for text and focus indicators, but chart colour palettes are not explicitly covered.

**Scope:** Add a chart-specific contrast checklist item to `design_system.md`'s Accessibility section.

**Acceptance Criteria:**
- AC-01: Checklist item added
- AC-02: Frontend Specifications & UX Documentation Owner sign-off

**Design Gate:** Not required — documentation addendum, no shipped UI change.

---

### EPIC-12 — BLG-OPS-120 — Cost-tag cloud infrastructure spend by EPIC

**Maps to:** S2-12 | **Owner:** FinOps & Resource Architect | **Priority:** P3 | **Effort:** M (~2-3 days)

**Problem:** Skill-Silo workforce economics (STEP 7.1) reasons about story counts only — no cloud infra cost signal feeds into the same workforce-economics picture.

**Scope:** Add EPIC-level cost tags to relevant cloud resources and surface a per-EPIC spend summary.

**Acceptance Criteria:**
- AC-01: Cost tags applied
- AC-02: Summary report available
- AC-03: FinOps & Resource Architect sign-off

**Design Gate:** Not required — infra tagging/reporting, no in-app UI.

---

### EPIC-13 — BLG-FE-129 — Dark-mode acceptance-criteria checklist addendum for Base44 prompt drafts

**Maps to:** S2-13 | **Owner:** Base44 Frontend Prompt Owner | **Priority:** P3 | **Effort:** S

**Problem:** The v7.8 dark-mode contrast audit (`BLG-FE-125`) found and fixed issues after the fact; no standing checklist item asks for explicit dark-mode acceptance criteria up front.

**Scope:** Add a short dark-mode AC checklist item to the Base44 prompt template.

**Acceptance Criteria:**
- AC-01: Checklist item added
- AC-02: Base44 Frontend Prompt Owner sign-off

**Design Gate:** Not required — process template edit, no shipped UI change.

---

### EPIC-14 — BLG-GOV-258 — Displacement debt register — track unused named displacement candidates

**Maps to:** S2-14 | **Owner:** Challenger; Head of Specs Team | **Priority:** P3 | **Effort:** S

**Problem:** STEP 8's "Displacement candidate flag" is recorded per-cycle in `initiative_register.md`, but there is no cross-cycle view of how many named candidates are ever actually displaced versus repeatedly named and never used.

**Scope:** Add a lightweight rolling count/log of named displacement candidates and their eventual disposition.

**Acceptance Criteria:**
- AC-01: Log format documented
- AC-02: Head of Specs Team sign-off

**Design Gate:** Not required — governance process artefact, no UI.

---

### EPIC-15 — BLG-QA-123 — Defined visual-regression baseline refresh cadence for Grid View components

**Maps to:** S2-15 | **Owner:** Head of UX & Design | **Priority:** P3 | **Effort:** S

**Problem:** `BLG-QA-81` established initial visual-regression baselines for contrast-sensitive components, but no cadence exists for refreshing those baselines as the Grid View evolves.

**Scope:** Define a refresh cadence (e.g. every N releases, or on any Grid View design-gate pass) for visual-regression baselines.

**Acceptance Criteria:**
- AC-01: Cadence documented
- AC-02: Head of UX & Design + Director of Quality sign-off

**Design Gate:** Not required — cadence definition/process, no shipped UI change.

---

## Summary

| Metric | Value |
|--------|-------|
| Total EPICs | 15 |
| Total estimated effort | ~26.5 days midpoint |
| Confirmed capacity | ~24-28 days |
| Design Gate required | Yes — EPIC-01, EPIC-02, EPIC-05 |
