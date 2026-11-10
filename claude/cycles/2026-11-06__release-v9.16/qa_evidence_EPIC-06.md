Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-10

# QA Evidence — EPIC-06 — Arc 2 Retrospective: QA Protocol, Lifecycle Test & Journey Map

**EPIC:** EPIC-06 — Arc 2 Retrospective: QA Protocol, Lifecycle Test & Journey Map
**Cycle:** 2026-11-06__release-v9.16
**Branch:** `exec/2026-11-06__release-v9.16/EPIC-06`
**Sprint goal:** Ship Site Structure & Usability Phase 2 complete (job-based sidebar with parent and onward links, the Dashboard Today list, "Plan this" with suggested size, the plan-linked pre-entry acknowledgement fix `BLG-FE-271`, and the first semantic colour tokens), and close the Anthropic key exposure by rotating the overdue key (`BLG-OPS-214`, P1) and removing the key secret from the public Pages build (`BLG-OPS-213`). EPIC-06 is Arc 2 retrospective work. It tests and reviews the "Plan this" and suggested-size flow the sprint goal ships, and does not itself carry a sprint-goal deliverable.
**Test scenarios used:** `tests/e2e/trade-plan-lifecycle.spec.js` (ST-26, SC-TPL-01..05), `tests/e2e/arc2-happy-path.spec.js` (ST-24, SC-ARC2-01..05), both over the shared mock `tests/e2e/mocks/trade-plan-lifecycle-backend.js`. ST-25 and ST-27 produce documents and were verified by document inspection against their ACs.

