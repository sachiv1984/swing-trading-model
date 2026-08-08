**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-08
**Source:** ST-30 (BLG-GOV-212, EPIC-07, v8.4)

---

# Cross-EPIC Merge Conflict Runbook — Dry Run

## 1. Purpose

ST-30's AC calls for dry-running `CLAUDE.md` §8 (Cross-EPIC Merge Conflict Resolution) against one sprint with genuinely parallel EPIC branches, and filing any gaps found as follow-ups. This cycle (`2026-08-07__release-v8.4`) has 7 EPIC branches executing in parallel — a live instance to dry-run against.

## 2. Method

`main` had already absorbed EPIC-01/02/03/04 (all merged earlier this cycle). EPIC-05 and EPIC-06 were both still open, in-progress branches, each having independently appended new entries to the two files every EPIC branch in this cycle writes to: `execution_state.json` and `execution_escalations.md`. Rather than wait for both to reach `done` and go through their own PR/merge-gate sequence (which this sprint's remaining live blockers on both EPICs prevent within this session), a direct test merge was run between the two sibling branches to observe conflict shape early:

```
git checkout exec/2026-08-07__release-v8.4/EPIC-06
git merge exec/2026-08-07__release-v8.4/EPIC-05 --no-commit --no-ff
```

This is not the exact production sequence (real cross-EPIC merges happen one-at-a-time via `main`, per the "Merge order note" in `execution_prompt.md` §4 — a later branch runs `git merge main` after an earlier sibling's PR lands, not sibling-into-sibling), but it produces the same conflict *shape*, since neither branch's shared-file changes were yet on `main` at test time. The merge was aborted (`git merge --abort`) immediately after inspection — no commit was made, no branch state changed.

## 3. Result: Runbook followed, with 2 gaps found

**Conflict occurred exactly where §8 anticipates:** `execution_state.json` (3 hunks) and `execution_escalations.md` (1 hunk) — the two shared files §8 names explicitly. `CLAUDE.md` §8 step 3's resolution rules were applied to reason through each hunk (not committed, since this was a dry run):

| File | Hunk | §8 rule applied | Outcome |
|------|------|-----------------|---------|
| `execution_escalations.md` | Both branches appended new `## ESC-EXEC-*` entries after the same base entry | Append-only union — keep both branches' new entries, in ID order | Resolves cleanly: `shared_standards.md` §7.1's append-only convention means both additions are independent inserts, not competing edits to the same text |
| `execution_state.json` | `last_updated_utc` differs | Not covered by §8 explicitly | Take the later timestamp — no ambiguity, but §8 doesn't name this field |
| `execution_state.json` | `blocked_items` — EPIC-06 branch listed only `["ST-28"]`, EPIC-05 branch listed only `["ST-19","ST-20","ST-21","ST-23"]` | §8 step 3 says "take the branch's (not main's) blocked/delegated lists" | **Gap 1 (below)** — rule is written for a branch-vs-`main` merge and doesn't resolve a sibling-vs-sibling case where neither side is `main` |
| `execution_state.json` | `open_escalations` — EPIC-06 branch: `list` of strings; EPIC-05 branch: `dict` of `{ESC-ID: status}` | Not covered by §8 | **Gap 2 (below)** — a schema-shape divergence, not a content conflict |

### Gap 1 — §8's "take the branch's blocked/delegated lists" rule doesn't name the sibling-vs-sibling case

`CLAUDE.md` §8 step 3's `execution_state.json` row reads: *"take the branch's (not main's) blocked/delegated lists as those reflect the more current state."* This phrasing assumes a two-party merge (one EPIC branch vs. `main`) where `main` is the stale side. It does not say what to do when **both** sides are EPIC branches that independently diverged from a common ancestor and both added genuinely new blocked items — as observed here, where the correct resolution is neither "take HEAD's list" nor "take the incoming branch's list" but the **union of both**. Filed as `BLG-GOV-289` (below) to make the union rule explicit for this case, consistent with how the same section already specifies union behavior for `completed_items`.

### Gap 2 — no rule for a shared JSON field's schema shape drifting mid-sprint between sibling branches

`open_escalations` was reshaped from `list` to `dict` on the EPIC-05 branch mid-session (to support per-escalation status lookups) without a corresponding update on EPIC-06, which had already branched from the pre-reshape `main`. `CLAUDE.md` §8 has no guidance for this class of conflict (a type/shape mismatch, not a value mismatch) — `git merge` reports it as an ordinary content conflict, but resolving it requires picking (or reconciling) a schema, not just picking values. Filed as `BLG-GOV-290` (below).

## 4. Follow-ups filed

- `BLG-GOV-289` — Add an explicit union rule to `CLAUDE.md` §8 for `execution_state.json` array fields (`blocked_items`, `delegated_items`) when the conflict is sibling-branch-vs-sibling-branch rather than branch-vs-`main`.
- `BLG-GOV-290` — Add a rule to `CLAUDE.md` §8 (or `shared_standards.md` §16.13's `execution_state.json` schema note) requiring any mid-sprint schema-shape change to a shared JSON field (e.g. `open_escalations` list→dict) to be applied uniformly across all sibling EPIC branches active that sprint, not just the branch making the change — or, alternatively, prohibiting shape changes to already-initialised shared fields mid-sprint entirely, deferring the shape change to the next cycle's STEP 0.

Both filed as new backlog items with `**Source:** ST-30 (EPIC-07), 2026-08-08` per `execution_prompt.md` §7's backlog write-scope exception.

## 5. Conclusion

The runbook's core mechanism (append-only-file union, `execution_state.json` story-status precedence) held up correctly under a real dry run. The two gaps found are both about fields the runbook's current text doesn't fully specify for a sibling-vs-sibling scenario — narrower than "the runbook doesn't work," and consistent with the AC's framing that gaps found should be filed as follow-ups rather than blocking this story.
