Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-06-16
Cycle: 2026-06-16__release-v5.6

---

# Lessons Learnt — 2026-06-16__release-v5.6

## Phase 3 — 2026-06-16__release-v5.6

| # | Friction area | Observation | Action | Priority |
|---|---------------|-------------|--------|----------|
| LL-v5.6-EX-01 | Staging-only AC pattern (performance) | All 4 EPIC-02 stories had staging-only ACs for production latency re-measurement. The engine handled these well (backlog items BLG-OPS-66–69 filed, implementable ACs completed), but delivery verification will need to confirm the staging items are on track. This pattern (performance fix + staging verification deferred) is now established — no further process change needed. | Monitor BLG-OPS-66–69 at v5.7 sprint planning; assess if any should be carried forward as firm stories. | P3 |
| LL-v5.6-EX-02 | Cross-session EPIC merge detection | EPIC-01 was merged between sessions. On resume, the engine correctly detected `state: MERGED` via `gh pr view` and synced pr_status before proceeding to EPIC-02. The LL-v3.9-P3-1 merge gate state sync protocol worked as intended. | No action — confirm this pattern in future cycles with >2 EPICs to keep protocol validated. | P3 |
| LL-v5.6-EX-03 | Circular import risk (lazy import pattern) | ST-07 research cache invalidation required `invalidate_research_cache()` to be called from `screener.py`, but `screener` is imported before `research` in `main.py`. Solved with lazy import inside the background task function. This is the canonical pattern for cross-router hooks in this codebase. | Document lazy-import pattern as standard for cross-router hooks in backend engineering patterns. Non-blocking. | P3 |

---

*No process improvements applied in-session this cycle — no template or prompt changes triggered by friction observations.*
