**Owner:** Director of Quality
**Class:** Class 2
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-07-26
**Sprint Item:** ST-10 (BLG-QA-117, EPIC-10, v7.8)

---

# Flaky-Test Quarantine Process

## Purpose

No quarantine mechanism previously existed for intermittently-failing Playwright tests, so a flaky test could block unrelated PRs indefinitely with no tracked path to a fix. This document defines the quarantine tag/process (BLG-QA-117) and distinguishes it from the environment-conditional skips already used elsewhere in this suite.

## When to Quarantine

Quarantine a test when **all** of the following are true:
1. The test fails intermittently (not deterministically) — the same test, same code, same environment sometimes passes and sometimes fails.
2. The failure is confirmed unrelated to the change in the PR that triggered it (re-running the test in isolation, or on `main`, reproduces the same intermittent behaviour).
3. The flakiness blocks merge of unrelated work.

**Do not** use this mechanism for:
- Environment-conditional skips (e.g. `test.skip()` when a precondition element isn't present in a given environment — see `tests/e2e/keyboard-shortcuts.spec.js` for the existing pattern). Those are deterministic, not flaky, and are not in scope for this process.
- A test that fails deterministically due to a real regression — fix the regression or the test, don't quarantine.

## Quarantine Tag and Required Format

Use Playwright's built-in `test.fixme(condition, description)`, called as the **first line inside the test body** (so it always takes effect regardless of prior conditional logic), with a description in this exact format:

```javascript
test('SC-XYZ-01: some flaky scenario', async ({ page }) => {
  test.fixme(true, 'FLAKY-QUARANTINE: <one-line reason> — tracked in BLG-QA-<id>');
  // ... existing test body, left in place (not deleted) ...
});
```

**Required elements in the description string:**
- The literal prefix `FLAKY-QUARANTINE:` — makes quarantined tests grep-able (`grep -r "FLAKY-QUARANTINE:" tests/e2e/`) and distinguishes this from other uses of `test.fixme`/`test.skip` in the suite.
- A one-line reason (what's flaky, e.g. "timing-dependent assertion on animation completion").
- A tracked backlog reference (`BLG-QA-<id>`) — a quarantine with no filed follow-up item is not tracked, and per the enforcement rule below, is treated as a process violation.

**Why `test.fixme` over `test.skip`:** `test.fixme` semantically signals "this is expected to fail/is broken and needs a fix" (matching the flaky-test intent), while `test.skip` is already used in this suite for deterministic environment-conditional cases. Keeping the two conventions visually and semantically distinct avoids future confusion between "this legitimately can't run right now" and "this is flaky and needs investigation."

## Backlog Follow-Up (Required)

Every quarantine must have a corresponding backlog item filed via `/backlog-add` (owner: Director of Quality, or the domain owner of the flaky surface) before or in the same commit as the quarantine, tracking the investigation/fix. The backlog ID goes directly in the `test.fixme` description string (see format above) — this is the single source of truth linking the quarantine to its follow-up, rather than a separate registry that can drift out of sync.

## Review Cadence

Quarantined tests are not a permanent state. At each `groom backlog` pass (`claude/system/backlog_management_prompt.md`), the Director of Quality (or PMO Lead performing the grooming pass) should grep for `FLAKY-QUARANTINE:` across `tests/e2e/` and confirm each entry's referenced backlog item is still open and not stale-target. A quarantine whose backlog item has shipped should have its `test.fixme` line removed in the same PR that fixes the underlying flakiness.

## Enforcement

`tests/test_flaky_quarantine_format.py` (Python, run via the backend test suite for consistency with this repo's other lint-style tests — e.g. `test_lint_api_contract_headings.py`) scans `tests/e2e/*.js` for any `test.fixme(` call and asserts every one includes the `FLAKY-QUARANTINE:` prefix and a `BLG-QA-` (or other `BLG-*`) reference. This prevents an untracked quarantine (a `test.fixme` added without a follow-up item) from silently accumulating.

## Currently-Known Flaky Tests (at story implementation time)

None. A repo-wide scan for existing `test.skip(` usage (`tests/e2e/visual-snapshots.spec.js`, `tests/e2e/keyboard-shortcuts.spec.js`) found only deterministic, environment-conditional skips (missing precondition elements) — not flakiness — so none qualify for migration to this new mechanism. This process is defined and ready for the next flaky test that is identified; per the story's own AC ("applied to any currently-known flaky test, if one exists at implementation time"), there is none to apply it to today.

---

## Acceptance

- Accepted by: Director of Quality
- Date: 2026-07-26
