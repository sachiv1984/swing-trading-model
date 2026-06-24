**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.2
**Cycle:** 2026-06-24__release-v6.2
**Last Updated:** 2026-06-24

---

# Release Plan — v6.2 Production Strategy Parity & AI Intelligence

---

## Readiness

**Roadmap authority:** §1 header `**Next planned release:** v6.2`; Now horizon v[TBD] confirmed by rebalance 2026-06-24__scheduled (STEP 8.2 PASS). Six Now-horizon items (BLG-FEAT-46–51) constitute the v6.2 feature scope. Four governance/QA debt items (BLG-GOV-135/136, BLG-OPS-75, BLG-QA-62) are explicitly targeted at v6.2.

**Context:** v6.1 closed all of Arc 2 (PT-04 Setup Quality Score shipped). v6.2 opens the next value arc: closing the gap between the live system and `production_strategy.py` backtest logic (the P1 cluster) and layering AI decision support on top (the P2 cluster). Product Value Alert from rebalance (ratio=0.209) reinforces the priority of product feature delivery over governance overhead in this cycle.

**Advisories from STEP 1:**
- ⚠ Advisory (§1.2): 6 items carry `Provisional-Target: [TBD]` — will be updated to v6.2 post-publish.
- ⚠ Advisory (§1.3): Design dependencies on BLG-FEAT-46/47/49/50/51 (observable UI). Design Gate required.
- ℹ No perennial-return items; no within-sprint date gates (§1.4a/b).
- ℹ Arc 4 data density: ~15 closed trades; SI-02 gate ~2–3 months out; PO-02/PO-04 data not available.

---

## Scope

| S2-ID | Backlog Item | Description | Priority | Effort | Type |
|-------|-------------|-------------|----------|--------|------|
| S2-01 | BLG-FEAT-46 | Nightly trailing stop computation for open positions | P1 | M | Feature |
| S2-02 | BLG-FEAT-47 | Month-end rebalance exit signal generation | P1 | M | Feature |
| S2-03 | BLG-FEAT-48 | Inverse-volatility position sizing for signal-driven entries | P1 | M | Feature |
| S2-04 | BLG-FEAT-49 | Risk-off exit alerts for existing positions | P1 | S | Feature |
| S2-05 | BLG-FEAT-50 | AI daily briefing endpoint and dashboard panel | P2 | M | Feature |
| S2-06 | BLG-FEAT-51 | Conversational AI trade advisor | P2 | M | Feature |
| S2-07 | BLG-GOV-135 | execution_prompt autonomous class hard gate | P2 | XS | Governance |
| S2-08 | BLG-GOV-136 | execution_prompt test_scenarios path validation | P3 | XS | Governance |
| S2-09 | BLG-OPS-75 | api_performance_baseline.md — 2 new v6.1 endpoints | P3 | XS | Operations |
| S2-10 | BLG-QA-62 | Playwright spec auto-registration via glob pattern | P2 | S | QA |

**Items explicitly deferred:** BLG-FEAT-52 (Trade tagging — gate-conditional; Arc 4 PO-02 not imminent). BLG-QA-63 (a11y testing — gate-conditional: Arc 5 not yet complete). BLG-OPS-76/77 (gate-conditional: BLG-OPS-25/71 not complete). SI-02 frontend (gate: <20 closed trades — not met). All other backlog items below P2 or gate-blocked.

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02, S2-03, S2-04 | Head of Engineering | RISK-03 | Sprint 1 first — EPIC-02 depends on EPIC-01 delivery |
| EPIC-02 | S2-05, S2-06 | Head of Engineering | RISK-01 | After EPIC-01; §13 review required before sprint planning seal |
| EPIC-03 | S2-07, S2-08, S2-09, S2-10 | Head of Specs Team / Director of Quality | RISK-02 | Independent — run Sprint 1 alongside EPIC-01 |

**EPIC-01 note:** P1 prerequisite cluster. All four items form a coherent parity layer — trailing stop ratchet (S2-01), rebalance exit signals (S2-02), inv-vol sizing (S2-03), and risk-off exit alerts (S2-04). S2-03 (inv-vol sizing) replaces the core sizing path for signal-driven entries — highest regression risk in the cluster.

