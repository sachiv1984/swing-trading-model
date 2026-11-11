Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active — Signed off
Last Updated: 2026-11-11
Cycle: 2026-11-06__release-v9.16

---

# Delivery Verification Report — 2026-11-06__release-v9.16

## 1. Verification Status

```
Status: Verified_with_deviations
Sprint goal: Ship Site Structure & Usability Phase 2 complete (job-based sidebar with parent and onward links, the Dashboard Today list, "Plan this" with suggested size, the plan-linked pre-entry acknowledgement fix BLG-FE-271, and the first semantic colour tokens), and close the Anthropic key exposure by rotating the overdue key (BLG-OPS-214, P1) and removing the key secret from the public Pages build (BLG-OPS-213).
Cycle: 2026-11-06__release-v9.16
Backlog slice source: claude/cycles/2026-11-06__release-v9.16/stage4_backlog_slice.md (read with its additive stage4_backlog_slice_addendum.md; no amended_backlog_slice_path)
Verification run: 2026-11-11T15:22:33Z
Mode: standard
```

All 30 stories merged. There is no P0, no open P1, no `Fail` result and no traceability gap. Three P3 canonical-spec deviations are recorded. Five open P2 found defects have documented Product Owner and Director of Quality acceptance: `BLG-BE-211`, `BLG-FE-278`, `BLG-FE-281`, `BLG-FE-282` and `BLG-OPS-217` (see §4 Acceptance Records).

