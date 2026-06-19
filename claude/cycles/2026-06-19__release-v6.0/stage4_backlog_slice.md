Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Release: v6.0
Cycle: 2026-06-19__release-v6.0
Last Updated: 2026-06-19

<!-- release-plan-marker: RP:v6.0:2026-06-19__release-v6.0 -->

---

# Stage 4 Backlog Slice — v6.0 Signal Correctness, User Intelligence & SI-05 Effectiveness

---

## EPIC-01 — Signal Correctness Fast-Track

**Maps to:** S2-01
**Owner:** Strategy Rules & System Intent Owner; Head of Engineering
**Estimated effort:** S (~0.5 day)
**Risk IDs:** RISK-01
**Execution sequence:** 1st — P0 correctness fast-track; no dependencies

**Epic description:** Correct the `suggested_shares` calculation in `signal_service.py` to use the canonical risk-based sizing model (`sizing_service.py`) instead of the cash-allocation model. Every signal card currently shows wrong share counts that vary with the number of concurrent signals and ignore the stop distance — a correctness violation that misrepresents the system's core risk management.

---

### ST-01 — Align signal_service suggested_shares to risk-based sizing model

**BLG-ID:** BLG-BE-36
**EPIC:** EPIC-01
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous (backend correctness fix; canonical spec confirmed)
**Dependencies:** Strategy Rules & System Intent Owner confirmation that risk-based formula is canonical (scoped within ST-01 as first AC)
**Staging-only ACs:** None (all ACs verifiable in CI via unit tests)

**Acceptance Criteria:**
- AC-01: Strategy Rules & System Intent Owner confirms risk-based formula (sizing_service.size_position()) is canonical for signal suggested_shares; confirmation recorded in QA evidence
- AC-02: signal_service.py calls sizing_service.size_position() using initial_stop as stop_price and portfolio's default risk_percent from settings
- AC-03: Signal card suggested_shares matches what the entry tab would produce for the same entry_price, initial_stop, and risk_percent
- AC-04: Share count is independent of how many other signals fire on the same day
- AC-05: Signals with no valid initial_stop produce suggested_shares = 0 (no crash)
- AC-06: Cash-allocation model fully removed from signal generation
- AC-07: Existing CI tests pass or are updated to reflect the new formula

**Spec references:** strategy_rules.md §4.1 (risk-based sizing); docs/specs/api_contracts/ (signals contract)

---

## EPIC-02 — User Intelligence Features

**Maps to:** S2-02, S2-03
**Owner:** Head of UX & Design; Financial Reporting & Records Owner
**Estimated effort:** M (~5 days total)
**Risk IDs:** RISK-02, RISK-03
**Execution sequence:** 2nd — after EPIC-01; addresses Product Value Alert commitment

**Epic description:** Deliver two P1 user-facing features that provide daily actionable intelligence: a Trader's Morning Briefing dashboard widget (composing existing endpoint data into a single start-of-day view) and net-of-costs R-multiple tracking (surfacing the real edge after transaction costs).

---

### ST-02 — Trader's Morning Briefing dashboard

**BLG-ID:** BLG-FEAT-46
**EPIC:** EPIC-02
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Estimated effort:** M (~2.5 days)
**Delegation class:** autonomous (frontend composition from existing endpoints; no new backend required)
**Dependencies:** None (all 5 composing endpoints are live)
**Staging-only ACs:** None (all AC verifiable in CI via Playwright)

**Acceptance Criteria:**
- AC-01: Morning Briefing section renders at top of DashboardHome.js on page load
- AC-02: Screener hits card renders with count of new screener hits since last visit; links to Screener page
- AC-03: Positions card renders any positions in EXIT_ZONE or GRACE_PERIOD states with days-in-state; links to Positions page; handles empty state
- AC-04: Red flags card renders count of new red flag events since last weekly digest; links to Red Flag Journal
- AC-05: Earnings card renders count of watchlisted or open-position tickers with earnings in next 7 days; links to earnings calendar
- AC-06: Compliance card renders current Arc 5 compliance score + trend arrow (up/down/flat vs prior week); links to PerformanceAnalytics
- AC-07: All cards handle loading and empty states without error (no crash on missing data)
- AC-08: Mobile: cards stack vertically at ≤ 768px breakpoint
- AC-09: Playwright coverage: morning briefing section renders; all 5 card types show data or empty state; links navigate correctly

