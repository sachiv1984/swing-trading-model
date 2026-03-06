# Stage 4.5 — Capacity Feasibility Sense Check

**Owner:** FinOps & Resource Architect
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9
**Last Updated:** 2026-03-06

---

## 1. Assumptions (No timebox or capacity flags provided at invocation)

As no `--timebox` or `--capacity` arguments were supplied, the following standard assumptions apply for this solo-dev, evenings-and-weekends project (consistent with v1.8 planning):

| Assumption | Value | Source |
|-----------|-------|--------|
| Developer type | Solo developer | Prior cycle pattern |
| Working pace | Evenings + weekends | Prior cycle pattern |
| Available hours/week | ~10–15 hours | Prior cycle pattern |
| Weeks available | 1–2 weeks | Consistent with prior release cadence |
| Total estimated capacity | ~15–25 hours | Conservative estimate |

**Assumption frozen at:** No timebox or capacity provided — standard assumptions applied.

---

## 2. Story Item Effort Estimates

| ST-ID | EPIC | Title | Estimated Effort | Notes |
|-------|------|-------|-----------------|-------|
| ST-01 | EPIC-01 | Compliance Metrics Definitions | ~1 day (6–8 hrs) | Metrics Definitions owner work; spec + backend + frontend |
| ST-02 | EPIC-01 | Trade Reflection Template | 1–2 days (8–12 hrs) | New spec + backend storage + frontend form |
| ST-03 | EPIC-02 | Cohort Analysis | 1–2 days (8–12 hrs) | Backend query + frontend chart |
| ST-04 | EPIC-02 | R-Multiple Distribution | 1–2 days (6–10 hrs) | Backend compute + frontend chart |
| ST-05 | EPIC-03 | Dashboard Homepage | 1–2 days (6–10 hrs) | New spec + frontend; composite endpoint optional |
| ST-06 | EPIC-04 | Drawdown Spec Alignment | <0.5 day (1–3 hrs) | Documentation only |
| ST-07 | EPIC-04 | Backend: US Currency Conversion | 0.5–1 day (3–6 hrs) | Backend service; straightforward FX pattern |
| ST-08 | EPIC-04 | Frontend: Error States | 0.5 day (2–4 hrs) | Frontend only; may need Base44 config check |
| ST-09 | EPIC-04 | Frontend: Table/Column Fixes | 0.5 day (2–4 hrs) | 4 items; small frontend changes |
| ST-10 | EPIC-04 | Frontend: HeatGauge + Cosmetic | 0.5 day (1–3 hrs) | 2 small cosmetic fixes |
| ST-11 | EPIC-05 | Test Infra Phase 1 (Risk Dashboard) | 1–2 days (6–10 hrs) | Infrastructure setup + 17 scenarios |
| ST-12 | EPIC-05 | Test Scenarios Phase 2 (Features) | 1 day (4–8 hrs) | Distributed across sprint |
| ST-13 | EPIC-05 | Service Coverage Standard + CI | 0.5–1 day (3–6 hrs) | Standard authoring + CI step |
| ST-14 | EPIC-06 | Terms Glossary | 0.5 day (2–4 hrs) | Documentation only |
| ST-15 | EPIC-06 | AI Governance Policy | 0.5 day (2–4 hrs) | Documentation only |
| ST-16 | EPIC-06 | Document GET /market/status | 0.5 day (2–4 hrs) | API contract + openapi.yaml update |
| ST-17 | EPIC-06 | settings_model.md | 0.5 day (2–4 hrs) | Data model doc |
| ST-18 | EPIC-06 | Error Response Standard | 0.5 day (2–4 hrs) | Spec + cross-reference updates |
| ST-19 | EPIC-06 | Spec/Doc Debt Small Fixes (7 items) | 0.5 day (2–4 hrs) | ~30 min each; batched |

**Total estimated effort:**

- Low estimate: ~64 hours
- High estimate: ~115 hours
- Mid-point: ~90 hours

---

## 3. Capacity vs Scope Assessment

| Item | Assessment |
|------|-----------|
| Total effort (mid): ~90 hours | Significant — approximately 6–9 weeks at 10–15 hrs/week |
| v1.9 is a consolidation release | Scope includes 11 backlog defect fixes + 4 new features + QA infra + doc hygiene |
| v1.8 was also a heavy release | Prior cycle delivered 12 story items including 4 EPICs |

### FinOps & Resource Architect Assessment

**Verdict: ⚠️ WARN — scope is ambitious for a solo developer at evenings-and-weekends pace.**

**Basis:**
- ~90 hours of estimated work at 10–15 hrs/week = 6–9 weeks
- This is longer than prior release cadences (v1.8: ~2 weeks)
- The scope is genuinely large: 6 EPICs, 19 story items, 30 S2 scope items

**Mitigations available (without changing governance decisions):**
1. **EPIC-04 is highest ROI:** 11 Risk Dashboard defects are well-defined, small individually, and high user impact. Completing EPIC-04 early delivers visible value fast.
2. **EPIC-06 documentation items are parallelisable** with feature EPICs — do not need sequential capacity.
3. **ST-12 (Phase 2 test scenarios)** is distributed naturally across the sprint; no fixed capacity block.
4. **EPIC-05 Phase 1 (ST-11) can be scoped down** if implementation approach (seeded DB vs mock layer) is chosen for simplicity over completeness.
5. **Sprint planning may prioritise a P1/P2 subset** if capacity is confirmed lower than assumed.

**LL-05 Capacity Check (RISK-01 — Metrics Definitions owner):**
The Metrics Definitions & Analytics Owner must be confirmed available before ST-01 enters sprint. In a solo-dev project, this role is held by the same person — so availability is self-confirming. FinOps notes: the concern in LL-05 was about competing commitments (EPIC-03 v1.7). Since v1.7 is closed and v1.8 is closed, no active competing commitment exists. **LL-05 check: PASS** — Metrics Definitions owner available for v1.9.

**Advisory recommendations:**
- Product Owner to confirm at sprint planning whether all 6 EPICs are targeted in a single sprint, or whether a phased approach (EPIC-04 + EPIC-05 Phase 1 sprint 1; remainder sprint 2) is preferred.
- If phased, split cycle at sprint planning; governance supports multi-sprint within a release planning cycle.
- No items need to be de-scoped at this stage — scope is valid; pace is the variable.

**Outcome: WARN (standard mode — advisory; not a blocker)**

In standard mode, a WARN on capacity is noted and does not block the publish gate. Product Owner is informed and may adjust at sprint planning.

---

## 4. Risk Register (Capacity-related)

| Risk | Impact | Mitigation |
|------|--------|-----------|
| RISK-01 (Metrics Defs owner capacity) | Resolved — LL-05 check passes | Self-confirming in solo-dev context; prior cycle closed |
| Scope volume (~90 hrs for solo dev) | Sprint may extend beyond 2 weeks | Product Owner may phase sprint; no governance action required |

---

## 5. Summary

| Check | Result |
|-------|--------|
| LL-05 capacity check (RISK-01) | ✅ PASS — no competing commitment |
| Effort estimates complete | ✅ |
| Capacity vs scope assessment | ⚠️ WARN — scope ambitious; advisories noted |
| No workforce escalation opened | ✅ (standard mode; warn advisory does not create escalation) |

**Stage 4.5 Outcome: WARN** (standard mode — allowed at publish gate)
