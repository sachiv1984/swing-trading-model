Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06 (EPIC-02 consolidation, STEP 3.2.A; DoQ sign-off pending)

# QA Evidence — EPIC-02 — Stop & Exit Transparency (build-and-ship)

**EPIC:** EPIC-02 — Stop & Exit Transparency (build-and-ship)
**Cycle:** 2026-10-06__release-v9.10
**Sprint goal:** Make every live stop come from one §11 parameter source, and show the ATR, multiplier, recalculation source and already-known exit conditions behind each position (BLG-BE-138, BLG-FE-193, BLG-FE-198), while clearing v9.10's lifecycle/gap-risk rulings and AI-governance, ops and QA hygiene items.
**Test scenarios used:** `tests/e2e/stop-cell-provenance.spec.js`, `tests/e2e/trailing-stop-explainer-tooltip.spec.js`, `tests/e2e/trade-entry-system-stop.spec.js`, `tests/test_add_position_stop_handling.py`, `tests/e2e/exit-condition-surfacing.spec.js`, `tests/e2e/recent-trades-zero-pnl-badge.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-06 | `positions.md` v2.12 §Stop Provenance Line and Per-Row Stop Details; design record `stop-cell-provenance/decision_record.md` | `StopProvenance.js`: always-visible `{m}× ATR {atr}` line and a per-row "How this stop was set" tooltip (ATR, multiplier state, §7.2 formula, §7.3 ratchet, last recalculated + nightly/on-load source, grace line), in both Table and Grid views. The header explainer drops "recalculated daily". Commit `b1921fd1`. | AC 1: stop cell/tooltip shows ATR, active multiplier and calculation source (SC-SCP-01..06). AC 2: explainer copy reflects the real recalculation events instead of "recalculated daily" (SC-SCP-07, SC-TSE-02). AC 3: `positions.md` describes the new cell (v2.11 design-gate section, finalised in v2.12). | Pending DoQ | None found |
| ST-07 | `position_form.md` v1.8 §ATR (14-day), §Initial Stop (set by system); design record `trade-entry-system-stop/decision_record.md` | Stop Price input removed. A read-only "Initial Stop (set by system)" panel shows entry − 5× ATR from the fixed §11 source. Risk and sizing use only that stop. The ATR field is relabelled. The plan stop is a reference note. The toast reports the stored stop. Commit `e5df8e65`. | AC 1: risk shown equals risk from the stored stop (SC-TES-01). AC 2: no input suggests it sets the stop (SC-TES-02, payload has no `stop_price`). AC 3: ATR not labelled "(Optional)" (SC-TES-03). AC 4: `add_position` stop handling pinned by `tests/test_add_position_stop_handling.py` (5 tests). | Pending DoQ | None found |
| ST-08 | `positions.md` §Exit Dialog Pre-Selection and Deep Link | Shared `getExitCondition` predicate (`src/lib/exitCondition.js`). `ExitModal.js` pre-selects "Risk-Off Signal" / "Stop Loss Hit" with a one-line reason; `?exit={id}` deep link. Commit `1d7b7a24`. | AC 1: risk-off → "Risk-Off Signal"; post-grace price ≤ stop → "Stop Loss Hit"; reason shown; user can change it (SC-EXD-01..04). AC 2: all others default to "Manual Exit" (SC-EXD-05, SC-ECP-01..04). | Pending DoQ | None found |
| ST-09 | `dashboard.md` §Exit Conditions Met Row | `ExitConditionsCard.js` morning-briefing card listing post-grace stop-breach / risk-off positions, each linking to the exit dialog. Commit `1d7b7a24`. | AC 1: card renders for qualifying positions and is absent otherwise (SC-EXC-01..02). AC 2: §13 display-only; wording passes the UI-copy boundary lint. | Pending DoQ | None found |
| ST-10 | `tests/e2e/recent-trades-zero-pnl-badge.spec.js` (Case C) | Neutral `Minus` glyph for zero/missing-P&L trades in `RecentTradesWidget.js`. Winners and losers keep their arrows. Commit `89f16aa4`. | AC 1: neutral glyph; arrows unchanged (SC-RTB-01..05). AC 2: spec extended to assert the glyph, passing in CI. | Pending DoQ | None found |

**QA test coverage:**
- Scenarios run: SC-SCP-01..07, SC-TSE-01..05, SC-TES-01..06, SC-EXD-01..05, SC-ECP-01..04, SC-EXC-01..02, SC-RTB-01..05 (Playwright); `tests/test_add_position_stop_handling.py` (pytest, 5). All pass locally. Real GitHub Actions CI on `exec/2026-10-06__release-v9.10/EPIC-02`: see sign-off Comments.
- Regression areas checked: Positions stop cell (Table and Grid: `position-stop-currency-basis`, `epic01-v62-stops-alerts`, `gap-risk-flag`, `compliance-recheck`, `epic01-v70-grid-badge-parity`, `number-format-tables`, `position-review-cadence-nudge`, 86/86); Trade Entry and sizing (`smoke-critical-paths`, `position-sizing-concentration`, `settings-strategy-parameters-fixed`, `v7.2-dashboard-tradeplan-ux-hardening`, `trade-plan-invalidation-link-toast-ai-badge`, `trade-plan-linkage-advisory`, `setup-thesis-digest`, `what-if-sizing-preview`, `keyboard-shortcuts`, `cash-management-global-trigger`, `empty-state-next-action`, `shadcn-token-remaining-families`, 82/82); morning briefing, lifecycle and axe (ST-08/ST-09 run, 68/68).
- Cross-spec selector updates (STEP 3.1.A step 13): ST-06 updated SC-TSE-02 for the new explainer copy. ST-07 moved SC-SPF-05, `smoke-critical-paths` and `position-sizing-concentration` from the removed Stop Price input to the ATR field.
- Known deviations: None found. All stories' deviation checks completed with nothing to file.

**Frontend testing gate (CLAUDE.md §2, LL-v3.1-EX-01):** every observable AC above is covered by a named Playwright scenario. No AC is "code review only". ST-09 AC 2 (copy boundary) is verified by the existing UI-copy lint, not visually.

**Environment-parity sub-clause (LL-v8.3-P3-02):** ST-06's tooltip opens on keyboard focus after the shared 200 ms delay (SC-SCP-02..06), and ST-08 pre-selects the exit reason when the dialog opens (SC-EXD-01..05). Both are interaction-timing ACs, so the DoQ comments must cite a real GitHub Actions CI run with these scenarios passing, not only the local runs.

**Same-EPIC cross-story testing-gap consistency check:** no story in EPIC-02 filed a testing-gap backlog item. Nothing to propagate.

---

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- Signed off by:
- Date:
- Comments:
