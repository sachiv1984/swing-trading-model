**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-27
**Cycle:** 2026-07-24__release-v7.8

---

# Sprint Close — 2026-07-24__release-v7.8

## Sprint Goal

Ship all 12 v7.8 EPICs — the release/spend-visibility feature set (in-app "what's new" panel, Telegram release digest, monthly P&L CSV export, AI spend trend chart) and the overdue engineering-hardening set (notification accessibility audit, dark-mode contrast audit, API key rotation cadence, endpoint rate-limiting review, shared retry/backoff pattern, flaky-test quarantine process, pilot contract tests, API-contract heading-level CI lint) — with every acceptance criterion met and QA sign-off recorded for each EPIC.

## Items Done

| EPIC | Story | Title | Commit SHA | PR | Spec References |
|------|-------|-------|-----------|-----|-----------------|
| EPIC-04 | ST-04 | Consolidated dark-mode contrast audit across shipped pages | `95ac48cbe676a4db9354d167135aeffe9a85b1a8` | #1077 | `docs/design/2026-07-24__release-v7.8/base44-dark-mode-contrast-audit/decision_record.md`; `docs/specs/frontend/design_system.md` |
| EPIC-03 | ST-03 | Contrast/focus-state accessibility pass on v7.7 notification UX | `5afe911734df8e91915bd72388df5ae3d046381d` | #1078 | `docs/design/2026-07-24__release-v7.8/notification-accessibility-audit/decision_record.md` |
| EPIC-09 | ST-09 | Extract shared retry/backoff decorator and migrate highest-traffic call site | `a3db2612` | #1070 | `backend/utils/retry.py` |
| EPIC-07 | ST-07 | Define rotation-and-audit schedule for all external API keys | `7fee996e` | #1071 | `docs/ops/api_key_rotation_and_audit_schedule.md` |
| EPIC-08 | ST-08 | Identify and remediate endpoints with no documented rate limit | `5115afe1` | #1072 | `docs/security/rate_limit_audit_2026-07-26.md` |
| EPIC-12 | ST-12 | Add CI lint step for API contract heading-level compliance | `1cd59c2e` | #1073 | `.github/workflows/openapi-drift.yml`; `scripts/lint_api_contract_headings.py` |
| EPIC-10 | ST-10 | Define and apply flaky-test quarantine mechanism | `68fba626` | #1074 | `docs/testing/flaky_test_quarantine_process.md` |
| EPIC-02 | ST-02 | Send Telegram digest of shipped items on post-ship closure | `a41757e3` | #1075 | `claude/system/post_ship_closure.md#STEP 1.5`; `backend/services/changelog_digest_service.py` |
| EPIC-01 | ST-01 | Build in-app "what's new" panel sourced from changelog.md | `4a20acaa` | #1079 | `docs/specs/frontend/pages/dashboard.md#6A`; `docs/specs/api_contracts/changelog_endpoints.md`; `docs/specs/frontend/design_system.md` |
| EPIC-05 | ST-05 | Add monthly CSV export option alongside existing tax-year export | `e7bedcf4` | #1080 | `docs/specs/api_contracts/reports_endpoints.md#CSV Export`; `docs/specs/frontend/pages/reports.md` |
| EPIC-06 | ST-06 | Add per-cycle AI spend trend chart to AI Usage & Costs view | `36147c75` | #1081 | `docs/specs/frontend/pages/settings.md#6a`; `docs/specs/api_contracts/ai_endpoints.md#GET /ai/spend-trend` |
| EPIC-11 | ST-11 | Add pilot contract tests for 3 highest-traffic endpoints | `65844970` | #1076 | `docs/testing/pilot_contract_test_approach.md`; `docs/specs/api_contracts/position_endpoints.md`; `docs/specs/api_contracts/trade_endpoints.md`; `docs/specs/api_contracts/portfolio_endpoints.md` |

