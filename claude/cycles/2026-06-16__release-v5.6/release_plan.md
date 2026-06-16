**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-16__release-v5.6
**Published:** 2026-06-16

---

# Release Plan — v5.6

**Theme:** Research Performance, SI-05 UX Improvements & Backlog Clearance

---

## Readiness

### 1.1 Backlog Age Advisory

No spec/documentation debt items in this release slice have aged 2+ cycles without a story assignment. BLG-FE-64 has been deferred twice (v5.4, v5.5) due to a date gate (2026-06-21) not being met — now classified as conditional, gate clears in 5 days. All other items are first-cycle picks.

Design dependency scan: 0 items flagged.

### 1.2 Provisional-Target Advisory

- Items with `Provisional-Target: v5.6`: BLG-OPS-22, BLG-OPS-62, BLG-FE-73, BLG-FE-74, BLG-FE-64
- Items with Provisional-Target: Unscheduled / prior version: BLG-OPS-63, BLG-OPS-64, BLG-OPS-65, BLG-QA-45, BLG-QA-49, BLG-GOV-106

ℹ 5 items carry `Provisional-Target: v5.6`. 6 items have no matching Provisional-Target for this release (promoted by scope pull-forward per "clear as much backlog as possible" directive).

### 1.3 Design-Gate Language Scan

Design dependency scan: 0 items flagged.

### 1.4 Gate-Condition Proximity Scan

| Item | Gate condition | Current trajectory | Projected clear date |
|------|---------------|-------------------|---------------------|
| BLG-FE-64 | SI-03 Red Flag Journal live ≥30 days (2026-06-21) | Gate clears in 5 days | 2026-06-21 ✅ |
| PT-04 (BLG-GOV-106 prerequisite) | ≥20 closed trades with plans | ~6 trades as of v5.3; rate unknown | trajectory unknown |
| SI-02 frontend | ≥20 closed trades (condition 1 of 3) | ~6 trades, slow accumulation | trajectory unknown |
| PO-02 | 6+ months AI journal entries | AI journals since v2.8 (2026-04-20) | ~2026-10-20 |
| PO-04 | 50+ trades with plans | ~6 closed trades, trajectory slow | trajectory unknown |

Arc 4 data density sub-check:
- Closed trade count: ~6 (per v5.3 verification at 2026-06-09; no new query available without production access). Monthly rate: low (1–2/month estimated).
- PO-02 (6+ months AI journals): AI journals active since v2.8 (2026-04-20) → projected 2026-10-20.
- PO-04 (50+ trades with plans): gate not met; trajectory unknown — Product Owner to surface at readiness review.
- SI-02 (20+ trades with plans): gate NOT MET; same trajectory as PO-04.

---

## Scope

| ID | Item | Source | Priority | Effort | Type |
|----|------|--------|----------|--------|------|
| S2-01 | BLG-FE-73 — Add deep links from SI-05 digest to relevant app screens | ST-10 v5.5 user journey | P2 | S | Frontend / UX |
| S2-02 | BLG-FE-74 — Clarify N/A pass rate reason in SI-05 digest message | ST-10 v5.5 user journey | P3 | XS | Backend / UX |
| S2-03 | BLG-OPS-22 — Research data caching layer | Rebalance DL-032; gate cleared 2026-06-11 | P2 | M | Performance |
| S2-04 | BLG-OPS-62 — Investigate GET /portfolio/concentration-status high latency | v5.5 ST-06 BLG-OPS-13 | P3 | S | Performance |
| S2-05 | BLG-OPS-63 — Investigate GET /portfolio/red-flag-journal high latency | v5.5 ST-06 BLG-OPS-13 | P3 | S | Performance |
| S2-06 | BLG-OPS-64 — Investigate GET /analytics/behavioural-drift high latency | v5.5 ST-06 BLG-OPS-13 | P3 | S | Performance |
| S2-07 | BLG-GOV-106 — PT-04 trade count gate re-verification | Rebalance DL-040 | P1 | S | Governance |
| S2-08 | BLG-QA-45 — Arc 5 QA completion criteria definition | Rebalance DL-039 | P2 | S | QA |
| S2-09 | BLG-QA-49 — Arc 5 test scenario completeness assessment | Rebalance DL-039 | P2 | S-M | QA |
| S2-10 | BLG-OPS-65 — Anthropic API cost 14-cycle trend analysis | Rebalance DL-046 | P3 | S | Cost governance |
| S2-11 [conditional] | BLG-FE-64 — RFJ visual design review pre-brief | Rebalance DL-039; gate 2026-06-21 | P2 | S | Frontend / UX pre-work |

**10 firm scope items. 1 conditional (S2-11: gate 2026-06-21 must clear before sprint planning assigns it).**

