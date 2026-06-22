**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-22

# Backlog Health Report — 2026-06-22

*Groom run: post-ship closure 2026-06-19__release-v6.0*

---

## Summary

```
Backlog Health Summary — 2026-06-22
---
Complete — Archive (new, v6.0): 11
Previously archived — removed from active: 0
Total items removed from active backlog: 11
Ephemeral sections retired: 2 (Release Slices v5.9 and v6.0)
Active BLG headings remaining: 104
Spec debt items open: 1 (BLG-OPS-73 — v6.1 target, XS effort)
Priority misalignments flagged: 0
Promotion candidates: 3 (advisory — BLG-SPEC-35, BLG-GOV-132, BLG-GOV-133)
Orphan items: 0
Stale blockers: 0
Duplicate IDs: none (ID uniqueness: PASS)
```

---

## Items Archived This Run

### New archives (v6.0 delivery — 11 items)

| ID | Title | Shipped |
|----|-------|---------|
| BLG-BE-36 | Align signal_service suggested_shares to risk-based sizing model | v6.0 ST-01 |
| BLG-FEAT-46 | Trader's Morning Briefing dashboard | v6.0 ST-02 |
| BLG-FEAT-20 | Net-of-costs performance tracking | v6.0 ST-03 |
| BLG-FEAT-47 | Screener data quality telemetry | v6.0 ST-04 |
| BLG-OPS-70 | SI-05 deep link AC-04 staging confirmation | v6.0 ST-05 |
| BLG-FE-64 | RFJ design review pre-brief | v6.0 ST-06 |
| BLG-FE-41 | Red Flag Journal visual design review | v6.0 ST-07 |
| BLG-GOV-112 | SI-05 digest weekly cadence review | v6.0 ST-08 |
| BLG-GOV-115 | SI-05 digest actionability metric definition | v6.0 ST-09 |
| BLG-GOV-130 | SI-05 Phase 2 activation decision scope | v6.0 ST-10 |
| BLG-OPS-59 | SI-05 service production p99 latency baseline review | v6.0 ST-11 |

### Ephemeral sections retired

| Section | Action |
|---------|--------|
| Release Slice — v5.9 | Replaced with retirement notice pointing to canonical record |
| Release Slice — v6.0 | Replaced with retirement notice pointing to canonical record |

---

## Spec Debt Check

| ID | Title | Type | Target | Status |
|----|-------|------|--------|--------|
| BLG-OPS-73 | Add PATCH /trades/{trade_id}/costs to api_performance_baseline.md | OPS / endpoint coverage drift | v6.1 | Active — XS effort, tracked |

**Assessment:** 1 open spec debt item. Filed during this post-ship closure (endpoint drift detected). Provisional target v6.1, effort XS. No spec debt blocker to sprint planning.

---

## Deferral Age Check

| ID | Title | Deferrals | Last PO Action | Gate Condition | Assessment |
|----|-------|-----------|---------------|----------------|------------|
| BLG-FEAT-25 | PT-04 Setup Quality Score | 6+ | PO re-park 2026-05-22 (confirmed gate condition: 20+ closed trades) | Gate NOT MET — 13 trades as of 2026-06-16; 7 more needed | Formal park with active gate. Not stale. No escalation required — trajectory accelerating (~7 new trades in 7 days at v5.6). |

**Assessment:** No hard deferral blockers. PT-04 is formally parked with PO sign-off and an active data-driven gate condition.

---

## Active Backlog Status

- Active BLG item count: 104 headings
- No orphan items detected (all items have BLG-TYPE-NNN format)
- No stale blocker patterns detected (gate-conditional items have defined gate criteria)
- No priority misalignment against roadmap (v6.1 now section not yet authored)
- ID uniqueness: PASS (no duplicates found)

---

## Promotion Shortlist (Advisory)

The following items are P1 and worth highlighting for v6.1 planning:

| ID | Title | Priority | Notes |
|----|-------|----------|-------|
| BLG-GOV-132 | Release planning: emit explicit Design Gate Required flag | P1 | Lessons learnt carry-forward from v6.0 — release planning engine update |
| BLG-GOV-133 | Sprint planning: enforce hard gate on design_gate_status | P1 | Lessons learnt carry-forward from v6.0 — sprint planning engine update |
| BLG-QA-60 | Register morning-briefing.spec.js and screener-quality.spec.js in playwright.yml | P2 (carry-forward) | v6.0 lessons learnt carry-forward item — Release Planning gate ~2026-07-02 |
| BLG-SPEC-35 | PO-02 §13 boundary review for AI cross-journal analysis | P1 | Arc 4 pre-planning; gate: PO-02 sprint planning imminent |

*This is an advisory list only. Promotion decisions are made at release planning (run roadmap / plan release).*

---

## Health Status

**PASS** — backlog cleaned; 11 completed v6.0 items archived to backlog_archive.md; 2 ephemeral release slices retired; 1 spec debt item tracked (v6.1); 0 deferral escalations; ID uniqueness confirmed.
