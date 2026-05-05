**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Filed
**Release:** v3.2
**Cycle:** 2026-05-05__release-v3.2
**Last Updated:** 2026-05-05
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Lessons Learnt — Release Planning v3.2

---

## Process Observations

### Carry-forward resolution (positive)
All 3 carry-forward items from v3.1 (CF-01: branch check, CF-02: test_scenarios advisory, CF-03: Playwright waitFor) are addressed in EPIC-03. Carry-forward tracking is working as intended — items reach sprint scope within one cycle of deferral.

### BLG-GOV-11 pattern (watchlist)
BLG-GOV-11 (cycle artefact inventory) has been deferred 3 consecutive cycles. This release planning run is the first to explicitly label it "mandatory". Consider adding a governance rule: any P3 item deferred 3+ consecutive cycles must enter the next release scope unless Product Owner explicitly re-defers with a named reason. This would surface the pattern automatically rather than relying on manual tracking.

### OA-01 still open
The v3.1 scope document (OA-01 from v3.1 closure) was not resolved before v3.2 planning commenced. The "before v3.2 plan release" deadline passed. This is a process gap in OA tracking — OAs owned by PMO Lead should be resolved before the next cycle opens, not allowed to drift into the next planning cycle.

### Design gate dependency on BLG-FE-22
BLG-FE-22 (Screener morning routine UX spec) is explicitly marked "before v3.2 sprint planning" in the backlog. The design gate is the correct mechanism to enforce this, but the design gate must be set as a hard prerequisite in sprint_planning_prompt.md STEP -1 to ensure it is consumed. This pattern (backlog item as design gate input) will recur with every Arc feature where the Arc 1→Arc 2 transition is visible to the user.

---

## Recommendations for Future Cycles

| # | Recommendation | Owner | Priority | Action |
|---|----------------|-------|----------|--------|
| R-01 | Add governance rule: any P3 backlog item deferred 3+ consecutive cycles must enter next release scope or receive named re-deferral from Product Owner | PMO Lead | Low | Backlog policy update |
| R-02 | Enforce OA completion before next cycle opens — PMO Lead to resolve owned OAs before post-ship closure of the following cycle | PMO Lead | Medium | Process reminder |
| R-03 | Design gate must explicitly consume "before sprint planning" backlog items — sprint_planning_prompt.md STEP -1 should check for open "before sprint planning" backlog items and block sealing if any remain unaddressed | Head of Specs Team | Low | Deferred — consider for next cycle with frontend scope |

---

// ARTEFACT_STATUS
```json
{
  "phase": "Release",
  "cycle_id": "2026-05-05__release-v3.2",
  "release": "v3.2",
  "status": "filed",
  "observations": 4,
  "recommendations": 3,
  "immediate_actions": 0,
  "deferred_actions": 0,
  "filed_utc": "2026-05-05T07:40:00Z"
}
```
