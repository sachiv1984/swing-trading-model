Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-10

# QA Evidence — EPIC-07 — Governance Process

**EPIC:** EPIC-07 — Governance Process
**Cycle:** 2026-11-06__release-v9.16
**Branch:** `exec/2026-11-06__release-v9.16/EPIC-07`
**Sprint goal:** Ship Site Structure & Usability Phase 2 complete (job-based sidebar with parent and onward links, the Dashboard Today list, "Plan this" with suggested size, the plan-linked pre-entry acknowledgement fix `BLG-FE-271`, and the first semantic colour tokens), and close the Anthropic key exposure by rotating the overdue key (`BLG-OPS-214`, P1) and removing the key secret from the public Pages build (`BLG-OPS-213`). EPIC-07 is governance support work. It does not carry a sprint-goal deliverable.
**Test scenarios used:** `tests/test_arc_velocity_report.py` (ST-29). ST-28 and ST-30 change governance documents only and were verified by document inspection against their ACs.

## Story evidence

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-28 | `claude/system/post_ship_closure.md#3.1 Mark shipped items complete` | `post_ship_closure.md` v2.45→v2.46. The STEP 3.1 split-achievability carve-out now has two cases. (i) Keep the item open when any unmet AC is tracked only by an escalation or by the source item. (ii) Banner the source ✅ COMPLETE, naming the follow-up items, when every unmet AC has moved to a named follow-up backlog item filed that cycle. Partial follow-up coverage stays case (i). Commit `5243368b`. | AC 1: "STEP 3.1 states both cases, citing `BLG-AI-23`/`BLG-AI-27` as the case (ii) example" | Pass. Both cases appear in STEP 3.1 and case (ii) cites `BLG-AI-23` → `BLG-AI-27`. | None |
| ST-28 | as above | — | AC 2: "`BLG-AI-23` and `BLG-OPS-48` are bannered or given a recorded reason to stay open at the next `groom backlog`" (*post-merge*, marked at seal) | Not due before merge. Marked `post-merge` in the sealed `sprint_backlog.md`, tracked by `BLG-GOV-414` (LL-v9.13-P3-03 exception: graded on in-sprint ACs). | None (planned post-merge, `BLG-GOV-414`) |
| ST-29 | `docs/governance/arc_velocity_report_arc2.md` (Case B); `claude/cycles/velocity_metrics.md`; `tests/test_arc_velocity_report.py` | Arc 2 velocity report (v3.1–v6.1, 31 cycles): stories per cycle, arc velocity 0.951, EPIC completion rate 0.963, 6-cycle rolling velocity, and findings. Reusable generator `scripts/arc_velocity_report.py`, with 7 tests. Commit `c196c094`. | AC 1: Arc 2 velocity report covering v3.1–v6.1, produced from `velocity_metrics.md` and the cycle records | Pass. Story counts come from `velocity_metrics.md` and EPIC counts from each cycle's `execution_state.json`. `test_arc2_report_matches_generator_output` checks that the committed data section equals the generator's output. | None |
| ST-29 | as above | — | AC 2: report format reusable for Arc 3+ | Pass. The generator takes any `--from`/`--to` range, and `--out` rewrites only the marked data section. The report's "Reusing this format for Arc 3+" section gives the steps. The range, EPIC-denominator, rolling-window and missing-input tests use synthetic fixtures. | None |
| ST-29 | as above | — | AC 3: PMO Lead confirms at the sprint planning seal that the cleared gate's evidence holds | Pass (met at seal). `sprint_backlog.md` Product Owner Sign-Off: "PMO Lead (ST-29) confirmed, agent-mediated (§5.3), 2026-11-09". | None |
| ST-29 | as above | — | AC 4: any governance prompt change making the report a Release Planning input follows CLAUDE.md §6 in the same commit; otherwise it is filed as a backlog item | Pass. No governance prompt was changed. The work is filed as `BLG-GOV-415` (arc-close output + arc-boundary Release Planning input), which is present in `backlog.md` (verified by grep). | None |
| ST-30 | `claude/system/OPERATIONAL_GUIDE.md#8.3 Delegation Model` | Base44 prompt versioning convention in `OPERATIONAL_GUIDE.md` §8.3 (v4.256). Each filed prompt carries a `**Story:**` header line, and each `delegated_frontend` delegation record carries a `**Base44 prompt file:**` field. Commit `1c21656d`. | AC 1: a dated decision names the convention (comment header, delegation log field, or both) | Pass. Base44 Frontend Prompt Owner ruling "both", 2026-11-10, given in session by the user acting in that role. It is recorded in `ESC-EXEC-20261110-02` (Resolved) and mirrored to `.claude_current_state.json` on `main`. | None |
| ST-30 | as above | — | AC 2: convention written into `OPERATIONAL_GUIDE.md` frontend delegation text and/or `execution_prompt.md` under CLAUDE.md §6 in the same commit | Pass. Added to `OPERATIONAL_GUIDE.md` §8.3, with the version 4.255→4.256 header, §14 self-row and Change Log top row, plus a `prompt_change_log.md` row, all in commit `1c21656d`. | None |
| ST-30 | as above | — | AC 3: one existing delegation log entry with a Base44 draft shown to satisfy the convention, or a dry-run example recorded | Pass (dry-run). §8.3 records `DEL-20260629-02` (v6.3 ST-11) with `docs/frontend/prompts/strategy-benchmark-v1.md`, whose header already reads `**Story:** ST-11 (BLG-FEAT-53, EPIC-03, v6.3)`. The delegation record predates the new field, so the dry run shows the line it would carry. | None |

