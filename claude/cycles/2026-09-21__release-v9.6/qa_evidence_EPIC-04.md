Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-22

---

# QA Evidence — EPIC-04: Operations & Security Debt

**EPIC:** EPIC-04 — Operations & Security Debt
**Cycle:** 2026-09-21__release-v9.6
**Sprint goal:** Ship the two build-and-ship product features committed at the 2026-09-19 rebalance — Clone-as-new-plan (`BLG-FEAT-96`) and CSV export for Screener and Watchlist (`BLG-FEAT-97`) — within the full 32-item, 7-EPIC v9.6 scope at the top of confirmed sprint capacity, landing the live-capital trailing-stop formula decision (`BLG-BE-119`) early so the nightly stop-update path can be hardened on a single agreed formula.
**Test scenarios used:** `tests/test_nightly_stop_update_staleness.py` (ST-14, 7 tests), `tests/test_ci_usage_report.py` (ST-17, 14 tests)

**Delegation class:** ST-14, ST-15, ST-17 `autonomous`; ST-16 `delegated_decision` (unblocked this cycle via direct human action, not agent ruling — see below). No file under `src/pages/**` or `src/components/**` was created or modified by this EPIC — entirely ops/CI/docs. **The Autonomous DoQ sign-off class (BLG-GOV-19) does NOT apply** — Criterion 1 requires all stories `autonomous`; ST-16 is `delegated_decision`. Standard Sign-Off Block used below.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-14 | `scripts/check_nightly_stop_update_staleness.py`; `tests/test_nightly_stop_update_staleness.py`; `.github/workflows/nightly-stop-update-staleness-check.yml` | Dead-man's-switch staleness check for the nightly trailing-stop job: reads `GET /health/scheduler` only (never calls the real update endpoint, so live stops cannot be disturbed — RISK-04), alerts via Telegram if not succeeded within 26h, scheduled every 6h | AC-01 A simulated missed run raises the alert within the window — `tests/test_nightly_stop_update_staleness.py` (7/7 pass, incl. deliberately-stale and most-recent-run-errored cases). AC-02 A successful run clears it — same suite, recent-successful-run case | Pass | None |
| ST-15 | `docs/ops/github_actions_secrets_ownership_map.md` | Inventory of all 14 distinct `secrets.*` names across `.github/workflows/*.yml`, each with consuming workflow(s), environment, and required access level; flags `DATABASE_URL` as a retired alias and documents `PROD_DATABASE_URL`'s read-write requirement explicitly (the exact mistake the source backlog item's problem statement describes) | AC-01 Every secret in the inventory with consuming workflow(s) and access level — done. AC-02 Document discoverable from the two named cross-references — `docs/infrastructure/staging_setup.md` §8 and `docs/ops/production_deployment_runbook.md` §7 both updated. AC-03 Infrastructure & Operations Owner sign-off — recorded in the document's own Sign-off section | Pass | None |
| ST-16 | `docs/ops/synthetic_uptime_monitor_confirmation_2026-09-16.md`; `.github/workflows/health-check-alert.yml` | Confirmed the synthetic uptime monitor's live-fire and Telegram delivery path with real evidence. Blocked in-session by an Actions-write token limitation (confirmed via two real 403s) — the user (Infrastructure & Operations Owner) triggered the run directly via the GitHub Actions UI instead. First attempt used a test URL (`httpstat.us/500`) that had gone stale (now returns 404) — found, disclosed, and fixed in-file rather than silently retried without explanation; second attempt (`httpbin.org/status/500`) confirmed 3/3 real HTTP 500s and a real Telegram delivery, independently confirmed received by the user | AC-01 A real live-fire test run confirmed to have triggered the alert path (run URL/ID recorded) — `https://github.com/sachiv1984/swing-trading-model/actions/runs/35727112554`. AC-02 A real Telegram notification confirmed received — Telegram API `{"ok":true,...}` plus independent user confirmation. AC-03 Confirmation doc §7/§8 updated; `BLG-OPS-158`/ST-11's original disclosed gap closed — done | Pass | None |
| ST-17 | `scripts/generate_ci_usage_report.py`; `tests/test_ci_usage_report.py`; `.github/workflows/ci-usage-report.yml`; `docs/ops/ci_usage_reports/2026-08.md` | Monthly per-workflow CI run-minutes and artifact-storage report; generated a real first report for 2026-08 (9958 runs, ~9755.6 estimated run minutes, 461.4 MB artifact storage, 36 workflows). Disclosed two findings rather than working around them silently: this public repo has no metered "billable minutes" (report tracks wall-clock `run_duration_ms` instead, clearly labelled); short-retention artifacts from a month closed >7 days before report generation are already deleted by GitHub (report computes and prints a per-workflow undercount caveat) | AC-01 A monthly per-workflow figure exists — done, real first report committed, monthly schedule wired. AC-02 All artifact uploads carry explicit retention — verified pre-met (all 6 existing `upload-artifact` call sites already had `retention-days`, predating this backlog item's filing) | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_nightly_stop_update_staleness.py` (7/7), `tests/test_ci_usage_report.py` (14/14); full backend suite re-run this cycle (EPIC-03's own re-run, 1685 passed/3 skipped/7 pre-existing unrelated failures — EPIC-04 added no new backend test dependencies beyond the two files above, both independently green).
- Regression areas checked: CI workflow additions (2 new scheduled workflows, both dry-run tested locally before commit); no application code paths touched (ops/CI/docs only).
- Known deviations: None found — all 4 stories' deviation checks completed with nothing to file. (ST-14/ST-16's disclosed limitations — the in-memory `GET /health/scheduler` reset-on-restart caveat, and the stale `httpstat.us` test fixture — are documented findings within each story's own scope, not gaps against that story's own AC.)

**Notes for the Director of Quality and Product Owner:**

1. **ST-16's blocker and resolution path is worth surfacing explicitly.** This session's own `gh` token could not dispatch a `workflow_dispatch` event (confirmed via two real `403`s, not assumed) — the user triggered the run directly via the GitHub Actions UI and confirmed Telegram receipt personally. This is the same disclose-rather-than-fabricate pattern used elsewhere this cycle (`ESC-EXEC-20260910-01` precedent), resolved by direct human action rather than an agent ruling.
2. **ST-17's "billable minutes" finding may be relevant to FinOps & Resource Architect's future cost reviews.** This repo being public means GitHub Actions minutes are unmetered/free — `docs/ops/ci_usage_reports/*.md`'s figures are a capacity/trend signal only, with no dollar-cost meaning today, but become the metric to watch if the repo is ever made private.

**Backlog items filed from this EPIC's findings:** None — all 4 stories' own scope was completed or transparently disclosed within their own AC; no out-of-scope findings surfaced.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations — none filed
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend files touched by this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-22
- Comments: All 4 stories' acceptance criteria verified against their canonical spec references (see table above). ST-16's live-fire confirmation used real, first-hand evidence obtained via direct user action (Actions UI trigger + independent Telegram receipt confirmation), not agent-mediated inference — the strongest evidentiary class available for this AC. Full backend suite (re-run at EPIC-03's own close, unaffected by EPIC-04's ops/CI/docs-only changes): 1685 passed, 3 skipped, 7 pre-existing unrelated failures. No frontend files touched. Merge remains subject to the always-human QA sign-off and Product Owner acceptance (`execution_prompt.md` §5.3 — this agent-mediated sign-off does not itself substitute for those).
