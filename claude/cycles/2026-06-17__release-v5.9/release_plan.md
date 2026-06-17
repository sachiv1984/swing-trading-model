**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-17__release-v5.9
**Published:** 2026-06-17
**Scope revision:** v1 — 2026-06-17: EPIC-02 replaced; removed 8 date-gated items; added 6 ungated ready-now items. Authorized by Product Owner before sprint planning.

---

# Release Plan — v5.9

## Readiness

Prior cycle: 2026-06-17__release-v5.8 — Closed_with_actions. post_ship_complete=true. next_cycle_unblocked=true.

Preflight: PASS. All required files present. All required agent roles verified. No amendment in progress. No stale backlog lock.

§-1.2: v5.9 confirmed on roadmap (RA:v5.9 section present). PASS.

## Scope

| S2-ID | Description | Stories | Status |
|-------|-------------|---------|--------|
| S2-01 | Governance Simplification Candidates SC-03–SC-07 | BLG-GOV-125, 126, 127, 128, 129 | Firm |
| S2-02 | QA Coverage & Test Infrastructure | BLG-QA-24, BLG-QA-34, BLG-QA-50 | Firm |
| S2-03 | Governance Audit & Process Records | BLG-GOV-38, BLG-GOV-53 | Firm |
| S2-04 | Frontend Pre-entry UX Improvement | BLG-FE-57 | Firm |

**Items explicitly deferred to v5.10:**
- BLG-FE-64, BLG-FE-41 (gate 2026-06-21) — BLG-FE-64 will be 6th deferral; carry-forward mandatory
- BLG-OPS-70 (gate ~2026-06-23) — trailing obligation; check at v5.10 sprint planning or delivery verification
- BLG-GOV-112, BLG-GOV-113, BLG-GOV-115, BLG-OPS-59, BLG-GOV-130 (gate 2026-07-04) — SI-05 effectiveness review items; v5.10 primary scope

**Firm count:** 11 | **Conditional count:** 0 | **Total:** 11

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Specs Team | RISK-01 | None — ready immediately; merge first |
| EPIC-02 | S2-02, S2-03, S2-04 | Director of Quality; QA Lead; Head of UX & Design | RISK-02 | None — all ready immediately; merge after EPIC-01 |

**EPIC-01 notes:** 5 governance prompt simplifications (SC-03–SC-07). No backend or frontend changes. ~1 hour each.

**EPIC-02 notes:** Mixed QA/governance/frontend stories, all ungated. BLG-FE-57 (ST-11) introduces a frontend-visible change — requires Playwright automated test coverage or human staging sign-off per CLAUDE.md §2 before PR opens.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Version drift if CLAUDE.md §6 checklist not followed on each prompt edit | Medium | Each story explicitly includes version bump + §14 + change log ACs | null |
| RISK-02 | EPIC-02 | BLG-FE-57 requires observable AC evidence (Playwright or staging sign-off); no other frontend stories in this release to share the staging effort | Low | Story ACs explicitly require Playwright coverage OR dated staging sign-off before PR opens | null |

## Capacity Check

| EPIC | Items | Estimate |
|------|-------|----------|
| EPIC-01 | 5 × XS | ~5 hrs |
| EPIC-02 | BLG-QA-24 (S), BLG-GOV-38 (S), BLG-QA-34 (S), BLG-GOV-53 (S), BLG-QA-50 (S), BLG-FE-57 (XS) | ~8–12 hrs |

**Total estimated:** ~13–17 hours. Single sprint. PASS.

## Integrity Validation

- All S2-IDs map to EPICs ✓
- All EPIC IDs in backlog slice reference correct S2 items ✓
- All RISK-IDs in EPIC table appear in Risk Register ✓
- No orphaned references ✓

STEP 5.5: **PASS** | Decision Record Integrity: **N/A**
