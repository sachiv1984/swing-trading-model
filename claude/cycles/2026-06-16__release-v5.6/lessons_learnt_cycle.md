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

---

## Phase 4

**Cycle:** 2026-06-16__release-v5.6
**Phase:** Delivery Verification

| # | Friction area | Observation | Action | Priority |
|---|---------------|-------------|--------|----------|
| LL-v5.6-DV-01 | Staging-deferred AC pattern (verification hygiene) | 5 staging-only ACs across 5 stories (BLG-FE-75 + BLG-OPS-66–69) all properly tracked with backlog items filed before PR open. The pattern is now well-established and verification friction is low — evidence files explicitly call out staging-deferred ACs and the corresponding backlog IDs. No process change needed. | Monitor BLG-OPS-66–69 and BLG-FE-75 at v5.7 sprint planning; confirm post-deployment measurement is scheduled. | P3 |
| LL-v5.6-DV-02 | Conditional story returned at planning (no mid-sprint disruption) | ST-03 (BLG-FE-64) returned at planning (gate 2026-06-21 not cleared) rather than mid-sprint. This is the third consecutive cycle this item has been returned at planning — consistent with LL pattern from v5.4 and v5.5. The gate date (2026-06-21) arrives 5 days after v5.6 close — ST-03 is a natural first candidate for v5.7 Sprint 1 if gate clears. | At v5.7 sprint planning: confirm gate 2026-06-21 cleared and schedule ST-03 as first priority if so. | P2 |
| LL-v5.6-DV-03 | Mixed EPIC sign-off class (no Tier 2 issues) | EPIC-01 used DoQ agent-mediated §5.3; EPIC-02 used I&O Owner + DoQ co-sign; EPIC-03 used autonomous class. Three different sign-off classes in one cycle — all accepted cleanly. The dual sign-off pattern for EPIC-02 (infrastructure owner + DoQ) is a valid pattern for backend-only stories where a domain specialist co-verifies implementable ACs. | No action — confirm this dual sign-off pattern is documented in execution_prompt as a recognised format for infrastructure EPICs. Non-blocking. | P3 |