## Story evidence

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-26 | `tests/e2e/trade-plan-lifecycle.spec.js` (Case C) | One Playwright journey: Signals "Plan this" → Trade Plan (Setup Quality Score shown, stop entered, ST-08 suggested size pre-fills shares, R target and early-exit conditions) → Save (`draft`) → reopen (score still shown) → Trade Plans "Start Trade" → Trade Entry → Create Position (`draft` → `active`, `position_id` set) → Positions Exit → Trade History Plan vs Reality (+1.51R, target 2R, −0.49R delta, +0.93% entry delta, Early Exit, PROFITABLE), values worked by hand in the test. Stateful mock copies the backend's link, §5 initial-stop, planned-entry snapshot and `plan_vs_reality_service.py` rules. Commit `3bb258da` (mock moved to a shared module in `46aed77f`). | AC 1: full lifecycle Playwright test authored and passing in CI | Pass_with_deviation. Passed first attempt in Playwright E2E run 42797119521 on `3bb258da` and in run 42797687776 on `46aed77f`; 3/3 locally. Mutation check: with Trade Entry sending `trade_plan_id: null` the test fails. Scope bullets: plan state transitions `draft`→`active` asserted (store log and Trade Plans badge); quality score persistence asserted as "shown again on reopen" (the score is recomputed per ticker, not stored on the plan, so that is what persistence means here); plan-vs-reality accuracy asserted against hand-worked values. The `active`→`closed` transition is not asserted because the backend does not perform it (`BLG-BE-211`, below). | `BLG-BE-211` — scope's "plan state transitions" is met for `draft`→`active` only; `active`→`closed` cannot be asserted until the backend writes it |
| ST-26 | as above | — | AC 2: QA Lead and Product Owner confirm at the sprint planning seal that the cleared gate's evidence holds | Pass (met at seal). `sprint_backlog.md` ST-26 notes: "Cleared-gate evidence confirmed at seal by the QA Lead (agent-mediated) and the Product Owner — AC 2 met." | None |
| ST-24 | `docs/qa/arc2_e2e_qa_protocol.md` (Case B); `tests/e2e/arc2-happy-path.spec.js` | Arc 2 arc-level QA protocol v1.0: feature inventory (PT-01..05 plus later flow additions), feature-level Playwright coverage map, happy path A1–A7 and its automation, 15-item manual checklist (backend write-through, data conditions, judgement), defects found. New Playwright journey SC-ARC2-01..05: Screener → Research View (score, heat) → Create Trade Plan → suggested size → thesis, R target, all four checklist items → Save (`draft`, checklist persisted) → Research shows the plan → Start Trade → linked (`active`). Commit `46aed77f`. | AC 1: Arc 2 E2E protocol document produced and filed in `docs/qa/` | Pass. `docs/qa/arc2_e2e_qa_protocol.md`. Two checklist claims were checked in code before commit: M-03 auto-link picks the newest plan (`ORDER BY created_at DESC LIMIT 1`); M-05 a partial exit writes a `trade_history` row. | None. Incidental findings filed: `BLG-FE-281`, `BLG-BE-212` |
| ST-24 | as above | — | AC 2: core happy path covered by Playwright | Pass. SC-ARC2-01..05 (Screener → linked position) plus ST-26's SC-TPL-01..05 (exit and Plan vs Reality) cover A1–A7. SC-ARC2 passed first attempt in Playwright E2E run 42797687776; the run reports 1 flaky test, the Reports axe scan, which is unrelated and seen before in this cycle. | None |
| ST-24 | as above | — | AC 3: QA Lead and Product Owner confirm at the sprint planning seal that the cleared gate's evidence holds | Pass (met at seal). `sprint_backlog.md` ST-24 notes: "confirmed at seal by the QA Lead (agent-mediated) and the Product Owner — AC 3 met." | None |
| ST-25 | `docs/qa/arc2_doq_standards_review.md` (Case B); `claude/system/shared_standards.md` §25 | Review of the DoQ rubric (`qa_evidence_template.md` v1.18, `execution_prompt.md` v3.93 §3.2.A, CLAUDE.md §2) against the six Arc 2 EPIC QA evidence files. Three gaps, each with a defect on `main` it let through; five Arc 2-era gaps already closed. `shared_standards.md` v3.41→v3.42 §25: conditional DoQ checks 25.1 hand-off, 25.2 lifecycle, 25.3 data gate. Commit `fcb00246`. | AC 1: DoQ standards reviewed; gaps (if any) documented | Pass. `docs/qa/arc2_doq_standards_review.md` §2–§3. | None |
| ST-25 | as above | — | AC 2: if amendments warranted, `shared_standards.md` updated per the CLAUDE.md §6 governance checklist | Pass. Header 3.42; `OPERATIONAL_GUIDE.md` 4.256→4.257 (header, §14 Shared Standards row, §14 self-row, Change Log top row); `shared_standards_changelog.md` 3.42; two `prompt_change_log.md` rows. Size budget held at 95,869 ≤ 95,910 bytes by moving five history passages verbatim to the changelog (§11 headroom rule). Template wiring is outside the AC and filed as `BLG-GOV-418`. §25's own sign-off line awaits the Head of Specs Team review below. | None. Follow-up: `BLG-GOV-418` |
| ST-25 | as above | — | AC 3: QA Lead confirms at the sprint planning seal that the cleared gate's evidence holds | Pass (met at seal). `sprint_backlog.md` ST-25 notes: "Cleared-gate evidence confirmed at seal by the QA Lead (agent-mediated) — AC 3 met." | None |
| ST-27 | `docs/ux/arc2_user_journey_map.md` (Case B) | Arc 2 user journey map, screener discovery → plan → execution: 7 entry points, stage table with steps and what carries over at each hand-off, 5 friction points, recommendation (maintain the structure, fix the hand-offs). Commit `3875e325`. | AC 1: journey map produced in `docs/ux/` alongside `si05_user_journey_map.md` | Pass. `docs/ux/arc2_user_journey_map.md`. | None |
| ST-27 | as above | — | AC 2: friction points enumerated; actionable items filed as backlog entries, cross-checked against the Site Structure & Usability programme items so no duplicate is filed | Pass. F-01..F-05. Filed `BLG-FE-282` (P2, F-03: Stop Level not pre-filled per `trade_plan.md` §5a.3, so the plan's size can rest on a stop Trade Entry will not store; `strategy_rules.md` §4.1.8), `BLG-FE-283` (P3, F-01 entry/signal), `BLG-FE-284` (P3, F-02); F-01 market and F-05 reference `BLG-FE-281` and `BLG-BE-211`. Cross-check list in the map §5, including held Phase 3 `BLG-FE-257`–`263`, `265`. All five items verified present in `backlog.md` by grep; integrity check passes. | None |
| ST-27 | as above | — | AC 3: Product Owner confirms at the sprint planning seal that the cleared gate's evidence holds | Pass (met at seal). `sprint_backlog.md` ST-27 notes: "Cleared-gate evidence confirmed at seal by the Product Owner — AC 3 met." | None |

## QA test coverage

- **Scenarios run:** `tests/e2e/trade-plan-lifecycle.spec.js` and `tests/e2e/arc2-happy-path.spec.js`, locally against the dev server and in CI. CI on each story commit:
  - ST-26 `3bb258da`: all 8 workflows success (Playwright E2E 42797119521, CI Pytest Suite 42797119509).
  - ST-24 `46aed77f`: all 8 workflows success (Playwright E2E 42797687776, CI Pytest Suite 42797688159).
  - ST-25 `fcb00246`: all 7 triggered workflows success (CI Pytest Suite 42798465550).
  - ST-27 `3875e325`: see sign-off comments.
- **Regression areas checked:**
  - No file under `src/**` or `backend/**` changed in this EPIC (`git diff --stat origin/main...HEAD`); the existing feature-level specs are untouched. `trade-plan-lifecycle.spec.js`'s refactor onto the shared mock was re-run locally and in CI with the same result.
  - `scripts/check_prompt_size_budget.py` passes (shared_standards.md 95,869 ≤ 95,910).
  - `scripts/check_backlog_item_integrity.py` passes after every backlog write.
  - `scripts/check_execution_state_consistency.py` passes after every state write.
- **Governance self-consistency (execution_prompt.md §3.2.A, LL-v8.5-P3-01):** `OPERATIONAL_GUIDE.md` header `**Version:**` 4.257, §14 self-row 4.257 and Change Log top row 4.257 match; §14 Shared Standards row reads v3.42, matching `shared_standards.md`'s header and its changelog top row.
- **CLAUDE.md §8 step 2a (RISK-07):** EPIC-07, which owns `OPERATIONAL_GUIDE.md` and `prompt_change_log.md` this cycle, merged before this branch was cut (`903147c4`), so 4.257 and 3.42 are the next free versions on `main`. EPIC-03 and EPIC-04 are still open; whichever merges after this EPIC must check these two files per file.
- **Frontend testing gate:** no story changes `src/**` and no AC is observable UI behaviour. ST-24 and ST-26 add Playwright tests; they are themselves the evidence.
- **Same-EPIC cross-story testing-gap check:** ST-24 and ST-26 share the "journey over a stateful mock" shape and the same known limits (no real backend write-through; `active`→`closed` not asserted). Both are recorded in the protocol (§4.2, §5.1) and the lifecycle test header; no sibling gap left unfiled.
- **Deviations:** none filed in a canonical spec. ST-26 is graded `Pass_with_deviation` against `BLG-BE-211` (the `active`→`closed` transition cannot be tested until the backend performs it). All four stories' deviation checks completed. The pre-existing `trade_plan.md` §5a.3 divergence found by ST-27 (Stop Level not pre-filled) is a gap in earlier work, tracked by `BLG-FE-282`, not a deviation of this EPIC's deliverables.

## Incidental findings filed this EPIC

| ID | Priority | Finding | Found by |
|----|----------|---------|----------|
| `BLG-BE-211` | P2 | No backend path moves a linked plan to `closed` when its position closes | ST-26 |
| `BLG-FE-281` | P2 | Research "Create Trade Plan" drops the market; UK plans open as US | ST-24 |
| `BLG-BE-212` | P3 | Plan vs Reality's planned entry comes from the signal price at exit, not the plan | ST-24 |
| `BLG-GOV-418` | P3 | Wire `shared_standards.md` §25 into the QA evidence template | ST-25 |
| `BLG-FE-282` | P2 | Trade Plan Stop Level not pre-filled from the §5 stop (spec §5a.3); size can rest on a stop Trade Entry will not store | ST-27 |
| `BLG-FE-283` | P3 | Research "Create Trade Plan" drops entry price and signal | ST-27 |
| `BLG-FE-284` | P3 | No "Start Trade from Plan" right after saving a new plan | ST-27 |

## Review passes

- **DoQ / Head of Specs Team / Head of UX & Design review pass 1 (agent-mediated, §5.3, 2026-11-10):** Director of Quality Blocked; Head of Specs Team Blocked; Head of UX & Design Approved. Blocking findings and fixes: (1) ST-26 AC 1 graded `Pass` although `active`→`closed` is in scope and unasserted — regraded `Pass_with_deviation`, Deviations `BLG-BE-211`; (2) journey-map edit, this file and `execution_state.json` uncommitted — committed; (3) `shared_standards.md` §25 heading carried ticket IDs (CLAUDE.md §2) — moved to the Purpose line. Non-blocking, also fixed: Strategy-values line overstated the mocked size as a §4.1 result (reworded; the reviewer computed §4.1.3 on the fixture as 14.72, not 10.7); size figure corrected to 95,869 bytes after the heading fix (was quoted 95,859, measured 95,906 before the fix); mock header now states its partial copies (no auto-link fallback, 2 dp stop rounding, fixed size fixture); §4.1.8 cite corrected to §4.1.1 in the map and here; `§25: not applicable` recorded below. The reviewer showed its Plan vs Reality arithmetic (166.75; 26/17.25 = 1.507 → 1.51; −0.49; 1.70/182.30 = 0.93%; 1.03% → minor_deviation; early_exit), matching the test.

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend change
- [ ] **Strategy values checked:** ST-26 test oracle — initial stop = entry − 5×ATR (`strategy_rules.md` §5, `InitialATRMultiplier` 5.0 per `src/constants/strategy.js`); the suggested size is a mocked pass-through of `POST /portfolio/size` (10.7 → 10 shares), not a §4.1 result — the test checks that the response reaches Planned Shares, and §4.1.3 itself is unit-tested elsewhere. ST-27 F-03 — §4.1.1 (the Stop in sizing is the entry-time initial stop) and §5.
- Signed off by: PENDING
- Date:
- Comments:
