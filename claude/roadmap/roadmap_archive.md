**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-03 (post-ship closure 2026-07-02__release-v6.5 — RA:v6.5 retired)

# Roadmap Archive — Momentum Trading Assistant

This document is the permanent record of completed and killed roadmap items retired from `claude/roadmap/current_roadmap.md`. Items are listed in retirement order, most recent first.

Entries are append-only. Do not edit existing entries.

---

## RA:v6.5 — Audit Debt Clearance, Backlog Debt Clearance & AI Thesis Feedback Loop

**Original roadmap location:** §1 Current Version
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-07-03
**Shipped version:** v6.5
**Cycle reference:** 2026-07-02__release-v6.5
**Verification report:** claude/cycles/2026-07-02__release-v6.5/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-07-03

### Original Roadmap Entry

**v6.4** — Audit Remediation, Security Hardening & Strategy Benchmark Enhancement — ✅ Shipped 2026-07-02 — cycle: 2026-07-02__release-v6.4
**Next planned release:** v6.5 — Audit Debt Clearance, Backlog Debt Clearance & AI Thesis Feedback Loop — cycle: 2026-07-02__release-v6.5

<!-- roadmap-annotation-marker: RA:v6.5:2026-07-02__release-v6.5 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-07-02__release-v6.5
- Plan published: 2026-07-02
- Cycle folder: claude/cycles/2026-07-02__release-v6.5/
- Backlog slice: claude/cycles/2026-07-02__release-v6.5/stage4_backlog_slice.md
- Status at annotation: Committed

**Verified:** 2026-07-03 (post-ship closure 2026-07-02__release-v6.5) — verification report: `claude/cycles/2026-07-02__release-v6.5/verification_report.md`. Full v6.5 scope (8 stories, 3 EPICs — AUD-2026-07-01 governance/lifecycle debt clearance, backlog debt clearance (api_performance_baseline.md registration + Playwright coverage + signals_scenarios.md review), Claude thesis feedback mechanism + adoption rate metric) delivered; see `docs/product/changelog.md#v6.5`.

---

## RA:v6.4 — Production Correctness Fast-Track (Audit Remediation, Security Hardening & Strategy Benchmark Enhancement)

**Original roadmap location:** §1 Current Version / §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-07-02
**Shipped version:** v6.4
**Cycle reference:** 2026-07-02__release-v6.4
**Verification report:** claude/cycles/2026-07-02__release-v6.4/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-07-02

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v6.4:2026-07-02__release-v6.4 -->

### v6.4 — Production Correctness Fast-Track — ✅ Complete — Shipped 2026-07-02 — cycle: 2026-07-02__release-v6.4

**Added:** 2026-07-01 (roadmap rebalance 2026-07-01__scheduled — STEP 8.0 mandatory fast-track)

| BLG ID | Title | Priority | Effort | Type | Status |
|--------|-------|----------|--------|------|--------|
| BLG-BE-40 | Signal generation reads deprecated `tickers` table instead of `ticker_universe` | P1 | XS | D | ✅ Shipped |

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-07-02__release-v6.4
- Plan published: 2026-07-02
- Cycle folder: claude/cycles/2026-07-02__release-v6.4/
- Backlog slice: claude/cycles/2026-07-02__release-v6.4/stage4_backlog_slice.md
- Status at annotation: Committed

**Verified:** 2026-07-02 (post-ship closure 2026-07-02__release-v6.4) — verification report: `claude/cycles/2026-07-02__release-v6.4/verification_report.md`. Full v6.4 scope (13 stories, 3 EPICs — production correctness, AI security hardening, AUD-2026-07-01 lifecycle-audit remediation, Strategy Benchmark Open Positions panel, UX/QA polish) delivered; see `docs/product/changelog.md#v6.4`.

---

## RA:v6.3 — Strategy Benchmark, AI Security & Quality Infrastructure

**Original roadmap location:** §1 Current Version / §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-30
**Shipped version:** v6.3
**Cycle reference:** 2026-06-26__release-v6.3
**Verification report:** claude/cycles/2026-06-26__release-v6.3/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-30

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v6.3:2026-06-26__release-v6.3 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-06-26__release-v6.3
- Plan published: 2026-06-26
- Cycle folder: claude/cycles/2026-06-26__release-v6.3/
- Backlog slice: claude/cycles/2026-06-26__release-v6.3/stage4_backlog_slice.md
- Status at annotation: Shipped 2026-06-30 (cycle 2026-06-26__release-v6.3)

---

## RA:v6.2 — Production Strategy Parity & AI Intelligence

**Original roadmap location:** §3 Delivery Plan — Horizon: Now (v[TBD] section)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-25
**Shipped version:** v6.2
**Cycle reference:** 2026-06-24__release-v6.2
**Verification report:** claude/cycles/2026-06-24__release-v6.2/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-25

### Original Roadmap Entry

**Added:** 2026-06-23 (user request — production_strategy.py gap analysis)

These six items close the gap between the live application and the `production_strategy.py` backtest logic, and layer in AI decision support. P1 items (BLG-FEAT-46–49) form a prerequisite cluster; P2 items (BLG-FEAT-50–51) depend on the P1 cluster completing first.

| BLG ID | Title | Priority | Effort | Type | Status |
|--------|-------|----------|--------|------|--------|
| BLG-FEAT-46 | Add nightly trailing stop computation for open positions | P1 | M | U | Queued |
| BLG-FEAT-47 | Add month-end rebalance exit signal generation | P1 | M | U | Queued |
| BLG-FEAT-48 | Implement inverse-volatility position sizing for signal-driven entries | P1 | M | U | Queued |
| BLG-FEAT-49 | Add risk-off exit alerts for existing positions | P1 | S | U | Queued |
| BLG-FEAT-50 | Build AI daily briefing endpoint and dashboard panel | P2 | M | U | Queued — depends on BLG-FEAT-46/47/49 |
| BLG-FEAT-51 | Build conversational AI trade advisor | P2 | M | U | Queued — depends on BLG-FEAT-50 |

---

## RA:v6.1 — Governance Correctness, CI Quality & User Value Foundation

**Original roadmap location:** §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-23
**Shipped version:** v6.1
**Cycle reference:** 2026-06-22__release-v6.1
**Verification report:** claude/cycles/2026-06-22__release-v6.1/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-23

### Original Roadmap Entry

**Added:** 2026-06-22 (rebalance 2026-06-22__scheduled — DL-053; STEP 8.1 Option a)
**Skill-Silo ceiling:** 40% G+D+P stories per sprint (STEP 7.1)

| BLG ID | Title | Priority | Effort | Type | Status |
|--------|-------|----------|--------|------|--------|
| BLG-GOV-132 | Release planning: emit explicit Design Gate Required flag for UI-facing scope | P1 | S | G | Firm — Correctness Fast-Track (STEP 8.0; DL-052) |
| BLG-GOV-133 | Sprint planning: enforce hard gate on design_gate_status at STEP -1 preflight | P1 | S | G | Firm — Correctness Fast-Track (STEP 8.0; DL-052) |
| BLG-QA-60 | Playwright CI registration gap (morning-briefing.spec.js, screener-quality.spec.js) | P2 | M | D | Firm — no-further-deferral carry-forward |
| BLG-FE-76 | Portfolio sector heat-map visualization | P2 | M | U | Firm — Product Value Alert pull-forward |
| BLG-GOV-131 | Governance overhead ceiling metric and accountability mechanism | P2 | S | G | Firm — v6.1 target confirmed (promoted IW-20260619-01; DL-049) |
| BLG-FE-78 | Trade gate proximity indicator on dashboard | P3 | S | U | Firm — STEP 5 Challenger PVC outcome (DL-054) |
| BLG-OPS-73 | api_performance_baseline.md: add row for PATCH /trades/{trade_id}/costs | P3 | XS | D | Firm — spec compliance advisory |
| BLG-FEAT-25/PT-04 | Setup Quality Score (deterministic win-rate from own trade history) | P1 | M | U | **Conditional** — Gate: ≥20 closed trades (currently ~13; projected ~2026-07-02). PMO Lead to re-verify count at v6.1 sprint planning. |

> **STEP 8.2 note:** BLG-FE-52 and BLG-FE-53 were referenced as SI-02 frontend candidates in the prior session context but were found in `backlog_archive.md` (pre-design docs shipped v4.4). SI-02 frontend implementation BLG items do not yet exist. Assess at v6.1 release planning once PT-04 gate review is complete.

> **User value commitment (STEP 5 Challenger PVC):** v6.1 sprint planning must include BLG-FE-76 and BLG-FE-78 as firm scope — not conditional, not deferred. Challenger Clearance Statement accepted on this basis (DL-054).

> **Release Plan:** cycle_id=2026-06-22__release-v6.1 — Published 2026-06-22. 4 EPICs: EPIC-01 (Governance Correctness, 3 stories), EPIC-02 (CI Quality, 2 stories), EPIC-03 (User Value, 2 stories), EPIC-04 (Conditional PT-04, 2 stories). 7 firm stories + 2 conditional stories = 9 total. design_gate_required=true. Capacity check: warn (phasing required). Slice: claude/cycles/2026-06-22__release-v6.1/stage4_backlog_slice.md. (RA:v6.1:2026-06-22__release-v6.1)

✅ **Complete — Shipped 2026-06-23 — cycle: 2026-06-22__release-v6.1** — 9/9 stories delivered; Verified; zero deviations; autonomous class sign-off misapplication (EPIC-03/04) resolved via retrospective DoQ counter-sign at delivery verification; PT-04 gate cleared (15 trades confirmed at sprint planning).

---

## RA:v5.9 — Red Flag Journal UX Improvements, SI-05 Effectiveness Review & Governance Housekeeping

**Original roadmap location:** §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-18
**Shipped version:** v5.9
**Cycle reference:** 2026-06-17__release-v5.9
**Verification report:** claude/cycles/2026-06-17__release-v5.9/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-18

### Original Roadmap Entry

**Target release:** v5.9
**Added:** 2026-06-17 (rebalance 2026-06-17__scheduled — STEP 8.1 Option (a) PO decision)
**Theme:** Close outstanding UX debt on Red Flag Journal, consume SI-05 effectiveness review outputs, clear governance complexity simplification items.

**Firm scope (gate confirmed cleared before sprint open):**

| Item | Description | Gate |
|------|-------------|------|
| BLG-FE-64 | Red Flag Journal visual design review pre-brief | 2026-06-21 — clears before any sprint open |
| BLG-FE-41 | Red Flag Journal visual design review | 2026-06-21 — clears before any sprint open |
| BLG-OPS-70 | SI-05 deep link AC-04 staging verification (FRONTEND_URL production confirm) | ~2026-06-23 (next digest delivery) |
| BLG-GOV-125 | Governance simplification candidate 1 (GCA-2026-06-17) | Ready now |
| BLG-GOV-126 | Governance simplification candidate 2 (GCA-2026-06-17) | Ready now |
| BLG-GOV-127 | Governance simplification candidate 3 (GCA-2026-06-17) | Ready now |
| BLG-GOV-128 | Governance simplification candidate 4 (GCA-2026-06-17) | Ready now |
| BLG-GOV-129 | Governance simplification candidate 5 (GCA-2026-06-17) | Ready now |

**Conditional scope (gate must be confirmed cleared at release planning):**

