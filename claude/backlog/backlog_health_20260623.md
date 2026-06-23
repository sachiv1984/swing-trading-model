**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-23

# Backlog Health Report — 2026-06-23

Invoked as STEP 12 subroutine of post-ship closure 2026-06-22__release-v6.1.

---

## Summary

```
Backlog Health Summary — 2026-06-23

Total items reviewed: 113 (105 active + 8 to archive)
Complete — Archive: 8 (BLG-FEAT-25, BLG-QA-60, BLG-OPS-73, BLG-GOV-131, BLG-GOV-132, BLG-GOV-133, BLG-FE-76, BLG-FE-78)
Killed — Archive: 0
Active — Keep: 105 (after archiving 8 shipped items and removing v6.1 release slice)
Ephemeral sections removed: 1 (Release Slice v6.1 → retirement note)
Orphans flagged: 0
Blocked — stale blocker flagged: 0
Spec debt items — resolved: 0
Spec debt items — still open: 7 (BLG-SPEC-35, 36, 44, 46, 55, 56, 57 — all gated on Arc 4 pre-work)
Priority misalignments flagged: 4 (Provisional-Target stale at v6.1)
Deferral age violations (3+ cycles): 0
Promotion candidates: 0
Ambiguous items resolved: 0
ID uniqueness: PASS
Health: PASS
```

---

## Archived Items

| Item ID | Title | Shipped | ST |
|---------|-------|---------|-----|
| BLG-FEAT-25 | PT-04 Setup Quality Score (backend + frontend) | v6.1 | ST-08/09 |
| BLG-QA-60 | Register morning-briefing.spec.js and screener-quality.spec.js in playwright.yml | v6.1 | ST-04 |
| BLG-OPS-73 | Add PATCH /trades/{trade_id}/costs to api_performance_baseline.md | v6.1 | ST-05 |
| BLG-GOV-131 | Governance overhead ceiling metric and accountability mechanism | v6.1 | ST-03 |
| BLG-GOV-132 | Release planning: emit explicit Design Gate Required flag for UI-facing scope | v6.1 | ST-01 |
| BLG-GOV-133 | Sprint planning: enforce hard gate on design_gate_status at STEP -1 preflight | v6.1 | ST-02 |
| BLG-FE-76 | Portfolio sector heat-map visualization | v6.1 | ST-06 |
| BLG-FE-78 | Trade gate proximity indicator on dashboard | v6.1 | ST-07 |

---

## Promotion Candidates

None identified.

---

## Priority Alignment Notes

4 items retain `Provisional-Target: v6.1` but were not shipped in v6.1. PO should update these to v6.2 at next sprint planning:

| Item ID | Title | Current Target | Recommended |
|---------|-------|----------------|-------------|
| BLG-GOV-134 | CI: inline OpenAPI drift detection for api_performance_baseline.md | v6.1 | v6.2 |
| BLG-QA-62 | Playwright spec auto-registration via glob pattern in playwright.yml | v6.1 | v6.2 |
| BLG-OPS-74 | Log Anthropic API token usage and cost per morning briefing call | v6.1 | v6.2 |
| BLG-FE-77 | Refactor Watchlist.js to ESLint compliance | v6.1 | v6.2 |

Note: Priority changes require PO confirmation. These are advisory flags only — targets not changed by this engine.

---

## Orphans Flagged

None — all active items have roadmap home or explicit deferral status.

---

## Blocked Items — Stale Blockers

None identified.

---

## Spec Debt Status

| Item ID | Spec | Status | Action taken |
|---------|------|--------|-------------|
| BLG-SPEC-35 | PO-02 §13 boundary review for AI cross-journal analysis | Open — gated on Arc 4 delivery | No change |
| BLG-SPEC-36 | PO-02 AI output audit schema | Open — gated on Arc 4 delivery | No change |
| BLG-SPEC-44 | SI-02 drift threshold calibration specification | Open — gated on SI-02 frontend delivery | No change |
| BLG-SPEC-46 | Arc 4 API contract pre-planning surface area | Open — gated on Arc 4 delivery | No change |
| BLG-SPEC-55 | Arc 4 API contract pre-planning surface area advancement check | Open — gated on Arc 4 delivery | No change |
| BLG-SPEC-56 | Arc 4 API contract pre-authoring (PO-02/03/04) | Open — gated on Arc 4 delivery | No change |
| BLG-SPEC-57 | Data model v3 pre-definition for Arc 4 journal intelligence | Open — gated on Arc 4 delivery | No change |

All BLG-SPEC items are gated on Arc 4 or SI-02 pre-conditions — no action required until those gates clear.

---

## Items Requiring Product Owner Decision

1. Update Provisional-Target from v6.1 → v6.2 for 4 items: BLG-GOV-134, BLG-QA-62, BLG-OPS-74, BLG-FE-77.
   Action: PO to confirm at v6.2 sprint planning — no immediate action required.
