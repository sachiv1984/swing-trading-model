Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-10

---

## Consolidation Block

**EPIC:** EPIC-03 — Operations & Cost Monitoring Debt
**Cycle:** 2026-09-09__release-v9.3
**Sprint goal:** Clear a full-capacity, cross-category slate of 27 debt items — backend reliability/correctness, QA/test infrastructure, operations/cost monitoring, spec/documentation, and governance-process/security — exhausting the confirmed ~24–28 day capacity band at 27.50 days, with zero P1/P2 debt items deferred on capacity grounds this cycle.
**Test scenarios used:** `tests/test_cost_monitoring.py` (30 tests: database functions, Alpaca instrumentation, research session logging, all 4 new endpoints)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-11 | `docs/specs/api_contracts/ops_endpoints.md#GET /ops/alpaca-call-report`; `backend/database.py#api_call_log` | `api_call_log` reference instrumentation table + `log_api_call()`; Alpaca call-count logging in `get_ohlcv_bars()`; `GET /ops/alpaca-call-report` daily/weekly aggregate | Alpaca API call count logged per endpoint per run; daily/weekly aggregate report computable; sequenced first as reference pattern; I&O Owner sign-off | Pass | None |
| ST-12 | `docs/specs/api_contracts/ops_endpoints.md#GET /ops/research-session-report` | Per-session (UUID) logging of `GET /research/{ticker}`'s 4 external calls, reusing ST-11's `api_call_log`; `GET /ops/research-session-report` with baseline + >2x-baseline anomaly flagging | External call count logged per session; weekly cost-per-session baseline computable; anomaly detection >2x baseline; reuses ST-11's logging approach; I&O Owner sign-off | Pass | None |
| ST-13 | `docs/ops/ai_audit_log_retention_policy.md` | Retention windows defined (gemini_audit_log 90 days unchanged/now-enforced; claude_audit_log 730 days new); `purge_claude_audit_log_older_than_730_days()`; `POST /ops/purge-audit-logs`; wired into `daily-snapshot.yml` | Retention window + archival/deletion procedure defined for both tables; first cleanup pass executed or explicitly deferred with rationale | Pass | None (first cleanup pass explicitly deferred — no live DB in this environment; mechanism fully implemented, unit-tested, and scheduled to run automatically on next deploy, per the AC's own "or explicitly deferred with rationale" clause) |
| ST-14 | `docs/specs/api_contracts/ai_endpoints.md#GET /ai/monthly-cost-by-feature` | `get_monthly_claude_cost_by_feature()` (GROUP BY endpoint, current month); `GET /ai/monthly-cost-by-feature`; tag taxonomy documented and independently verified against every actual call site | Cost-tracking records tagged by feature; per-feature monthly breakdown available; reuses ST-11's logging approach where applicable | Pass | None |
| ST-15 | `docs/ops/ci_pipeline_baseline.md#9. Shard Count Increase 4→8 — Before/After Evidence` | `playwright-e2e` shard count 4→8 in `playwright.yml` | Independent CI test jobs (backend/frontend at minimum) parallelized; measured CI wall-clock time reduced for a representative PR, with before/after evidence recorded | Pass | None |

**Pre-existing parallelization finding (ST-15):** backend (`ci-tests.yml`) and frontend (`playwright.yml`) were already fully parallel — separate workflow files, no `needs:` dependency anywhere in `.github/workflows/` except 2 unrelated maintenance workflows — and Playwright's own E2E job was already 4-way sharded (confirmed balanced, within budget). This story's actual increment was doubling the shard count (4→8), the only remaining lever once existing parallelization was confirmed. Real before/after evidence (2 actual CI runs on this branch): critical path 198.5s → 163.0s average, a ~17.9% reduction.

**QA test coverage:**
- Scenarios run: `tests/test_cost_monitoring.py` (30/30 pass, local `backend/.venv` run — covers `log_api_call`, `get_api_call_report`, `get_api_session_report`, `get_monthly_claude_cost_by_feature`, `purge_claude_audit_log_older_than_730_days`, Alpaca/research instrumentation, and all 4 new endpoints)
- Regression areas checked: full backend suite (1411 passed, 10 skipped, 0 failures), `scripts/openapi_3way_drift_sweep.py` (143 router decorators / 144 contract headings / 144 openapi.yaml paths, no drift), `scripts/check_api_performance_baseline_drift.py` (clean), `tests/test_system_status_endpoint_count.py` (AST-derived fallback count consistency, 118→122)
- Known deviations: None found — all 5 stories' deviation checks completed with nothing to file

**Agent-mediated sign-off (execution_prompt.md §5.3):**
- **Infrastructure & Operations Owner** (sole owner ST-11/ST-12; joint with FinOps & Resource Architect for ST-13/ST-14; sole for ST-15) — a subagent reviewing against `claude/agents/infrastructure_operations_owner.md`'s charter examined the full working tree (branch had not yet merged at review time), independently re-ran every verification command (30/30 new tests, 1411/1411 full suite, both drift scripts, YAML parse), re-verified the anomaly-detection math, and independently grepped every `create_claude_audit_entry()` call site to confirm the ST-14 tag taxonomy matches documentation exactly rather than trusting the doc. **Verdict: Approved.** 4 informational (non-blocking) notes, all addressed same-session: (a) `Specs_Index.md`'s `ops_endpoints.md` description updated to include `POST /ops/purge-audit-logs`; (b) no dedicated index on `claude_audit_log.generated_at` — disclosed, not blocking, candidate for future backlog if the table grows large; (c) confirmed FinOps & Resource Architect joint sign-off needed separately for ST-13/ST-14 (obtained, below); (d) unreachable defensive-fallback code in `alpaca_service.py` clarified with an explanatory comment (pre-existing pattern, not introduced by this story).
- **FinOps & Resource Architect** (joint owner, ST-13/ST-14 only) — a second subagent reviewing against `claude/agents/finops_resource_architect.md`'s charter evaluated the retention-window cost/storage tradeoff, the per-feature attribution granularity, and the deferred-cleanup-pass decision from a resource-governance lens. **Verdict: Approved.** No blocking findings; 3 follow-on observations (storage/row-count projection, per-feature spend-trend view, silent-purge-failure visibility) filed as `BLG-OPS-153` rather than treated as gaps in this delivery.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend component touched this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Infrastructure & Operations Owner role — §5.3)
  Sprint Execution Engine (agent-mediated, FinOps & Resource Architect role — §5.3)
- Date: 2026-09-10
- Comments: BLG-GOV-19 autonomous class is not available for this EPIC per Criterion 1's own wording only in the sense that named-role sign-offs were required by the individual stories' AC (ST-11/ST-12/ST-13/ST-14 each explicitly name Infrastructure & Operations Owner and/or FinOps & Resource Architect sign-off) — per the Mixed-Class EPIC Signer Format Note (`qa_evidence_template.md`), the agent-mediated format above is used since named-authority sign-off, not the generic autonomous-class block, is what each story's own AC calls for. All 5 stories are otherwise `autonomous` classification (no `delegated_*` items in this EPIC) and no frontend-visible change was introduced. **This document's own DoQ block does not itself satisfy the STEP 4 merge gate's "QA sign-off" or "Product Owner acceptance" conditions** — those remain always-human per `execution_prompt.md` §5.3 and CLAUDE.md §2, and must be given directly on the pull request before merge.
