**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-12
**Cycle:** 2026-10-12__release-v9.12

# Design Gate Record — 2026-10-12__release-v9.12

## Gate Status: PASSED

Completed: 2026-10-12
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

All 48 items are classified and cleared. No item is conditionally cleared or blocked.

| Classification | Count | Items |
|----------------|-------|-------|
| Design Required | 9 | ST-10, ST-15, ST-17, ST-18, ST-20, ST-22, ST-23, ST-24, ST-26 |
| Design Pre-Approved | 7 | ST-01, ST-07, ST-08, ST-13, ST-14, ST-19, ST-21 |
| Design Not Applicable | 32 | the remaining items |

**RISK-03 is resolved.** The release plan requires ST-23's light-mode decision before Sprint Planning seals. Light mode is ruled a supported theme, so ST-23 takes its first AC branch and its estimate stands. See `light-theme-support/decision_record.md` and the addendum.

**Classification notes:**
- The slice marks 11 stories UI-facing. Two are Pre-Approved rather than Design Required:
  - **ST-13** changes which existing status a US row shows, not how it is shown.
  - **ST-21** moves numbers into a constants module with no intended visible change.
- **ST-20** is wording only (FI-P3-02). It is classed Design Required because the spec text had to change first. The new text is in `settings.md` v1.9.
- Four stories not marked UI-facing change values that existing specs already display, and are Pre-Approved with a locked reference: ST-01, ST-07, ST-08 and ST-14. ST-19 is test coverage of the changed Trade Entry page.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-BE-162) | Accept UUID trade IDs in the journal summary, end to end | Design Pre-Approved | Restores an existing feature that has failed with 422 since 2026-04-18. No rendering change. §13: an existing AI call, not extended. Gate-cleared under `SRB-v1.7-2026-03-02__release-v1.7.md` (BLG-FEAT-16) and the v2.8 decision record. | N/A | `trade_history.md` v1.15 (locked reference — AI Journal Summary, design source v2.8) | ✅ Cleared | Head of UX & Design |
| ST-02 (BLG-AI-11) | Drop briefing actions that name a ticker outside the context | Design Not Applicable | Output filter and logging. The briefing card is unchanged, and a dropped action simply does not render. §13: covered by `decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`. It narrows output and adds no call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-AI-12) | Label available cash and starting capital separately in the briefing context | Design Not Applicable | Prompt context text. §13: covered by the BLG-FEAT-50-51 review. No new call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 (BLG-AI-10) | Check that briefing and chat responses citing a stop include its recalculation time | Design Not Applicable | Output validator. If the failure action appends the time, the result is model-text content in the existing card or bubble, with no layout change. §13: covered by the BLG-FEAT-50-51 review. Strengthens a v9.11 ST-08 obligation. No new call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 (BLG-AI-13) | Widen the monthly P&L narrative's instrument-directive scan | Design Not Applicable | Backend scan and tests. §13: covered by `decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md` (CONDITIONAL). The change tightens the directive check that the review's conditions rely on. No new call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 (BLG-OPS-183) | Make the daily AI cost alert count Claude calls | Design Not Applicable | Cost monitoring. Counts existing calls and adds none. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 (BLG-BE-157) | Give zero-ATR signals no allocation in batch sizing | Design Pre-Approved | Corrects `suggested_shares` for zero-ATR signals, a value the Signals page already shows. The new `reason` is API-only this release. Displaying it needs its own design pass. | N/A | `signals.md` v0.4 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-08 (BLG-BE-158) | Include entry fees in batch signal total cost | Design Pre-Approved | Corrects `total_cost`, summed by the Signals page's capital total. No new element. | N/A | `signals.md` v0.4 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-09 (BLG-QA-205) | Assert §4.1.5 FX and §4.1.6 insufficient-cash sizing in CI | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 (BLG-BE-159) | Make the Trail Stop action work against a real route, or remove it | Design Required | Changed modal action, button label and states. Both ruling outcomes are designed, and no lower-stop control is allowed under either (§7.3). | `docs/design/2026-10-12__release-v9.12/trail-stop-action/decision_record.md` (new) | `positions.md` v2.15 → v2.16 (§Trail Stop Action, conditional) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-11 (BLG-BE-160) | Never let 2-dp rounding lower a stored stop | Design Not Applicable | Backend rounding. Shown values are 2 dp either way. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 (BLG-BE-145) | Recompute US positions with a NULL fill_price without error | Design Not Applicable | Backend error path and tests | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 (BLG-BE-149) | Decide Risk page LOSING/PROFITABLE on native P&L | Design Pre-Approved | Changes which existing status a US row shows. Labels, colours and layout are unchanged. | N/A | `risk_dashboard.md` v0.1.13 (locked reference — §6 Position Risk table) | ✅ Cleared | Head of UX & Design |
| ST-14 (BLG-BE-148) | Use the US exchange calendar for gap-risk "next trading session" | Design Pre-Approved | Changes which positions are flagged. The badge, label and tooltip are unchanged. Not an AI item. Its AC already cites §13.3 and §13.5 for any Ruling 3 addendum. | N/A | `positions.md` v2.16 (locked reference — §Gap Risk Badge, §Gap Risk Reason Labels) | ✅ Cleared | Head of UX & Design |
| ST-15 (BLG-FE-202) | Show the user when a position's stop is frozen for lack of ATR | Design Required | New data displayed: a frozen-stop indicator in the stop cell and tile, plus a tooltip row | `docs/design/2026-10-12__release-v9.12/frozen-stop-indicator/decision_record.md` (new) | `positions.md` v2.16 (§Frozen Stop Indicator) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-16 (BLG-BE-144) | Keep first-time Settings saves from writing NULL strategy columns | Design Not Applicable | Backend create path. The values shown on Settings come from the constants mirror, not the row. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 (BLG-BE-146) | ATR preview endpoint so Trade Entry shows the stop, risk and size before save | Design Required | New data displayed and new states in the Initial Stop panel and the sizing widget | `docs/design/2026-10-12__release-v9.12/trade-entry-atr-preview/decision_record.md` (new, shared with ST-18) | `components/position_form.md` v1.8 → v1.9 (§ATR, §Initial Stop, §Widget inputs) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-18 (BLG-FE-203) | Show the currency unit on the ATR field and reject implausible typed ATRs | Design Required | Changed label, a new inline error, and submit disabled for that input | `docs/design/2026-10-12__release-v9.12/trade-entry-atr-preview/decision_record.md` (new, shared) | `components/position_form.md` v1.9 (§ATR, §Validation Errors) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-19 (BLG-QA-206) | Cover the §4.1.7 sizing-widget behaviours with Playwright | Design Pre-Approved | Test coverage of the widget as changed by ST-17 and ST-18. No UI change of its own. | N/A | `components/position_form.md` v1.9 (locked reference — §Position Sizing Calculator) | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-FE-201) | Correct the Settings helper text for the fixed strategy parameters | Design Required | User-visible copy whose spec text had to change first. Wording only (FI-P3-02). | `docs/design/2026-10-12__release-v9.12/settings-copy-and-last-change/decision_record.md` (new, shared with ST-26) | `settings.md` v1.8 → v1.9 (§1 Strategy Parameters) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-21 (BLG-GOV-369) | Strategy-copy conformance: constants module, CI lint, named owner | Design Pre-Approved | Text sourced from constants, with no intended visible change. Any visible difference the lint surfaces must match the locked specs, or needs its own design pass. | N/A | `settings.md` v1.9, `positions.md` v2.16, `components/position_form.md` v1.9, `trade_plan.md` v1.18 §5a (locked references) | ✅ Cleared | Head of UX & Design |
| ST-22 (BLG-FE-207) | Link each Grace Period row to its position, and align the panel's text | Design Required | New interaction (row link and Positions deep link with a timed highlight) and changed text | `docs/design/2026-10-12__release-v9.12/grace-panel-position-link/decision_record.md` (new) | `risk_dashboard.md` v0.1.12 → v0.1.13 (§5.2); `positions.md` v2.16 (§Position Deep Link) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-23 (BLG-FE-200) | Make Reports and Notifications pass WCAG contrast in the light theme | Design Required | Light-theme colours on 4 page views. Decision: light mode supported (RISK-03). | `docs/design/2026-10-12__release-v9.12/light-theme-support/decision_record.md` (new) | `reports.md` v0.22 → v0.23; `notifications.md` v0.10 → v0.11 (§Light Theme) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-24 (BLG-FE-210) | Move white-on-amber-600 badges to a passing contrast outside Replay | Design Required | Colour change. Applies the pre-existing `BLG-FE-165` rule (amber-700, 5.02:1), so no new decision record is needed (v9.11 ST-15 precedent). Scope sites are in the addendum. | Pre-existing canonical rule (`dashboard.md` §9 v3.4; `docs/design/2026-09-03__release-v9.1/dashboardhome-ai-advisory-badge-contrast/decision_record.md`) | `positions.md` v2.16; `dashboard.md` v3.8 → v3.9; `trade_plan.md` v1.17 → v1.18; `strategy_benchmark.md` v0.7 → v0.8 | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-25 (BLG-OPS-184) | Stop the post-grace stop-health monitor alerting on the morning grace ends | Design Not Applicable | Ops monitor | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 (BLG-SEC-41) | Audit trail for strategy-parameter changes in Settings | Design Required | New data displayed: the last-change line on Settings | `docs/design/2026-10-12__release-v9.12/settings-copy-and-last-change/decision_record.md` (new, shared) | `settings.md` v1.9 (§Last Change Line) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-27 (BLG-SEC-42) | Re-assess the bundled `REACT_APP_API_KEY` against its write scope | Design Not Applicable | Credential classification. A narrower key has no visible effect. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 (BLG-TECH-22) | Apply the in-range dependency bumps | Design Not Applicable | Dependency update. Any visible regression is a defect caught by Playwright, not a design change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 (BLG-OPS-181) | Find out why a hook deploy of a governance-only commit never went live | Design Not Applicable | Ops investigation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 (BLG-OPS-182) | Live-fire the stale-staging check from main | Design Not Applicable | Ops check | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-31 (BLG-OPS-185) | Add requirements-dev.txt to the local setup instructions | Design Not Applicable | Documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 (BLG-GOV-371) | Inventory the scheduled GitHub workflows | Design Not Applicable | Documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 (BLG-SPEC-176) | Reconcile DELETE /trade-plans/{id}'s success envelope | Design Not Applicable | Contract or envelope. The frontend reads no body on delete success. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-34 (BLG-SPEC-178) | Triage the drift detector's new findings | Design Not Applicable | Spec and data-model triage | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 (BLG-SPEC-179) | Name the Gap Risk Badge's real data source in positions.md | Design Not Applicable | Spec text only, with no UI change. `positions.md` v2.16 §Gap Risk Badge already names `GET /positions/{position_id}/gap-risk` (v9.10 correction). The story confirms that no other reference claims a `gap_risk` field on `GET /positions`, and makes its own version bump. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-36 (BLG-SPEC-181) | Replace positions.stop_price with current_stop in the action-rate spec | Design Not Applicable | Spec and docstring | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-37 (BLG-SPEC-182) | Refresh the Gap Risk Flag §13 decision record | Design Not Applicable | Decision-record text. Not an AI item. Its AC cites §13.3 and §13.5. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-38 (BLG-SPEC-183) | Settle positions.entry_price's currency in the specs | Design Not Applicable | Data-model specs. A code fix, if chosen, must not change displayed values without a design pass. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-39 (BLG-GOV-385) | Check backlog item integrity after every cross-EPIC merge | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-40 (BLG-GOV-386) | Report gated items whose gating item has shipped | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-41 (BLG-GOV-363) | Script the execution_state.json read-back check | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-42 (BLG-GOV-367) | Name one Skill-Silo aggregation method | Design Not Applicable | Governance prompt | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-43 (BLG-GOV-364) | Rule on reduced-roster idea-intake windows | Design Not Applicable | Governance ruling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-44 (BLG-GOV-372) | Split-credit secondary tally in compute_role_share_history.py | Design Not Applicable | Governance script | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-45 (BLG-QA-212) | Unit tests for compute_role_share_history.py | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-46 (BLG-QA-209) | Scope utils.* test stubs | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-47 (BLG-QA-213) | Guard the positions.fees_paid NOT NULL invariant | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-48 (BLG-QA-202) | Remove the leaked sandbox /tmp path from backend/setup.cfg | Design Not Applicable | Configuration | N/A | N/A | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

