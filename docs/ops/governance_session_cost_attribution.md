**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-15 (ST-19, EPIC-05, v9.4, BLG-GOV-302: initial version)

---

# Governance-Overhead vs. Delivery Session Cost Attribution

**Added:** ST-19 (EPIC-05, v9.4, BLG-GOV-302)

## 1. Problem

Governance overhead (idea intake, roadmap rebalance, release planning, design gate, delivery verification, post-ship closure) consumes Claude Code session compute — the same resource delivery work (sprint execution) consumes — but nothing distinguishes the two, making it hard to assess the true cost-of-governance ratio for this system.

## 2. Why a Proxy Metric, Not a Direct One

No per-session token/dollar cost is logged anywhere in this repository — Claude Code sessions are not billed or metered in-repo, and no cycle artefact records session token counts. A "lightweight" attribution method (this story's own AC framing, and its S/0.5-day effort estimate) therefore cannot be a true cost ledger. Instead, this document defines a **git-history-derived proxy**: commit volume and line-change volume, classified by which governed routine produced each commit. This is measurable today, from data every cycle already produces (commit messages, per CLAUDE.md §2's non-negotiable format), with no new instrumentation.

This is an explicit trade-off: commit/line-count is not the same as compute cost (a short commit can follow a very long deliberation; a large mechanical file move can inflate line-count without much actual reasoning cost). It is offered as the best available proxy given no real cost data exists, not as a precise cost figure.

## 3. Method

For a given cycle's commit window on `main` (from its `plan release`/`run roadmap` kickoff commit to its `post-ship closure` commit — or, for an in-progress cycle, up to the present):

1. Run `git log main --since=<cycle_start> --until=<cycle_end> --pretty=format:"%s" --shortstat` (or an exact `--since`/`--until` pair bounding the cycle).
2. Classify each commit by its message prefix, per CLAUDE.md §2's commit format:
   - `[GOVERNANCE] ...` → **governance-overhead** (idea intake, roadmap rebalance, release planning, design gate, sprint planning seal, delivery verification, post-ship closure, and any other non-delivery governed routine — these all use the `[GOVERNANCE]` prefix per CLAUDE.md §2).
   - `[EPIC-xx] ...` with or without an `[ST-xx]` tag, provided it does not carry the `[GOVERNANCE]` prefix → **delivery** (sprint execution work against a specific story, or delivery-branch housekeeping such as a merge-gate state sync or an orphaned-commit reconciliation — CLAUDE.md §8 — that legitimately has no single ST to tag).
   - `Merge pull request ...` → structural, zero-diff-of-its-own (the merge commit itself carries no line changes on a fast-forward-eligible history; excluded from the ratio rather than mis-attributed to either side).
3. Sum commit count and `insertions`/`deletions` (from `--shortstat`) per category.
4. Report the ratio. A rising governance-overhead share over successive cycles is exactly the signal the existing **Product Value Ratio** metric (`.claude_current_state.json.last_rebalance_pvr` — currently `0.092`, 2nd consecutive Alert-tier reading per the 2026-09-14 scheduled rebalance) already tracks from the opposite direction (U/G/D/P item counts rather than commit volume) — this document's ratio is a second, independent proxy for the same underlying concern, not a replacement for it.

## 4. Applied Retrospectively: Cycle `2026-09-09__release-v9.3`

Chosen because it is the most recently **fully closed** cycle at the time of writing (post-ship closure complete, `closure_status: Closed_with_actions`) — a complete, stable dataset, unlike the still-`Executing` `2026-09-14__release-v9.4`.

Window: `2026-09-07T00:00:00` to `2026-09-09T23:59:59` (cycle kickoff through sprint close), `git log main`.

| Category | Commits | Insertions | Deletions |
|----------|--------:|-----------:|----------:|
| Governance-overhead (`[GOVERNANCE]`) | 39 | 9,894 | 2,071 |
| Delivery (`[EPIC-xx][ST-xx]`) | 66 | 8,671 | 1,401 |
| Merge commits (excluded from ratio) | 9 | 0 | 0 |

**Governance-overhead share of commits:** 39 / (39+66) = **37%**.
**Governance-overhead share of line changes:** 9,894 / (9,894+8,671) = **53%** of insertions.

**Reading this:** by commit count, delivery work outnumbers governance-overhead commits roughly 5:3. By line volume, governance-overhead edged out delivery for this specific cycle — largely because several `[GOVERNANCE]` commits in this window carried large structural documents (release plan, sprint backlog, qa_evidence consolidation, post-ship closure artefacts) that are inherently verbose relative to a typical single-story code commit. This is consistent with, and gives a second independent data point for, the same overhead concern the Product Value Ratio metric already flags at Alert tier — it does not by itself indicate governance process is "half the cost" of delivery in dollar terms, only that it is at least comparably sized by this proxy.

## 5. Reproducing / Re-Applying

Re-run §3's method against any other cycle by substituting its own start/end commit timestamps (from that cycle's `release_plan.md#published_utc` and `sprint_close.md`/`closure_record.md` dates). No script is checked in for this — the `git log` one-liner in §3 step 1 is short enough that a dedicated script would add more maintenance overhead than it saves for an occasional retrospective check; if this becomes a recurring per-cycle report, promote it to a `scripts/` script at that point (same pattern as `scripts/generate_escalation_response_time_report.py`, ST-18).

## 6. Sign-Off

- Signed off by: Sprint Execution Engine (agent-mediated, FinOps & Resource Architect role — §5.3)
- Date: 2026-09-15
- Comments: Independently re-ran §4's git commands; all figures (39/9,894/2,071 governance; 66/8,671/1,401 delivery; 9 merges) matched exactly. Minor wording gap noted (§3 step 2's delivery-bucket definition didn't literally cover 3 no-ST-tag `[EPIC-xx]` housekeeping commits already included in the 66) — fixed in the same edit as this sign-off.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-15 | ST-19 (EPIC-05, v9.4, BLG-GOV-302): Initial version. Git-history-derived commit/line-volume proxy for governance-overhead vs. delivery session cost, applied retrospectively to `2026-09-09__release-v9.3`. |
