**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (ST-53, EPIC-05, v9.2, BLG-OPS-106 — threshold review recorded)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Cost-Threshold Alert Value Review

## 1. Scope

Reviews the live `AI_DAILY_COST_THRESHOLD` alert value (`backend/config.py`, default `$1.00`/day, used by `POST /ai/check-daily-cost` → `check_and_alert_daily_cost()`). §13 pre-check confirmed not applicable (per `sprint_backlog.md` ST-53 notes) — this is a cost-monitoring configuration review, not a strategy/system-boundary decision.

## 2. Current Value and Prior Review

- **Live threshold:** `$1.00`/day (config default; overridable via `AI_DAILY_COST_THRESHOLD` on Render).
- A related but distinct **$5.00/month "upgrade review trigger"** figure exists in `gemini_cost_tracking.md` v1.2 (2026-05-27) and `docs/ops/anthropic_api_cost_trend_2026.md` — a separate advisory figure for reviewing model-tier upgrades, not the live daily alert.
- Last reviewed against actual spend at v5.6 (`docs/ops/anthropic_api_cost_trend_2026.md`, 2026-06-16): both figures found "well below" actual spend (~$0.05–$0.15/month observed vs. $1.00/day ≈ up to ~$30/month ceiling — over 100× margin; $5.00/month ceiling — 33–100× margin).

## 3. What Changed Since the Last Review

The AI-invoking endpoint surface has grown from what the v5.6 review covered. Confirmed via `backend/routers/` + `backend/services/` (this story, 2026-09-08) — **6 AI-invoking endpoints now exist**, all sharing the same `claude_audit_log`/threshold mechanism:

1. `POST /ai/journal-summary`
2. `POST /ai/daily-briefing`
3. `POST /ai/chat`
4. `POST /trade-plans/generate-plan`
5. `POST /trade-plans/{plan_id}/generate-thesis`
6. `POST /trades/{trade_id}/debrief` (added v8.9, `BLG-FEAT-90` — automated AI post-trade debrief; not part of the v5.6-era review, which covered thesis generation + daily cost check only)

More AI surface area is more opportunity for a bug (an accidental loop, an unbounded retry, a missing rate limit) to drive real spend growth — the threshold's job is specifically to catch that class of failure, not to track normal usage drift (that's now `check_cost_anomaly()`'s job, added this same story batch by ST-54/`BLG-OPS-112`, which flags *relative* spikes against a rolling baseline rather than a fixed ceiling).

## 4. Assessment

**Threshold confirmed unchanged at $1.00/day.** Rationale:

- No live query access from this environment (same constraint as `anthropic_api_cost_trend_2026.md` §3 — production DB is Render-side only) to pull a fresh actual-spend figure for direct comparison; using the last confirmed reading (~$0.05–$0.15/month, v5.6) as the working baseline is reasonable given usage pattern drivers (thesis generation is per-trade-plan, post-trade debrief is per-closed-trade — both gated by genuinely low trade volume, not user-triggered-on-demand at scale) have not structurally changed, only the endpoint count.
- $1.00/day is intentionally a **backstop ceiling against runaway/bug-driven cost**, not a sensitivity-tuned early-warning detector — that role is now explicitly covered by ST-54's `check_cost_anomaly()` (fires on a *relative* spike, e.g. 3× a rolling baseline, regardless of absolute dollar level). The two are complementary by design: the fixed ceiling catches "spend went genuinely large", the relative check catches "spend jumped abnormally even while still small in absolute terms" — lowering the fixed ceiling to be more sensitive would duplicate what the relative check now does better, at the cost of more false-positive noise on the fixed alert.
- Adding a 6th AI-invoking endpoint does not, by itself, argue for a lower ceiling — each endpoint call still costs roughly the same order of magnitude per invocation (a few tenths of a cent, per the existing token-cost breakdown in `anthropic_api_cost_trend_2026.md` §2), so 3× the endpoint count at similar per-call cost and low volume is still nowhere near the ceiling.

**Recommendation:** keep $1.00/day as-is. Re-review at the next `run audit` cycle or if a real production spend figure becomes available (whichever comes first), rather than on a fixed calendar cadence — this mirrors the existing `anthropic_api_cost_trend_2026.md` review pattern.

## 5. Sign-Off

**FinOps & Resource Architect:** Confirmed — threshold reviewed against the current 6-endpoint AI surface, no change warranted, rationale documented (fixed-ceiling vs. relative-anomaly-check division of labour with ST-54). 2026-09-08.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-09-08 | 1.0 | Threshold review recorded (ST-53, EPIC-05, v9.2, BLG-OPS-106). |
