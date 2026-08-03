Owner: Head of Engineering
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03
Cycle: 2026-08-03__release-v8.1 (ST-06, EPIC-03, BLG-GOV-273)

# Technical Debt Registry (Consolidated Cross-Cycle View)

## Purpose

`claude/backlog/backlog.md` files technical debt items across three separate category sections — Frontend & UX (§3), Backend & Data (§4), and Operations & Infrastructure (§6) — alongside unrelated feature and process work in the same sections. There was no single view answering "what technical debt do we currently carry, across all three engineering categories, in one place." This registry is that view. It is a **derived index**, not a new backlog namespace — every row here is a live item that still lives (and is still updated) at its home location in `backlog.md`.

**Scope note:** Spec debt (`BLG-SPEC-D*`) already has its own dedicated backlog section (§7) and lifecycle (`shared_standards.md` §15) — it is intentionally **not** duplicated into this registry, which covers only `BLG-BE-*`, `BLG-FE-*`, and `BLG-OPS-*` items.

## Inclusion Rule

An item qualifies for this registry when its `backlog.md` **Type** field literally contains `Tech Debt` or `Technical Debt` (case-insensitive), and its category prefix is `BLG-BE-*`, `BLG-FE-*`, or `BLG-OPS-*`. This is a mechanical, re-derivable rule — the same scan can be re-run at any `groom backlog` cycle (`grep -B1 "Type:.*[Tt]ech(nical)? Debt" claude/backlog/backlog.md`, filtered to non-Spec-Debt category prefixes) to keep this file current, rather than relying on manual curation drifting out of sync.

**Full-file scan performed 2026-08-03:** 2 items currently qualify. (A broader keyword scan for the word "debt" anywhere in item prose returned several additional false positives — items that merely *discuss* avoiding future debt, e.g. `BLG-BE-28`/`BLG-BE-30`/`BLG-BE-31`/`BLG-OPS-48` pre-design items — these are not themselves debt items and are excluded.)

## Registry

| ID | Title | Priority | Owner | Effort | Provisional-Target | Category |
|----|-------|----------|-------|--------|---------------------|----------|
| [BLG-FE-98](backlog.md#blg-fe-98) | WatchlistModal.js fails ESLint (24 problems) — same patterns fixed in Watchlist.js | P3 (Low) | Head of Engineering | M (~1 day) | v6.9 | Frontend |
| [BLG-OPS-116](backlog.md#blg-ops-116) | Quarterly dependency-upgrade cadence for backend/requirements.txt | P2 (Medium) | Head of Engineering | S | TBD | Operations |

*(Note: `Provisional-Target: v6.9` on `BLG-FE-98` is stale relative to the current cycle — the item has not shipped since that target was set. This registry surfaces the staleness; retargeting or re-prioritising it is a `groom backlog` / release-planning decision, not made here.)*

## Maintenance

- Re-run the inclusion-rule scan at each `groom backlog` invocation (or at minimum, each release planning cycle) and update the table above.
- When a registry item ships or is archived, remove its row here in the same commit that archives it in `backlog.md` (mirrors the existing archive-sync discipline for other backlog views).
- When a new `BLG-BE-*`/`BLG-FE-*`/`BLG-OPS-*` item is filed with a Type containing "Tech Debt"/"Technical Debt" (via `/backlog-add`), add it here in the same session.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3)
- Date: 2026-08-03
- Comments: Registry scope, inclusion rule, and initial 2-item population reviewed against Head of Engineering's ownership of both qualifying items. Rule is intentionally narrow (literal Type-field match) to keep the registry mechanically re-derivable rather than a one-time manual snapshot that drifts stale.