**No flags.** No item introduces or extends a call to an AI provider. Each AI-adjacent item modifies the inputs, filtering or validation of an existing call that is already covered:

- **ST-01:** journal summary input type. Covered by `SRB-v1.7-2026-03-02__release-v1.7.md` and `decisions--2026-04-17__release-v2.8.md` (BLG-FEAT-16). This restores the existing call and does not extend it.
- **ST-02, ST-03 and ST-04:** briefing and chat. Covered by `decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`. Each one narrows or checks output, or corrects context labels.
- **ST-05:** monthly narrative. Covered by `decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md` (CONDITIONAL). The wider directive scan supports that review's conditions.
- **ST-06:** counts existing Claude spend and adds no call.

The AI endpoint security checklist is not triggered: no new AI-calling endpoint. ST-14 and ST-37 are §13-relevant but not AI. Their ACs already cite §13.3 and §13.5 under the clause-citation rule (`design_gate_prompt.md` v1.11).

## Blocked Items

None.

## Notes

### Post-gate-correction addendum

`claude/cycles/2026-10-12__release-v9.12/stage4_backlog_slice_addendum.md` was created with 4 items: ST-23, ST-24, ST-10 and ST-22. Sprint Planning and Sprint Execution must read it together with the sealed slice. Each item corrects or clarifies within an item's existing scope. None changes scope.