## QA test coverage

- **Scenarios run:** `tests/test_arc_velocity_report.py`, 7 passed locally (stub `DATABASE_URL`, project venv). CI on each story commit:
  - ST-28 `5243368b`: all 7 workflows success (CI Pytest Suite 42791340576).
  - ST-29 `c196c094`: all 7 workflows success (CI Pytest Suite 42791766580, Critical-Path Smoke 42791766855).
  - ST-30 `1c21656d`: all 7 workflows success (CI Pytest Suite 42792403600).
- **Regression areas checked:**
  - `scripts/check_prompt_size_budget.py` passes. `post_ship_closure.md` is 72,734 bytes against its 72,930 baseline. To stay within it, three precedent sentences were moved verbatim to `post_ship_closure_changelog.md` 2.46.
  - `scripts/check_backlog_item_integrity.py` passes after `BLG-GOV-415`.
  - `scripts/check_execution_state_consistency.py` passes after each state write.
  - Pre-commit OpenAPI three-way drift check: no drift.
- **Governance self-consistency (execution_prompt.md §3.2.A, LL-v8.5-P3-01):** `OPERATIONAL_GUIDE.md` was bumped twice in this EPIC. In both cases the header `**Version:**`, the §14 self-row and the Change Log top row match: 4.255 after ST-28 and 4.256 after ST-30. `post_ship_closure.md` 2.46 matches in its header, the §10 source-prompt line and the §14 Post-Ship Closure Engine row.
- **Frontend testing gate:** not applicable. No story touches `src/**` and no AC is observable UI behaviour.
- **Deviations:** none filed. ST-28 AC 2 is a seal-marked post-merge AC (`BLG-GOV-414`), not a deviation.
- **CLAUDE.md §8 step 2a note for later merges:** this EPIC bumps `OPERATIONAL_GUIDE.md` (4.255, 4.256) and `post_ship_closure.md` (2.46). EPIC-06 ST-25 may bump `shared_standards.md` and `OPERATIONAL_GUIDE.md`. After this EPIC merges, check those per file and renumber where needed.

## Decisions and Escalations

