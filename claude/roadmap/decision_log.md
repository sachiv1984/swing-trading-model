**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-21 (cycle 2026-05-21__scheduled — DL-032 appended)

---

# Roadmap Decision Log

## Purpose

This document records **explicit roadmap decisions** made from this point forward.

It exists to:
- Preserve rationale for Add / Replace / Defer / Kill decisions
- Make trade‑offs and opportunity cost visible
- Provide an audit trail for roadmap evolution

This document does **not** attempt to reconstruct historical decisions made prior to its creation.

---

## Scope & Start Point

- Decisions are recorded **from the first Claude‑executed roadmap rebalance onward**
- Earlier roadmap changes are out of scope and intentionally undocumented
- Absence of an entry implies the decision predates formal logging

This is deliberate.

---

## Decision Entries

Each decision entry must include:

- Date
- Decision type (Add / Replace / Defer / Kill)
- Initiative(s) affected
- Explicit rationale
- Displacement (if applicable)
- Decision owner

---

## Decisions

<!-- Decision entries are appended below this line -->

---

### DL-001 — 2026-03-01

**Decision type:** Kill
**Cycle:** 2026-03-01__item-3.2
**Date:** 2026-03-01
**Decision owner:** Product Owner

**Initiative:** 4.1a — CSV Export of Trade History

**Displacement:** N/A — superseded item; no active work displaced.

**Workforce impact:** None. BLG-FEAT-07 already delivered this feature; no ongoing allocation existed.

**Rationale:** BLG-FEAT-07 (CSV Export of Trade History) was delivered as part of the QWB Quick Wins Bundle and shipped in v1.6.1 (2026-03-01) with Director of Quality sign-off. The roadmap item 4.1a explicitly stated: "If BLG-FEAT-07 ships in v1.6.1, this item is superseded." That condition is satisfied. Retaining an active planning item with no remaining work creates false planning debt and violates lifecycle integrity.

---

### DL-002 — 2026-03-01

**Decision type:** Modify (pre-conditions elevated from advisory to hard gates)
**Cycle:** 2026-03-01__item-3.2
**Date:** 2026-03-01
**Decision owner:** Product Owner

**Initiative:** 3.5 — Alerts & Notifications (v2.0)

**Displacement:** N/A — existing roadmap item; no new addition.

**Workforce impact:** No change to allocated workforce. Hard gates prevent premature resource allocation.

**Rationale:** The three pre-conditions for 3.5 Alerts (observability standards, API versioning decision record, QA planning session for notification delivery) were advisory notes in the prior roadmap version. The structured debate Challenger raised a valid concern that advisory notes do not prevent premature pre-alignment opening — specifically, that async failure modes would be unobservable and notification delivery would ship without adequate QA coverage if pre-alignment opened before these were complete. Product Owner accepted the modification: all three pre-conditions are elevated to explicit hard gates. v2.0 pre-alignment may not open until all three are confirmed. Feature remains v2.0; no change to roadmap position.

---

### DL-003 — 2026-03-04

**Decision type:** Defer (confirmed — gate condition update with auto-advance trigger)
**Cycle:** 2026-03-04__item-3.4
**Date:** 2026-03-04
**Decision owner:** Product Owner

**Initiative:** 3.5 — Alerts & Notifications (v2.0)

**Displacement:** None — existing deferred roadmap item; no new addition.

**Workforce impact:** No premature workforce allocation. Hard gate prevents v2.0 pre-alignment until QA planning session is completed.

**Rationale:** Two of three hard gates are now cleared (EPIC-04 logging ✅, EPIC-05 API versioning ✅). The third gate — QA planning session for notification delivery — remains uncleared as of 2026-03-04. The defer status is confirmed with a new auto-advance condition: once the QA planning session is completed and documented, 3.5 Alerts auto-advances to active v2.0 planning without requiring a new rebalance cycle. The session output must specify: test types required, notification delivery modes to be tested, expected test infrastructure. Roadmap corrected: gate 3 was incorrectly marked "complete" in the prior roadmap text — corrected to "pending".

---

### DL-004 — 2026-03-04

**Decision type:** Replace (gated → active v2.0 planning)
**Cycle:** 2026-03-04__item-3.4
**Date:** 2026-03-04
**Decision owner:** Product Owner

**Initiative:** 4.3 — Signal Exposure Enhancement

**Displacement:** None — gated item unblocked, not a new addition. No stop required.

**Workforce impact:** No change to workforce totals. Item was already on roadmap at low effort.

**Rationale:** The v1.7 SRB (EPIC-02) confirmed that `top_n` and `lookback_days` are display/query-scope controls, not strategy execution parameters, and their exposure does not violate strategy_rules.md §13.2. PoG POG-20260304-01 issued 2026-03-04 (file: `claude/evidence/gates/signal-exposure-4.3_20260304.md`). Referenced document: strategy_rules.md v1.3. Item status changed from "Planned — gated" to "Planned — active v2.0 planning". Scope constraint is immutable: only `top_n` and `lookback_days` are cleared; any additional parameters require a new §13 review.

---

### DL-005 — 2026-03-04

**Decision type:** Add (backlog-level — not roadmap-level initiatives)
**Cycle:** 2026-03-04__item-3.4
**Date:** 2026-03-04
**Decision owner:** Product Owner

**Initiatives added to backlog:**
1. BLG-NEW-01 — Golden Output Regression Baseline for CI (P1)
2. BLG-NEW-02 — Backtest vs Live Stop Reconciliation Report (P1; dependency: after BLG-NEW-01)
3. BLG-NEW-03 — Define and Document Unavailability Failure Mode (P1)
4. BLG-NEW-04 — AI-Assisted Workflow Governance Policy (P2)
5. BLG-NEW-05 — Dependency Vulnerability Scanning in CI (P1)
6. BLG-NEW-06 — Realised vs Unrealised P&L Labelling (merged into 4.1b pre-work — not standalone)
7. BLG-NEW-07 — Running API Changelog Document (P1)
8. BLG-NEW-08 — Automated OpenAPI Drift Detection in CI (P1)

**Displacement:** None at roadmap level. These are backlog-level items only. They compete within v1.8 release capacity via the release planning engine. No roadmap-level Add requires a Stop; 0 Adds ≥ 0 Stops ✅.

**Stop candidate noted:** 4.1c Server-Side PDF Report is the lowest-value existing roadmap item and the natural displacement candidate if a future roadmap-level Add requires stops.

**Workforce impact:** New items are predominantly execution-heavy (CI, engineering). Combined governance items (BLG-NEW-03, 04, 07) are low-effort. Skill-Silo check: governance load ~21% (within 20–60% bounds). No Skill-Silo Alert issued.

**Source:** IW-20260304-01 idea intake window (44 submissions, 22 agents). BLG-NEW-06 merged into 4.1b scope — not promoted as standalone.

---

### DL-006 — 2026-03-06

**Decision type:** Add (backlog-level — not roadmap-level initiatives)
**Cycle:** 2026-03-06__item-3.4
**Date:** 2026-03-06
**Decision owner:** Product Owner

**Initiatives added to backlog:**
1. BLG-NEW-09 — R-Multiple Distribution Report (Analytics/User Value, P2; Metrics Definitions owner required; sequence after BLG-FEAT-08)
2. BLG-NEW-10 — Canonical Test Scenario Library (QA Infrastructure, P1; scoped to Risk Dashboard + new v1.9 features)
3. BLG-NEW-11 — Canonical Terms Glossary (Governance/Spec, P2; Class 2 Supporting document; Head of Specs Team owner)
4. BLG-NEW-12 — Service Layer Test Coverage Standard (Engineering Quality, P1; CI-enforceable coverage threshold required)

