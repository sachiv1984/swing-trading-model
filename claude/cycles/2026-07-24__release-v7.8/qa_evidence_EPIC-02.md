Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-26

# QA Evidence — EPIC-02 (v7.8)

**EPIC:** EPIC-02 — Automated Telegram changelog digest after each release
**Cycle:** 2026-07-24__release-v7.8
**Sprint goal:** Ship all 12 v7.8 EPICs with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_changelog_digest_service.py`

## ST-02 — Send Telegram digest of shipped items on post-ship closure

**Spec reference:** `claude/system/post_ship_closure.md#STEP 1.5`, `backend/services/changelog_digest_service.py` (Case B)
**Commit:** `90fd8e37` (implementation `a41757e3`)

**What was built:** `backend/services/changelog_digest_service.py` parses `docs/product/changelog.md` for a release's `### Changes shipped` table and sends a Telegram MarkdownV2 digest, reusing the existing `si05_digest_service.py` POST+JSON+retry infrastructure (shipped v2.4/v5.1) rather than a new send path. `scripts/send_changelog_digest.py` provides the CLI entry point wired into `post_ship_closure.md`'s new STEP 1.5 (between STEP 1 Changelog Entry and STEP 2 Roadmap Update). `send_changelog_digest()` never raises — a failed send (missing credentials, Telegram API error, missing changelog) is logged and returned as a non-fatal result dict.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-02 | `post_ship_closure.md#STEP 1.5` | New STEP 1.5, invokes `send_changelog_digest.py` | Digest sent automatically as part of Post-Ship Closure, reusing existing Telegram infrastructure (v2.4) | Pass | None |
| ST-02 | `changelog_digest_service.py` | `extract_changes_shipped()` parses the exact changelog table | Digest content matches the release's `### Changes shipped` entries in changelog.md | Pass | None |
| ST-02 | (same) | `send_changelog_digest()` catches all exceptions, never raises | Failure to send does not block Post-Ship Closure — logged, not fatal | Pass — unit-tested explicitly (`test_send_changelog_digest_failure_does_not_raise`) | None |

**QA test coverage:**
- Scenarios run: `tests/test_changelog_digest_service.py` — 10 tests covering extraction (most-recent version, specific version by prefix, unknown version, empty changelog), MarkdownV2 escaping, no-credentials path, successful send, send-failure-does-not-raise, missing-changelog-file, and a live integration check against the real `docs/product/changelog.md`. All 10 pass. CLI script (`scripts/send_changelog_digest.py`) manually verified end-to-end via the project venv (graceful no-credentials path, exit code 0 always).
- Regression areas checked: full backend suite (764 tests) — all pass, no behavioural change to `si05_digest_service.py` (imported, not modified) or any other module.
- Known deviations filed: None.

**Governance file edit (CLAUDE.md §6):** `post_ship_closure.md` v2.18→v2.19 modified as part of this story. Full checklist applied in the implementation commit: file's own version bumped + companion changelog entry (`post_ship_closure_changelog.md`), `OPERATIONAL_GUIDE.md` §10 source prompt header + §14 governance table row + §14 self-metadata version (4.109→4.110) all updated, `prompt_change_log.md` appended. Verified self-consistent via the `governance-drift` skill before committing (all three self-consistency checkpoints — header, §14 self-row, Change Log top row — confirmed matching at 4.110/2026-07-26).

## Autonomous class eligibility check (BLG-GOV-19)

- Criterion 1 (all stories autonomous): ✓ — ST-02 is the only story, classified `autonomous`.
- Criterion 2 (all AC verifiable by code review/tests alone): ✓ — no UI surface, no staging run required.
- Criterion 3 (no frontend-visible change): ✓ — only `backend/services/`, `scripts/`, `tests/`, and `claude/system/` (governance) touched.
- Criterion 4 (engine signer field populated): ✓.

**All four criteria met — autonomous class applies.**

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-26
- Comments: Autonomous class sign-off — all four qualifying criteria met. No named domain authority beyond standard Director of Quality is named in this story's AC.
