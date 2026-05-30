**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-05-30__release-v4.5
**Phase:** Release Planning
**Filed:** 2026-05-30

---

# Lessons Learnt — Release Planning v4.5

## Planning Observations

### Observation 1 — Roadmap gap at planning invocation
v4.5 was absent from the roadmap when `plan release --version v4.5` was invoked. Preflight -1.2 would have halted per strict mode. User authorized annotation to progress. Annotation added in same session before planning proceeded.

**Implication:** v4.5 was a logical next release (v4.4 OA closure record explicitly targeted v4.5, post-ship next_release was TBD). The rebalance engine should set `next_release` to the planned version label after determining the release scope. Currently `next_release=TBD` leaves the roadmap ambiguous at planning time.

**Action:** Consider adding roadmap_prompt.md advisory — after DL decision, set `next_release` in `.claude_current_state.json` to the projected next version label if determinable. Low priority; advisory not a hard gate.

**Disposition:** defer — not a hard pattern change.

### Observation 2 — Resolved backlog items (BLG-GOV-30/31/55) still open
Three P1 backlog items confirmed resolved per prompt_change_log.md entries but still active in backlog.md (not archived). These appeared as scope candidates and had to be triaged manually at planning time. This is the second time resolved items have appeared as scope candidates (same pattern noted previously).

**Implication:** `groom backlog` should run after each cycle that resolves backlog items via prompt_change_log.md entries, not just after sprint close. Or, the groom backlog engine could scan prompt_change_log.md entries against open backlog items as part of its sweep.

**Action:** defer — the groom backlog engine improvement is BLG-type work. No immediate action required.

**Disposition:** defer — not urgent.

### Observation 3 — EPIC-03 conditional gate pattern working well
The conditional EPIC (EPIC-03) pattern with explicit PO gate confirmation requirement continues to work well for gated features. v4.4 used the same pattern for SI-02 pre-planning; v4.5 extends it for SI-02 spec completion. Gate is documented in both the backlog slice and cycle_summary. Sprint planning engine will enforce gate check.

**Disposition:** positive confirmation — no action.

---

## Action Summary

### Action-now (0)

None.

### Deferred (1)

| # | Action | Owner | Target |
|---|--------|-------|--------|
| 1 | Consider roadmap_prompt.md advisory to set next_release after DL decision | Head of Specs Team | TBD (low priority) |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle": "2026-05-30__release-v4.5",
  "status": "complete",
  "action_now_count": 0,
  "deferred_count": 1,
  "escalated_count": 0
}
