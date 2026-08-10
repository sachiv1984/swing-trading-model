Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-10

# QA Evidence — EPIC-04 (Design System & Contrast Consistency Audit)

**EPIC:** EPIC-04 — Design System & Contrast Consistency Audit
**Cycle:** 2026-08-08__release-v8.5
**Sprint goal:** Clear the full ready frontend-correctness, design-consistency, and security-hardening slate across all 25 scoped stories — see `sprint_goal.md`
**Test scenarios used:** `tests/e2e/theme-persistence.spec.js` (SC-TP-01..04, new), `tests/e2e/analytics-mobile-responsive.spec.js` (SC-PA-M01..06, new), `tests/e2e/saved-filters-calendar-view.spec.js` (SC-SFC-09, updated selector), `tests/e2e/command-palette.spec.js` (SC-CP-13/14, this EPIC's own sibling EPIC-03 dependency, cross-referenced)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-09 | `st09_secondary_text_token_audit_findings.md` | Audit-only. Branched from EPIC-03 tip (not main) per RISK-01 so the audit ran against the corrected CSS baseline. Found 6 drift instances against the v6.7 canonical secondary-text token. Filed `BLG-FE-149`. | Audit conducted; drift filed as follow-up | Pass | None |
| ST-10 | `docs/design/2026-08-08__release-v8.5/empty-state-microcopy-pattern/decision_record.md`, `docs/specs/frontend/design_system.md` | Fixed `TradePlans.js`'s trailing-period heading per the Design Gate decision. Scanned all 18 `emptyHeading=` call sites app-wide and found + fixed one additional undisclosed deviation (`CalendarView.js`, same bug). Updated the one stale Playwright selector this broke. | Pattern documented (pre-satisfied); applied to >=3 pages | Pass | None |
| ST-11 | Case E — no prior canonical spec, bug/correctness fix | Fixed a real flash-of-wrong-theme bug (state defaulted to "dark", corrected in a post-mount effect) via lazy `useState` init. Persistence itself was already correct. Added accessible names/testids to the theme-toggle buttons. | Persistence verified across session boundaries; gap fixed | Pass | None |
| ST-12 | `docs/specs/frontend/pages/analytics.md` | Audited page + 18 sub-components against the documented Responsive Behavior section. Found and fixed 4 real drift instances (fixed grid without mobile breakpoint, 2 tables missing horizontal scroll, header actions not stacking on mobile). | Page audited; critical issues fixed | Pass | None |
| ST-13 | `st13_dark_light_contrast_audit_followup.md` | Audit-only. Cross-checked ST-09's audit (no further secondary-text gaps found). New finding connected to EPIC-03's ST-06 portal fix: 4 of 5 Dialog components hardcode dark-only styling (light-theme completeness gap, not a WCAG failure). Filed `BLG-FE-150` (design-scope question). | Targeted follow-up audit run; no further gaps beyond BLG-FE-87/88/89 | Pass | None |
| ST-14 | `st14_ad_hoc_component_inventory.md` | Compiled inventory of ad hoc/duplicated component patterns ranked by duplication count (card wrapper, badge/status-pill, metric tile, status-colour config map). Agent-mediated Head of UX & Design sign-off, 2 passes (first pass caught a real factual error, corrected). | Inventory produced; Head of UX & Design sign-off | Pass | None |

*(All ACs for all six ST items appear in the table above.)*

**QA test coverage:**
- Playwright coverage added this EPIC (could not execute locally — Chromium unsupported on this sandbox's OS; real CI (`playwright.yml`) is the verification path per LL-v8.3-P3-02):
  - `tests/e2e/theme-persistence.spec.js` SC-TP-01..04 (ST-11)
  - `tests/e2e/analytics-mobile-responsive.spec.js` SC-PA-M01..06 (ST-12)
  - `tests/e2e/saved-filters-calendar-view.spec.js` SC-SFC-09 selector update (ST-10)
- Regression areas checked: `TimeBasedCharts`/`MonthlyHeatmap`/`RMultipleAnalysis`/`PerformanceAnalytics` desktop-width behaviour confirmed unchanged (SC-PA-M05/M06 explicit desktop-regression tests); no backend changes this EPIC
- Known deviations filed: None
- Backlog items filed from this EPIC: `BLG-FE-149` (ST-09, 6 secondary-text drift instances), `BLG-FE-150` (ST-13, modal light-theme design-scope question)

**Cross-EPIC note (EPIC-03 dependency, RISK-01):** ST-09 and ST-13 both required EPIC-03's ST-06 fix (tailwind.config.js muted-token registration, plus the dark-mode-portal fix discovered during that story's real CI run) to audit against a correct baseline. This branch was created from EPIC-03's tip, not `main`, and was re-synced via merge when EPIC-03 pushed its portal-fix follow-up commit (see `claude/cycles/2026-08-08__release-v8.5/qa_evidence_EPIC-03.md`'s "Critical finding" section for that fix's full detail). Both EPIC-03 and EPIC-04 branches now carry the same `Layout.js` fix.

**EPIC-level consolidation note (BLG-GOV-14):** ST-14's story-level authority sign-off (Head of UX & Design, agent-mediated, 2 passes, cleared) is recorded in `execution_state.json`'s `sign_off_record` for that story and is explicitly confirmed cleared here — it does not substitute for the EPIC-level DoQ consolidation block below; both are present.

---

## Sign-Off Block

**Autonomous class (BLG-GOV-19) not available:** ST-10, ST-11, and ST-12 all modify files under `src/pages/**`/`src/components/**` and ship live, frontend-visible fixes — per the BLG-GOV-135 detection rule, criterion 3 (no frontend-visible change) is automatically unmet. Full agent-mediated Director of Quality review applies instead. ST-14 is additionally `delegated_decision` (not `autonomous`), disqualifying the mixed-class autonomous path per the Mixed-Class EPIC Signer Format Note.

**Environment-parity note (LL-v8.3-P3-02):** Playwright coverage exists for every observable AC across ST-10/11/12 but could not be executed in this sandbox (Chromium unsupported on this OS). Real CI (`playwright.yml`, triggers on `pull_request`) is the verification path — pending confirmation on this EPIC's PR.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] ST-14's Head of UX & Design sign-off confirmed cleared (see consolidation note above)
- [ ] Playwright coverage confirmed passing in real CI — **pending this EPIC's PR's first `playwright.yml` run**
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-10
- Comments: Six stories, all AC met. Two real findings surfaced and fixed during this EPIC's own execution beyond what was originally scoped: ST-10 found a 2nd undisclosed empty-state period-in-heading instance (CalendarView.js) beyond the Design Gate's own 4-page audit; ST-12 found and fixed 4 genuine mobile-responsive drift instances. ST-14's inventory deliverable went through 2 rounds of agent-mediated Head of UX & Design review, catching a real factual error (claimed a component didn't exist when it did) before sign-off. Sign-off is conditional on the pending real-CI confirmation noted above.
