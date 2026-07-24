Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-24

# QA Evidence Log — EPIC-10 (v7.7)

## Consolidation Block

**EPIC:** EPIC-10 — Nightly backtest job monitoring/alerting
**Cycle:** 2026-07-21__release-v7.7
**Sprint goal:** Ship the four design-gated Strategy Intelligence & Notification UX items and clear seven ready capacity-fill items to fully utilise this sprint's confirmed capacity.
**Test scenarios used:** Local simulation of both alert-trigger paths (exit 1 hard failure, exit 2 drift anomaly) plus a mock-HTTP-server verification of the Telegram POST logic — no committed test file (CI/infra correctness, per STEP 3.1.A Case D)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-10 | `.github/workflows/backtest.yml` | Added a monitoring/alerting step to the nightly backtest job. Captures `import_backtest.py`'s exit code (0/1/2) without failing the step, sends a Telegram alert distinguishing a hard failure (exit 1) from a detected output anomaly (exit 2, `BACKTEST_DRIFT_ALERT` per EPIC-09's audit / BLG-BE-60), degrades gracefully with a `::warning::` annotation if Telegram secrets aren't configured, and still fails the job on any non-zero exit code (preserving existing CI-red visibility). Filed BLG-OPS-115 for the operational follow-up (configuring the GH repo secrets). | Monitoring/alerting mechanism added for nightly backtest job failures or output anomalies; confirmed to fire on a simulated failure/anomaly | Pass | None |

**QA test coverage:**
- Scenarios run: local bash simulation of both `CODE=1` and `CODE=2` message-construction paths (confirmed correct, distinct text for each); mock local HTTP server test confirming the `curl --data-urlencode` POST correctly reaches a Telegram-`sendMessage`-shaped endpoint with correctly URL-encoded `chat_id`/`text` parameters; `pytest tests/ -k backtest` (1 passed, no regression); `yaml.safe_load` confirms `backtest.yml` remains valid after the restructure
- Regression areas checked: confirmed the final "Fail job if import step did not succeed" gate step preserves the pre-existing CI-red-on-failure behaviour (same external visibility as before this change) — agent-mediated review independently verified this against the actual YAML
- Known deviations filed: None — actual live Telegram delivery requires `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` to be configured as GH Actions repo secrets (currently only present as Render backend env vars); filed as BLG-OPS-115 (P2, Infrastructure & Operations Owner) since the engine cannot configure repo secrets itself. Sprint backlog's own ST-10 entry confirms "Staging-only ACs: None — simulated-failure trigger is engine/CI-executable," so the local simulation described above satisfies the Quality AC without requiring the live secrets.

**Dependency note:** ST-10 depends on ST-09 (EPIC-09) per `sprint_planning_notes.md`'s Shared File Ownership Advisory (both EPICs touch `backtest.yml`/nightly backtest job surface). Satisfied by merging EPIC-09's commits directly into the EPIC-10 branch before implementation began, so ST-10 builds on the idempotency-audited version of the job (including the `concurrency` guard), not a pre-audit baseline.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, CI workflow change only, no frontend code
- Signed off by: Sprint Execution Engine (agent-mediated, Infrastructure & Operations Owner + Head of Engineering roles — §5.3)
- Date: 2026-07-24
- Comments: No frontend-visible change. Named dual-authority sign-off obtained per sprint_backlog.md's ST-10 Verification field ("Infrastructure & Operations Owner confirms the simulated-failure trigger test; Head of Engineering sign-off"). Human Director of Quality review and Product Owner acceptance still required before merge per §5.3 "Always-human gates".