**Displacement:** None at roadmap level. These are backlog-level items only. 0 roadmap Adds ≥ 0 roadmap Stops ✅.

**Workforce impact:** Combined ~3.5–7 days across analytics, QA, spec, and engineering skill domains. No scarce skill constraint violated. Metrics Definitions owner sequencing constraint noted: BLG-FEAT-08 definitions must precede BLG-NEW-09 work. LL-05 capacity check applies to both.

**Source:** IW-20260304-01 parked carry-forwards (cycle 2026-03-04__item-3.4). All 4 items met STEP 5 debate advancement criteria.

---

### DL-007 — 2026-03-06

**Decision type:** No-change / Confirm (roadmap-level)
**Cycle:** 2026-03-06__item-3.4
**Date:** 2026-03-06
**Decision owner:** Product Owner

**Initiative(s) affected:** All active roadmap initiatives (no change)

**Displacement:** N/A — no additions.

**Workforce impact:** No change to roadmap-level workforce allocations.

**Rationale:** All roadmap initiatives were re-validated in STEP 2. No initiative merits Kill, Replace, or Defer beyond the standing DL-003 status for 3.5 Alerts. The roadmap is correctly balanced for the v1.9 → v2.0 delivery sequence. v1.9 scope is confirmed: 5.1, BLG-FEAT-08, 5.2, 5.3, BLG-RD deviation bundle, TEST-GAP-EPIC-01. No roadmap-level changes are required at this time. Roadmap updated with Last Updated date per lifecycle compliance requirement.

---

### DL-008 — 2026-03-15

**Decision type:** Kill + Add (net-zero — 1 Kill, 1 Add)
**Cycle:** 2026-03-15__item-5.3
**Date:** 2026-03-15
**Decision owner:** Product Owner

**Initiatives affected:**
- ❌ **Kill:** 4.1c — Server-Side PDF Report
- ➕ **Add:** BLG-OPS-01 — Development Environment (v1.10)

**Displacement:** 4.1c killed to create roadmap slot for BLG-OPS-01. Net-zero: 1 Kill + 1 Add ✅.

**Workforce impact:** 4.1c had no active workforce allocation (v2.0 planning not yet open). BLG-OPS-01 enters v1.10 as P1 — Infrastructure & Operations Owner is the primary delivery lead.

**Rationale — Kill 4.1c:**
Server-Side PDF Report was the lowest-value active roadmap item, documented as the standing displacement candidate since DL-005 (2026-03-04). The problem it solves — browser-print PDF inconsistency — is a UX inconvenience. Browser-print remains functional. With a P1 infrastructure gap (BLG-OPS-01) now demanding roadmap capacity, 4.1c is the correct item to displace. The §2 single-user product boundary limits the urgency of a polished PDF export further.

**Rationale — Add BLG-OPS-01:**
The absence of a development/staging environment is a structural governance failure. The Director of Quality sign-off workflow requires testing a live application before acceptance, but the only live application is production. This forced a merge-before-test workflow in v1.9 Sprint 2, which led to post-merge bug discovery (BLG-TECH-06). BLG-OPS-01 was raised as P1 in the backlog (2026-03-13) and is elevated to roadmap to guarantee capacity commitment in v1.10 planning. Without dedicated roadmap inclusion, infrastructure items are consistently squeezed out by feature work.

**Challenger debate summary:** Both the Kill and Add were challenged during STEP 4 structured debate. All challenges were answered satisfactorily and withdrawn. Motion approved unanimously.

---

### DL-009 — 2026-03-17

**Decision type:** No-change (roadmap-level confirm) + Add (backlog-level — 3 items)
**Cycle:** 2026-03-17__item-v1.10
**Date:** 2026-03-17
**Decision owner:** Product Owner

**Initiatives affected (roadmap-level):**
All active roadmap initiatives reviewed and confirmed. No roadmap-level Add, Replace, Defer, or Kill decisions required.

**Completion recorded:**
- ✅ **Complete:** BLG-OPS-01 — Development Environment (v1.10, shipped 2026-03-16). Moved to Completed in initiative register.

**Displacement:** N/A — no roadmap-level Adds. Net-zero: 0 Adds ≤ 0 Kills ✅.

**Workforce impact:** v1.10 capacity released (~15–20 days). Immediately available for v2.0 pre-alignment. No scarce skill conflicts identified for v2.0 scope (4.1b: backend + financial spec; 4.3: frontend only).

**Rationale — Roadmap No-Change:**
All five active roadmap initiatives (3.5 Alerts, 4.1b Tax-Year P&L, 4.3 Signal Exposure, 4.2 Watchlists, Chart Interactivity Enhancements) were re-validated in STEP 2. No initiative merits Kill, Replace, or Defer. The roadmap is correctly balanced for the v2.0 delivery sequence. CPS = 2.40 (prior: 2.17 post-rebalance). No Strategy Drift Alert required. PoG POG-20260304-01 (item 4.3) remains valid — strategy_rules.md v1.3 unchanged. Horizon structure (Now/Next/Later) added to roadmap as lifecycle compliance update.

**New backlog items (from STEP 5 debate — IW-20260304-01 idea pool):**
1. BLG-OPS-02 — Production Deployment Runbook (P2; Infrastructure & Operations Owner; v2.0)
2. BLG-DATA-01 — Positions Table Data Dictionary (P2; Data Model Domain & Schema Owner; v2.0; positions table fields only; Class 2 Supporting)
3. BLG-TECH-07 — Database Migration Governance Standard (P2; Backend Engineering Patterns Owner + Head of Engineering; v2.0)

**Displacement (backlog-level):** None at roadmap level. Backlog-level items only. 3 Adds ≥ 0 roadmap Stops ✅ (per DL-005/DL-006 precedent).

**Skill-Silo check:** Governance load ~0% for v2.0 execution scope. Below 20% floor. Product Owner sign-off capacity confirmed. No Skill-Silo Alert issued.

**Displacement candidate noted (initiative register — forward-looking):** Chart Interactivity Enhancements (CHART-IX) flagged as the natural displacement candidate if a future roadmap-level Add requires stops. Lowest strategic urgency relative to impact; smallest scope (S effort). Recorded in initiative_register.md only.

**Challenger debate summary:** Three ideas advanced to STEP 5 debate; Challenger issued two clearances and one counter-argument (Positions Table Data Dictionary overlap with BLG-NEW-13). Product Owner rebutted the overlap argument with scope distinction. One idea (Lessons Learnt Action Item Register) was parked at STEP 5 when PO accepted Challenger's overlap argument with BLG-GOV-01/02. STEP 8.6 guardrail passed (one candidate parked).

---

### DL-010 — 2026-03-18

**Decision type:** No-change (roadmap-level confirm) + Add (backlog-level — 2 items) + Completion recorded
**Cycle:** 2026-03-18__item-4.3
**Date:** 2026-03-18
**Decision owner:** Product Owner

**Completion recorded:**
- ✅ **Complete:** 4.3 — Signal Exposure Enhancement (v2.0, shipped 2026-03-17). Moved to Completed in initiative register.
- ✅ **Complete:** 4.1b — Tax-Year P&L Statement (v2.0, shipped 2026-03-17). Moved to Completed in initiative register. *(Note: 4.1b completion recorded in this cycle for initiative register hygiene; the primary completion event for this run is item 4.3.)*

