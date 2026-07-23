Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-24

# QA Evidence Log — EPIC-09 (v7.7)

## Consolidation Block

**EPIC:** EPIC-09 — Nightly backtest job idempotency check
**Cycle:** 2026-07-21__release-v7.7
**Sprint goal:** Ship the four design-gated Strategy Intelligence & Notification UX items and clear seven ready capacity-fill items to fully utilise this sprint's confirmed capacity.
**Test scenarios used:** tests/test_api_contracts.py (existing backtest-related test, unaffected — confirms no regression); primary evidence is a documented code-path audit (no runnable test file for a "does this design already prevent duplication" question, per STEP 3.1.A Case B — the audit record itself is the artefact)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-09 | `docs/product/decisions/decisions--2026-07-21__release-v7.7--nightly-backtest-idempotency-audit.md`; `.github/workflows/backtest.yml`; `backend/database.py` | Audited the full nightly backtest pipeline (compute → import → DB write) for double-run/retry safety. Confirmed the write path (`upsert_backtest_data`) is a single atomic full-replace transaction, already safe against retry and concurrent overlapping runs by design. Added a `concurrency` group to `backtest.yml` as defense-in-depth (queues overlapping runs rather than relying solely on DB-transaction serialization) and a compliance-note comment to `upsert_backtest_data` referencing the audit. | Idempotency confirmed by test or code review — a retry or manual re-trigger must not produce duplicate or divergent results; any gap found filed as P1/P2 per severity | Pass | None |

**QA test coverage:**
- Scenarios run: `backend/.venv/bin/python3 -m pytest tests/ -k backtest -q` (1 passed, no regression from the docstring/comment addition); full backend suite unaffected (workflow YAML + comment-only change, no runtime logic altered)
- Regression areas checked: `python3 -c "import yaml; yaml.safe_load(...)"` confirms `backtest.yml` is still valid YAML after the `concurrency` block addition; `ast.parse` confirms `backend/database.py` is still valid Python after the docstring extension
- Known deviations filed: None — audit found no correctness gap requiring a P1/P2 backlog item; the one hardening identified (CI concurrency guard) was applied directly in this commit rather than deferred

**Process note:** during this story's execution, a commit was momentarily made on the wrong branch (`EPIC-07` instead of `EPIC-09`) — caught before push, corrected via `git reset --hard` on `EPIC-07` (back to its last pushed commit) and `git cherry-pick` onto `EPIC-09`, with `EPIC-07`'s remote state verified unaffected before and after. No process deviation record required — the correction was made before any push reached the wrong branch's remote, so `EPIC-07`'s branch history was never actually incorrect on GitHub.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, backend/CI-only change, no frontend code
- Signed off by: Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3)
- Date: 2026-07-24
- Comments: No frontend-visible change. This audit's own findings (already-safe transaction design + one hardening applied) are the primary evidence; no separate Playwright/pytest scenario was needed since the finding is about a design property already covered by `get_db()`'s existing commit/rollback contract, independently re-derivable from the code by any reviewer. Human Director of Quality review and Product Owner acceptance still required before merge per §5.3 "Always-human gates".