**Preflight (STEP -1).**
- Branch `main`, in sync with `origin/main`.
- `execution_state.json` is `sealed: true` (2026-11-11T15:17:34Z). This is a single-file cycle, with no `execution_state/` directory.
- `.claude_current_state.json` status is `Sprint_Complete`.
- No amended slice. The slice pointer matches `execution_state.json.backlog_slice_source`.
- `sprint_close.md` Verification Readiness Statement: all three fields `Yes`.
- All 7 merged EPICs have a QA evidence log signed `Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)`. That is a compliant format. Each log has a date, all checkboxes ticked, and a `## Merge Gate Confirmations` section recording the human DoQ and PO confirmations.
- All 7 EPICs have a non-null `pr_number`. GitHub confirms each PR (#2227 to #2233) is `MERGED`, at the `merged_utc` recorded in `execution_state.json`.
- All required input files in Section 4 are present.

## 2. Traceability Matrix

| ST Item | Title | Outcome | Spec Reference | Backlog Entry |
|---------|-------|---------|----------------|---------------|
| ST-01 | Build the job-based sidebar and surface Trade Plans and Research | merged | `navigation.md`; `sidebar-nav-groups.spec.js` and 3 more specs | N/A |
| ST-02 | Add a parent link on detail pages | merged | `navigation.md` §Parent Links; `parent-links.spec.js` | N/A |
| ST-03 | Give each dead-end page an onward next-step link | merged | `navigation.md` §Onward Links; slice addendum § ST-03; `onward-links.spec.js` | N/A |
| ST-04 | Anchor the digest's Risk Dashboard link to the right section | merged | `analytics.md` §19.1; `digest-section-link/decision_record.md` | N/A |
| ST-05 | Require the acknowledgement on plan-linked Trade Entry when the plan's checks were WARN/FAIL | merged | `position_form.md#Pre-Entry Checks`; `trade_plan.md#5e`; `strategy_rules.md#4.2.1`; `trade_plan_endpoints.md#PUT /trade-plans/{id}` | N/A |
| ST-06 | Build the "Today" action list on the Dashboard | merged | `dashboard.md#1B` | N/A |
| ST-07 | Add "Plan this" to Signals and Screener rows | merged | `signals.md`; `screener_results.md#11.1`; `trade_plan.md#5a.1`; `signal-to-plan-flow/decision_record.md` | N/A |
| ST-08 | On Trade Plan, show the suggested size before asking for shares | merged | `trade_plan.md#5f` | N/A |
| ST-09 | Semantic colour tokens for the base, card and table shells | merged | `design_system.md#Semantic Colour Tokens`; `semantic-colour-tokens/decision_record.md` | N/A |
| ST-10 | Inputs apply dark:text-slate-400 to typed text instead of the placeholder | merged | `design_system.md#Input Text Colours` | N/A |
| ST-11 | Rotate the Anthropic API key and revoke the old key | done (EPIC merged) | `external_api_credential_inventory.md`; `api_key_rotation_and_audit_schedule.md` | N/A |
| ST-12 | Stop injecting REACT_APP_ANTHROPIC_API_KEY into the public GitHub Pages build | done (EPIC merged) | `deploy.yml`; `TradePlan.js`; `trade_plan.md`; slice addendum § ST-12 | N/A |
| ST-13 | Record the weekly market-data call-volume baseline from production | done (EPIC merged) | `data_model.md#DS-36`; `data_pipeline_cost_baseline.md` | N/A |
| ST-14 | Record the full screener run p50/p95 baseline from production | done (EPIC merged) | `api_performance_baseline.md#53` | N/A |
| ST-15 | Fail the staging smoke host check when the backend reports no Render service ID | done (EPIC merged) | `staging_smoke_test.py`; `staging_deploy_notes.md` | N/A |
| ST-16 | Exiting a US position with a NULL fill_price fails in the P&L arithmetic | merged | `data_model_positions_dictionary.md` | N/A |
| ST-17 | Lifecycle badge and Risk page disagree for a US row with no fill_price and no fx_rate | merged | `position_endpoints.md#GET /positions` | N/A |
| ST-18 | Frozen-stop marker is not written when the on-load recompute has no live price | merged | `position_endpoints.md#GET /positions/analyze` | N/A |
| ST-19 | Read production briefing ticker-caveat tokens and add any non-tickers | merged | `ai_endpoints.md#POST /ai/daily-briefing` | N/A |
| ST-20 | Handle _NON_TICKER_WORDS entries that are also real tickers deliberately | merged | `ai_endpoints.md#POST /ai/daily-briefing`, `#POST /ai/chat` | N/A |
| ST-21 | Journal summary: remove the stale AI_MODEL override line | merged | `ai_endpoints.md#POST /ai/journal-summary` | N/A |
| ST-22 | Add the 11 missing positions columns to the positions data dictionary | merged | `data_model_positions_dictionary.md` | N/A |
| ST-23 | Point settings.md at the moved strategy constants module | merged | `settings.md` | N/A |
| ST-24 | Arc 2 end-to-end QA protocol | merged | `arc2_e2e_qa_protocol.md`; `arc2-happy-path.spec.js` | N/A |
| ST-25 | Arc 2 DoQ standards review | merged | `arc2_doq_standards_review.md`; `shared_standards.md#25` | N/A |
| ST-26 | Trade plan lifecycle end-to-end test | merged | `trade-plan-lifecycle.spec.js` | N/A |
| ST-27 | Arc 2 user journey map | merged | `arc2_user_journey_map.md` | N/A |
| ST-28 | Split-achievability carve-out | merged | `post_ship_closure.md#3.1` | N/A |
| ST-29 | Arc velocity tracking dashboard | merged | `arc_velocity_report_arc2.md`; `velocity_metrics.md` | N/A |
| ST-30 | Base44 prompt versioning convention | merged | `OPERATIONAL_GUIDE.md#8.3` | N/A |

`Traceability gaps: 0 | Items returned: 0 | Backlog entries added this run: 0`

EPIC-04's five stories are recorded as `done`, and their EPIC is `merged` (PR #2233). Every story's `spec_references` is non-empty, and every story has `deviations_filed = true`. `execution_state.json.deferred_at_planning` is empty, and no slice item was deferred at planning. The slice mentions `ST-33` only as a reference to v9.15's ST-33, the item seated again this cycle as ST-13. It is not an in-scope item.

## 3. QA Evidence Summary

| EPIC | Items | Pass | Fail | Sign-off | Notes |
|------|-------|------|------|----------|-------|
| EPIC-01 | 4 | 4 (ST-01 Pass_with_deviation) | 0 | ✓ DoQ (agent-mediated §5.3) 2026-11-09; human DoQ/PO before merge 2026-11-09 | `DEV-NAV-ST01-01` (P3) |
| EPIC-02 | 4 | 4 (ST-05 Pass_with_deviation) | 0 | ✓ DoQ 2026-11-09; human 2026-11-09T15:13:44Z | `DEV-v9.16-ST05-01` (P3); found gap `BLG-FE-278` (P2, accepted) |
| EPIC-05 | 8 | 8 | 0 | ✓ DoQ 2026-11-10; human 2026-11-10 | — |
| EPIC-07 | 3 | 3 | 0 | ✓ DoQ 2026-11-10; human 2026-11-10 | ST-28 AC 2 post-merge (seal-marked, `BLG-GOV-414`) |
| EPIC-06 | 4 | 4 (ST-26 Pass_with_deviation) | 0 | ✓ DoQ 2026-11-10; human 2026-11-10T13:41:19Z; P2 acceptances 2026-11-11T15:13:05Z | Found defects `BLG-BE-211`, `BLG-FE-281`, `BLG-FE-282` (P2, accepted) |
| EPIC-03 | 2 | 2 | 0 | ✓ DoQ 2026-11-10 (pass 5 of 5); human before merge 2026-11-11 | — |
| EPIC-04 | 5 | 5 (ST-12 Pass_with_deviation) | 0 | ✓ DoQ 2026-11-11; human 2026-11-11T11:54:34Z; P2 acceptance 2026-11-11T15:13:05Z | `DEV-v9.16-ST12-01` (P3); ST-12 post-merge ACs met 2026-11-11; found defect `BLG-OPS-217` (P2, accepted) |

**STEP 2.1 / 2.3 checks.**
- Every `Result` is a recognised value: `Pass`, `Pass (met at seal)`, `Pass (dry-run)` or `Pass_with_deviation`. ST-28 AC 2 reads "Not due before merge". It is a seal-marked post-merge AC (LL-v9.13-P3-03), checked in §5.
- Each `Pass_with_deviation` names its AC gap and a confirmed backlog item:
  - ST-01: `DEV-NAV-ST01-01` / `BLG-SPEC-226`.
  - ST-05: `DEV-v9.16-ST05-01` / `BLG-FE-277`.
  - ST-12: AC 3 moved post-merge / `BLG-OPS-218`, and `DEV-v9.16-ST12-01` / `BLG-SPEC-229`.
  - ST-26: `active`→`closed` not assertable / `BLG-BE-211`.
- All 7 sign-off blocks have every checkbox ticked, and each has a substantive Comments field.

**Found-defect rule (LL-v9.11-P4-01 / LL-v9.13-P4-01).** This was applied at every grade.
- ST-26 (`Pass_with_deviation`) found `BLG-BE-211` (P2), so its severity is P2, not the P3 default.
- `Pass` grades also named P2 found defects: ST-24 (`BLG-FE-281`), ST-27 (`BLG-FE-282`) and ST-13 (`BLG-OPS-217`).
- `BLG-FE-278` (P2) is a found gap from the PR #2228 review of ST-05.
- All five take §7's PO + DoQ acceptance path (§4).

**ST-12 AC 3.** It was moved post-merge by the PO at the merge gate, not at seal, so it keeps the `Pass_with_deviation` grade as signed. Its tracker `BLG-OPS-218` was met on 2026-11-11 (console check), before this run. There is no remaining gap.

**STEP 2.2.** No AC was narrowed or omitted without a filed backlog item. Two planned remainders are checked in §5, not as deviations:
- ST-06 locked `dashboard.md` §1B TL-01..TL-29 except TL-09 and TL-10 at seal (`sprint_backlog.md` ST-06 Notes, RISK-04). Those two ACs need `BLG-BE-205`.
- The seal-marked post-merge ACs are ST-12 AC 2 and the production half of AC 4 (`BLG-OPS-215`), and ST-28 AC 2 (`BLG-GOV-414`).

**Frontend testing gate (CLAUDE.md §2).** EPIC-01, EPIC-02, EPIC-03 and EPIC-04 (ST-12) record Playwright coverage, run in real CI, for every observable AC. None records an AC as "code review only". EPIC-05, EPIC-06 and EPIC-07 change no `src/**` file.

## 4. Deviation Register

Three canonical-spec `DEV-*` records were filed this sprint. The register also covers each `Pass_with_deviation` gap and each found defect listed in `sprint_close.md` "Deviations Filed This Sprint". Priorities are read from `backlog.md`.

| Deviation Ref | ST Item | Priority | Description | Disposition | Backlog Item |
|---------------|---------|----------|-------------|-------------|--------------|
| `DEV-NAV-ST01-01` | ST-01 | P3 | Sidebar collapse state survives a full page reload; `navigation.md` says it resets | Recorded. Known Deviations entry present (`navigation.md` §Known Deviations) | `BLG-SPEC-226` (P3) |
| `DEV-v9.16-ST05-01` | ST-05 | P3 | Edited plan's pre-entry snapshot is replaced but never cleared, because `PUT` treats `null` as "leave unchanged" | Recorded. Known Deviations entry present (`trade_plan.md`) | `BLG-FE-277` (P3) |
| `DEV-v9.16-ST12-01` | ST-12 | P3 | `trade_plan.md` §5b still names the removed `HAS_AI` gate | Recorded. Known Deviations entry present (`trade_plan.md`) | `BLG-SPEC-229` (P3) |
| PWD-ST12-AC3 | ST-12 | P3 (deviation); tracker P2 | AC 3 (console check) moved post-merge at the merge gate | Resolved post-merge 2026-11-11, before this run. PO accepted the move, and the DoQ the grade, at 2026-11-11T11:54:34Z | `BLG-OPS-218` (P2; met, ✅ banner pending post-ship closure) |
| FD-ST26 | ST-26 | **P2** | Found pre-existing defect: no backend path moves a linked plan to `closed`, so `active`→`closed` cannot be asserted | **Accepted** (PO + DoQ, 2026-11-10T13:41:19Z) | `BLG-BE-211` (P2) |
| FD-ST05 | ST-05 | **P2** | Found gap (PR #2228 DoQ review): Trade Plan pre-entry acknowledgement is not reset when the check result changes | **Accepted** (PO + DoQ, 2026-11-09T15:13:44Z) | `BLG-FE-278` (P2) |
| FD-ST24 | ST-24 | **P2** | Found pre-existing defect: Research "Create Trade Plan" drops the market, so UK plans open as US | **Accepted** (PO + DoQ, 2026-11-11T15:13:05Z) | `BLG-FE-281` (P2) |
| FD-ST27 | ST-27 | **P2** | Found pre-existing defect: Trade Plan Stop Level is not pre-filled from the §5 stop (`trade_plan.md` §5a.3) | **Accepted** (PO + DoQ, 2026-11-11T15:13:05Z) | `BLG-FE-282` (P2) |
| FD-ST13 | ST-13 | **P2** | Found pre-existing defect: 665 of 7,105 weekly production calls fail, all Yahoo calls in on-demand features | **Accepted** (PO + DoQ, 2026-11-11T15:13:05Z) | `BLG-OPS-217` (P2) |

### Hard Blocks

- P0: none.
- P1: none open. `BLG-OPS-214` (P1, carried from v9.15) is closed by ST-11.
- P2 open: `BLG-BE-211`, `BLG-FE-278`, `BLG-FE-281`, `BLG-FE-282` and `BLG-OPS-217`. All five are accepted with a rationale (below), and each has a confirmed backlog item.
- `BLG-OPS-218` (P2 tracker for ST-12 AC 3) and `BLG-OPS-215` (P2 seal-marked post-merge tracker) were both met on 2026-11-11 and are not open.

### Acceptance Records

| Item | Priority | Accepted by | When | Rationale | Source |
|------|----------|-------------|------|-----------|--------|
| `BLG-BE-211` | P2 | Product Owner and Director of Quality (the user, holding both roles) | 2026-11-10T13:41:19Z, before the merge | The backend gap existed before this sprint. The `active`→`closed` transition cannot be tested until the backend writes it. | `qa_evidence_EPIC-06.md` Merge Gate Confirmations |
| `BLG-FE-278` | P2 | Product Owner and Director of Quality (the user) | 2026-11-09T15:13:44Z, before the merge | The PR #2228 DoQ review rated it non-blocking. Both roles accepted it by name as a follow-up. | `qa_evidence_EPIC-02.md` Merge Gate Confirmations |
| `BLG-FE-281` | P2 | Product Owner and Director of Quality (the user) | 2026-11-11T15:13:05Z, at sprint close | It existed before this sprint, and no v9.16 code introduced it. Tracked at P2 for v9.17. | `qa_evidence_EPIC-06.md` Merge Gate Confirmations |
| `BLG-FE-282` | P2 | Product Owner and Director of Quality (the user) | 2026-11-11T15:13:05Z, at sprint close | It existed before this sprint, and no v9.16 code introduced it. Seated ahead of the other v9.17 P2s, per the PO's PR #2231 note. | `qa_evidence_EPIC-06.md` Merge Gate Confirmations |
| `BLG-OPS-217` | P2 | Product Owner and Director of Quality (the user) | 2026-11-11T15:13:05Z, at sprint close | It existed before this sprint; ST-13 only measured it. Tracked at P2 for v9.17. | `qa_evidence_EPIC-04.md` Merge Gate Confirmations |

### Known Deviations Sync (LL-v2.3-CL-03)

- All three `DEV-*` records have a Known Deviations entry in their canonical spec. Each entry carries priority, description, canonical requirement, target, owner and the matching backlog reference: `navigation.md` `DEV-NAV-ST01-01` → `BLG-SPEC-226`; `trade_plan.md` `DEV-v9.16-ST05-01` → `BLG-FE-277`; `trade_plan.md` `DEV-v9.16-ST12-01` → `BLG-SPEC-229`. No stale placeholder references remain.
- The `Pass_with_deviation` rows not backed by a `DEV-*` record (ST-12 AC 3, ST-26) are exempt under `ESC-CLOSE-20260930-03`. Neither comment shows shipped behaviour contradicting the cited spec. ST-12 AC 3 was an evidence-timing gap. ST-26's gap is a pre-existing backend omission found by a test, and `trade-plan-lifecycle.spec.js` is its only spec reference.
- The found defects `BLG-FE-281`, `BLG-FE-282` and `BLG-OPS-217` are pre-existing and are not divergences introduced by this sprint's stories. Their backlog entries, together with this register, are the tracking record. `BLG-FE-282` names `trade_plan.md` §5a.3. Whether that spec should carry a Known Deviations entry for the pre-existing gap is routed to Post-Ship Closure STEP 5 for the Frontend Specifications & UX Documentation Owner. This engine may not edit canonical specs (§5).

## 5. Outstanding Items and Deferred Execution Blockers

### (a) Outstanding items carried to backlog

| Item | Type | Outcome | Backlog ref |
|------|------|---------|-------------|
| ST-28 AC 2 | Seal-marked post-merge AC | Open. Due at the first `groom backlog` after ST-28 merged | `BLG-GOV-414` ✓ |
| ST-12 AC 2 and AC 4 production half | Seal-marked post-merge AC | Met 2026-11-11 (secret deleted; production AI control works). ✅ banner pending post-ship closure | `BLG-OPS-215` ✓ |
| ST-12 AC 3 | Moved post-merge at the merge gate | Met 2026-11-11 (console shows one active key). ✅ banner pending post-ship closure | `BLG-OPS-218` ✓ |
| ST-06 TL-09 / TL-10 (Stops moved group) | Excluded at seal (RISK-04) | Open, waiting for the backend data | `BLG-BE-205` ✓ |
| ST-13 / ST-14 source items | Met by this sprint's stories | ✅ banners pending post-ship closure | `BLG-OPS-197` ✓, `BLG-OPS-198` ✓ |
| Delegations `DEL-20261110-01`, `DEL-20261111-01`, `DEL-20261111-02`, `DEL-20261111-03` | Human-Delegation | All unblocked and terminal in-sprint | N/A |
| `ESC-EXEC-20261110-01`, `ESC-EXEC-20261110-02` | This cycle's escalations | Both `Resolved` in session | N/A |
| `ESC-EXEC-20260910-01` (cycle v9.3) | Prior-cycle Deferred escalation, non-blocking | Not from this cycle. Its trigger (`DEL-20261030-04`) is still unmet | `BLG-GOV-399` ✓ |

No new `backlog.md` entries were required. Every outstanding item already has a traceable entry. `delegated_items` and `blocked_items` are empty. The 41 out-of-scope follow-ups filed during execution are listed in `sprint_close.md` and are not repeated here.

### (b) Deferred execution blocker dispositions

No deferred execution blockers. `state.json.deferred_execution_blockers` is `[]`.

### Stale parked items (STEP 4.3)

Skipped. The authoritative slice contains no `parked` items.

## 6. Test Coverage Assessment

Every EPIC has a populated `test_scenarios` list. Every listed file exists on disk and is cited in its EPIC's QA evidence log, either under "Scenarios run" or in the per-story evidence. Frontend-visible ACs in EPIC-01, EPIC-02, EPIC-03 and EPIC-04 (ST-12) have Playwright coverage run in real CI.

No story replaced a core algorithm, model or scoring function, so the AUD-2026-06-22-007 advisory does not apply. ST-17 changes the native-entry fallback order, and ST-20 moves four words to a context rule. Both extend existing logic, and both are covered by purpose-built tests listed in `test_scenarios`.

| EPIC | Scenario files | Cited as run | Status |
|------|----------------|--------------|--------|
| EPIC-01 | 8 | 8 | Covered |
| EPIC-02 | 6 | 6 | Covered |
| EPIC-03 | 5 | 5 | Covered |
| EPIC-04 | 3 | 3 | Covered |
| EPIC-05 | 9 | 9 | Covered |
| EPIC-06 | 2 | 2 | Covered |
| EPIC-07 | 1 | 1 | Covered |

### Test Scenario Gaps — Structured Register

No test scenario gaps identified. Table N/A.

These known coverage remainders already have their own backlog items, so they are not new gaps:
- `BLG-BE-211`: `active`→`closed` in the lifecycle test, once the backend writes it.
- `BLG-BE-205`: TL-09 and TL-10.
- `BLG-QA-254`: UK tickers in "Plan this".
- `BLG-QA-255`: mobile action rows.
- `BLG-QA-257`: staging check of US badges.
- `BLG-QA-258`: Arc 2 write-through checks on staging.
- `BLG-QA-259`: coverage matrix re-derivation.
- `BLG-QA-260`: axe "incomplete" results.

## 7. System Status Confirmation

**Confirmed accurate, with the routine status-line update.** `docs/System_status_report.md` § Sprint 2026-11-06__release-v9.16 does the following:
- It lists all 7 merged EPICs with correct spec references.
- It records "None" under "Capabilities deferred or returned". This is correct: none of the 30 stories was returned or deferred.
- It shows each P3 deviation and each accepted P2 found defect against its capability row.

Corrections made this run:
1. `**Status:**` line updated from `Sprint_Complete — pending verification` to `Verified_with_deviations — 2026-11-11` (routine, BLG-GOV-170).
2. `**Last Updated:**` header updated (current entry plus 2 prior, per `shared_standards.md` §16.14).

## 9. Sign-off Block

## Director of Quality Sign-off

- [x] Traceability complete (or gaps documented with rationale)
- [x] QA evidence reviewed and accepted
- [x] Deviation register reviewed; all P0/P1/P2 dispositions confirmed
- [x] Test coverage gaps actioned (backlog items created)
- [x] System status report confirmed accurate
- [x] Deferred execution blockers dispositioned

Signed off by: Director of Quality (the user, in session)
Date: 2026-11-11
Comments: Signed off as Verified_with_deviations. The three P3 deviations are recorded, with Known Deviations entries and backlog items. The P2 acceptances for `BLG-BE-211`, `BLG-FE-278`, `BLG-FE-281`, `BLG-FE-282` and `BLG-OPS-217` are re-confirmed. ST-12's post-merge ACs are met (`BLG-OPS-215`, `BLG-OPS-218`).

## Product Owner Acceptance

- [x] Outstanding items confirmed in backlog
- [x] P1/P2 deviation acceptances confirmed (if any)
- [x] Deferred execution blocker outcomes acknowledged
- [x] Next cycle cleared to open

Accepted by: Product Owner (the user, in session)
Date: 2026-11-11
Comments: Accepted. Outstanding items are confirmed in the backlog (`BLG-GOV-414`, `BLG-BE-205`, plus `BLG-OPS-215`, `BLG-OPS-218`, `BLG-OPS-197` and `BLG-OPS-198`, all met and awaiting banners). The P2 acceptances are re-confirmed. There are no deferred execution blockers. The next cycle is cleared to open.
