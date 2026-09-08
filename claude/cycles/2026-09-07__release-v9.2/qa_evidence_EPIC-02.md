Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-08

---

**EPIC:** EPIC-02 — Frontend Accessibility & Spec Compliance
**Cycle:** 2026-09-07__release-v9.2
**Sprint goal:** Ship the Arc 5 low-volume compliance-score advisory and clear a full-capacity slate of 55 accessibility, QA/CI reliability, governance-process, and spec/tech/ops debt items across all 5 EPICs — exhausting the confirmed ~24–28 day capacity band at 27.55 days, with 0 P1/P2 debt items carried past this sprint on capacity grounds.
**Test scenarios used:** `tests/e2e/accessibility-axe-scan.spec.js`, `tests/e2e/arc5-compliance-section.spec.js`, `tests/e2e/trade-plan.spec.js`, `tests/e2e/ai-usage-costs.spec.js`, `tests/e2e/visual-regression-baselines.spec.js` (dedicated advisory CI job, `playwright.visual-regression.config.js`)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-02 | *(no canonical spec — see notes)* | `Settings.js` `SectionCard` heading bumped `h3`→`h2`; `className` unchanged | axe-core no longer reports `heading-order` for Settings; no visual/layout regression | Pass | None |
| ST-03 | *(no canonical spec — see notes)* | `TradePlan.js` (`Field` gained `labelId` prop; Market/Status/Setup Type selects use `aria-labelledby`) and `Settings.js` (Default Currency/Theme `Label` gained `id`, `SelectTrigger` uses `aria-labelledby`) | All 5 controls use `aria-labelledby` instead of `aria-label`; `accessibility-axe-scan.spec.js` continues passing with no new violations | Pass | None |
| ST-04 | `docs/specs/frontend/components/arc5_compliance_section.md#Card 3 — Top Rule Breach` | Corrected Card 3's Format/Null-display row to document the already-shipped `fmtText` behaviour (space-separated slug, em-dash on null); no component/test change | Spec and implementation agree on Card 3's text format and null display; `SC-ARC5-07`/`SC-ARC5-08` continue to pass | Pass | None — resolves the pre-existing Known Deviation opened at v9.1 ST-13 (BLG-FE-172) |
| ST-05 | `docs/specs/frontend/design_system.md#Accessibility`, `docs/design/2026-09-07__release-v9.2/motion-contrast-guideline-standard/decision_record.md` | Added the Motion-vs-contrast guideline for text-element entrance animations (v1.12) — bounds total time-to-full-opacity (delay+duration) at 500ms, documents 4 known non-compliant components, requires contrast scans to evaluate the settled state | `design_system.md` gains an explicit guideline; Head of UX & Design sign-off | Pass | None — follow-up gap for the 4 non-compliant components filed separately as `BLG-SPEC-136` (not a deviation from this story's own AC) |

**QA test coverage:**
- Scenarios run: `tests/e2e/accessibility-axe-scan.spec.js` (4/4 — DashboardHome, Positions, TradePlan, Settings), `tests/e2e/arc5-compliance-section.spec.js` (15/15), `tests/e2e/trade-plan.spec.js` (50/50), `tests/e2e/ai-usage-costs.spec.js` (9/9) — all re-run green locally, post-change. `tests/e2e/visual-regression-baselines.spec.js` (Settings/TradePlan baselines) runs only in its dedicated non-blocking CI job (`playwright.yml`'s `playwright-visual-regression`, `continue-on-error: true`) per `playwright.config.js`'s own `testIgnore` for this file — not reliably reproducible locally (pixel-level, font/anti-aliasing variance across environments per the file's own header comment) — will be observed on the PR's CI run.
- Regression areas checked: Settings page rendering (heading structure, Default Currency/Theme selects), TradePlan form (Market/Status/Setup Type selects, full 50-scenario regression suite), Arc5ComplianceSection (full 15-scenario suite covering all 4 cards + low-volume advisory), AI usage/costs section on Settings (9-scenario suite, unaffected by ST-02/03 but re-run as a Settings-page regression check).
- Known deviations: None found — all 4 stories' deviation checks completed with nothing to file. ST-04 *resolves* a pre-existing deviation (not files a new one); its own resolving-commit fields were updated in `docs/specs/frontend/components/arc5_compliance_section.md`'s Known Deviations section per LL-v9.0-P4-01.

**Frontend testing gate (LL-v3.1-EX-01) — observable AC coverage:**
- ST-02 "axe-core no longer reports heading-order": Playwright (`accessibility-axe-scan.spec.js`, Settings scenario) — Pass.
- ST-02 "no visual/layout regression": `className` unchanged on the only element touched (semantic tag swap only); Playwright visual regression baseline exists for Settings (`visual-regression-baselines.spec.js`, dedicated CI job, both themes) as the observable-rendering backstop.
- ST-03 "5 controls use aria-labelledby" + "no new axe violations": Playwright (`accessibility-axe-scan.spec.js`) — Pass. Accessible-name-by-association is also implicitly exercised by every existing `getByLabel`/interaction test in `trade-plan.spec.js` that locates these controls by their visible label text (Playwright's accessible-name computation follows `aria-labelledby` the same as `aria-label` or a native `<label>` association) — all 50 scenarios in that file continue to pass.
- ST-04 is a spec-only, non-code change (no observable AC to test beyond the existing, already-passing `SC-ARC5-07`/`SC-ARC5-08`).
- ST-05 is a documentation-only deliverable (no rendering/UI surface of its own); the AC is code-review/sign-off verifiable, not staging/Playwright-verifiable.

**Sign-off history note (ST-05):** Agent-mediated Head of UX & Design review ran 3 rounds under §5.3 (initial + the 2 permitted retries), each finding and resolving one genuine issue; the retry budget was then exhausted with round 3's fix unverified by a further automated pass. Per §5.3 step 7, escalated as `ESC-EXEC-20260908-01` rather than retrying again. The user then directly assumed the Head of UX & Design role (role match against ST-05's `sprint_backlog.md` Owner field confirmed first, per CLAUDE.md), independently re-verified every factual claim in the guideline against source, and signed off. Full detail in `execution_state.json` → `epics.EPIC-02.stories.ST-05.sign_off_record` and the resolved escalation record.

---

## Standard Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):** does **not** apply — Criterion 3 automatically unmet per the BLG-GOV-135 detection rule: ST-02 and ST-03 modify files under `src/pages/` (`Settings.js`, `TradePlan.js`), a frontend-visible change. Standard Sign-Off Block used instead.

- [x] All acceptance criteria verified against canonical spec (or against the story's own stated AC where no canonical spec governs — ST-02/ST-03, see notes above)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no new URL construction introduced this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-08
- Comments: All 4 stories' local Playwright evidence (accessibility-axe-scan.spec.js 4/4, arc5-compliance-section.spec.js 15/15, trade-plan.spec.js 50/50, ai-usage-costs.spec.js 9/9) re-run green post-change. Pixel-level visual regression coverage (Settings/TradePlan) exists but runs only in its dedicated advisory CI job — will confirm on the PR. This EPIC-level block is agent-mediated per §5.3, consistent with the precedent set at EPIC-01 (`qa_evidence_EPIC-01.md`); it evidences the aggregate story-level verification but does not itself satisfy STEP 4's separate merge-gate condition requiring a human Director of Quality comment on the PR — that remains outstanding before merge.
