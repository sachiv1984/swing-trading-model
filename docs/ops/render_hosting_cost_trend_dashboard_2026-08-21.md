**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-21
**Story:** ST-26 (BLG-OPS-95, EPIC-05, v9.0)

---

# Render Hosting Cost Trend Dashboard

## 1. Purpose

`BLG-OPS-95`: "Render hosting cost is reviewed monthly ad hoc with no trend visualisation — harder to spot a cost trajectory shift early." The story's own scope calls for "a simple monthly cost-vs-request-volume trend chart, sourced from existing monthly review data."

## 2. Finding: no existing monthly $-cost review data exists in this repository (AC reframed)

Searched the repo for a recurring Render-hosting-dollar-cost review series (the "existing monthly review data" the story's scope assumes): none exists. `docs/ops/cloud_infra_spend_by_epic.md` (ST-23, BLG-OPS-123, v8.4) already established why, for a related story, and the same finding applies here:

> "Render has no native resource-tagging or per-tag cost breakdown... Production services have no git history in this repository — there is no version-controlled record of which EPIC provisioned or resized them. Render's dashboard is the only source of truth for production plan tier and actual dollar spend; this document cannot reproduce that from repo state alone."

The only recurring monthly *cost* review series in this repo is `docs/ops/claude_cost_review_2026-05.md` / `docs/ops/anthropic_api_cost_trend_2026.md` — the Anthropic API spend line, a genuinely separate budget item from Render hosting. There is no equivalent for Render itself.

**Substitute, applied below (same reframe pattern as `cloud_infra_spend_by_epic.md`'s AC-01):** since actual dollar figures aren't repo-derivable, this builds the load-side half of a cost-vs-volume trend — request/endpoint-count growth, which genuinely is git-derivable across real historical commits — cross-referenced against the cost side's one confirmed fact: **the Render plan tier has not changed in this window** (confirmed below), so cost has been flat while load has grown. This tells the same story a $-figure trend chart would (is cost growing in proportion to load, or is there slack/pressure?) without fabricating dollar figures this session cannot verify.

## 3. Load-side trend (4 real historical snapshots, ~90 days)

Endpoint count (`@router.*` in `backend/routers/*.py` + `@app.*` in `backend/main.py`) at 4 real points in git history, sampled at ~30-day intervals:

| Date | Commit | Router endpoints | App-level endpoints | Total |
|------|--------|-------------------|----------------------|-------|
| 2026-05-23 | `ac30e1fa` | 50 | 37 | **87** |
| 2026-06-22 | `cb0bb33f` | 57 | 38 | **95** |
| 2026-07-21 | `68082191` | 81 | 46 | **127** |
| 2026-08-21 | `5f066b11` (today) | 92 | 46 | **138** |

```
Endpoint count trend (proxy for feature/load footprint)

140 |                                                    ● 138
130 |                                          ● 127
120 |
110 |
100 |
 90 |                        ● 95
 80 |         ● 87
    +---------+--------------+--------------+--------------+
      05-23         06-22          07-21          08-21
```

Growth is +58.6% over ~90 days (87 → 138), but — per `render_starter_tier_headroom_reassessment_2026-08-13.md` §4, reconfirmed 8 days later by this cycle's own ST-25 (`render_hosting_tier_review_2026-08-21.md`) — every added endpoint is a stateless, synchronous, on-demand handler, not new background compute. Endpoint *count* growing is not the same signal as *load* growing proportionally; a single-user system's realistic concurrent request volume does not scale 1:1 with how many distinct routes exist.

## 4. Cost-side: confirmed flat in this window

`git log -- render.yaml` shows no plan-tier-affecting commit in the reviewed window (cross-checked in ST-25's own review, same session). Production is Render Starter tier throughout, dashboard-managed (not tracked in `render.yaml`, which only defines the $0/month staging services per `cloud_infra_spend_by_epic.md` §"Resources not defined in this repository"). No tier change, no new paid service added.

## 5. Reading the trend together

Cost: flat (no tier change). Load-proxy: +58.6% endpoint count over ~90 days, but qualitatively unchanged in *kind* (still all synchronous, stateless, on-demand — no new always-on process). This is consistent with, not contradictory to, ST-25's independent Hold recommendation: the load growing is real, but it's growing in a dimension (endpoint count) that doesn't consume idle-time resources on a single-instance Starter dyno, so flat cost alongside growing endpoint count is not itself a red flag.

**If a genuine dollar-cost trend is wanted going forward:** that requires either (a) live Render dashboard/invoice access this sandbox does not have, checked monthly and appended here, or (b) Render exposing billing-by-tag (confirmed unavailable, `cloud_infra_spend_by_epic.md` §"Finding"). Recommend: whoever next has Render dashboard access append one row per month to §3's table with the actual invoiced amount, extending this into a real $-cost trend over time rather than the endpoint-count proxy used for this first pass.

## 6. Sign-off

**FinOps & Resource Architect (agent-mediated, §5.3):** Approved — 2026-08-21. Endpoint-count trend table (87/95/127/138) independently re-derived and matched exactly; no recurring Render $-cost review series confirmed absent; render.yaml/changelog checks re-verified independently. Reframe (load-proxy trend + flat-cost fact, in place of an unavailable dollar-figure trend) judged honest and appropriately labelled throughout, not presented as a cost figure.
