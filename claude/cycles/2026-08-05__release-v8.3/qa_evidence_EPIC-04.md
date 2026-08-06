Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-06

# QA Evidence — EPIC-04: QA & Spec Debt

**EPIC:** EPIC-04 — QA & Spec Debt
**Cycle:** 2026-08-05__release-v8.3
**Sprint goal:** Restore and harden the SI-05 weekly digest pipeline (fix plus delivery-failure alerting) while clearing a curated slate of backend resilience, frontend design-system, QA/spec, and governance-process debt — leaving no ungated P1 operational gap open and no item below its stated acceptance bar.
**Test scenarios used:**
- `tests/e2e/watchlist.spec.js` (SC-WL-01 through SC-WL-05, all new this EPIC)
- `tests/e2e/epic03-v34-frontend.spec.js` (SC-E03-15b new; 20 pre-existing scenarios re-verified passing, no regression)
- `tests/test_doq_signoff_staleness_check.py` (5 new unit tests)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-16 | `tests/e2e/watchlist.spec.js` | New baseline Playwright coverage for Watchlist.js — entry rendering, news toggle expand/collapse, non-US entry has no toggle, Add Ticker modal open | New spec file passes in CI; covers entry rendering, news toggle, Add Ticker modal open | Pass | None — a strict-mode locator defect found by agent-mediated review was fixed pre-merge, not shipped |
| ST-17 | `scripts/openapi_3way_drift_sweep.py`, `docs/ops/openapi_3way_sweep_log.md` | Quarterly 3-way drift sweep (router/@app decorators vs contracts vs openapi.yaml) — the missing 3rd leg the existing 2-way CI gate can't check | Sweep procedure documented; first run scheduled; zero drift confirmed or gaps filed | Pass | None — 1 genuine gap found and filed (`BLG-SPEC-111`), all other findings investigated and confirmed false positives (documented rationale in `KNOWN_GAPS`) |
| ST-18 | `scripts/check_doq_signoff_staleness.py`, `.github/workflows/quality_gate.yml` | Pre-merge lint catching residual "Pending DoQ"/"Awaiting QA" placeholders in the active cycle's qa_evidence files (catches the CLAUDE.md §8 cross-EPIC-merge scenario) | Lint check added to quality_gate.yml; fails on a synthetic Pending-row test case | Pass | None |
| ST-19 | `docs/ops/openapi_response_example_spot_check_2026-08-06.md` | Spot-checked 6 endpoints' documented example payloads against live response-construction code | Sample check performed and documented; drift filed as follow-up items | Pass | None — 4 genuine drift findings filed (`BLG-SPEC-112` through `115`); one item's initial justification was corrected post-review (see Process Note below) |
| ST-20 | `docs/specs/api_contracts/conventions.md#14` | New deprecation-window policy (30/90-day notice windows, marking convention, changelog requirement, removal process) | Deprecation-window policy section added; Head of Specs Team sign-off | Pass | None |
| ST-21 | `docs/specs/frontend/design_system.md#Error States`, `tests/e2e/watchlist.spec.js`, `tests/e2e/epic03-v34-frontend.spec.js` | Closed the dark-only-token gap (`text-rose-400` → `text-rose-700 dark:text-rose-400`) in the 2 shipped form-validation-error instances the design gate's own clearing rationale flagged (`WatchlistModal.js`, `TradePlan.js` Abandon modal) | Canonical error-message pattern spec added to design_system.md (pre-existing, written at Design Gate); Frontend Specifications & UX Documentation Owner sign-off | Pass | None — a missing-Playwright-coverage hard-gate finding was fixed pre-merge (2 new tests added and actually run against a real Chromium binary), not shipped without evidence |

**Process Note (ST-19 / BLG-SPEC-115):** the first-pass agent-mediated review found `BLG-SPEC-115`'s problem statement overstated its own finding — it claimed `is_stale`/`days_on_watchlist` were "entirely absent from the contract," when in fact both fields are correctly documented in `watchlist_endpoints.md`'s own field table and version history; only the illustrative JSON example was stale. Corrected in the same session (priority P2→P3, wording fixed in both `backlog.md` and the spot-check doc) before this PR opened. Recorded here per the "ironic for a docs-accuracy story" observation in the review — the correction itself is now part of this EPIC's evidence trail, not a silent fix.

**QA test coverage:**
- Scenarios run: `tests/e2e/watchlist.spec.js` (5 scenarios, all new) and `tests/e2e/epic03-v34-frontend.spec.js` (21 scenarios, 1 new + 20 pre-existing) both actually executed against a real Chromium binary and the real dev server during agent-mediated review — not code-review-only; `tests/test_doq_signoff_staleness_check.py` (5 unit tests) executed via `backend/.venv/bin/python3 -m pytest`
- Regression areas checked: Watchlist page (entry rendering, news toggle, Add Ticker modal), TradePlan Abandon modal (all pre-existing Escape/Cancel/focus/tab-order scenarios re-verified passing after the colour-token change)
- Known deviations filed: None — a strict-mode locator defect (ST-16) and a missing-Playwright-coverage hard gate (ST-21) were both found and fixed pre-merge by agent-mediated review, not shipped as deviations

**Frontend Testing Gate disposition (LL-v3.1-EX-01):** ST-21 carries 2 observable ACs (colour-token change on 2 shipped components) — both have real, actually-executed Playwright coverage (`SC-WL-05`, `SC-E03-15b`), not code-review-only. ST-16 is itself the Playwright-coverage deliverable (test infrastructure, Design Not Applicable). ST-17/ST-18/ST-19/ST-20 have no frontend-visible change (backend script/CI/documentation stories).

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no URL construction introduced in this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-06
- Comments: BLG-GOV-19 autonomous class does not apply — Criterion 3 automatically unmet per the BLG-GOV-135 detection rule (ST-21 modified files under `src/pages/**` and `src/components/**`). Standard sign-off block used instead. All 6 stories are `autonomous` classification with prior story-level agent-mediated sign-off by the relevant domain authority (Director of Quality for ST-16/ST-18, API Contracts & Documentation Owner for ST-17/ST-19, Head of Specs Team for ST-20, Frontend Specifications & UX Documentation Owner for ST-21 — see `sign_off_record` entries in `execution_state/EPIC-04.json`); this EPIC-level block is the required DoQ consolidation and does not substitute for, nor is substituted by, those story-level sign-offs. Two hard-gate findings (ST-16 strict-mode defect, ST-21 missing Playwright evidence) were caught by agent-mediated review and fixed pre-merge, re-verified via actual Playwright execution against a real Chromium binary — not shipped as deviations.
