Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-31

# QA Evidence — EPIC-04 (Operations & Reliability)

**EPIC:** EPIC-04 — Operations & Reliability
**Cycle:** 2026-07-30__release-v8.0
**Sprint goal:** Close the platform's outstanding backend error-masking, security-hardening, and FX/data-spec debt while shipping keyboard/focus accessibility fixes to the Trade Plan flow, strengthening QA/CI test infrastructure, hardening operational alerting and disaster-recovery readiness, and fixing the recurring cross-EPIC `execution_state.json` merge-conflict pattern.
**Test scenarios used:** Live `workflow_dispatch` run (GitHub Actions run `30575941928`) against a safe public test endpoint (`https://httpbin.org/status/500`).

**Status:** In progress — ST-13, ST-14, ST-15 done and verified below; ST-16/17 remain blocked_backend. ST-16's initial "no gap found" finding was reversed by FinOps & Resource Architect review pending a stronger check (see below). This file will be completed with those entries once unblocked.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-13 | `.github/workflows/health-check-alert.yml` | Scheduled (every 15 min) + `workflow_dispatch` poll of production `GET /health`, 3 attempts 20s apart, alerts Telegram only on a sustained (3/3) 5xx. Added a `test_url` `workflow_dispatch` input for safe live-fire testing without touching real infrastructure. | Lightweight health-check poll posts a Telegram alert on a sustained 5xx spike; alert confirmed to fire on a simulated 5xx spike or documented dry-run; depends on ST-14's secrets for full E2E confirmation | Pass | None |
| ST-14 | `claude/cycles/2026-07-30__release-v8.0/stage4_backlog_slice.md#ST-14` | Pure GitHub repo-secret configuration (no code) — `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` added to repo Settings → Secrets and variables → Actions by the user (Infrastructure & Operations Owner capacity), same values as existing Render env vars. | `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` present in repo secrets; a manual `workflow_dispatch` re-run against a deliberately-broken endpoint confirms a Telegram message is actually received (not just the `::warning::` fallback) | Pass | None |
| ST-15 | `docs/operations/render_rollback_runbook.md` (v1.1→v1.2) | Execution-history audit (found no prior real rollback or drill), then a deliberate rollback drill actually executed against the non-production staging service (`trading-assistant-api-staging`) by the Infrastructure & Operations Owner. | Historical execution evidence recorded, OR a deliberate rollback drill run and its outcome documented either way | Pass | None — one procedure correction applied to Step 3 based on tested reality (see below), not a deviation from the AC |
| ST-16 | `docs/ops/render_build_deploy_path_filter_audit.md` (v1.0→v1.1) | In-repo runtime-read file inventory, then production's dashboard-only Build Filters configuration read live. | Production filter configuration recorded and confirmed to cover the same runtime-read file set as the in-repo inventory | **Blocked — pending stronger verification** | Initial "no gap found" conclusion was reversed by FinOps & Resource Architect review; see detail below |

**Live-fire test detail (ST-13 + ST-14, shared evidence):**
- Trigger: `gh workflow run "Production Health Check Alert" -f test_url="https://httpbin.org/status/500"`
- Run: https://github.com/sachiv1984/swing-trading-model/actions/runs/30575941928 (job `90984130543`, both steps succeeded)
- Poll results: `Attempt 1: HTTP 500`, `Attempt 2: HTTP 500`, `Attempt 3: HTTP 500` → `fail_count=3`
- Alert step took the real Telegram-send branch (both secrets present) — Telegram API response: `{"ok":true,"result":{"message_id":298,"from":{"username":"Trading_Assistant_Alert_bot"},"chat":{"first_name":"Sachiv","last_name":"Patel","type":"private"},...}}`
- This confirms: (a) the poll/count/alert logic works correctly against a real HTTP 500 response, and (b) a real Telegram message was actually delivered to the configured chat — not merely the `::warning::` graceful-degradation path.
- **Human confirmation:** Infrastructure & Operations Owner confirmed direct receipt of the alert message in their own Telegram client, independently corroborating the API response above.

