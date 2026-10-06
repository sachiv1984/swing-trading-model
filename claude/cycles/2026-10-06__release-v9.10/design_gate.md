**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-06
**Cycle:** 2026-10-06__release-v9.10

# Design Gate Record — 2026-10-06__release-v9.10

## Gate Status: PASSED

Completed: 2026-10-06
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

All 21 items are cleared:

| Classification | Count | Items |
|----------------|-------|-------|
| Design Required | 8 | ST-01, ST-06, ST-07, ST-08, ST-09, ST-10, ST-12, ST-14 |
| Design Pre-Approved | 3 | ST-02, ST-19, ST-20 |
| Design Not Applicable | 10 | the remaining items |

Every Design Required item has an approved decision record and an updated frontend spec. There are no blocked items, and `sprint_planning_pre_condition` is met.

**Classification note:** the slice flagged EPIC-02 and EPIC-03 as carrying observable UI ACs. STEP 1 confirmed this for ST-06 to ST-10, ST-12 and ST-14, and added ST-01:

- **ST-01** is a backend-first item, but it has two visible parts:
  - The Settings form fallbacks currently seed `5`/`2`/`3` against the spec's `10`/`5.0`/`2.0`.
  - Ruling (a) in AC 2 explicitly turns the Settings stop parameters read-only.

  It is classified Design Required and given a ruling-conditional design.
