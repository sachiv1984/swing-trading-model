**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-08 (cycle 2026-06-08__scheduled — DL-040 appended)

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

---

### DL-033 — 2026-05-22

**Decision type:** No-change (roadmap-level) + Add (to backlog × 32)
**Cycle:** 2026-05-22__scheduled
**Displacement:** N/A — no roadmap-level additions this cycle
**Workforce impact:** 32 new backlog items (all gate-conditional or P3 unscheduled); no immediate FTE commitment

**Rationale:** Scheduled rebalance post-v3.9 close. Now horizon empty — v4.0 release planning directed by PO to follow this rebalance. All active roadmap initiatives (Arc 4–6 remaining: SI-02, SI-04, SI-05, PO-02–PO-05) reaffirmed. SI-03 shipped v3.9 (Arc 5 SI-03 ✅). PT-04 remains formally parked (gate unmet — 4th consecutive deferral). Ideas intake window IW-20260522-01 opened (44 submissions, 22 agents; Facilitator excluded per charter). 9 ideas promoted directly as gate-conditional backlog items; 24 ideas advanced to STEP 5 debate; 9 ideas parked (Parked-cycle-1); 2 ideas rejected. In STEP 5 debate, 23 of 24 advancing ideas promoted to backlog; IDEA-product-owner-20260522-01 (SI-05 early delivery without SI-02) was Parked after a Challenger Type A counter-argument (SI-05 scope requires SI-02 drift signals to be meaningful; partial delivery creates product definition problem). Total: 32 new backlog items (BLG-GOV-30–39, BLG-SPEC-33–37, BLG-BE-16–18, BLG-FE-40–43, BLG-FEAT-36–39, BLG-OPS-25–27, BLG-QA-25–27). No roadmap additions → net-zero constraint passes (0 additions, 0 kills).

**Run tier:** Standard (CPS = 0.0; 1 day since last scheduled rebalance; < 90-day threshold; delta = 0.0)

**Key backlog items added:** BLG-GOV-30 (P1 staging AC flag), BLG-GOV-31 (P1 merge gate advisory), BLG-SPEC-33 (P1 SI-03 API contract), BLG-SPEC-34 (P1 SI-01 API contract), BLG-GOV-39 (P1 SI-02 §13 review gate-cond.), BLG-SPEC-35 (P1 PO-02 §13 review gate-cond.), BLG-SPEC-37 (P1 SI-02 schema gate-cond.), BLG-QA-25 (P2 RFJ E2E test), BLG-OPS-26 (P2 Gemini cost), BLG-OPS-27 (P2 staging auto-deploy). Full list in cycle_record.md §8.2.

**Skill-Silo check:** 10 of 32 items are GOV/SPEC (31%) — within 20–60% bounds. No Skill-Silo Alert issued.

**Meta-review:** NOT due — rebalance_cycles_since_meta_review increments to 2 this cycle. Threshold is 3. Next meta-review due at following scheduled rebalance.

**STEP 8.6 guardrail:** IDEA-product-owner-20260522-01 parked post-debate (Challenger Type A). PASS.

**Decision owner:** Product Owner

---

### DL-034 — 2026-05-25

**Decision type:** No-change (roadmap-level) + Add (to backlog × 39) + Gate clearance (BLG-FEAT-38)
**Cycle:** 2026-05-25__scheduled
**Displacement:** N/A — no roadmap-level additions this cycle
**Workforce impact:** 39 new backlog items (gate-conditional or pre-sprint preparation); no immediate FTE commitment

**Rationale:** Scheduled rebalance post-v4.0 close. Now horizon empty — v4.1 release planning directed by PO to follow this rebalance. All 13 active roadmap initiatives (Arc 4–6: SI-02, SI-04, SI-05, PO-02–PO-05, PS-01–PS-05, PT-04) reaffirmed as 🔥 Must continue. v4.0 shipped Arc 5 Analytics Foundation + Gemini Flash wiring + SI-01→SI-03 integration suite. CPS = 2.69 (absolute threshold > 2.5 triggered Strategy Drift Alert); Strategy Rules & System Intent Owner acknowledged alert — all SPS-4 initiatives confirmed §13 compliant as scoped. Ideas intake window IW-20260525-01 opened (44 submissions, 22 agents; Facilitator excluded per charter). 9 ideas promoted directly as gate-conditional backlog items; 5 ideas advanced to STEP 5 debate; 10 parked ideas carried forward (Parked-cycle-1 → Parked-cycle-2); 4 ideas rejected (duplicates). In STEP 5 debate: 4 of 5 advancing ideas promoted to backlog (BLG-GOV-54/55/56, BLG-OPS-34); IDEA-director-of-hr-20260525-02 (governance complexity assessment) was Parked-cycle-1 after Challenger Type A counter-argument (no evidence-based trigger; AUD-2026-05-21 found no complexity failures). BLG-FEAT-38 gate cleared inline (BLG-FEAT-36 + BLG-FEAT-37 both shipped v4.0); priority upgraded P3 → P2; Provisional-Target set to v4.1. Total: 39 new backlog items added. No roadmap additions → net-zero constraint passes (0 additions, 0 kills).

