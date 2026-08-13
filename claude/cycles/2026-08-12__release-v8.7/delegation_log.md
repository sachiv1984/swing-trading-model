Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-13

---

## DEL-20260813-01

- **ST Item:** ST-07 — Staging verification of ST-03's (v8.6) trade-plan-linkage enforcement, and legacy orphaned-row audit
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering; Data Model, Domain & Schema Owner
- **GitHub Issue:** #1370
- **Branch:** exec/2026-08-12__release-v8.7/EPIC-02
- **Delegated at:** 2026-08-13T08:15:00Z
- **What is needed:** Live staging/production Postgres access to (a) confirm `POST /portfolio/position` links a trade plan by default via the "Start Trade from Plan" flow, (b) run `SELECT ... WHERE status='active' AND position_id IS NULL` against `trade_plans` for the 11 known legacy rows, (c) confirm the DS-12 CHECK constraint (`trade_plans_active_requires_position_check`) is present and `NOT VALID` on the live table (query in `docs/specs/data_model.md` §DS-12 Verification). Layer: database/infrastructure (live query access), not code.
- **Spec reference:** `docs/specs/data_model.md#DS-12` (Verification note, ST-07, EPIC-02, v8.7)
- **Unblock criteria:** Genuine staging/production database credentials or dashboard read access become available in-session or in a future session.
- **Commit format required:** `[EPIC-02][ST-07] <description>` pushed to `exec/2026-08-12__release-v8.7/EPIC-02`
- **Status:** Unblocked

**Unblocked in-session — best-available-proxy execution per Product Owner (agent-mediated) authority recorded at sprint planning (`sprint_planning_notes.md` Pre-sprint Planning Required Decisions, 2026-08-12), same session as delegation.** Staging/live-Postgres access confirmed still unavailable in this sandbox (re-checked 2026-08-13 — no `DATABASE_URL`, no `psql`, no outbound reachability, unchanged since v8.6). AC-01 and AC-03 verified via code-path/test-suite and startup-invocation proxy evidence instead — see `docs/specs/data_model.md#DS-12` Verification note and `qa_evidence_EPIC-02.md`. AC-02 (legacy-row live query) is **not proxyable** and remains a disclosed residual gap, not silently treated as met; the v8.6 P0-escalation condition (any of the 11 known rows found `status='active'` escalates immediately, independent of this story's timeline) carries forward unchanged.
- Sign-off step: Head of Engineering + Data Model & Domain Schema Owner sign-off cleared (agent-mediated, §5.3) — 2026-08-13, recorded in `docs/specs/data_model.md#DS-12`.
- Push step: commit_sha recorded in `execution_state.json` for ST-07 at push time.
