**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-06-17__release-v5.8
**Phase:** Release Planning

---

# Lessons Learnt — v5.8 Release Planning

## Process Observations

| ID | Observation | Type | Action |
|----|-------------|------|--------|
| LL-RP-v58-01 | §-1.2 cleared via post-ship closure `next_release` declaration for second consecutive cycle (same as v5.7). The pattern of running release planning immediately after post-ship closure without an intervening rebalance is now established. | Observation | Advisory — consider whether a lightweight Now-section addition at post-ship closure (rather than waiting for rebalance) would streamline this step in future cycles. Owner: PMO Lead |
| LL-RP-v58-02 | BLG-FE-64 perennial-return check (4th return) triggered PO active disposition correctly. Gate 2026-06-21 is now time-certain — confirming that within-sprint gates that are time-certain should be treated as firm, not conditional. | Positive | No process change needed. The perennial-return gate (§1.4a) correctly surfaced this and forced PO disposition. |
| LL-RP-v58-03 | Ghost backlog entries detected: BLG-GOV-116/117/118/BLG-BE-34/BLG-GOV-120 remain in active backlog.md without ✅ markers but are confirmed shipped (backlog_archive.md shows ✅). Groom backlog did not catch these in v5.7 run (groom archived only v5.7 items). | Process gap | Deferred: at v5.8 post-ship, groom backlog should clean up these ghost entries. Owner: PMO Lead. |

## Key Planning Outcomes

- 7 stories scoped: 4 firm (Sprint 1) + 3 conditional (Sprint 2, gate 2026-07-04)
- 2 EPICs: EPIC-01 (UX/ops/governance) + EPIC-02 (SI-05 effectiveness, conditional)
- Design gate: NOT required (0 new features requiring design decisions; EPIC-01 items are design reviews and ops, not new feature implementation)
- No escalations raised

---

// ARTEFACT_STATUS
```json
{
  "phase": "Release",
  "cycle_id": "2026-06-17__release-v5.8",
  "release": "v5.8",
  "status": "Published",
  "stories_firm": 4,
  "stories_conditional": 3,
  "epics": 2,
  "open_escalations": 0,
  "publish_gate": "PASS"
}
```