- **ST-11 and ST-13** are rulings. Their UI consequences are absorbed by ST-12 and ST-14.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-BE-138) | One source for §11 stop parameters across the on-load and nightly stop paths | Design Required | Settings form fallbacks are visible values (code `5`/`2`/`3` vs spec/§11 `10`/`5.0`/`2.0`). Ruling (a)/(c) changes the Strategy Parameters from inputs to read-only values. Designed for all 3 ruling outcomes; the ruling itself stays with the Strategy Rules & System Intent Owner. | `docs/design/2026-10-06__release-v9.10/stop-parameter-settings-presentation/decision_record.md` (new) | `settings.md` v1.6 → v1.7 (§1 Strategy Parameter Fallbacks and Editability) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-02 (BLG-BE-139) | Remove silent ATR fallbacks and record ATR provenance | Design Pre-Approved | Backend plus an API field (`atr_source`). Its AC renders nothing; the display of `atr_source` is designed under ST-06 (optional " · estimated" / " · entered" suffix). | N/A | `positions.md` v2.11 (locked reference — §Stop Provenance Line covers any display of `atr_source`) | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-SPEC-187) | Contract corrections: losing-stop formula, analyze side effects, settings-change effect | Design Not Applicable | API contract and docstring corrections, no UI. The settings-change-effect text it writes is reused by the ST-01 outcome (b) UI note. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 (BLG-QA-207) | Unit-test the live exit decision and grace-period behaviour | Design Not Applicable | Backend tests and traceability matrix only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 (BLG-BE-137) | Rule on strategy-version registry coverage and enforce it with a test | Design Not Applicable | Governance ruling, docstring/spec alignment, test only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 (BLG-FE-193) | Show ATR, active multiplier and recalculation source in the stop-loss cell | Design Required | New data displayed (provenance line, per-row tooltip) and changed explainer copy. Needs a new on-load/nightly source field, recorded as an execution obligation. | `docs/design/2026-10-06__release-v9.10/stop-cell-provenance/decision_record.md` (new) | `positions.md` v2.10 → v2.11 (§Stop Provenance Line and Per-Row Stop Details; explainer copy) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-07 (BLG-FE-197) | Trade Entry shows the stop and risk the system will actually store | Design Required | Removes an input, adds a read-only system-stop panel, and changes field labels and the risk/sizing basis | `docs/design/2026-10-06__release-v9.10/trade-entry-system-stop/decision_record.md` (new) | `position_form.md` v1.6 → v1.7 (§ATR (14-day), §Initial Stop (set by system), widget Idle state) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-08 (BLG-FE-198) | Exit dialog pre-selects the exit reason the system already knows | Design Required | Changed default interaction plus a new explanatory note in `ExitModal`, and a new `?exit=` deep link | `docs/design/2026-10-06__release-v9.10/exit-condition-surfacing/decision_record.md` (new, shared with ST-09) | `positions.md` v2.11 (§Exit Dialog Pre-Selection and Deep Link) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-09 (BLG-FE-199) | Morning briefing card for §8 exit recommendations | Design Required | New conditional Morning Briefing element. Placed as a full-width row above the 5-card grid so the grid layout is unchanged. §13 pre-check: deterministic, no AI call. | `docs/design/2026-10-06__release-v9.10/exit-condition-surfacing/decision_record.md` (new, shared with ST-08) | `dashboard.md` v3.6 → v3.7 (§1A Exit Conditions Met Row) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-10 (BLG-FE-194) | Recent Trades badge shows a neutral glyph for a break-even trade | Design Required | Visible glyph change. Applies the existing `design_system.md` v1.21 neutral-zero rule to the glyph. | `docs/design/2026-10-06__release-v9.10/recent-trades-neutral-glyph/decision_record.md` (new) | `dashboard.md` v3.7 (§4 Card 5 icon glyph) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-11 (BLG-SPEC-185) | Reconcile the lifecycle-state registry with strategy_rules.md §9 | Design Not Applicable | Ruling and spec reconciliation, no UI of its own. The badge consequences are designed under ST-12 (the `flat_after_grace` copy is dormant if §9 governs). | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 (BLG-FE-196) | Positions lifecycle badge agrees with the §6 grace window, in calendar days | Design Required | Changed badge label, tooltip copy, alert copy and a new UNKNOWN reason display. Needs a backend reason field, recorded as an execution obligation. | `docs/design/2026-10-06__release-v9.10/lifecycle-badge-grace-calendar-days/decision_record.md` (new) | `positions.md` v2.11 (§Position Lifecycle State Badge, §Grace Period Alert Zone) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-13 (BLG-GOV-365) | Gap Risk Flag §13.3 ruling on UK-ticker earnings flags and day-0 timing | Design Not Applicable | Strategy ruling and tests. The label impact is designed under ST-14. §13 pre-check: a ruling on an existing deterministic flag, no AI call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 (BLG-BE-136) | Gap risk flag: weekend-hold disposition and trigger-timing label/spec alignment | Design Required | Changed reason-label text, plus a possible removal of a visible reason. Designed per disposition branch. | `docs/design/2026-10-06__release-v9.10/gap-risk-trigger-label-alignment/decision_record.md` (new) | `positions.md` v2.11 (§Gap Risk Reason Labels) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-15 (BLG-GOV-140) | AI chat advisory §13 quarterly self-audit checklist | Design Not Applicable | Governance document. §13 pre-check: audits existing AI chat, introduces no AI call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 (BLG-GOV-141) | AI model output logging completeness audit | Design Not Applicable | Code-path audit and possible backend logging fix, no UI. §13 pre-check: covers logging of existing `POST /ai/daily-briefing` and `POST /ai/chat` calls, adds or extends no AI call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 (BLG-OPS-92) | Quarterly dependency update review | Design Not Applicable | Security/ops review, no UI. Any dependency upgrade it applies must keep existing Playwright green. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 (BLG-OPS-171) | Confirm the stale-staging-deploy alert fires on a real condition | Design Not Applicable | CI/ops verification, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 (BLG-QA-195) | Add Reports and Notifications pages to the axe scan | Design Pre-Approved | Test coverage. Any serious/critical fix must use existing `design_system.md` tokens (contrast pairs) and change no layout. A fix needing a new colour or layout change needs its own design pass. | N/A | `design_system.md` v1.21 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-SPEC-171) | Correct the PO-05 pre-assessment and replay page spec wording | Design Pre-Approved | Spec/document wording. The replay results-view caption is a wording-only change inside an existing caption element (`replay-fx-basis-caption` area), decided by the Strategy Rules & System Intent Owner per AC 1. No layout, colour or interaction change (CLAUDE.md §2 FI-P3-02 wording-only exception applies). | N/A | `replay_mode.md` v0.2 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-21 (BLG-GOV-357) | Sign-off single-point-of-failure matrix | Design Not Applicable | Governance document under `docs/ops/`, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

No item introduces or extends a call to an AI provider. AI-adjacent items are checked individually:

- **ST-15:** a self-audit checklist for the existing AI chat.
- **ST-16:** a logging-completeness audit of the existing `POST /ai/daily-briefing` and `POST /ai/chat` paths. A fix to `database.create_claude_audit_entry()`'s error swallowing is a logging change, not an AI call.
- **ST-09:** a deterministic display of §8 conditions the system already computes.
- **ST-13 and ST-14:** concern the deterministic gap-risk flag, which already has a §13 review record (`docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`). ST-13 adds an addendum to it.

No `Gate Status: §13 PRE-CHECK REQUIRED` flags. The AI endpoint security checklist (`ai_endpoint_security_checklist.md`) is not triggered.

## Blocked Items

