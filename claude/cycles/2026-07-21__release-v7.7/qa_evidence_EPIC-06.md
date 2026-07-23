Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-24

# QA Evidence Log — EPIC-06 (v7.7)

## Consolidation Block

**EPIC:** EPIC-06 — CI curl response validation (daily-snapshot.yml)
**Cycle:** 2026-07-21__release-v7.7
**Sprint goal:** Ship the four design-gated Strategy Intelligence & Notification UX items and clear seven ready capacity-fill items to fully utilise this sprint's confirmed capacity.
**Test scenarios used:** Simulated-failure test (local curl reproduction, no committed test file — CI/infra correctness, per STEP 3.1.A Case D)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-06 | `.github/workflows/daily-snapshot.yml` | Added `--fail --show-error` to the three business-endpoint curl invocations (Run Position Analysis, Create Portfolio Snapshot, Generate Signals). The "Wake up API" health-check call's `\|\| true` fallback is unchanged (intentional — non-fatal cold-start ping, not a business write). | `--fail` (or explicit status/body validation) added to all three curl invocations; a broken write path now surfaces as a failed CI run; other workflows posting to business endpoints audited for the same gap, confirming `backtest.yml`'s existing Python status-code validation is sufficient | Pass | None |

**QA test coverage:**
- Scenarios run: local simulated-failure reproduction — `curl --fail --show-error` against an unreachable host (exit 7) and against a local mock server returning HTTP 500 (exit 22), both confirmed independently by two separate reviewers (self-check at implementation time, and Infrastructure & Operations Owner agent-mediated review)
- Regression areas checked: full audit of all 5 workflow files using `curl` (`alert-evaluation.yml` — already `curl -f`; `validate-analytics.yml` — already `curl -sf`; `staging-deploy.yml` — already explicit `HTTP_STATUS` check + `exit 1`; `backtest.yml` — business write via `import_backtest.py`, already `sys.exit(1)` on non-200; `daily-snapshot.yml` — the one with the gap, now fixed). No other workflow required changes.
- Known deviations filed: None

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, CI workflow change only, no frontend code
- Signed off by: Sprint Execution Engine (agent-mediated, Infrastructure & Operations Owner role — §5.3)
- Date: 2026-07-24
- Comments: No frontend-visible change (CI/infra only); BLG-GOV-19 autonomous class criteria would technically be met (all-autonomous, code-review-verifiable, no UI change), but the sprint_backlog.md ST-06 Verification field explicitly names "Infrastructure & Operations Owner confirms simulated-failure test and audit completeness" as the required sign-off path, so that named-authority review was obtained instead of substituting the generic autonomous-class shortcut. Reviewer noted their charter is scoped to operational documentation governance rather than CI workflow correctness per se, but completed and independently reproduced all requested technical verification, which held up. Human Director of Quality review and PR-level sign-off still required before merge per §5.3 "Always-human gates".
