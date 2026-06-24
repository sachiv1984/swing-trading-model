**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 2.0
**Last Updated:** 2026-06-24 (rebalance 2026-06-24__scheduled — 8 terminal hard-cap ideas disposed (4 Rejected, 4 Backlog-gate-conditional); 3 Parked-cycle-1 ideas Rejected (2 gate-condition re-eval, 1 intent fulfilled); 8 Parked-cycle-1 → Parked-cycle-2; 8 rows remain)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Ideas Register

Migrated from per-file model (44 submissions from IW-20260304-01) on 2026-03-17 per ST-19 (EPIC-06).
Schema: per `shared_standards.md §16.5`

| Idea ID | Title | Submitter | Window | Submitted At | Status | Park Count | Park Rationale | Step 4 | Step 5 |
|---------|-------|-----------|--------|--------------|--------|------------|----------------|--------|--------|
| IDEA-product-owner-20260622-02 | Morning briefing section configurability | Product Owner | IW-20260622-01 | 2026-06-22 | Parked-cycle-2 | 1 | v[TBD] not yet started; morning briefing usage patterns not yet established; configurability decisions premature | Park C2 | — |
| IDEA-head-of-specs-20260622-02 | Governance artefact completeness gate at run roadmap STEP 0 | Head of Specs Team | IW-20260622-01 | 2026-06-22 | Parked-cycle-2 | 1 | STEP 0 artefact checks remain adequate; formal gate adds complexity; BLG-GOV-28 and related items cover gate requirements | Park C2 | — |
| IDEA-pmo-lead-20260622-01 | Governance health score persistence across cycles | PMO Lead | IW-20260622-01 | 2026-06-22 | Parked-cycle-2 | 1 | GHS framework still maturing (3+ consistent audits needed); persistence before framework stabilises would create noisy trend data | Park C2 | — |
| IDEA-pmo-lead-20260622-02 | Backlog item age tracking and stale item detection | PMO Lead | IW-20260622-01 | 2026-06-22 | Parked-cycle-2 | 1 | backlog_management_prompt.md v1.9 ghost entry detection remains adequate; age tracking overhead not yet warranted | Park C2 | — |
| IDEA-director-of-quality-20260622-02 | API endpoint test coverage gap report in CI | Director of Quality | IW-20260622-01 | 2026-06-22 | Parked-cycle-2 | 1 | BLG-GOV-134 open (target v6.2); this is complementary — park until BLG-GOV-134 ships | Park C2 | — |
| IDEA-finops-20260622-02 | Release cost estimation at release planning | FinOps & Resource Architect | IW-20260622-01 | 2026-06-22 | Parked-cycle-2 | 1 | BLG-OPS-74 (cost logging prerequisite) filed v6.1 post-ship — gate still pending; revisit after BLG-OPS-74 ships | Park C2 | — |
| IDEA-infra-ops-20260622-01 | Background scheduler health monitoring endpoint | Infrastructure & Operations Owner | IW-20260622-01 | 2026-06-22 | Parked-cycle-2 | 1 | BLG-FEAT-46/47 in Now horizon — background job complexity will increase post-v[TBD]; monitoring value higher after v[TBD] ships | Park C2 | — |
| IDEA-infra-ops-20260622-02 | Deployment health dashboard widget showing version and timestamp | Infrastructure & Operations Owner | IW-20260622-01 | 2026-06-22 | Parked-cycle-2 | 1 | System status page remains adequate at current single-environment scale; deployment version display low urgency | Park C2 | — |

---

*Terminal disposals from 2026-06-24__scheduled (pending housekeeping archival):*
*IDEA-product-owner-20260619-02 → Backlog-gate-conditional (BLG-FEAT-52)*
*IDEA-pmo-lead-20260619-01 → Rejected (hard cap; automation adds overhead without proportional value)*
*IDEA-pmo-lead-20260619-02 → Rejected (hard cap; velocity_metrics.md infrastructure not yet established)*
*IDEA-director-of-quality-20260619-02 → Backlog-gate-conditional (BLG-QA-63)*
*IDEA-strategy-owner-20260619-02 → Rejected (hard cap; scope covered by BLG-GOV-122 and BLG-GOV-95)*
*IDEA-finops-20260619-02 → Rejected (hard cap; BLG-OPS-17 addresses cost optimization)*
*IDEA-infra-ops-20260619-02 → Backlog-gate-conditional (BLG-OPS-76)*
*IDEA-challenger-20260619-01 → Backlog-gate-conditional (BLG-OPS-77)*
*IDEA-strategy-owner-20260622-01 → Rejected (gate-condition re-eval: PT-04 shipped; scope subsumed by BLG-FE-78 + planned BLG-FEAT-50)*
*IDEA-strategy-owner-20260622-02 → Rejected (intent fulfilled: BLG-GOV-112 completed SI-05 Phase 1 effectiveness review in v6.0)*
*IDEA-challenger-20260622-02 → Rejected (gate-condition re-eval: PT-04 shipped under count-based gate; threshold question resolved)*
