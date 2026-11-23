---
name: first-time-right
description: Run the first-time-right checks for a sprint story so it ships right first time and files fewer follow-up backlog items. Use at the start of every story that changes code or a spec (before writing code), and again before its commit and before asking for review. Use whenever the user says "first-time-right", "pre-build check", "are we ready to build ST-xx?", or when a story touches a value shown on screen, a shared function, a stored field, a spec premise or test fixtures, or replaces, merges or renames a page. Records a dated "First-time-right:" line in the story's execution_state.json notes, which the commit-gates hook looks for.
---

# First-Time-Right Checks

Twenty-four checks, each learned from a real miss in v9.17 (EPIC-01 filed 12 follow-ups; EPIC-02 to -07 added the rest) or v9.18 EPIC-01. Run them in two passes:
- **Pass A, before build:** checks 1–8, 11, 17–21, 23 and 24. These shape what you build.
- **Pass B, before commit or review:** checks 9, 10, 12–16 and 22, plus a re-run of 18, 19 and 24 against the tests and tooling you wrote.

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

For each check, write one line: **done**, **N/A** (with the reason), or **raised** (with what was raised to whom). Raise means stop and ask the owning role (via `AskUserQuestion` when the user holds the role) before building that part. **Raise in the same turn you find it.** A gap found in Pass A goes to the owner before the build starts, folded into any ruling question already being asked; never hold it for the end-of-story report. *(v9.18 ST-39: two detector misses found before the build were raised only after it, so the ruling took three steps and BLG-AI-34 was filed separately.)*

