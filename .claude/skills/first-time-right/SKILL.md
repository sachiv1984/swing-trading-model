---
name: first-time-right
description: Run the first-time-right checks for a sprint story so it ships right first time and files fewer follow-up backlog items. Use at the start of every story that changes code or a spec (before writing code), and again before its commit and before asking for review. Use whenever the user says "first-time-right", "pre-build check", "are we ready to build ST-xx?", or when a story touches a value shown on screen, a shared function, a stored field, a spec premise or test fixtures, or replaces, merges or renames a page. Records a dated "First-time-right:" line in the story's execution_state.json notes, which the commit-gates hook looks for.
---

# First-Time-Right Checks

Twenty-two checks, each learned from a real miss in v9.17 (EPIC-01 filed 12 follow-ups; EPIC-02, -04, -05, -06 and -07 added the rest). Run them in two passes:
- **Pass A, before build:** checks 1–8, 11, 17–21. These shape what you build.
- **Pass B, before commit or review:** checks 9, 10, 12–16 and 22, plus a re-run of 18 and 19 against the tests you wrote.

**Apply each check to everything the change touches, not only the new code.** Moved code, reused copy, child components and every reader of a renamed page count. Most of EPIC-02's follow-ups came from applying an existing check too narrowly (EPIC-02, v9.17).

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
   - For every **input** the page passes down (a period, a filter, an id), trace it through the API client to the request it actually sends. A parameter the client or endpoint drops silently is a spec question to raise now.
   - *(ST-14: a US signal's `atr_value` is GBP while `current_price` is USD. ST-06: the page period never reached `GET /analytics/compliance-metrics`, found late by a test — BLG-FE-299.)*
2. **Worked examples.** For a value shown on more than one surface, or a rule with a threshold, write the exact text each surface shows for boundary inputs: 0, 1, 2, null, true/false/null, and a value exactly at the threshold.
3. **Pure logic.** Check new `src/lib` or helper functions with a quick `node -e` run on null, missing, string, 0 and negative inputs. CI has no frontend unit tests until BLG-QA-262.
4. **Test data for layout.** Layout, no-scroll and axe tests use populated fixtures for every panel on the page. Axe checks also fail on `incomplete`.
5. **Review depth.** Plan a `/code-review` at **high** when this story creates a module that later stories build on. Otherwise medium.
6. **Collision grep.** When replacing UI, grep `tests/e2e` for the old body copy as well as headings and labels. When a page is renamed, merged or removed, grep the **whole repo** (`src`, `backend`, `tests`, `docs/specs`) for the old route **and** the old label, in every form: `#/Route`, `'/Route'`, `href*="Route"`, `createPageUrl("Route")`, link text and notification or digest copy. *(ST-05/ST-06: a test using `href*=` and the digest's link text kept the retired names — BLG-BE-222.)*
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
    - Build the response shape from the code that writes it (the service or router), not from the contract's summary: which object each field sits in, and its nesting. *(ST-06: fixtures put `has_enough_data` and the consistency fields in the wrong objects, which hid two adapter bugs until review.)*
    - Fields derived from each other must agree.
    - A NOT NULL column must not be null.
    - Include one case where the rounding is not exact.
19. **Change matrix for derived UI.** For every value the page derives (a pre-fill, a computed line, a deep-link jump):
    - list each input that can change after it is shown (ticker, market, entry, a fetch that arrives late, edit vs new, a user clearing the field);
    - list **every** async source on the page, including child components that start fetching only after they mount, and give each a "arrives late" row **and** a "fails" row;
    - write the expected screen for each.
    *(ST-06/ST-07: the section jump waited for the first request only, and a failed plan load never released it — BLG-FE-302.)*
20. **Copy in edge cases.** Read every new user-facing string in each edge case from 2, 8 and 19, **and every moved or reused string in its new context** (a component placed on a new page, or shown twice). If a literal reading would mislead the user ("tick again" when nothing was ticked; "results changed" when nothing visible changed; "Enter Your First Position" when the user has trades), raise it for a wording ruling. *(ST-06: copy moved from Analytics unchanged — BLG-FE-301.)*
21. **Parity with what the story replaces.** When a story replaces, merges or moves a page or panel, list every state of the **old** one (empty, few rows, below a threshold, loading, error, each period or filter) and write what the **new** one shows in the same state. Raise every difference the spec does not state as intended, before the spec is approved, and list the accepted ones as behaviour changes in the PR. *(ST-06: the new Summary hid Total P&L in quiet months where the old Reports tab showed it — BLG-FE-300, P2.)*

## Step 3 — Pass B (before commit or review)

9. **Fix, don't file, your own XS gaps.** A gap in this story's own work that takes under an hour gets fixed here, not filed.
10. **Specs stay in sync.** Any follow-up commit that changes behaviour updates the contract, data model, OpenAPI and page spec in the same commit.
12. **Ask for the follow-up query with the run.** When asking permission for a live read, include the check its known blind spots need.
13. **Read back edited Markdown tables.** After editing near a spec table, print the section with `sed -n` and confirm every row has the same number of `|`.
14. **Keep the query that tells causes apart.** Wait for it before naming a cause or a fix.
15. **Caller-units audit.** For a changed shared function, run one worked example through every caller. Grep the pattern class (`/ 100`, `> 1000`, `* fx`) and decide every instance together.
16. **Stored-data check.** When the change alters the meaning of values already written, ask permission and query the existing rows before asking for review.
22. **Navigation and structure basics.** For any custom link click handler, page section or deep link the story adds:
    - Ctrl/Cmd/Shift-click and middle-click still open a new tab (return early before `preventDefault()` on a modifier or non-primary button);
    - the heading outline stays nested: a component moved inside a new section drops a level, and a page-wide axe scan with `heading-order` passes (region-scoped scans miss it);
    - a deep link to a missing or failed item ends in a usable state, not a jump that never happens.
    *(ST-06/ST-07 — BLG-FE-302.)*
- **Re-run 18 and 19 against the tests actually written.** Do the fixtures match the writer? Is every row of the change matrix asserted? Does each test perform the action its row names: key-by-key typing (`pressSequentially`) for a debounce or typing rule, not a single `fill()`? *(ST-05: SC-JNL-17 used `fill()` — BLG-QA-266.)* Where the spec says "in order", does a test assert that order? *(ST-06: Summary card order — BLG-FE-301.)*

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