**EPIC-02 note:** P2 AI intelligence layer. S2-05 (daily briefing) depends on S2-01/02/04 data being live. S2-06 (chat advisor) depends on S2-05 context assembly pattern. EPIC-02 is conditional in Sprint 1 — may form Sprint 2 if EPIC-01 fill capacity.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-02 | §13 compliance not yet formally reviewed for BLG-FEAT-50/51 (AI advisory endpoints). Must confirm advisory-only, no automated execution. | High | Strategy Rules & System Intent Owner §13 review required before sprint planning seal | null |
| RISK-02 | Release-level | Capacity risk — 10.5–12.5 days estimated across 3 EPICs; solo dev evenings. 2-sprint plan mitigates but EPIC-02 conditional status carries uncertainty. | Medium | Phase to Sprint 1 (EPIC-01 + EPIC-03) + Sprint 2 (EPIC-02); EPIC-02 conditional at sprint planning | null |
| RISK-03 | EPIC-01 | BLG-FEAT-48 (inv-vol sizing) replaces core sizing path for signal-driven entries. Regression risk for live signal allocations if test coverage is insufficient. | High | Existing sizing unit tests must pass; regression test suite must confirm manual sizing path unchanged | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**S2 → EPIC mapping check:**
- S2-01, S2-02, S2-03, S2-04 → EPIC-01 ✅
- S2-05, S2-06 → EPIC-02 ✅
- S2-07, S2-08, S2-09, S2-10 → EPIC-03 ✅

**RISK → EPIC mapping check:**
- RISK-01 → EPIC-02 ✅
- RISK-02 → Release-level ✅
- RISK-03 → EPIC-01 ✅

**Dependency chain integrity:** EPIC-01 → EPIC-02 dependency explicit in execution plan; no circular dependencies. EPIC-03 independent.

**Model integrity: PASS**

---

## Capacity Check

**Effort estimates (inline — no scored_initiatives.md match):**

| EPIC | Stories | Effort (days) | Notes |
|------|---------|--------------|-------|
| EPIC-01 | ST-01 to ST-05 | 7 | S2-01 backend (2d) + S2-01 frontend (1d) + S2-02 (1.5d) + S2-03 (2d) + S2-04 (0.5d) |
| EPIC-02 | ST-06 to ST-09 | 4 | S2-05 backend (2d) + S2-05 frontend (0.5d) + S2-06 backend (1d) + S2-06 frontend (0.5d) |
| EPIC-03 | ST-10 to ST-13 | 1.5 | BLG-GOV-135 (0.25d) + BLG-GOV-136 (0.25d) + BLG-OPS-75 (0.25d) + BLG-QA-62 (0.75d) |
| **Total** | **13** | **12.5** | — |

**Capacity assumption:** ~10–15 hrs/week solo dev (consistent with v6.1); 2 weeks per sprint = ~20–30 hrs/sprint.

**Assessment:** 12.5 total days (~100 hrs) against ~20–30 hrs/sprint available capacity = approximately 3–5 sprints at low end or 2 at high end. However, many stories are well-scoped and the governance items (EPIC-03) are trivially small. Likely achievable in 2 sprints with EPIC-02 as Sprint 2.

**Outcome: WARN** — Total estimated effort exceeds single-sprint capacity; 2-sprint plan required.

### Phasing Recommendation

| Phase | EPICs | Estimated effort | Rationale |
|-------|-------|-----------------|-----------|
| Sprint 1 | EPIC-01 + EPIC-03 | ~8.5 days | P1 strategy parity cluster + low-effort governance debt; independent EPICs can run in parallel |
| Sprint 2 | EPIC-02 | ~4 days | AI intelligence layer; depends on EPIC-01 live data; §13 review must complete at Sprint 1 close |

**Ordering rationale:** EPIC-01 is the prerequisite for EPIC-02 (trailing stop, rebalance exit, and risk-off data must be live for daily briefing to synthesise). EPIC-03 has no dependencies and its XS items minimise overhead drag. EPIC-02 can enter Sprint 2 once EPIC-01 is verified.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**5.5 Cross-Stage Integrity:**
- All S2 IDs (S2-01 through S2-10) map to EPICs in stage3 ✅
- All EPIC IDs in stage4_backlog_slice.md (EPIC-01, EPIC-02, EPIC-03) match stage3 ✅
- All RISK IDs in EPIC table (RISK-01, RISK-02, RISK-03) appear in Risk Register ✅
- No orphaned S2/EPIC/RISK references ✅

**5.7 Decision Record Integrity:** No escalations raised (`artifacts.escalations = none`) — 5.7 not applicable.

**Cross-stage integrity: PASS**