| Item | Description | Gate | Classification per STEP 1.4b |
|------|-------------|------|------------------------------|
| BLG-GOV-112 | SI-05 effectiveness review protocol execution | 2026-07-04 | Conditional — within v5.9 sprint window |
| BLG-GOV-113 | SI-05 digest actionability metric definition | 2026-07-04 | Conditional — within v5.9 sprint window |
| BLG-GOV-115 | SI-05 effectiveness review outputs — BLG-GOV-115 sub-scope | 2026-07-04 | Conditional — within v5.9 sprint window |
| BLG-OPS-59 | SI-05 latency review (post-effectiveness review) | 2026-07-04 | Conditional — within v5.9 sprint window |
| BLG-GOV-130 | SI-05 Phase 2 activation decision (new — filed this rebalance) | 2026-07-04 | Conditional — within v5.9 sprint window |

Execution notes: Cycle 2026-06-17__release-v5.9; Plan published 2026-06-17; 11/11 stories shipped (EPIC-01 governance simplification SC-03–SC-07; EPIC-02 QA/audit/UX); zero deviations; zero returns. RA:v5.9 complete. Shipped 2026-06-18.

---

## RA:v4.9 — Security/CI Hardening & SI-05 Phase 1

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-02
**Shipped version:** v4.9
**Cycle reference:** 2026-06-02__release-v4.9
**Verification report:** claude/cycles/2026-06-02__release-v4.9/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-02

### Original Roadmap Entry

v4.9 Security/CI Hardening & SI-05 Phase 1. EPIC-01: npm devDependency HIGH CVE remediation (BLG-OPS-49) — 21 HIGH CVEs cleared via npm audit fix + overrides; 6 moderate remain (CRA chain, non-production); security_register.md Audit 001 updated; Anthropic SDK upgrade 0.40.0 → 0.105.2 (BLG-OPS-50) — requirements.txt updated; 447 tests passing; Messages API changelog reviewed (no breaking changes); staging validation deferred BLG-OPS-52. EPIC-02: Real Postgres CI service wired Phase B (BLG-QA-40) — postgres:15 service container; DATABASE_URL injected; 13 pre-existing Phase B test isolation failures surfaced and fixed; Phase A unaffected; schema lifecycle column smoke tests (BLG-QA-41) — tests/test_schema.py; skips Phase A, passes Phase B. EPIC-03: roadmap_prompt.md STEP 8.1 Empty Now Horizon gate strengthening (BLG-GOV-78) — STEP 8.1 converted to soft gate; both decision options documented; v6.7→v6.8; OPERATIONAL_GUIDE.md v4.25→v4.26. EPIC-04 (ST-06/ST-07 SI-05 Phase 1, BLG-GOV-67) gate-deferred at planning — gate clears 2026-06-21. 5/5 in-scope stories delivered. Zero spec deviations. Verified 2026-06-02. completed_cycle_count = 35.

---

## RA:v4.8 — Governance Hardening, Ops/Security Debt & SI-05 Phase 1

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-02
**Shipped version:** v4.8
**Cycle reference:** 2026-06-01__release-v4.8
**Verification report:** claude/cycles/2026-06-01__release-v4.8/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-02

### Original Roadmap Entry

v4.8 Governance Hardening, Ops/Security Debt & SI-05 Phase 1. EPIC-01: §13 register completion (BLG-GOV-69) — OPERATIONAL_GUIDE §14 updated, all 7 Class 6 prompts verified in §13 and §14; agent charter header compliance remediation (BLG-GOV-70) — pre-met in v4.5, verified across all 23 agent files; AUD-2026-05-30-006 gap resolution verification (BLG-GOV-72) — all 3 v4.4 deferred patches confirmed resolved in v4.5. Sprint close governance patch: execution_prompt.md v3.34→v3.35 (LL-v4.8-EX-01 — commit SHA record immediately after push). EPIC-02: Build minutes monitoring policy (BLG-OPS-46) — build_minutes_monitoring_policy.md v1.0 created; dependency audit (BLG-OPS-47) — security_register.md v1.0; pip clean, 45 npm vulns (21 HIGH devDep); BLG-OPS-49/50 filed; coverage matrix + v4.7 contract verification (BLG-QA-39) — playwright_coverage_matrix.md v1.1; GET /reports/monthly-pnl v0.6 verified; SI-04 endpoint contract pre-authored (BLG-SPEC-43) — strategy_version_comparison_contract.md v0.1.0 + openapi.yaml placeholder. EPIC-03 (SI-05 Phase 1, BLG-GOV-67) deferred_at_planning — gate NOT MET (clears 2026-06-21). 7/7 in-scope stories delivered. Zero spec deviations. Verified 2026-06-02. completed_cycle_count = 34.

---

## RA:v4.7 — Arc 5 Completion Pre-work, Staged Verifications & Aged Backlog Clearance

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-01
**Shipped version:** v4.7
**Cycle reference:** 2026-05-31__release-v4.7
**Verification report:** claude/cycles/2026-05-31__release-v4.7/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-01

### Original Roadmap Entry

v4.7 Arc 5 Completion Pre-work, Staged Verifications & Aged Backlog Clearance. EPIC-01 SI-04 §13 Formal Pre-Assessment: §13 review applied; determination PASS; 6 binding conditions documented; Arc 5 completion path cleared; si04_section13_preassessment.md produced (BLG-GOV-62). EPIC-02 Arc 5 Compliance Score in Monthly P&L: compliance_summary field (validation_pass_rate, override_count, red_flag_events_count, most_frequent_rule_breach) added to GET /reports/monthly-pnl; field renamed strategy_compliance → compliance_summary; 2 unit tests + SC-REP-05a/05b Playwright scenarios (BLG-FEAT-38). EPIC-03 Staging Verifications & Ops Housekeeping: RENDER_STAGING_DEPLOY_HOOK confirmed; code-change deploy and docs-only filter verified (BLG-OPS-28); all 5 DS-07 SI-02 columns and 3 indexes confirmed on staging (BLG-OPS-44); severity column, default assignment, backfill confirmed (BLG-OPS-45); Render 7-day log retention documented; database audit tables confirmed durable; policy: no additional archiving required (BLG-OPS-31). EPIC-04 Cost & UX Assessments: Anthropic API no upgrade required; $5/month trigger threshold defined (BLG-OPS-37); PreEntryValidationPanel UX reviewed; 3 improvement candidates ranked; BLG-FE-56/57/58 filed (BLG-FE-49). 8/8 firm stories delivered. Zero spec deviations. Verified 2026-06-01. completed_cycle_count = 33.

---

## RA:v4.0 — Release Annotation

**Original roadmap location:** §1 Current Version header (roadmap annotation block)
**Status at retirement:** ✅ Complete — annotation retired post-ship
**Retired from active roadmap:** 2026-05-25
**Shipped version:** v4.0 (2026-05-25)
**Cycle reference:** 2026-05-22__release-v4.0
**Verification report:** claude/cycles/2026-05-22__release-v4.0/verification_report.md
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-25

### Original Roadmap Entry

v4.0 Arc 5 Analytics Foundation + Spec Closure + Gemini Compliance: Arc 5 compliance analytics (GET /analytics/arc5-compliance — 5 metric fields; Arc5ComplianceSection.js); SI-01→SI-03 Playwright integration (8 scenarios); ticker symbol validation (POST /ticker-universe 422 gate); red flag endpoint security review (PASS); starlette CVE remediation (1.0.1); Gemini Flash base wiring (POST /trade-plans/{plan_id}/generate-thesis); gemini_audit_log (90-day retention); cost tracking ($0.075/$0.30 per M tokens); CI/CD staging auto-deploy (path-filtered workflow). 11/11 firm stories delivered. EPIC-04 PT-04 conditional deferred (gate not met — <20 closed trades, 4th deferral). Verified 2026-05-25. completed_cycle_count = 26.

---

## RA:v3.9 — Release Annotation

**Original roadmap location:** §1 Current Version header (roadmap annotation block)
**Status at retirement:** ✅ Complete — annotation retired post-ship
**Retired from active roadmap:** 2026-05-22
**Shipped version:** v3.9 (2026-05-22)
**Cycle reference:** 2026-05-21__release-v3.9
**Verification report:** claude/cycles/2026-05-21__release-v3.9/verification_report.md
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-22

### Original Roadmap Entry

v3.9 Screener Quality & Reliability + Arc 5 Red Flag Journal + Governance Patches: Yahoo Finance crumb/401 retry + exponential backoff (ST-01); sector/industry restored (ST-02); DAY ticker removed (ST-03); degraded-run banner (ST-04); .L suffix stripped from Ticker Universe (ST-05); company_name column + CSV backfill (ST-06); Arc 5 SI-03 Red Flag Journal backend + frontend (ST-07/08); 5 governance carry-forward patches (ST-09/10/11/12). Zero deviations. Verified 2026-05-22. completed_cycle_count = 25.

---

## RA:v3.8 — Release Annotation

**Original roadmap location:** §1 Current Version header (roadmap annotation block)
**Status at retirement:** ✅ Complete — annotation retired post-ship
**Retired from active roadmap:** 2026-05-21
**Shipped version:** v3.8 (2026-05-20)
**Cycle reference:** 2026-05-19__release-v3.8
**Verification report:** `claude/cycles/2026-05-19__release-v3.8/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-21

### Annotation at retirement

<!-- roadmap-annotation-marker: RA:v3.8:2026-05-19__release-v3.8 — COMPLETE -->

**Execution notes (v3.8 — Complete):**
- Cycle: 2026-05-19__release-v3.8
- Plan published: 2026-05-19
- Cycle folder: claude/cycles/2026-05-19__release-v3.8/
- Backlog slice: claude/cycles/2026-05-19__release-v3.8/stage4_backlog_slice.md
- Status: ✅ Complete — shipped 2026-05-20
- Verification: Verified_with_deviations (8/8 stories; 1 P3 deviation resolved; DoQ + PO sign-off 2026-05-20)
- Scope delivered: EPIC-04 (BLG-FEAT-22 Ticker Universe Management page; BLG-GOV-24 governance debt), EPIC-03 (BLG-FEAT-23 setup type field; BLG-FE-36 news context panel; BLG-FEAT-24 AI thesis generation), EPIC-01 (SI-01 §13 gate PASS + backend pre-entry validation + frontend panel)
- Scope deferred: EPIC-02 (PT-04 Setup Quality Score — formally parked by PO decision 2026-05-19; gate not met ×3 consecutive cycles)

---

## RA:v3.7 — Release Annotation

**Original roadmap location:** §1 Current Version header (roadmap annotation block)
**Status at retirement:** ✅ Complete — annotation retired post-ship
**Retired from active roadmap:** 2026-05-19
**Shipped version:** v3.7 (2026-05-18)
**Cycle reference:** 2026-05-18__release-v3.7
**Verification report:** `claude/cycles/2026-05-18__release-v3.7/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-19

### Annotation at retirement

<!-- roadmap-annotation-marker: RA:v3.7:2026-05-18__release-v3.7 — COMPLETE -->

**Execution notes (v3.7 — Complete):**
- Cycle: 2026-05-18__release-v3.7
- Plan published: 2026-05-18
- Cycle folder: claude/cycles/2026-05-18__release-v3.7/
- Backlog slice: claude/cycles/2026-05-18__release-v3.7/stage4_backlog_slice.md
- Status: ✅ Complete — shipped 2026-05-18
- Verification: Verified (8/8 stories; 0 deviations; DoQ + PO sign-off 2026-05-18)
- Scope delivered: EPIC-01 (BLG-FE-33 signal watchlisted status + PATCH endpoint + Add to Watchlist CTA; BLG-FE-34 trade plan signal context panel), EPIC-03 (execution_prompt.md patches ×3; qa_evidence_template.md BLG-GOV-19 criterion 3 fail-path), EPIC-04 (BLG-QA-20 conftest consolidation; BLG-OPS-16 pycache git hygiene + BLG-FE-35 font staging; BLG-GOV-23 scored_initiatives.md refresh)
- Scope deferred: EPIC-02 (PT-04 Setup Quality Score — gate not met; <20 closed trades at v3.7 sprint planning; deferred to v3.8; two consecutive conditional defers)