**Spec references:** GET /portfolio/grace-period-alerts; GET /positions; GET /portfolio/red-flag-journal; GET /earnings/{ticker}; GET /analytics/arc5-compliance

---

### ST-03 — Net-of-costs performance tracking

**BLG-ID:** BLG-FEAT-20
**EPIC:** EPIC-02
**Owner:** Financial Reporting & Records Owner; Head of Engineering
**Estimated effort:** M (~2.5 days)
**Delegation class:** autonomous (additive data model + backend + frontend)
**Dependencies:** None
**Staging-only ACs:** None (all AC verifiable in CI)

**Acceptance Criteria:**
- AC-01: Brokerage cost fields capturable per trade (commission_gbp, spread_cost_gbp — optional fields; not all trades will have explicit cost data)
- AC-02: Net-of-costs R-multiple calculated and displayed where cost data exists
- AC-03: Performance report breakdowns show gross vs net comparison where cost data is present and difference is material
- AC-04: No impact to existing R-multiple calculations where cost data is absent (backward-compatible)
- AC-05: New fields are optional; existing trades without cost data remain unaffected

**Spec references:** docs/specs/api_contracts/ (trade history endpoints); data_model.md (trade cost fields)

---

## EPIC-03 — Screener Quality & Ops Closure

**Maps to:** S2-04, S2-05
**Owner:** Head of UX & Design; Infrastructure & Operations Owner
**Estimated effort:** S/XS (~1.1 days)
**Risk IDs:** RISK-04
**Execution sequence:** 3rd (after EPIC-01; parallel with EPIC-02 possible)

**Epic description:** Replace the generic screener degraded-run banner with structured data quality telemetry (run quality badge, loaded ratio, failed ticker list), and confirm SI-05 deep links work in production after FRONTEND_URL was set.

---

### ST-04 — Screener data quality telemetry

**BLG-ID:** BLG-FEAT-47
**EPIC:** EPIC-03
**Owner:** Head of UX & Design; Head of Backend Engineering
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous (backend + frontend; existing patterns)
**Dependencies:** None
**Staging-only ACs:** None (CI verifiable)

**Acceptance Criteria:**
- AC-01: GET /screener/results response includes `tickers_requested` (int), `tickers_loaded` (int), `tickers_failed` (list), `last_full_run_utc` (ISO timestamp), `run_quality` (FULL/DEGRADED/FAILED)
- AC-02: Screener page shows structured quality panel for all three run_quality values (replaces previous generic degraded-run banner)
- AC-03: FULL state: green badge + loaded ratio shown (e.g. "500 / 500")
- AC-04: DEGRADED state: amber badge + loaded ratio + expandable failed ticker list + "Results may be incomplete — N tickers failed to load" message
- AC-05: FAILED state: red badge + retry prompt
- AC-06: Stale advisory renders when last_full_run_utc > 24 hours ago ("Last full run: X hours ago")
- AC-07: Playwright: all three quality states render correctly; failed ticker count shown in DEGRADED state; retry prompt shown in FAILED state

**Spec references:** docs/specs/api_contracts/ (screener results contract — update required)

---

### ST-05 — SI-05 deep link AC-04 staging confirmation

**BLG-ID:** BLG-OPS-70
**EPIC:** EPIC-03
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous (ops verification)
**Classification:** Conditional (gate ~2026-06-23; within-sprint date gate per STEP 1.4b — may only be classified as conditional; must not be included as firm capacity at sprint planning)
**Dependencies:** SI-05 Telegram digest delivery after 2026-06-17 FRONTEND_URL set
**Staging-only ACs:** AC-01, AC-02, AC-03 — all require live Telegram digest delivery; cannot be reproduced in CI

