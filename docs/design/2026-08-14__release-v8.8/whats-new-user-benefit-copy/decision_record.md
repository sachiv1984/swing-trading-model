**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-08-14__release-v8.8
**Story:** ST-13 (EPIC-03, BLG-FE-161)

# Decision Record — What's New Panel: User-Benefit Copy Source

## 1. Problem

`WhatsNewCard` (`dashboard.md` §6A, shipped v7.8) renders the `Description` column of `changelog.md`'s most recent `### Changes shipped` table verbatim. That column is authored as a per-EPIC engineering summary ("N+1 query audit across trade/position list endpoints") — accurate for governance record-keeping, wrong register for an end user scanning what changed for them. Every EPIC row appears in the feed even when its content is pure backend/governance work with no user-facing effect (e.g. v8.7's EPIC-02, EPIC-06 rows).

## 2. Decision

Add a second, independent column to the `### Changes shipped` table: **`User Impact`** — curated, present-tense, user-benefit copy, one to two sentences, written from the user's point of view ("Trade plan drafts now capture your invalidation conditions at entry, not just at review time"). `Description` is retained unchanged as the engineering record; `User Impact` is new and additive, not a replacement.

**Sourcing rule for `GET /changelog/latest`:** parse `User Impact`, not `Description`. Rows with an empty/`—` `User Impact` cell are excluded entirely from the parsed feed — this is the mechanism satisfying "an EPIC with no user-facing change does not appear in the What's New feed." A row is included only when its author has deliberately written user-facing copy for it.

**Authoring convention (documented for whoever writes `changelog.md` at post-ship closure, per this story's third AC):** write `User Impact` only for EPICs that changed something a user can see, click, or notice the effect of. Leave it blank (`—`) for backend/infra/governance/test-coverage rows. Write in second person or implied second person, present tense, no ticket IDs, no implementation nouns (endpoint names, table names, component file names).

### Component impact

None. `WhatsNewCard.js` itself is unchanged — same bullet-list rendering, same `DataState` states, same 8-bullet cap with "+N more" trailer (`dashboard.md` §6A, unchanged). This is a data-source change only: the backend endpoint now reads a different column and applies a non-empty filter before returning rows.

## 3. Constraints Checked

- Does not contradict `strategy_rules.md` §13 — display-only content, no AI-generated or automated recommendation involved.
- No AI-provider call introduced or extended — not subject to the §13 boundary pre-check.

## 4. Follow-up (outside this gate's write scope)

- `docs/product/changelog.md`'s table header and its own authoring convention note need the `User Impact` column added — implementation-time change, not made by this gate (write scope restriction, `design_gate_prompt.md` §5).
- `GET /changelog/latest`'s parsing logic needs to switch source column and add the empty-cell filter — implementation detail for Sprint Execution.
