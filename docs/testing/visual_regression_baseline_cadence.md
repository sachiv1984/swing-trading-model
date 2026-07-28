Owner: Head of UX & Design; Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27
Source: ST-15 (BLG-QA-123, EPIC-15, v7.9)

# Visual-Regression Baseline Refresh Cadence

## Purpose

`playwright.config.js` already wires a Playwright snapshot pipeline (`snapshotDir: 'tests/e2e/__snapshots__/'`, refreshed via `npx playwright test tests/e2e/visual-snapshots.spec.js --update-snapshots`), and `BLG-QA-81` proposed capturing initial pixel baselines for the contrast-sensitive components remediated in v6.6/v6.7. No cadence exists for refreshing baselines as components evolve — without one, baselines either drift silently (never refreshed, so real changes get rubber-stamped) or block every legitimate visual change (refreshed reflexively, so real regressions get rubber-stamped too). This document defines that cadence.

## Dependency status (finding, recorded here — see note below)

**`BLG-QA-81` has not actually shipped baselines yet.** Verified at the time of writing:
- `claude/backlog/backlog.md` still lists `BLG-QA-81` as open, `Provisional-Target: Unscheduled`, `Gate criteria: None`.
- No `tests/e2e/__snapshots__/` directory exists in the repository.
- `tests/e2e/visual-snapshots.spec.js` (the file `playwright.config.js` names as the baseline source) is CSS-class/attribute assertion based, not pixel-snapshot based — its own header states it was "Originally pixel-snapshot based; converted to CSS assertions to ensure reliable cross-platform CI." No pixel baselines exist anywhere in the test suite today.

This cadence policy is therefore **defined now but dormant** — it takes effect once `BLG-QA-81` (or an equivalent pixel-baseline-capture story) actually lands. Documenting the cadence ahead of the baselines existing is still useful: it gives whoever picks up `BLG-QA-81` a ready-made refresh policy to adopt immediately, rather than having to define one retroactively once baselines already exist and have started drifting. `claude/backlog/backlog.md` is outside this routine's write scope, so `BLG-QA-81`'s own entry is not updated here — flagging for the next backlog grooming pass to cross-reference this document from `BLG-QA-81`'s scope.

## Cadence

Grid View visual-regression baselines (once established per `BLG-QA-81`) are refreshed on either trigger, whichever comes first:

1. **Every 3rd release** that ships a Grid View change — matches this repo's existing "3-cycle" cadence convention already used elsewhere (e.g. the Skill-Silo Alert rolling-3-cycle average in `roadmap_prompt.md`), so contributors already have a mental model for this window size.
2. **Any release where a Grid View component passes through the Design Gate** (`design_gate_status: Passed` with a Grid View–touching spec change) — a passed design gate is direct evidence the component's approved visual state changed, so the baseline should refresh immediately rather than waiting for the periodic trigger to catch up.

Whichever trigger fires first resets the 3-release counter for trigger (1).

## Refresh procedure

1. Confirm the pending Grid View change has passed Design Gate (if applicable) or code review (if a non-visual-intent change incidentally touched Grid View markup).
2. Run `npx playwright test tests/e2e/visual-snapshots.spec.js --update-snapshots` locally against the updated build.
3. Review the diff of updated PNGs manually before committing — an automatic refresh must never be committed unreviewed, since that would silently accept a real regression as the new baseline. This review must be performed by the PR reviewer, not the author of the change that triggered the refresh — the person who ran `--update-snapshots` is not an independent check on their own diff.
4. Commit the updated baseline files in the same PR as the triggering change, not a follow-up PR — an unreviewed baseline gap between the change landing and the baseline refreshing is itself a drift window.

## Non-goals

This cadence governs Grid View only, matching `BLG-QA-123`'s scope. Extending pixel-baseline coverage to other contrast-sensitive components (the original `BLG-QA-81` scope) or to other page layouts is a separate decision, not implied by this document.
