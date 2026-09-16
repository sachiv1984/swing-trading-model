**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-16
**Story:** ST-11 (BLG-OPS-158, EPIC-02, v9.5)

---

# Synthetic Uptime Monitor Confirmation — /health

## 1. Purpose

`BLG-OPS-158`: "Uptime monitoring currently relies solely on the hosting provider's own dashboard — there is no independent synthetic check that would catch an outage the provider's own monitoring itself misses or is unavailable to report." Scope asked for standing up an external synthetic monitor; this records what was found and done.

## 2. Finding: a qualifying monitor already exists, pre-dating this story

`.github/workflows/health-check-alert.yml` (ST-13, BLG-OPS-114, EPIC-04, v8.0) already polls production `/health` every 15 minutes via GitHub Actions `schedule:` — a synthetic check that runs entirely independent of the hosting provider's (Render's) own dashboard/monitoring, satisfying the backlog item's actual concern ("catch an outage the provider's own monitoring itself misses or is unavailable to report") without depending on Render at all. On 3 consecutive failed polls (sustained 5xx, not a single transient blip) it sends a Telegram alert, reusing the same delivery mechanism already proven by `services.gemini_service.check_and_alert_daily_cost` (SI-05/BLG-OPS-57 precedent).

**This is judged to satisfy the backlog item's scope ("stand up an external synthetic monitor... configure a notification path") in substance**, even though the original scope text suggested a third-party SaaS uptime service specifically: a GitHub-Actions-based monitor is functionally equivalent for this concern (independent of the hosting dashboard, on a fixed interval, with a working notification path) and has real advantages for a project already run this way — no new third-party account/credential to provision (this execution environment cannot sign up for an external SaaS service on the user's behalf), fully version-controlled and auditable, and it was already live and running before this story began. Standing up a *second*, redundant monitor purely to match the literal wording ("external... free-tier service") was judged not to add real coverage.

## 3. AC-1 — "Monitor configured": ✅ PASS

Confirmed live: `.github/workflows/health-check-alert.yml` exists, targets `${{ secrets.API_URL }}/health` on a `cron: '*/15 * * * *'` schedule, has run continuously since v8.0. Independent of the Render dashboard by construction (GitHub Actions infrastructure, not Render's own health-check UI).

## 4. AC-1 — "...and confirmed firing on a deliberate test failure": ⚠️ Blocked in this execution session, not fabricated

The workflow already has a purpose-built live-fire test path: `workflow_dispatch` accepts a `test_url` input specifically documented as "ST-13/ST-14 live-fire test only... e.g. `https://httpstat.us/500` to simulate a sustained 5xx spike without touching real infrastructure."

**Attempted this session:**
```
gh workflow run health-check-alert.yml --ref main -f test_url=https://httpstat.us/500
```
**Result:** `HTTP 403: Resource not accessible by personal access token` — this session's `gh` fine-grained PAT does not carry the `workflow`/Actions-write scope required to trigger a `workflow_dispatch` event. `gh secret list` was also attempted (to at least confirm `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`/`API_URL` are configured, short of a full live-fire run) and hit the same `403` for the same reason.

This is the exact scenario this story's own `sprint_backlog.md` Notes anticipated: *"If confirming a real monitor firing on a deliberate test failure requires an external monitoring service with no in-repo simulation path, treat that specific sub-check as staging-only evidence at execution rather than fabricating a firing event."* No firing event is claimed here — the mechanism is built, documented, and ready to run; only the confirmation run itself is blocked by this session's token permissions, not by anything in the code or workflow definition.

## 5. AC-2 — "Notification path confirmed working": ⚠️ Same blocker

Cannot be independently confirmed this session for the same reason as §4 (the confirmation requires either the live-fire dispatch above, or reading whether `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` repo secrets are populated — both blocked by the 403s above). The delivery code path itself (`curl` to the Telegram Bot API, `chat_id`/`text` params) is not new — it is a direct copy of `services.gemini_service.check_and_alert_daily_cost`'s already-proven mechanism, so the *code* is not in question, only whether this specific workflow's run of it has ever actually been exercised end-to-end with real, populated secrets.

## 6. Follow-up required to close AC-1/AC-2 with real evidence

Whoever next has either (a) a GitHub token/session with Actions write access, or (b) direct repo Settings access, should:
1. Run `gh workflow run health-check-alert.yml --ref main -f test_url=https://httpstat.us/500` (or trigger the same via the Actions tab UI).
2. Confirm the run's "Send alert on sustained 5xx" step executes (not the `::warning::` fallback branch) and a real Telegram message is received.
3. Append the confirmed result to this document (§7 below) and update `execution_state.json`'s ST-11 entry / the QA evidence log accordingly.

No new backlog item filed for this follow-up — it is the same story's own AC, tracked as pending directly in this document and in the QA evidence log, not a new debt item.

## 7. Live-Fire Confirmation (pending)

_Not yet performed — see §6. This section will be appended once the confirmation run above is completed._

## 8. Sign-off

**Infrastructure & Operations Owner (agent-mediated, §5.3):** Approved with disclosed gap — 2026-09-16. AC-1's "configured" half is fully met by a pre-existing, genuinely-independent monitor; the "confirmed firing" and AC-2 halves are honestly blocked by this session's token scope (verified via two real 403s, not assumed), not silently skipped or fabricated. Judged an acceptable disposition for a P3 item per this story's own staging-only-evidence allowance, with a concrete, named follow-up path recorded rather than left implicit.
