Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21

## Consolidation Block

**EPIC:** EPIC-04 — QA Coverage, Accessibility & Cost/Quality Visibility Expansion
**Cycle:** 2026-08-21__release-v9.0
**Sprint goal:** Close out the correctness and data-integrity follow-through surfaced directly by v8.9's own PR-review process, while hardening operational resilience (deploy-path and staging safeguards) and expanding QA and cost/capacity hygiene coverage.
**Test scenarios used:** `tests/test_r_multiple_calculation.py`, `tests/e2e/accessibility-axe-scan.spec.js`, `tests/e2e/visual-regression-baselines.spec.js`, `tests/test_generate_backend_coverage_report.py`, plus the pre-existing suites cross-referenced by the ST-17/ST-20 QA-document refresh stories (`tests/e2e/si01-si03-integration.spec.js`, `tests/e2e/red-flag-journal.spec.js`, `tests/e2e/arc5-compliance-section.spec.js`, `tests/e2e/reports-si02-gate-status.spec.js`, `tests/e2e/si04-version-comparison.spec.js`, `tests/e2e/weekly-digest.spec.js`, `tests/e2e/trade-plan.spec.js`)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-17 | `docs/qa/arc5_qa_protocol.md` (new) | Canonical arc-level Arc 5 QA protocol covering the full flow (validation gate → override event → red flag journal → drift detection review → strategy version comparison → weekly digest), consolidating/extending `arc5_e2e_integration_test_spec.md` and `arc5_coverage_audit.md` rather than duplicating them; corrected a stale SI-04 status in `arc5_qa_completion_criteria.md`'s prior assessment; documented SI-02 frontend's partial consumption (`SI02GateStatusSection`, `BLG-FEAT-86`) accurately rather than as flat non-existence | Arc 5 E2E protocol document produced and filed; core happy path covered by Playwright; BLG-QA-26 trigger gate (already cleared 2026-06-16 per `arc5_qa_completion_criteria.md`) reconfirmed, not re-litigated | Pass | None — 30/34 shipped-scope scenarios (88.2%) Playwright-automated; 4 manual (staging-only) scenarios inherited unchanged from `arc5_e2e_integration_test_spec.md`; drift-review substantive UI correctly documented as not-yet-shipped, not fabricated |
| ST-18 | `tests/e2e/visual-regression-baselines.spec.js` (new); `playwright.config.js`; `playwright.visual-regression.config.js` (new) | First pixel-level `toHaveScreenshot()` baselines in the repo: dual-theme (dark+light) baselines for 4 representative contrast-sensitive pages (DashboardHome, Positions, TradePlan, Settings) plus dual-theme PerformanceAnalytics baselines as the chart-heavy end-to-end proof of pattern | Baselines captured for components touched by BLG-FE-87/88/89 contrast remediation (represented by the 4-page cross-section); baselines captured for ≥1 chart-heavy component end-to-end | Pass | None — wired as an advisory-only CI job (`continue-on-error: true`) rather than blocking, per this repo's own established precedent (`visual-snapshots.spec.js`'s prior conversion away from pixel snapshots for exactly this cross-environment-rendering reason); documented as a deliberate, disclosed choice, not an omission |
| ST-19 | `docs/specs/metrics_definitions.md#R-Multiple (Canonical Server-Side)` | `tests/test_r_multiple_calculation.py` — regression coverage for `AnalyticsService.calculate_r_multiple_distribution`: hand-computed known-fixture distributions, bucket-range boundary counts, all 3 qualifying-condition exclusions, the <5-trades insufficient-data path, and the Cross-Currency Normalization invariant (mixed USD/GBP fixture, byte-identical aggregates regardless of `fx_rate`) | Server-side R-multiple formula has regression coverage locking behaviour against the canonical spec | Pass | None — no explicit sign-off role named in this story's own AC; test shape follows the spec's own prescribed "Validation" note verbatim |
| ST-20 | `docs/qa/arc5_coverage_audit.md` | Refreshed the Arc5ComplianceSection Playwright coverage audit to value-formatting granularity (fmtRate/fmtCount/fmtText + null-handling); added the previously-missing SC-ARC5-05 row (BLG-QA-58, v5.7); found and filed 3 new gaps (GAP-ARC5-06/07/08 → BLG-QA-154/155/156) | Coverage gap audit refreshed at value-formatting granularity; new gaps filed as backlog items | Pass | None — QA Lead review caught and required correction of a factual mischaracterization (GAP-ARC5-02's disposition), fixed same-session, re-review Approved |
| ST-21 | `tests/e2e/accessibility-axe-scan.spec.js` (new) | Standalone `@axe-core/playwright` CI scan across 4 representative pages (DashboardHome, Positions, TradePlan, Settings); `KNOWN_VIOLATIONS` baseline map for the 5 genuine pre-existing serious/critical violations found on introduction | Automated accessibility scan added to CI, ≥3 pages, only serious/critical violations block, pre-existing debt grandfathered not silently hidden | Pass | 5 pre-existing accessibility violations found and filed (BLG-FE-165 through BLG-FE-169) — not fixed here (out of this story's scope), correctly grandfathered rather than blocking the gate or being silently dropped |
| ST-22 | `scripts/generate_backend_coverage_report.py` (new); `.github/workflows/backend-coverage-report.yml` (new) | Backend test coverage (pytest-cov) summary posted as a PR comment, with a delta vs. base branch computed via a separate git worktree run; advisory only, never blocks merge | Coverage report posted to PRs with delta where feasible | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_r_multiple_calculation.py` (new, ST-19); `tests/e2e/accessibility-axe-scan.spec.js` (new, ST-21, 4 pages); `tests/e2e/visual-regression-baselines.spec.js` (new, ST-18, 10 tests — generated and re-verified reproducible: ran with `--update-snapshots`, then re-ran without and confirmed all 10 pass); `tests/test_generate_backend_coverage_report.py` (new, ST-22, 5 tests); ST-17/ST-20 are QA-documentation refresh stories cross-referencing the pre-existing suites named in the Test scenarios line above, verified present and matching by direct file/line inspection during agent-mediated review, not merely cited from memory.
- Regression areas checked: full backend test suite unaffected by this EPIC's changes (no backend runtime code touched — ST-19/ST-22 are new test/tooling files, ST-17/ST-18/ST-20/ST-21 are docs/test-infra only); YAML syntax validated programmatically (`python3 -c "import yaml; yaml.safe_load(...)"`) for all workflow files touched (`playwright.yml`, `update-visual-snapshots.yml`).
- Known deviations: None requiring escalation. Two stories (ST-20, ST-17) required review-driven corrections before sign-off — both resolved same-session, documented in each story's own commit message and `execution_state.json` `sign_off_record` field. ST-21 found and filed 5 pre-existing accessibility violations as backlog items (BLG-FE-165–169), correctly out of this story's own scope to fix.

---

## Sign-Off

**Mixed-Class EPIC Signer Format:** All 6 stories in EPIC-04 are `autonomous` classification with agent-mediated review sign-offs from the relevant domain authority per story (QA Lead for ST-20; Director of Quality for ST-17 and ST-18). No `delegated_*` or cross-domain authority stories in this EPIC — the single Director of Quality consolidation block below applies.

Individual story sign-offs on record:
- ST-17: Director of Quality agent-mediated sign-off, Approved 2026-08-21 (3 review passes, at the max-2-retries budget — see `execution_state.json` ST-17 `sign_off_record` for full detail)
- ST-18: Director of Quality agent-mediated sign-off, Approved 2026-08-21 (1 pass, 1 minor non-blocking observation fixed same-commit)
- ST-19: No explicit sign-off role named in this story's own AC (BLG-QA-89) — test-only story, verified via direct execution (`pytest` run, all assertions pass) and code review against the canonical spec's own prescribed test shape
- ST-20: QA Lead agent-mediated sign-off, Approved 2026-08-21 (1 retry: first pass Blocked on a factual mischaracterization, corrected, re-review Approved)
- ST-21: No explicit sign-off role named in this story's own AC (BLG-QA-83) — verified via direct execution (Playwright run against real Chromium, all 4 pages scanned, `KNOWN_VIOLATIONS` baseline confirmed accurate)
- ST-22: No explicit sign-off role named in this story's own AC (BLG-QA-84) — verified via direct execution (`pytest` run on `test_generate_backend_coverage_report.py`, all 5 tests pass; YAML validated)

```
Director of Quality

EPIC-04 consolidation reviewed. All 6 stories done, acceptance criteria verified,
spec_references populated. No P0 deviations. 5 pre-existing accessibility
violations found (ST-21) correctly filed as backlog items rather than silently
fixed out-of-scope or hidden. Two stories (ST-17, ST-20) required review-driven
factual corrections before their individual sign-offs — both resolved
same-session and documented. EPIC-04 ready for PR.

Signed: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
Date: 2026-08-21
```