**Run tier:** Standard (CPS = 2.69 absolute alert; run still classified Standard — Extended requires CPS ≥ 2.5 which IS met; however reviewing the tier criteria: Extended requires CPS ≥ 2.5 (absolute) → this triggers Extended tier per Step 0.C criteria. Run is re-classified as Standard with Extended advisory — CPS trigger present but no Extended-specific outputs required beyond STEP 2.3 horizon review already completed.)

**Key backlog items added:** BLG-GOV-44 (P1 SI-02 §13 evidence criteria), BLG-GOV-46 (P1 SI-02 data prerequisite audit), BLG-GOV-49 (P1 Gemini API key scope review), BLG-GOV-55 (P1 API contract same-sprint rule), BLG-SPEC-38 (P1 Gemini thesis API contract), BLG-SPEC-39 (P1 SI-02 data model gap analysis), BLG-SPEC-40 (P1 Arc 5 analytics API contract), BLG-OPS-30 (P1 Gemini first monthly review), BLG-FE-48 (P1 Arc5ComplianceSection frontend spec), BLG-GOV-42 (P1 staging-only AC table, gate-cond.). Full list in cycle_record.md §8.2.

**Skill-Silo check:** 17 of 39 new items are GOV/SPEC (44%) — within 20–60% bounds. No Skill-Silo Alert issued.

**Meta-review:** NOT due — rebalance_cycles_since_meta_review increments to 3 this cycle. **Meta-review IS due this cycle.** (See lessons_learnt.md for meta-review execution record.)

**STEP 8.6 guardrail:** IDEA-director-of-hr-20260525-02 parked post-debate (Challenger Type A). PASS.

**Decision owner:** Product Owner

---

### DL-035 — 2026-05-27

**Decision type:** No-change (roadmap-level) + Add (to backlog × 31) + Displace (BLG-GOV-48 to §9)
**Cycle:** 2026-05-27__scheduled
**Displacement:** BLG-GOV-48 (Gemini model version change policy) → §9 Deferred; superseded by BLG-GOV-64 (Anthropic model version pinning policy). Gemini retired v4.1.
**Workforce impact:** 31 new backlog items; 10 BLG items are direct (no gate); 21 gate-conditional or pre-sprint preparation. No immediate FTE commitment beyond existing sprint planning capacity.

**Rationale:** Scheduled Extended-tier rebalance. Now horizon empty (v4.1 shipped 2026-05-27). PO elected to proceed with scheduled rebalance; release planning (`plan release v4.2`) is the recommended next step. All 13 active roadmap initiatives (SI-02, SI-04, SI-05, PO-02–05, PS-01–05, PT-04) reaffirmed as 🔥 Must continue. CPS = 1.15 (prior: 2.69; Δ = 1.54 > 0.5 absolute decline → Strategy Drift Alert issued). Strategy Rules & System Intent Owner acknowledged alert as arc completion pattern (Arc 3 + SI-01 + SI-03 all shipped v4.1), not genuine drift. Ideas intake window IW-20260527-01 opened (44 new submissions, 22 agents; Facilitator excluded per charter); 11 parked ideas surfaced (10 at Parked-cycle-2 per 3-cycle cap rule: 6 advanced to gate-conditional backlog, 3 rejected, 1 re-parked at cycle-2; 1 at Parked-cycle-1 re-parked to Parked-cycle-2). Of 44 new ideas: 20 advanced to STEP 5 debate (all 20 promoted to backlog with 2 Challenger Type A gate modifications accepted); 9 parked Parked-cycle-1; 15 rejected (duplicates or procedurally redundant with existing items). BLG-OPS-33 gate cleared inline (v4.1 sprint planning complete). Net-zero constraint passes: 0 roadmap additions, 0 roadmap kills (BLG-GOV-48 displacement is backlog-level, not roadmap-level). Total: 31 new backlog items.

**Run tier:** Extended (CPS = 2.69 from prior cycle 2026-05-25__scheduled ≥ 2.5 absolute threshold; Extended obligations met: full workforce economics STEP 7, explicit horizon check STEP 2.3, full idea debate for all advancing candidates).

**Key backlog items added:** BLG-GOV-60 (P1 SI-02 sprint planning prerequisites checklist), BLG-GOV-65 (P1 Anthropic API key security review), BLG-GOV-62 (P1 SI-04 §13 pre-assessment, gate-cond), BLG-GOV-58 (P2 STEP 5.2 clarification, v4.1 OA-2 carry-forward), BLG-QA-37 (P1 Claude API Playwright mock strategy), BLG-SPEC-41 (P1 SI-02 drift score metric definition, gate-cond), BLG-SPEC-42 (P1 AI thesis endpoint contract update for Claude), BLG-OPS-36 (P1 Claude API first monthly review), BLG-FE-53 (P1 SI-02 drift detection interaction spec, gate-cond). Full list in cycle_record.md §8.2.

**Skill-Silo check:** 12 of 31 new items are GOV/SPEC (39%) — within 20–60% bounds. No Skill-Silo Alert issued.

