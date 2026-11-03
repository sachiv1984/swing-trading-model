**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-03
**Window:** IW-20261103-01

# Idea Intake Summary — IW-20261103-01

**Reduced-roster disclosure (§4.1):** participating roles 2 of 23 eligible — Head of UX & Design, Frontend Specifications & UX Documentation Owner. Reason: this rebalance is focused on the Head of UX & Design website review held in session on 2026-11-03 (first-principles target vs current site, IA verdict "modify substantially", 26-item fix list), which the user asked to be written to the roadmap as its focus. Authorised by the Product Owner (the user, in session), 2026-11-03. Preceding window: `IW-20261016-01` — full roster. Roster rule (§2.1 step 2a): both participating roles are user-facing.

## Window Status: Closed

Opened: 2026-11-03T12:59:37Z
Closed: 2026-11-03T13:01:33Z

*(Real shell timestamps. The surface reads behind these submissions were done earlier in the same session, during the review itself.)*

Invoked inline as STEP -1.6 of `run roadmap --reason "scheduled"` (`2026-11-03__scheduled`). The register held 0 rows with `Status: Submitted`/`Parked-cycle-<n>`, below the 20-item threshold. No standalone window ran beforehand.

**Stale-idea horizon check (STEP -0.5):** 0 rows at `Parked-cycle-2`, so no advisory.

**Parked queue pre-check (§2.0 steps 1–4):** no `Parked-cycle-<n>` rows exist, so there was nothing to resubmit.

**Backlog scope overlap check (§2.0 step 5):** every topic was grepped against `claude/backlog/backlog.md` and `backlog_archive.md`. No topic was dropped. Partial overlaps are recorded in each submission: `BLG-FE-54`/`58`/`62` (pre-entry gateway on the planned path; ideas 01 and 04 refine it), `BLG-FE-224`/`242` (per-element light-theme fixes; frontend-specs 03 refines them), `BLG-BE-199` (backend FX validation; frontend-specs 02 is the UI default), `BLG-BE-183` (grace numbering; a symptom idea 05 removes). The v8.5 nav exploration (`st15_nav_bar_redesign_exploration.md`) assessed the sidebar pattern only, not grouping; idea 03 keeps the pattern.

**Codebase overlap check (§2.0 step 6):** every mechanism-naming topic was confirmed absent or defective in `src/` at `ab7fbf23` (file and line cited in each submission).

**Method note:** submissions are engine-generated under agent perspectives from the in-session review, the same convention every prior window used. Full template fields are in `claude/cycles/2026-11-03__scheduled/cycle_record.md` `### Submission Details`.

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|-----------------|--------------------|-------|
| Head of UX & Design | 7 | 0 | 7 |
| Frontend Specifications & UX Documentation Owner | 4 | 0 | 4 |
| **Total** | **11** | **0** | **11** |

## Agents Without Minimum Submissions

None — both participating roles met the minimum. The other 21 roles were not opened (reduced roster); per §4.1 that is not a §2.3 shortfall.

## Ideas Available for Roadmap STEP 4

| Idea ID | Agent | Title | Recommendation | Status |
|---------|-------|-------|----------------|--------|
| IDEA-head-of-ux-20261103-01 | Head of UX & Design | Run the pre-entry checks on every route into Trade Entry | Now | Submitted |
| IDEA-head-of-ux-20261103-02 | Head of UX & Design | Turn the Dashboard into a prioritised "Today" action list | Now | Submitted |
| IDEA-head-of-ux-20261103-03 | Head of UX & Design | Re-group navigation around the trader's jobs and fix wayfinding | Now | Submitted |
| IDEA-head-of-ux-20261103-04 | Head of UX & Design | One flow from signal to entered trade | Now | Submitted |
| IDEA-head-of-ux-20261103-05 | Head of UX & Design | One place per concept: grace period, journal, performance | Soon | Submitted |
| IDEA-head-of-ux-20261103-06 | Head of UX & Design | Decision-first Positions table, with a phone layout | Soon | Submitted |
| IDEA-head-of-ux-20261103-07 | Head of UX & Design | First-principles UX re-review when the programme completes | Now (final, sequenced) | Submitted |
| IDEA-frontend-specs-20261103-01 | Frontend Specifications & UX Documentation Owner | Use one name per concept across sidebar, headings and command palette, and fix the inverted FX label | Now | Submitted |
| IDEA-frontend-specs-20261103-02 | Frontend Specifications & UX Documentation Owner | Pre-fill Trade Entry's FX rate from the live rate, not 1.27 | Now | Submitted |
| IDEA-frontend-specs-20261103-03 | Frontend Specifications & UX Documentation Owner | Semantic colour tokens so the light theme stops breaking piecemeal | Soon | Submitted |
| IDEA-frontend-specs-20261103-04 | Frontend Specifications & UX Documentation Owner | Fix three small chrome defects: version label, What's New heading, sidebar height | Soon | Submitted |

## Parked Ideas Carried Forward (Not Resubmitted)

None.

## Notes

Build-and-ship candidates (§2.1 step 2a): 10 — `IDEA-head-of-ux-20261103-01` to `-06` (Head of UX & Design), `IDEA-frontend-specs-20261103-01` to `-04` (Frontend Specifications & UX Documentation Owner). User-facing roles with none: None. `IDEA-head-of-ux-20261103-07` is review-shaped by design (the user's requested post-programme re-review).

The 11 ideas cover the review's 26 proposed backlog items: ideas 01 (item 1), 02 (12–13), 03 (4–11), 04 (14–15 and the `BLG-FE-54` re-scope), 05 (16–19), 06 (20–23), 07 (the re-review); frontend-specs 01 (3, 7), 02 (2), 03 (24–25), 04 (26).