Items explicitly deferred: LL-P3-03-v55 / LL-P4-01-v55 governance patches not treated as separate stories — guidance applied at this planning by classifying BLG-FE-64 as conditional per the lesson.

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02, S2-11 | Head of Backend Engineering; Head of UX & Design | RISK-01 | After gate check for S2-11; S2-01/02 no dependencies |
| EPIC-02 | S2-03, S2-04, S2-05, S2-06 | Infrastructure & Operations Owner; Head of Backend Engineering | RISK-02 | S2-03 may depend on S2-05/S2-06 results if same caching layer; run investigations (S2-04/05/06) before implementing cache (S2-03) |
| EPIC-03 | S2-07, S2-08, S2-09, S2-10 | PMO Lead; Director of Quality; FinOps & Resource Architect | RISK-03 | S2-07 (PT-04 gate check) should run first — if gate clears it affects Arc 2 horizon |

**EPIC-02 note:** S2-04 (concentration-status latency), S2-05 (red-flag-journal latency), S2-06 (behavioural-drift latency) are short investigations each producing an index/cache fix. S2-03 (research data caching) is the larger M-effort item. Merge order: EPIC-03 → EPIC-01 → EPIC-02 (largest last to avoid holding a merge waiting on the investigation results).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | BLG-FE-64 gate date (2026-06-21) may not clear before sprint planning seals | Low | Classified as conditional; sprint planning picks it up only if gate clears | null |
| RISK-02 | EPIC-02 | BLG-OPS-22 caching layer may require Redis infrastructure not yet available | Medium | Prompt accepts in-memory TTL cache as fallback; no Redis dependency required per AC | null |
| RISK-03 | EPIC-03 | PT-04 gate re-verification may confirm gate still not met (< 20 trades) | Low | Result is advisory; either outcome (met/not met) closes BLG-GOV-106; no sprint blocker | null |

---

## Capacity Check

| EPIC | Items | Estimated effort | Effort source |
|------|-------|-----------------|---------------|
| EPIC-01 | S2-01 (S), S2-02 (XS), S2-11 conditional (S) | ~1.5 days firm + 0.5 conditional | inline estimate |
| EPIC-02 | S2-03 (M), S2-04 (S), S2-05 (S), S2-06 (S) | ~4 days | inline estimate (S2-03 from scored_initiatives N/A — no row; inline M=2–3d) |
| EPIC-03 | S2-07 (S), S2-08 (S), S2-09 (S-M), S2-10 (S) | ~3–4 days | S2-07 from scored_initiatives S; others inline |

**Total estimated: ~9–10 days firm + 0.5 conditional.**

Rolling 6-cycle velocity: 0.91 (v5.0–v5.5). Expected completion: ~10 of 11 firm stories based on velocity.

**Capacity feasibility: WARN** — total effort approaches a 2-sprint capacity boundary. Phasing recommended.

### Phasing Recommendation

- **Sprint 1:** EPIC-01 + EPIC-03 — estimated 4.5–5.5 days. Lower risk, governance P1 item (S2-07), QA docs, SI-05 UX fixes.
- **Sprint 2 (if needed):** EPIC-02 — estimated 4 days. Performance investigations and caching implementation. These are P2/P3 and stand alone.

Ordering rationale: EPIC-03 contains the P1 item (BLG-GOV-106); EPIC-01 contains the conditional (BLG-FE-64 gate 2026-06-21). EPIC-02 performance work is valuable but deferred to Sprint 2 if capacity is tight.

Applying LL-P3-03-v55 lesson: if Sprint 2 stories cannot execute due to capacity or other constraints, this is expected — EPIC-02 items are valuable-but-not-blocking P2/P3 work.

---

## Integrity Validation — 3.5 Local Model Integrity

All S2 IDs map to distinct backlog items. No duplicates. All EPIC IDs assigned (EPIC-01 through EPIC-03). All RISK IDs in EPIC table appear in Risk Register Summary. No circular dependencies. BLG-FE-64 correctly marked conditional on S2-11 (gate 2026-06-21).

**Stage 3.5: PASS**

---

## Integrity Validation — 5.5 Cross-Stage Integrity

- All S2 IDs (S2-01 through S2-11) present in Scope table and referenced in EPIC table
- EPIC-01: maps to S2-01, S2-02, S2-11 ✅
- EPIC-02: maps to S2-03, S2-04, S2-05, S2-06 ✅
- EPIC-03: maps to S2-07, S2-08, S2-09, S2-10 ✅
- All RISK-IDs (RISK-01 through RISK-03) appear in Risk Register ✅
- stage4_backlog_slice EPIC IDs match stage3 ✅
- No orphaned references ✅

**Stage 5.5: PASS**

**5.7 Decision Record Integrity:** decisions--2026-06-16__release-v5.6.md present; all fields populated; no AR/SRB records raised. **PASS**