---

## RA:v3.5 — Release Annotation + Arc 3 Full Completion

**Original roadmap location:** §8 Release Summary annotation block + §5 Arc 3 section
**Status at retirement:** ✅ Complete — annotation retired post-ship; Arc 3 fully complete
**Retired from active roadmap:** 2026-05-15
**Shipped version:** v3.5 (2026-05-15)
**Cycle reference:** 2026-05-15__release-v3.5
**Verification report:** `claude/cycles/2026-05-15__release-v3.5/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-15

### Annotation at retirement

<!-- roadmap-annotation-marker: RA:v3.5:2026-05-15__release-v3.5 — COMPLETE -->

**Execution notes (v3.5 — Complete):**
- Cycle: 2026-05-15__release-v3.5
- Plan published: 2026-05-15
- Cycle folder: claude/cycles/2026-05-15__release-v3.5/
- Backlog slice: claude/cycles/2026-05-15__release-v3.5/stage4_backlog_slice.md
- Status: ✅ Complete — shipped 2026-05-15
- Verification: Verified (13/13 stories; 0 deviations; DoQ + PO sign-off 2026-05-15)
- Scope delivered: EPIC-01 (IT-06 §13 PASS + backend + frontend, Arc 3 complete), EPIC-02 (Arc 4 foundation: arc4_data_requirements.md v1.0 + PO-01 backend + frontend), EPIC-03 (BLG-SPEC-29/30/31, BLG-QA-19), EPIC-04 (BLG-GOV-22 sprint_planning_prompt.md v3.1, execution_prompt.md v3.20)
- Scope deferred: entry_delta_pct null (planned_entry_price not yet snapshotted — not a deviation per arc4_data_requirements.md §3.1)

---

## RA:v3.3 — Release Annotation

**Original roadmap location:** §1 Current Version header (roadmap annotation block)
**Status at retirement:** ✅ Complete — annotation retired post-ship
**Retired from active roadmap:** 2026-05-13
**Shipped version:** v3.3 (2026-05-13)
**Cycle reference:** 2026-05-09__release-v3.3
**Verification report:** `claude/cycles/2026-05-09__release-v3.3/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-13

### Annotation at retirement

<!-- roadmap-annotation-marker: RA:v3.3:2026-05-09__release-v3.3 — COMPLETE -->

**Execution notes (v3.3 — Complete):**
- Cycle: 2026-05-09__release-v3.3
- Plan published: 2026-05-09
- Cycle folder: claude/cycles/2026-05-09__release-v3.3/
- Backlog slice: claude/cycles/2026-05-09__release-v3.3/stage4_backlog_slice.md
- Status: ✅ Complete — shipped 2026-05-13
- Verification: Verified_with_deviations (14/17 stories; 4 P3 deviations accepted; DoQ + PO sign-off 2026-05-13)
- Scope delivered: EPIC-01 (IT-01 backend — DS-05 lifecycle state machine), EPIC-02 (IT-02/IT-03 backend — grace period alerts + stop trail), EPIC-03 (research view spec closure — BLG-SPEC-24/25/26, BLG-FE-28, BLG-QA-14/15/16/17, BLG-OPS-15, BLG-SEC-06, BLG-GOV-20), EPIC-04 (governance patches OA-01–05, BLG-GOV-19, BLG-FEAT-13, BLG-FEAT-21 backend)
- Scope deferred: IT-01/02/03 frontend (ST-03/05/07) → v3.4; BLG-FEAT-21 frontend → v3.4

---

## v3.1 — Arc 2 Trade Plan Foundation (RA:v3.1)

**Original roadmap location:** §1 Current Version + §8 Release Summary + §4 Priority 2 Arc 2 section (annotation RA:v3.1)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-05-05
**Shipped version:** v3.1 (2026-05-05)
**Cycle reference:** 2026-04-29__release-v3.1
**Verification report:** `claude/cycles/2026-04-29__release-v3.1/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-05

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v3.1:2026-04-29__release-v3.1 — COMPLETE -->

**Execution notes (v3.1 — Complete):**
- Cycle: 2026-04-29__release-v3.1
- Plan published: 2026-04-29
- Cycle folder: claude/cycles/2026-04-29__release-v3.1/
- Backlog slice: claude/cycles/2026-04-29__release-v3.1/stage4_backlog_slice.md
- Status: ✅ Complete — shipped 2026-05-05
- Verification: Verified (14/14 stories; no spec deviations; DoQ + PO sign-off 2026-05-05)
- Scope delivered: EPIC-01 (PT-01 Trade Plan Object full — data model, backend CRUD, frontend), EPIC-02 (PT-02 Pre-Trade Research View backend), EPIC-03 (DS-04 Earnings Calendar, BLG-FE-20 UK screener fix, BLG-QA-10/11 screener QA docs), EPIC-04 (BLG-FEAT-19 Monthly P&L report, BLG-SEC-03/04+BLG-GOV-17 security docs, CF-01/CF-02 governance patches)
- Scope deferred: PT-02 frontend (Pre-Trade Research View UI) → v3.2; PT-03 (Prospective Heat at Entry) → v3.2; PT-05 (Pre-Trade Entry Checklist) → v3.2+

---

## v3.0 — Arc 1 Screener Engine & Results Page (RA:v3.0)

**Original roadmap location:** §1 Current Version + §8 Release Summary + §4 Priority 2 Arc 1 section (annotation block RA:v3.0)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-28
**Shipped version:** v3.0 (2026-04-27)
**Cycle reference:** 2026-04-25__release-v3.0
**Verification report:** `claude/cycles/2026-04-25__release-v3.0/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-04-28

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v3.0:2026-04-25__release-v3.0 — COMPLETE -->

**Execution notes (v3.0 — Complete):**
- Cycle: 2026-04-25__release-v3.0
- Plan published: 2026-04-25
- Cycle folder: claude/cycles/2026-04-25__release-v3.0/
- Backlog slice: claude/cycles/2026-04-25__release-v3.0/stage4_backlog_slice.md
- Status: ✅ Complete — shipped 2026-04-27
- Verification: Verified (16/16 stories; no open deviations)
- Scope delivered: EPIC-01 (DS-01 screener engine), EPIC-02 (DS-02/DS-07/BLG-FE-18 screener frontend), EPIC-03 (BLG-OPS-12/14, TEST-GAP-ST14, BLG-FE-19), EPIC-04 (execution_prompt patches, streak metric, model version contract)
- Scope deferred: DS-04 (Earnings Calendar) → v3.1

---

## v2.9 — Arc 1 Foundation: Stock Discovery & Screening Spec & Infrastructure (RA:v2.9)

**Original roadmap location:** §4 Priority 2 Arc 1 section (annotation block RA:v2.9)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-28
**Shipped version:** v2.9 (2026-04-24)
**Cycle reference:** 2026-04-22__release-v2.9
**Verification report:** `claude/cycles/2026-04-22__release-v2.9/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure v3.0 2026-04-28

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v2.9:2026-04-22__release-v2.9 — COMPLETE -->

**Execution notes (v2.9 — Complete):**
- Cycle: 2026-04-22__release-v2.9
- Plan published: 2026-04-22
- Cycle folder: claude/cycles/2026-04-22__release-v2.9/
- Backlog slice: claude/cycles/2026-04-22__release-v2.9/stage4_backlog_slice.md
- Status: ✅ Complete — shipped 2026-04-24
- Verification: Verified_with_deviations (DEV-01 P3 accepted; BLG-FE-18 filed; resolved in v3.0)
- Scope delivered: EPIC-01 (Arc 1 specs: BLG-SPEC-21/22/23, BLG-FE-17), EPIC-02 (DS-03/05/06 implementation), EPIC-03 (governance/QA infrastructure: BLG-GOV-16, BLG-QA-08/09), EPIC-04 (governance debt + quick wins: BLG-GOV-14/15, BLG-FE-15, BLG-AI-01, TEST-GAP-EPIC-04)
- Scope deferred: DS-01 (screener engine) and DS-02 (screener results page) → v3.0 (delivered)

---

## v2.8 — Frontend Completion, Test Quality & AI Journal Feature (RA:v2.8)

**Original roadmap location:** §1 Current Version + §3 Delivery Plan — Horizon: Now (annotation block RA:v2.8)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-20
**Shipped version:** v2.8 (2026-04-20)
**Cycle reference:** 2026-04-17__release-v2.8
**Verification report:** `claude/cycles/2026-04-17__release-v2.8/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-04-20

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v2.8:2026-04-17__release-v2.8 — COMPLETE -->

**Execution notes (v2.8 — Complete):**
- Cycle: 2026-04-17__release-v2.8
- Plan published: 2026-04-17
- Shipped: 2026-04-20
- Cycle folder: claude/cycles/2026-04-17__release-v2.8/
- Backlog slice: claude/cycles/2026-04-17__release-v2.8/stage4_backlog_slice.md
- Theme: Frontend Completion, Test Quality & AI Journal Feature
- Status: ✅ Complete — Verified 2026-04-20

### v2.8 — Frontend Completion, Test Quality & AI Journal Feature

**Arc position:** v2.8 is a carry-forward and foundation release. EPIC-01 through EPIC-03 close v2.7 obligations. EPIC-04 (AI Journal Summarisation) is the first delivery of Arc 4 — it ships the AI infrastructure and journal data foundation that the full post-trade intelligence arc builds on.

|EPIC   |Scope item                                                 |Arc             |Effort|Notes                                                                                        |
|-------|-----------------------------------------------------------|----------------|------|---------------------------------------------------------------------------------------------|
|EPIC-01|BLG-FE-14 — Market Correlation frontend view               |Arc 2 pre-work  |M     |Completes v2.7 deferred AC-6; carry-forward obligation; feeds Pre-Trade Research View (PT-02)|
|EPIC-02|BLG-QA-13 — Test scenario coverage (SC-CORR/SC-SIG-IND)    |Quality         |M     |Fills v2.7 test gap                                                                          |
|EPIC-03|CF-1/CF-2/BLG-GOV-13 — Governance hardening + backlog dedup|Governance      |S×3   |Carry-forward + quick win                                                                    |
|EPIC-04|BLG-FEAT-16 — AI Journal Summarisation                     |Arc 4 foundation|M     |Gate-cleared (SRB-v1.7); first AI feature; external LLM API                                  |

---

## AI Journal Summarisation (AI-SUM) — §6 Gated Feature

**Original roadmap location:** §6 Gated Features table + §4 Priority 2 — Next Phase (initiative_register.md Priority 2)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-20
**Shipped version:** v2.8 (2026-04-20) — EPIC-04 (ST-07, ST-08)
**Cycle reference:** 2026-04-17__release-v2.8
**Verification report:** `claude/cycles/2026-04-17__release-v2.8/verification_report.md`
**Decision log reference:** Gate cleared 2026-04-04 — SRB-v1.7 CONDITIONALLY COMPLIANT; Strategy Rules owner sign-off at EPIC-04 merge 2026-04-20
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-04-20

### Original Roadmap Entry (§6)