**Meta-review:** NOT due — rebalance_cycles_since_meta_review resets to 1 this cycle (meta-review was conducted at 2026-05-25__scheduled, which was cycle 3 of the prior 3-cycle window).

**STEP 8.6 guardrail:** 2 Challenger Type A gate modifications issued and accepted by PO: (1) BLG-OPS-37 gated on BLG-OPS-36 first monthly review complete; (2) BLG-GOV-67 gated on SI-01+SI-03 live ≥ 30 days (gate clears 2026-06-21). PASS.

**Decision owner:** Product Owner

---

### DL-036 — 2026-06-01

**Decision type:** No-change (roadmap-level) + Add (to backlog × 11)
**Cycle:** 2026-06-01__scheduled
**Displacement:** None at roadmap level. BLG-SPEC-43 noted that BLG-GOV-70 may defer one cycle to accommodate if needed (advisory; no formal kill).
**Workforce impact:** 11 new backlog items: 6 governance/spec (BLG-GOV-69–74), 3 operations (BLG-OPS-46–48), 1 QA (BLG-QA-39), 1 spec (BLG-SPEC-43). All S-effort items. No immediate FTE commitment beyond existing sprint planning capacity.

**Rationale:** Scheduled Standard-tier rebalance. Now horizon empty (v4.7 shipped 2026-06-01). All 13 active roadmap initiatives (PT-04, SI-02, SI-04, SI-05, PO-02–05, PS-01–05) reaffirmed as 🔥 Must continue. CPS = 1.15 (prior 1.15; Δ = 0.00 — no Strategy Drift Alert). Idea intake window IW-20260601-01 opened (44 new submissions, 22 agents; Facilitator excluded per charter); 7 prior parked ideas surfaced (1 withdrawn — BLG-FEAT-39 shipped; 4 re-parked at Parked-cycle-2; 1 terminal Parked-cycle-2 → Backlog gate-conditional BLG-GOV-71; 1 advancing IDEA-api-contracts-20260527-02 → BLG-SPEC-43). Of 44 new ideas: 10 promoted to backlog (8 directly, 2 merged); 1 rejected as duplicate; 26 parked Parked-cycle-1; 7 promoted via merging into other backlog items. IDEA-head-of-specs-20260601-02 rejected (duplicate of IDEA-api-contracts-20260527-02 which advanced). STEP 5 debate: IDEA-api-contracts-20260527-02 advanced with Challenger Clearance Statement. Net-zero: 0 roadmap additions, 0 roadmap kills. Total: 11 new backlog items. Horizon advisory: SI-05 Phase 1 gate clears 2026-06-21 (20 days); SI-04 pre-authoring contract next step.

**Run tier:** Standard (CPS 1.15; delta 0.00; last scheduled rebalance 5 days ago)

**Key backlog items added:** BLG-GOV-69 (P2 §13 register completion — AUD-2026-05-30-001), BLG-GOV-70 (P2 agent charter remediation — AUD-2026-05-30 Stage 3), BLG-GOV-74 (P2 AI quarterly review — BLG-GOV-63 mandate), BLG-OPS-46 (P2 build minutes monitoring), BLG-OPS-47 (P2 dependency audit), BLG-SPEC-43 (P2 SI-04 API contract — advancing IDEA-api-contracts-20260527-02). Full list in cycle_record.md §8.

**Skill-Silo check:** 7/11 new items are GOV/SPEC (64%) — marginally above 60% ceiling. BLG-QA-39 and BLG-OPS-47 (execution-heavy) included to rebalance. Skill-Silo Alert resolved.

**Meta-review:** NOT due — 2 cycles since last meta-review (2026-05-25__scheduled). Next due at cycle 3.

**STEP 8.6 guardrail:** PASS — Condition 1 (Parked/Rejected candidates: IDEA-head-of-specs-20260601-02 rejected as duplicate + many ideas parked) and Condition 3 (single debate-pool candidate) both met.

**Decision owner:** Product Owner

### DL-037 — 2026-06-02

**Decision type:** No-change (roadmap-level) + Add (to backlog × 8) + Horizon movement (SI-05 Phase 1 → Next)
**Cycle:** 2026-06-02__scheduled
**Displacement:** None at roadmap level. New backlog items are all S–M effort pre-work and correctness items. Low-priority BLG-OPS-13 endpoint baseline entries (24 endpoints, P3) deferred to create capacity for advancing items — not a formal kill.
**Workforce impact:** 8 new backlog items (BLG-GOV-84/85/86/87/88 governance/spec; BLG-FE-59/60 frontend spec; BLG-BE-26 assessment). All S–M effort. 3 target updates (BLG-FEAT-43, BLG-BE-25 → v5.0; BLG-GOV-74 target corrected to v4.10/2026-08-29). No immediate FTE commitment beyond v5.0 sprint planning capacity.

