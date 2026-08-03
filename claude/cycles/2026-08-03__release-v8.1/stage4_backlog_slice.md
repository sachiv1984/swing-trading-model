Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03
Cycle: 2026-08-03__release-v8.1
Release: v8.1

# Backlog Slice — v8.1

<!-- release-plan-marker: RP:v8.1:2026-08-03__release-v8.1 -->

19 stories across 7 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution).

---

## EPIC-01 — User-Facing Accessibility Fix

**Maps to:** S2-01
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design

**Staging-only ACs:** ST-01 carries an observable UI interaction AC — see RISK-01; Design Gate PASS or Playwright coverage/staging sign-off required before this AC may be considered met (per CLAUDE.md §2).

### ST-01 — Trade Plan tag-suggestion buttons use `onMouseDown`, not keyboard-operable
**Source:** BLG-FE-137
**Effort:** XS
**Acceptance Criteria:**
- Tabbing to a tag suggestion button and pressing Enter/Space adds it (change `onMouseDown` to `onClick`, or add both, in `src/pages/TradePlan.js`, matching `TradeEntry.js`'s existing correct pattern)
- Playwright coverage or a recorded staging sign-off confirms the fix
- Head of UX & Design sign-off

---

## EPIC-02 — Operational Safety

**Maps to:** S2-02
**Owner:** Infrastructure & Operations Owner

### ST-02 — Recurring manual `pg_dump` backup schedule for production Supabase
**Source:** BLG-OPS-127
**Effort:** S
**Acceptance Criteria:**
- Recurring `pg_dump` schedule configured and confirmed running
- Restore procedure documented and dry-run tested against a non-production target
- `database_backup_disaster_recovery_runbook.md` updated to reflect the closed gap
- Infrastructure & Operations Owner sign-off

---

## EPIC-03 — Governance Process Hardening

**Maps to:** S2-03, S2-04, S2-05, S2-06, S2-07, S2-08, S2-09
**Owner:** Product Owner; Challenger; FinOps & Resource Architect; Head of Engineering; Director of HR; AI Compliance & Governance Officer; Head of Specs Team

### ST-03 — Formal sunset criteria for perennially-returning gated backlog items
**Source:** BLG-GOV-280
**Effort:** S
**Acceptance Criteria:**
- Explicit sunset criteria defined (e.g. N consecutive perennial-return cycles with no gate progress triggers a formal Kill decision, not just further parking)
- Criteria applied retroactively to assess `BLG-FEAT-73`/`BLG-FEAT-74`'s current status
- Product Owner sign-off

### ST-04 — Escalation path for Product Value Ratio's persistent Advisory tier
**Source:** BLG-GOV-268
**Effort:** S
**Acceptance Criteria:**
- Sustained-Advisory escalation clause drafted for STEP 2.4 (mirroring the Skill-Silo 3-consecutive-worsening mandatory clause)
- Reviewed with Head of Specs Team
- If adopted, `roadmap_prompt.md` STEP 2.4 updated per the standard governance file edit checklist

### ST-05 — Minimum capacity buffer floor recommendation for sprint planning
**Source:** BLG-GOV-254
**Effort:** S
**Acceptance Criteria:**
- Minimum capacity buffer floor proposed (e.g. a percentage of confirmed capacity) for `sprint_planning_prompt.md` STEP 4.5 to reference
- FinOps & Resource Architect + PMO Lead sign-off

### ST-06 — Technical debt registry (consolidated cross-cycle view)
**Source:** BLG-GOV-273
**Effort:** M
**Acceptance Criteria:**
- Consolidated registry built, pulling technical-debt-classified items from across `BLG-BE-*`/`BLG-FE-*`/`BLG-OPS-*` backlog categories into one view
- Head of Engineering sign-off

### ST-07 — Skill-Silo mitigation: rotate execution-heavy story assignment pattern
**Source:** BLG-GOV-246
**Effort:** M
**Acceptance Criteria:**
- Lightweight rotation guideline documented (e.g. a soft target that at least 1 in 3 release cycles leads with execution-heavy scope by default)
- Guideline explicitly tied to the STEP 7.1 Skill-Silo alert as its trigger condition
- Documented in `release_planning_prompt.md` or a referenced companion doc

### ST-08 — Automated PII scan gate for new backend endpoints
**Source:** BLG-GOV-241
**Effort:** M
**Acceptance Criteria:**
- Lightweight CI check added that scans new/changed response schemas in `docs/reference/openapi.yaml` for common PII field-name patterns and flags them for manual review
- Confirmed to fire on a deliberately-introduced PII-shaped field in a test PR

### ST-09 — Governed write path for a non-empty, unversioned Now-horizon carry-forward
**Source:** BLG-GOV-240
**Effort:** S
**Acceptance Criteria:**
- One remediation path selected and implemented (either a narrow `shared_standards.md` §17 standing-authority extension, or a `roadmap_prompt.md` STEP 8.1 condition-1 amendment) via the standard governance file edit checklist (version bump, `OPERATIONAL_GUIDE.md` §14 update, `prompt_change_log.md` entry)
- A non-empty, unversioned Now-horizon carry-forward no longer requires an out-of-band write to receive a formal version label

---

## EPIC-04 — QA Process & Debt Closure

**Maps to:** S2-10, S2-11, S2-12, S2-13
**Owner:** Director of Quality; QA Lead; QA & Testing Owner

**Staging-only ACs:** ST-10 is itself a staging-only verification task (no CI-reproducible equivalent) — see acceptance criteria below.

### ST-10 — Staging sign-off: custom price alert live delivery firing
**Source:** BLG-QA-115
**Effort:** XS
**Acceptance Criteria:**
- Human staging run performed: create a price alert with a threshold already crossed by the live market price, trigger `POST /alerts/evaluate` on staging
- Confirm alert deactivates (`active=false`, `triggered_at` set), a `notifications` row is created (`alert_type='custom_price_alert'`), and Telegram delivery is received
- Staging run dated in the ST-02 (EPIC-02, v7.5) DoQ sign-off block (`qa_evidence_EPIC-02.md`)
- This backlog item closed/archived once recorded

### ST-11 — Recurring pre-sprint-planning endpoint test coverage audit
**Source:** BLG-QA-113
**Effort:** S
**Acceptance Criteria:**
- Recurring (pre-sprint-planning) audit added comparing all `@router.get/post/put/delete` decorators against `test.py` entries
- Run once against current state with results recorded (pass, or gaps filed)

### ST-12 — Cross-EPIC deviation (DEV-*) consolidation review across cycles
**Source:** BLG-QA-129
**Effort:** S
**Acceptance Criteria:**
- Periodic review added consolidating DEV-* records across recent cycles to surface recurring patterns
- First consolidation review performed
- Director of Quality sign-off

### ST-13 — Post-parallelization Playwright shard balance audit
**Source:** BLG-QA-131
**Effort:** S
**Acceptance Criteria:**
- Shard runtimes audited post-parallelization (REC-CI-01 follow-up)
- Shard runtimes confirmed balanced, or rebalanced if skewed
- QA Lead sign-off

---

## EPIC-05 — Spec Debt: SI-02 Definitional Clarity

**Maps to:** S2-14, S2-15, S2-16
**Owner:** Product Owner; Strategy Rules & System Intent Owner; Head of UX & Design

### ST-14 — Revisit SI-02 Gate Status Condition 2/3 threshold definitions
**Source:** BLG-SPEC-72
**Effort:** S
**Acceptance Criteria:**
- AC-01: Gate Condition 2 and 3 definitions explicitly product-reviewed and documented in the canonical spec, no longer marked as an engine-filled gap
- AC-02: If thresholds change, `src/pages/Reports.js`'s `SI02GateStatusSection` updated to match, with Playwright coverage for the new thresholds

### ST-15 — Explicit §13 continuity note for v6.9 on-demand recheck
**Source:** BLG-SPEC-82
**Effort:** S
**Acceptance Criteria:**
- Short explicit §13 continuity note added confirming the on-demand recheck (`BLG-FEAT-64`) doesn't introduce new automation/prediction surface beyond SI-01's existing gate
- Note added to `strategy_rules.md` or a linked decision doc
- Strategy Rules & System Intent Owner sign-off

### ST-16 — Formally define SI-02 condition-3 "sufficient data" threshold
**Source:** BLG-SPEC-86
**Effort:** S
**Acceptance Criteria:**
- Exact trade-count/window threshold the `behavioural-drift` endpoint uses internally to move off `insufficient_data` documented in `strategy_rules.md` §5 (Arc 5) or a linked spec
- Cross-referenced from `current_roadmap.md`'s SI-02 structured field

---

## EPIC-06 — Backend Hardening

**Maps to:** S2-17, S2-18
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner

### ST-17 — Standardise pagination pattern across list endpoints (consolidated)
**Source:** BLG-BE-47
**Effort:** M
**Acceptance Criteria:**
- Canonical cursor-based pagination pattern documented in `backend_engineering_patterns.md`
- Shared pagination helper/dependency built, documented, with at least one existing endpoint migrated as a reference example
- At least the next 2 new/modified list endpoints follow the canonical pattern
- Not required to retrofit all existing endpoints in one pass

### ST-18 — `trade_plans.position_id` historical backfill design
**Source:** BLG-BE-55
**Effort:** S
**Acceptance Criteria:**
- Backfill scoping document produced covering the 11 historically-affected rows: technical approach, effort estimate, and risk of a future backfill
- Recorded as an explicit, documented trade-off (not a silent gap) alongside `BLG-BE-52`'s original "no backfill" resolution
- Data Model & Domain Schema Owner sign-off

---

## EPIC-07 — Cross-EPIC Execution State Structural Fix

**Maps to:** S2-19
**Owner:** Head of Engineering

### ST-19 — Implement per-EPIC `execution_state.json` files (Option 1)
**Source:** BLG-GOV-284
**Effort:** L
**Acceptance Criteria:**
- Per-EPIC `execution_state/EPIC-xx.json` files in place; no shared `execution_state.json` write surface remains across EPIC branches
- Computed, regenerate-on-read summary view built for Delivery Verification/Post-Ship Closure consumption, confirmed never hand-mergeable
- `shared_standards.md` §12 Rule 2 retired and §12 updated to reference the new mechanism, in the same commit (Rules 1/3 remain active)
- Head of Engineering sign-off
- (Retrospective confirmation of reduced per-branch conflicts deferred to the next multi-EPIC sprint's delivery verification — not required for this story's own closure)

---

## Capacity Summary (see `release_plan.md §Capacity Check` for full detail)

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days |
| Total estimated effort (in-scope) | ~25.75 days |
| Utilisation | ~92-107% |
| Over-allocation | No |
