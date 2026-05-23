**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-23
**Amendment ID:** AMD-20260523-01
**Original Cycle:** 2026-05-22__release-v4.0

# Amendment Lessons — AMD-20260523-01

## Amendment Section

| # | Observation | Type | Action |
|---|-------------|------|--------|
| 1 | BLG-BE-19 (Gemini wiring prerequisite) was identified during release planning (noted in cycle_summary.md) but not added to the backlog slice. The release planning engine produced the cycle_summary "Pre-sprint Scope Addition" advisory but did not initiate a slice update at that time. | Process gap | Release Planning engine should add confirmed prerequisite items to the slice at the point they are identified, not defer to a post-publish advisory. Consider adding a STEP to release_planning_prompt.md: "For each 'Pre-sprint Scope Addition' identified, add to slice before publishing." |
| 2 | The starlette CVE was caught by the pre-sprint pip-audit scan (STEP -1 advisory 6 in sprint_planning_prompt.md) — exactly the intended mechanism. Process worked as designed. | Positive — no action | None |
| 3 | Amendment cycle was straightforward: 2 XS/S additions, both ratified in the same session. Total overhead was minimal (~15 min). The process is proportionate for small scope additions. | Positive — no action | None |

## Process Assessment

**Was the amendment necessary?** Yes — BLG-BE-19 was a confirmed hard-blocker for EPIC-03 execution; the starlette CVE required a medium-severity security fix.

**Was the process proportionate?** Yes — both additions are XS/S effort; the amendment was straightforward; no capacity ceiling exceeded (BLG-BE-19 effort was implicit in original EPIC-03 estimates).

**Earlier detection possible?** Yes for BLG-BE-19: the release planning engine identified this prerequisite but didn't add it to the slice. Earlier detection could have avoided the amendment cycle entirely.