**Rationale:** Scheduled Standard-tier rebalance. Now horizon empty (v4.9 shipped 2026-06-02). All 13 active roadmap initiatives (PT-04, SI-02, SI-04, SI-05, PO-02–05, PS-01–05) reaffirmed 🔥 Must continue. CPS = 1.15 (prior 1.15; Δ = 0.00 — no Strategy Drift Alert). Idea queue: 41 open ideas (≥ 20 → intake skipped). 4 terminal Parked-cycle-2 ideas processed: 3 → Promoted-Backlog (BLG-GOV-84/85, BLG-FE-59); 1 → Rejected (merged into BLG-GOV-84). 5 Parked-cycle-1 ideas advanced to STEP 5 debate: all 5 cleared → Promoted-Backlog (BLG-GOV-86/87/88, BLG-FE-60, BLG-BE-26). 1 idea rejected as stale (IDEA-product-owner-20260601-01 — v4.8 framing, intent fulfilled in STEP 8.1). 30 ideas re-parked at Parked-cycle-2. STEP 8.1 soft gate fired (empty Now horizon + no next-release section): PO chose Option (a) → v5.0 section added to current_roadmap.md. STEP 8.6 guardrail PASS: Challenger issued 1 type-A counter-argument (Debate 3 — SI-02 information asymmetry, PO Rebut). Meta-review triggered (3rd rebalance since last review 2026-05-25__scheduled): idea_intake_prompt.md §2.0 parked queue pre-check patch applied action-now (v2.3 → v2.4); backlog_management_prompt.md archive verification deferred (target: next groom backlog). STEP 9.0 net-zero: 0 roadmap initiative additions, 0 roadmap initiative kills.

**v5.0 scope established:** Governance hardening (BLG-GOV-79/80/81/82/83/86/87/88), product correctness (BLG-FEAT-43, BLG-BE-25), SI-05 Phase 1 (BLG-GOV-67 conditional — gate 2026-06-21), assessment (BLG-BE-26), UX pre-work (BLG-FE-60). SI-05 Phase 1 promoted to Next horizon. SI-04 noted as Next candidate.

**Run tier:** Standard (CPS 1.15; delta 0.00; scheduled run 1 day since last)

**Key backlog items added:** BLG-GOV-84 (Arc 6 gate revision assessment, gate: ≥50 trades), BLG-GOV-85 (Arc 6 §13 boundary document, gate: Arc 6 release planning trigger), BLG-FE-59 (Arc5ComplianceSection extension spec, gate: SI-02+SI-04 imminent), BLG-GOV-86 (SI-05 Telegram format spec, v5.0), BLG-GOV-87 (SI-02 re-entry trigger definition, v5.0), BLG-BE-26 (SI-02 drift summary assessment, v5.0 conditional), BLG-GOV-88 (SI-04 binding conditions decisions doc, v5.0), BLG-FE-60 (SI-05 notification channel trade-off, v5.0).

**Skill-Silo check:** 8/13 new scope items are GOV/SPEC (62%) — marginally above 60% ceiling. BLG-FEAT-43, BLG-BE-25, BLG-BE-26 (execution-heavy) provide balance. Amber status — acceptable.

**Meta-review:** DUE — 3 cycles since last meta-review (2026-05-25__scheduled). Completed this cycle. Action-now patch applied: idea_intake_prompt.md v2.3 → v2.4 (§2.0 parked queue pre-check). See meta_review.md.

**STEP 8.6 guardrail:** PASS — Condition 2 met (Challenger issued type-A counter-argument for Debate 3).

**Decision owner:** Product Owner

---

## DL-038

**Date:** 2026-06-03
**Decision type:** No-change (roadmap) + Add (to backlog × 18; terminal idea dispositions)
**Cycle:** 2026-06-03__scheduled
**Displacement:** None at roadmap level. 18 new backlog items are gate-conditional pre-work (S–M effort). 8 ideas Rejected as stale or subsumed. No roadmap initiative additions or kills.
**Workforce impact:** 18 new backlog items across QA, Backend, Frontend, OPS, SPEC, GOV categories — all gate-conditional, no immediate FTE commitment. All gates are ≥2 months out (closest: v5.1 sprint planning).

**Rationale:** Scheduled Standard-tier rebalance. Now horizon empty (v5.0 shipped 2026-06-03). All 13 active roadmap initiatives reaffirmed 🔥 Must continue. CPS = 1.15 (prior 1.15; Δ = 0.00 — no Strategy Drift Alert). Idea queue: 26 open ideas (all Parked-cycle-2, all at terminal park per §4.5 three-cycle cap). Terminal dispositions: 18 → Promoted-Backlog (new BLG items with gate criteria); 8 → Rejected (not strong — stale scope or subsumed by existing backlog). Zero ideas advanced to STEP 5 debate. STEP 8.6 guardrail PASS: 8 ideas rejected → Condition 1 met. STEP 8.1 soft gate fired (empty Now + no next-release section): PO chose Option (b) — defer, with rationale: SI-05 Phase 1 gate clears 2026-06-21 (18 days); `plan release v5.1` is the appropriate next step. STEP 9.0 net-zero: 0 roadmap initiative additions, 0 kills. Meta-review: NOT DUE (1 cycle since last meta-review 2026-06-02__scheduled; due after 2 more cycles).

