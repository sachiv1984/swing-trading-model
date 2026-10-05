Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-05

# QA Evidence Log — EPIC-05

**EPIC:** EPIC-05 — Spec & Data-Model Debt Clearance
**Cycle:** 2026-09-30__release-v9.9
**Sprint goal:** Ship a single canonical ATR/stop-recalculation implementation with timestamp visibility on `GET /positions` (`BLG-BE-135`), while clearing the queued backend, security, QA, governance, spec, and frontend debt items that make up the rest of v9.9's full-capacity scope.
**Test scenarios used:** `tests/test_check_data_model_drift.py`

## Process Deviation — Merged to main via EPIC-02's PR without its own merge gate

This EPIC's story commits were never merged through an EPIC-05 PR. They were made on the same linear branch history as EPIC-04's, which EPIC-02's branch was later cut on top of, so PR #1886 (merged as `362ff619`) carried them into `main`. Neither PR #1886's body nor `qa_evidence_EPIC-02.md` named any EPIC-05 story, so none of this EPIC's work received a Director of Quality review or Product Owner acceptance before reaching `main`.

- **Commits affected (this EPIC):** `3677d86e` (ST-33), `ebc23c14` (ST-34), `e0026238` (ST-31 escalation), `62eebdd8` (ST-32), `241db980` (ST-29/ST-30 delegation), `aba5e44b` (ST-28), `9bc5b07e` (ST-28 record).
- **Rule breached:** CLAUDE.md §2 — story commits must land on the branch matching their EPIC prefix; never merge a PR without QA sign-off and Product Owner acceptance.
- **State staleness also found:** `execution_state.json` still showed ST-33/ST-34 as `not_started` although both commits were on `main`. Backfilled 2026-10-05 (SHA, authored-timestamp `completed_utc`, spec references, `deviations_filed`) after re-verifying both stories' AC on `main`.
- **Disposition (user direction, 2026-10-05):** retroactive merge gate. The code stays on `main`; the sign-off block below is left blank for the Director of Quality. Product Owner acceptance must also be recorded. Also recorded in `qa_evidence_EPIC-02.md` and `qa_evidence_EPIC-04.md`.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-28 | `scripts/check_data_model_drift.py` | Read-only drift detector comparing the live schema with `data_model.md`; lists undocumented and missing objects. Of the 5 known divergence classes, the 2 still live (orphaned columns BLG-SPEC-150; missing index BLG-SPEC-148, still applying on staging) are reproduced. The other 3, already resolved in docs and live, are correctly reported clean. New findings filed as BLG-SPEC-178. | Covers AC-01 (5 known divergences reproduced), AC-02 (output lists undocumented and missing objects) | Pass with notes — 3 of 5 divergence classes no longer exist live, so the tool reports them clean rather than reproducing them | None (BLG-SPEC-178 incidental finding) |
| ST-29 | — | Not built. Delegated to Data Model & Domain Schema Owner (live DDL needs write access to the live DB). | 4 columns dropped live; Migration History updated | Pending — blocked_backend | DEL-20261001-02 |
| ST-30 | — | Not built. Delegated to Data Model & Domain Schema Owner (disposition decision + live DDL). | Disposition recorded; spec and live schema agree | Pending — blocked_backend | DEL-20261001-03 |
| ST-31 | — | Not built. Escalated: the AC needs an edit to `claude/roadmap/current_roadmap.md`, which is outside write scope. | SI-02 cross-reference; v9.7 ST-23 AC fully met | Pending — blocked_decision | ESC-EXEC-20261001-05 |
| ST-32 | `docs/specs/data_model.md#DS-19` | DS-19 Verification status rewritten to state what was confirmed live on staging, and when: both CHECK constraints and the unique index, via read-only user-approved queries. Header/footer version drift fixed in the same file. | Covers AC-01 (no "never run" claim; states what/where/when), AC-02 (header/footer versions in sync) | Pass | None |
| ST-33 | `docs/specs/api_contracts/ai_endpoints.md`, `docs/ops/external_api_dependency_register.md` | Corrected 4 citations in `ai_endpoints.md` plus CFM-03 in the dependency register from `BLG-BE-128` to `BLG-BE-129`. Documentation only. | Covers AC-01 (no misattributed BLG-BE-128 remains — re-verified by grep 2026-10-05), AC-02 (BLG-BE-128's own references untouched) | Pass — text-only change, verified by code review per CLAUDE.md §2's FI-P3-02 exception | None |
| ST-34 | `docs/specs/frontend/pages/notifications.md`, `docs/testing/alert_thresholds_empty_state_scenarios.md` | Dropped the trailing period from both empty-state headings in the spec and the scenario doc, matching shipped code and `design_system.md` §Data States. DEV-v9.7-ST05-01 marked Resolved citing ST-34/BLG-SPEC-169. | Covers AC-01 (both headings without trailing period — re-verified by grep 2026-10-05), AC-02 (DEV-v9.7-ST05-01 resolved with this item's ID) | Pass — wording-only, verified by code review per CLAUDE.md §2's FI-P3-02 exception | None (closes DEV-v9.7-ST05-01) |

**QA test coverage:**
- Scenarios run: `tests/test_check_data_model_drift.py` (ST-28). Re-run retroactively 2026-10-05 together with EPIC-04's tests: 22 passed.
- Regression areas checked: `data_model.md` (DS-19, version header/footer), `ai_endpoints.md`, dependency register, `notifications.md` empty states
- Known deviations: None found — all 4 done stories' deviation checks completed with nothing new to file. ST-34 closed the pre-existing DEV-v9.7-ST05-01. Process deviation above (merge-gate bypass) recorded separately; it is not a spec deviation.

---

## Standard Sign-Off Block

> Autonomous class (BLG-GOV-19) not applicable: Criterion 1 is unmet (ST-32's verification used live staging queries, per BLG-GOV-335; ST-29/ST-30/ST-31 are delegated). The merge-gate bypass above also needs human review. The EPIC is not yet `done` — 3 stories are still blocked.

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- Signed off by:
- Date:
- Comments: Retroactive merge gate. Director of Quality to review the 4 done stories already on `main` (via PR #1886) and complete this block. Product Owner acceptance still needs recording separately.