**Initiatives affected (roadmap-level):**
All active roadmap initiatives reviewed and confirmed. No roadmap-level Add, Replace, Defer, or Kill decisions required.

**Displacement:** N/A — no roadmap-level Adds. Net-zero: 0 Adds ≤ 0 Kills ✅.

**Workforce impact:** v2.0 capacity fully released. Available for v2.1 pre-work. Primary blocker is BLG-TECH-08 (async notification ADR) for 3.5 Alerts. CPS = 2.33 (prior: 2.40) — slight decrease as SPS=4 item (4.3) and SPS=1 item (4.1b) exit the active pool.

**Rationale — Roadmap No-Change:**
Three active roadmap initiatives (3.5 Alerts, 4.2 Watchlists, CHART-IX) were re-validated in STEP 2. No initiative merits Kill, Replace, or Defer beyond the standing DL-003 defer status for 3.5 Alerts. 3.5 Alerts updated to v2.1 target in initiative register (was v2.0 — corrected for accuracy post-v2.0 ship). The roadmap is correctly balanced for the v2.1 delivery sequence.

**New backlog items (from STEP 5 debate — IW-20260317-01 ideas):**
1. BLG-FR-01 — Tax Year P&L Report PDF Export (P2; Financial Reporting Owner; v2.1; S effort)
2. BLG-FR-02 — Tax Year P&L Report CSV Table Export (P2; Financial Reporting Owner; v2.1; S effort)

Both items originated from v2.0 staging feedback. Challenger issued a Type A counter-argument for PDF Export (DL-008 consistency concern); PO rebutted on grounds that DL-008 was a capacity-kill, not a value-kill, and the statutory filing use case distinguishes the tax year P&L report from 4.1c. STEP 8.6 guardrail passed (Challenger issued one Type A counter-argument).

**Stale idea dispositions:** 19 ideas at Parked-cycle-3 received mandatory active PO disposition — 8 rejected, 11 re-parked with written rationale. Recorded in ideas_register.md.

**Displacement (backlog-level):** None required. Backlog-level items only per DL-005 precedent. 2 Adds ≥ 0 roadmap Stops ✅.

---

### DL-011 — 2026-03-21

**Decision type:** No-change (roadmap-level confirm) + Add (backlog-level — 11 items) + Completion recorded
**Cycle:** 2026-03-21__item-3.5
**Date:** 2026-03-21
**Decision owner:** Product Owner

**Completion recorded:**
- ✅ **Complete:** 3.5 — Alerts & Notifications (v2.1, shipped 2026-03-21). Moved to Completed in initiative register.
- ✅ **Complete (noted):** 4.2 — Watchlists & Screening (v2.1, shipped 2026-03-21). Register corrected in this run (LL-01-patch-4.3 partial mitigation).
- ✅ **Complete (noted):** CHART-IX — Chart Interactivity Enhancements (v2.1, shipped 2026-03-21). Register corrected in this run.

**Initiatives affected (roadmap-level):**
Zero active roadmap initiatives as of this run — all shipped in v2.1. No roadmap-level Add, Replace, Defer, or Kill decisions required.

**Displacement:** N/A — no roadmap-level Adds. Net-zero: 0 Adds ≤ 0 Kills ✅.

**Workforce impact:** Full v2.1 capacity released (~6–8 sprints across backend, frontend, QA). Available for v2.2 scope. v2.2 theme TBD; release planning engine will scope from the enriched backlog. BLG-OPS-04 (P1, alert scheduling) is the most important unresolved gap and is likely to anchor the v2.2 release theme.

**Rationale — Roadmap No-Change:**
Zero active initiatives post-v2.1 ship. The roadmap is correctly balanced at the strategic level — all planned v2.1 items delivered. v2.2 scope will be determined by the release planning engine. No initiative merits Kill, Replace, or Defer at the strategic level. Gated items (AI-SUM, TECH-IND, MKT-COR) remain appropriately gated.

**CPS this cycle:** 0.0 (zero active initiatives — all shipped). Prior CPS: 2.33. Delta: −2.33 (expected — completion event). No strategy drift alert.

**New backlog items (from STEP 5 debate — IW-20260321-01 + stale idea clearing):**

1. BLG-SPEC-T01 — Spec-to-Test Traceability Matrix (P2; Director of Quality; v2.2; M effort) — gate cleared (ST-17 shipped v2.1)
2. BLG-FE-02 — Loading State Standardisation (P3; Base44 Frontend; v2.2; M effort) — gate cleared (BLG-TECH-08 shipped v2.1)
3. BLG-FEAT-09 — Metrics Staleness Indicator (P2; Metrics Definitions & Analytics Owner; v2.2; S–M effort) — gate cleared (BLG-FEAT-03 shipped v2.1)
4. BLG-OPS-05 — API Endpoint Performance Baseline (P3; Head of Engineering; v2.2; S effort) — gate cleared (API surface stable post-v2.1)
5. BLG-QA-02 — Test Automation Readiness Assessment (P2; QA & Testing Owner; v2.2; XS effort) — prerequisite for BLG-QA-01 sequencing
6. BLG-FEAT-10 — Alert Threshold Customisation (P2; Product Owner + Backend Engineering; v2.2; M effort) — natural extension of v2.1 alerts
7. BLG-FEAT-11 — Strategy Compliance Score — display-only (P2; Strategy Rules & System Intent Owner + Backend + Frontend; v2.2; M–L effort) — **Scope constraint: display-only panel, no automated enforcement, no alerts generated by score**
8. BLG-SEC-01 — API Key Authentication (P1; Backend Engineering; v2.2; M effort) — financial data security gap on Render deployment
9. BLG-FEAT-12 — Alert History Table (P2; Data Model Owner + Backend + Frontend; v2.2; M effort) — audit trail for alert system; best scheduled alongside BLG-OPS-04
10. BLG-OPS-06 — Health Check Endpoint `GET /health` (P3; Infrastructure & Operations Owner; v2.2; XS effort) — direct backlog routing (no debate required)
11. BLG-SEC-02 — Content Security Policy (CSP) Headers (P3; Cybersecurity & Trust Lead + Frontend; v2.2; XS effort) — direct backlog routing

**Stale idea dispositions (IW-20260321-01):** 11 ideas at Parked-cycle-4 received mandatory active PO disposition — 0 rejected, 7 advanced (gates cleared), 4 re-parked with written rationale. Recorded in ideas_register.md.

**Idea intake (IW-20260321-01):** 44 new submissions from 22 agents (Facilitator excluded by charter). 9 advanced through STEP 5 debate; 36 parked; 2 directly routed to backlog. Challenger issued 2 Type A counter-arguments (strategy compliance score SPS=4; API authentication single-user threat model). STEP 8.6 guardrail passed.

**Displacement (backlog-level):** None at roadmap level. Backlog-level items only per DL-005 precedent. 0 roadmap Adds ≥ 0 roadmap Stops ✅.

**Skill-Silo check:** Governance load ~15–20%. Within 20–60% bounds. No Skill-Silo Alert issued.

---

### DL-012 — 2026-03-24

**Decision type:** No-change (roadmap-level confirm) + Add (backlog-level — 8 items)
**Cycle:** 2026-03-24__scheduled
**Date:** 2026-03-24
**Decision owner:** Product Owner

**Run type:** Scheduled rebalance (first-ever scheduled run; Extended tier triggered — `last_scheduled_rebalance_utc` absent from state.json, treated as never run ≥ 90-day criterion met)

