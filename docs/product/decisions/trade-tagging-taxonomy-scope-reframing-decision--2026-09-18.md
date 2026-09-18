**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-18
**BLG-ID:** BLG-GOV-320
**Story:** ST-35 (this cycle) — records a decision originally made inline by ST-20 (`BLG-SPEC-76`, EPIC-04, `2026-09-09__release-v9.3`)
**Cycle:** 2026-09-15__release-v9.5

---

# Trade Tagging Taxonomy — "No Closed Vocabulary" Scope Reframing Decision

**Decision date (original call):** 2026-09-10 (ST-20, `2026-09-09__release-v9.3`)
**Decision record filed (this story):** 2026-09-18 (ST-35, `BLG-GOV-320`)

---

## Background

ST-20's acceptance criteria read: "canonical allowed-tag taxonomy for `trade_plans.trade_tags` ... documented." A literal reading of "allowed-tag taxonomy" suggests a closed vocabulary — a fixed list of permitted tag strings the system validates against.

ST-20 instead found, and independently verified, that `trade_plans.trade_tags` was never built as a closed taxonomy: it is free-text tagging constrained only by format rules (character set, length, count, deduplication), a deliberate design decision already recorded in the original UX spec (`docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md` §1). No component of the implementation — backend validator, frontend input, or autocomplete source — enforces a closed set of tag names.

ST-20 documented this finding in `docs/specs/trade_tagging_taxonomy.md`'s own Purpose section, but this codebase has an established, separate pattern for exactly this kind of "AC assumed X, accepting Y instead" call: a dedicated `docs/product/decisions/*.md` record, filed alongside the spec change (precedent: `setup-type-other-conflation-decision--2026-08-21.md`). No such record was filed for ST-20 at the time — the reasoning existed only inline in the spec document, not as a standalone, cross-referenced decision. `BLG-GOV-320` (filed from an agent-mediated Product Owner review of PR #1632) tracked closing that gap; this record closes it.

## Decision

**Accept the reframing.** ST-20's AC is satisfied by documenting the taxonomy *as it actually exists* — a format-constrained free-text namespace — rather than inventing a fixed tag vocabulary that was never part of the system's design. No new enum, no closed value list, no schema or validation change.

## Rationale

1. **The closed-taxonomy reading was never how the feature was built.** The original UX spec's tag examples ("breakout", "earnings-play") were always illustrative, not an exhaustive canonical list — confirmed by re-reading `ux_spec.md` §1 directly, not inferred.
2. **No implementation component enforces a closed set.** ST-20's own review confirmed the backend validator (`_TAG_PATTERN`, `_TAG_MAX_LENGTH`, `_TAG_MAX_COUNT`) and the frontend's independently-declared constants match exactly, and both are format constraints, not a vocabulary allowlist.
3. **Inventing a closed taxonomy now would be a larger, out-of-scope design change.** It would affect the UX, every existing user-entered tag, and the autocomplete/reporting model (`GET /analytics/tag-performance`) — well beyond an `S`-effort documentation story's scope, and not something this decision reopens.
4. **This is a scope-reframing, not a deviation.** ST-20's literal AC wording could not be met once the closed-taxonomy premise was found to be false — documenting the taxonomy as it genuinely exists, with the "intentionally open, not closed" finding stated explicitly (`trade_tagging_taxonomy.md` §"The Taxonomy Is Intentionally Open, Not a Closed Value List"), is the correct and only accurate resolution.

## Spec cross-referenced

`docs/specs/trade_tagging_taxonomy.md` §"The Taxonomy Is Intentionally Open, Not a Closed Value List" now links back to this decision record.

## Sign-off

**Product Owner:** Approved — 2026-09-18 (agent-mediated, §5.3). The reframing is the only accurate outcome once the closed-taxonomy premise is checked against the actual implementation; ratifying it formally, with a cross-referenced record matching this codebase's own established precedent, closes `BLG-GOV-320` without reopening ST-20's already-shipped spec work.
