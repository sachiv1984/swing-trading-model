---
name: first-time-right
description: Run the first-time-right checks for a sprint story so it ships right first time and files fewer follow-up backlog items. Use at the start of every story that changes code or a spec (before writing code), and again before its commit and before asking for review. Use whenever the user says "first-time-right", "pre-build check", "are we ready to build ST-xx?", or when a story touches a value shown on screen, a shared function, a stored field, a spec premise or test fixtures. Records a dated "First-time-right:" line in the story's execution_state.json notes, which the commit-gates hook looks for.
---

# First-Time-Right Checks

Twenty checks, each learned from a real miss in v9.17 (EPIC-01 filed 12 follow-ups; EPIC-04, -05, -06 and -07 added the rest). Run them in two passes:
- **Pass A, before build:** checks 1–8, 11, 17–20. These shape what you build.
- **Pass B, before commit or review:** checks 9, 10, 12–16, plus a re-run of 18 and 19 against the tests you wrote.

The checks are judgement calls, which is why this is a skill and not a hook. The commit-gates hook only warns when a story has no record (Step 4).

## Step 0 — Load lessons

Read `.claude/skills/lessons_learnt.md` and apply any entries tagged `[first-time-right]`.

## Step 1 — Identify the story

1. Read `.claude_current_state.json` and get `active_cycle` and `execution_state_path`.
2. Read the story's acceptance criteria in `claude/cycles/<cycle_id>/stage4_backlog_slice.md`, the addendum if one exists, and its `sprint_backlog.md` notes.
3. Read the specs the ACs name and any design record they name.
4. List:
   - every value the story **shows**, **writes**, **derives** or **reads**;
   - every shared function it changes;
   - every spec premise it relies on ("only X does Y", "written by Z").

## Step 2 — Pass A (before build)

For each check, write one line: **done**, **N/A** (with the reason), or **raised** (with what was raised to whom). Raise means stop and ask the owning role (via `AskUserQuestion` when the user holds the role) before building that part.

1. **Data source, units and currency.**
   - For every field the story shows, open its contract in `docs/specs/api_contracts/` and confirm the endpoint returns it for the whole list shown.
   - Then trace the number to the code that **writes** it. Note its unit (GBP or native, pence or pounds, 2 dp or 4 dp, UTC or local) before combining it with any other field. The contract may not say.
   - *(ST-14: a US signal's `atr_value` is GBP while `current_price` is USD.)*
2. **Worked examples.** For a value shown on more than one surface, or a rule with a threshold, write the exact text each surface shows for boundary inputs: 0, 1, 2, null, true/false/null, and a value exactly at the threshold.
3. **Pure logic.** Check new `src/lib` or helper functions with a quick `node -e` run on null, missing, string, 0 and negative inputs. CI has no frontend unit tests until BLG-QA-262.
4. **Test data for layout.** Layout, no-scroll and axe tests use populated fixtures for every panel on the page. Axe checks also fail on `incomplete`.
5. **Review depth.** Plan a `/code-review` at **high** when this story creates a module that later stories build on. Otherwise medium.
6. **Collision grep.** When replacing UI, grep `tests/e2e` for the old body copy as well as headings and labels.
7. **Spec premises.** For every "only X does Y" or "written by X", grep every writer of that field or behaviour. If the premise is false, raise it.
8. **Time boundaries.** For any date, window or "latest" rule, write examples for:
   - stale data (no event for a week);
   - quiet days and weekends;
   - UTC midnight;
   - the latest row disappearing.

   Raise a missing data source, such as a run date, before choosing an assumption.
11. **Competing user-set values.** When a threshold lives only in code, grep for any user-set value of the same concept and write one example where they disagree. Raise it before choosing wording.
17. **Readers of a new state.** When the story adds a new write or state transition, grep every **reader** of that field. Run the normal case, the partial case and a legacy row (NULL foreign key, pre-migration shape) through each. Fix readers this change breaks; file only what was already wrong.
18. **Real-shaped fixtures.** Plan fixtures from the writer's own formula or from a real row:
    - Fields derived from each other must agree.
    - A NOT NULL column must not be null.
    - Include one case where the rounding is not exact.
19. **Change matrix for derived UI.** For every value the page derives (a pre-fill, a computed line):
    - list each input that can change after it is shown (ticker, market, entry, a fetch that arrives late, edit vs new, a user clearing the field);
    - write the expected screen for each.
20. **Copy in edge cases.** Read every new user-facing string in each edge case from 2, 8 and 19. If a literal reading of the spec would mislead the user ("tick again" when nothing was ticked; "results changed" when nothing visible changed), raise it for a wording ruling.

## Step 3 — Pass B (before commit or review)

9. **Fix, don't file, your own XS gaps.** A gap in this story's own work that takes under an hour gets fixed here, not filed.
10. **Specs stay in sync.** Any follow-up commit that changes behaviour updates the contract, data model, OpenAPI and page spec in the same commit.
12. **Ask for the follow-up query with the run.** When asking permission for a live read, include the check its known blind spots need.
13. **Read back edited Markdown tables.** After editing near a spec table, print the section with `sed -n` and confirm every row has the same number of `|`.
14. **Keep the query that tells causes apart.** Wait for it before naming a cause or a fix.
15. **Caller-units audit.** For a changed shared function, run one worked example through every caller. Grep the pattern class (`/ 100`, `> 1000`, `* fx`) and decide every instance together.
16. **Stored-data check.** When the change alters the meaning of values already written, ask permission and query the existing rows before asking for review.
- **Re-run 18 and 19 against the tests actually written.** Do the fixtures match the writer? Is every row of the change matrix asserted?

## Step 4 — Record

Append one line to the story's `notes` in `execution_state.json`. Pass A must be recorded **before** the first code commit:

```
First-time-right: <YYYY-MM-DD> pass A — 1 done (atr_value GBP for US, traced to signal_service.py:264); 7 raised (Trade Entry ATR source → wording ruling 2026-11-13); 19 done (ticker, entry, late signal); 3,4,5,6,8,11,17,18,20 done/N/A …
```

Add a `pass B` line before the review request. Keep each line short. Detail belongs in the commit message or the QA evidence.

`.claude/hooks/check_commit_gates.py` warns, and never blocks, when a story commit on an `exec/**` branch stages non-test `src/` or `backend/` code and that story's notes have no `First-time-right:` line.

## Step 5 — Report

Tell the user:
- which checks raised something, and what is waiting on a decision;
- what changed in the plan because of a check.

Do not list the "done" checks one by one.

## Error handling and lessons learnt

When a review or a backlog item later shows that a check missed something, or that a new kind of miss needs a check:
1. Add or sharpen the check here, with its origin in one parenthesis.
2. Append a row to `.claude/skills/lessons_learnt.md`: `| {date} | first-time-right | {what was missed} | {the check that now covers it} |`.

**Source:** the user's first-time-right direction (2026-11-12), built as a skill on 2026-11-16. These checks belong in `execution_prompt.md` STEP 3.1.A once Phase 3 lessons learnt and post-ship closure adopt them. BLG-GOV-422, BLG-QA-262 and BLG-TECH-35 will turn parts of them into design-gate and CI checks.
