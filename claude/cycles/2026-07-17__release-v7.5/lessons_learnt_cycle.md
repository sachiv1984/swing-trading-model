Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-20
Cycle: 2026-07-17__release-v7.5

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-17__release-v7.5
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-20
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| All four EPICs registered new endpoints in the same set of shared files (`backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js`, `docs/specs/data_model.md`, `docs/ops/api_performance_baseline.md`, `docs/reference/openapi.yaml`) — every EPIC after the first hit a guaranteed cross-EPIC merge conflict against main, requiring two full CLAUDE.md §8 resolution passes this sprint (EPIC-03 vs EPIC-02, then EPIC-04 vs EPIC-02+EPIC-03) | Phase 3 | C | defer | Process worked as designed (CLAUDE.md §8 resolved both conflicts cleanly with no data loss), but the underlying pattern is now recurrent across cycles (also seen in 2026-07-10__release-v6.9's sprint_close.md). Consider a structural fix — e.g. splitting the endpoint test registry and performance baseline into per-EPIC append-only manifest files aggregated at build/CI time — to remove the shared-file collision surface entirely, rather than continuing to resolve it manually each multi-EPIC sprint. | Head of Engineering | next roadmap review |
| A real regression was caught during EPIC-04's own DoQ verification pass: pre-existing `tests/e2e/net-r-trade-history.spec.js` crashed because the newly-mounted components called `.map()` on `json.data \|\| []`, which does not guard against a non-array truthy `data` value returned by the test suite's generic catch-all mock. The same weak-guard pattern (`json.data \|\| []` instead of `Array.isArray(json.data) ? json.data : []`) was independently reused across at least two of this sprint's four EPICs before being fixed in EPIC-04 | Phase 3 | D | defer | Not fixed as a repo-wide sweep this sprint (out of scope — only the two call sites causing the actual failure were patched). Recommend a coding-standard note (or lint rule) requiring `Array.isArray(...)` guards on any `.map()`/`.filter()` call over a JSON API response field, to catch this class of bug before Playwright does. | Head of Engineering | next roadmap review |

**Recurrence Notes:**
The shared-registration-file conflict pattern (friction item 1) recurred from the 2026-07-10__release-v6.9 cycle, where the same file set (endpoint test registry, performance baseline, data model) produced an analogous EPIC-02-vs-EPIC-01 conflict, resolved the same way. This is the second consecutive multi-EPIC sprint to hit it — worth escalating from "resolve each time" to "consider removing the collision surface," per the action column above.
