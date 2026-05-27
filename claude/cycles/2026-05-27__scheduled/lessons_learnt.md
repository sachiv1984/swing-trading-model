**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-27__scheduled

---

# Lessons Learnt — 2026-05-27__scheduled

## Process

| # | Observation | Owner | Action |
|---|-------------|-------|--------|
| LL-01 | CPS decline from 2.69 → 1.15 (Δ −1.54) triggered Strategy Drift Alert. Root cause is arc completion (Arc 3 + SI-01 + SI-03 shipped), not genuine strategy drift. Alert mechanism functioned correctly. | Strategy Rules & System Intent Owner | No action — monitoring sufficient. Advisory: expect CPS to stay low until SI-02 ships and SPS of delivered initiatives resets. |
| LL-02 | 3-cycle cap enforcement on 10 Parked-cycle-2 ideas completed without incident. All 10 correctly classified (6 advanced to gate-conditional backlog, 3 rejected, 1 re-parked). Cap enforcement is working as designed. | PMO Lead | No action. |
| LL-03 | IW-20260527-01 generated 44 new ideas heavily themed around Claude API transition compliance (audit trail, key security, cost monitoring) and SI-02 pre-planning. This reflects appropriate agent awareness of the v4.1 Gemini → Claude switch. | PMO Lead | Monitor: if Claude API compliance items are not sprint-planned within 2 cycles (v4.2/v4.3), flag as backlog congestion. |
| LL-04 | 15 of 44 new ideas (34%) were rejected for scope overlap with existing backlog items. Duplication rate increased from 9% (prior cycle) to 34%. Most overlaps were "execute this existing backlog item" ideas rather than genuinely new scope. | PMO Lead | Advisory: agents should consult backlog before submitting execution-level ideas. Consider adding "check if BLG item already exists" guidance to idea_intake_prompt.md. No immediate action this cycle. |
| LL-05 | BLG-OPS-33 gate cleared inline during STEP 4.0 — v4.1 sprint planning is now confirmed complete. Gate-cleared backlog item now ready for v4.2 sprint planning inclusion. | Infrastructure & Operations Owner | Action: include BLG-OPS-33 in v4.2 sprint planning candidate list. |
| LL-06 | BLG-GOV-48 (Gemini model version change policy) was correctly displaced to §9 Deferred as Gemini was retired in v4.1. BLG-GOV-64 (Anthropic model version pinning policy) supersedes its scope. Backlog displacement pattern functioned correctly. | Head of Specs Team | No action. |

## Deferred Patches

None.

## Outstanding Actions (for v4.2)

| # | Action | Owner | Target |
|---|--------|-------|--------|
| OA-1 | BLG-GOV-58: STEP 5.2 returned_to_backlog in-flight clarification — patch execution_prompt.md | Head of Specs Team | v4.2 sprint seal |
| OA-2 | BLG-OPS-35: POST /ai/check-daily-cost to api_performance_baseline.md | Infrastructure & Operations Owner | v4.2 sprint |
| OA-3 | STEP 5.0A null pr_number guard (carry-forward from v4.1 OA-1) | Head of Specs Team | v4.2 sprint seal |
