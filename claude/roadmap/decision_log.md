**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-06

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
