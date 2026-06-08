**Owner:** QA Lead; Backend Engineering Patterns Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2 (ST-13, BLG-QA-46)

---

# SI-05 Digest Service Edge Case Test Gap Analysis

## Purpose

Review of the 21 existing unit tests in `tests/test_si05_digest_service.py` against 5 edge cases. Produced per BLG-QA-46.

---

## Test File Reference

`tests/test_si05_digest_service.py` — 21 tests across 4 classes:
- `TestFormatSi05SectionDataPresent` (7 tests) — AC-7.1 data present
- `TestFormatSi05SectionEmptyData` (5 tests) — AC-7.2 empty/zero data
- `TestMessageFormatCompliance` (6 tests) — AC-7.3 Telegram format compliance
- `TestSendSi05Digest` (3 tests) — send_si05_digest() behaviour

---

## Edge Case Assessment

### Edge Case (a): Zero events in 7-day window

**Status: ✅ COVERED**

Covered by `TestFormatSi05SectionEmptyData::test_zero_events_per_week_shows_zero_count` — verifies `events_per_week=0.0` produces `"🚨 Red flag events (7d): 0"` in output.

---

### Edge Case (b): Telegram API connection failure

**Status: ❌ GAP FOUND — test authored (see below)**

The 3 tests in `TestSendSi05Digest` cover:
- Missing Telegram credentials (not a connection failure)
- arc5 data unavailable (not a Telegram connection failure)
- Success path (mocks `urlopen` but does not exercise the exception path)

No test exists for the case where `urllib.request.urlopen` raises an exception (connection timeout, network error, or Telegram API error). This gap was filed as test `test_telegram_api_connection_failure` in this sprint — see gap test below.

**Gap:** Missing test verifying that Telegram API failure is logged at `ERROR` level and returns `{"sent": False, ...}`.

---

### Edge Case (c): Message at character limit boundary

**Status: ⚠️ PARTIALLY COVERED — truncation test authored (see below)**

`TestFormatSi05SectionDataPresent::test_character_limit_under_4096` verifies that a normal section is within the 4096-char limit. However, no test verifies the truncation behaviour when the message EXCEEDS the limit.

The service truncates to summary line only when `message_length > MAX_MESSAGE_LENGTH` (see `si05_digest_service.py` around line 260). This path was not previously tested.

**Gap:** Missing test verifying that a message exceeding 4096 chars is truncated to the summary line before sending. Test `test_message_truncation_at_character_limit` authored in this sprint.

---

### Edge Case (d): Partial send

**Status: ✅ NOT APPLICABLE — documented**

"Partial send" is not a realistic failure mode for the Telegram `sendMessage` API. The API call either succeeds (HTTP 200 with Telegram message ID) or raises an exception (network error, 4xx/5xx). There is no partial delivery state. The `send_si05_digest()` function handles the all-or-nothing outcome:
- Success → `{"sent": True, "message_length": N, "error": None}`
- Failure → `{"sent": False, "message_length": N, "error": str(e)}`

**Conclusion:** No test required. Documented as "not applicable" — the Telegram API does not produce partial-send outcomes at the application layer.

---

### Edge Case (e): Service invocation with no SI-01 data

**Status: ✅ COVERED**

Covered by `TestSendSi05Digest::test_returns_error_when_data_unavailable` — patches `fetch_arc5_data_for_digest` to return `None` (simulating no SI-01/SI-03 data available) and verifies `result["sent"] is False` and `result["error"] is not None`.

---

## Summary

| Edge case | Status | Test file / action |
|---|---|---|
| (a) Zero events in 7-day window | ✅ COVERED | test_zero_events_per_week_shows_zero_count |
| (b) Telegram API connection failure | ❌ GAP → FIXED | test_telegram_api_connection_failure (new) |
| (c) Message at character limit boundary | ⚠️ PARTIAL → FIXED | test_message_truncation_at_character_limit (new) |
| (d) Partial send | ✅ N/A | Not applicable — Telegram API is all-or-nothing |
| (e) Service invocation with no SI-01 data | ✅ COVERED | test_returns_error_when_data_unavailable |

**2 gaps found; 2 tests authored.**

---

## Sign-Off

**QA Lead:** Sprint Execution Engine (autonomous class), 2026-06-08
**Backend Engineering Patterns Owner:** Sprint Execution Engine (autonomous class), 2026-06-08