|~~AI Journal Summarisation~~    |~~§13 boundary decision — does non-deterministic AI output conflict with the deterministic system principle?~~                      |~~Product Owner + Strategy Rules owner~~|~~Gate open~~ **Gate cleared 2026-04-04 (SRB-v1.7, CONDITIONALLY COMPLIANT). In scope v2.8 (EPIC-04). Strategy Rules owner sign-off required before merge. ✅ Shipped v2.8 — EPIC-04 delivered 2026-04-20.**|

> **Note (at retirement):** The AI Journal Summarisation struck-through entry was retained for audit continuity per roadmap note. Formally retired to archive 2026-04-20 at v2.8 post-ship closure.

---

## v2.7 — Performance, Governance Hardening & Market Intelligence (RA:v2.7)

**Original roadmap location:** §3 Delivery Plan — Horizon: Now (annotation block RA:v2.7)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-16
**Shipped version:** v2.7 (2026-04-16)
**Cycle reference:** 2026-04-13__release-v2.7
**Verification report:** `claude/cycles/2026-04-13__release-v2.7/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-04-16

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v2.7:2026-04-13__release-v2.7 — COMPLETE -->

**Execution notes (v2.7 — Complete):**
- Cycle: 2026-04-13__release-v2.7
- Plan published: 2026-04-13
- Shipped: 2026-04-16
- Cycle folder: claude/cycles/2026-04-13__release-v2.7/
- Backlog slice: claude/cycles/2026-04-13__release-v2.7/stage4_backlog_slice.md
- Theme: Performance, Governance Hardening & Market Intelligence
- Status: ✅ Complete — Verified 2026-04-16

---

## Market Correlation Analysis (MKT-COR) — §5 Priority 3 + §6 Gate

**Original roadmap location:** §5 Priority 3 table + §6 Gated Features table
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-16
**Shipped version:** v2.7 (2026-04-16) — ST-08 (EPIC-04)
**Cycle reference:** 2026-04-13__release-v2.7
**Verification report:** `claude/cycles/2026-04-13__release-v2.7/verification_report.md`
**Decision log reference:** Gate cleared 2026-04-04 — Yahoo Finance pipeline confirmed sufficient
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-04-16

### Original Roadmap Entry (§5)

| ~~Market Correlation Analysis~~ | ~~High~~ | ~~Gate cleared 2026-04-04~~. ✅ Shipped v2.7 — `GET /analytics/market-correlation` backend endpoint delivered (ST-08, 2026-04-16). AC-6 frontend rendering deferred to future story. |

---

## New Technical Indicators (TECH-IND) — §5 Priority 3 + §6 Gate

**Original roadmap location:** §5 Priority 3 table + §6 Gated Features table
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-16
**Shipped version:** v2.7 (2026-04-16) — ST-09 (EPIC-04)
**Cycle reference:** 2026-04-13__release-v2.7
**Verification report:** `claude/cycles/2026-04-13__release-v2.7/verification_report.md`
**Decision log reference:** Gate cleared 2026-04-04 — Strategy Rules owner: display-only scope approved
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-04-16

### Original Roadmap Entry (§5)

| ~~New Technical Indicators~~ | ~~Low–Medium~~ | ~~Gate cleared 2026-04-04~~. ✅ Shipped v2.7 — four supplementary indicator fields delivered in ST-09 (display-only, §13 COMPLIANT). |

---

## Signal Parameter Exposure (4.3) — §6 Gate

**Original roadmap location:** §6 Gated Features table
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-16
**Shipped version:** v2.0 (2026-03-17)
**Cycle reference:** 2026-03-17__release-v2.0
**Verification report:** N/A (shipped under prior governance)
**Decision log reference:** Gate cleared 2026-03-04 — PoG POG-20260304-01
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-04-16 (item remained in §6 as struck-through entry; now formally archived)

### Original Roadmap Entry (§6)

| ~~Signal parameter exposure (4.3)~~ | ~~`strategy_rules.md` updated to formally define `top_n` and `lookback_days` as user-configurable~~ | ~~Strategy Rules owner + Product Owner~~ |

---

## v2.5 — Integration Baseline, Quick Wins & Governance Debt (RA:v2.5)

**Original roadmap location:** §3 Delivery Plan — Horizon: Now (annotation block RA:v2.5)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-10
**Shipped version:** v2.5 (2026-04-10)
**Cycle reference:** 2026-04-05__release-v2.5
**Verification report:** `claude/cycles/2026-04-05__release-v2.5/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-04-10

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v2.5:2026-04-05__release-v2.5 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-04-05__release-v2.5
- Plan published: 2026-04-05
- Cycle folder: claude/cycles/2026-04-05__release-v2.5/
- Backlog slice: claude/cycles/2026-04-05__release-v2.5/stage4_backlog_slice.md
- Status at annotation: ✅ Complete — Shipped 2026-04-10 (Verified_with_deviations)

---

## v2.4 — Correctness, Insight & Governance Hardening (RA:v2.4)

**Original roadmap location:** §3 Delivery Plan — Horizon: Now (annotation block RA:v2.4)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-04-03
**Shipped version:** v2.4 (2026-04-03)
**Cycle reference:** 2026-03-31__release-v2.4
**Verification report:** `claude/cycles/2026-03-31__release-v2.4/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-04-03

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v2.4:2026-03-31__release-v2.4 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-03-31__release-v2.4
- Plan published: 2026-03-31
- Cycle folder: claude/cycles/2026-03-31__release-v2.4/
- Backlog slice: claude/cycles/2026-03-31__release-v2.4/stage4_backlog_slice.md
- Status at annotation: Validated

**✅ Complete — Shipped 2026-04-03 | Cycle: 2026-03-31__release-v2.4 | Verified_with_deviations**
- Theme: Correctness, Insight & Governance Hardening — 17/17 stories delivered, 6 EPICs merged
- Changelog: docs/product/changelog.md#v2.4

---

## v2.3 — Quality Automation & User Insight (RA:v2.3)

**Original roadmap location:** §3 Delivery Plan — Horizon: Now (annotation block RA:v2.3)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-30
**Shipped version:** v2.3 (2026-03-30)
**Cycle reference:** 2026-03-24__release-v2.3
**Verification report:** `claude/cycles/2026-03-24__release-v2.3/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-03-30

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v2.3:2026-03-24__release-v2.3 -->

✅ **Complete — v2.3 — Quality Automation & User Insight — Shipped 2026-03-30**
- Cycle: 2026-03-24__release-v2.3
- Plan published: 2026-03-24 | Shipped: 2026-03-30
- Verification: Verified_with_deviations
- Cycle folder: claude/cycles/2026-03-24__release-v2.3/
- Theme: Quality Automation & User Insight — 16/17 stories delivered; 5 EPICs merged; 1 item returned to backlog (BLG-GOV-08)
- Changelog: docs/product/changelog.md#v2.3

---

## v2.2 — Security, Alert Maturity & Quality (RA:v2.2)

**Original roadmap location:** §3 Delivery Plan — Horizon: Now (annotation block RA:v2.2)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-24
**Shipped version:** v2.2 (2026-03-24)
**Cycle reference:** 2026-03-21__release-v2.2
**Verification report:** `claude/cycles/2026-03-21__release-v2.2/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-03-24

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v2.2:2026-03-21__release-v2.2 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-03-21__release-v2.2
- Plan published: 2026-03-21
- Cycle folder: claude/cycles/2026-03-21__release-v2.2/
- Backlog slice: claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md
- Status at annotation: Shipped — 2026-03-24 (cycle 2026-03-21__release-v2.2) ✅ Complete

---

## v2.0 — Reporting & Alerts Annotation Block (RA:v2.0)

**Original roadmap location:** §3 Delivery Plan — Horizon: Now (annotation block RA:v2.0)
**Status at retirement:** ✅ Complete (underlying items 4.1b and 4.3 retired 2026-03-17; annotation block tombstone retired 2026-03-24)
**Retired from active roadmap:** 2026-03-24
**Shipped version:** v2.0 (2026-03-17)
**Cycle reference:** 2026-03-17__release-v2.0
**Verification report:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-03-24

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v2.0:2026-03-17__release-v2.0 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-03-17__release-v2.0
- Plan published: 2026-03-17
- Cycle folder: claude/cycles/2026-03-17__release-v2.0/
- Backlog slice: claude/cycles/2026-03-17__release-v2.0/stage4_backlog_slice.md
- Status at annotation: Shipped — 2026-03-17 (cycle 2026-03-17__release-v2.0) ✅ Complete

### v2.0 — Reporting & Alerts *(consolidated)* ✅ Complete — Shipped 2026-03-17

*3.5 Alerts & Notifications retired to `claude/roadmap/roadmap_archive.md` on 2026-03-21 — shipped in v2.1 (EPIC-01/EPIC-02, cycle 2026-03-18__release-v2.1).*
*4.1b Tax-Year P&L Statement and 4.3 Signal Exposure Enhancement retired to `claude/roadmap/roadmap_archive.md` on 2026-03-17 — both shipped in v2.0.*

---

## v2.1 — Alerts, Watchlists & Enhancements Annotation Block (RA:v2.1)

**Original roadmap location:** §3 Delivery Plan — Horizon: Now (annotation block RA:v2.1)
**Status at retirement:** ✅ Complete (underlying items 3.5, 4.2, CHART-IX retired 2026-03-21; annotation block tombstone retired 2026-03-24)
**Retired from active roadmap:** 2026-03-24
**Shipped version:** v2.1 (2026-03-21)
**Cycle reference:** 2026-03-18__release-v2.1
**Verification report:** `claude/cycles/2026-03-18__release-v2.1/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-03-24

### Original Roadmap Entry

<!-- roadmap-annotation-marker: RA:v2.1:2026-03-18__release-v2.1 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-03-18__release-v2.1
- Plan published: 2026-03-18
- Cycle folder: claude/cycles/2026-03-18__release-v2.1/
- Backlog slice: claude/cycles/2026-03-18__release-v2.1/stage4_backlog_slice.md
- Status at annotation: Shipped — 2026-03-21 (cycle 2026-03-18__release-v2.1) ✅ Complete

*4.2 Watchlists & Screening and Chart Interactivity Enhancements retired to `claude/roadmap/roadmap_archive.md` on 2026-03-21 — both shipped in v2.1 (cycle 2026-03-18__release-v2.1).*

---

## 4.1b — Tax-Year P&L Statement

**Original roadmap location:** §3 Delivery Plan — v2.0 section
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-17
**Shipped version:** v2.0 (2026-03-17)
**Cycle reference:** 2026-03-17__release-v2.0
**Verification report:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

#### 4.1b — Tax-Year P&L Statement *(new sub-item)*
**Status:** ✅ Complete — Shipped v2.0 (2026-03-17, cycle 2026-03-17__release-v2.0, EPIC-02/ST-04, ST-05)
**Effort:** Low–Medium (1–2 days)
**Value:** High (formal financial record for tax purposes)

A structured, server-side generated tax-year P&L statement. GBP-adjusted, fee-inclusive, covering all realised gains and losses in a given tax year. This is a financial record, not an analytics view — it requires its own canonical specification separate from the analytics endpoint. Dedicated report endpoint required.

> **Scope note (2026-03-04):** Realised vs Unrealised P&L display labelling (originally submitted as BLG-NEW-06) is pre-work for this item. The P&L statement must clearly distinguish realised and unrealised amounts per trade. BLG-NEW-06 is merged into 4.1b pre-work scope — not a standalone backlog item.

---

## 4.3 — Signal Exposure Enhancement

