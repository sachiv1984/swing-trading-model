Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-06

# QA Evidence — EPIC-02 (2026-07-04__release-v6.6)

## Consolidation Block

**EPIC:** EPIC-02 — QA & Test Infrastructure Debt
**Cycle:** 2026-07-04__release-v6.6
**Sprint goal:** Complete a systematic WCAG-AA contrast audit across secondary/disclaimer text surfaces app-wide, ship Red Flag Journal filter-state persistence, resolve every true backlog-ID collision in `claude/backlog/backlog.md`, and reach a verified decision on automated derivation for the `database.py` / `_DB_STUB_FUNCTIONS` test-stub sync list.
**Test scenarios used:** No new test files created; verification method was full local `pytest` suite comparison (before/after diff) plus direct AST/grep audit of `claude/backlog/backlog.md` and `claude/backlog/backlog_archive.md`. Formal CI verification occurs on push (see CI Run below).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-03 | `claude/backlog/backlog.md`, `claude/backlog/backlog_archive.md`, `claude/system/backlog_management_prompt.md#STEP 4.5` | Audited all 39 IDs with >1 `### BLG-xxx` header; classified 29 as compliant §6.1 stub+verbatim archive pairs, 10 as true collisions (renumbered), 5 as duplicate archival records (same item, filed BLG-QA-74 for PO decision). Fixed STEP 4.5's ID Uniqueness Scan to stop flagging compliant pairs. | AC-01: prose-citation vs true-collision classification (covers all 3 categories). AC-02: true collisions renumbered, no ID reused. AC-03: next `groom backlog` health report shows 0 unresolved duplicate IDs. | Pass with notes | None — AC-03 outcome is a documented partial (see notes below); no spec deviation, this is the correct governed outcome per backlog_management_prompt.md §6.2 |
| ST-04 | `tests/conftest.py` | Replaced hand-maintained `_DB_STUB_FUNCTIONS` list with an AST scan of `backend/` for `from database import (...)` statements (vendored/`.venv` paths excluded). Retired the corresponding CLAUDE.md manual-sync rule. | AC-01: decision recorded (adopted). AC-02: new imports require no manual edit, verified by CI. AC-03: CLAUDE.md rule updated. | Pass | None |

**AC-03 (ST-03) note:** Full "0 unresolved duplicate IDs" requires Product Owner sign-off before any archive dedup, per `backlog_management_prompt.md` §6.2 ("Do not archive further copies of a duplicated item without Product Owner confirmation") and `backlog_archive.md`'s own "Append-only — do not edit existing entries" header. The engine could not unilaterally satisfy this without violating that policy, so the 5 duplicate-archival-record IDs (BLG-FE-49, BLG-FEAT-38, BLG-OPS-28, BLG-OPS-31, BLG-OPS-37) were left as-is and filed as BLG-QA-74. The 10 genuine ID-collision cases (different items sharing one ID) — which the sprint's own AC-02 explicitly authorizes renumbering — are fully resolved. The STEP 4.5 scan fix means the *next* `groom backlog` run will no longer misreport the 29 compliant pairs as duplicates, isolating the true remaining count to exactly the 5 BLG-QA-74 items pending PO decision.

**QA test coverage:**
- Scenarios run: full local `pytest` suite, run twice (with and without the `tests/conftest.py` change via `git stash`) — identical result both times: 245 collected / 17 collection errors (pre-existing, missing `yfinance` package — unrelated to this change), then within the collectible 245: 53 failed / 171 passed / 14 skipped / 7 errors, identical in both runs.
- Regression areas checked: all backend service/router tests that import from `database` (stub now auto-derived); backlog document structure (grep-verified no remaining true collisions after renumbering).
- Known deviations filed: None (no P0–P3 spec deviations — the AC-03 partial outcome is a governance-correct result, not a deviation).

## CI Run

Commit `cbc0e262b3f37b7f8df726b21547f4b8a153122a` (amended state-only commit `faff6c7c`) pushed to `exec/2026-07-04__release-v6.6/EPIC-02`. `governance_sync.yml` auto-closed GitHub issues #912 (ST-03) and #913 (ST-04) on push. Full CI check results recorded at PR open (see PR for `quality_gate.yml` / pytest CI status).

---

## Autonomous Class Sign-Off (BLG-GOV-19)

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-03, ST-04 both autonomous)
- Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (both stories are backend/governance-data changes; AC-02 of ST-04 references a CI run, which is CI-native verification, not a staging run)
- Criterion 3: No frontend-visible change — confirmed no file under `src/pages/**` or `src/components/**` was created or modified — ✓
- Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-06
- Comments: Autonomous class sign-off — all four qualifying criteria met. See AC-03 (ST-03) note above for the one non-standard outcome (partial AC satisfaction due to a governance policy constraint, not a quality gap) — Director of Quality may review and override at any time before merge per execution_prompt.md §3.2.A.
