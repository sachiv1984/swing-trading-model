**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-21

# Roadmap Management Run Log — 2026-08-21

Invoked as STEP 11 of `post_ship_closure.md`, cycle `2026-08-17__release-v8.9`.

## Summary

Items retired: 0
Items flagged stale: 0
Items kept active: 0
Ambiguous items resolved: 0
RA: markers pruned: 53   # ST-22, BLG-GOV-260, v8.9 — first live run of the stale-RA-marker pruning rule

## Retired Items

None. `§3. Delivery Plan — Horizon: Now` has been empty since 2026-07-27 (`2026-07-24__release-v7.8` post-ship closure), and `v8.9` — like `v8.5`–`v8.8` before it — shipped fully backlog-driven with no formal per-item `## vX.Y` roadmap section (Option (b) equivalence from `2026-08-11__scheduled`, per `current_roadmap.md §1`'s own execution notes). No item in `§4 Priority 2`, `§5 Priority 3`, or `§6 Gated Features` reached a new Complete/Killed classification this cycle.

## Stale Items Flagged

None. No item in the Now-horizon or Priority-2/3 sections showed cycle-activity staleness this run (the Now horizon has no items to be stale; Priority 2/3 Arc-detail tables record historical shipping status, not open initiatives requiring staleness review).

## Ambiguous Items

None.

## RA: Marker Pruning (ST-22, BLG-GOV-260, v8.9 — first run)

Scanned the entire `current_roadmap.md` document for already-retired `*RA:vX.Y retired — see roadmap_archive.md ...*` one-line pointers with a numeric `vX.Y` identifier. Current highest referenced release: `v8.9` (`§1 Current Version`).

For each numeric marker found, computed the count of shipped release versions strictly between it and `v8.9` (inclusive of `v8.9`, exclusive of the marker's own version), using the full de-duplicated, version-sorted list of `✅ Shipped`/`✅ Complete` rows in `§8 Release Summary` (77 unique shipped versions). All 53 numeric `RA:` pointer lines found — ranging from `RA:v7.7` (13 releases behind) to `RA:v2.9`/`RA:v3.0` (60/59 releases behind) — exceeded the >3-releases-older threshold and were pruned (line deleted outright, not just content). This is expected for a rule's first live invocation against a document that had accumulated retirement pointers, uncapped, since `v2.9` (2026-04-24) with no prior forcing function.

Non-numeric marker `*RA:Gated-carry-forward-2026-07-27 retired...*` (§3) — left untouched per the rule's own scope restriction (no numeric `vX.Y` identifier, no defined "how many releases older" computation).

Still-active `<!-- roadmap-annotation-marker: RA:v7.4:2026-07-17__release-v7.4 -->` (§3) — left untouched; the pruning rule applies only to already-retired one-line pointers, never to an active marker block, regardless of age.

Post-prune cosmetic cleanup: collapsed resulting 3+ consecutive blank lines to 2 (whitespace only, no content change) and removed one duplicated `-----` section-separator line left adjacent by the removal of the markers previously sitting between two separators (§3, Now-horizon block) — both are formatting-only corrections, not scope/content changes, and fall within STEP 5.2's own "no other content change" constraint (which governs item content, not incidental whitespace/separator artefacts of a line-deletion operation).

No content beyond the 53 pruned lines and their immediate whitespace/separator artefacts was touched.

## Write Scope Verification

- All writes within Section 5 scope: Yes (`current_roadmap.md` only this run — no `roadmap_archive.md` append, no `initiative_register.md` change, since 0 items were retired)
- No content changes beyond status and location: Yes (RA: marker pruning is explicitly authorised by STEP 5.2, ST-22/BLG-GOV-260, v8.9)
- No backlog modifications: Yes
