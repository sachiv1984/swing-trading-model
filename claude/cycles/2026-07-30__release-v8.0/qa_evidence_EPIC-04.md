Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-30

# QA Evidence — EPIC-04 (Operations & Reliability)

**EPIC:** EPIC-04 — Operations & Reliability
**Cycle:** 2026-07-30__release-v8.0
**Sprint goal:** Close the platform's outstanding backend error-masking, security-hardening, and FX/data-spec debt while shipping keyboard/focus accessibility fixes to the Trade Plan flow, strengthening QA/CI test infrastructure, hardening operational alerting and disaster-recovery readiness, and fixing the recurring cross-EPIC `execution_state.json` merge-conflict pattern.
**Test scenarios used:** Live `workflow_dispatch` run (GitHub Actions run `30575941928`) against a safe public test endpoint (`https://httpbin.org/status/500`).

**Status:** In progress — ST-13 and ST-14 done and verified below; ST-15/16/17 remain blocked_backend pending separate live dashboard actions (Render, Supabase). This file will be completed with those entries once unblocked.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-13 | `.github/workflows/health-check-alert.yml` | Scheduled (every 15 min) + `workflow_dispatch` poll of production `GET /health`, 3 attempts 20s apart, alerts Telegram only on a sustained (3/3) 5xx. Added a `test_url` `workflow_dispatch` input for safe live-fire testing without touching real infrastructure. | Lightweight health-check poll posts a Telegram alert on a sustained 5xx spike; alert confirmed to fire on a simulated 5xx spike or documented dry-run; depends on ST-14's secrets for full E2E confirmation | Pass | None |
| ST-14 | `claude/cycles/2026-07-30__release-v8.0/stage4_backlog_slice.md#ST-14` | Pure GitHub repo-secret configuration (no code) — `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` added to repo Settings → Secrets and variables → Actions by the user (Infrastructure & Operations Owner capacity), same values as existing Render env vars. | `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` present in repo secrets; a manual `workflow_dispatch` re-run against a deliberately-broken endpoint confirms a Telegram message is actually received (not just the `::warning::` fallback) | Pass | None |

**Live-fire test detail (ST-13 + ST-14, shared evidence):**
- Trigger: `gh workflow run "Production Health Check Alert" -f test_url="https://httpbin.org/status/500"`
- Run: https://github.com/sachiv1984/swing-trading-model/actions/runs/30575941928 (job `90984130543`, both steps succeeded)
- Poll results: `Attempt 1: HTTP 500`, `Attempt 2: HTTP 500`, `Attempt 3: HTTP 500` → `fail_count=3`
- Alert step took the real Telegram-send branch (both secrets present) — Telegram API response: `{"ok":true,"result":{"message_id":298,"from":{"username":"Trading_Assistant_Alert_bot"},"chat":{"first_name":"Sachiv","last_name":"Patel","type":"private"},...}}`
- This confirms: (a) the poll/count/alert logic works correctly against a real HTTP 500 response, and (b) a real Telegram message was actually delivered to the configured chat — not merely the `::warning::` graceful-degradation path.
- **Human confirmation:** Infrastructure & Operations Owner confirmed direct receipt of the alert message in their own Telegram client, independently corroborating the API response above.

**Process note:** Because GitHub only exposes `workflow_dispatch` for workflows present on the default branch, `.github/workflows/health-check-alert.yml` was merged to `main` early via a separate, scoped PR (#1163, `[GOVERNANCE]` title to avoid triggering the full-EPIC QA-evidence gate prematurely) rather than waiting for the rest of EPIC-04's stories to unblock. This is documented as a deliberate, user-approved deviation from strict "whole EPIC merges together" sequencing — see `execution_state.json` process_notes and `delegation_log.md` DEL-20260731-01/02 resolution notes for full detail.

**QA test coverage:**
- Scenarios run: Live `workflow_dispatch` execution against a real (if synthetic) HTTP 500 source, real Telegram API call — not a mock or unit test.
- Regression areas checked: N/A (new workflow, no existing behavior touched).
- Known deviations filed: None.

---

## Autonomous class eligibility check (BLG-GOV-19)

Not applicable yet — this EPIC contains `delegated_backend` stories (ST-13 through ST-17), so the autonomous class sign-off path does not apply per execution_prompt.md §3.2.A. A mixed-class signer format (agent-mediated, named domain role) will be used for the full EPIC-level consolidation once all 5 stories are done.

## Partial sign-off (ST-13, ST-14 only — EPIC-level consolidation pending remaining stories)

- [x] AC verified for ST-13 and ST-14 against the canonical spec (`stage4_backlog_slice.md`)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (N/A — new workflow only)
- Signed off by: Infrastructure & Operations Owner (user, sachiv.patel@hotmail.co.uk)
- Date: 2026-07-30
- Comments: Live-fire test evidence above is objective and reproducible (run log linked). Infrastructure & Operations Owner independently confirmed direct receipt of the Telegram alert message in their own Telegram client, corroborating the Telegram API's `{"ok":true,"result":{"message_id":298,...}}` response with first-hand delivery confirmation. Partial sign-off for ST-13/ST-14 is finalized; full EPIC-04 sign-off remains pending ST-15/16/17.