**Active initiatives:** Zero. All v2.2 items shipped 2026-03-24. v2.3 scope TBD — pending release planning.

**Initiatives affected (roadmap-level):**
All active roadmap initiatives reviewed and confirmed. No roadmap-level Add, Replace, Defer, or Kill decisions required. Gated items (AI-SUM, TECH-IND, MKT-COR) remain appropriately gated. Now→Next horizon review (Extended tier): no movements recommended — no triggering events for any Later or Gated item post-v2.2.

**Displacement:** N/A — no roadmap-level Adds. Net-zero: 0 Adds ≤ 0 Kills ✅.

**CPS this cycle:** 0.0 (zero active initiatives — all v2.2 items shipped). Prior CPS: 0.0 (cycle 2026-03-21__item-3.5). Delta: 0.0. No drift alert.

**Workforce impact:** Combined backlog pool now ~23 active items (~37–47 days estimated effort). Release planning will scope a realistic v2.3 sprint plan from this pool. No scarce skill conflicts. QA automation skill is the dominant domain in new additions (4 items, ~4.5 days) — already represented by existing BLG-QA-01.

**Rationale — Roadmap No-Change:**
Zero active initiatives post-v2.2 ship. Extended-tier horizon review confirmed no movements warranted for any Later or Gated item. The 15-item existing backlog plus 8 new items provides a rich candidate pool for v2.3 release planning. No strategic trigger event occurred that would justify reopening any of the deferred or gated items.

**New backlog items (from STEP 4/5 — ideas window 2026-03-24__scheduled):**

1. BLG-OPS-07 — System Health Check Playbook (P3; Infrastructure & Operations Owner; v2.3; S effort) — BLG-OPS-06 shipped; playbook companion warranted
2. BLG-QA-03 — Canonical Test Execution Report Template (P3; QA Lead; v2.3; S effort) — BLG-QA-02 shipped; standardised reporting follows naturally
3. BLG-QA-04 — Integration Test Coverage Report (P3; QA & Testing Owner; v2.3; M effort) — BLG-QA-02 specifically called out coverage reporting as next step
4. BLG-QA-05 — Critical-path Smoke Test — Playwright (P2; QA & Testing Owner; v2.3; M effort) — BLG-QA-02 identified 3 critical paths without automation; **§3 scope constraint: Playwright pass is supporting evidence only — not DoQ gate replacement; flaky test failures must not block human review**
5. BLG-OPS-08 — Staging Data Reset Script (P3; Infrastructure & Operations Owner; v2.3; S effort) — BLG-QA-02 identified state pollution between staging QA runs; prerequisite for BLG-QA-05
6. BLG-OPS-09 — Database Size Monitoring Alert (P2; FinOps & Resource Architect + Backend Engineering; v2.3; S effort) — BLG-OPS-06 shipped; active data-loss risk on Render free tier
7. BLG-FE-05 — Alert Notification Badge in Nav (P3; Base44 Frontend Prompt Owner; v2.3; S effort) — BLG-FEAT-12 shipped; badge needs alert persistence (now available)
8. BLG-QA-06 — Test Data Seed Script Library (P2; QA & Testing Owner + Backend Engineering; v2.3; S–M effort) — BLG-QA-02 identified seed data reproducibility as prerequisite for automation

**Stale idea dispositions (cycle-5 mandatory):** 5 ideas at Parked-cycle-5 received mandatory PO disposition — 2 advanced (BLG-OPS-07, BLG-QA-03), 2 re-parked to cycle-6 with written rationale, 1 rejected (IDEA-head-of-ux-20260304-02 — Design Token System — permanently closed after 5 cycles with no triggering event).

**Idea intake (IW-20260321-01 cycle-1 items):** 35 ideas at Parked-cycle-1 reviewed — 6 advanced through STEP 5 debate, 29 re-parked to cycle-2. Challenger issued 1 Type A counter-argument (BLG-QA-05 — §3 human-in-loop automation risk). PO rebutted with existing scope constraint evidence. STEP 8.6 guardrail passed (Type A counter-argument issued).

**Displacement (backlog-level):** None at roadmap level. Backlog-level items only per DL-005 precedent. 0 roadmap Adds ≥ 0 roadmap Stops ✅.

**Skill-Silo check:** Governance load 0% for new additions. Below 20% floor. Product Owner sign-off capacity confirmed. No Skill-Silo Alert issued.

**Meta-review:** Due (3rd rebalance cycle since initialisation). Conducted. No new prompt patches warranted. Dominant pattern: Type D cognitive fatigue (3/4 friction items across 2 cycles). All identified patterns from prior meta-review already resolved. See `claude/cycles/2026-03-24__scheduled/meta_review.md`.

---

### DL-013 — 2026-03-31

**Decision type:** Add (backlog-level)
**Cycle:** 2026-03-31__scheduled
**Date:** 2026-03-31
**Decision owner:** Product Owner

**Initiative:** BLG-FEAT-14 — Weekly trading review digest

**Gate cleared:** BLG-FEAT-11 (strategy compliance score) and BLG-FEAT-09 (staleness indicator) shipped in v2.3 — prior park rationale "defer until land and usage patterns clearer" satisfied.

**Displacement:** BLG-FE-03 (user-facing error mapping layer, P3) deprioritised in v2.4 planning queue.

**Workforce impact:** M effort (~2–3 days). Backend (new endpoint) + Frontend (digest component). No scarce skill conflicts at backlog level.

**Rationale:** v2.3 analytics investments now provide sufficient data for a meaningful weekly digest. Scope explicitly constrained to raw data aggregation only — no generated text or interpretation. Challenger raised §3 boundary concern (soft automated reporting); PO accepted scope constraint. SPS = 2. Zero-sum satisfied: 1 Add, 1 displacement named.

---

### DL-014 — 2026-03-31

**Decision type:** Add (backlog-level)
**Cycle:** 2026-03-31__scheduled
**Date:** 2026-03-31
**Decision owner:** Product Owner

**Initiative:** BLG-OPS-10 — Render hosting tier review

**Gate cleared:** BLG-OPS-04 (cron alert scheduling) shipped v2.2; one full sprint cycle (v2.3) of scheduling observed — prior park rationale "observe for one sprint" satisfied.

**Displacement:** BLG-TECH-05 (Prometheus metrics endpoint, P3) deprioritised in v2.4 planning queue.

**Workforce impact:** XS effort (<1 hour). FinOps + Infrastructure Owner only. Negligible engineering cost.

**Rationale:** Operational hygiene — documenting hosting cost decisions before issues surface silently. Challenger cleared with no counter-argument (SPS=1, pure operational). Zero-sum satisfied: 1 Add, 1 displacement named.

---

### DL-015 — 2026-03-31

**Decision type:** Add (backlog-level)
**Cycle:** 2026-03-31__scheduled
**Date:** 2026-03-31
**Decision owner:** Product Owner

**Initiative:** BLG-BE-06 — Alert evaluation idempotency

**Gate cleared:** BLG-OPS-04 (cron alert scheduling) shipped v2.2; one full sprint (v2.3) of scheduling behaviour observed — prior park rationale "observe for one sprint first" satisfied.

**Displacement:** BLG-BE-04 (R-Multiple stop price fix, P3) deprioritised in v2.4 planning queue.

**Workforce impact:** M effort (~1–2 days). Backend engineering only. No frontend dependency.

**Rationale:** Duplicate alert notifications on scheduler retry/misfire are a real risk that degrades user trust. Challenger raised §3 boundary concern (evaluation suppression risk); PO accepted scope constraint (notification dispatch deduplication only, not evaluation suppression). SPS = 2. Zero-sum satisfied: 1 Add, 1 displacement named.