**Original roadmap location:** §3 Delivery Plan — v2.0 section
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-17
**Shipped version:** v2.0 (2026-03-17)
**Cycle reference:** 2026-03-17__release-v2.0
**Verification report:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`
**Decision log reference:** DL-004 (2026-03-04) — §13 gate cleared by PoG POG-20260304-01
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

#### 4.3 — Signal Exposure Enhancement *(new — narrow scope)*
**Status:** ✅ Complete — Shipped v2.0 (2026-03-17, cycle 2026-03-17__release-v2.0, EPIC-01/ST-01, ST-02)
**Effort:** Low (frontend only — backend already supports these parameters)
**Value:** Medium

Expose the existing `top_n` and `lookback_days` signal generation parameters as user-facing controls on the signals page. The backend already supports these parameters — this is a frontend and spec task, not an engineering one.

> **Gate clearance (DL-004, 2026-03-04):** The v1.7 SRB (EPIC-02) confirmed that `top_n` and `lookback_days` are display/query-scope controls, not strategy execution parameters, and their exposure does not violate §13.2. PoG: `claude/evidence/gates/signal-exposure-4.3_20260304.md` (POG-20260304-01). Referenced document: `strategy_rules.md` v1.3.

> **Scope constraint (immutable):** Only `top_n` and `lookback_days` are cleared by this PoG. Any parameter beyond these two — including signal weights, scoring logic, or ranking methodology — requires a new §13 review before it may enter pre-alignment. This PoG is automatically stale if `strategy_rules.md` is incremented.

---

## v1.10 — Operations & Quality Foundation

**Original roadmap location:** §3 Delivery Plan — v1.10 section
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-16
**Shipped version:** v1.10 (2026-03-16)
**Cycle reference:** 2026-03-15__release-v1.10
**Verification report:** `claude/cycles/2026-03-15__release-v1.10/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

### v1.10 — Operations & Quality Foundation ✅ Complete — 2026-03-16

<!-- roadmap-annotation-marker: RA:v1.10:2026-03-15__release-v1.10 -->

**Execution notes (added by Release Planning Engine):**
- Cycle: 2026-03-15__release-v1.10
- Plan published: 2026-03-15
- Cycle folder: claude/cycles/2026-03-15__release-v1.10/
- Backlog slice: claude/cycles/2026-03-15__release-v1.10/stage4_backlog_slice.md
- Status at annotation: Validated

**Closure notes (added by Post-Ship Closure Engine):**
- Shipped: 2026-03-16
- Verification status: Verified_with_deviations
- Changelog: docs/product/changelog.md#v1.10
- Closure record: claude/cycles/2026-03-15__release-v1.10/closure_record.md

#### BLG-OPS-01 — Development Environment *(elevated from backlog — P1)*
**Status:** ✅ Complete — Shipped 2026-03-16 (cycle 2026-03-15__release-v1.10)
**Effort:** Low–Medium (CI/CD pipeline + staging environment provisioning)
**Value:** Critical — structural QA gap. No non-production environment exists; all QA runs against production.

Provision a staging/dev environment tracking `main`. CI/CD auto-deploys to staging on merge. QA sign-off process updated to use staging URL, not production. Prerequisite for safe pre-merge quality validation.

> **Elevated from backlog (DL-008, 2026-03-15):** BLG-OPS-01 elevated to roadmap — displaces 4.1c (Server-Side PDF, killed). The absence of a development environment is a structural governance failure: Director of Quality sign-off requires testing a live application, but no non-production environment exists for pre-merge testing. See DL-008.

---

## v1.9 — User Value & Insight (5.1, BLG-FEAT-08, 5.2, 5.3)

**Original roadmap location:** §3 Delivery Plan — v1.9 section
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-15
**Shipped version:** v1.9 (Sprint 1: 2026-03-09; Sprint 2: 2026-03-13)
**Cycle reference:** 2026-03-06__release-v1.9
**Verification report:** `claude/cycles/2026-03-06__release-v1.9/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

### v1.9 — User Value & Insight *(✅ Fully Shipped 2026-03-13)*

Sprint 1 (2026-03-09): Risk Dashboard deviation fixes (EPIC-04), Playwright test infrastructure + Service Layer Test Coverage Standard (EPIC-05 partial), documentation hygiene (EPIC-06). Sprint 2 (2026-03-13): BLG-FEAT-08, 5.1, 5.2, 5.3, R-Multiple Distribution, Canonical Test Scenario Library Phase 2. All items verified.

#### 5.1 Structured Trade Reflection Template
**Status:** ✅ Complete — Shipped 2026-03-13 (v1.9 Sprint 2, EPIC-01/ST-02)

#### BLG-FEAT-08 — Basic Compliance Metrics
**Status:** ✅ Complete — Shipped 2026-03-13 (v1.9 Sprint 2, EPIC-03/ST-01)

#### 5.2 Cohort Analysis
**Status:** ✅ Complete — Shipped 2026-03-13 (v1.9 Sprint 2, EPIC-02/ST-03)
> Note: BLG-TECH-06 (CohortAnalysis.js client-side computation residue) filed in backlog at P2 for v1.10.

#### 5.3 Dashboard Homepage / Session Summary
**Status:** ✅ Complete — Shipped 2026-03-13 (v1.9 Sprint 2, EPIC-03/ST-05)

---

## 4.1c — Server-Side PDF Report

**Original roadmap location:** §3 Delivery Plan — v2.0 section
**Status at retirement:** ❌ Killed
**Retired from active roadmap:** 2026-03-15
**Shipped version:** N/A — killed
**Cycle reference:** 2026-03-15__item-5.3
**Verification report:** N/A
**Decision log reference:** DL-008 (2026-03-15)
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

#### ~~4.1c — Server-Side PDF Report~~ *(killed — DL-008, 2026-03-15)*
**Status:** ❌ Killed — displaced by BLG-OPS-01 (Development Environment)

Standing displacement candidate since DL-005 (2026-03-04). BLG-OPS-01 (P1 infrastructure gap — no dev environment for QA) is categorically higher priority. Browser-print PDF remains functional; UX inconvenience does not outweigh structural QA governance gap.

---

## 3.1 — Performance Analytics Page

**Original roadmap location:** §3 Delivery Plan — §3.1
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-15
**Shipped version:** v1.5
**Cycle reference:** N/A (predates governance)
**Verification report:** N/A (predates governance — no formal verification report exists)
**Decision log reference:** N/A (predates formal logging)
**Retirement confirmed by:** Product Owner — explicit confirmation 2026-03-15 (`manage roadmap` run): "item is complete, shipped v1.5, PO confirms retirement; no formal verification report exists as it predates governance"

### Original Roadmap Entry

**3.1 Performance Analytics Page**
**Status:** ✅ Complete (shipped v1.5)
Delivered via a unified GET /analytics/metrics?period= endpoint. Includes a POST /validate/calculations endpoint for smoke-testing metric correctness against a known dataset.

> ⚠️ **Product Owner Action Required:** No verification report path or decision log entry exists for this item (predates governance). Please provide a verification reference or decision log entry before the next `manage roadmap` run so this item can be retired to the archive.

---

## §3.4 / v1.8 — Risk Dashboard

**Original roadmap location:** §3 Delivery Plan — v1.8 section
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-06
**Shipped version:** v1.8
**Cycle reference:** 2026-03-04__release-v1.8
**Verification report:** `claude/cycles/2026-03-04__release-v1.8/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

### v1.8 — Risk Dashboard *(expanded from 3.4)* ✅ Complete — Shipped 2026-03-06

#### 3.4 Risk Dashboard
**Status:** ✅ Complete — Shipped 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | Verified_with_deviations
**Effort:** Medium (3–4 days with expanded scope)
**Value:** High (risk management — daily visibility)
**Pre-requisite:** Metrics Definitions (Portfolio Heat formula and thresholds) must be canonical before pre-alignment opens *(v1.7 gate — cleared)*

Previously scoped as a single Portfolio Heat Gauge widget. Scope expanded to a dedicated Risk Dashboard page that consolidates all risk-awareness features.

**Planned page contents:**
- Portfolio Heat Gauge — total capital at risk across open positions as a percentage of portfolio value
- Current Drawdown summary — from peak equity, days underwater *(if not already shipped in v1.6.1)*
- Grace Period status panel — positions currently in grace period with days remaining
- Position-level risk table — stop distance, ATR, position state (GRACE / LOSING / PROFITABLE) per open position
- Prospective heat indicator — integration with Position Sizing Calculator to show heat impact of a new position before entry

> **Before implementation:** The heat formula and display thresholds must be canonical in `docs/specs/metrics_definitions.md`. All other data is available from existing endpoints — `GET /portfolio`, `GET /positions`, `GET /analytics/metrics`. No new backend data dependencies beyond the heat calculation endpoint.

---

## §3.3 — Foundation & Governance (v1.7)

