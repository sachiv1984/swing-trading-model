**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-07 (created — v9.1 ST-33, BLG-GOV-274)

---

# Specs_Index.md Automated Freshness Check

## Purpose

BLG-GOV-274: `Specs_Index.md`'s maintenance previously lapsed silently for 5 consecutive cycles before being caught manually (`2026-07-21__release-v7.7` closure Carry-Forward Item 3). This adds an automated, re-runnable check comparing `Specs_Index.md`'s tracked references against the live `docs/specs/` tree.

## The Check

`scripts/check_specs_index_freshness.py` — compares every `.md` file under `docs/specs/` against every spec-file reference (full path or bare filename) found anywhere in `Specs_Index.md`, reporting:
- **ADDITIONS:** live files with no reference anywhere in the index.
- **REMOVALS:** index references with no matching live file anywhere in `docs/specs/` — and, to avoid false positives, also checked against the whole repo, since `Specs_Index.md` legitimately cross-references many canonical files that live outside `docs/specs/` (e.g. `claude/strategy/strategy_rules.md`, `claude/backlog/backlog.md`) by bare filename.

Run: `python3 scripts/check_specs_index_freshness.py`. Exit code 0 = clean, 1 = findings present (detection only — no CI gate wired up by this story, consistent with the `S`-effort AC of "check added," not "check enforced").

## First Run Results (2026-09-07)

**Removals: 0.** After filtering for whole-repo cross-references (an earlier draft of this check without that filter produced 29 apparent "removals," all of which turned out to be correctly-scoped cross-references to non-`docs/specs/` files, not actual staleness — see the script's own comments for this false-positive class).

**Additions: 78.** A substantial, genuine gap — including nearly every `docs/specs/frontend/pages/*.md` file (spot-checked `positions.md`: zero mentions anywhere in `Specs_Index.md`, confirmed via direct grep, not a script artefact). `Specs_Index.md`'s §3 "Canonical Spec Domains" section registers domain-level ownership (Strategy, Data Model, Metrics, API Contracts) but was never extended into a full per-file page/component registry — this looks like a structural gap in the index's own design, not merely staleness from a lapsed update cycle. Full list of all 78 files: see the script's own output (re-run it; not duplicated here to avoid a second copy that itself goes stale).

## Disposition

**This story's own scope is the check, not the fix.** Populating 78 missing entries into `Specs_Index.md` is a substantially larger effort than this `S`-sized story budgets for, and is itself a judgement call for Head of Specs Team (which of the 78 genuinely need a dedicated index entry vs. which are adequately covered by the existing domain-level registration). Filed as `BLG-SPEC-135` (P3) — see backlog.md — recommending the index-population work as its own future story, with this check's script as the tool to verify completion.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3)
- Date: 2026-09-07
- Comments: Check built, run, and produces a real, verified (not merely plausible) result — spot-checked one finding (`positions.md`) directly rather than trusting the script's own output uncritically. An earlier draft's false-positive class (29 apparent removals) was caught and fixed before finalising, not left in the shipped tool. Satisfies BLG-GOV-274's AC (check added; Head of Specs Team sign-off) — the substantial population gap found is correctly scoped to a follow-up item, not force-fit into this story.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-07 | Initial creation — v9.1 ST-33, BLG-GOV-274. |