---

### DL-016 — 2026-03-31

**Decision type:** Add (backlog-level)
**Cycle:** 2026-03-31__scheduled
**Date:** 2026-03-31
**Decision owner:** Product Owner

**Initiative:** BLG-GOV-09 — Cycle velocity metric

**Gate cleared:** v2.3 shipped; capacity freed from BLG-GOV-07 (shipped) and BLG-GOV-08 (returned to backlog at P3) — prior park rationale "capacity constrained with GOV-07/08 in v2.3" resolved.

**Displacement:** BLG-GOV-03 (simplify cycle artefact sealing, P3) deprioritised in v2.4 planning queue.

**Workforce impact:** S effort (~0.5 day). PMO Lead + Head of Engineering documentation task.

**Rationale:** v2.3 triggered a capacity warn that historical throughput data might have predicted. Velocity metric directly addresses recurring over-planning pattern. Challenger cleared with no counter-argument (SPS=1, pure governance tooling). Zero-sum satisfied: 1 Add, 1 displacement named.


---

### DL-017 — 2026-04-05

**Decision type:** Add (backlog-level)
**Cycle:** 2026-04-05__scheduled
**Date:** 2026-04-05
**Decision owner:** Product Owner

**Initiative:** BLG-FE-09 — Frontend Performance Budget

**Gate cleared:** BLG-OPS-05 (API performance baseline) shipped v2.4 — prior park rationale "BLG-OPS-05 still active" now resolved. Frontend budget can now be aligned to the documented backend latency floor.

**Displacement:** BLG-GOV-08 (engine prompt compression, P3, L effort) deprioritised in v2.5 planning queue.

**Workforce impact:** S effort (~0.5 day). Frontend Specifications & UX Documentation Owner — spec document only, no code change.

**Rationale:** BLG-OPS-05 shipping created a natural alignment point for a companion frontend performance budget. Challenger cleared (SPS=2, pure documentation). Zero-sum satisfied: 1 Add, 1 displacement named.

---

### DL-018 — 2026-04-05

**Decision type:** Add (backlog-level)
**Cycle:** 2026-04-05__scheduled
**Date:** 2026-04-05
**Decision owner:** Product Owner

**Initiative:** BLG-SPEC-D17 — Spec Dependency Map

**Gate cleared:** BLG-SPEC-T01 shipped v2.2; BLG-SPEC-D15/D16 shipped v2.4 — prior park rationale "spec debt items higher priority" resolved. Canonical spec library now stable enough that a dependency map provides real impact-analysis value.

**Displacement:** BLG-FE-03 (error message mapping layer, P3, M effort) deprioritised in v2.5 planning queue.

**Workforce impact:** M effort (~1–2 days). Head of Specs Team — read-only reference document (scope constrained: not a CI-checked index).

**Rationale:** Challenger issued Type A counter-argument (maintenance risk for a living document). PO accepted scope constraint: read-only reference with explicit staleness acknowledgement — eliminates the maintenance risk while preserving impact-analysis value. Zero-sum satisfied: 1 Add, 1 displacement named.

---

### DL-019 — 2026-04-05

**Decision type:** Add (backlog-level)
**Cycle:** 2026-04-05__scheduled
**Date:** 2026-04-05
**Decision owner:** Product Owner

**Initiative:** BLG-GOV-14 — Governance Health Score

**Gate cleared:** BLG-GOV-09 (cycle velocity metric, companion idea IDEA-pmo-lead-20260321-01) shipped v2.4 — prior park rationale "revisit once IDEA-pmo-lead-20260321-01 advances" satisfied.

**Displacement:** BLG-GOV-11 (cycle artefact inventory, P3, M effort) deprioritised in v2.5 planning queue.

**Workforce impact:** M effort (~1–2 days). PMO Lead + Head of Specs Team — advisory indicator implementation; formula must be documented in AC before implementation.

**Rationale:** Natural companion to BLG-GOV-09 (velocity). Challenger cleared (SPS=1, pure governance tooling) with formula-completeness note — formula explicitly included in backlog AC. Advisory only, not a gate. Zero-sum satisfied: 1 Add, 1 displacement named.

---

### DL-020 — 2026-04-17

**Decision type:** No-change
**Cycle:** 2026-04-17__scheduled
**Date:** 2026-04-17
**Decision owner:** Product Owner

**Summary:** Scheduled roadmap rebalance — no initiatives added, replaced, deferred, or killed.

**Rationale:** No active Now initiatives exist. The v2.8 backlog (8 P3 items) is the appropriate planning input for the next release. All 22 parked ideas were re-parked after stale-idea review — none met the threshold for advancement at this time. No new ideas submitted (intake engine skipped; 22 open ideas ≥ 20 threshold). CPS = 0.0 (no active initiatives); no strategy drift. No workforce allocation changes required.

**Roadmap impact:** current_roadmap.md Last Updated bumped to 2026-04-17. No content changes.

**Workforce impact:** None — no new allocations required.

---

### DL-021 — 2026-04-21

**Decision type:** No-change (roadmap) + Backlog Add (×14)
**Cycle:** 2026-04-21__scheduled
**Date:** 2026-04-21
**Decision owner:** Product Owner

**Summary:** Scheduled roadmap rebalance — no roadmap-level initiatives added, replaced, deferred, or killed. 14 new backlog items promoted from idea intake (IW-20260421-01 + 5 stale ideas newly gate-cleared). 2 ideas parked during debate.

**Initiatives added (backlog-level):**

| ID | Title | Priority | Effort | Displacement |
|----|-------|----------|--------|-------------|
| BLG-SPEC-20 | Machine-readable spec front-matter standard | P3 | S | BLG-GOV-11 (P3) deprioritised |
| BLG-AI-01 | AI Journal summary audit log | P2 | S | TEST-GAP-EPIC-04 (P3) deprioritised |
| BLG-AI-02 | Model version contract for AI Journal | P3 | S | BLG-FEAT-13 (P3) deprioritised |
| BLG-FEAT-18 | Consecutive losing streak metric | P2 | S | BLG-DATA-01 (Positions Data Dictionary, P2) deprioritised |
| BLG-FEAT-19 | Monthly P&L summary report | P2 | S | BLG-GOV-11 (P3) dual displacement |
| BLG-FE-16 | React component inventory | P3 | M | BLG-FE-15 (P3) deprioritised |
| BLG-SPEC-21 | Screener results schema spec | P1 | S | BLG-GOV-11 (P3) triple displacement (combined S+S+S effort < M displaced) |
| BLG-SPEC-22 | Alpaca API integration contract | P1 | S | BLG-GOV-08 (P3) further deferred |
| BLG-SPEC-23 | Screener internal API contract | P1 | S | BLG-TECH-05 (P3) deprioritised |
| BLG-QA-08 | External API mock harness for CI | P1 | M | BLG-FEAT-13 (P3) displaced |
| BLG-GOV-16 | §13 review record for DS-06 Alpaca News | P1 | S | BLG-FE-09 (P3) deprioritised |
| BLG-OPS-12 | External API health check extension | P2 | S | BLG-GOV-11 (P3) dual displacement |
| BLG-QA-09 | Screener test data library | P1 | M | BLG-FEAT-13 (P3) dual displacement |
| BLG-FE-17 | Screener results page UX spec | P1 | M | BLG-TECH-05 (P3) dual displacement |

