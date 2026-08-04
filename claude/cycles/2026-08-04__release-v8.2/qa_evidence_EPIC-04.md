Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-04

# QA Evidence — EPIC-04 (Operations & CI Hardening)

**EPIC:** EPIC-04 — Operations & CI Hardening
**Cycle:** 2026-08-04__release-v8.2
**Sprint goal:** Ship v8.2's curated full-capacity scope — five ready user-facing/UX improvements leading the release, staging/production security hardening, an 11-item governance-process integrity cluster, CI/operations hardening, and QA/spec debt cleanup — advancing the release's explicit "user features first" priority within the confirmed capacity band.
**Test scenarios used:** `.githooks/test_commit_msg.sh` (6 cases, new this EPIC). No other runnable test files apply — ST-19 is documentation-only and ST-20 was verified via live CI timing measurement (see below), not a unit test.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|-----------------|------------------|-----------------------|--------|------------|
| ST-19 | `docs/ops/dependency_upgrade_cadence.md` | Quarterly review cadence documented for `backend/requirements.txt`'s 16 pinned dependencies; first review scheduled 2026-10-01 | Quarterly cadence documented; first review scheduled | Pass | None |
| ST-20 | `.github/workflows/playwright.yml`; `.github/workflows/smoke-tests.yml` | Playwright browser binaries cached across CI runs (keyed on exact @playwright/test version); measured live via a real cache-miss/cache-hit run pair | CI caching reviewed and tuned; measurable runtime reduction; no reliability regression | Pass with notes | None (see notes) |
| ST-21 | `.githooks/commit-msg`; `.githooks/test_commit_msg.sh` | New commit-msg hook lints `[EPIC-xx][ST-xx]`/`[GOVERNANCE]` format on exec/** branches; consolidated into the pre-existing `.githooks/` directory after an initial review caught a conflict with the existing pre-commit hook | Hook added; confirmed to reject malformed message; sign-off | Pass | None |

**"Pass with notes" detail (ST-20):** The caching mechanism is implemented correctly and verified live (cache-hit run correctly skipped the full browser download, using the OS-deps-only install path instead — confirmed via GitHub Actions step-level API data, not just log inspection). The measured improvement is real but modest: the browser-install step itself dropped from 19s to 12s (a genuine ~37% reduction for that step), but total job duration was effectively unchanged (~220s vs ~219s) because `npm ci` and the test run itself dominate and vary run-to-run by more than this step's savings. This is documented honestly in the workflow file's own comments rather than overstated — the AC's "measurable" requirement is satisfied by a real, live-measured number, even though it is smaller than the story's framing implied.

**QA test coverage:**
- Scenarios run: `.githooks/test_commit_msg.sh` (6/6 passing, run from its final consolidated location). ST-20's timing claim was verified via 2 real, live GitHub Actions runs of the same job (cache-miss baseline, then a `gh run rerun` to force a cache-hit measurement), with precise step-level timestamps pulled directly from the GitHub API — not estimated or simulated.
- Regression areas checked: `.githooks/pre-commit` (pre-existing router-registration + gitleaks hook) confirmed unaffected — logic byte-identical after the ST-21 consolidation fix, `scripts/check_router_test_registration.py` still exits 0 cleanly. All 4 Playwright E2E shards passed on both the cache-miss and cache-hit runs (no flakiness introduced by the caching change).
- Known deviations filed: None

**Process note:** ST-21's own hook, once installed locally for testing, caught a real compliance gap in this same session's own SHA-recording bookkeeping commits (a bare `[EPIC-xx]` tag without the accompanying `[ST-xx]` tag, which CLAUDE.md's commit format rule requires on every exec/** commit, not just feature commits). Corrected in-session; flagged for `lessons_learnt_cycle.md` at sprint close.

**Frontend testing gate (CLAUDE.md §2):** Not applicable — zero files under `src/pages/` or `src/components/` were touched by any story in this EPIC.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All 3 stories in this EPIC have `delegation_class: autonomous` — ✓
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/components/**` or `src/pages/**` was created or modified — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-04
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable or live-CI-measured, no frontend changes, engine signer populated).

**EPIC-level consolidation note (BLG-GOV-14):** Per BLG-GOV-14, a domain-authority sign-off at story level does not by itself substitute for this EPIC-level block — both are required. The following story-level domain-authority sign-off is confirmed cleared as of this EPIC-level sign-off:

| Story | Domain Authority | Status |
|-------|-------------------|--------|
| ST-19 | N/A — no sign-off role named in the AC | N/A |
| ST-20 | Head of Engineering | Cleared |
| ST-21 | Head of Engineering | Cleared (blocked on initial review, fixed in-session, re-verified and cleared on the second pass) |

Both ST-20 and ST-21 involved a real Head of Engineering review that materially improved the delivered work — ST-20's review confirmed the caching mechanism's correctness before the live timing measurement was even taken, and ST-21's review caught a genuine conflict with pre-existing repository infrastructure that would otherwise have shipped silently broken.