**ST-15 rollback drill detail:**
- Target: `trading-assistant-api-staging` (non-production, per `render.yaml`) — production was not touched.
- Outcome: rolled back cleanly, deploy transitioned to Live (green) in the Render dashboard.
- Post-rollback verification: `GET /health` returned `{"status":"ok","db":"connected", ...}` — matches the runbook's Step 4 expected outcome.
- Procedure finding: no log entries (error or otherwise) were visible in the Render Logs tab during/after the rollback, despite the deploy succeeding. The runbook's Step 3 has been corrected to note that an empty Logs tab is not itself a failure signal — Deploy status (green/Live) plus `/health` are the authoritative checks. See `render_rollback_runbook.md` §Execution History and its corrected Step 3 for full detail.

**ST-16 production filter detail (still open):**
- Read live: Root Directory `backend`, Build Command `pip install -r requirements.txt`, Included Paths `docs/product/changelog.md` (only entry).
- Initial concern: a bare Included Paths entry might act as an exhaustive allow-list, meaning only changelog-only commits would auto-deploy and all `backend/**` changes would be silently ignored — a potentially serious production drift risk.
- First-pass test: production's most recent deploy is live for commit `95b2e6bf` (`[EPIC-01] Data Model & Spec Integrity`), a backend-only commit with no changelog.md change, and it deployed. This was initially read as disproving the allow-list hypothesis.
- **FinOps & Resource Architect review reversed this:** a single deploy observation cannot distinguish an automatic push-triggered deploy from a human manually clicking "Deploy latest commit" after the merge — both produce the identical observation. Render's own documentation was also found to be inconsistent across two pages on this exact interaction. **Not resolved yet.** Required follow-up: check the `95b2e6bf` deploy's trigger-source label in the Render dashboard, or run a trivial backend-only live-fire push test (same rigor as ST-13/14) to confirm autodeploy fires with zero manual intervention.

**Process note:** Because GitHub only exposes `workflow_dispatch` for workflows present on the default branch, `.github/workflows/health-check-alert.yml` was merged to `main` early via a separate, scoped PR (#1163, `[GOVERNANCE]` title to avoid triggering the full-EPIC QA-evidence gate prematurely) rather than waiting for the rest of EPIC-04's stories to unblock. This is documented as a deliberate, user-approved deviation from strict "whole EPIC merges together" sequencing — see `execution_state.json` process_notes and `delegation_log.md` DEL-20260731-01/02 resolution notes for full detail.

**QA test coverage:**
- Scenarios run: Live `workflow_dispatch` execution against a real (if synthetic) HTTP 500 source, real Telegram API call — not a mock or unit test.
- Regression areas checked: N/A (new workflow, no existing behavior touched).
- Known deviations filed: None.

---

## Autonomous class eligibility check (BLG-GOV-19)

Not applicable yet — this EPIC contains `delegated_backend` stories (ST-13 through ST-17), so the autonomous class sign-off path does not apply per execution_prompt.md §3.2.A. A mixed-class signer format (agent-mediated, named domain role) will be used for the full EPIC-level consolidation once all 5 stories are done.

## Partial sign-off (ST-13, ST-14, ST-15 — EPIC-level consolidation pending ST-16/17)

- [x] AC verified for ST-13, ST-14, and ST-15 against their canonical specs
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (N/A — new workflow / documentation only)
- Signed off by: Infrastructure & Operations Owner (user, sachiv.patel@hotmail.co.uk)
- Date: 2026-07-31
- Comments: Live-fire test evidence for ST-13/ST-14 is objective and reproducible (run log linked); Infrastructure & Operations Owner independently confirmed direct receipt of the Telegram alert in their own Telegram client. ST-15's staging rollback drill was executed directly by the Infrastructure & Operations Owner against `trading-assistant-api-staging`, confirmed via a clean Live/green deploy and a post-rollback `/health` check. Partial sign-off for ST-13/ST-14/ST-15 is finalized; full EPIC-04 sign-off remains pending ST-16 (reopened — see detail above, needs deploy trigger-source confirmation) and ST-17.