**Explicit displacement:**
- BLG-GOV-11 displaced by 4 items (BLG-SPEC-20, BLG-FEAT-19, BLG-SPEC-21, BLG-OPS-12); combined effort ~2.5 days S-band < M-band displaced
- BLG-FEAT-13 displaced by 3 items (BLG-AI-02, BLG-QA-08, BLG-QA-09)
- BLG-TECH-05 displaced by 2 items (BLG-SPEC-23, BLG-FE-17)

**Roadmap impact:** current_roadmap.md Last Updated bumped to 2026-04-21. No content changes.

**Workforce impact:** ~13.5 days total across mixed skill domains. Governance load ~22% (within 20–60% bounds). No scarce skill conflicts. All items are Arc 1 pre-work (spec authoring, test infrastructure, governance compliance).

**Rationale:** 14 items advanced from IW-20260421-01 (44 new ideas + 16 stale parked) following structured debate with 16 candidates. Two candidates parked during debate (IDEA-strategy-owner-20260321-02 accepted Challenger argument; IDEA-challenger-20260421-02 self-assessment accepted). All items are Arc 1 prerequisite work (screener specs, Alpaca contracts, test infrastructure, §13 governance) needed before v2.9 sprint planning. Net-zero satisfied at roadmap level (0 adds, 0 kills). Backlog-level net-zero satisfied via named displacements. Workforce gate: PASS. STEP 8.6 guardrail: PASS (2 items parked during debate; Challenger issued 4 Type A counter-arguments).

---

### DL-022 — 2026-04-24

**Decision type:** No-change (roadmap) + Backlog Add (×2)
**Cycle:** 2026-04-24__scheduled
**Date:** 2026-04-24
**Decision owner:** Product Owner

**Summary:** Scheduled roadmap rebalance — no roadmap-level initiatives added, replaced, deferred, or killed. 2 new backlog items promoted from gate-cleared idea review.

**Initiatives added (backlog-level):**

| ID | Title | Priority | Effort | Displacement |
|----|-------|----------|--------|-------------|
| BLG-FE-19 | Keyboard shortcuts for trading actions | P3 | S | BLG-TECH-05 (P3) moved to §9 Deferred |
| BLG-OPS-14 | AI Journal monitoring metrics | P3 | S | BLG-SPEC-20 (P3) moved to §9 Deferred |

**Explicit displacement:**
- BLG-TECH-05 (Prometheus metrics endpoint, P3, M effort, single-user scale deferral) — permanently deferred to §9 Future Candidates
- BLG-SPEC-20 (machine-readable spec front-matter standard, P3, S effort) — deferred to §9; Arc 1 specs shipped without requiring this standard; investment deferred until CI compliance checking becomes a priority

**Roadmap impact:** current_roadmap.md Last Updated bumped to 2026-04-24. No content changes to arc structure or horizon placements.

**Workforce impact:** ~1 FTE-day total (2 × S effort). Frontend (keyboard shortcuts) + backend (GET /health extension). Governance load 0% — PO sign-off capacity confirmed.

**Rationale:** 45 ideas reviewed. 10 gate-cleared ideas surfaced (BLG-SPEC-21, BLG-SPEC-22, BLG-FE-17, BLG-AI-01, BLG-QA-08 shipped v2.9). 7 gate-cleared ideas rejected as superseded by spec delivery. 2 advanced: keyboard shortcuts (BLG-FE-02/03 gate cleared 10 cycles ago), AI Journal monitoring (BLG-AI-01 gate cleared this cycle). 1 gate-cleared idea parked after debate (data pipeline tests belong in DS-01 sprint scope, not pre-implementation backlog). 3 stale ideas retired (cycle 6, no path). Net-zero satisfied: 2 adds, 2 confirmed defers. Workforce gate: PASS. STEP 8.6 guardrail: PASS (Challenger issued Type A counter-argument for data pipeline tests; 1 item parked).

---

### DL-023 — 2026-04-24

**Decision type:** Defer (backlog-level)
**Cycle:** 2026-04-24__scheduled
**Date:** 2026-04-24
**Decision owner:** Product Owner

**Initiatives deferred to §9 Future Candidates:**

| ID | Title | Reason |
|----|-------|--------|
| BLG-TECH-05 | Prometheus metrics endpoint | Indefinitely deferred — single-user scale; no operational need at current deployment; permanently moved to Future Candidates |
| BLG-SPEC-20 | Machine-readable spec front-matter standard | Deferred — Arc 1 spec delivery (BLG-SPEC-21/22/23) shipped without requiring this standard; CI compliance checking investment deferred; moved to Future Candidates |

**Workforce impact:** None — no work stopped; both items were P3 with no active sprint slot.

**Rationale:** Displacement required for DL-022 backlog additions. Both items are P3 with no urgency increase in the foreseeable roadmap. BLG-TECH-05 has been deprioritised across multiple prior cycles (DL-021, DL-023 rotation). BLG-SPEC-20 was added only 1 cycle ago but its stated precondition (Arc 1 specs) is now met and CI checking is not yet a bottleneck.

---

### DL-024 — 2026-05-05

**Decision type:** No-change (roadmap) + Backlog Add (×5)
**Cycle:** 2026-05-05__scheduled
**Date:** 2026-05-05
**Decision owner:** Product Owner

**Summary:** Scheduled roadmap rebalance — no roadmap-level initiatives added, replaced, deferred, or killed. 5 new backlog items promoted from gate-cleared and stale idea review. 2 items parked in STEP 5 debate (accepted Challenger). 10 items rejected (9 not strong, 1 strong). 15 re-parked with updated rationales.

**Run tier:** Standard (scheduled; last scheduled rebalance 2026-04-29; < 90 day threshold; CPS = 0.0)

**CPS this cycle:** 0.0 (zero active initiatives — all v3.1 items shipped). Prior CPS: 0.0 (cycle 2026-04-24__scheduled). Delta: 0.0. No drift alert.

**Key context:** Arc 1 fully complete (DS-04 shipped v3.1). 24 parked ideas had gate-cleared conditions triggered by Arc 1 completion — mandatory re-evaluation performed on all. Now horizon empty post-v3.1. Arc 2 continuation (PT-02 frontend, PT-03, PT-05) correctly placed in Next horizon.

**Initiatives added (backlog-level):**

| ID | Title | Priority | Effort | Source | Displacement |
|----|-------|----------|--------|--------|-------------|
| BLG-FE-21 | Design system document | P3 | M | IDEA-head-of-ux-20260321-02 (stale, gate cleared Arc 1) | Next P3 FE backlog slot |
| BLG-FEAT-20 | Net-of-costs performance tracking | P2 | M | IDEA-financial-reporting-20260321-02 (stale, PT-01 unlocks) | P2 FEAT backlog slot; delivery deferred to Arc 3/4 context |
| BLG-FE-22 | Screener morning routine UX spec | P2 | S | IDEA-product-owner-20260421-01 (gate cleared DS-01/02) | P2 UX spec backlog slot |
| BLG-GOV-18 | External API dependency risk register | P3 | S | IDEA-pmo-lead-20260421-01 (gate cleared Arc 1) | P3 GOV backlog slot |
| BLG-SEC-05 | Alpaca API key rotation policy + credential audit | P2 | S | IDEA-cybersecurity-20260421-01 + -02 (gate cleared Arc 1) | P2 SEC backlog slot; IDEA-cybersecurity-20260421-02 scope subsumed |

