**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.5
**Cycle:** 2026-07-02__release-v6.5
**Last Updated:** 2026-07-02
**Sprint Backlog Source:** This slice is authoritative. Sprint Planning Engine reads this file at Phase 2.

---

# v6.5 Backlog Slice — 2026-07-02__release-v6.5

<!-- release-plan-marker: RP:v6.5:2026-07-02__release-v6.5 -->

---

## EPIC-01 — Audit Remediation Cluster

**Purpose:** Close the 10 still-open findings from lifecycle audit AUD-2026-07-01 (v6.4's BLG-GOV-150–153 closed 7 of 17: AUD-002/004/005/008/011/014/017). Includes AUD-006, flagged in the audit's own SLA section as a P0-escalation risk if still open at the next audit.

**Sprint assignment:** Sprint 1

**Maps to:** S2-06, S2-07, S2-08

---

### ST-01 — Lifecycle/prompt/state wording and consistency fixes (BLG-GOV-157)

**Type:** Firm
**Effort:** XS (<1 hour)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-157
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** Three governance wording/consistency findings from AUD-2026-07-01: staging-only AC protocol ambiguity unresolved 2 audit cycles (AUD-007); `FRICTION_LOAD` formula wording ambiguous about its time window (AUD-012); a state file contradicts the audit config on the prior open-item count (AUD-013).

**Acceptance criteria:**
- AC-01: Staging-only AC protocol ambiguity resolved with explicit wording in the relevant governance prompt
- AC-02: `FRICTION_LOAD` formula wording specifies its time window explicitly
- AC-03: State file and audit config open-item counts reconciled to a single consistent value

---

### ST-02 — README.md document hygiene sweep (BLG-GOV-158)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-158
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** Four document-hygiene findings from AUD-2026-07-01: README §4 documents only 1 of 13 governed routines (AUD-006 — Medium effort, flagged as a P0-escalation risk if still open at the next audit); README §2 references a non-existent file path (AUD-009); README.md is 101 days stale (AUD-010); `pmo_lead.md` header fields not bolded per Class 6 header convention (AUD-015).

**Acceptance criteria:**
- AC-01: README §4 lists all governed routines currently in `CLAUDE.md` §1
- AC-02: README §2's referenced file path exists
- AC-03: `README.md` Last Updated date and content reflect current system state
- AC-04: `pmo_lead.md` header fields bolded consistent with other agent charter files

---

### ST-03 — OPERATIONAL_GUIDE/prompt version-sync drift (BLG-GOV-159)

**Type:** Firm
**Effort:** XS (<1 hour)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-159
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** Three version-sync drift findings from AUD-2026-07-01: `OPERATIONAL_GUIDE.md` header/§14 self-row/Change Log top entry version-sync pattern (AUD-001); §14 Roadmap Rebalance Prompt row must be verified against `roadmap_prompt.md`'s actual current version (AUD-003, v8.0 as of `2026-07-02__scheduled`); Metrics owner role-name drift vs `team_charter.md` (AUD-016).

**Acceptance criteria:**
- AC-01: `OPERATIONAL_GUIDE.md` header, §14 self-row, and Change Log top entry show one consistent version number
- AC-02: §14 Roadmap Rebalance Prompt row matches `roadmap_prompt.md`'s actual current version
- AC-03: Metrics owner role name matches `team_charter.md` exactly

---

## EPIC-02 — Backlog Debt Clearance

**Purpose:** Close two backlog items explicitly targeted at v6.5 (endpoint baseline registration, Playwright coverage gap) and resolve the 3-cycle carry-forward BLG-QA-61 disposition.

**Sprint assignment:** Sprint 1

**Maps to:** S2-01, S2-02, S2-03

---

### ST-04 — Add v6.4 endpoint to `api_performance_baseline.md` (BLG-OPS-83)

**Type:** Firm
**Effort:** XS (<1 hour)
**Owner:** Infrastructure & Operations Owner
**Backlog ref:** BLG-OPS-83
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** `GET /strategy/benchmark/open-positions` (shipped v6.4, EPIC-03 BLG-FEAT-54) is not registered in `docs/ops/api_performance_baseline.md`.

**Acceptance criteria:**
- AC-01: Endpoint registered in `api_performance_baseline.md` with measured p50/p95 (minimum 5 warm requests)
- AC-02: Regression threshold documented per the existing dynamic-2x pattern (precedent: BLG-OPS-82)
- AC-03: Infrastructure & Operations Owner sign-off

---

### ST-05 — Playwright coverage for Strategy Benchmark Panel 0 rendering (TEST-GAP-EPIC-03-v64)

**Type:** Firm
**Effort:** XS (<0.5 day)
**Owner:** QA & Testing Owner
**Backlog ref:** TEST-GAP-EPIC-03-v64
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** v6.4 ST-08 (BLG-FEAT-54) added the "Panel 0 — Open Positions" section to the Strategy Benchmark page with an observable rendering AC that was cleared by code review only this sprint (v6.4 EPIC-03 QA evidence log). This item closes that deferred Playwright gap.

**Acceptance criteria:**
- AC-01: Playwright test covering ST-08/AC-01 (Panel 0 conditional rendering — ≥1 position renders, 0 positions omits)
- AC-02: Playwright test covering the Market-filter-only interaction (no Year filter dependency, per ux_spec.md)
- AC-03: Playwright test covering the Panel 0 API-error state ("Open positions temporarily unavailable.")
- AC-04: Tests added to `tests/e2e/strategy-benchmark.spec.js`

---

### ST-06 — Review `signals_scenarios.md` against ST-01 signal sizing model changes (BLG-QA-61)

**Type:** Firm
**Effort:** XS (<1 hour)
**Owner:** QA & Testing Owner; Director of Quality
**Backlog ref:** BLG-QA-61
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** `docs/testing/signals_scenarios.md` may contain scenarios asserting `suggested_shares` values based on the cash-allocation formula that v6.0 ST-01 replaced with risk-based `size_position()` sizing. This item has carried 3 consecutive cycles without resolution (`2026-07-02__release-v6.4` lessons_learnt_closure.md Carry-Forward #1) — promoted to firm scope this cycle per the STEP 1.4a active disposition in `release_plan.md`.

**Acceptance criteria:**
- AC-01: Every scenario in `signals_scenarios.md` referencing `suggested_shares` reviewed against the risk-based sizing formula
- AC-02: Any scenario with stale cash-allocation-based expected values updated
- AC-03: Review outcome ("no changes needed" or updated scenarios) committed and noted in this sprint's QA evidence

---

## EPIC-03 — AI Thesis Feedback Loop

**Purpose:** Address the `2026-07-02__scheduled` rebalance's explicit finding that the Skill-Silo rolling-3-cycle average worsened to 64.8% despite a single U-item pull-forward in v6.4, and its instruction that v6.5 prioritise more than one user-facing item.

**Sprint assignment:** Sprint 1

**Maps to:** S2-04, S2-05

**Design Gate:** Required before sprint planning seals — ST-07 carries an observable UI acceptance criterion (see RISK-03).

---

### ST-07 — Claude thesis generation user feedback mechanism (BLG-FE-46)

**Type:** Firm
**Effort:** S (~1 day)
**Owner:** Base44 Frontend; Head of UX & Design
**Backlog ref:** BLG-FE-46
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-03

**Context:** The Claude thesis generation button (shipped v4.0) produces a thesis with no feedback mechanism — the user cannot signal whether it was useful, edited heavily, or discarded, so the system cannot track thesis quality over time.

**Acceptance criteria:**
- AC-01: Simple feedback UI available after thesis generation ("Useful / Not useful" binary or brief edit indicator)
- AC-02: Feedback data persisted (table or audit log field)
- AC-03: UX reviewed and signed off by Head of UX & Design before sprint planning seals (design gate)

---

### ST-08 — Claude thesis adoption rate metric (BLG-FEAT-41)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Metrics Definitions & Analytics Owner
**Backlog ref:** BLG-FEAT-41
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-03

**Context:** No metric exists tracking whether Claude-generated theses (shipped v4.0) are accepted, edited, or discarded. Adoption rate is an early signal of feature value and cost-per-use justification, and complements ST-07's feedback mechanism.

**Acceptance criteria:**
- AC-01: `thesis_adoption_rate` metric defined in `metrics_definitions.md` (trade plans with non-empty setup_thesis at entry / trade plans with thesis generated)
- AC-02: Query approach documented (`claude_audit_log` join `trade_plans`)
- AC-03: Reviewed by Financial Reporting & Records Owner and Product Owner

---
