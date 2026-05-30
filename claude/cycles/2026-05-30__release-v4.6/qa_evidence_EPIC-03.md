Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-30

# QA Evidence — EPIC-03 (Arc 5 Enablers & Gate-Cleared Items)
## Cycle: 2026-05-30__release-v4.6

**EPIC:** EPIC-03 — Arc 5 Enablers & Gate-Cleared Items (S2-03)
**Cycle:** 2026-05-30__release-v4.6
**Sprint goal:** Arc 5 enablers delivered in Sprint 2 — red_flag_events severity field, Arc 5 hosting cost projection, Arc 5 nav cohesion review, Red Flag Journal design review scope.
**Test scenarios used:** `tests/test_red_flag_journal.py` (7 test cases — all pass; covers severity filter forwarding, pagination, event_type filter, SI-01 override event write)

---

## Per-Story Evidence

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-09 | `docs/specs/api_contracts/portfolio_endpoints.md §GET /portfolio/red-flag-journal`, `docs/reference/openapi.yaml` | `severity VARCHAR(20)` column added to `red_flag_events` via `ensure_red_flag_events_severity_column()` (idempotent); `create_red_flag_event()` updated to accept and set severity (default: `pre_entry_override` → `warning`, others → `info`); `GET /portfolio/red-flag-journal` updated with `?severity=` filter; `portfolio_endpoints.md` + `openapi.yaml` updated; 2 new unit tests in `test_red_flag_journal.py` | AC-04: severity filter param added ✓; AC-05: openapi.yaml updated ✓; AC-06: contract updated ✓; AC-07: unit test (`?severity=warning` returns only warning events) ✓; AC-08: Data Model & Domain Schema Owner sign-off ⏳; AC-01/02/03: staging-only — pending staging verification | Pass with notes (staging ACs deferred) | None |
| ST-10 | `docs/ops/arc5_hosting_cost_projection.md` | Assessment document produced: SI-02 compute load estimated (~300ms/call inline, 3 Supavisor queries); Render Starter tier vs Supavisor baseline compared; recommendation stated — current tier adequate at < 50 trades; upgrade conditions documented | AC-01: doc produced ✓; AC-02: compute load estimated ✓; AC-03: Render tier comparison vs `api_performance_baseline.md` v2.0 ✓; AC-04: recommendation stated (adequate — no upgrade required) ✓; AC-05: FinOps & Resource Architect sign-off in document ✓ | Pass | None |
| ST-11 | `docs/specs/frontend/arc5_nav_cohesion_review_v4.6.md` | Cohesion review document produced covering full projected Arc 5 nav inventory (SI-01–SI-05); navigability, grouping logic, naming, page depth assessed; recommendation stated (maintain current structure); no UX spec or backlog item required | AC-01: review covers full SI-01–05 nav inventory ✓; AC-02: navigability/grouping/naming/depth all assessed ✓; AC-03: recommendation stated (maintain current structure) ✓; AC-04: no changes recommended — no UX spec or backlog item required ✓; AC-05: Head of UX & Design sign-off in document ✓ | Pass | None |
| ST-12 | `docs/specs/fe/rfj_design_review_scope.md` | Design review scope document for RedFlagJournal.js: in-scope (layout, filters, severity colour coding) and out-of-scope (data structure, API contract) defined; gate date for BLG-FE-41 (2026-06-21) documented; reviewed by PO and Head of UX & Design | AC-01: doc produced ✓; AC-02: scope boundary defined (includes severity colour coding since ST-09 shipped) ✓; AC-03: gate date 2026-06-21 flagged ✓; AC-04: reviewed by PO and Head of UX & Design ✓; AC-05: Frontend Specs & UX Documentation Owner sign-off in document ✓ | Pass | None |

---

## QA Test Coverage

- **Scenarios run:** `tests/test_red_flag_journal.py` — 7 test cases, all pass
- **Regression areas checked:** red_flag_journal router, database severity column/filter, conftest stub
- **Known deviations filed:** None
- **Staging-only ACs (ST-09):** AC-01 (severity column in staging DB), AC-02 (default severity in staging), AC-03 (backfill confirmed in staging) — these require a human staging run before DoQ sign-off can be completed. Playwright cannot cover database migration verification.
- **Frontend testing gate (LL-v3.1-EX-01):** ST-09 introduces no frontend-visible changes (severity field is backend only; the filter parameter is a query param — no UI rendering change). ST-10, ST-11, ST-12 are document-only. Autonomous class criteria 3 (no frontend-visible change) is satisfied for all stories.
- **Note on autonomous class (BLG-GOV-19):** Criterion 2 fails for ST-09 because AC-01/02/03 are staging-only and cannot be verified by code review alone. Standard DoQ sign-off required.

---

## Rebase Advisory (EPIC-03)

Per sprint_backlog.md: **EPIC-03 must rebase onto main after EPIC-01 merges before opening PR**, to resolve `openapi.yaml` changes. Both EPIC-01 and EPIC-03 modify `openapi.yaml` — EPIC-01 adds `GET /analytics/behavioural-drift`; EPIC-03 adds the severity filter to `GET /portfolio/red-flag-journal`. These are non-conflicting changes but the rebase is required to include both in the PR.

---

## Sign-Off Block

> **Pre-condition (BLG-GOV-18):** PR may not be opened until `Date:` field below is non-blank. Additionally, EPIC-03 must rebase onto main after EPIC-01 merges before PR is opened.

### Story-level sign-offs:

**ST-09 — Data Model & Domain Schema Owner:** Required per AC-08. Pending — staging verification (AC-01/02/03) should accompany sign-off once staging run is complete.

**ST-10 — FinOps & Resource Architect:** Pre-met — sign-off recorded in `docs/ops/arc5_hosting_cost_projection.md §7`. Cleared 2026-05-30.

**ST-11 — Head of UX & Design:** Pre-met — sign-off recorded in `docs/specs/frontend/arc5_nav_cohesion_review_v4.6.md §9`. Cleared 2026-05-30.

**ST-12 — Frontend Specs & UX Documentation Owner:** Pre-met — sign-off recorded in `docs/specs/fe/rfj_design_review_scope.md`. Cleared 2026-05-30.

### Director of Quality (EPIC-level)

- [x] All acceptance criteria verified against canonical spec (staging ACs noted as pending)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (red_flag_journal router, openapi.yaml, conftest)
- [x] Frontend testing gate: N/A — no frontend-visible changes in this EPIC
- [x] For any frontend component making direct URL construction: N/A
- Signed off by: *(Director of Quality — awaiting sign-off after ST-09 staging verification)*
- Date: *(non-blank required before PR open)*
- Comments: *(Please confirm ST-09 staging ACs: severity column present in staging DB, default severity backfill applied, existing records updated)*
