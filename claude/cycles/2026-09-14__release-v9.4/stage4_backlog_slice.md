Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-14
Cycle: 2026-09-14__release-v9.4
Release: v9.4

# Backlog Slice — v9.4

<!-- release-plan-marker: RP:v9.4:2026-09-14__release-v9.4 -->

28 stories across 6 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope set to the top of the confirmed ~24–28 day/sprint capacity band per explicit user "use full capacity" instruction (2026-09-14). Ready pool: 74 items / ~65.05 days (largest on record). Selected round-robin across all 13 represented categories, P2-first then oldest-first within category, to fill capacity. 3 selected items (`BLG-FE-174`, `BLG-FEAT-95`, `BLG-AI-05`) carry an observable UI acceptance criterion — `design_gate_required: true`.

---

## EPIC-01 — Backend & Platform Engineering Debt

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Head of Engineering

### ST-01 — DB-level unique constraint on (ticker, entry_date) for open positions
**Source:** BLG-BE-115
**Priority:** P2
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Migration applies cleanly against production-shaped data
- A duplicate insert attempt is rejected at the DB layer with a clear error surfaced to the caller
- No existing duplicate rows confirmed to violate the constraint before applying (see RISK-01 — pre-check must be part of the migration script itself if live DB access is unavailable)

### ST-02 — Nullable trade_plan_id FK migration path
**Source:** BLG-BE-116
**Priority:** P2
**Effort:** M (~2–3 days)
**Acceptance Criteria:**
- Migration approach documented in `data_model.md`, distinguishing "backfill" from "forward-only" options
- Explicit statement of whether backfill is in scope (expected: no, per `BLG-BE-52`'s existing decision) — formalise/cross-reference that decision, not reopen it
- Confirms which approach `BLG-BE-91`'s existing enforcement already assumes

### ST-03 — CI check for the inverse OpenAPI drift case
**Source:** BLG-API-02
**Priority:** P3
**Effort:** M (~1–3 days)
**Acceptance Criteria:**
- New check runs in CI alongside the existing OpenAPI Drift Detection gate
- Any pre-existing inverse-drift gap found is filed as its own `BLG-SPEC-*` item, not silently fixed inline

### ST-04 — Deprecated-endpoint removal-follow-through scan
**Source:** BLG-API-03
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Scan method documented (manual grep acceptable at current scale)
- Any qualifying stale-deprecated endpoint (deprecated > 2 releases ago, no removal follow-up filed) found this run is filed as its own item

### ST-05 — Investigate consolidating the 3 scheduled-job runners into one orchestrator
**Source:** BLG-TECH-20
**Priority:** P3
**Effort:** M (~1–3 days)
**Acceptance Criteria:**
- Inventory of the 3 runners and their trigger mechanisms produced
- Recommendation documented (consolidate now / defer / not worth it) with rationale — spec-only this cycle, no migration performed

---

## EPIC-02 — QA & Test Coverage Debt

**Maps to:** S2-02
**Owner:** QA Testing Owner; Director of Quality

### ST-06 — Add boundary-condition Playwright coverage for Arc5ComplianceSection low-trade-volume advisory
**Source:** BLG-QA-162
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Advisory shown at `total_closed_trades = 19`, hidden at `= 20` (strict `< 20` boundary verified)
- Copy reads "1 closed trade" (singular) at count 1, "0 closed trades" at count 0
- All added scenarios pass in CI

### ST-07 — Add backend pytest coverage for GET /analytics/arc5-compliance total_closed_trades field
**Source:** BLG-QA-163
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- New unit test(s) for `get_arc5_trade_plan_adherence_rate` cover all three return paths (success, zero-trades, `UndefinedTable`)
- Integration assertion confirms `total_closed_trades` is present in the endpoint's response
- New tests pass in CI

### ST-08 — Pinned regression assertion for Settings heading-order fix and TradePlan/Settings aria-labelledby swap
**Source:** BLG-QA-164
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A CI-blocking test fails if the Settings heading-order regresses (h1→h3 skip reintroduced)
- A CI-blocking test fails if any of the 5 controls' `aria-labelledby` association is removed or broken

---

## EPIC-03 — Operations & Security Debt

**Maps to:** S2-03
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect; Cybersecurity & Trust Lead

### ST-09 — Wire the AI endpoint cost/latency anomaly check into a scheduled job and alert channel
**Source:** BLG-OPS-151
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A scheduled job invokes `check_cost_anomaly`/`check_latency_anomaly` against real production data on a defined cadence
- A firing anomaly reaches a real alert channel (Telegram, matching the SI-05/`BLG-OPS-57` precedent), not log-only
- Infrastructure & Operations Owner sign-off
- If live production data access is unavailable in the execution environment, the wiring is delivered and verified against a mocked/simulated feed, and the "runs against real data" sub-criterion is explicitly disclosed as pending rather than claimed complete (see RISK-03)

### ST-10 — Run real Q3 2026 AI cost-trend query against production data
**Source:** BLG-OPS-152
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `docs/ops/ai_feature_cost_trend_2026_q3.md` §3 contains an actual query result for Q3 2026, not an estimate
- Confirms whether `claude_audit_log` carries a column identifying which of the 6 AI-invoking endpoints produced each row; if not, notes that as its own prerequisite gap
- FinOps & Resource Architect sign-off
- If production DB access is unavailable in the execution environment, this is explicitly disclosed (not fabricated) and the existing carried-forward estimate is left in place with the disclosure dated (see RISK-03)

### ST-11 — Rotate and scope-narrow the CI service account token
**Source:** BLG-SEC-35
**Priority:** P2
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Minimum scopes CI workflows actually require are confirmed
- New token in place with confirmed-minimal scope
- All CI workflows still pass with the new token

### ST-12 — Automated secret-scanning pre-commit hook
**Source:** BLG-SEC-36
**Priority:** P2
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Hook/check runs and blocks a deliberately-introduced test secret pattern
- False-positive override procedure documented

---

## EPIC-04 — Spec, Documentation & Financial Reporting Debt

**Maps to:** S2-04
**Owner:** Frontend Specifications & UX Documentation Owner; Metrics Definitions & Analytics Canonical Owner; Financial Reporting & Records Owner

### ST-13 — Framer Motion stagger-delay entrance animations can exceed the 500ms motion-vs-contrast guideline ceiling
**Source:** BLG-SPEC-136
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `design_system.md`'s motion-vs-contrast guideline explicitly addresses delay-based stagger, not duration alone
- The 4 listed components (`SystemStatus.js`, `Reports.js`, `Signals.js`, `RecentTradesWidget.js`) are either brought into compliance or explicitly listed as known non-compliant instances with a target release

### ST-14 — Name the GBP-basis FX-conversion display pattern in design_system.md
**Source:** BLG-SPEC-137
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Pattern documented in `design_system.md` (or equivalent): any GBP-basis financial figure derived from a form that can represent a US-market position must read `fx_rate_used` and divide by it before display
- Both existing precedent instances (Trail Stop tile, trade_plan.md R at Risk) cross-referenced
- Frontend Specifications & UX Documentation Owner sign-off

### ST-15 — Review placement of Appendix D governance metrics in metrics_definitions.md
**Source:** BLG-SPEC-138
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Explicit placement decision recorded (Product Owner + Metrics Definitions & Analytics Canonical Owner): does governance-process metrics content belong in `docs/governance/` instead of a Class 1 API-facing spec
- Content relocated if the decision is to move it

### ST-16 — Reconciliation check: journal-derived P&L vs broker-statement import totals
**Source:** BLG-FR-02
**Priority:** P3
**Effort:** M (~1–2 days, spec/dependency-mapping only this cycle)
**Acceptance Criteria:**
- Reconciliation calculation and acceptable tolerance defined
- Explicit dependency note recorded against `BLG-QA-122`'s blocked status (no broker-import mechanism exists)
- Not blocked on implementation this cycle — spec/dependency-mapping only until `BLG-QA-122` clears

### ST-17 — Carried-forward-loss field on the tax-year P&L statement
**Source:** BLG-FR-03
**Priority:** P3
**Effort:** M (~1–2 days)
**Acceptance Criteria:**
- Carried-forward-loss field present on the tax-year P&L statement
- Calculation behaviour documented, or explicit informational-only status stated for this iteration

---

## EPIC-05 — Governance Process & AI Compliance Debt

**Maps to:** S2-05
**Owner:** PMO Lead; AI Compliance & Governance Officer; FinOps & Resource Architect; Director of HR

### ST-18 — Cross-role escalation response-time tracker
**Source:** BLG-GOV-301
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Tracker aggregating escalation response times by role added, across cycles
- PMO Lead sign-off

### ST-19 — Idea-intake / roadmap-session compute cost attribution
**Source:** BLG-GOV-302
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Lightweight cost-attribution method documented, distinguishing governance-overhead sessions from delivery sessions
- Method applied to at least one cycle retrospectively
- FinOps & Resource Architect sign-off

### ST-20 — Recurring data-density gate trajectory re-estimate cadence
**Source:** BLG-GOV-304
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Recurring cadence defined for re-estimating data-density gate trajectories (e.g. every N scheduled rebalances)
- First re-estimate run under the new cadence
- PMO Lead sign-off

### ST-21 — Quarterly automated re-scan of AI-generated copy for boundary-language drift
**Source:** BLG-AI-04
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Quarterly cadence and scope documented (which templates/screens/AI-surfaced copy are in scope)
- Lightweight, re-usable-each-quarter checklist produced
- First scan scheduled with an owner and date

### ST-22 — In-app disclosure block: advisory-only AI outputs vs deterministic outputs
**Source:** BLG-AI-05
**Priority:** P3
**Effort:** M (~1–3 days)
**Acceptance Criteria:**
- Small, reusable disclosure/badge component designed and documented in a canonical frontend spec
- Applied to at least the daily-briefing surface as a first instance
- **Design-gate note:** this is an observable UI element (a new visible badge/disclosure block) — before execution, the AC must be extended with either Playwright coverage of the badge's presence on the daily-briefing surface, or a recorded staging sign-off, per the CLAUDE.md frontend-visible-change standard. "Documented in a canonical frontend spec" alone does not satisfy that standard.

### ST-23 — Implement generation-time opt-in sampling hook for AI-output boundary-language audits
**Source:** BLG-AI-06
**Priority:** P2
**Effort:** M (~1–2 days)
**Acceptance Criteria:**
- Sampling hook implemented and gated behind an explicit opt-in flag (env var or settings toggle), default off
- Hook is opt-in / sampling-rate-bounded (not full-content logging of every AI response)
- `scripts/run_ai_output_boundary_sample_audit.py` can consume real sampled records from the new store when available
- A genuine (non-illustrative) sample of at least 10 AI outputs can be drawn and scanned using this mechanism
- Documented in the AI-endpoint contract docs and cross-referenced from `BLG-GOV-178`
- `ESC-EXEC-20260910-01` closed as `Resolved` (superseding its interim `Deferred` disposition) once a genuine sample has actually been run using this mechanism, findings filed as backlog items if any

---

## EPIC-06 — Frontend, UX & Product Debt

**Maps to:** S2-06
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design; Product Owner

### ST-24 — Audit Base44 components for orphaned props
**Source:** BLG-FE-173
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Audit list produced for components with 3+ recorded prompt revisions (per the Base44 prompt versioning changelog)
- Confirmed-orphaned props removed with no visual/behavioural regression (existing Playwright coverage passes)

### ST-25 — Standardise the loading-skeleton pattern across screens
**Source:** BLG-FE-174
**Priority:** P3
**Effort:** M (~1–3 days)
**Acceptance Criteria:**
- Canonical loading-skeleton pattern documented in the relevant frontend spec
- All 3 divergent screens (Dashboard, Screener, Journal) use the same pattern
- Playwright visual check or recorded staging sign-off confirms no regression (observable UI change — CLAUDE.md frontend-visible-change standard applies)

### ST-26 — Usability pass on the Arc 5 compliance advisory banner
**Source:** BLG-UX-03
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Review of current banner against original intent and the 3 subsequent revisions completed and documented
- Any recommended change filed as its own item (not fixed inline as part of this review)

### ST-27 — Standard interaction-timing rule for toast notifications
**Source:** BLG-UX-04
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Standard timing rule documented in the relevant frontend spec (e.g. by message length or severity)
- List of non-conforming screens produced for future remediation (documentation only this cycle)

### ST-28 — Minimal "trade plan required before entry" UI soft-nudge
**Source:** BLG-FEAT-95
**Priority:** P2 (corrected from P3 at this document-touch — Skill-Silo mandatory-pull-forward candidate, see `run_manifest.md`)
**Effort:** S (~0.5–1 day)
**Acceptance Criteria:**
- Non-blocking UI nudge (soft warning/confirmation) appears on the position-entry flow when no trade plan is linked
- User can proceed without one (non-blocking) — does not conflict with §13 (no automation of the entry decision itself)
- Playwright coverage confirms the nudge does not block entry (observable UI change — CLAUDE.md frontend-visible-change standard applies)