None.

## Notes

### Artefacts produced and specs updated

- **Design artefacts produced this run (7 decision records, covering 8 items):** under `docs/design/2026-10-06__release-v9.10/`:
  - `stop-parameter-settings-presentation`
  - `stop-cell-provenance`
  - `trade-entry-system-stop`
  - `exit-condition-surfacing` (shared by ST-08 and ST-09, which share one predicate)
  - `recent-trades-neutral-glyph`
  - `lifecycle-badge-grace-calendar-days`
  - `gap-risk-trigger-label-alignment`
- **Frontend specs updated (4 files):** `positions.md` 2.10→2.11, `dashboard.md` 3.6→3.7, `settings.md` 1.6→1.7, `position_form.md` 1.6→1.7. Each is logged in `prompt_change_log.md`.
- **Write-scope interpretation, disclosed:** `position_form.md` is the canonical Trade Entry spec, but it lives under `docs/specs/frontend/components/`, not `pages/`. This follows the `2026-09-14__release-v9.4` gate precedent, which bumped `position_form.md` v1.3→v1.4 for ST-28. No Trade Entry spec exists under `pages/`.

### Ruling-conditional designs

Three designs depend on rulings that are sub-steps of their own stories. Each design specifies every outcome, so execution is not blocked waiting for the gate. The story's own spec-sync commit removes the branches that were not chosen:

- **ST-01:** parameter authority (a), (b) or (c).
- **ST-12:** the post-grace `flat_after_grace` copy is dormant if the ST-11 ruling says §9 governs.
- **ST-14:** whether the weekend-hold trigger is removed or retained.

### Obligations passed to Sprint Execution (outside this gate's write scope)

- **ST-06** needs a new nullable field on `GET /positions` that distinguishes on-load from nightly stop recalculation (working name `stop_calculation_source`). It is naturally written by ST-01's changes to both paths.
- **ST-12** needs a backend UNKNOWN reason field (working name `lifecycle_reason`) and a grace-first, calendar-day classification in `position_lifecycle_service.py`.
- **ST-14** may shrink the `gap_risk.reasons` enum.
- Each of these must update `position_endpoints.md` and `docs/reference/openapi.yaml` in the same commit (CLAUDE.md §2). None adds a new route, so `backend/routers/test.py` is unaffected unless execution adds one.
- **ST-14** must also update `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md` §5 (named in its own AC 3). That file is a prior cycle's artefact, outside this gate's write scope.

### Playwright coverage (CLAUDE.md §2)

All 8 Design Required items carry observable UI ACs. Each decision record's §5 lists the Playwright assertions. ST-01's Settings fallback assertion is new; the slice's ST-01 ACs do not name Playwright, so execution must add it or file a backlog item before the PR opens.

### Sequencing (from the slice, still binding)

- ST-01's ruling comes before ST-03, ST-06 and ST-07.
- ST-08 comes before ST-09, which share the predicate.
- ST-13 comes before ST-14.
- ST-11's ruling shapes ST-12's post-grace copy only.

### Observations (out of scope, not actioned)

- `dashboard.md` §1A's Cards table still describes a "Positions to Act On" card. The shipped card is "Positions to Watch" (`ExitZoneCard.js`, grace alerts). This is noted inline in the spec. It is pre-existing drift, in the same family as the v9.9 gate's Card 5 observation, and a candidate BLG-SPEC item.
- The v9.9 gate's observation about the Card 5 Recent Activity prose remains open.

### Other

- **Post-gate-correction addendum:** not required. No correction to the sealed `stage4_backlog_slice.md` was needed. The ruling-conditional designs fit within each item's existing AC.
- **Motion/timing (§6):** no motion or timing parameter changes. ST-06's tooltip reuses the existing 200 ms explainer delay, and ST-07's toast uses the existing toast-timing standard.
- **Preflight observation:** the cycle-level `state.json` carries no `sprint_sealed` key, while the root pointer has `sprint_sealed: false`. It is treated as unsealed, the same as the v9.6 gate.

### Role sign-offs

Head of UX & Design and Product Owner confirmations are agent-mediated (Design Gate Engine acting under those roles), consistent with prior gates. The genuine product calls the Product Owner may wish to review before `plan sprint` are:

1. Removing the Trade Entry Stop Price input outright rather than relabelling it (ST-07).
2. Placing the exit card as a conditional full-width row rather than a sixth card (ST-09).
3. Risk-off taking priority over stop breach in pre-selection (ST-08).
4. The GRACE badge switching from days-in-state to days-left (ST-12).
