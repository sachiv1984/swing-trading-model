**Owner:** Base44 Frontend Prompt Owner
**Class:** Class 3 — Operational Record
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-10
**Source:** ST-24 (BLG-GOV-180, EPIC-05, v9.3 sprint execution)

---

# Base44 Prompt Versioning Changelog

## Purpose

ST-24's problem statement: "Base44 frontend scaffold prompts change over time with no changelog — regressions from a prompt change are hard to trace." This document is the single discoverable entry point for that history.

**Finding, before writing a word of new history:** this problem was already substantially solved, twice over, by work this repo did not connect back to `BLG-GOV-180` at the time:

1. `claude/agents/base44_frontend_prompt_owner.md` §3 ("The Base44 Prompt Standard" — the required section structure every Base44 prompt must follow) already carries its own `## Changelog` table, versioned v1.0 through v1.3, fully backfilled to its origin (no "— Initial canonical version" gap).
2. `docs/specs/frontend/base44_prompt_template_library.md` (pre-approved reusable prompt-section fragments for recurring UI patterns) already carries its own `## Change Log` table, versioned v1.0 through v1.8, likewise fully backfilled to its origin.

Both are real, currently-maintained, already-accurate changelogs — not stale or abandoned. **This document does not replace or duplicate either.** What was actually missing was a single place naming both and explaining which one governs which kind of prompt change, since "the Base44 prompt" is really two related-but-distinct artefacts and a reader chasing "what changed in the Base44 prompt" has no way to know there are two changelogs to check without already knowing this document structure exists.

## The Two Artefacts

| Artefact | What it versions | Changelog location |
|----------|-------------------|---------------------|
| **The Base44 Prompt Standard** | The *required section structure* every individual Base44 prompt must follow (Context, Change, API Contract, Behaviour Rules, Non-Functional Rules, Expected Outcome — per `execution_prompt.md` §5.1) — the format, not any one prompt's content. | `claude/agents/base44_frontend_prompt_owner.md` §3, own `## Changelog` table (currently v1.3) |
| **The Base44 Prompt Template Library** | Pre-approved, reusable section *fragments* for recurring UI patterns (empty states, skeletons, modals, etc.) that a prompt draft can cite instead of re-deriving from scratch, plus process conventions layered on top (§16 provenance tags, §17 regeneration diff checklist). | `docs/specs/frontend/base44_prompt_template_library.md`, own `## Change Log` table (currently v1.8) |

Neither document tracks the version history of any *individual, per-feature* Base44 prompt draft (e.g. the ones delegated and executed for a specific story) — those live in each cycle's `delegation_log.md` and are not the "scaffold" this changelog is about.

## Most Recent Known Prompt Change (backfilled, per this story's own AC)

The most recent change to either governing artefact, at the time of this entry:

**2026-09-08 — Base44 Prompt Template Library v1.8** (`base44_prompt_template_library.md`'s own Change Log): added §16 Prompt-Version Provenance Tag convention (every Base44-generated file must carry a `// Base44-generated — template_library vX.Y §N (<template>) — <date>` provenance comment) and §17 Regeneration Diff Checklist — a design-token compliance pass to run against the diff whenever a Base44 component is regenerated (`ST-45`/`BLG-SPEC-121`, `ST-46`/`BLG-SPEC-122`, EPIC-05, v9.2).

The Base44 Prompt Standard's own most recent change (`base44_frontend_prompt_owner.md` §3) is earlier — v1.3, 2026-07-02: added a Playwright strict-mode advisory requiring a unique `data-testid` when a generated element could match more than one locator.

## Going Forward

A change to the prompt *format/structure* is recorded in `base44_frontend_prompt_owner.md` §3's own Changelog. A change to the *reusable template fragments or generation-time/regeneration-time process conventions* is recorded in `base44_prompt_template_library.md`'s own Change Log. This document is not itself a third place to record entries — it is updated only when the *set* of governing artefacts changes (e.g. if a third prompt-related document is introduced), not on every individual version bump of the two above.

## Acceptance

- Created by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — a documentation/index deliverable, no observable UI behaviour)
- Date: 2026-09-10
