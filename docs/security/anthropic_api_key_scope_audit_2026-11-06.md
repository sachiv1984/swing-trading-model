**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-11-06 (created — ST-29, EPIC-05, v9.15, BLG-OPS-48)
**Cycle:** 2026-11-03__release-v9.15
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Anthropic API Key Six-Month Scope Audit

## Purpose

`BLG-OPS-48` asks for a follow-up, six months after the v4.2 scope review (`docs/security/anthropic_api_key_scope_review.md`, 2026-05-27), confirming that `ANTHROPIC_API_KEY` is still used only where documented and that it has been rotated on schedule. This record answers ST-29's three acceptance criteria:

1. Key scope confirmed minimal: used only by the AI endpoints in the current AI endpoint register, each named.
2. Key rotation confirmed per the BLG-OPS-38 schedule.
3. Review findings documented.

## Method

- **Code audit (engine, 2026-11-05).** Every reference to `ANTHROPIC_API_KEY` and every `anthropic.Anthropic(...)` client in `backend/`, `scripts/`, `src/` and `.github/` was found with `grep`, and each client was traced to the route that reaches it.
- **Published frontend check (engine, 2026-11-05).** The live GitHub Pages bundle (`gh-pages` commit `c329390a`) was searched for the Anthropic key pattern by match count only. No value was printed.
- **Console read (Cybersecurity & Trust Lead, the user, in session, 2026-11-06, `DEL-20261105-04`).** Anthropic Console → Settings → API Keys: names and dates only, no key values.

## Findings

### 1. Endpoints using the key

Six live endpoints reach an Anthropic client. All six are shipped, user-triggered features; none is undocumented scope creep.

| Endpoint | Service | Client |
|----------|---------|--------|
| `POST /ai/journal-summary` | `ai_service.summarise_journal_notes` | `ai_service.py` |
| `POST /ai/daily-briefing` | `ai_service.generate_daily_briefing` | `ai_service.py` |
| `POST /ai/chat` | `ai_service.py` (chat) | `ai_service.py` |
| `POST /trade-plans/generate-plan` | `gemini_service.generate_full_plan` | `gemini_service.py` |
| `POST /trades/{trade_id}/debrief` | `debrief_service.generate_trade_debrief` | `debrief_service.py` |
| `POST /reports/monthly-pnl/narrative` | `monthly_pnl_narrative_service.py` (v9.11) | `monthly_pnl_narrative_service.py` |

`POST /trade-plans/{plan_id}/generate-thesis` is retired (404 since v9.14) and no longer reaches a client. Monitoring endpoints (`/ai/check-daily-cost`, `/ai/monthly-cost`, `/ai/spend-trend`, `/ai/claude-audit-log`) read logged data and make no Anthropic call.

**Register drift.** The AI endpoint register (`docs/governance/ai_feature_touchpoint_register.md` v1.0) still lists `generate-thesis` (tracked by `BLG-SPEC-211`) and omits `POST /reports/monthly-pnl/narrative`. The anomaly check's endpoint list (`ai_endpoint_anomaly_service.py`) and the credential inventory's Purpose row have the same gaps. The key is used by exactly the six endpoints above; the register is behind the code, not the other way round. Tracked by **`BLG-SPEC-223`**.

**Other uses of the key.**
- Backend: none outside the six services above. The key is read from the environment only and is not logged.
- `scripts/`: none.
- **GitHub Actions: a second copy.** `.github/workflows/deploy.yml` passes the secret `REACT_APP_ANTHROPIC_API_KEY` into the public GitHub Pages build. Create React App inlines every `REACT_APP_*` value into the client bundle. `src/pages/TradePlan.js:122` uses it only as a boolean (`HAS_AI`), and the minifier folds that expression, so the published bundle contains no key (match count 0). The frontend makes no Anthropic call. Any future code that reads the value would publish it. The secret was set on 2026-05-25, the same day the only console key was created (finding 2), so it very likely holds the live key. Tracked by **`BLG-OPS-213`**.

**AC 1 result:** not met as worded. The application uses the key only for the six live AI endpoints named above, all shipped features. But one of them is missing from the register (`BLG-SPEC-223`), and the GitHub Pages secret is a second, unnecessary copy of the key (`BLG-OPS-213`).

### 2. Keys and rotation

Console read, 2026-11-06:

| Keys in the workspace | Created | Last used |
|-----------------------|---------|-----------|
| 1 (prefix not recorded here) | 2026-05-25 | 2026-10-14 |

- There is one key, so it is the key Render's `ANTHROPIC_API_KEY` holds. This is inferred from the console list, not checked against the Render environment value.
- The 2026-10-14 last-used date fits current usage: every AI feature is user-triggered (the daily briefing runs on a button press, not on refresh), and the app has not been used since.
- `docs/ops/api_key_rotation_policy.md` sets the Anthropic key's first rotation due on **2026-08-25** (90 days from first inventory, then annual). The key has not been rotated since its creation on 2026-05-25, so the rotation is about ten weeks overdue. `docs/ops/external_api_credential_inventory.md` records "Last rotated: Unknown".

**AC 2 result:** **not met.** The rotation due 2026-08-25 has not happened. Carried post-merge by **`BLG-OPS-214`** (rotate the key, revoke the old one, delete the GitHub secret).

### 3. Changes since the v4.2 review

| v4.2 statement (2026-05-27) | Now |
|-----------------------------|-----|
| Key-level scope restriction is not available on the Anthropic platform | Not re-checked in the console; application-level controls remain the mitigation |
| Only one model is called (`claude-haiku-4-5`) | Stale. The daily briefing and chat call `claude-sonnet-4-6`; the other features call Haiku (`ai_feature_touchpoint_register.md`) |
| Thesis generation is the only AI use | Stale. Six endpoints (finding 1) |
| No application-level rate limit | The per-endpoint anomaly check (`POST /ai/check-endpoint-anomalies`) and daily cost alert (`POST /ai/check-daily-cost`) now exist |
| Key stored in environment variables only, not logged, not committed | Still true for the backend. The GitHub Pages build secret is the exception (finding 1) |

## Follow-ups

| Item | Priority | What |
|------|----------|------|
| `BLG-OPS-214` | P1 | Rotate the Anthropic key (overdue since 2026-08-25), revoke the old key, record the rotation |
| `BLG-OPS-213` | P2 | Remove `REACT_APP_ANTHROPIC_API_KEY` from `deploy.yml` and GitHub secrets |
| `BLG-SPEC-223` | P3 | Add `POST /reports/monthly-pnl/narrative` to the register, the anomaly check list and the credential inventory |

## Sign-off

- **Console evidence:** supplied by the Cybersecurity & Trust Lead (the user, in session), 2026-11-06, `DEL-20261105-04`.
- **Review:** Sprint Execution Engine (agent-mediated, Cybersecurity & Trust Lead role — §5.3), 2026-11-06. AC 1 not met as worded (`BLG-SPEC-223`, `BLG-OPS-213`), AC 2 not met (`BLG-OPS-214`), AC 3 met by this record.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-11-06 | Created — ST-29, EPIC-05, v9.15, BLG-OPS-48. |