**Original roadmap location:** §3 Delivery Plan — §3.3
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-04
**Shipped version:** v1.7
**Cycle reference:** 2026-03-02__release-v1.7
**Verification report:** `claude/cycles/2026-03-02__release-v1.7/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

### 3.3 Foundation & Governance (v1.7)

**Status:** ✅ Complete — Shipped 2026-03-03
**Cycle:** 2026-03-02__release-v1.7
**Verification:** Verified — `claude/cycles/2026-03-02__release-v1.7/verification_report.md`
**Changelog:** `docs/product/changelog.md` — v1.7 entry

This release delivered the technical and governance foundations that de-risk everything that follows. It was non-user-facing but a hard dependency for several v1.8+ features.

#### BLG-TECH-04 — CI/CD GitHub Actions Validation Workflow
**Status:** ✅ Complete — 2026-03-03 (EPIC-01)
`.github/workflows/validate-analytics.yml` merged. Triggers on PR/push to main/develop. Blocks merge on `critical_failed > 0`. Posts severity breakdown as PR comment. PR #11 merged.

#### Strategy Rules §13 Boundary Review
**Status:** ✅ Complete — 2026-03-03 (EPIC-02)
Three features reviewed: Signal Params COMPLIANT, AI Journal CONDITIONALLY COMPLIANT, New Indicators COMPLIANT if canonical. §13-gated features cleared to proceed. Decision record: `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md`.

#### Metrics Definitions — Portfolio Heat Formula & Thresholds *(pre-work gate for v1.8)*
**Status:** ✅ Complete — 2026-03-03 (EPIC-03)
`metrics_definitions.md` v1.6.0: Position Risk (GBP-adjusted), Portfolio Heat formula, explicit display thresholds. v1.8 pre-alignment gate cleared.

#### Structured Logging / Observability Standards
**Status:** ✅ Complete — 2026-03-03 (EPIC-04)
`docs/specs/structured_logging_standards.md` v0.1.0 created (Class 1 Canonical Specification). Log levels, JSON format, correlation IDs, async observability. v2.0 pre-alignment gate (logging) cleared.

#### API Versioning Strategy Decision Record
**Status:** ✅ Complete — 2026-03-03 (EPIC-05)
`docs/product/decisions/api-versioning-v1.7.md` filed. URL path versioning deferred to first breaking change; 60-day deprecation; webhooks versioned from inception. v2.0 pre-alignment gate (API versioning) cleared.

#### Spec Debt Resolution (BLG-TECH-06, BLG-TECH-08, BLG-TECH-09)
**Status:** ✅ Complete — 2026-03-03 (EPIC-06)
`analytics_endpoints.md` v1.9.0 (14 metrics, OBS-01 resolved); `portfolio_endpoints.md` v1.9.0 (corrected to live API, OBS-QWB-R1-01 resolved); `trade_endpoints.md` v1.9.0 (`holding_days` added, OBS-QWB-R3-01 resolved).

---

## v1.6.1 — Correctness & Quick Wins

**Original roadmap location:** §3 Delivery Plan — v1.6.1 section
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-04
**Shipped version:** v1.6.1
**Cycle reference:** N/A (pre-cycle governance)
**Verification report:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

### v1.6.1 — Correctness & Quick Wins *(new)*

This release is inserted immediately after v1.6. It exists to resolve known correctness issues and ship a cluster of small, high-value backlog items before any new feature investment begins. No new feature work opens until this release is complete.

#### BLG-TECH-01 — Fix Sharpe Variance + Capital Efficiency *(promoted from backlog — P0)*
**Status:** ✅ Complete — 2026-02-21
**Closed:** Canonical Owner sign-off granted 2026-02-21. Validation confirmed 13/13 pass at 2026-02-21T00:24:41Z. `metrics_definitions.md` updated to v1.5.7 (Appendix E both items resolved). `analytics_endpoints.md` updated to v1.8.1. No regressions.

Fix `_calculate_sharpe()` to use sample variance (n−1) for portfolio and trade-level Sharpe. Fixed capital efficiency to use `total_cost (GBP)` from `trade_history` instead of `entry_price × shares`. `validation_data.py` expected values updated accordingly. v1.6 quality gate satisfied.

#### BLG-TECH-02 + BLG-TECH-03 — Validation Severity Model + Service Layer Consolidation (promoted from backlog — P1)
**Status:** ✅ Complete — 2026-02-21
**Closed:** Director of Quality sign-off 2026-02-21T21:30:00Z. 14/14 validation results pass with severity model. Phase Gate Documents filed.

Severity field added to every validation result (critical / high / medium / low) per analytics_endpoints.md v1.8.1
by_severity aggregation added to summary — all four tiers always present
All validation logic consolidated into services/validation_service.py per backend_engineering_patterns.md §3
Router thinned to HTTP in/out only — delegates entirely to ValidationService.validate_all()
Delivered co-delivered on single branch: fix/blg-tech-02-03-severity-service-consolidation
Phase Gate Documents: docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md, docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md
BLG-TECH-04 (CI/CD gate) dependency now unblocked ✅

#### Quick Wins Bundle *(promoted from backlog --- P2)*

**Status:** ✅ Complete --- 2026-03-01 **Estimated total effort:** ~8--10.5 hours (revised from ~6--8 hours to account for spec authoring --- A-S05, 2026-02-25) **Scope document:** `docs/product/scope/scope--QWB-quick-wins-bundle.md` **Decisions record:** `docs/product/decisions/QWB-quick-wins-bundle.md` **Phase Gate Document:** `docs/product/phase_gates/QWB_quick_wins_bundle_phase_gate.md` **Value:** Visible, tangible user-facing improvements. All decisions closed. All specs locked and QA-signed.

| Item | Effort | Status |
| --- | --- | --- |
| BLG-FEAT-01 --- Current Drawdown Widget | ~30 min | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-02 --- R-Multiple Column in Trade History | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-04 --- Best / Worst Trades Widget | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-05 --- Win Rate by Month Chart | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-06 --- Grace Period Indicator | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-07 --- CSV Export of Trade History | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |

**Locked canonical specs (implementation source of truth):**

| Spec | Version |
| --- | --- |
| `docs/specs/metrics_definitions.md` | v1.5.8 |
| `docs/specs/api_contracts/portfolio_endpoints.md` | v1.8.2 |
| `docs/specs/api_contracts/position_endpoints.md` | v1.8.3 |
| `docs/specs/api_contracts/trade_endpoints.md` | v1.8.4 |
| `docs/specs/api_contracts/analytics_endpoints.md` | v1.8.1 |
| `docs/specs/data_model.md` | v1.7 |
| `docs/specs/frontend/pages/dashboard.md` | v1.1 |
| `docs/specs/frontend/pages/trade_history.md` | v1.1 |
| `docs/specs/frontend/pages/analytics.md` | v1.2 |
| `docs/specs/frontend/pages/positions.md` | v1.2 |
| `docs/specs/api_dependencies.md` | v1.2 |
| `docs/reference/openapi.yaml` | current |

Verification: docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
Director of Quality sign-off: 2026-03-01 — Pass with logged deferrals (F-17, F-27)
Changelog: docs/product/changelog.md — v1.6.1 entry
Last Updated: 2026-03-01

---

## 3.2 — Position Sizing Calculator

**Original roadmap location:** §3 Delivery Plan — §3.2
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-04
**Shipped version:** v1.6
**Cycle reference:** N/A (pre-cycle governance)
**Verification report:** `docs/product/verification/3.2-position-sizing-calculator-verification.md` (v1.4)
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

**3.2 Position Sizing Calculator (Primary Feature)**
**Status:** ✅ Complete (shipped v1.6)
**Effort:** Low–Medium (2–3 days) (revised from 1–2 days — see scope note below)
**Value:** High (daily workflow improvement)
Always-visible widget inside the position entry form, directly above the shares field. User provides risk percentage (pre-populated from settings default) and stop price; system calculates suggested share count. Auto-fills the shares field when empty; shows a "use this" affordance when the user has already entered a value. Validates against available cash in real time via debounced calculation (300ms).

**Scope note (revised 2026-02-19):** Scope expanded during pre-alignment to include default_risk_percent field in the settings table, settings endpoint, and settings page UI. This is required to support widget pre-population and is in scope for v1.6 — not deferred. The original 1–2 day estimate did not account for the settings field, database migration, and additional spec updates across four documents. Revised estimate: 2–3 days. Full decision rationale: docs/product/decisions/3.2-position-sizing-calculator.md.

**Canonical specifications:** Sizing formula, validity rules, FX handling, and cash constraint behaviour are canonicalised in docs/specs/strategy_rules.md §4.1. Endpoint contract at docs/specs/api_contracts/portfolio_endpoints.md (POST /portfolio/size). Data model at docs/specs/data_model.md §6. Settings field at docs/specs/api_contracts/settings_endpoints.md.

**Shipped:** Director of Quality sign-off 2026-02-20. Verification report: docs/product/verification/3.2-position-sizing-calculator-verification.md (v1.4). Changelog: v1.6 entry. Scope and decisions documents superseded.

---

## 4.1a — CSV Export of Trade History

**Original roadmap location:** §3 Delivery Plan — v2.0 section
**Status at retirement:** ❌ Killed
**Retired from active roadmap:** 2026-03-04
**Shipped version:** N/A — killed
**Cycle reference:** 2026-03-01__item-3.2
**Verification report:** N/A
**Decision log reference:** DL-001 (2026-03-01)
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

#### 4.1a — CSV Export of Trade History
**Status:** ❌ Killed — superseded by BLG-FEAT-07 (shipped v1.6.1, 2026-03-01)

BLG-FEAT-07 (CSV Export) was delivered as part of the QWB Quick Wins Bundle and shipped in v1.6.1. This planning item is closed. Decision log: 2026-03-01__item-3.2.

---

## 3.5 — Alerts & Notifications

**Original roadmap location:** §3 Delivery Plan — Horizon: Now (v2.0 section)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-21
**Shipped version:** v2.1
**Cycle reference:** 2026-03-18__release-v2.1 (EPIC-01 ST-01, EPIC-02 ST-02 through ST-07)
**Verification report:** claude/cycles/2026-03-18__release-v2.1/verification_report.md
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-03-21

### Original Roadmap Entry

Alert rules engine for 4 alert types (stop_loss_approach, grace_period_warning, market_regime_change, daily_portfolio_summary). Notification delivery via Telegram Bot API (email deferred — Gmail SMTP blocked on Render free tier; revisit v2.2, BLG-OPS-04). In-app notification feed with read/unread state. Configurable per-user preferences. ADR-003 (async notification delivery architecture) authored as EPIC-01 prerequisite. Spec: docs/specs/api_contracts/alerts_endpoints.md. Deviation DEV-ST04-01 (P2) accepted.

---

## 4.2 — Watchlists & Screening

**Original roadmap location:** §4 Priority 2 — Horizon: Next (v2.1)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-21
**Shipped version:** v2.1
**Cycle reference:** 2026-03-18__release-v2.1 (EPIC-03 ST-08, ST-09, ST-10)
**Verification report:** claude/cycles/2026-03-18__release-v2.1/verification_report.md
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-03-21

### Original Roadmap Entry

Monitor tickers for entry signals. Target entry and stop price fields. Quick-add to position entry modal. New watchlist data model tables, REST endpoints. Signal status integration via LEFT JOIN LATERAL. Spec: docs/specs/api_contracts/watchlist_endpoints.md; docs/specs/frontend/pages/watchlist.md. AC-6 sort order (Active→Watch→No Signal→alpha) deferred — TEST-GAP-EPIC-03.

---

## Chart Interactivity Enhancements

**Original roadmap location:** §4 Priority 2 — Horizon: Next (v2.1)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-21
**Shipped version:** v2.1
**Cycle reference:** 2026-03-18__release-v2.1 (EPIC-04 ST-11)
**Verification report:** claude/cycles/2026-03-18__release-v2.1/verification_report.md
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-03-21

### Original Roadmap Entry

Hover tooltips, zoom, drill-down on analytics page charts (underwater equity curve, monthly heatmap, R-multiple distribution). No new indicators, no client-side re-derivation. All 16 SC-CHART-IX sub-scenarios verified on staging. Spec: docs/specs/frontend/pages/analytics.md.



---

## RA:v3.2 — Release Annotation

**Original roadmap location:** §1 Current Version header (roadmap annotation block)
**Status at retirement:** ✅ Complete — annotation retired post-ship
**Retired from active roadmap:** 2026-05-09
**Shipped version:** v3.2
**Cycle reference:** 2026-05-05__release-v3.2
**Verification report:** claude/cycles/2026-05-05__release-v3.2/verification_report.md
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-09

### Original Roadmap Entry

v3.2 Arc 2 Pre-Trade Research & Planning: PT-02 (Pre-Trade Research View frontend), PT-03 (Prospective Heat at Entry integration), PT-05 (Pre-Trade Entry Checklist). EPIC-03 governance hardening (OA-02–05). EPIC-04 documentation and security (BLG-FE-16, BLG-FE-21, BLG-SEC-05, BLG-GOV-18, BLG-GOV-11). 17/17 stories delivered. Verified 2026-05-07.


---

## RA:v4.3 — Governance Consolidation, QA Debt Clearance & Ops Hardening

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-05-29
**Shipped version:** v4.3
**Cycle reference:** 2026-05-29__release-v4.3
**Verification report:** claude/cycles/2026-05-29__release-v4.3/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-29

### Original Roadmap Entry

v4.3 Governance Consolidation, QA Debt Clearance & Ops Hardening. EPIC-01: v4.2 OA resolution (execution_prompt.md v3.32, qa_evidence_template.md v1.3, OPERATIONAL_GUIDE.md v4.13 §7.8 staging-only AC ref table; AI feature inventory v1.0). EPIC-02: QA debt clearance (Playwright for Arc5ComplianceSection; Arc 5 E2E test spec; CI pipeline baseline — BLG-QA-27 cleared; Playwright coverage matrix + Arc 5 coverage audit; 3 staging verifications: Claude thesis, ticker validation, cost alert). EPIC-03: Ops & security hardening (API key rotation policy + security register; staging parity audit v4.3; claude-audit-log performance baseline §16 — BLG-OPS-42 closed; ANTHROPIC_API_KEY added to staging permanently). EPIC-04: Frontend fixes + Arc 5 P&L (pre-entry price bug fix; Gemini→HAS_AI copy audit; Arc 5 compliance in monthly P&L). 18/18 stories delivered. Verified 2026-05-29.

---

## RA:v4.1 — Governance Hardening, Spec Debt, Arc 5 Compliance + SI-02 Pre-Planning

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-05-27 (backfilled — gap from prior manage_roadmap run)
**Shipped version:** v4.1
**Cycle reference:** 2026-05-26__release-v4.1
**Verification report:** claude/cycles/2026-05-26__release-v4.1/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-29 (backfill)

### Original Roadmap Entry

v4.1 Governance Hardening, Spec Debt, Arc 5 Compliance + SI-02 Pre-Planning. EPIC-01: execution_prompt.md v3.28 (merge-gate HARD GATE; OA-01), sprint_planning_prompt.md v3.7 (staging-only AC gate; OA-02), shared_standards.md v3.4, delivery_verification_prompt.md v2.6 (PR null guard; OA-04). EPIC-02: four API contracts documented (SI-03 red flag, SI-01 pre-entry, Arc 5 analytics, AI thesis). EPIC-03: Arc 5 composite score + Reports P&L section; POST /ai/check-daily-cost Telegram alert; Research view signal_type; arc5_compliance_section.md spec. EPIC-04: SI-02 pre-planning (gap analysis + 3 prereq docs); ANTHROPIC_API_KEY scope review; delivery_verification_prompt.md STEP 9.0; ops baselines. 14/15 stories delivered (ST-11 ACs 02-04 deferred to v4.3 as BLG-QA-28/29/30). Verified 2026-05-27.

---

## RA:v4.2 — Claude API Governance, SI-02 Pre-Work Readiness & Spec Debt

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-05-29
**Shipped version:** v4.2
**Cycle reference:** 2026-05-27__release-v4.2
**Verification report:** claude/cycles/2026-05-27__release-v4.2/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-29

### Original Roadmap Entry

v4.2 Claude API Governance, SI-02 Pre-Work Readiness & Spec Debt. EPIC-01: Claude API compliance & security (model version pinning, API key security review, accountability assignment, log hygiene). EPIC-02: Operational monitoring & baselines (api_performance_baseline update, first monthly cost review, thesis generation latency baseline). EPIC-03: Gemini→Claude spec debt clearance (audit trail backend, AI thesis contract, Playwright mock strategy, prompt caching assessment). EPIC-04: SI-02/SI-04 pre-planning (prerequisites checklist, scope definition, v4.1 review, namespace audit). 13/13 stories delivered. Verified 2026-05-29.

---

## RA:v4.4 — Governance Patches, SI-02 Pre-Planning Sprint & Ops Hardening

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-05-30
**Shipped version:** v4.4
**Cycle reference:** 2026-05-29__release-v4.4
**Verification report:** claude/cycles/2026-05-29__release-v4.4/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-30

### Original Roadmap Entry

v4.4 Governance Patches, SI-02 Pre-Planning Sprint & Ops Hardening. EPIC-01: v4.3 OA resolution — roadmap_prompt.md v6.6 (STEP 8.1 empty-Now-horizon advisory), sprint_planning_prompt.md v3.8 (frontend classification fast-path), execution_prompt.md v3.33 (auto-set deviations_filed on delegation clearance), qa_evidence_template.md v1.4 (delegated_qa DoQ sign-off both format variants), release_planning_prompt.md v2.32 (STEP 7 RESUME PRECHECK). EPIC-04: OPERATIONAL_GUIDE.md v4.19 §7.9 Staging URL Disambiguation. EPIC-02: SI-02 backend pre-planning — drift detection query pre-design, Arc 5 architecture review + ADR-001 (cached-synchronous), query index pre-assessment (3 indexes), background job ADR-SI02-001. EPIC-03: SI-02 FE+QA pre-planning — component pre-design (Option B), interaction spec (5 states, 13 DFT IDs), Playwright scenario pre-design (DFT-01–DFT-13). All 7 SI-02 pre-planning gate conditions met — SI-02 implementation sprint now unblocked. 13/13 stories delivered. Zero spec deviations. Verified 2026-05-30.

## RA:v4.5 — Governance Prompt Hardening, Audit Debt & SI-02 Spec Pre-Planning

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-05-30
**Shipped version:** v4.5
**Cycle reference:** 2026-05-30__release-v4.5
**Verification report:** claude/cycles/2026-05-30__release-v4.5/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-30

### Original Roadmap Entry

v4.5 Governance Prompt Hardening, Audit Debt & SI-02 Spec Pre-Planning. EPIC-01: execution_prompt.md v3.34 — four v4.4 OA patches: two-phase DEL terminal-status write (ST-01), pr_status sync after PR open (ST-02), LL-v4.5-EX-01 verification-class sub-criterion (ST-03), LL-v4.5-EX-02 spec_references policy for doc-creation stories (ST-04). EPIC-02: Agent role header standardization — 5 agent files updated to **Role:** format (AUD-2026-05-30-005). EPIC-03: SI-02 spec pre-sprint — §13 boundary review PASS (9 binding conditions; ST-06), drift score metric definition (4 metrics, 90-day window, green/amber/red bands; ST-07), data schema pre-definition (5 trade_plans columns + DS-07 migration; ST-08). All 4 v4.4 outstanding actions resolved. SI-02 sprint planning unblocked. 8/8 stories delivered. Zero spec deviations. Verified 2026-05-30.

---

## RA:v4.3 — Governance Consolidation, QA Debt Clearance & Ops Hardening

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-05-31 (backfill — execution notes block present in §1 after prior manage roadmap runs)
**Shipped version:** v4.3
**Cycle reference:** 2026-05-29__release-v4.3
**Verification report:** claude/cycles/2026-05-29__release-v4.3/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-31

### Original Roadmap Entry

v4.3 Governance Consolidation, QA Debt Clearance & Ops Hardening. v4.2 OA resolution: execution_prompt.md v3.32 (STEP 3.2.A + STEP 5.3/8 hard gate), qa_evidence_template.md v1.3, OPERATIONAL_GUIDE.md v4.13 (§7.8 staging-only AC ref table); AI feature inventory v1.0. QA debt: Playwright for Arc5ComplianceSection, Arc 5 E2E test spec, CI pipeline baseline (BLG-QA-27 cleared), coverage matrix + coverage audit. Ops/Security: API key rotation policy, security register, staging parity audit v4.3, claude-audit-log performance baseline §16. Frontend: pre-entry price bug fix, HAS_GEMINI→HAS_AI rename, Arc 5 compliance in monthly P&L. 18/18 stories delivered. Verified 2026-05-29.

---

## RA:v4.6 — SI-02 Behavioural Drift Detection & Arc 5 Completion

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-05-31
**Shipped version:** v4.6
**Cycle reference:** 2026-05-30__release-v4.6
**Verification report:** claude/cycles/2026-05-30__release-v4.6/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-05-31

### Original Roadmap Entry

v4.6 SI-02 Behavioural Drift Detection & Arc 5 Completion. EPIC-01 SI-02 Backend: DS-07 data migration (5 new trade_plans columns: signal_id, risk_percent_used, portfolio_value_at_entry, pre_entry_validation_snapshot, effective_settings_snapshot); POST /trade-plans updated to capture all 5 SI-02 fields; 4-metric behavioural drift service (entry_timing_drift, sizing_adherence, consecutive_loss_sizing, regime_context; 90-day window; §13 binding conditions); GET /analytics/behavioural-drift endpoint + API contract (behavioural_drift_contract.md) + openapi.yaml (60 total endpoints); 35-case SI-02 unit test suite. EPIC-03 Arc 5 Enablers: red_flag_events severity field (backfill + filter support; BLG-BE-16); Arc 5 hosting cost projection (current tier adequate; BLG-OPS-40); Arc 5 nav cohesion review (maintain current structure; BLG-FE-42); Red Flag Journal design review scope doc (gate 2026-06-21; BLG-FE-47). EPIC-04 Governance & Spec Debt: OA-01 System_status_report.md v4.4 correction; release_planning_prompt.md v2.33 STEP 1.4 gate scan (BLG-GOV-32/43); closed trade count audit (Q1=6, Q2=0, gate NOT MET — 6th deferral; BLG-GOV-33); Arc 4 data density trajectory Option A (BLG-GOV-34); Arc 6 Monte Carlo §13 PASS 10 binding conditions (BLG-GOV-45); trade plan schema audit 25 fields 0 orphaned (BLG-GOV-52); sprint close automation investigation — workflow functioning (BLG-GOV-41); external API spec template (BLG-SPEC-32); OA-02 roadmap_prompt.md v6.7 next_release advisory. EPIC-02 DEFERRED (data density gate NOT MET — 6th deferral; ST-06/07/08 returned to backlog; BLG-FEAT-25). 18/21 firm stories delivered (EPIC-02 gate-deferred); Verified_with_deviations (2 P3 staging deviations: BLG-OPS-44/45); 2026-05-31.

---

---

## RA:v5.0 — Governance Hardening, Product Correctness & SI-05 Pre-work

**Original roadmap location:** §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-03
**Shipped version:** v5.0
**Cycle reference:** 2026-06-03__release-v5.0
**Verification report:** claude/cycles/2026-06-03__release-v5.0/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-03

### Original Roadmap Entry

v5.0 Governance Hardening, Product Correctness & SI-05 Phase 1 Pre-work. Theme: Close governance debt from AUD-2026-06-02, fix two product correctness issues that slipped v4.9, and complete SI-05 Phase 1 pre-work ahead of the 2026-06-21 gate clearance. 13 stories/4 EPICs. Governance patches: BLG-GOV-79/80/81/82/83. Product correctness: BLG-FEAT-43 (allocation_insufficient status + frontend badge), BLG-BE-25 (shared market cache), BLG-OPS-52 (Anthropic SDK staging verification). SI-05 Phase 1 pre-work: BLG-FE-60 (channel trade-off + PO decision — Telegram confirmed), BLG-GOV-86 (Telegram message format spec v1.0), BLG-GOV-87 (SI-02 re-entry criteria), BLG-GOV-88 (SI-04 §13 binding conditions decisions doc), BLG-BE-26 (SI-02 drift summary feasibility assessment). BLG-GOV-67 (SI-05 Phase 1 implementation) conditional — gate 2026-06-21. All 13 firm stories delivered. Verified 2026-06-03. Zero spec deviations. PRs #663–#666.

---

## RA:v5.1 — SI-05 Phase 1 & Governance Debt

**Original roadmap location:** §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-04
**Shipped version:** v5.1
**Cycle reference:** 2026-06-21__release-v5.1
**Verification report:** claude/cycles/2026-06-21__release-v5.1/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-04

### Original Roadmap Entry

v5.1 SI-05 Phase 1 & Governance Debt. SI-05 Phase 1 weekly Telegram digest delivered (si05_digest_service.py; POST /digest/si05/send; 21 unit tests; BLG-GOV-67); BLG-SPEC-45 financial reporting scope confirmed OUT OF SCOPE; delivery_verification_prompt.md §-1.3 Tier 2 agent-mediated signer fix (v2.9→v3.0; LL-RP-v5.0-D-2); SignalCard allocation_insufficient badge Playwright E2E coverage (5 scenarios; BLG-FE-61 — 3-cycle recurrence closed); compliance_summary validation by code review (BLG-QA-43); staged verification sprint protocol document v1.0 (BLG-GOV-89). 6/6 stories. 1 P3 deviation (DEV-v51-EPIC01-01; BLG-SPEC-47 filed). PRs #675–#677. Verified_with_deviations 2026-06-21.

---

## RA:v5.2 — Governance Debt, SI-05 Ops & Spec Compliance

**Original roadmap location:** §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-08
**Shipped version:** v5.2
**Cycle reference:** 2026-06-08__release-v5.2
**Verification report:** claude/cycles/2026-06-08__release-v5.2/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-08

### Original Roadmap Entry

v5.2 Governance Debt, SI-05 Ops & Spec Compliance. OA-01 + OA-02 governance patches (release_planning_prompt.md v2.34; execution_prompt.md v3.37); BLG-SPEC-47 resolved (DEV-v51-EPIC01-01 closed; Option(a) chosen); BLG-SPEC-48 contract authored (digest_endpoints.md v0.3); SI-05 operational hardening (BLG-BE-32 retry; BLG-BE-33 log table); deployment runbook v0.2 + health check procedure; 3 security reviews (model deprecation PASS; bot token PASS with recommendation; endpoint auth GAP_FOUND — BLG-BE-35 filed); endpoint coverage audit (50 routes; 6 gaps: BLG-SPEC-49–52); SI-05 QA acceptance protocol + edge case tests (26 total); effectiveness criteria (review 2026-07-04). 16/16 stories. Zero spec deviations. PRs #694–#697. Verified 2026-06-08.

---

## RA:v5.3 — Spec Debt, Security Hardening & Ops Governance

**Original roadmap location:** §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-09
**Shipped version:** v5.3
**Cycle reference:** 2026-06-08__release-v5.3
**Verification report:** claude/cycles/2026-06-08__release-v5.3/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-09

### Original Roadmap Entry

v5.3 Spec Debt, Security Hardening & Ops Governance. All 6 known API contract gaps resolved (BLG-SPEC-49–52 contracts authored + openapi.yaml + test.py; BLG-SPEC-53 resolution plan; BLG-SPEC-54 completeness audit); POST /digest/si05/send API key authentication (BLG-BE-35); CI secret scanning gate via gitleaks (BLG-OPS-58); SI-05 Telegram failure alerting (BLG-OPS-57); 3 AI governance policy docs (AI model pin update policy BLG-GOV-108, AI audit log retention policy BLG-GOV-109, Arc 4 trade_plan data completeness audit BLG-GOV-110); SI-05 effectiveness review protocol + digest log schema validation (BLG-GOV-113/114); strategy_rules.md §11 parameter validation (BLG-GOV-104); SI-02 frontend activation gate criteria precision (BLG-GOV-107); QA acceptance criteria template (BLG-QA-51); tax year P&L boundary tests (BLG-QA-52); SI-05 Playwright E2E coverage (BLG-QA-53); Playwright coverage matrix updated (BLG-QA-54); Red Flag Journal UX review (BLG-FE-66); BLG-FE-64 design review scope definition (BLG-FE-67); LL-v5.2-P4-01/02 carry-forwards resolved. 24/24 stories. Zero spec deviations. PRs #722–#725. Verified 2026-06-09. completed_cycle_count = 39.


---

## RA:v5.4 — Ops Monitoring, UX Debt Clearance & Governance Patches

**Original roadmap location:** §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-10
**Shipped version:** v5.4
**Cycle reference:** 2026-06-09__release-v5.4
**Verification report:** claude/cycles/2026-06-09__release-v5.4/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-10

### Original Roadmap Entry

v5.4 Ops Monitoring, UX Debt Clearance & Governance Patches. ST-01 (BLG-OPS-60): v5.3 endpoints added to api_performance_baseline.md (5 endpoints with live Render measurements); ST-02 (BLG-FE-56): pre-entry override UX spec (pre_entry_override_ux_spec.md); ST-04 (BLG-GOV-92): SI-05 Phase 2 activation criteria doc (si05_phase2_activation_criteria.md, PO-approved). ST-03 (BLG-FE-64) returned to backlog — date gate 2026-06-21 not met; eligible from next cycle. 3/4 firm stories. Zero spec deviations. PRs #734–#736. Verified 2026-06-10. completed_cycle_count = 40.


---

## RA:v5.5 — SI-05 Effectiveness Review, Governance Hardening & UX Debt Clearance

**Original roadmap location:** §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-16
**Shipped version:** v5.5
**Cycle reference:** 2026-06-10__release-v5.5
**Verification report:** claude/cycles/2026-06-10__release-v5.5/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-16

### Original Roadmap Entry

v5.5 SI-05 Effectiveness Review, Governance Hardening & UX Debt Clearance.

---

## RA:v5.6 — Research Performance, SI-05 UX Improvements & Governance Patches

**Original roadmap location:** §3 Now (current_roadmap.md)
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-16
**Shipped version:** v5.6
**Cycle reference:** 2026-06-16__release-v5.6
**Verification report:** claude/cycles/2026-06-16__release-v5.6/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-16

### Original Roadmap Entry

v5.6 Research Performance, SI-05 UX Improvements & Governance Patches. SI-05 digest deep links + N/A reason clarification (BLG-FE-73/74, ST-01/02). Performance latency hardening — 4 endpoints: concentration-status 5-min TTL FX cache; red-flag-journal schema-once guard; behavioural-drift schema-once + 15-min cache; research 15-min per-ticker TTL + screener invalidation (BLG-OPS-22/62/63/64, ST-04/05/06/07). PT-04 gate re-verification: 13/20 closed trades — NOT MET (BLG-GOV-106, ST-08). Arc 5 QA completion criteria: BLG-QA-26 gate updated (BLG-QA-45, ST-09). Arc 5 test scenario assessment: 3 P3 Playwright gaps BLG-QA-56/57/58 (BLG-QA-49, ST-10). Anthropic API cost trend: stable, est. $0.05–$0.15/month (BLG-OPS-65, ST-11). ST-03 (BLG-FE-64) conditional — returned at planning (gate 2026-06-21 not cleared). 10/10 firm stories. Zero spec deviations. PRs #764–#766. Verified 2026-06-16. completed_cycle_count = 42. Governance patches: sprint_planning_prompt.md date gate advisory (BLG-GOV-116, ST-01); execution_prompt.md pr_status mandatory persist + branch ordering gate (BLG-GOV-117, ST-02; LL-v5.5-EX-02); qa_evidence commit advisory (BLG-GOV-118, ST-03; LL-v5.5-EX-01). Trade count gate-monitoring view GET /portfolio/gate-metrics + SI-05 data density line (BLG-BE-34/GOV-120, ST-04/05). API performance baseline complete — 18 endpoints measured v2.8–v5.4 (BLG-OPS-13/54/61, ST-06/07/08). Formal regression test suite baseline 387 scenarios / 66 endpoints (BLG-QA-50, ST-09). SI-05 user journey map + BLG-FE-73/74 friction (BLG-FE-65, ST-10). ST-11–14 returned — gate dates 2026-06-21/2026-07-04 not met. 10/14 firm stories. Zero spec deviations. PRs #751–#753. Verified 2026-06-16. completed_cycle_count = 41.


---

## RA:v5.7 — Staging Verification Completion, SI-05 Effectiveness Review & Engineering/Governance Patches

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-17
**Shipped version:** v5.7
**Cycle reference:** 2026-06-16__release-v5.7
**Verification report:** claude/cycles/2026-06-16__release-v5.7/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-17

### Original Roadmap Entry

v5.7 Staging Verification Completion, SI-05 Effectiveness Review & Engineering/Governance Patches. Production latency verifications: concentration-status p95=755ms (BLG-OPS-66, ST-01); red-flag-journal p95=872ms (BLG-OPS-67, ST-02); behavioural-drift p95=677ms cached (BLG-OPS-68, ST-03); research view p95=105ms (BLG-OPS-69, ST-04). SI-05 deep links mobile Telegram staging confirmed (BLG-FE-75, ST-05; 2 in-sprint bug fixes). Arc 5 Playwright coverage gaps closed: SC-SI-01d (BLG-QA-56, ST-06); SC-RFJ-04 (BLG-QA-57, ST-07); SC-ARC5-05 (BLG-QA-58, ST-08). Lazy-import pattern documented in backend_engineering_patterns.md v1.1 (BLG-BE-36, ST-10). Dual sign-off class confirmed in execution_prompt.md §5.3 (BLG-GOV-123, ST-11; LL-v5.6-DV-03 resolved). ST-09 (BLG-FE-64) conditional — 4th deferral, gate 2026-06-21. EPIC-03 (ST-12/13/14) gate-deferred 2026-07-04. 10/10 firm Sprint 1 stories. Zero spec deviations. PRs #781/782. Verified 2026-06-17. completed_cycle_count = 43.


---

## RA:v5.8 — RFJ UX Design Completion, SI-05 Effectiveness Review & Production Hardening

**Original roadmap location:** §1 Current Version / Release Summary §8
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-17
**Shipped version:** v5.8
**Cycle reference:** 2026-06-17__release-v5.8
**Verification report:** claude/cycles/2026-06-17__release-v5.8/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-17

### Original Roadmap Entry

v5.8 RFJ UX Design Completion, SI-05 Effectiveness Review & Production Hardening. FRONTEND_URL production env var configured on Render backend (trading-assistant-api-c0f9.onrender.com) — restores SI-05 deep-link functionality; deployment runbook v0.3 updated (ST-03; BLG-OPS-70 AC-04 deferral filed). Governance model complexity assessment produced — GCA-2026-06-17; complexity confirmed secondary factor (not root cause); 7 simplification candidates BLG-GOV-123–129 filed (ST-04; BLG-GOV-101 closed). ST-01/02 (BLG-FE-64/41) returned — gate 2026-06-21 (5th deferral). EPIC-02 (ST-05/06/07) gate-deferred 2026-07-04 (3rd consecutive deferral). 2/7 stories delivered (2/4 firm Sprint 1). Zero spec deviations. PR #790. Verified 2026-06-17. completed_cycle_count = 44.

---

## RA:v6.0 — Signal Correctness, User Intelligence & SI-05 Effectiveness

**Original roadmap location:** §3 Delivery Plan — Horizon: Now
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-06-22
**Shipped version:** v6.0
**Cycle reference:** 2026-06-19__release-v6.0
**Verification report:** claude/cycles/2026-06-19__release-v6.0/verification_report.md
**Decision log reference:** N/A
**Retirement confirmed by:** PMO Lead — manage roadmap STEP 11, post-ship closure 2026-06-22

### Original Roadmap Entry

Release v6.0 — Signal Correctness, User Intelligence & SI-05 Effectiveness. Theme: Correct signal suggested_shares calculation (P0 correctness fast-track BLG-BE-36 — every signal card shows wrong share counts); Trader's Morning Briefing dashboard (BLG-FEAT-46, P1 user-value); net-of-costs performance tracking (BLG-FEAT-20, P1 user-value); screener data quality telemetry (BLG-FEAT-47, P1); SI-05 deep link AC-04 staging confirmation (BLG-OPS-70); RFJ design review pre-brief (BLG-FE-64, gate 2026-06-21, 6th attempt — cleared); Red Flag Journal visual design review (BLG-FE-41, gate 2026-06-21); SI-05 Phase 1 effectiveness reviews (BLG-GOV-112/115/130, gate 2026-07-04); SI-05 latency baseline (BLG-OPS-59, gate 2026-07-04). Product Value Alert resolved. Skill-Silo constraint: G+D+P ≤ 60% per sprint (roadmap_prompt.md v7.4 ceiling — note: v7.5 corrects to 40%). 11/11 stories delivered. 2 P3 process deviations (ST-11), accepted under PO gate-override authority. Verified_with_deviations. PRs #808–822. Verified 2026-06-22. completed_cycle_count = 46.