**Key backlog items added:** BLG-FEAT-44 (compliance score advisory), BLG-FE-62 (pre-entry panel combined spec), BLG-FE-63 (Arc 5 visual consistency), BLG-BE-27 (SI-02 query perf baseline), BLG-BE-28 (PO-03 storage pre-design), BLG-BE-29 (SI-02 index review), BLG-BE-30 (SI-04 schema pre-design; gate cleared), BLG-BE-31 (PO-04 data prerequisites), BLG-QA-42 (SI-02 Playwright scaffold), BLG-QA-43 (compliance_summary validation), BLG-QA-44 (SI-04 test planning; gate cleared), BLG-OPS-53 (log retention expansion), BLG-SPEC-44 (SI-02 threshold calibration; gate cleared), BLG-SPEC-45 (SI-05 financial scope verification; gate cleared), BLG-SPEC-46 (Arc 4 API surface area), BLG-GOV-89 (staged verification protocol), BLG-GOV-90 (model deprecation procedure), BLG-GOV-91 (SI-04 security review; gate cleared).

**Horizon movements:** None. SI-05 Phase 1 remains Next (gate clears 2026-06-21). SI-04 remains Next candidate. All Later items confirmed no promotion.

**Run tier:** Standard (CPS 1.15; delta 0.00; scheduled run; 1 day since last scheduled rebalance)

**STEP 8.1 decision:** Option (b) — defer. Rationale: SI-05 Phase 1 gate clears in 18 days; `plan release --version v5.1 --date 2026-06-21` is the appropriate next command.

**Decision owner:** Product Owner

---

## DL-039

**Date:** 2026-06-07
**Decision type:** No-change (roadmap) + Add (to backlog × 25; idea intake IW-20260607-01 classifications)
**Cycle:** 2026-06-07__scheduled
**Displacement:** No roadmap-level additions → no roadmap-level kills required. Each backlog addition has a named deprioritisation (see item list below).
**Workforce impact:** 25 new backlog items, predominantly XS–S effort; no immediate FTE commitment. All gate-conditional or unscheduled. Skill-Silo check PASS (52% governance load, within 20–60% bounds).

**Rationale:** Scheduled Standard-tier rebalance. v5.1 shipped 2026-06-04. All 13 active roadmap initiatives reaffirmed 🔥 Must continue. CPS = 1.15 (prior 1.15; Δ = 0.00 — no Strategy Drift Alert). Ideas register was empty (post-ship archival 2026-06-04) → intake window IW-20260607-01 opened inline (44 submissions, 22 agents; Facilitator excluded per charter). STEP 4: 24 ideas advanced, 2 gate-conditional promoted to backlog, 5 rejected, 13 parked at Parked-cycle-1. STEP 5: 23 ideas Promoted-Added; 1 Promoted-Rejected (IDEA-head-of-specs-20260607-01 — duplicate of BLG-SPEC-47); 3 Challenger Type A counter-arguments; 3 PO rebuts accepted. STEP 8.1 soft gate fired (empty Now + no v5.2 section): PO chose Option (a) — v5.2 section added to current_roadmap.md with OA-01/02 pre-conditions and backlog anchors. STEP 8.6 guardrail PASS (Condition 1: 5 Rejected + 13 Parked in STEP 4; 1 Promoted-Rejected in STEP 5). STEP 9.0 net-zero: 0 roadmap additions, 0 roadmap kills.

**23 ideas Promoted-Added (new BLG items):**

| BLG ID | Title | Priority | Effort | Displacement |
|--------|-------|----------|--------|-------------|
| BLG-GOV-92 | SI-05 Phase 2 activation criteria definition | P2 | S | BLG-GOV-27 deprioritised |
| BLG-GOV-93 | OA-01/02 enforcement procedure | P1 | XS | BLG-GOV-26 deprioritised |
| BLG-GOV-94 | SI-05 Phase 1 delivery verification protocol | P2 | S | BLG-QA-21 deprioritised |
| BLG-QA-45 | Arc 5 QA completion criteria definition | P2 | S | BLG-QA-22 deprioritised |
| BLG-GOV-95 | strategy_rules.md annual parameter review schedule | P3 | S | BLG-GOV-29 deprioritised |
| BLG-OPS-55 | Deployment runbook update for SI-05 | P2 | XS | BLG-OPS-20 deprioritised |
| BLG-GOV-96 | SI-05 Phase 1 effectiveness measurement criteria | P2 | S | BLG-FEAT-44 deprioritised |
| BLG-QA-46 | SI-05 digest service edge case test gap analysis | P2 | XS | BLG-QA-23 deprioritised |
| BLG-BE-32 | SI-05 Telegram delivery retry and failure handling | P2 | S | BLG-BE-21 deprioritised |
| BLG-GOV-97 | Claude API model deprecation compliance check | P1 | XS | BLG-GOV-84 deprioritised |
| BLG-GOV-98 | Telegram bot token minimal-permission security review | P2 | S | BLG-OPS-41 deprioritised |
| BLG-GOV-99 | SI-05 digest endpoint authentication review | P2 | S | BLG-OPS-18 deprioritised |
| BLG-GOV-100 | Backend endpoint documentation coverage audit | P2 | S | BLG-OPS-19 deprioritised |
| BLG-OPS-56 | SI-05 service scheduled run health check | P2 | XS | BLG-OPS-23 deprioritised |
| BLG-BE-33 | SI-05 digest delivery log table | P2 | S | BLG-BE-14 deprioritised |
| BLG-BE-34 | Trade count gate-monitoring view | P2 | S | BLG-BE-13 deprioritised |
| BLG-GOV-101 | Governance model complexity assessment | P2 | M | BLG-QA-34 deprioritised |
| BLG-SPEC-48 | POST /digest/si05/send API contract gap check | P1 | XS | BLG-SPEC-46 deprioritised |
| BLG-QA-47 | SI-05 Phase 1 acceptance test protocol | P2 | S | BLG-QA-24 deprioritised |
| BLG-QA-48 | Regression test suite baseline refresh | P2 | XS | BLG-QA-27 deprioritised |
| BLG-QA-49 | Arc 5 test scenario completeness assessment | P2 | S | BLG-FE-39 deprioritised |
| BLG-FE-64 | BLG-FE-41 visual design review pre-brief | P2 | S | BLG-FE-27 deprioritised |
| BLG-FE-65 | User journey: SI-05 digest to app action | P3 | S | BLG-FE-55 deprioritised |