**Items parked in STEP 5 debate (Challenger argument accepted):**
- IDEA-cybersecurity-20260421-02: Scope subsumed into BLG-SEC-05 (overlap argument accepted)
- IDEA-finops-20260421-01: Premature — 10 days of DS-01 operation insufficient to characterise Alpaca call volume; park for 60 days

**Items rejected this cycle:** 10 (IDEA-challenger-20260321-01, IDEA-ai-compliance-20260321-01 [strong], IDEA-infra-ops-20260421-02, IDEA-challenger-20260421-01, IDEA-backend-engineering-20260421-01, IDEA-head-of-engineering-20260421-02, IDEA-data-model-20260421-02, IDEA-director-of-hr-20260421-02, IDEA-qa-testing-20260421-02, IDEA-qa-lead-20260421-02)

**Roadmap impact:** current_roadmap.md Last Updated bumped to 2026-05-05. No arc structure or horizon changes.

**Workforce impact:** ~5–8 FTE-days total across 5 new items (all documentation/spec/governance tasks). Governance load 6% — below 20% floor; PO confirmed adequate sign-off capacity. No Skill-Silo Alert.

**Displacement:** No roadmap-level Adds → no roadmap-level Kills required. Net-zero: 0 Adds = 0 Kills ✅. Backlog-level: each new item takes a named backlog priority slot per table above.

**STEP 8.6 guardrail:** 2 items parked in debate (IDEA-cybersecurity-20260421-02, IDEA-finops-20260421-01); Challenger issued Type A counter-arguments for both. PASS.

**Meta-review:** NOT due — 2 cycles since last meta-review (2026-04-21__scheduled); threshold is 3 cycles. Next meta-review due: v3.3 rebalance cycle or 2026-06-05__scheduled (whichever comes first).

---

### DL-025 — 2026-05-08

**Decision type:** Add (backlog-level × 16)
**Cycle:** 2026-05-08__scheduled
**Date:** 2026-05-08
**Decision owner:** Product Owner
**Run tier:** Standard

**Context:** Scheduled rebalance. No active roadmap-level initiatives (CPS = 0.0). v3.2 Verified 2026-05-05; post-ship closure complete 2026-05-07. Ideas window IW-20260508-01 opened (44 submissions, 22 agents). 17 open parked ideas reviewed. Register integrity correction applied (IDEA-finops-20260421-01 and IDEA-cybersecurity-20260421-02 park counts corrected +1 for 2026-05-05 cycle miss).

**Gate-cleared ideas actioned:**
- IDEA-frontend-ux-20260304-02: BLG-FE-16 shipped v3.2 → gate cleared → PO re-park (accessibility still P3)
- IDEA-cybersecurity-20260421-02: BLG-SEC-05 shipped v3.2 → gate cleared → Rejected (purpose delivered)

**Items added to backlog (16):**

| BLG ID | Title | Priority | Effort | Source Idea | Slot |
|--------|-------|----------|--------|------------|------|
| BLG-SPEC-24 | PT-02 research view canonical spec | P1 | M | IDEA-head-of-specs-20260508-01 | P1 SPEC backlog slot |
| BLG-SPEC-25 | PT-02 research endpoint API contract | P1 | S | IDEA-api-contracts-20260508-01 | P1 SPEC backlog slot |
| BLG-SPEC-26 | Research view data source provenance spec | P1 | S | IDEA-challenger-20260508-01 | P1 SPEC backlog slot |
| BLG-FE-28 | Pre-Trade Research View UX spec | P1 | S | IDEA-frontend-ux-20260508-01 | P1 FE backlog slot |
| BLG-FE-29 | Watchlist research status indicator (binary flag) | P2 | XS | IDEA-product-owner-20260508-02 | P2 FE backlog slot |
| BLG-FE-30 | Trade plan status badges | P2 | S | IDEA-base44-frontend-20260508-02 | P2 FE backlog slot |
| BLG-GOV-19 | PT-05 entry checklist §13 compliance review | P1 | XS | IDEA-strategy-owner-20260508-01 | P1 GOV backlog slot |
| BLG-GOV-20 | Trade plan field extension governance | P2 | S | IDEA-data-model-20260508-01 | P2 GOV backlog slot |
| BLG-GOV-21 | Arc 4 data requirements capture | P3 | XS | IDEA-head-of-ux-20260508-02 | P3 GOV backlog slot |
| BLG-FEAT-21 | Trade plan abandonment status field | P2 | S | IDEA-challenger-20260508-02 | P2 FEAT backlog slot |
| BLG-OPS-15 | Research endpoint latency monitoring | P2 | S | IDEA-infra-ops-20260508-01 | P2 OPS backlog slot |
| BLG-QA-15 | PT-02 research view acceptance test protocol | P1 | S | IDEA-director-of-quality-20260508-01 | P1 QA backlog slot |
| BLG-QA-16 | Research endpoint integration test coverage | P1 | S | IDEA-head-of-engineering-20260508-01 | P1 QA backlog slot |
| BLG-QA-17 | Research view test scenario library | P1 | S | IDEA-qa-testing-20260508-01 | P1 QA backlog slot |
| BLG-SEC-06 | Trade plan data sensitivity classification | P2 | XS | IDEA-cybersecurity-20260508-01 | P2 SEC backlog slot |
| BLG-AI-03 | AI Journal Summarisation quarterly review cadence | P3 | XS | IDEA-ai-compliance-20260508-02 | P3 AI backlog slot |

**Items parked in STEP 5 (from new submissions):** 28 ideas → Parked-cycle-1

**Items rejected this cycle:** 1 (IDEA-cybersecurity-20260421-02 — purpose delivered by BLG-SEC-05)

**Challenger Type A counter-arguments:** 4 (BLG-GOV-19, BLG-FE-29, BLG-GOV-20, BLG-GOV-21); all PO accepted with rationale

**Roadmap impact:** current_roadmap.md Last Updated bumped to 2026-05-08. No arc structure or horizon changes.

**Displacement (backlog-level net-zero):** Each add has a named displacement: BLG-FE-23 (for BLG-GOV-19), BLG-FE-24 (for BLG-SPEC-26, BLG-FE-28, BLG-AI-03), BLG-FE-25 (for BLG-FE-29, BLG-FE-30, BLG-QA-17), BLG-FE-26 (for BLG-SPEC-24), BLG-FE-27 (for BLG-SEC-06, BLG-GOV-21), BLG-FEAT-20 (for BLG-GOV-20, BLG-FEAT-21, BLG-QA-15), BLG-OPS-13 (for BLG-SPEC-25, BLG-OPS-15, BLG-QA-16). Net-zero: backlog-level Adds with named deprioritisations ✅

**Skill-Silo check:** 6 of 16 items are governance/spec (37.5%) — within 20–60% bounds. No Skill-Silo Alert.

**STEP 8.6 guardrail:** 4 Challenger Type A counter-arguments across 16 advancing ideas; not all candidates advanced without challenge. PASS.

**Meta-review:** DUE — 3rd cycle since last meta-review (2026-04-21__scheduled). Conducted — no prompt patches warranted. Single Type D incident (2026-05-05 F-01) was isolated. `last_meta_review_cycle` updated to 2026-05-08__scheduled.

---

### DL-026 — 2026-05-13

