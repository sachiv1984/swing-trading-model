**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-17

# Backlog Health Report — 2026-03-17

**Invoked by:** Post-Ship Closure Engine (STEP 12) — `run post-ship --cycle 2026-03-17__release-v2.0`
**Run date:** 2026-03-17
**Lock:** GROOM-20260317-01

---

## Summary

```
Backlog Health Summary — 2026-03-17

Total items reviewed: 16
Complete — Archive: 4 (TEST-GAP-EPIC-02, BLG-BE-02, BLG-GOV-01, BLG-GOV-02)
Killed — Archive: 0
Active — Keep: 12
Orphans flagged: 0
Blocked — stale blocker flagged: 0
Spec debt items — resolved: 0 (none of the BLG-SPEC-* items were resolved this cycle)
Spec debt items — still open: 5 (BLG-SPEC-G6, BLG-SPEC-D10, BLG-SPEC-D11, BLG-SPEC-D12, BLG-SPEC-D13)
Priority misalignments flagged: 1 (BLG-SPEC-D10 — re-targeted v2.0 post-ship → v2.1)
Promotion candidates: 2 (BLG-TECH-08, BLG-SPEC-D12)
Ambiguous items resolved: 0
```

---

## Classification Table

| Item ID | Title | Current Priority | Classification | Evidence | Action |
|---------|-------|-----------------|----------------|----------|--------|
| BLG-TECH-05 | Prometheus metrics endpoint | P3 | Active — Keep | Target v2.1, no blockers | No change |
| BLG-FEAT-03 | Slippage Tracking | P2 | Active — Keep | Target v2.1, PO confirmed 2026-03-15 | No change |
| TEST-GAP-EPIC-02 | CohortAnalysis regression scenario | P3 | Complete — Archive | Shipped v2.0 EPIC-05/ST-20 | Archived |
| BLG-BE-02 | GET /portfolio/prospective-heat | P3 | Complete — Archive | Shipped v2.0 EPIC-04/ST-13 | Archived |
| BLG-SPEC-G6 | total_return_pct not returned | P3 | Active — Keep | Added v2.0, target v2.1 | No change |
| BLG-SPEC-D10 | api_dependencies.md v2.0 additions | P3 | Active — Keep (re-targeted) | Added v2.0; was "v2.0 post-ship" — re-targeted to v2.1 | Target updated |
| BLG-SPEC-D11 | data_model.md §501 trade_reflections | P3 | Active — Keep | Added v2.0, target v2.1 | No change |
| BLG-SPEC-D12 | Bulk lifecycle header remediation | P2 | Promote Candidate | Added v2.0, target v2.1, no blockers | Shortlisted |
| BLG-SPEC-D13 | metrics_definitions.md Owner field | P2 | Active — Keep | Added v2.0, target v2.1 | No change |
| TEST-GAP-SIG-01 | Signals page controls scenarios | P3 | Active — Keep | Added v2.0, target pre-next-sprint | No change |
| TEST-GAP-TAX-01 | Tax Year P&L report scenarios | P3 | Active — Keep | Added v2.0, target pre-next-sprint | No change |
| BLG-PROC-01 | Cross-EPIC branch commits follow-up | P3 | Active — Keep | Added v2.0, target v2.1 retrospective | No change |
| BLG-TECH-08 | Async notification architecture ADR | P2 | Promote Candidate | v2.1 prerequisite, no blockers | Shortlisted |
| BLG-OPS-03 | Pre-merge preview environments | P2 | Active — Keep | Added v2.0, target v2.1 | No change |
| BLG-GOV-01 | Roadmap stage document consolidation | P2 | Complete — Archive | Shipped v2.0 EPIC-06/ST-18 | Archived |
| BLG-GOV-02 | Ideas register | P2 | Complete — Archive | Shipped v2.0 EPIC-06/ST-19 | Archived |

---

## Promotion Candidates

| Item ID | Title | Priority | Why Promote | Target Release | Pre-work Status |
|---------|-------|----------|-------------|----------------|-----------------|
| BLG-TECH-08 | Async notification architecture ADR | P2 | v2.1 prerequisite — EPIC-03 (Alerts) cannot be sprint-planned without this ADR; no blockers | v2.1 | Complete — no pre-work outstanding |
| BLG-SPEC-D12 | Bulk lifecycle header remediation (28 docs) | P2 | Low-risk, high-compliance-value, no spec dependencies; can be batched as governance sprint item in v2.1 | v2.1 | Complete — no pre-work outstanding |

Note: This list is advisory only. No items are added to the roadmap by this engine.

---

## Priority Alignment Notes

| Item ID | Note |
|---------|------|
| BLG-SPEC-D10 | Target release was "v2.0 post-ship" — v2.0 has now shipped. Re-targeted to v2.1 in this grooming run. |

No other priority misalignments found.

---

## Orphans Flagged

None — all active items have a stated target release or owner-confirmed rationale.

---

## Blocked Items — Stale Blockers

None — no items have stale blockers.

---

## Spec Debt Status

| Item ID | Spec | Status | Action taken |
|---------|------|--------|-------------|
| BLG-SPEC-G6 | `analytics_endpoints.md` | Still open — `total_return_pct` absent from response | Active — Keep |
| BLG-SPEC-D10 | `api_dependencies.md` | Still open — v2.0 additions not yet reflected | Active — Keep; re-targeted to v2.1 |
| BLG-SPEC-D11 | `data_model.md §501` | Still open — trade_reflections entry not updated | Active — Keep |
| BLG-SPEC-D12 | 28 spec documents | Still open — lifecycle header compliance gap | Active — Keep; shortlisted for promotion |
| BLG-SPEC-D13 | `metrics_definitions.md` | Still open — Owner field non-compliant | Active — Keep |

---

## Items Requiring Product Owner Decision

None — all classifications were unambiguous. Promotion candidates (BLG-TECH-08, BLG-SPEC-D12) are advisory and require Product Owner decision before roadmap entry.