- `ESC-EXEC-20261110-02` (ST-30, Lifecycle, Base44 Frontend Prompt Owner): raised 2026-11-10T09:34:25Z and resolved 2026-11-10T09:37:55Z in session. Ruling: both.
- **ST-30 reclassification (execution_prompt.md §5.1, LL-v2.3-EX-02):** sealed as `delegated_decision`. After the ruling resolved the decision, it was reclassified to `autonomous` for the write. `execution_state.json` records `classification: autonomous`, with the history in the story notes. Because the EPIC had a `delegated_*` story, the BLG-GOV-19 autonomous-class sign-off was not used (`qa_evidence_template.md` mixed-class note).
- **DoQ review pass 1 (agent-mediated, 2026-11-10): Blocked.** Finding 1 was blocking: the Arc 2 report said five of the six shortfalls fell in v5.4–v5.8, but the correct figure is four, and v4.1 was omitted. Fixed, together with non-blocking findings 2, 3, 5 and 6, in the ST-29 follow-up commit. Finding 4 (the placeholder for ST-30's CI) was filled before the review completed.

- **PR #2230 review (agent-mediated, on behalf of Director of Quality and Product Owner, 2026-11-10):** both reviews were Approved with Comments, and no story grade changed. Two non-blocking follow-ups were filed. `BLG-GOV-416`: the Base44 prompt file field is not yet in the `shared_standards.md` §16.3 delegation schema or `base44_frontend_prompt_owner.md` §7/§12 (ST-30 AC 2 was met in `OPERATIONAL_GUIDE.md`). `BLG-GOV-417`: ST-28 case (ii) should carry an open escalation onto the follow-up item before the source is bannered. There was also a note with no filing: for an arc shorter than 6 cycles, pass `--window` to get a rolling figure. The human QA sign-off and PO acceptance are still required at merge.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend change
- [x] **Strategy values checked:** N/A — no stop/grace/ATR/exit/sizing logic touched
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-11-10
- Comments: Pass 1 was Blocked (1 blocking and 5 non-blocking findings; see Decisions and Escalations). Pass 2 on `788f3ce0` was Approved, with all six findings fixed and the arithmetic re-shown. 365−347 = 18 missed stories = 14 gate + 3 `delegated_frontend` + 1 PO deferral. 6 cycles are below 1.00, so 25 of 31 are at 1.00. The lowest rolling velocity is 4.46/6 = 0.743 and the rolling velocity at arc close is 5/6 = 0.833. `tests/test_arc_velocity_report.py`: 7 passed. The generator's output is identical to the report's data section. `check_prompt_size_budget.py`: OK. `check_execution_state_consistency.py`: OK. After pass 2, the STEP 0 changelog sentence's escaped quotes were made byte-identical to the original. CI: all 7 workflows succeeded on each story commit (runs listed above). All 9 ACs are graded Pass. ST-28 AC 2 is post-merge, as marked at seal, and tracked by `BLG-GOV-414`. No deviations were filed. Human Director of Quality QA sign-off and Product Owner acceptance remain required at the merge gate. This agent-mediated sign-off does not satisfy them.

## Merge Gate Confirmations

- **Director of Quality QA sign-off:** given by the human repository owner, acting as Director of Quality, in session at 2026-11-10T09:54:17Z ("give DOQ and PO acceptance"), before the merge. It accepts:
  - this evidence, with all 9 in-sprint ACs for ST-28, ST-29 and ST-30 graded Pass;
  - the agent-mediated sign-off block above: pass 1 was Blocked (1 blocking and 5 non-blocking findings, all fixed in `99b3c818`, `788f3ce0` and `23f478e2`), and pass 2 was Approved;
  - the agent-mediated PR #2230 review (comment 6764295689): DoQ ⚠️ Approved with Comments and PO ⚠️ Approved with Comments, with no blocking finding and follow-ups filed as BLG-GOV-416 and BLG-GOV-417.

  At acceptance the PR head was `2f04ece9`, with 36 checks passed, 3 pending, 5 skipped and no failures. The pending checks must be green before merge.
- **Product Owner acceptance:** given by the human repository owner, acting as Product Owner, in the same instruction at 2026-11-10T09:54:17Z, before the merge. It accepts ST-28, ST-29 and ST-30 against `stage4_backlog_slice.md`, including:
  - the ST-30 convention ruling ("both", `ESC-EXEC-20261110-02`);
  - `BLG-GOV-26`'s arc-close and Release Planning scope moving to BLG-GOV-415 under ST-29 AC 4.

  Post-merge AC: ST-28 AC 2, tracked by BLG-GOV-414 at the next `groom backlog`. Follow-ups: BLG-GOV-414, BLG-GOV-415, BLG-GOV-416, BLG-GOV-417.
- **Merge:** pending. To be recorded (who, when, merge commit) when the human merges PR #2230.