### Artefacts produced and specs updated

- **Design artefacts produced this run:** 6 decision records covering 8 items, under `docs/design/2026-10-12__release-v9.12/`:
  - `trail-stop-action` (ST-10)
  - `frozen-stop-indicator` (ST-15)
  - `trade-entry-atr-preview` (ST-17 and ST-18)
  - `settings-copy-and-last-change` (ST-20 and ST-26)
  - `grace-panel-position-link` (ST-22)
  - `light-theme-support` (ST-23, RISK-03)
- **ST-24** uses the pre-existing `BLG-FE-165` rule, with no new record.
- **Frontend specs updated (9 files):** each is logged in `prompt_change_log.md`.
  - `positions.md` 2.15→2.16
  - `components/position_form.md` 1.8→1.9
  - `settings.md` 1.8→1.9
  - `risk_dashboard.md` 0.1.12→0.1.13
  - `reports.md` 0.22→0.23
  - `notifications.md` 0.10→0.11
  - `dashboard.md` 3.8→3.9
  - `trade_plan.md` 1.17→1.18
  - `strategy_benchmark.md` 0.7→0.8

  `position_form.md` sits in `components/` but is the Trade Entry page spec. The v9.10 gate updated it on the same basis.

### Obligations passed to Sprint Execution (outside this gate's write scope)