1. **Data source, units and currency.**
   - For every field the story shows, open its contract in `docs/specs/api_contracts/` and confirm the endpoint returns it for the whole list shown.
   - Then trace the number to the code that **writes** it. Note its unit (GBP or native, pence or pounds, 2 dp or 4 dp, UTC or local) before combining it with any other field. The contract may not say.
   - For every **input** the page passes down (a period, a filter, an id), trace it through the API client to the request it actually sends. A parameter the client or endpoint drops silently is a spec question to raise now.
   - *(ST-14: a US signal's `atr_value` is GBP while `current_price` is USD. ST-06: the page period never reached `GET /analytics/compliance-metrics`, found late by a test — BLG-FE-299.)*
2. **Worked examples.** For a value shown on more than one surface, or a rule with a threshold, write the exact text each surface shows for boundary inputs: 0, 1, 2, null, true/false/null, and a value exactly at the threshold.
   - **List every surface that shows the concept, not only the one the story changes**, including the settings page that switches it on and any history or log page. For each surface the story leaves alone, write what it now says in the story's new edge case, and raise any contradiction. *(v9.18 ST-03: "was this alert sent?" lives on Preferences, the Feed and Notification History; only the Feed was fixed — BLG-FE-326, BLG-FE-327.)*
   - **For a small derived-status or classification function, test the full input product,** not each input alone: one table-driven case per combination (e.g. delivered × attempts bucket × error kind × preference × read). *(v9.18 ST-03: `derive_delivery_status` missed read + never-attempted, and first missed read + failed — BLG-SPEC-242.)*
3. **Pure logic.** Check new `src/lib` or helper functions with a quick `node -e` run on null, missing, string, 0 and negative inputs. CI has no frontend unit tests until BLG-QA-262.
   - **A check that withholds or flags generated text must also pass the near misses,** not only fail the bad samples: negations and refusals ("should not be moved", "I cannot suggest whether…"), past-tense or reported wording, and rule-based recommendations. When the story also adds a prompt line telling the model not to do X, test the sentences that line invites: a model told "don't suggest changing stops" will write "the stop should not be changed". **And the reverse: an exemption for near misses must cover only the near-miss phrase itself,** so advice beside a negation or after a disclaimer in the same sentence still fails ("Consider tightening stops since NVDA has not moved.", "I can't advise on trades, but you should tighten your stop."). Test both directions. *(v9.18 ST-39: the §13.2 check withheld "Your stop should not be moved", caught by the high code review; the first exemption then let 14 disclaimer-then-advice sentences through, caught by the PR review.)*
   - **A new guard, lint or check script must fail on a deliberately bad sample of every form it claims to catch,** not only on the old code. For a source scanner that means at least: a multi-line string, a template literal with `${}`, and text containing an apostrophe. State any form it cannot see in its docstring and failure message. *(ST-08: the colour token check passed review but could not see multi-line or template class strings — BLG-QA-267.)*
4. **Test data for layout.** Layout, no-scroll and axe tests use populated fixtures for every panel on the page. Axe checks also fail on `incomplete`.
   - **"Every panel" includes the conditional ones.** For each page in scope, grep its JSX (and its children's) for conditional rendering (`&&`, `? (`, `hidden=`, `open=`, `isOpen`) and list every panel, modal, drawer and widget it can show: a panel shown once a field is filled, a modal opened from the sidebar, an open chat. Give each one a fixture state and a scan, or record why it is out of scope.
   - **When scope is defined per component, check coverage per component, not per route.** Run the story's own scanner over the whole component tree, and for every hit decide: rendered on an in-scope page? Then it is in scope. A route list alone hides components that only appear in a state. *(ST-08: the scope was "any component failing on a routed page", the scans were per route, and six components in unscanned states — What-if sizing, Setup Thesis Digest, AI spend chart, Cash and Daily Monitor modals, Advisor chat — were found only at PR review: BLG-FE-303, P2. DoQ round 1's Trade History calendar view was the same miss.)*
5. **Review depth.** Plan a `/code-review` at **high** when this story creates a module that later stories build on. Otherwise medium.
6. **Collision grep.** When replacing UI, grep `tests/e2e` for the old body copy as well as headings and labels. When a page is renamed, merged or removed, grep the **whole repo** (`src`, `backend`, `tests`, `docs/specs`) for the old route **and** the old label, in every form: `#/Route`, `'/Route'`, `href*="Route"`, `createPageUrl("Route")`, link text and notification or digest copy. *(ST-05/ST-06: a test using `href*=` and the digest's link text kept the retired names — BLG-BE-222.)*
7. **Spec premises.** For every "only X does Y" or "written by X", grep every writer of that field or behaviour. If the premise is false, raise it.
   - **This includes the design record's own descriptions of existing fields**, even ones the story does not change ("the Notified column shows whether a notification was created"). Grep the writer and confirm the description before relying on it. *(v9.18 ST-03: `notification_sent` is set when delivery is queued, not when a notification is created — BLG-FE-327.)*
8. **Time boundaries.** For any date, window or "latest" rule, write examples for:
   - stale data (no event for a week);
   - quiet days and weekends;
   - UTC midnight;
   - the latest row disappearing.

   Raise a missing data source, such as a run date, before choosing an assumption.
   - **An event on the boundary day itself** (an ex-date equal to the entry date, an event at the window's first instant): write what it means, and raise it if the rule's "on or after" wording gives the wrong answer. Do not build to approved wording you have doubts about; raise it in the same turn. *(v9.18 ST-27: "on or after the entry date" flagged a position bought on the ex-date at the post-split price; caught only at code review, ruled the same day.)*
   - **The window between an event and the job that detects it.** List every path that reads the affected data before the detecting job runs (on-load, alert run, risk-off run) and write what each does in that window. *(v9.18 ST-27: detection ran only in the nightly job, so an ex-date page load read the split as a stop breach.)*
11. **Competing user-set values.** When a threshold lives only in code, grep for any user-set value of the same concept and write one example where they disagree. Raise it before choosing wording.
17. **Readers of a new state.** When the story adds a new write or state transition, grep every **reader** of that field. Run the normal case, the partial case and a legacy row (NULL foreign key, pre-migration shape) through each. Fix readers this change breaks; file only what was already wrong.
    - **A change of units or scale** (a split, a currency basis, pence to pounds): list every value-bearing field in each reader's SELECT, **including fields from joined tables** (a trade plan's stop next to a position's entry), and every **stored live field** (current price, previous stop) as well as the entry fields. For each, say which units it is in during **each** state (before, pending, applied) and which writes are paused in between. *(v9.18 ST-27: `current_price` stayed pre-split after confirmation, the reports and lifecycle read pending positions in mixed units, and the grace alert's plan stop was missed — four review findings and BLG-BE-230.)*
    - **Every reader of the same comparison, not only the ones the story names.** When the story fixes or relies on "entry vs live price", grep every place that compares a stored entry with a live price, not only the pattern the story's guard test looks for. *(v9.18 ST-25: the inline-copy regex could not see `GET /positions/{id}/stop-trail`, which used the GBP `entry_price` with no `fill_price` at all — BLG-BE-229.)*
18. **Real-shaped fixtures.** Plan fixtures from the writer's own formula or from a real row:
    - Build the response shape from the code that writes it (the service or router), not from the contract's summary: which object each field sits in, and its nesting. *(ST-06: fixtures put `has_enough_data` and the consistency fields in the wrong objects, which hid two adapter bugs until review.)*
    - Fields derived from each other must agree.
    - A NOT NULL column must not be null.
    - Include one case where the rounding is not exact.
    - **Include a round trip through the column type** when a value is converted on read and converted back on write (e.g. divided then multiplied by a factor and stored as DECIMAL(10,4)). Assert the re-read equals the value the user saw. *(v9.18 ST-27: 20 shares after a 3:1 split were stored as 6.6667 and read back as 20.0001.)*
    - **Check existing fixtures for the endpoint you touch.** If a test you did not write builds the row with the wrong shape (e.g. a native `entry_price` for a US row), the fixture is hiding a bug; fix it with the code. *(v9.18: the v9.15 stop-trail fixture used a native `entry_price` and hid BLG-BE-229 for three releases.)*
19. **Change matrix for derived UI.** For every value the page derives (a pre-fill, a computed line, a deep-link jump):
    - list each input that can change after it is shown (ticker, market, entry, a fetch that arrives late, edit vs new, a user clearing the field);
    - list **every** async source on the page, including child components that start fetching only after they mount, and give each a "arrives late" row **and** a "fails" row;
    - write the expected screen for each.
    *(ST-06/ST-07: the section jump waited for the first request only, and a failed plan load never released it — BLG-FE-302.)*
20. **Copy in edge cases.** Read every new user-facing string in each edge case from 2, 8 and 19, **and every moved or reused string in its new context** (a component placed on a new page, or shown twice). If a literal reading would mislead the user ("tick again" when nothing was ticked; "results changed" when nothing visible changed; "Enter Your First Position" when the user has trades), raise it for a wording ruling. *(ST-06: copy moved from Analytics unchanged — BLG-FE-301.)*
21. **Parity with what the story replaces.** When a story replaces, merges or moves a page or panel, list every state of the **old** one (empty, few rows, below a threshold, loading, error, each period or filter) and write what the **new** one shows in the same state. Raise every difference the spec does not state as intended, before the spec is approved, and list the accepted ones as behaviour changes in the PR. *(ST-06: the new Summary hid Total P&L in quiet months where the old Reports tab showed it — BLG-FE-300, P2.)*

23. **Mechanical sweeps and bulk replacements.** Before applying a scripted rewrite across many files:
    - dry-run it and count repeated output strings; any multi-class string repeated five or more times is a candidate for one shared class, token or component. Raise it with the design owner before the sweep, not after. *(ST-08: the themed card surface was written into ~22 places — BLG-FE-304.)*
    - check both directions of the rule. A sweep that fixes light-theme failures should also flag what fails in the dark theme (for example a bare dark text colour with no `dark:` partner), because axe may not report it. *(ST-08: CalendarView outside-month days stayed dark on dark — BLG-FE-305.)*
    - review every conversion the script cannot see context for (a value supplied by a variable, an inline `style`, a parent element) by hand.

24. **Harnesses, CI installs and AC quantifiers.**
    - **A measurement or test harness serves things the way production does,** or says where it does not: compression (GitHub Pages serves gzip), the Content-Security-Policy, the public path. Check one transfer size or header against production before recording a number. *(v9.18 ST-06: the Lighthouse mock served the 2 MB bundle uncompressed, inflating mobile LCP by ~7 s; found at PR review.)*
    - **Pin every tool CI installs** with a committed lockfile and `npm ci` (or a hashed requirements file). An unpinned `npm install tool@x.y.z` still floats its transitive dependencies. *(v9.18 ST-06: `lighthouse@13.6.0` pulled an `@sentry` version not yet on the registry and the PR run failed.)*
    - **Read quantifiers in an AC literally.** "Each PR", "every page", "all types": no path filter, sample or allowlist may narrow them unless the narrowing is raised and ruled. *(v9.18 ST-06: a `pull_request` path filter narrowed "on each PR" and missed build inputs; DoQ round 1 blocked it.)*
    - **A state or pointer change committed to `main` carries what it points at.** `scripts/check_staged_state_path.py` (pre-commit) now enforces this for `.claude_current_state.json`. *(v9.18 sprint start: `Executing` on `main` without `execution_state.json` failed every PR from `main` — BLG-GOV-430.)*

## Step 3 — Pass B (before commit or review)

9. **Fix, don't file, your own XS gaps.** A gap in this story's own work that takes under an hour gets fixed here, not filed.
   - "Your own work" includes a test, guard or script you wrote for the story (BLG-QA-267), a defect in a file you are already editing that the in-file disclosure rule allows (`execution_prompt.md` §7; a one-class fix such as BLG-FE-305), and a workflow or tool the story relies on (BLG-OPS-220).
   - **Before relying on a workflow to write** (push, comment, deploy), check it can: read its `permissions:` block and run `gh run list --workflow <file>` to see whether that step has ever succeeded. *(ST-08: the visual-baseline workflow's push had no write permission and failed with 403.)*
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
