Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Release: v3.7
Cycle: 2026-05-18__release-v3.7
Last Updated: 2026-05-18

---

# Lessons Learnt — Release Planning v3.7

**Phase:** Release Planning (Phase 1B)
**Engine version:** release_planning_prompt.md v2.28

---

## Planning Observations

1. **EPIC-02 conditional pattern:** The PT-04 gate condition (20+ closed trades) has now caused EPIC-02 to carry through two consecutive release plans (v3.6 deferred, v3.7 conditional). The design gate + sprint planning gate pattern is working — but if the gate is not met at v3.7 either, consider whether to formally park PT-04 until the gate is confirmed rather than carrying it as conditional every cycle.

2. **Arc 4 data density timeline:** PO-02/03/04 are gated on 6+ months of AI-summarised journal entries. AI Journal (BLG-FEAT-16) shipped v2.8 (2026-04-20). At the current ~1 month elapsed, these features cannot enter scope until approximately November 2026. v3.7 correctly excluded them. Future release planning should note this as a hard gate until then.

3. **scored_initiatives.md escalation threshold:** OA-RP-05 carried through two consecutive post-ship closures before reaching the "treat as escalation" threshold stated in v3.6 lessons_learnt_closure.md. Including BLG-GOV-23 in v3.7 scope (ST-11) resolves this before a formal escalation was required. The BLG-GOV-23 backlog item filed at 2026-05-18__scheduled rebalance provided the appropriate tracking.

4. **Prompt change log gaps (advisory):** Three prompt version gaps identified at STEP -1.7 — execution_prompt.md (v3.18→v3.22), sprint_planning_prompt.md (v3.0→v3.2), backlog_management_prompt.md (v1.6→v1.7). These suggest sprint execution governance patches are not consistently appending change log entries. ST-07 includes retroactive entries as part of scope. Root cause: sprint execution engine does not explicitly prompt for change log entries when bumping governance prompt versions within a story. Recommend adding a change log entry requirement to the governance patch story template.

5. **S2-01 UX scope:** BLG-FE-33 and BLG-FE-34 both target v3.7 and are P1. The signal → watchlist dependency chain (BLG-FE-33 must ship before BLG-FE-34) is correctly captured as RISK-02 and sequenced within EPIC-01. This is the correct approach — sequential story dependencies within a single EPIC are manageable.

---

## Action Items

| Action | Owner | Target | Priority |
|--------|-------|--------|----------|
| Sprint Planning: confirm sub-step 10a present in execution_prompt.md before execution begins (carry-forward) | Sprint Planning Engine | v3.7 sprint planning | Process |
| Sprint Execution: flag BLG-GOV-19 class eligibility for all observable-AC stories (carry-forward) | Sprint Execution Engine | v3.7 sprint execution | Process |
| After ST-07 ships: verify prompt_change_log.md has retroactive entries for all three gap prompts | Head of Specs Team | v3.7 EPIC-03 | P1 |
| After v3.7 closes: evaluate PT-04 gate status — if still not met, explicitly park to "pending gate" rather than conditional scope again | Product Owner | v3.7 post-ship | Advisory |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-05-18__release-v3.7",
  "status": "complete",
  "generated_utc": "2026-05-18T12:50:00Z"
}
