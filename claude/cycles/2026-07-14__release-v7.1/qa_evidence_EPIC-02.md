Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-14

# QA Evidence — EPIC-02 (Table View Badge Spec Compliance)

## Consolidation Block

**EPIC:** EPIC-02 — Table View Badge Spec Compliance
**Cycle:** 2026-07-14__release-v7.1
**Sprint goal:** Eliminate the two P1 nightly-backtest data-integrity bugs feeding the Strategy Benchmark page (EPIC-01), bring the Table View RISK OFF badge into spec compliance (EPIC-02), and close out the four v7.0 post-ship hardening gaps (EPIC-03) — delivering all v7.1 mandatory anchors plus capacity-filling hardening in a single sprint.
**Test scenarios used:** `tests/e2e/epic01-v62-stops-alerts.spec.js` (16 scenarios, incl. `SC-RO-02` updated this sprint), `tests/e2e/epic01-v70-grid-badge-parity.spec.js` (9 scenarios, incl. `SC-GVP-02` — cross-view parity check), `tests/e2e/gap-risk-flag.spec.js` (8 scenarios — combined-badge stacking regression)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-03 | `docs/specs/frontend/pages/positions.md#Alerts Column` | `AlertsCell` (`src/pages/Positions.js`) RISK OFF badge changed from `bg-amber-900/60 text-amber-300` + `ShieldAlert` icon + "Risk-Off" label to `background-color: #1E40AF`, no icon, "RISK OFF" label — matching the spec and the v7.0 Grid View badge (`PositionCard.js`). `SC-RO-02` updated in the same commit to assert the spec-correct colour instead of the amber values it previously encoded as expected. Unused `ShieldAlert` import removed. `positions.md` §Known Deviations updated to close `DEV-EPIC01-ST05-01` (v2.3→v2.4, no §Alerts Column text change — spec was already correct). Design gate resolution: option (a). Covers AC-01, AC-02, AC-03, AC-04. | AC-01: design gate resolves treatment (option (a) chosen). AC-02: Table View and Grid View use a single consistent colour/label. AC-03: `SC-RO-02` and `SC-GVP-02` internally consistent. AC-04: combined-badge hue-separation rationale verified true for both views. | Pass | None (DEV-EPIC01-ST05-01 closed by this story, not a new deviation) |

**QA test coverage:**
- Scenarios run: `tests/e2e/epic01-v62-stops-alerts.spec.js` (16/16 pass), `tests/e2e/epic01-v70-grid-badge-parity.spec.js` (9/9 pass, incl. `SC-GVP-09` confirming Table View breach indicator unchanged), `tests/e2e/gap-risk-flag.spec.js` (8/8 pass, confirms RISK OFF/GAP RISK stacking unaffected) — 33/33 passing, 0 failures
- Regression areas checked: Table View Alerts column (breach badge unaffected — SC-TS-04 still asserts orange, not amber, and now also asserts distinct from risk-off blue); Grid View unaffected (built correctly in v7.0, this story only touched Table View); combined GAP RISK/RISK OFF stacking (still amber vs blue, hue separation now genuinely holds for both views per AC-04)
- Known deviations filed: None — this story **closes** `DEV-EPIC01-ST05-01` (pre-existing since v6.2), does not file a new one

---

## Frontend Testing Gate (LL-v3.1-EX-01)

Observable ACs for this EPIC (colour/label rendering — AC-02, AC-03, AC-04):
1. **Playwright coverage:** Yes — `SC-RO-02` (`tests/e2e/epic01-v62-stops-alerts.spec.js`) asserts `background-color: rgb(30, 64, 175)` (#1E40AF) directly via `toHaveCSS`; `SC-GVP-02` (`tests/e2e/epic01-v70-grid-badge-parity.spec.js`) asserts the same for Grid View, confirming parity. No staging run required — full colour/label assertion coverage exists in CI.

The autonomous DoQ sign-off class (BLG-GOV-19) does **not** apply to this EPIC — Criterion 3 (no frontend-visible change) is unmet: ST-03 modifies `src/pages/Positions.js`. Standard sign-off block used below.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object (N/A — no URL construction in this change)
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-07-14
- Comments: Playwright coverage is complete and passing (33/33 scenarios across 3 spec files, independently re-run by the engine, not only self-reported) — colour, label, icon-removal, and cross-view parity all directly asserted via `toHaveCSS`, not just smoke-tested. Verified diff against canonical spec (`positions.md` §Alerts Column): label "RISK OFF" and background `#1E40AF` match exactly. No unresolved P0/P1 deviations — the only referenced deviation (`DEV-EPIC01-ST05-01`) is being closed, not introduced. Documentation update to §Known Deviations is text-only and consistent with the code change.