All 12 EPICs merged to `main` (PRs #1070–#1081), merge-committed by the human Product Owner/repo owner (explicit authorization given for the final merge action per this cycle's session record — QA sign-off/review content itself was agent-mediated per `execution_prompt.md` §5.3, but the merge click and PR acceptance remained a human action throughout, consistent with the "engine may not self-approve a merge" rule). All merges were preceded by green CI runs (`quality_gate.yml` and its constituent jobs).

## Items Returned to Backlog

None — all 12 in-scope ST items reached `done`/`merged` within the sprint.

## Items Delegated and Outstanding

None this sprint via the formal delegation-log mechanism (`delegation_log.md` was not created — no `delegated_backend`/`delegated_frontend`/`delegated_qa` items arose). One story, ST-11 (EPIC-11), was classified `delegated_decision` at sprint planning (RISK-03 — no telemetry-backed pilot-endpoint ranking existed) and escalated as `ESC-EXEC-20260727-01` rather than logged via the delegation-log path (per shared_standards.md, decision-type delegations route through the escalation mechanism). Resolved same-day via agent-mediated Head of Engineering review — see Process Notes.

## QA Evidence Logs Produced

`qa_evidence_EPIC-01.md` through `qa_evidence_EPIC-12.md` (12 files, one per EPIC). All sign-off blocks have non-blank `Date:` fields, confirmed at STEP 5.1's QA Evidence Persistence Check. Sign-off methods used:
- **Standard human Director of Quality sign-off** (agent-mediated review + human-confirmed sign-off content, per this cycle's explicit attribution convention): EPIC-01, EPIC-03, EPIC-04, EPIC-05, EPIC-06 — all frontend-visible, so BLG-GOV-19 autonomous class was unavailable (BLG-GOV-135 detection rule).
- **Autonomous class (BLG-GOV-19)**: EPIC-02, EPIC-07, EPIC-08, EPIC-09, EPIC-10, EPIC-11, EPIC-12 — no frontend-visible change, all AC verifiable by code/test review alone.
- **Story-level domain-authority sign-offs recorded separately per BLG-GOV-14** (in addition to the EPIC-level DoQ/autonomous-class block): EPIC-01 (Infrastructure & Operations Owner, `api_performance_baseline.md` §30 — caught and corrected a version/Document-History desync on first review pass); EPIC-06 (Infrastructure & Operations Owner, §31 — added post-PR-open after the API Performance Baseline Drift Detection CI gate caught a missing registration); EPIC-07 (Cybersecurity & Trust Lead — verified both "no credential" claims against the code before approving); EPIC-08 (Cybersecurity & Trust Lead — first review round caught a real endpoint-count arithmetic error, 44/126 claimed vs 46/128 actual, corrected then re-approved); EPIC-11 (Head of Engineering — RISK-03 pilot-endpoint selection).

## Process Notes

- **Real production bug found and fixed via actual test execution (EPIC-01):** `WhatsNewCard.js` read `data?.data`, but `doFetch()` already unwraps the `{status, data}` envelope — the double-unwrap meant the card would always have rendered the empty state in production regardless of real changelog content. Found by running `tests/e2e/whats-new-panel.spec.js` against a real browser (3/5 scenarios failed), not by reading the test file. Fixed (one-line change, commit `453e1d23`), re-verified all 5 pass.
- **Cross-test-isolation bug (EPIC-06):** an early draft of `tests/test_ai_spend_trend_service.py` copied an unnecessary `sys.modules.pop("database", None)` from an existing precedent, which evicted conftest's session-scoped DB stub and broke a different, alphabetically-later test file when the full suite ran together. Caught by running the full suite (not just the new file in isolation), fixed by removing the unneeded pop.
- **Same-day release date-tie bug (EPIC-06):** `ai_spend_trend_service.py`'s naive `cycles.sort(key=...)` left same-day releases (real case: v7.5/v7.6 both 2026-07-20) in ambiguous order. Fixed by reversing the parsed (newest-first) list before the stable date sort, so document order resolves ties correctly. Caught via a dedicated test using the real dates.
- **Playwright execution in an unsupported-OS sandbox:** this session's sandbox OS (ubuntu26.04) is unsupported by the installed Playwright's bundled-browser download. Rather than leaving Playwright coverage as "written but not executed," the system's pre-installed `snap` Chromium was used via a local, uncommitted `executablePath` config override (never committed to the repo) to actually run every new/modified Playwright spec (EPIC-01, EPIC-03, EPIC-04, EPIC-05, EPIC-06) against a real browser before sign-off.
- **RISK-03 resolution (EPIC-11):** `ESC-EXEC-20260727-01` (pilot-endpoint selection for the contract-test pilot) resolved via agent-mediated Head of Engineering review. Confirmed pilot endpoints: `GET /positions`, `GET /trades`, `GET /portfolio`. The named "dashboard" candidate did not map to a single endpoint — `DashboardHome.js` composes ~12 independent queries, 2 of which already duplicate the positions/trades candidates — resolved to `GET /portfolio` as the genuinely distinct, dashboard-representative, every-session-load endpoint. Full reasoning in `execution_escalations.md`. ST-11 reclassified `delegated_decision` → `autonomous` and implemented same day.
- **API Performance Baseline Drift Detection gap (EPIC-06):** `GET /ai/spend-trend` was added to `openapi.yaml` without its required `docs/ops/api_performance_baseline.md` registration entry — the LL-v7.6-P3-01 pre-PR advisory was missed at implementation time. Caught by CI on the open PR (not pre-empted at PR-open), fixed by adding §31 (estimated latency derived from the comparable `GET /ai/monthly-cost` baseline) with agent-mediated Infrastructure & Operations Owner sign-off.
- **Endpoint-count collision across independently-cut branches (EPIC-06):** both this branch and the already-merged EPIC-01 independently bumped `SystemStatus.js`'s endpoint-count fallback and the `SC-SS-01b` Playwright assertion from 99→100 for their own new endpoint. Git's merge could not detect this as a conflict because both branches happened to write the identical literal `'100'`, so it auto-merged "cleanly" onto a semantically wrong value. Caught by AST-counting the real total in `backend/routers/test.py` post-merge (101 — both new endpoints present) and manually correcting the fallback constant and Playwright assertion to 101 in both files.
- **Cross-EPIC `execution_state.json`/shared-file conflict resolution (CLAUDE.md §8), all 12 branches:** every EPIC branch was cut before this cycle's sprint execution had progressed on `main`, so each carried an independently-diverging snapshot of `execution_state.json`. As each EPIC merged, `main` became the authoritative combined ledger; every remaining branch was resolved by taking `main`'s version wholesale and re-applying only that branch's own more-current `pr_number`/`pr_status` fields (never reverting a story from `done`/`merged` to an earlier state). Two branches also carried genuine content conflicts beyond the ledger file: EPIC-05 and EPIC-06 both required combining independently-added `docs/specs/api_contracts/api_changelog.md` entries under the same `v7.8.0` section (union, no content dropped, per CLAUDE.md §8). Conflict-resolution commits: `ae0edb69` (EPIC-04), `1e46448c` (EPIC-03), `54348e5d` (EPIC-09), `cf673d92` (EPIC-07), `0f2ae7c8` (EPIC-08), `f97bcc30` (EPIC-12), `f38d5353` (EPIC-10), `d9f1576b` (EPIC-02), `781943db` (EPIC-01), `584d94e0` (EPIC-05), `be3673e0` (EPIC-06). EPIC-11's branch required no conflict resolution (still mergeable against `main` at merge time).
- **Transient CI infrastructure failure (EPIC-03):** one `Pytest Phase B (integration — real Postgres service)` run failed with a Docker Hub image-pull timeout (`registry-1.docker.io` connection timeout) — not a real test failure. Confirmed by a parallel run on the same PR passing, and by re-running the specific failed job, which then passed.

## Deviations Filed This Sprint

None. Every `done` ST item's deviation check (STEP 3.1.A step 10) found no divergence between implementation and canonical spec. One structural correction was made at sprint close (not a deviation): EPIC-11/ST-11's `deviations_filed` flag was `false` with no deviation record present anywhere (spec or `qa_evidence_EPIC-11.md`, which explicitly states "Known deviations filed: None") — corrected to `true` per STEP 5.1's auto-correction rule.

Several EPICs found and fixed genuine bugs during implementation or CI (WhatsNewCard double-unwrap, EPIC-06's test-isolation bug, EPIC-06's same-day-tie bug, the endpoint-count collision, the missing API performance baseline registration) — these are implementation/test-quality corrections caught before or during merge, not spec-vs-implementation deviations, and are documented in the relevant `qa_evidence_EPIC-xx.md` files and the Process Notes above rather than as `/dev-file` DEV-* records.

## Open Escalations

None remaining. One escalation was raised and resolved within this sprint: `ESC-EXEC-20260727-01` (EPIC-11/ST-11, RISK-03 pilot-endpoint selection) — raised 2026-07-27T01:15:00Z, resolved 2026-07-27 via agent-mediated Head of Engineering review (see Process Notes). `execution_state.json.open_escalations` is empty.

## Net Outcome vs Sprint Goal

Goal fully met. All 12 v7.8 EPICs shipped: the 4-item release/spend-visibility set (in-app "what's new" panel, Telegram release digest, monthly P&L CSV export, AI spend trend chart) and the 8-item engineering-hardening set (notification accessibility audit, dark-mode contrast audit, API key rotation cadence, endpoint rate-limiting review, shared retry/backoff pattern, flaky-test quarantine process, pilot contract tests, API-contract heading-level CI lint). 12/12 ST items done and merged; 0 returned to backlog; 0 outstanding delegations; 0 open escalations. Two real production/process bugs (WhatsNewCard double-unwrap, endpoint-count collision) were caught before or shortly after merge via genuine test execution and CI, not left latent.

## System Status Report Corrections

Checked per STEP 5.1.B (BLG-GOV-15): no distinct SC-* scenario count cells table exists in `docs/System_status_report.md` to check against this sprint's additions (the document's structure is per-sprint capability tables, not a standing scenario-count table). `execution_prompt.md`'s current version (3.59) is not referenced anywhere in the SSR's historical log rows (each row documents the version in effect at that past sprint, not a live pointer) — no correction needed, consistent with the same finding at the prior (`2026-07-21__release-v7.7`) sprint close.

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
