Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-20
Cycle: 2026-07-20__release-v7.6

# Sprint Close — 2026-07-20__release-v7.6

## Sprint Goal

Ship print/PDF export for WeeklyDigest and TradePlan (BLG-FE-119) and clear six ready backend/QA/documentation items to fully utilise this sprint's confirmed capacity.

## Items Done

| ST | EPIC | Title | Commit SHA | Spec References |
|----|------|-------|------------|------------------|
| ST-01 | EPIC-01 | Add print/PDF export action to WeeklyDigest and TradePlan | `a973bcdc` | `docs/specs/frontend/pages/weekly_digest.md`#4; `docs/specs/frontend/pages/trade_plan.md`#7c |
| ST-04 | EPIC-04 | Standardise error-response envelope across all routers | `37fdadfd` | `docs/specs/api_contracts/backend_engineering_patterns.md`#Error-response envelope conformance |
| ST-02 | EPIC-02 | Update regression suite baseline for BLG-FE-115-119 interaction surfaces | `a5837f78` | `docs/qa/regression_test_suite_baseline.md`#Part 2 |
| ST-03 | EPIC-03 | Reconcile realised P&L export against trade_plan closes | `e219b34d` | `docs/specs/pnl_export_reconciliation.md` |
| ST-05 | EPIC-05 | Build shared mock payload fixture library from openapi.yaml | `9f1c76a3` | `tests/e2e/fixtures/api-mocks.js` |
| ST-06 | EPIC-06 | Audit nightly batch jobs for idempotency risk | `d32ee3ed` | `docs/specs/nightly_batch_idempotency_audit.md` |
| ST-08 | EPIC-08 | Add standing regression suite for ticker/market input sanitisation | `b097a1ba` | `tests/test_ticker_market_sanitization_regression.py` |
| ST-07 | EPIC-07 | Add Claude API monthly cost summary (reframed) | `c74a0d08` | `docs/design/.../consolidated-ai-cost-view/ux_spec.md`#7; `docs/specs/frontend/pages/settings.md`#6; `docs/specs/api_contracts/ai_endpoints.md`#GET /ai/monthly-cost |

All 8 EPICs merged to `main` via PR (#1028, #1029, #1030, #1031, #1032, #1033, #1034, #1035 respectively).

## Items Returned to Backlog

None. All 8 stories delivered within the sprint.

## Items Delegated and Outstanding

None. No story used `delegated_backend`/`delegated_frontend` classification this sprint; no `delegation_log.md` was created (STEP 5.0 vacuous — `delegated_items: []`).

## QA Evidence Logs Produced

`qa_evidence_EPIC-01.md` through `qa_evidence_EPIC-08.md` (all 8 present). Sign-off methods:
- Autonomous class (BLG-GOV-19): EPIC-02, EPIC-03, EPIC-04, EPIC-05, EPIC-06, EPIC-08
- Agent-mediated Director of Quality (§5.3): EPIC-01, EPIC-07 (both introduced frontend-visible changes, disqualifying autonomous class per criterion 3)

## Process Notes

- **ESC-EXEC-20260720-01** (EPIC-07, Quality trigger): during execution of ST-07, tracing `backend/services/gemini_service.py` found the story's premise — that Gemini and Claude are two separate cost-generating AI providers — was factually incorrect; no Gemini integration exists anywhere in this codebase. Escalated rather than silently implemented or silently redesigned. Product Owner resolved in-session (option (a): single-provider reframe). ST-07 was reclassified `autonomous` → `delegated_decision` (escalated) → `autonomous` (resolved) within the same sprint. Full resolution: `claude/cycles/2026-07-20__release-v7.6/execution_escalations.md`.
- **Agent-mediated DoQ review caught 2 real issues on EPIC-07's first review pass** (missing shared Playwright fixture on a branch that hadn't merged `main` since EPIC-05 landed it; one stale "Gemini + Claude" spec bullet that survived the §6 reframe edit) — both fixed and re-verified before sign-off cleared. Documented in `qa_evidence_EPIC-07.md`.
- **Post-sign-off CI gate finding on EPIC-07:** the "API Performance Baseline Drift Detection (ST-12)" hard gate failed on PR #1035 — `docs/reference/openapi.yaml` gained the `/ai/monthly-cost` path but the companion `docs/ops/api_performance_baseline.md` entry was missed in the signed-off commit. Fixed in a follow-up commit (§29 registration entry, following the established §26–28 pattern), re-verified CI green, then merged. This was outside the DoQ review's given scope (the review prompt did not ask it to check CI gate results) — noted as a process gap for future agent-mediated reviews to also confirm CI status, not just re-run tests locally.
- **Cross-EPIC merge conflicts:** every EPIC after the first encountered a conflict in `execution_state.json` (top-level `completed_items` array) against the prior EPIC's already-merged state, resolved per `CLAUDE.md §8` (union of completed items) for all 7 subsequent merges (EPIC-04, EPIC-02, EPIC-03, EPIC-05, EPIC-06, EPIC-08, EPIC-07). `backlog.md`'s `Last Updated` header also conflicted on the EPIC-02/EPIC-04 merge (both EPICs filed new backlog items in the same session) — resolved by combining both sessions' entries, no items lost or duplicated (verified: BLG-BE-68, BLG-BE-69, BLG-QA-116 all present exactly once post-merge).
- **PR review/approval gap:** none of the 8 PRs received a formal GitHub review before merge — `reviewDecision: REVIEW_REQUIRED` on all. Product Owner acceptance was instead recorded as explicit in-session chat authorization (a comment posted on each PR referencing this), and merges used `gh pr merge --admin` to bypass the branch-protection required-review rule. This is a deviation from the normal PR-review flow, authorized directly by the Product Owner (repository owner) in this session rather than via a GitHub-native approving review.

## Deviations Filed This Sprint

None (code-vs-spec sense — no `/dev-file` DEV-* records filed). **EPIC-07 design-artefact deviation** (not a code deviation): the original UX spec's premise was factually wrong; documented as `docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md` v1.1 §7 addendum, per `document_lifecycle_guide.md` §9's treatment of design-artefact corrections. Severity: not applicable (no P0–P3 priority assigned — this is a premise correction, not a code-vs-spec conformance gap).

## Open Escalations

None. `ESC-EXEC-20260720-01` raised and resolved within this sprint (Disposition: Resolved).

## Net Outcome vs Sprint Goal

Both halves of the sprint goal achieved: print/PDF export shipped (EPIC-01), and all six additional ready backend/QA/documentation items cleared (EPIC-02 through EPIC-06, EPIC-08), plus EPIC-07 delivered in corrected (reframed) form after a genuine premise defect was caught and resolved rather than shipped silently. 8 of 8 sprint stories done, 0 returned to backlog, 0 open escalations at close.

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
