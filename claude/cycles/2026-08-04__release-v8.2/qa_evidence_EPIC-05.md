Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-04

# QA Evidence — EPIC-05 (QA & Spec Debt Cleanup)

**EPIC:** EPIC-05 — QA & Spec Debt Cleanup
**Cycle:** 2026-08-04__release-v8.2
**Sprint goal:** Ship v8.2's curated full-capacity scope — five ready user-facing/UX improvements leading the release, staging/production security hardening, an 11-item governance-process integrity cluster, CI/operations hardening, and QA/spec debt cleanup — advancing the release's explicit "user features first" priority within the confirmed capacity band.
**Test scenarios used:** `tests/test_system_status_endpoint_count.py` (2 cases, new this EPIC); full backend regression suite (`backend/.venv/bin/python3 -m pytest -q`, 952 passed / 5 skipped, run before and after ST-24's removal to confirm no behaviour change).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|-----------------|------------------|-----------------------|--------|------------|
| ST-22 | `stage4_backlog_slice.md#ST-22` | New `tests/test_system_status_endpoint_count.py` — AST-parses `backend/routers/test.py`'s `test_cases` list length (110) and regex-extracts `src/pages/SystemStatus.js`'s hardcoded fallback (110); asserts equality. Second test writes a synthetic stale fallback to a `tmp_path` copy and asserts the drift check catches it. | Snapshot/assertion test added comparing fallback to AST-derived count; test fails on a deliberately-stale value; QA & Testing Owner sign-off | Pass | None |
| ST-23 | `stage4_backlog_slice.md#ST-23` | 13 missing rows (v3.1–v3.13) reconstructed in `claude/system/changelogs/sprint_planning_changelog.md` from `git log -p` on `sprint_planning_prompt.md`, inserted newest-first between the existing v3.14 and v3.0 rows, each tagged with its source commit hash | All 13 rows added, newest-first, consistent with surrounding rows, using `git log -p` as source; Head of Specs Team sign-off | Pass | None |
| ST-24 | `stage4_backlog_slice.md#ST-24` | Removed the dead-code duplicate `@app.post("/test/endpoints")` handler and its unused `test_all_endpoints` import from `backend/main.py`; removed the companion test that exercised the dead handler directly (`tests/test_st04_implicit_200_error_paths_fixed.py`) | Duplicate handler removed; `routers/test.py`'s route remains sole handler; full regression suite passes with no behaviour change | Pass | None |
| ST-25 | `stage4_backlog_slice.md#ST-25` | New motion/timing-sensitive interaction note added to `design_gate_prompt.md` §6 Design Requirement Classification (chart animations, tooltip delay timing, debounce/throttle windows always Design Required) | Explicit checklist item added to classification table; Head of UX & Design sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_system_status_endpoint_count.py` (2/2 passing); full backend suite (952 passed, 5 skipped) run twice — once after ST-24's removal to confirm zero regression, once as the EPIC's final consolidated run.
- Regression areas checked: `backend/routers/test.py`'s live `POST /test/endpoints` route confirmed untouched and still the sole handler for that path; `tests/e2e/system-status.spec.js`'s `SC-SS-01b` scenario (which independently expects the "110 endpoints" fallback text) cross-checked for consistency with ST-22's AST-derived count — no update needed since ST-22 didn't change the fallback value, only added a test guarding it.
- Known deviations filed: None

**Process note (ST-23):** This closes `BLG-SPEC-110`, filed during `2026-08-03__release-v8.1` EPIC-03/ST-05 when the changelog gap (prompt header at v3.13, changelog at v3.0) was first discovered. Reconstruction independently fact-checked by the Head of Specs Team agent-mediated review (5 of 13 rows spot-checked against `git show`/`git log -1 --format=%B`, plus a specific verification of the v3.6 parallel-branch-collision claim).

**Frontend testing gate (CLAUDE.md §2):** Not applicable — zero files under `src/pages/` or `src/components/` were touched by any story in this EPIC.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All 4 stories in this EPIC have `delegation_class: autonomous` — ✓
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/components/**` or `src/pages/**` was created or modified — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-04
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable or test-verified, no frontend changes, engine signer populated).

**EPIC-level consolidation note (BLG-GOV-14):** Per BLG-GOV-14, a domain-authority sign-off at story level does not by itself substitute for this EPIC-level block — both are required. The following story-level domain-authority sign-offs (agent-mediated per `execution_prompt.md` §5.3) are confirmed cleared as of this EPIC-level sign-off:

| Story | Domain Authority | Status |
|-------|-------------------|--------|
| ST-22 | QA & Testing Owner | Cleared — PASS (independently re-derived both the AST count and fallback value, confirmed the stale-value test genuinely exercises the failure path via a real `tmp_path`-based re-run of the extraction logic, not a stub) |
| ST-23 | Head of Specs Team | Cleared — PASS (independently re-ran `git log --follow` and spot-checked 5 of 13 reconstructed rows against `git show`/commit messages, including a specific check on the v3.6 parallel-branch-collision claim) |
| ST-24 | Head of Engineering | Cleared — PASS (independently re-derived the route-shadowing/dead-code claim from `include_router` ordering rather than trusting the commit message; confirmed regression suite matches baseline exactly, 952 passed / 5 skipped) |
| ST-25 | Head of UX & Design | Cleared — PASS WITH ADVISORY NOTE (confirmed §6 text is unambiguous and non-duplicative of the existing "when in doubt" line; confirmed §6 placement is defensible given STEP 1 already directs readers to §6; noted as a non-blocking strengthening opportunity that a one-line STEP 1 cross-reference could add defense-in-depth — not required for this AC; full CLAUDE.md §6 checklist compliance independently verified across all 4 locations) |

All four story-level reviews were real, independent verification passes (re-deriving claims from source rather than trusting commit messages) — none surfaced a blocking finding. ST-25's advisory note is recorded for awareness but does not block sign-off, as the story's AC ("explicit checklist item added to the classification table") is fully met by the current placement.