**Decision type:** Kill
**Initiative:** BLG-GOV-08 — Engine Prompt Compression (roadmap deferred items reference)
**Cycle:** 2026-05-13__scheduled
**Displacement:** N/A — this is a Kill/retirement
**Workforce impact:** None (deferred item, consuming no active resources)
**Rationale:** 9+ consecutive deferrals (v2.4–v3.3). Original scope was compression of roadmap_prompt.md and release_planning_prompt.md for token efficiency. Partial delivery achieved: roadmap_prompt.md v6.0 (cycle 2026-05-13 AUD-2026-05-13 Tier 1 improvement) saved 8,104 tokens/cycle — the primary value has been delivered. BLG-GOV-08 is already in backlog_archive.md; the roadmap's deferred items section carried a stale pointer with a ⚠️ stale notice explicitly requesting retirement at this rebalance. No new trigger has emerged in 9 cycles. Retiring the roadmap reference. The archived backlog item record is preserved for historical reference.
**Decision owner:** Product Owner

---

### DL-027 — 2026-05-13

**Decision type:** Add (to backlog)
**Initiative:** BLG-QA-18 — Screener Accuracy Test Protocol
**Source idea:** IDEA-director-of-quality-20260421-02
**Cycle:** 2026-05-13__scheduled
**Displacement:** BLG-OPS-13 deprioritised (performance baseline update for 18 new endpoints — P3; no latency incidents; continuing to defer)
**Workforce impact:** S effort (~0.5–1 day); adds to QA backlog; no new FTE required
**Rationale:** Screener in stable production 46+ days since v3.0. A formal accuracy test protocol against known inputs is now warranted to prevent silent regression of §11 deterministic filter logic. Gate condition cleared. Stale idea (3 consecutive parks) requires active promotion per STEP 4.5. Challenger issued a Clearance Statement confirming no §13 engagement. Scores: Risk Reduction 4/5; SPS = 1; Effort S.
**Decision owner:** Product Owner

---

### DL-028 — 2026-05-13

**Decision type:** Add (to backlog)
**Initiative:** BLG-FE-31 — Research View Component Library
**Source idea:** IDEA-base44-frontend-20260508-01
**Cycle:** 2026-05-13__scheduled
**Displacement:** BLG-FE-27 deprioritised (Nav bar redesign exploration, P3; no immediate implementation target)
**Workforce impact:** S effort (~0.5–1 day); adds to FE backlog; no new FTE required
**Rationale:** PT-02 research view frontend shipped v3.2. Arc 3 frontend stories ST-03/05/07 (returned to backlog) are confirmed v3.4 items that will reuse PT-02 components (price card, regime panel, news feed, source attribution). A component catalogue at sprint planning time prevents duplicate implementation. Gate condition (PT-02 frontend delivery) cleared. Challenger Type A counter-argument (staleness risk) rebutted by PO: reuse trigger is confirmed, not speculative. Scores: Risk Reduction 3/5; SPS = 1; Effort S.
**Decision owner:** Product Owner

---

### DL-029 — 2026-05-15

**Decision type:** No-change (roadmap-level) + Add (to backlog)
**Initiative:** BLG-QA-19 — Research View Regression Test Protocol
**Source idea:** IDEA-qa-lead-20260508-02
**Cycle:** 2026-05-15__scheduled
**Displacement:** BLG-FE-27 deprioritised (Nav bar redesign exploration, P3; no immediate sprint dependency — existing displacement candidate)
**Workforce impact:** S effort (~0.5 day); adds to QA backlog; no new FTE required
**Rationale:** BLG-QA-15 (PT-02 research view acceptance test protocol) ✅ v3.3; PT-03 (entry conditions) ✅ v3.2; PT-05 (entry checklist UX) ✅ v3.2. Research view now encompasses data from all three shipped features. Arc 3 stories IT-04/IT-05 (risk data fields) are confirmed to add further fields to the research endpoint. Without a regression protocol, each story must independently define coverage. Challenger argument (gate-cleared advance): research view scope now encompasses PT-03/04 data fields; formalising the regression protocol before IT-04/IT-05 prevents coverage inconsistency. PO accepted. Scores: Risk Reduction 4/5; SPS = 1; Effort S.
**Decision owner:** Product Owner

---

### DL-030 — 2026-05-16

**Decision type:** No-change (roadmap and backlog)
**Cycle:** 2026-05-15__scheduled-2
**Displacement:** N/A — no additions this cycle
**Workforce impact:** None
**Rationale:** Post-v3.5-close scheduled rebalance. Horizon Now empty — v3.6 planning has not yet commenced. All active initiatives (Arc 4–6, PT-04) reaffirmed as 🔥 Must continue. Two gate-cleared ideas reviewed (IDEA-ai-compliance-20260508-01 and IDEA-financial-reporting-20260508-02 — both gated on BLG-GOV-21 which shipped v3.5): both re-parked with updated rationale (ai-compliance: AI trade plan summarisation not yet scoped; financial-reporting: planned_entry_price snapshotting explicitly deferred in arc4_data_requirements.md §3.1). No advancing candidates. Zero displacement required. No backlog additions warranted — existing 7 active backlog items provide sufficient near-term work queue for v3.6 planning.
**Decision owner:** Product Owner

---

### DL-031 — 2026-05-19

**Decision type:** No-change (roadmap and backlog)
**Cycle:** 2026-05-19__scheduled
**Displacement:** N/A — no additions this cycle
**Workforce impact:** None
**Rationale:** Scheduled rebalance post-v3.7 close. Now horizon empty — v3.8 release planning not yet commenced. All active initiatives (Arc 4–6, PT-04) reaffirmed as 🔥 Must continue. One gate-cleared idea re-evaluated: IDEA-financial-reporting-20260508-02 (planned_entry_price snapshotting shipped v3.6 — technical gate met). PO re-parked with new rationale: data density insufficient (fewer than 20 closed trades with plans and entry_delta_pct populated); portfolio-level entry zone discipline metric premature; entry_delta_pct already surfaced at trade-plan detail level via PlanVsReality (v3.6). 32 other ideas re-parked with park counts incremented (+1 each; last committed increment was cycle 2026-05-15__scheduled-2). No advancing candidates. Zero displacement required. No backlog additions warranted — 5 active backlog items sufficient for v3.8 planning. Note: prior cycles 2026-05-18__scheduled and 2026-05-18__scheduled-2 have no committed artefacts; decision log entries DL-031 through DL-032 cited in memory records are absent from this file — this run uses DL-031 as next sequential entry.
**Decision owner:** Product Owner

---

### DL-032 — 2026-05-21

**Decision type:** No-change (roadmap-level) + Ideas register migration (3-cycle cap enforcement)
**Cycle:** 2026-05-21__scheduled
**Displacement:** N/A — no roadmap additions this cycle
**Workforce impact:** None
**Rationale:** Scheduled rebalance post-v3.8 close. Now horizon empty — v3.9 release planning not yet commenced. All active initiatives (Arc 4–6 remaining) reaffirmed as 🔥 Must continue. SI-01 shipped v3.8; Arc 5 active initiatives updated. One gate-cleared idea evaluated: IDEA-pmo-lead-20260508-01 (Arc 3 completion gate met) — PO rejects: milestone tracking covered by existing artefacts at sole-developer scale. First rebalance run under roadmap_prompt.md v6.3+ (3-cycle hard cap). 33 parked ideas all at park count ≥ 3 (range 5–13); terminal classification applied: 29 promoted to backlog as gate-conditional items (BLG-FEAT-26–35, BLG-FE-39, BLG-BE-13–14, BLG-QA-21–23, BLG-OPS-17–24, BLG-SPEC-32, BLG-GOV-26–29), 4 rejected not strong. Ideas register now clean. No roadmap additions; net-zero passes (0 additions, 0 kills).
**Decision owner:** Product Owner