**Acceptance Criteria:**
- AC-01: SI-05 Telegram digest received after FRONTEND_URL env var applied to production backend [staging-only evidence]
- AC-02: Deep links in digest are present and resolve to correct frontend pages [staging-only evidence]
- AC-03: Infrastructure & Operations Owner confirmation recorded in QA evidence [staging-only evidence]

**Spec references:** SI-05 digest delivery runbook; deployment_runbook.md

---

## EPIC-04 — SI-05 Effectiveness Reviews & RFJ Design (Conditional)

**Maps to:** S2-06, S2-07, S2-08, S2-09, S2-10, S2-11
**Owner:** PMO Lead; Product Owner; Head of UX & Design; Infrastructure & Operations Owner
**Estimated effort:** ~4.35 days (if all activate)
**Risk IDs:** RISK-05
**Execution sequence:** 4th — conditional; activates cluster by cluster as gates clear

**Epic description:** This EPIC contains two gate clusters. Cluster A activates when SI-03 Red Flag Journal has been live ≥30 days (gate 2026-06-21). Cluster B activates after the SI-05 Phase 1 effectiveness review is conducted (gate 2026-07-04). If a gate is not met by sprint close, affected items return to backlog.

**Cluster A (gate 2026-06-21):** S2-06 (ST-06), S2-07 (ST-07)
**Cluster B (gate 2026-07-04):** S2-08 (ST-08), S2-09 (ST-09), S2-10 (ST-10), S2-11 (ST-11)

---

### ST-06 — RFJ design review pre-brief

**BLG-ID:** BLG-FE-64
**EPIC:** EPIC-04
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision (UX document production; Head of UX & Design owns)
**Classification:** Conditional — gate 2026-06-21 (within-sprint date gate per STEP 1.4b)
**Dependencies:** Gate confirmed: SI-03 Red Flag Journal live ≥ 30 days. Must complete before ST-07 begins.
**Sprint history note:** 5 consecutive returns (v5.4–v5.8); perennial-return PO disposition recorded in run_manifest.md — retain conditional, gate genuinely imminent.
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: Gate condition confirmed: SI-03 has been live ≥ 30 days (on or after 2026-06-21)
- AC-02: Design review brief produced covering: review scope (filters UX, severity visual hierarchy, event type colour coding, timeline vs list layout), evaluation criteria, expected deliverable format
- AC-03: Head of UX & Design sign-off on brief scope recorded
- AC-04: Brief serves as direct input to ST-07 (BLG-FE-41) sprint planning

---

### ST-07 — Red Flag Journal visual design review

**BLG-ID:** BLG-FE-41
**EPIC:** EPIC-04
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** M (~1.5 days)
**Delegation class:** delegated_decision (UX design review; Head of UX & Design owns)
**Classification:** Conditional — gate 2026-06-21 + depends on ST-06 (within-sprint date gate per STEP 1.4b)
**Dependencies:** ST-06 (BLG-FE-64 pre-brief) must complete first; gate 2026-06-21
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: Gate condition confirmed: SI-03 has been live ≥ 30 days; ST-06 brief complete
- AC-02: Design recommendation document produced covering: severity visual hierarchy, event type colour coding, timeline vs list layout evaluation
- AC-03: If redesign recommended: UX spec produced and implementation backlog item filed
- AC-04: Review conducted against existing design system

---

### ST-08 — SI-05 digest weekly cadence review

