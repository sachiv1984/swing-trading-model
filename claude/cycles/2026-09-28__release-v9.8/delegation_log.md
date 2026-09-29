Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-29

---

## DEL-20260929-01

- **ST Item:** ST-15 — Mutation-testing pilot on the sizing calculator and stop ratchet
- **EPIC:** EPIC-03
- **Classification:** delegated_qa
- **Assigned to:** QA Lead
- **GitHub Issue:** #1818
- **Branch:** exec/2026-09-28__release-v9.8/EPIC-03
- **Delegated at:** 2026-09-29T00:00:00Z
- **What is needed:** The engine's own investigation (`docs/testing/mutation_testing_pilot_sizing_and_stop_ratchet.md`) found a structural, environmental blocker in `mutmut` 3.x's `sys.path` assumptions vs. this repo's `tests/conftest.py` convention — not a quick fix, and resolving it (BLG-QA-198) requires a decision on which of two fix options to take, one of which (option b) affects the whole test suite's collection path. QA Lead/Director of Quality to: (1) rule on BLG-QA-198's fix option, (2) once applied, re-run the scoped mutmut config already documented in the investigation doc and record the resulting mutation score + survivor triage in that same document.
- **Unblock criteria:** `BLG-QA-198` resolved (either fix option applied) and a real mutation score recorded for `backend/services/sizing_service.py` and `backend/utils/calculations.py`.
- **Commit format required:** `[EPIC-03][ST-15] <description>` pushed to `exec/2026-09-28__release-v9.8/EPIC-03`
- **Status:** Pending