**2 ideas gate-conditional Promoted-Backlog:** BLG-GOV-102 (gate: Arc 5 fully complete; disp: BLG-GOV-85), BLG-GOV-103 (gate: BLG-GOV-89 used 2+ times; disp: BLG-GOV-90).

**Horizon movements:** v5.2 Now section added per STEP 8.1 Option (a).

**Run tier:** Standard (CPS 1.15; delta 0.00; scheduled run; 4 days since last scheduled rebalance 2026-06-03__scheduled)

**STEP 8.1 decision:** Option (a) — v5.2 section added to current_roadmap.md. Rationale: OA-01/02 due before v5.2 sprint planning seals; BLG-SPEC-47 target v5.2; BLG-GOV-97 (P1) and BLG-SPEC-48 (P1) require immediate attention anchoring v5.2 scope.

**Meta-review:** NOT DUE — 1 cycle since last meta-review (2026-06-02__scheduled). Next meta-review due after 2 more cycles.

**Decision owner:** Product Owner

---

## DL-040

**Date:** 2026-06-08
**Cycle:** 2026-06-08__scheduled
**Type:** Add (backlog)
**Run tier:** Standard (CPS 1.15; delta 0.00; scheduled; 1 day since last scheduled rebalance 2026-06-07__scheduled)

**Roadmap initiative changes:** None. All 13 active initiatives confirmed 🔥 Must continue. No Add / Replace / Defer / Kill for roadmap initiatives.

**22 ideas Promoted (19 Promoted-Added + 3 Promoted-Backlog):**

| BLG ID | Title | Priority | Effort | Displacement |
|--------|-------|----------|--------|-------------|
| BLG-SPEC-53 | BLG-SPEC-49–52 contract gap resolution plan | P1 | M | BLG-GOV-101 deprioritised |
| BLG-QA-51 | BLG-SPEC-49–52 QA acceptance readiness | P2 | S | BLG-QA-44 deprioritised |
| BLG-GOV-104 | strategy_rules.md §11 parameter validation (first instance) | P2 | M | BLG-GOV-101 deprioritised |
| BLG-GOV-105 | Arc 6 PS-03 Monte Carlo §13 threshold pre-assessment | P2 | S | BLG-GOV-111 deprioritised (lower-P) |
| BLG-OPS-57 | SI-05 Telegram delivery failure alerting | P1 | S | BLG-OPS-13 deprioritised |
| BLG-GOV-106 | PT-04 trade count gate re-verification | P1 | S | BLG-GOV-101 deprioritised |
| BLG-GOV-107 | SI-02 frontend activation criteria precision | P2 | S | BLG-GOV-101 deprioritised |
| BLG-GOV-108 | AI model pin update policy (BLG-GOV-64 gap) | P2 | S | BLG-GOV-101 deprioritised |
| BLG-GOV-109 | AI audit log retention policy | P2 | S | BLG-OPS-13 deprioritised |
| BLG-OPS-58 | CI secret scanning gate | P1 | S | BLG-OPS-13 deprioritised |
| BLG-OPS-59 | SI-05 service production p99 latency review | P2 | S | BLG-OPS-13 deprioritised |
| BLG-FE-66 | Red Flag Journal post-launch UX review | P3 | S | BLG-FE-55 deprioritised |
| BLG-GOV-110 | Arc 4 trade_plan data completeness audit | P2 | S | BLG-GOV-101 deprioritised |
| BLG-QA-52 | Tax year P&L boundary edge case validation | P2 | S | BLG-QA-44 deprioritised |
| BLG-SPEC-54 | openapi.yaml completeness audit (all 50 routes) | P1 | S | BLG-SPEC-46 deprioritised |
| BLG-QA-53 | SI-05 digest Playwright E2E coverage | P2 | M | BLG-QA-44 deprioritised |
| BLG-QA-54 | Playwright coverage matrix update post-v5.2 | P2 | S | BLG-QA-44 deprioritised |
| BLG-FE-67 | BLG-FE-64 design review scope definition | P2 | S | BLG-GOV-101 deprioritised |
| BLG-GOV-111 | v5.3 design gate pre-assessment | P2 | S | BLG-GOV-101 deprioritised |

