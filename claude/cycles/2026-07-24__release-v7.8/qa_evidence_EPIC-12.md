Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-26

# QA Evidence — EPIC-12 (v7.8)

**EPIC:** EPIC-12 — Automated lint check for API contract `##` heading level
**Cycle:** 2026-07-24__release-v7.8
**Sprint goal:** Ship all 12 v7.8 EPICs with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_lint_api_contract_headings.py`

## ST-12 — Add CI lint step for API contract heading-level compliance

**Spec reference:** `.github/workflows/openapi-drift.yml`, `scripts/lint_api_contract_headings.py` (new artefacts, Cases D and B)
**Commit:** `bf81e730` (implementation `1cd59c2e`)

**What was built:** `scripts/lint_api_contract_headings.py` scans `docs/specs/api_contracts/*.md` for any HTTP-method+path-shaped heading not at exactly the canonical `##` (depth-2) level — the exact silent-fail case documented in CLAUDE.md §2, where the existing OpenAPI Drift Detection gate only matches literal `## ` headings and silently ignores any other depth. Added as a new step in `openapi-drift.yml` running before the existing drift-detection step, satisfying "runs ahead of/alongside." Running the new lint against the real contracts directory surfaced 2 depth-3 headings in `ai_advisory_contract_checklist.md`; investigation confirmed these are legitimate nested subsections of a checklist template (not a silent-fail bug — the real canonical contract for those endpoints is `ai_endpoints.md`), so a documented single-file exemption was added rather than a broader/less precise regex.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-12 | `lint_api_contract_headings.py`, `openapi-drift.yml` | Heading-depth lint script + CI step | Lint step added scanning for `## METHOD /path` heading-level compliance, catches the `###`-level silent-fail case | Pass | None |
| ST-12 | (same) | Negative test in `tests/test_lint_api_contract_headings.py` | Lint step confirmed to catch a deliberately-miscoded test heading before merge | Pass — `test_deliberately_miscoded_heading_is_caught` | None |
| ST-12 | (same) | New step placed before "Detect drift" in the same job | Lint step runs ahead of/alongside the existing OpenAPI Drift Detection gate | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_lint_api_contract_headings.py` — 7 tests: correctly-leveled heading (no violation), the required negative test (deliberately miscoded `###` heading, caught), a too-shallow (`#`) heading also caught, multiple violations all reported, non-endpoint headings ignored regardless of depth, multiple correctly-leveled methods produce no violations, and a regression guard confirming the real `docs/specs/api_contracts/` directory lints clean today (with the one documented exemption applied). All 7 pass.
- Regression areas checked: full backend suite (761 tests) — all pass, no behavioural change elsewhere.
- Known deviations filed: None.

## Autonomous class eligibility check (BLG-GOV-19)

- Criterion 1 (all stories autonomous): ✓ — ST-12 is the only story, classified `autonomous`.
- Criterion 2 (all AC verifiable by code review/tests alone): ✓.
- Criterion 3 (no frontend-visible change): ✓ — only `scripts/`, `tests/`, and `.github/workflows/` touched.
- Criterion 4 (engine signer field populated): ✓.

**All four criteria met — autonomous class applies.**

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-26
- Comments: Autonomous class sign-off — all four qualifying criteria met. No named-authority sign-off is required by this story's own AC (unlike ST-07/ST-08 in this same sprint).