- **New routes and the CLAUDE.md §2 registration chain (RISK-04):**
  - **ST-17:** `GET /market/atr/{ticker}`.
  - **ST-10:** `PATCH /positions/{id}/stop`, Branch A only.

  Each needs, in the same commit: a `##` contract heading, an `openapi.yaml` entry, a `routers/test.py` entry, the `SystemStatus.js` fallback count and `SC-SS-01b`. If both ship, recompute the count from `routers/test.py` at merge.
- **New response fields:**
  - ST-15's `stop_frozen_reason` on `GET /positions`, in `position_endpoints.md` and `openapi.yaml`.
  - ST-26's `last_change` on `GET /settings`, in `settings_endpoints.md` and `openapi.yaml`.
- **ST-23** adds the light-mode token table to `docs/specs/frontend/design_system.md` (Class 1). It also corrects `docs/frontend/design_system.md` §6 (Class 2, stale "dark-only" statement). Both files are outside this gate's write scope.
- **ST-21:** a display mirror of the strategy numbers already exists at `src/lib/strategyParameters.js`, pinned by `tests/test_strategy_parameter_parity.py`. ST-21's AC names `src/constants/strategy.js`. Sprint Planning should confirm whether the story creates the new module and moves the mirror into it, or treats the existing module as satisfying the AC, so that two sources are not left in place.
- **Observation, not filed:** `strategy_benchmark.md` §7 lists tinted exit-reason badges, while the shipped Trade Log uses filled ones. `bg-teal-600 text-white` (Rebalance) also measures about 3.7:1, below AA. This is outside ST-24's amber scope. Recommend filing it with `/backlog-add` at Sprint Planning.

### Playwright coverage (CLAUDE.md §2)

Each Design Required decision record's testability section lists its assertions. Three go beyond the slice's ACs, so execution must add them or file a backlog item before the PR opens:
- **ST-10:** the no-raise note when `trail_difference ≤ 0`.
- **ST-15:** no indicator during grace.
- **ST-22:** `data-highlighted` on the target row.

ST-20 and ST-22's text alignment are wording only (FI-P3-02).

### Motion and timing (§6)

One new timing parameter: ST-22's 2000 ms deep-link highlight, specified in its record and in `positions.md` §Position Deep Link. ST-17 reuses Trade Entry's existing 300 ms debounce, so it adds no new parameter.

### Other

- **Preflight observation:** the cycle-level `state.json` has no `sprint_sealed` key, while the root pointer has `sprint_sealed: false`. It is treated as unsealed, the same as the v9.6, v9.10 and v9.11 gates.

### Role sign-offs

Head of UX & Design and Product Owner confirmations are agent-mediated (Design Gate Engine acting under those roles), consistent with prior gates. The product calls the Product Owner may wish to review before `plan sprint` are:

1. **Light mode supported (ST-23, RISK-03).** This rests on the Class 1 design system, the shipped toggle, and five prior gates that treated light-theme defects as defects.
2. **Keeping the spec's Grace Period wording** over the shipped text, and the 2-second deep-link highlight (ST-22).
3. **Recommending rejection, not storage,** of a supplied entry `stop_price` (ST-10 AC 3). Also, renaming the button "View Trail" if the ruling forbids manual stops.
4. **Never placing the fetched ATR into the input** (ST-17), so `atr_source` stays `system`. This is shown as a "Fetched:" hint instead.
5. **Disabling submit for an implausible typed ATR** (ST-18). It is the only Trade Entry validation that blocks submit, as the item's AC requires.