**3 ideas gate-conditional Promoted-Backlog:**
- BLG-GOV-112 (gate: 2026-07-04 SI-05 effectiveness review complete; disp: BLG-GOV-85 deprioritised)
- BLG-GOV-113 (gate: before 2026-07-04 effectiveness review; disp: BLG-QA-34 deprioritised)
- BLG-GOV-114 (gate: before 2026-07-04 effectiveness review; disp: BLG-GOV-90 deprioritised)

**1 idea Parked post-debate:** IDEA-metrics-analytics-20260608-01 (Arc 6 data audit) — Challenger Type-A accepted by PO; Arc 6 24+ months away.

**Horizon movements:** v5.3 Now section added to current_roadmap.md per STEP 8.1 Option (a). Rationale: 22 new backlog items from this rebalance plus BLG-SPEC-49–52 and BLG-BE-35 from v5.2 provide clear v5.3 scope; advancing to plan release v5.3.

**STEP 8.1 decision:** Option (a) — v5.3 section added to current_roadmap.md Now horizon. Section: v5.3 — Spec Debt, Security Hardening & Ops Governance.

**Meta-review:** NOT DUE — 2 cycles since last meta-review (2026-06-02__scheduled). Next meta-review due after 1 more cycle.

**Decision owner:** Product Owner

---

## DL-043

**Date:** 2026-06-10
**Cycle:** 2026-06-10__scheduled
**Decision type:** Terminal disposition — Parked-cycle-2 ideas (IW-20260608-01)
**Initiatives affected:** None (backlog-level items only)
**Displacement:** N/A (1 Promoted-Backlog; gate-conditional; not in active sprint)
**Workforce impact:** None
**Rationale:** 17 IW-20260608-01 ideas reached Parked-cycle-2 terminal status per §4.5 hard cap. 16 Rejected (not strong or superseded — no novel evidence, gate rationales exhausted, or source scope shipped). 1 Promoted-Backlog: IDEA-frontend-ux-20260608-02 → BLG-FE-72 (Arc 4 PO-02 journal pattern UX spec, gate-conditional on PO-02 imminent). No Rejected-Strong entries — none met the threshold.
**Decision owner:** Product Owner

---

## DL-044

**Date:** 2026-06-10
**Cycle:** 2026-06-10__scheduled
**Decision type:** Backlog additions (from LL carry-forwards + idea intake IW-20260610-01)
**Initiatives affected:** None (backlog items only — no roadmap initiative changes)
**Displacement:** N/A (governance patches, gate-conditional; no active sprint commitments)
**Workforce impact:** None (all items autonomous/documentation class; no new FTE)
**Rationale:** 9 new backlog items added this cycle. 3 from v5.4 LL carry-forwards (BLG-GOV-116/117/118 — governance patches for sprint_planning_prompt.md and execution_prompt.md targeting LL-P3-01/02/03). 4 gate-conditional from IW-20260610-01 (BLG-GOV-119 Arc 5 retrospective, BLG-GOV-121 Phase 2 §13 pre-clearance, BLG-FE-72 PO-02 UX spec, and BLG-GOV-122 §11 annual review). 2 ready/near-term items (BLG-GOV-120 trade data density tracker, BLG-OPS-61 endpoint baseline extension). IW-20260610-01: 44 submissions; 9 Promoted-Backlog; 35 Parked-cycle-1 with specific rationale.
**Decision owner:** Product Owner

---

## DL-045

**Date:** 2026-06-10
**Cycle:** 2026-06-10__scheduled
**Decision type:** Roadmap Now horizon — Add v5.5 Now section (STEP 8.1 Option a)
**Initiatives affected:** v5.5 release planning enabled
**Displacement:** N/A (scheduled rebalance; no active initiative killed)
**Workforce impact:** None — v5.5 scope is governance/ops/UX documents and patches; no new FTE commitment
**Rationale:** Now horizon empty post-v5.4; ~37 active backlog items; time-sensitive SI-05 effectiveness review cluster (BLG-OPS-59/GOV-112/113/114/115 gate 2026-07-04) requires sprint window post-July-4; LL-P3-01/02/03 carry-forwards ready as governance patches (BLG-GOV-116/117/118); BLG-FE-64 gate clears 2026-06-21; UX/FE debt queue (BLG-FE-61/62/65/66) and BLG-BE-16/BLG-GOV-120/BLG-OPS-61 available. STEP 8.1 Option (a) selected. Section: v5.5 — SI-05 Effectiveness Review, Governance Hardening & UX Debt Clearance.
**Decision owner:** Product Owner

---

## DL-041

