**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Last Updated:** 2026-06-16
**Cycle:** 2026-06-10__release-v5.5

Superseded by: v5.5 ship — 2026-06-16
Changelog: docs/product/changelog.md#v55
Verification report: claude/cycles/2026-06-10__release-v5.5/verification_report.md
Cycle: 2026-06-10__release-v5.5

---

# Scope Document — v5.5
## SI-05 Effectiveness Review, Governance Hardening & UX Debt Clearance

**Release:** v5.5
**Cycle:** 2026-06-10__release-v5.5
**Last Updated:** 2026-06-10

---

## Items in Scope

| S2-ID | Backlog Item | Description | Sprint |
|-------|-------------|-------------|--------|
| S2-01 | BLG-GOV-116 | sprint_planning_prompt.md within-sprint date gate advisory | 1 |
| S2-02 | BLG-GOV-117 | execution_prompt.md pr_status read-after-open improvement | 1 |
| S2-03 | BLG-GOV-118 | qa_evidence commit discipline advisory in execution_prompt.md | 1 |
| S2-04 | BLG-BE-34 | Trade count gate-monitoring view (backend database view / optional endpoint) | 1 |
| S2-05 | BLG-GOV-120 | Trade data density progress tracker (System Status or SI-05 digest display) | 1 |
| S2-06 | BLG-OPS-13 | v2.8–v4.6 endpoint performance baseline re-run (24 endpoints) | 1 |
| S2-07 | BLG-OPS-61 | v5.1–v5.4 endpoint baseline extension (POST /digest/si05/send + remaining new endpoints) | 1 |
| S2-08 | BLG-OPS-54 | Add POST /digest/si05/send to api_performance_baseline.md (complements OPS-61) | 1 |
| S2-09 | BLG-QA-50 | Create formal regression test suite baseline document | 1 |
| S2-10 | BLG-FE-65 | User journey map: SI-05 Telegram digest to app action | 1 |
| S2-11 | BLG-FE-64 | Red Flag Journal visual design review pre-brief (gate: 2026-06-21) | 2 |
| S2-12 | BLG-OPS-59 | SI-05 p99 production latency baseline review (gate: ≥2026-07-04) | 2 |
| S2-13 | BLG-GOV-112 | SI-05 digest weekly cadence review (gate: 2026-07-04) | 2 |
| S2-14 | BLG-GOV-115 | SI-05 digest actionability metric definition (gate: 2026-07-04) | 2 |

---

## Items Explicitly Deferred

| Item | Reason for deferral |
|------|---------------------|
| BLG-GOV-119 (Arc 5 retrospective) | Gate: SI-04 + SI-05 Phase 2 both shipped; not met |
| BLG-GOV-121 (SI-05 Phase 2 §13 pre-clearance) | Gate: 2026-07-04 review + Phase 2 activation decision; to be scoped post-Sprint 2 |
| BLG-GOV-122 (strategy_rules.md §11 annual review) | Requires 12 months of trade data; only ~3 months available |
| BLG-FE-62 (Pre-entry panel combined spec) | Gate: SI-02 frontend (20+ closed trades); NOT MET (6 closed trades) |
| BLG-QA-55 (SI-02 Playwright scaffold readiness) | Gate: 20+ closed trades; NOT MET |
| BLG-OPS-53 (audit log retention expansion) | Gate: claude_audit_log 6+ months old (~Nov 2026) |
| BLG-GOV-95 (strategy_rules.md parameter review schedule) | Gate: ≥30 closed trades with stop exits; NOT MET |
| BLG-GOV-74 (AI feature quarterly review) | Gate: first review due 2026-08-29 |

---

## Supersession Note

*(Completed at Post-Ship Closure)*
