**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-08-08
**Cycle:** 2026-08-05__release-v8.3 (ST-01 — BLG-OPS-129); staging verification closed 2026-08-08 (ST-19, EPIC-05, v8.4 — BLG-OPS-132)

---

# SI-05 Weekly Digest Delivery — Root Cause Investigation

## Summary

The SI-05 weekly strategy-integrity Telegram digest stopped delivering. Root cause: **no automated trigger mechanism was ever committed to call `POST /digest/si05/send` on a schedule.** The endpoint itself, its data fetch, its Telegram send logic (with retry/backoff), and its delivery log (`si05_digest_log`) have all worked correctly since v5.1 — but nothing has ever invoked the endpoint on a recurring basis. This is a gap in delivery *infrastructure*, not a bug in the digest *logic*.

## Investigation

1. **Endpoint exists and is implemented correctly.** `POST /digest/si05/send` (`backend/routers/digest.py`) calls `send_si05_digest()` (`backend/services/si05_digest_service.py`), which fetches arc5-compliance data, formats the MarkdownV2 message, and sends it via the Telegram Bot API with retry/backoff (`_send_telegram_request`, 2 retries at 30s/60s). Every send attempt (success or failure) is logged to `si05_digest_log`. No defect found in this path.
2. **No scheduled trigger exists anywhere in the repo.** Searched `.github/workflows/*.yml` for any digest- or SI-05-related schedule: none found. `render.yaml` explicitly documents that Render cron requires a paid tier and that the one existing scheduled job (`alert-evaluation.yml`) uses GitHub Actions' free-tier `schedule` trigger instead — the same pattern was never applied to the SI-05 digest.
3. **Endpoint docstrings confirm the gap was known but unaddressed.** Both `digest.py` (`"Intended to be called by a weekly scheduler (Render cron or external scheduler)"`) and `docs/specs/api_contracts/digest_endpoints.md` (`"Intended for weekly cron/scheduled invocation"`) describe an intended trigger mechanism that was never built.
4. **The 2026-06-22 cadence review's "confirmed deliveries" were not automated.** `docs/product/decisions/si05-digest-cadence-review--2026-06-22.md` records deliveries on 2026-06-08, 2026-06-15, and a triggered delivery on 2026-06-17. Git history shows no digest-scheduling workflow was ever added or removed — these deliveries were manual/ad hoc invocations (e.g. `workflow_dispatch`-equivalent manual `curl` calls) made during Phase 1 development and verification, not evidence of a working recurring schedule. Once manual triggering stopped after the review closed, delivery stopped with it — consistent with `BLG-OPS-129`'s report of the digest going silent.

## Root Cause

**Missing automated trigger.** The SI-05 digest send path has always required something external to call it; that "something" was a person, not a schedule. No code defect exists in the send/format/retry/logging logic.

## Fix

Added `.github/workflows/si05-weekly-digest.yml` — a GitHub Actions scheduled workflow (`cron: '0 19 * * 0'`, 19:00 UTC Sunday, matching the cadence review's "Sunday evening, Europe/London" cadence) that calls `POST /digest/si05/send` with the `API_KEY` header, following the identical pattern already proven by `alert-evaluation.yml`. Also retains `workflow_dispatch` for manual triggering (testing, or an ad hoc re-send).

This uses the same `API_URL`/`API_KEY` GitHub Actions repo secrets already configured for `alert-evaluation.yml` and `daily-snapshot.yml` — no new secrets required.

## Verification

- CI-verifiable: the workflow YAML is syntactically valid and mirrors the working `alert-evaluation.yml` pattern (same secrets, same `curl -f` failure semantics).
- **Staging-only (not CI-reproducible):** confirming an actual live Telegram send from the new schedule (or a manual `workflow_dispatch` run against the deployed API) requires production credentials and cannot be verified in CI. Tracked as `BLG-OPS-132` (filed this story) — see `sprint_close.md` for this cycle. Per CLAUDE.md §2, this backlog item is filed before the PR opens since the corresponding AC ("SI-05 digest delivery confirmed working again — at least one successful send observed post-fix") is deferred to post-merge staging verification.

## Next Steps

- ~~Infrastructure & Operations Owner to trigger a manual `workflow_dispatch` run (or wait for the next scheduled Sunday run) after this PR merges, and record the outcome against `BLG-OPS-132`.~~ **Done — see Staging Verification below.**
- No further code or spec change identified as necessary — the fix is purely the missing trigger.

## Staging Verification (ST-19, EPIC-05, v8.4 — BLG-OPS-132, 2026-08-08)

`si05-weekly-digest.yml` manually triggered via `workflow_dispatch` (run [31247847064](https://github.com/sachiv1984/swing-trading-model/actions/runs/31247847064)) against the live production API.

**Evidence:**
1. **Endpoint response** (printed to the Actions run log): `{"status":"ok","sent":true,"message_length":456,"error":null}`
2. **`si05_digest_log` row** (queried directly by Infrastructure & Operations Owner via production DB access):
   ```
   id: 24, sent_at: 2026-08-08 08:11:21.85389+00, status: sent,
   event_count: 14, telegram_message_id: null, error_message: null
   ```
   `sent_at` matches the workflow run timestamp; `status = 'sent'`.
3. **Live Telegram message** — confirmed received by Infrastructure & Operations Owner (human check, not code-verifiable).

**Result: SI-05 digest delivery confirmed working.** Both AC evidence sources (`si05_digest_log` + live Telegram message) are satisfied. `BLG-OPS-132` closed.

**Follow-up finding (not blocking, filed separately):** `telegram_message_id` is `null` on this confirmed-successful row, and is `None` at *every* call site in `si05_digest_service.py` — `_send_telegram_request()` calls `urllib.request.urlopen()` but never reads the response body, so Telegram's own returned `message_id` (present in a successful API response) is discarded rather than stored. The column exists specifically to hold this value (`BLG-BE-33`) but has never been populated. Filed as a follow-up backlog item — see `prompt_change_log.md`-adjacent backlog entry for this cycle.

---

## Sign-Off

- Reviewed by: Infrastructure & Operations Owner
- Date: 2026-08-05
- Disposition: Root cause confirmed (missing scheduled trigger, not a code defect). Fix applied (`si05-weekly-digest.yml`). Live-send confirmation deferred to staging per `BLG-OPS-132`.

## Sign-Off — Staging Verification

- Reviewed by: Infrastructure & Operations Owner
- Date: 2026-08-08
- Disposition: Live send confirmed successful via endpoint response, `si05_digest_log` row, and direct Telegram receipt confirmation. `BLG-OPS-132` closed. No remaining action on the digest delivery fix itself; `telegram_message_id` population gap filed as a separate, non-blocking follow-up.
