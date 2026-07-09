**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-08
**Approved by:** Product Owner — 2026-07-08
**Story:** ST-05 (BLG-FEAT-52) — Trade tagging and tag-based performance filtering
**Cycle:** 2026-07-08__release-v6.8

---

# UX Specification — Trade Tagging and Tag-Based Performance Filtering

## 1. Scope Decision

Descoped (2026-07-08 rebalance) to tags-only: no dependency on `trade_annotations`/PO-02. Tags are a **new, independent field on `trade_plans`** (`trade_tags`) — not a re-use of the existing position/trade tags already documented in `journal_components.md` (`GET /positions/tags`), which apply to journal entries on positions, not trade plans. The two tag systems are visually consistent (same component) but data-independent.

**Rationale:** Trade plans are created pre-trade and persist independent of position lifecycle; tagging the plan (e.g. "breakout", "earnings-play") lets a user classify a setup at the point of decision, before a position or journal entry exists. Reusing the existing Tag Editor / Tag List components (`journal_components.md` §4, §1) gives visual consistency with zero new component design.

## 2. Placement

**Page:** Trade Plan Detail View (`/trade-plans/{id}`) and Edit Form (`/trade-plans/{id}/edit`) — `docs/specs/frontend/pages/trade_plan.md` §5 and §7.

**Position:** New "Tags" row directly below the core plan fields (ticker, stop, R-target) and above the Pre-Trade Checklist (§6) in both the edit form and the read-only detail view. Does not displace Setup Quality Score (§7a) or Signal Context Panel (§5a).

**Component reuse:**
- Edit form: Tag Editor (Autocomplete Input) — `journal_components.md` §4, unchanged behaviour (Enter to add, click X to remove, lowercase/hyphen validation, max 20 chars, dedup, tag limit)
- Detail view (read-only): Tag List display — `journal_components.md` §1-equivalent pill rendering, no edit affordance
- Autocomplete source: new `GET /trade-plans/tags` endpoint (mirrors existing `GET /positions/tags` shape)

## 3. PerformanceAnalytics Page — Tag Filter Controls

**Page:** `docs/specs/frontend/pages/analytics.md` §14 "Performance by Strategy Tag"

**Decision:** Add a tag filter control directly above the existing §14 table, rather than a new section. The existing table (source: `trades_for_charts` tag field, i.e. position/journal tags) is unaffected. The new filter is a **separate, additional row** beneath the §14 heading:

> "Filter by trade plan tag" — multi-select dropdown, same interaction pattern as the Positions page tag filter (`positions.md` — Tag filter: dismissible pills below the dropdown, OR logic across selected tags).

Selecting one or more trade-plan tags re-fetches `GET /analytics/tag-performance?tags={csv}` and renders win rate + average R **per selected tag** as a small comparison row above the existing table (existing table content/behaviour unchanged). When no tags selected: comparison row hidden, existing table displays as today.

**No new page section, no new nav item.** Consistent with prior "extend existing section rather than fragment the page" precedent (analytics.md v1.9 changelog, Behavioural Drift integration decision).

## 4. Data Source

New endpoint: `GET /analytics/tag-performance?tags={csv}` → per requested tag: `{tag, win_rate, avg_r_multiple, trade_count}`. Confirmed at design gate: no dependency on `trade_annotations`/PO-02 structures (per ST-05 AC-04) — reads only `trade_plans.trade_tags` and existing closed-trade linkage.

## 5. States

| State | Behaviour |
|-------|-----------|
| No tags on plan | Detail view: "No tags" muted placeholder. Edit form: empty Tag Editor, ready for input |
| No tags selected (Analytics filter) | Comparison row hidden; existing §14 table unaffected |
| Tags selected, no matching trades | Comparison row shows "No closed trades for selected tag(s)" per tag |
| Loading | Comparison row: inline skeleton |
| Error | Comparison row hidden silently; does not block §14 table or page |

## 6. §13 Compliance

Display-only. No automated action taken on tag values. No advisory or recommendation content.

## 7. Playwright Coverage Required

Per CLAUDE.md frontend-visible-change rule (ST-05 AC-05): tag add/remove on trade plan edit form, and tag filter control + comparison row on PerformanceAnalytics page.
