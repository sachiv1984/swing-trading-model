**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-17

---

# Stage 2 — Backlog Health Review

**Cycle:** 2026-03-17__item-v1.10
**Date:** 2026-03-17
**Authorities:** Head of Specs Team (process), Product Owner (planning ownership)

---

## Backlog State Review

### Recently Completed (v1.10 — archived to backlog_archive.md)

| Item | Status |
|------|--------|
| BLG-OPS-01 — Provision development environment | ✅ Shipped v1.10 (EPIC-01) |
| BLG-TECH-06 — Fix CohortAnalysis client-side computation | ✅ Shipped v1.10 (EPIC-02) |
| BLG-API-01 — Backend API integration tests | ✅ Shipped v1.10 (EPIC-03) |
| TEST-GAP-EPIC-06 — v1.7 QA scenario coverage gaps | ✅ Shipped v1.10 (EPIC-03) |

These are correctly recorded in the Closed Items table and the archive.

---

### Active Backlog Items — Health Assessment

#### BLG-BE-01 — GET /portfolio missing 4 fields (P1)
**Target:** v1.11
**Health:** Healthy. GAP-03 finding from v1.10 staging execution. P1 priority appropriate — these fields are required by `portfolio_endpoints.md` v1.9.0. Evidence base is strong (staging API response vs spec comparison). Owner is Head of Engineering. Target release v1.11 is realistic. No orphan status — properly scoped with acceptance criteria.

#### TEST-GAP-EPIC-02 — CohortAnalysis backend integration regression scenario (P3)
**Target:** Before next sprint touching analytics components
**Health:** Healthy. Test scenario coverage gap from v1.10 verification. P3 priority appropriate — not blocking. QA & Testing Owner responsible. No orphan status.

#### BLG-BE-02 — Spec and implement GET /portfolio/prospective-heat endpoint (P3)
**Target:** v2.0 (or earlier if ProspectiveHeatPanel becomes a priority)
**Health:** Healthy. DEV-ST05-01 finding from v1.10 sprint execution. P3 priority appropriate — frontend component exists but endpoint not specced. Ownership clear (Head of Engineering + Head of Specs Team joint). `@unittest.skip` is a technical debt marker with clear resolution path.

#### BLG-NEW-13 — Spec Coverage Inventory (P2)
**Target:** v2.0 (or v1.10 if capacity allows)
**Health:** Healthy. v1.10 capacity was committed to infrastructure — target was aspirational. v2.0 is realistic. No pre-work blockers. Owned by Head of Specs Team. Complements BLG-GOV-01.

#### BLG-GOV-01 — Roadmap stage document consolidation (P2)
**Target:** v2.0 governance prep
**Health:** Healthy. Well-scoped: specific prompt files, acceptance criteria, and validation step defined. Owned by Head of Specs Team. No orphan status. This is a meaningful governance improvement for future cycle efficiency.

#### BLG-GOV-02 — Ideas register redesign (P2)
**Target:** v2.0 governance prep
**Health:** Healthy. Well-scoped: clear migration path, specific prompt changes identified. Owned by Head of Specs Team. Depends on BLG-GOV-01 (or can proceed in parallel — both are prompt/template changes). Note: current idea submission pool has 29 Parked-cycle-2 ideas; the redesign will reduce future intake overhead significantly.

#### BLG-FEAT-03 — Slippage Tracking (P2)
**Target:** v2.1
**Health:** Healthy. Data model pre-work gate correctly noted (Fill Price field must be defined in data_model.md first). Orphan status resolved 2026-03-15. No active blocker — properly deferred to v2.1.

#### BLG-TECH-05 — Prometheus metrics endpoint (P3)
**Target:** v2.1 or multi-user milestone
**Health:** Healthy. Correctly deferred — single-user system doesn't need Prometheus now. Gate condition clear (operational need or multi-user). No action required.

---

### Backlog Health Summary

| Check | Result |
|-------|--------|
| Obsolete items? | None identified |
| Duplicates? | None identified. BLG-NEW-13 (Spec Coverage Inventory) and BLG-GOV-01 (stage consolidation) are complementary, not duplicate. |
| Strategic alignment? | All items align. BLG-BE-01 is a correctness item (high value). BLG-GOV-01/02 are process improvements supporting governance quality. |
| Quick wins being ignored? | BLG-BE-01 is P1 and v1.11 targeted — will be prioritised in next release planning. BLG-NEW-13 is P2 and executable in v2.0. No quick wins being ignored. |
| Technical debt accumulating? | BLG-BE-02 (`@unittest.skip`) is a tracked debt item. BLG-BE-01 is a spec-divergence item. Both are visible, owned, and targeted. No silent accumulation. |
| Promotion candidates? | BLG-BE-01 is already P1 and v1.11 targeted. Does not require roadmap-level elevation — will be handled in release planning. |

---

### Observations for STEP 4–5

- BLG-GOV-01 and BLG-GOV-02 are already in the backlog. Any ideas advancing from STEP 4 that overlap with these should be parked (Challenger will flag overlap).
- BLG-BE-01 is P1 and targeted at v1.11 — signals that a v1.11 patch release may be warranted (to be decided in release planning, not this roadmap rebalance).
- 3 backlog items targeting v2.0 (BLG-NEW-13, BLG-BE-02, and implicitly BLG-GOV-01/02 as governance prep) — v2.0 release planning will need to sequence these against the core initiatives (4.1b, 4.3).
