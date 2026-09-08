**Owner:** QA Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (created — ST-16, v9.2 EPIC-03, BLG-QA-132)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# FI-P3-02 Staging Sign-Off Exception Tracker

## Purpose

`BLG-QA-132`: `CLAUDE.md` §2's `FI-P3-02` exception (a wording-only AC — text content, no visual rendering/colour/layout claim — may substitute code review of the static JSX/text for a staging sign-off or Playwright coverage) is applied per-story with no consolidated tracker of how often it's invoked. Without one, there is no way to notice if the exception starts being over-relied upon — used for an AC that is not genuinely wording-only, or used repeatedly to avoid building real Playwright coverage for a page that keeps changing.

## Backfill scope note

Backfilled by grepping every `claude/cycles/*/qa_evidence_EPIC-*.md` file for the literal string `FI-P3-02` — the exception's own name. A genuine invocation that describes the same substitution (code review standing in for staging/Playwright on a wording-only AC) without citing the rule by name would not be caught by this method and is not claimed to be represented here. This is the same honest-scope-boundary approach used by `docs/ops/pip_audit_trend_log.md` (ST-14, this cycle) — a defensible, disclosed search boundary rather than a claim of exhaustive coverage.

## Log

| Cycle | Story | Type | Description | Result |
|-------|-------|------|--------------|--------|
| `2026-07-02__release-v6.4` | ST-06 (EPIC-02) | **Rule created**, not an invocation | `CLAUDE.md` §2 gained the wording-only-vs-visual AC exception itself (closing `FI-P4-01`/`DF-10`'s sibling finding `FI-P3-02`) — this is the story that introduced the exception, not a use of it. Listed here for completeness so a reader doesn't wonder why the tracker's first genuine use isn't also the exception's first mention in the record. | N/A — governance change, not a sign-off substitution |
| `2026-07-12__release-v7.0` | ST-10 (EPIC-02) | Invocation | `dashboard.md §6` copy matched to `GateProgressStrip.js`'s copy exactly — wording-only, no visual/colour/layout change. QA evidence log cites `FI-P3-02` directly: "Wording-only AC — code review may substitute for staging sign-off per FI-P3-02... Applied — no visual/colour/layout change, code review sufficient." | Applied cleanly; AC genuinely wording-only (a copy-parity check between two already-rendered strings) |
| `2026-08-05__release-v8.3` | ST-08 (EPIC-02) | Invocation | 4 frontend call sites (`TickerUniverse.js`, `Signals.js`, `CustomPriceAlertsSection.js`, `StrategyBenchmark.js`) updated to read a relocated error-response JSON field (`.detail` → `.message`/flattened structure) — same rendered message strings either way, so text/data-source-only. 2 Playwright spec files already exercised these exact paths and were kept in sync in the same commits (so Playwright coverage did exist); the `FI-P3-02` citation specifically covers a **local execution gap**, not an absence of coverage — the sandbox couldn't run `npx playwright install chromium` ("Playwright does not support chromium on ubuntu26.04-x64"), so the code-review data-flow trace substituted for a *locally executed* confirmation, disclosed as an environment limitation rather than a skipped step; CI executed the real spec files on push. | Applied with disclosure; note this instance is a slightly different shape from ST-16's canonical case (Playwright coverage existed and ran in CI — the substitution covered only local pre-push confirmation) |

**No further invocations found** in the remaining `qa_evidence_EPIC-*.md` files carrying the literal string `FI-P3-02` as of this backfill (2026-09-08). The current cycle (`2026-09-07__release-v9.2`) has not invoked it as of this story.

## Reading the log so far

2 genuine invocations across ~30 completed cycles since the exception's creation (`v6.4` → `v9.2`) is a low rate — no sign of over-reliance. Both instances are defensible: one a literal copy-parity check (about as "wording-only" as an AC can be), the other a disclosed environment-limitation substitution where Playwright coverage existed and ran in CI regardless. Neither stretches the exception to cover a genuinely visual/layout/interaction claim.

## Maintenance

Append a new row here whenever a `qa_evidence_EPIC-xx.md` cites `FI-P3-02` — ideally in the same commit that adds the citation, so this tracker doesn't itself require a future re-backfill. If a future invocation looks like it's being used for an AC with any visual/rendering/colour/layout/timing component, flag it to the QA Lead immediately rather than waiting for this log's own periodic review — `CLAUDE.md` §2 already states such an AC is never eligible for this substitution "regardless of how simple the change appears."

## Sign-off

```
QA Lead

Tracker created; backfilled via literal-string grep across all qa_evidence_EPIC-*.md files
for every completed cycle through 2026-09-07__release-v9.2. 2 genuine invocations found
(v7.0/ST-10, v8.3/ST-08) plus 1 rule-origin story correctly excluded from the invocation
count (v6.4/ST-06). Both invocations reviewed and found within the exception's intended
scope — no over-reliance signal. Maintenance convention established for future invocations.

Signed: Sprint Execution Engine (agent-mediated, QA Lead role — §5.3) — 2026-09-08
```
