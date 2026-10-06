Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-05

# QA Evidence Log — EPIC-02

**EPIC:** EPIC-02 — Operational Reliability & Security Hardening
**Cycle:** 2026-09-30__release-v9.9
**Sprint goal:** Ship a single canonical ATR/stop-recalculation implementation with timestamp visibility on `GET /positions` (`BLG-BE-135`), while clearing the queued backend, security, QA, governance, spec, and frontend debt items that make up the rest of v9.9's full-capacity scope.
**Test scenarios used:** `tests/test_non_registry_dependency_check.py`, `tests/test_daily_cost_alert.py`, `tests/test_ai_endpoint_anomaly_service.py`, `tests/test_price_alerts_service.py`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-06 | `scripts/check_non_registry_dependencies.py`, `tests/test_non_registry_dependency_check.py` | Closed 2 residual gaps in the non-registry dependency guard: (1) added `_PIP_BARE_DOT_PATH_RE` so bare `-e .`/`-e ..` (no trailing slash) are rejected, previously missed by the trailing-slash-requiring `_PIP_LOCAL_PATH_RE`; (2) added `_file_url_is_within_repo()` so a legitimate npm-workspace-local `file:` lockfile entry (resolved path stays within the repo) is no longer a false positive, while a genuine non-workspace `file:`/git resolved URL is still flagged. | `-e .`/`-e ..` rejected by a test; synthetic workspace-local `file:` entry confirmed not flagged while a non-workspace one still is | Pass | None |
| ST-07 | `backend/services/gemini_service.py`, `backend/database.py` | Added `database.py`'s `scheduled_alert_dedup` table (additive, idempotent `CREATE TABLE IF NOT EXISTS`, applied at app startup — no manual DB step) plus `get_last_alert_fingerprint`/`record_alert_fingerprint` helpers. `check_and_alert_daily_cost()` fingerprints by UTC date; a second same-day call with the threshold still exceeded does not re-send. | A second call on the same UTC day, after an alert already sent for a still-exceeded threshold, does not send a second Telegram message | Pass | None |
| ST-08 | `backend/services/ai_endpoint_anomaly_service.py` | Reuses ST-07's `scheduled_alert_dedup` table. `run_scheduled_anomaly_check()` fingerprints by the set of firing `(endpoint, metric)` pairs; a second call within the same firing window does not re-send. A changed firing set is treated as new; when nothing is firing, the stored fingerprint is cleared so a later identical-signature recurrence still alerts. | A second call within the same firing window, with the same anomalies still firing, does not send a second Telegram message | Pass | None |
| ST-09 | `backend/services/alerts_service.py`, `alerts_endpoints.md#POST /price-alerts` | `create_price_alert()` now checks for an existing **active** alert with the same `(portfolio_id, ticker, condition, threshold_price)` before inserting; a double-submit returns the existing alert. A past (inactive/triggered) alert with the same values does not block a new one. Not DB-unique-constraint-backed — closes the sequential double-submit case, not a true concurrent race (same limitation as the adjacent, pre-existing active-alert cap check). `alerts_endpoints.md`'s Idempotency subsection updated (v0.12→v0.13), closing `BLG-OPS-174`. | A double-submit of the same `(ticker, condition, threshold_price)` while the first alert is still active does not create a second active alert | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_non_registry_dependency_check.py` (ST-06, 36 tests, +4 new), `tests/test_daily_cost_alert.py` (ST-07, 7 tests, +2 new), `tests/test_ai_endpoint_anomaly_service.py` (ST-08, 16 tests, +3 new), `tests/test_price_alerts_service.py` (ST-09, 26 tests, +2 new)
- Regression areas checked: full backend suite run after this EPIC's commits — 1992 passed, 12 skipped (same pre-existing, unrelated skips tracked under ST-10/EPIC-03 in this sprint, confirmed present before this EPIC's first commit)
- Known deviations: None found — all 4 stories' deviation checks completed with nothing to file

---

## Standard Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-06/07/08/09 all autonomous)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run, no live system interaction — ✓ (all 4 stories verified via unit tests against mocked DB cursors; no live DB/staging access used or required for verification)
- [x] Criterion 3: No frontend-visible change — ✓ (no file under `src/pages/` or `src/components/` created or modified; all 4 stories are backend-only)
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-10-05
- Comments: Autonomous class sign-off — all four qualifying criteria met. This EPIC-level block does not itself satisfy the STEP 4 merge gate's separate "QA sign-off comment from Director of Quality on PR" and "Product Owner acceptance" rows — both remain always-human per `execution_prompt.md` §5.3 and are expected to halt at STEP 4 pending human action.

---

## Process Deviation — PR #1886 also carried EPIC-04 and EPIC-05 commits (recorded 2026-10-05)

This EPIC's branch was cut on top of a linear history that already held EPIC-04's commits (ST-19–ST-27, `018f5c1c`..`53842d71`) and EPIC-05's (ST-28–ST-34, `3677d86e`..`9bc5b07e`). When PR #1886 merged (`362ff619`), those 19 commits (12 `[EPIC-04]`, 7 `[EPIC-05]`; corrected 2026-10-05 from a mis-stated 17, per the PR #1891 review) went into `main` with it. The PR body and this log listed only ST-06–ST-09, so the autonomous-class sign-off above covers **only** ST-06–ST-09. It does not extend to any EPIC-04 or EPIC-05 content.

- **Rule breached:** CLAUDE.md §2 — story commits must land on the branch matching their EPIC prefix (documented here and in both other EPICs' QA logs, per that rule).
- **Disposition (user direction, 2026-10-05):** retroactive merge gate. The code stays on `main`; `qa_evidence_EPIC-04.md` and `qa_evidence_EPIC-05.md` record the bypass and carry blank Director of Quality sign-off blocks for after-the-fact review. ST-06–ST-09's own evidence and result above are unaffected.