**Date:** 2026-06-09
**Cycle:** 2026-06-09__scheduled
**Decision type:** Backlog additions (Promoted-Backlog from Parked-cycle-2 ideas)
**Initiatives affected:** None (backlog items only — no roadmap initiative changes)
**Displacement:** N/A (gate-conditional backlog items; no active sprint commitments)
**Workforce impact:** None (gate-conditional items, not yet in sprint)
**Rationale:** 12 IW-20260607-01 parked-cycle-2 ideas reached cycle-3 terminal: 4 Rejected (insufficient evidence of value; trigger conditions not met), 8 Promoted-Backlog (all gate-conditional — gates: BLG-FE-45, Phase 2 channel decision, 2026-07-04 effectiveness review, ≥20 closed trades, ≥2026-08-05, PO-02 imminent). New backlog items: BLG-GOV-115, BLG-FE-68/69/70/71, BLG-FEAT-45, BLG-SPEC-55, BLG-QA-55.
**Decision owner:** Product Owner

---

## DL-042

**Date:** 2026-06-09
**Cycle:** 2026-06-09__scheduled
**Decision type:** Roadmap Now horizon — Add v5.4 Now section (STEP 8.1 Option a)
**Initiatives affected:** v5.4 release planning enabled
**Displacement:** N/A (scheduled rebalance; no active initiative killed)
**Workforce impact:** None — v5.4 scope is governance/ops/UX documents and patches; no new FTE commitment
**Rationale:** Now horizon empty post-v5.3; ~40 active backlog items provide clear v5.4 scope; time-sensitive items (BLG-OPS-59, BLG-GOV-112/115) require action before 2026-07-04 SI-05 effectiveness review; deferred DP-2 governance patch should enter v5.4; pre-entry panel and RFJ UX debt items (BLG-FE-47/49/56/64) are queued. STEP 8.1 Option (a) selected. Section: v5.4 — Ops Monitoring, UX Debt Clearance & Governance Patches.
**Decision owner:** Product Owner

---

## DL-046

**Date:** 2026-06-16
**Cycle:** 2026-06-16__scheduled
**Decision type:** Backlog addition (Promoted-Backlog from advancing idea) + Roadmap Now horizon (STEP 8.1 Option a)
**Initiatives affected:** v5.6 release planning enabled; no roadmap initiative changes
**Displacement:** BLG-OPS-18 (data pipeline cost baseline, P3, gate-conditional on BLG-OPS-17) deprioritised in favour of BLG-OPS-63
**Workforce impact:** None — all items are governance/ops/UX documents; no new FTE commitment
**Rationale:** Scheduled rebalance — Extended tier (CPS 2.85; arc pipeline artefact acknowledged by Strategy Rules & System Intent Owner). 35 Parked-cycle-1 ideas evaluated: 1 advanced (IDEA-finops-20260610-01 → BLG-OPS-65: Anthropic API cost 14-cycle trend analysis — gate cleared via BLG-GOV-74 COMPLETE v4.4); 5 Rejected (BLG-QA-50/48/54/SPEC-54 delivered; advocacy purposes fulfilled); 29 re-parked (Parked-cycle-2) with updated specific rationales — all valid per §4.1 Facilitator gate. No roadmap initiative changes — all 13 active initiatives remain 🔥 Must continue (all gated by data density or date). STEP 8.1 Option (a): Now horizon empty post-v5.5; ~37 active backlog items; BLG-OPS-22 gate cleared; BLG-FE-73/74 outstanding; BLG-FE-64 gate imminent (2026-06-21); LL-RP-02 action-now patch actionable. v5.6 section added. Meta-review NOT DUE — 1 cycle since last meta-review (2026-06-09__scheduled).
**Decision owner:** Product Owner


## DL-047

**Date:** 2026-06-17
**Decision type:** No-change (roadmap initiatives) + Backlog add (BLG-GOV-130) + Roadmap Now section added (STEP 8.1 Option a)
**Cycle:** 2026-06-17__scheduled
**Initiatives affected:** No active roadmap initiatives — v5.9 Now section added
**Displacement:** None (BLG-GOV-130 is a gate-conditional backlog add; no initiative displacement required)
**Workforce impact:** None — no new FTE commitment
**Rationale:** Scheduled rebalance — Standard tier (CPS = N/A; zero active initiatives in register; scheduled same-day as prior cycle; > 90 days threshold not met). 29 IW-20260610-01 ideas evaluated at terminal cycle 3: 1 promoted-backlog (IDEA-product-owner-20260610-02 → BLG-GOV-130: SI-05 Phase 2 activation decision scope, gate 2026-07-04); 28 rejected — all duplicates of tracked BLG items or low-value at terminal cycle; none classified Rejected-Strong. No roadmap initiative changes. STEP 8.1 Option (a): v5.9 Now section added with BLG-FE-64/41 (gate 2026-06-21 — 4 days), BLG-OPS-70, BLG-GOV-125–129 as firm scope; BLG-GOV-112/113/115/130/BLG-OPS-59 as conditional (gate 2026-07-04; within v5.9 sprint window per STEP 1.4b mandatory rule). Action-now patch applied: release_planning_prompt.md v2.35→v2.36 (STEP 1.4b Within-Sprint Date Gate Classification mandatory — LL-P3-03-v55/LL-P4-01-v55 overdue resolved). Meta-review DUE (3rd cycle since 2026-06-09__scheduled) — see lessons_learnt.md.
**Decision owner:** Product Owner