**BLG-ID:** BLG-GOV-112
**EPIC:** EPIC-04
**Owner:** Product Owner; Director of Quality
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision (PO product review)
**Classification:** Conditional — gate 2026-07-04 (within-sprint date gate per STEP 1.4b)
**Sprint history note:** 3 consecutive returns (v5.5, v5.7, v5.8); perennial-return PO disposition: retain conditional, gate is scheduled event.
**Dependencies:** 2026-07-04 SI-05 effectiveness review (BLG-GOV-96) complete
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: Gate condition confirmed: 2026-07-04 effectiveness review complete; review outputs available
- AC-02: Cadence review document produced post-review
- AC-03: Assessment of weekly cadence appropriateness: maintain weekly / bi-weekly / adaptive cadence
- AC-04: Recommendation made with data backing (si05_digest_log delivery count; user action signals)
- AC-05: Product Owner sign-off on cadence recommendation

---

### ST-09 — SI-05 digest actionability metric definition

**BLG-ID:** BLG-GOV-115
**EPIC:** EPIC-04
**Owner:** Metrics Definitions & Analytics Owner; Infrastructure & Operations Owner
**Estimated effort:** S (~0.75 day)
**Delegation class:** autonomous (metrics definition document)
**Classification:** Conditional — gate 2026-07-04 (within-sprint date gate per STEP 1.4b)
**Sprint history note:** 3 consecutive returns (v5.5, v5.7, v5.8); perennial-return PO disposition: retain conditional.
**Dependencies:** BLG-GOV-113 (SI-05 effectiveness review protocol) complete — i.e., 2026-07-04 review conducted
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: Gate condition confirmed: 2026-07-04 effectiveness review (BLG-GOV-113 protocol) complete
- AC-02: 2–4 actionability metrics formally defined with data source mapping (si05_digest_log, red_flag_events, trade data)
- AC-03: Metrics definition document reviewed by Metrics Definitions & Analytics Owner
- AC-04: Metrics feed BLG-GOV-112 cadence review and BLG-GOV-96 effectiveness criteria

---

### ST-10 — SI-05 Phase 2 activation decision scope

**BLG-ID:** BLG-GOV-130
**EPIC:** EPIC-04
**Owner:** Product Owner; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision (PO formal decision document)
**Classification:** Conditional — gate 2026-07-04 (within-sprint date gate per STEP 1.4b)
**Dependencies:** 2026-07-04 effectiveness review outputs available; BLG-GOV-121 §13 pre-clearance and SI-02 gate status available for reference
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: Gate condition confirmed: 2026-07-04 effectiveness review outputs reviewed by PO
- AC-02: Formal Phase 2 activation decision document produced and filed in docs/product/decisions/
- AC-03: Document covers: activation criteria met/not met, activation timeline (if met), deferral rationale with revised review date (if not met)
- AC-04: If activation criteria met: Phase 2 sprint planning timeline confirmed; SI-02 gate status re-checked
- AC-05: Document filed as Class 3 Operational Record per document_lifecycle_guide.md

---

### ST-11 — SI-05 service production p99 latency baseline review

**BLG-ID:** BLG-OPS-59
**EPIC:** EPIC-04
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** S (~0.5 day) [from scored_initiatives.md — Tier 1]
**Delegation class:** autonomous (ops measurement + doc)
**Classification:** Conditional — gate 2026-07-04 (≥4 weeks SI-05 production operation; within-sprint date gate per STEP 1.4b)
**Sprint history note:** 3 consecutive returns (v5.5, v5.7, v5.8); perennial-return PO disposition: retain conditional.
**Dependencies:** ≥4 weeks of POST /digest/si05/send production operation (SI-05 live 2026-06-04 → gate 2026-07-04)
**Staging-only ACs:** AC-01 through AC-04 require live production Render log data

**Acceptance Criteria:**
- AC-01: Post-4-week p99 latency extracted from Render logs for POST /digest/si05/send [staging-only evidence]
- AC-02: Comparison against BLG-OPS-54 pre-launch baseline documented [staging-only evidence]
- AC-03: Performance PASS or investigation item filed: if p99 > 2× baseline → file investigation item; otherwise record PASS [staging-only evidence]
- AC-04: Infrastructure & Operations Owner sign-off recorded [staging-only evidence]
