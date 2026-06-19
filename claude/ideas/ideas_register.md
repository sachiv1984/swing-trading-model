**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.8
**Last Updated:** 2026-06-19 (roadmap rebalance 2026-06-19__scheduled — 16 IW-20260619-01 ideas classified)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Ideas Register

Migrated from per-file model (44 submissions from IW-20260304-01) on 2026-03-17 per ST-19 (EPIC-06).
Schema: per `shared_standards.md §16.5`

| Idea ID | Title | Submitter | Window | Submitted At | Status | Park Count | Park Rationale | Step 4 | Step 5 |
|---------|-------|-----------|--------|--------------|--------|------------|----------------|--------|--------|
| IDEA-product-owner-20260619-01 | Portfolio sector heat-map visualization | Product Owner | IW-20260619-01 | 2026-06-19 | Promoted-Backlog | 0 | Advanced via STEP 5 — Challenger Product Velocity Concern supports; no §13 concern | Advance → STEP 5 | BLG-FE-76 (P2, v6.1) |
| IDEA-product-owner-20260619-02 | Trade tagging and tag-based performance filtering | Product Owner | IW-20260619-01 | 2026-06-19 | Parked-cycle-1 | 0 | v6.0 user-value quota absorbed by FEAT-46/47/20/BE-36; BLG-FE-76 covers portfolio visualisation investment; data model change is multi-sprint; revisit for v6.1 | Park C1 | — |
| IDEA-head-of-specs-20260619-01 | Arc 4 API contract pre-authoring (PO-02/03/04) | Head of Specs Team | IW-20260619-01 | 2026-06-19 | Promoted-Backlog | 0 | High-leverage pre-authoring; Arc 4 gate ~2026-10; no §13 concern at this stage | Promoted-Backlog (immediate) | BLG-SPEC-56 |
| IDEA-head-of-specs-20260619-02 | Data model v3 pre-definition for Arc 4 journal intelligence | Head of Specs Team | IW-20260619-01 | 2026-06-19 | Promoted-Backlog | 0 | Pairs with BLG-SPEC-56; reduces execution risk when PO-02 gate clears | Promoted-Backlog (immediate) | BLG-SPEC-57 |
| IDEA-pmo-lead-20260619-01 | Automated governance health score computation script | PMO Lead | IW-20260619-01 | 2026-06-19 | Parked-cycle-1 | 0 | Useful but not critical-path; run_manifest.md reports health accurately; not a bottleneck | Park C1 | — |
| IDEA-pmo-lead-20260619-02 | Sprint velocity trend chart (last 10 cycles) | PMO Lead | IW-20260619-01 | 2026-06-19 | Parked-cycle-1 | 0 | Velocity data exists in velocity_metrics.md; visualisation adds value but low urgency | Park C1 | — |
| IDEA-director-of-quality-20260619-01 | Arc 4 E2E test strategy pre-design (PO-02/03/04) | Director of Quality | IW-20260619-01 | 2026-06-19 | Promoted-Backlog | 0 | Test strategy decisions before sprint planning pressure; complements SPEC-56/57 | Promoted-Backlog (immediate) | BLG-QA-59 |
| IDEA-director-of-quality-20260619-02 | Automated accessibility testing (axe-core) in Playwright CI | Director of Quality | IW-20260619-01 | 2026-06-19 | Parked-cycle-1 | 0 | Valuable but not on critical path at this Arc stage; park for later Arc 4+ design work | Park C1 | — |
| IDEA-strategy-owner-20260619-01 | §13 pre-assessment for Arc 4 AI features (PO-02/03) | Strategy Rules & System Intent Owner | IW-20260619-01 | 2026-06-19 | Rejected | 0 | Exact duplicate of BLG-SPEC-35 (P1, active — already tracked) | Rejected (duplicate) | — |
| IDEA-strategy-owner-20260619-02 | Formal strategy rules effectiveness review cadence | Strategy Rules & System Intent Owner | IW-20260619-01 | 2026-06-19 | Parked-cycle-1 | 0 | strategy_rules.md v1.4 stable; formal cadence adds overhead — contradicts governance simplification direction (v5.9) | Park C1 | — |
| IDEA-finops-20260619-01 | AI API cost model for Arc 4 journal intelligence features | FinOps & Resource Architect | IW-20260619-01 | 2026-06-19 | Promoted-Backlog | 0 | FinOps charter item; Arc 4 AI features will have material API cost; cost model should precede build | Promoted-Backlog (immediate) | BLG-OPS-72 |
| IDEA-finops-20260619-02 | Alpaca API tier and cost optimization assessment | FinOps & Resource Architect | IW-20260619-01 | 2026-06-19 | Parked-cycle-1 | 0 | BLG-OPS-37 (Anthropic tier assessment) completed with no-upgrade outcome; Alpaca stable at current levels | Park C1 | — |
| IDEA-infra-ops-20260619-01 | Database index audit for Arc 4 cross-table queries | Infrastructure & Operations Owner | IW-20260619-01 | 2026-06-19 | Promoted-Backlog | 0 | Arc 4 introduces cross-table query patterns not in current schema; pre-audit prevents post-ship latency surprises | Promoted-Backlog (immediate) | BLG-BE-37 |
| IDEA-infra-ops-20260619-02 | Enhanced health check with external dependency verification | Infrastructure & Operations Owner | IW-20260619-01 | 2026-06-19 | Parked-cycle-1 | 0 | Current health check adequate; external dependency probing valuable later if SLA monitoring required | Park C1 | — |
| IDEA-challenger-20260619-01 | Data provider diversity risk assessment and failover strategy | Challenger | IW-20260619-01 | 2026-06-19 | Parked-cycle-1 | 0 | Alpaca deeply integrated; failover requires significant architecture work; single-provider risk accepted at current stage | Park C1 | — |
| IDEA-challenger-20260619-02 | Governance overhead ceiling metric and accountability mechanism | Challenger | IW-20260619-01 | 2026-06-19 | Promoted-Backlog | 0 | Elevated: directly addresses Product Value Alert (G+D+P=90.7% last 5 cycles) and Skill-Silo Alert; governance accountability mechanism is load-bearing | Promoted-Backlog (immediate; elevated) | BLG-GOV-131 |
